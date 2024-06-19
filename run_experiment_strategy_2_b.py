import logging
import os
import warnings
import json
from preprocessing.config import (
    PARAMS,
    PATH_DAT_FILES,
    PESOS_PROMEDIO,
    path_parte_diario,
    path_scrapped_prices_df,
    intervalos_madurez,
)
from preprocessing.generate_LP_inputs import build_LP_inputs
from preprocessing.data_prep import delete_log_files

warnings.filterwarnings("ignore")

log = logging.getLogger("logger")
log.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(message)s")
fh = logging.FileHandler("test.log", mode="w", encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
log.addHandler(ch)

delete_log_files("lp_logs")

from datetime import datetime
from dateutil.relativedelta import relativedelta

# Original dictionary
exp_grid_base = {
    '2019_periods': {'fecha_inicio': '18/01/2019', 'periodos_modelo': 24, 'fecha_fin_ejercicio': '08/01/2021', 'fix_prices': False, "mantain_c3_stock": 1},
    '2019_periods_fix_prices': {'fecha_inicio': '18/01/2019', 'periodos_modelo': 24, 'fecha_fin_ejercicio': '08/01/2021', 'fix_prices': True, "mantain_c3_stock": 1},
}

# Expansion parameters
start_periods = 24
end_periods = 120
step = 12

# Generate extra keys
exp_grid = {}
for key, value in exp_grid_base.items():
    for i in range(start_periods, end_periods + step , step):
        new_key = f"{key}{i}_periods"
        new_value = value.copy()
        new_value['periodos_modelo'] = i
        new_value['fecha_fin_ejercicio'] = (datetime.strptime('18/01/2019', '%d/%m/%Y') + relativedelta(months=i)).strftime('%d/%m/%Y')
        exp_grid[new_key] = new_value



for experiment, items in exp_grid.items():
    PARAMS["fecha_inicio"] = items["fecha_inicio"]
    PARAMS["periodos_modelo"] = items["periodos_modelo"]
    PARAMS["fecha_fin_ejercicio"] = items["fecha_fin_ejercicio"]
    PARAMS["mantain_c3_stock"] = items["mantain_c3_stock"]

    if experiment == '2019_24periods_p_index_70':
        PARAMS["pregnancy_index"] = 0.7
    
    if experiment == '2019_24periods_fix_costs_100':
        PARAMS["fix_cost_sales"] = 100

 # generate business variant run
    #business_excercise, df_ventas, df_final_stock_value, PARAMS['c3_stock_at_end'] = business_variant(
    #    PARAMS, PESOS_PROMEDIO, path_parte_diario, path_scrapped_prices_df
    #)
    #exp_grid[experiment]["business_results"] = business_excercise
    #df_final_stock_value.to_csv(f"lp_logs/df_final_stock_value_{experiment}.csv")

    #log.info(f"{PARAMS['c3_stock_at_end']}")

    # generate LP inputs
    (
        exp_grid[experiment]["lp_stock_history_cost"],
        df_precios,
    ) = build_LP_inputs(
        PARAMS,
        PATH_DAT_FILES,
        path_scrapped_prices_df,
        PESOS_PROMEDIO,
        path_parte_diario,
        intervalos_madurez,
        COST_TEST=False,
        INITIAL_STOCK_TEST=False,
        fix_prices=items["fix_prices"],
    )

    #run LP heuristic based on business requirements
    os.system(
       f"sudo docker exec scipTeach2 scip -f model_strategy_2eng.zpl -l lp_logs/{experiment}_h.log"
    )

    #run LP without heuristic requirements
    os.system(
       f"sudo docker exec scipTeach2 scip -f model_strategy_1eng.zpl -l lp_logs/{experiment}.log"
    )

    # ! required by explore_results.ipynb
    # pfix = items['fix_prices']
    # df_precios.to_csv(f"lp_logs/df_precios_fix{pfix}.csv")

    


log.info("saving experiment results at lp_logs/experiments_results.json")
with open("lp_logs/experiments_results.json", "w") as json_file:
    json.dump(exp_grid, json_file)

log.info("saving experiment params at lp_logs/params.json")
with open("lp_logs/params.json", "w") as json_file:
    json.dump(PARAMS, json_file)
