import logging
import pandas as pd

from preprocessing.data_prep import (
    clear_model_inputs,
    write_params_file,
    costs_to_dat_test,
    get_interplolator,
    get_precios_scrapped,
    prices_to_usd_b,
    precios_scrapped_to_dat,
    get_stock_inicial_test,
    get_stock_inicial_from_parte_diario,
    get_precios_del_periodo,
    quote_stock,
    costs_to_dat_realistic,
    apply_contant_prices,
    apply_discount_factor_to_prices,
)

log = logging.getLogger("logger")


def build_LP_inputs(
    PARAMS,
    PATH_DAT_FILES,
    path_scrapped_prices_df,
    PESOS_PROMEDIO,
    path_parte_diario,
    intervalos_madurez,
    COST_TEST=False,
    INITIAL_STOCK_TEST=False,
    fix_prices=False,
    disc_fact=None,
):
    log.info(f"cleaning .dat files from {PATH_DAT_FILES}")
    clear_model_inputs(PATH_DAT_FILES)

    ### COSTS ###

    if COST_TEST:
        log.info("building costs.dat test mode ON")
        costs_to_dat_test(
            PATH_DAT_FILES,
            PARAMS["periodos_modelo"],
            PARAMS["meses_max_animales"],
            PARAMS["clases"],
        )
    else:
        log.info("building costs.dat realistic")
        costs_interpolator = get_interplolator(PARAMS, output_plot_path='interpolator_costs.png')
        costs_to_dat_realistic(costs_interpolator, PATH_DAT_FILES, PARAMS)

    ### PRICES ###
    log.info("getting prices from historical scrapped data")
    df_precios = get_precios_scrapped(
        fecha_inicio=PARAMS["fecha_inicio"], input=path_scrapped_prices_df
    )

    log.info("prices to USD B")
    df_precios = prices_to_usd_b(
        df_prices_ars=df_precios,
        usd_b_path="data/usd_b_fill.csv",
        cols_to_normalize=[
            "VAQUILLONAS270",
            "VAQUILLONAS391",
            "NOVILLITOS300",
            "NOVILLITOS391",
        ],
    )

    df_precios = pd.read_csv('data/df_precios_usd_w_forecast203301.csv')
    df_precios['PERIODO_INICIO'] = pd.to_datetime(df_precios['PERIODO_INICIO'])
    if fix_prices:
        df_precios = apply_contant_prices(df_precios)

    # Apply discount factor if specified
    if disc_fact is not None:
        log.info(f"Applying discount factor of {disc_fact}% to prices")
        df_precios = apply_discount_factor_to_prices(
            df_precios,
            disc_fact,
            PARAMS["fecha_inicio"]
        )

    log.info("writing prices.dat file")
    precios_scrapped_to_dat(
        df_precios,
        PARAMS,
        PATH_DAT_FILES,
        PESOS_PROMEDIO,
    )

    ### INITIAL STOCK ###

    if INITIAL_STOCK_TEST:
        log.info("building stock_inicial.dat test mode ON")
        get_stock_inicial_test(PARAMS, PATH_DAT_FILES["stock_inicial"])

    else:
        log.info("building stock_inicial.dat realistic")
        initial_stock_row = get_stock_inicial_from_parte_diario(
            PARAMS,
            PARAMS["fecha_inicio"],
            PARAMS["clases"],
            PARAMS["meses_max_animales"],
            parte_diario_path=path_parte_diario,
            output=PATH_DAT_FILES["stock_inicial"],
            intervalos=intervalos_madurez,
        )
    log.info(
        """get costs from stock before the model starts, 
        so we can substract to LP revenue so its comparable to 
        business which sells and pays cost for all its stock"""
    )
    # get initial stock cost only (no income)
    prices_initial_period = get_precios_del_periodo(
        pd.to_datetime(PARAMS["fecha_inicio"], format="%d/%m/%Y"), df_precios
    ).to_dict()
    initial_stock_cost = quote_stock(
        prices_initial_period, initial_stock_row, PESOS_PROMEDIO, costs_interpolator, PARAMS
    )["cost"].sum()

    log.info("creating parameters.dat file")

    if not PARAMS.get('virtual_ventas_max_por_mes'):
        PARAMS['virtual_ventas_max_por_mes']  = int(initial_stock_row['TOTAL'].values[0].replace(',','')) * PARAMS['virtual_venta_max_mult']
    
    
    write_params_file(PATH_DAT_FILES, PARAMS)

    log.info(f"MODEL initial stock cost: {initial_stock_cost}")

    return initial_stock_cost, df_precios
