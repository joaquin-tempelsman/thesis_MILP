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
exp_grid = {
    # # var prices
    '2019_24periods' : {'fecha_inicio': '18/01/2019', 'periodos_modelo': 24, 'fecha_fin_ejercicio': '08/01/2021', 'fix_prices': False, "mantain_c3_stock": 1},
    'm2019_24periods' : {'fecha_inicio': '07/06/2019', 'periodos_modelo': 24, 'fecha_fin_ejercicio': '03/06/2021', 'fix_prices': False, "mantain_c3_stock": 1},
    '2020_24periods' : {'fecha_inicio': '03/01/2020', 'periodos_modelo': 24, 'fecha_fin_ejercicio': '06/01/2022', 'fix_prices': False, "mantain_c3_stock": 1},
    '2019_36periods' : {'fecha_inicio': '18/01/2019', 'periodos_modelo': 36, 'fecha_fin_ejercicio': '06/01/2022', 'fix_prices': False, "mantain_c3_stock": 1},
    '2019_42periods' : {'fecha_inicio': '18/01/2019', 'periodos_modelo': 42, 'fecha_fin_ejercicio': '02/06/2022', 'fix_prices': False, "mantain_c3_stock": 1},
    '2019_48periods' : {'fecha_inicio': '18/01/2019', 'periodos_modelo': 48, 'fecha_fin_ejercicio': '05/01/2023', 'fix_prices': False, "mantain_c3_stock": 1},
    
    # # fix prices
    '2019_24periods_fix_prices' : {'fecha_inicio': '18/01/2019', 'periodos_modelo': 24, 'fecha_fin_ejercicio': '08/01/2021', 'fix_prices': True, "mantain_c3_stock": 1},
    'm2019_24periods_fix_prices' : {'fecha_inicio': '07/06/2019', 'periodos_modelo': 24, 'fecha_fin_ejercicio': '03/06/2021', 'fix_prices': True, "mantain_c3_stock": 1},
    '2020_24periods_fix_prices' : {'fecha_inicio': '03/01/2020', 'periodos_modelo': 24, 'fecha_fin_ejercicio': '06/01/2022', 'fix_prices': True, "mantain_c3_stock": 1},
    '2019_36periods_fix_prices' : {'fecha_inicio': '18/01/2019', 'periodos_modelo': 36, 'fecha_fin_ejercicio': '06/01/2022', 'fix_prices': True, "mantain_c3_stock": 1},
    '2019_42periods_fix_prices' : {'fecha_inicio': '18/01/2019', 'periodos_modelo': 42, 'fecha_fin_ejercicio': '02/06/2022', 'fix_prices': True, "mantain_c3_stock": 1},
    '2019_48periods_fix_prices' : {'fecha_inicio': '18/01/2019', 'periodos_modelo': 48, 'fecha_fin_ejercicio': '05/01/2023', 'fix_prices': True, "mantain_c3_stock": 1},

    # # forcasted prices, fix and var prices
    '2019_120periods_fcst' : {'fecha_inicio': '18/01/2019', 'periodos_modelo': 120, 'fecha_fin_ejercicio': '08/01/2021', 'fix_prices': False, "mantain_c3_stock": 1},
    '2019_120periods_fix_prices_fcst' : {'fecha_inicio': '18/01/2019', 'periodos_modelo': 120, 'fecha_fin_ejercicio': '08/01/2021', 'fix_prices': True, "mantain_c3_stock": 1},
    '2023_24periods_fcst': {'fecha_inicio': '05/01/2023', 'periodos_modelo': 24, 'fecha_fin_ejercicio': '05/01/2025', 'fix_prices': False, "mantain_c3_stock": 1},
    '2023_48periods_fcst': {'fecha_inicio': '05/01/2023', 'periodos_modelo': 48, 'fecha_fin_ejercicio': '05/01/2027', 'fix_prices': False, "mantain_c3_stock": 1},
    '2023_72periods_fcst': {'fecha_inicio': '05/01/2023', 'periodos_modelo': 72, 'fecha_fin_ejercicio': '05/01/2029', 'fix_prices': False, "mantain_c3_stock": 1},

    # changes in business parameters
    '2019_24periods_p_index_70' : {'fecha_inicio': '18/01/2019', 'periodos_modelo': 24, 'fecha_fin_ejercicio': '08/01/2021', 'fix_prices': False, "mantain_c3_stock": 1},
    '2019_24periods_fix_sales_costs_100' : {'fecha_inicio': '18/01/2019', 'periodos_modelo': 24, 'fecha_fin_ejercicio': '08/01/2021', 'fix_prices': False, "mantain_c3_stock": 1},

    # discount factor experiments
    '2019_120periods_fcst_disc_fact_0.5perc': {'fecha_inicio': '18/01/2019', 'periodos_modelo': 120, 'fecha_fin_ejercicio': '08/01/2021', 'fix_prices': False, "mantain_c3_stock": 1, 'disc_fact': 0.5},
    '2019_120periods_fcst_disc_fact_1perc': {'fecha_inicio': '18/01/2019', 'periodos_modelo': 120, 'fecha_fin_ejercicio': '08/01/2021', 'fix_prices': False, "mantain_c3_stock": 1, 'disc_fact': 1.0},
    '2019_24periods_disc_fact_0.5perc': {'fecha_inicio': '18/01/2019', 'periodos_modelo': 24, 'fecha_fin_ejercicio': '08/01/2021', 'fix_prices': False, "mantain_c3_stock": 1, 'disc_fact': 0.5},
    '2019_24periods_disc_fact_1perc': {'fecha_inicio': '18/01/2019', 'periodos_modelo': 24, 'fecha_fin_ejercicio': '08/01/2021', 'fix_prices': False, "mantain_c3_stock": 1, 'disc_fact': 1.0},
}

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
    # Extract discount factor if present in experiment config
    disc_fact = items.get("disc_fact", None)

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
        disc_fact=disc_fact,
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
