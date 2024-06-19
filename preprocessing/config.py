SCRAMBLE_NUMS = False
SCRAMBLE_MODIF = 0.5

version = "0.09"
clases = 3
meses_max_animales = 12 * 10  # 10 años, impacta en reproductoras
virtual_venta_max_mult = 3 #multiplicador para el techo virtual maximo, stock inicial total * virtual_venta_max_mult
ventas_min_por_mes = 10
sell_c1_c2_before = 37
path_parte_diario = "data/datos experimento tesis  - parte_diario completo.csv"
path_scrapped_prices_df = "data/scrapping_df3 - scrapping_df3.csv"

VENTA_DESTETE = [6, 7, 8]
VENTA_NOVILLO_VAQUILLONA = [16, 17, 18]
VENTA_PESADOS = [30, 31, 32, 33, 34, 35, 36]

fix_cost_sales = 10
pregnancy_index = 0.86

peso_prom_destete = 164
peso_prom_vaquillonas = 314
peso_prom_novillitos = 367
peso_prom_vaquillonas_pesados = 433
peso_prom_novillos_pesados = 438

usd_18_04_2023 = 397.2

# this points are used to build the function, then will be replaced for info
# in dictionary costos_meses_usd_c1_c2, that has the actual function values
# that are slightly different, and used for both variants.
costos_meses_usd_c1_c2_pre_norm = {
    0: (33000 /2) / usd_18_04_2023,
    6: 33000 / usd_18_04_2023,
    17: 94000 / usd_18_04_2023,
    21: 128000 / usd_18_04_2023,
}

costos_meses_usd_c1_c2 = {}

# extra percentage cost from c2 to c1
c1_over_cost = 0.1

c3_costs = {
    'monthly_cost_over_12': (1836 / usd_18_04_2023),
    }

    


costos_c3_mes = 12  # cual es el costo q se toma para la c3 respecto de la c2
c1_c2_over_21 = 10  # pasados los 21, para clase 1 y 2, el costo mensual es el equivalente a los 10 meses
                    # dado que ya se ha pagado el primer engorde para el modelo, se incluye un sobre costo leve para el segundo engorde que llega hasta 30
                    # en adelante donde se puede vender hasta los 36
multiplicador_destete = 1.2  # precio venta 20% mas que el precio del novillito
multiplicador_c3 = 0.5  # precio de venta 50% de VAQUILLONAS270
venta_c3_from = 24 # se puede vender c3 desde los 24 en adelante

intervalos_madurez = {
    "VACAS": [36, 96, 3],
    "VAQ 1-2": [12, 17, 2],
    "VAQ. 1-2 Servicio": [12, 36, 3],
    "VAQ. 2-3": [24, 48, 3],
    "NOVILLOS": [19, 24, 1],
    "NOVILLITOS": [12, 18, 1],
    "TERNEROS": [6, 11, 1],
    "TERNERAS": [6, 11, 2],
    "OREJANO_MACHOS": [0, 5, 1],
    "OREJANO_HEMBRAS": [0, 5, 2],
}

intervalos_madurez = {
    "VACAS": [60, 61, 3],
    "VAQ 1-2": [17, 18, 2],
    "VAQ. 1-2 Servicio": [30, 30, 3],
    "VAQ. 2-3": [36, 37, 3],
    "NOVILLOS": [21, 22, 1],
    "NOVILLITOS": [17, 18, 1],
    "TERNEROS": [6, 7, 1],
    "TERNERAS": [6, 7, 2],
    "OREJANO_MACHOS": [6, 7, 1],
    "OREJANO_HEMBRAS": [6, 7, 2],
}

SALES_PERIODS = {
    "venta_destete": VENTA_DESTETE,
    "venta_novillo_vaquillona": VENTA_NOVILLO_VAQUILLONA,
    "venta_pesados": VENTA_PESADOS,
}

PESOS_PROMEDIO = {
    "peso_prom_destete": peso_prom_destete,
    "peso_prom_vaquillonas": peso_prom_vaquillonas,
    "peso_prom_novillitos": peso_prom_novillitos,
    "peso_prom_vaquillonas_pesados": peso_prom_vaquillonas_pesados,
    "peso_prom_novillos_pesados": peso_prom_novillos_pesados,
}

PARAMS = {
    "version": version,
    "meses_max_animales": meses_max_animales,
    "clases": clases,
    "ventas_min_por_mes": ventas_min_por_mes,
    "virtual_venta_max_mult" :virtual_venta_max_mult,
    "costos_meses_usd_c1_c2_pre_norm": costos_meses_usd_c1_c2_pre_norm,
    "costos_meses_usd_c1_c2": costos_meses_usd_c1_c2,
    "costos_c3": costos_c3_mes,
    "c1_c2_over_21": c1_c2_over_21,
    "sell_c1_c2_before": sell_c1_c2_before,
    "multiplicador_destete": multiplicador_destete,
    "multiplicador_c3": multiplicador_c3,
    "SALES_PERIODS": SALES_PERIODS,
    "PESOS_PROMEDIO": PESOS_PROMEDIO,
    "venta_c3_from": venta_c3_from,
    "usd_18_04_2023": usd_18_04_2023,
    "c3_costs": c3_costs,
    "c1_over_cost": c1_over_cost,
    "fix_cost_sales": fix_cost_sales,
    "pregnancy_index": pregnancy_index,
    "SCRAMBLE_NUMS": SCRAMBLE_NUMS,
    "SCRAMBLE_MODIF": SCRAMBLE_MODIF,
}

# ! WARNING, this will be deleted and regenerated when running build_model_inputs.py
# ! dont add other files here
PATH_DAT_FILES = {
    "parameters": "model_inputs/parameters.dat",
    "agosto_si": "model_inputs/august.dat",
    "agosto_no": "model_inputs/non_august.dat",
    "costos": "model_inputs/costs.dat",
    "precios": "model_inputs/prices.dat",
    "stock_inicial": "model_inputs/initial_stock.dat",
}

if SCRAMBLE_NUMS:
    PARAMS['costos_meses_usd_c1_c2_pre_norm'][0] = PARAMS['costos_meses_usd_c1_c2_pre_norm'][0] + PARAMS['costos_meses_usd_c1_c2_pre_norm'][0] * PARAMS['SCRAMBLE_MODIF']
    PARAMS['costos_meses_usd_c1_c2_pre_norm'][6] = PARAMS['costos_meses_usd_c1_c2_pre_norm'][6] + PARAMS['costos_meses_usd_c1_c2_pre_norm'][6] * PARAMS['SCRAMBLE_MODIF']
    PARAMS['costos_meses_usd_c1_c2_pre_norm'][17] = PARAMS['costos_meses_usd_c1_c2_pre_norm'][17] + PARAMS['costos_meses_usd_c1_c2_pre_norm'][17] * PARAMS['SCRAMBLE_MODIF']
    PARAMS['costos_meses_usd_c1_c2_pre_norm'][21] = PARAMS['costos_meses_usd_c1_c2_pre_norm'][21] + PARAMS['costos_meses_usd_c1_c2_pre_norm'][21] * PARAMS['SCRAMBLE_MODIF']
    PARAMS['c3_costs']['monthly_cost_over_12'] = PARAMS['c3_costs']['monthly_cost_over_12'] + PARAMS['c3_costs']['monthly_cost_over_12'] * PARAMS['SCRAMBLE_MODIF']
    PARAMS['c1_over_cost'] = PARAMS['c1_over_cost'] + PARAMS['c1_over_cost'] * PARAMS['SCRAMBLE_MODIF']
