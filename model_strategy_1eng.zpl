#####----------- PARAMETERS -----------######

# Duration of the exercise in months
param max_periods := read "model_inputs/parameters.dat" as "2n" skip 1 use 1;

# Maximum allowed age of animals
param animal_max_age := read "model_inputs/parameters.dat" as "2n" skip 2 use 1;

# Maximum sales per month (virtual_venta_max)
param max_sell_c1_c2 := read "model_inputs/parameters.dat" as "2n" skip 3 use 1;

# Minimum sales per month
param min_sell_c1_c2 := read "model_inputs/parameters.dat" as "2n" skip 4 use 1;

# Sell class 1 and class 2 before a particular month
param sell_c1_c2_before := read "model_inputs/parameters.dat" as "2n" skip 5 use 1;

# Demand initial stock of class 3 to be equal to final stock of class 3
param MANTAIN_C3_STOCK := read "model_inputs/parameters.dat" as "2n" skip 6 use 1;

# Fix selling cost per period for class 1  2
param SELL_FIX_COST_c1c2 := read "model_inputs/parameters.dat" as "2n" skip 7 use 1;

# pregnancy index as how many births per year class 3 generates
param preg_index := read "model_inputs/parameters.dat" as "2n" skip 8 use 1;

# Possible months with births
set august_periods := { read "model_inputs/august.dat" as "<1n>"};

# Months with no births
set not_august_periods := { read "model_inputs/non_august.dat" as "<1n>"};

# Set of periods
set T := { 1 .. max_periods };

# max month allowed for animals
set E := { -1 .. animal_max_age };

# Animal classes
set C := { 1, 2, 3 };

# Cost of animals in each T, E, C
param cost[T*E*C] := read "model_inputs/costs.dat" as "<1n,2n,3n> 4n";

# Price of animals in each period for each gender
param price[T*E*C] := read "model_inputs/prices.dat" as "<1n,2n,3n> 4n";

# Initial stock for period 0
param initial_stock[E*C] := read "model_inputs/initial_stock.dat" as "<1n,2n> 3n";

#####----------- DEFINITION OF VARIABLES -----------#####

# Stock variable
var x[(T union {0}) * E * C] >= 0; 

# Sales variable
var y[(T union {0}) * E * C] >= 0; 

# Transfer variable from class 2 to class 3
var w[(T union {0}) * E] >= 0; 

# Birth variable
var n[(T union {0}) * C] >= 0; 

# Binary sales variable, v[t] equals 1 if there are sales in period t
var s[T] binary;

#####----------- OBJECTIVE FUNCTION -----------#####

# Objective function
maximize fobj: sum <t,e,c> in T*E*C: (y[t,e,c] * price[t,e,c] - x[t,e,c] * cost[t,e,c] - s[t] * SELL_FIX_COST_c1c2);

#####----------- CONSTRAINTS -----------#####

# Conservation of flow equations. Linking the stock and sales variables

subto r_flow_class_1: forall <t,e> in T*E with e > 0:
    x[t,e,1] == x[t-1,e-1,1] - y[t-1,e-1,1];

subto r_flow_class_2: forall <t,e> in T*E with e > 0:
    x[t,e,2] == x[t-1,e-1,2] - y[t-1,e-1,2] - w[t-1,e-1];

subto r_flow_class_3: forall <t,e> in T*E with e >= 0:
    x[t,e,3] == x[t-1,e-1,3] - y[t-1,e-1,3] + w[t-1,e-1];

########## - SALES - ##########

# Minimum sales if there are sales, or zero if s[t] is 0
subto r_minimum_sales: forall <t> in T:
    sum <e,c> in E*C with c !=3: y[t,e,c] >= min_sell_c1_c2 * s[t];

# Maximum sales if there are sales, or zero if s[t] is 0
subto r_maximum_sales: forall <t> in T:
    sum <e,c> in E*C with c != 3: y[t,e,c] <= max_sell_c1_c2 * s[t];

# Sales constraint, I cannot sell more than what is available
subto r_control_sales: forall <t,e,c> in T*E*C:
    y[t,e,c] <= x[t,e,c];

subto r_no_zero_price_sales: forall <t,e,c> in T*E*C:
    if (price[t,e,c] <= 0) then y[t,e,c] == 0 end;

subto no_sales_final_period: forall <e,c> in E*C:
    y[max_periods,e,c] == 0;

########## - STOCK - ##########

subto r_initial_stock_set: forall <e,c> in E*C:
    x[0,e,c] == initial_stock[e,c];

# No stock in negative age. Otherwise, this case would be outside the flow constraint
subto r_non_negative_age_stock: forall <t,c> in T*C:
    x[t,-1,c] == 0;

# require to sustain or increase c3 stock at the end of the period
subto r_maintain_c3_bigger_or_equal_end_of_period_all:
    if MANTAIN_C3_STOCK == 1 then
        sum <e> in E: x[0, e, 3] <= sum <e> in E: x[max_periods, e, 3]
    end;

#same as before but limit it to younger subset
subto r_maintain_c3_bigger_or_equal_end_of_period_young:
    if MANTAIN_C3_STOCK == 1 then
        sum <e> in E with e < 30: x[0, e, 3] <= sum <e> in E: x[max_periods, e, 3]
    end;

######## - TRANSFERS - #######

# Limit the transfer variable W not to exceed the difference between stock and sales.
subto r_control_transfers: forall <t,e> in T*E:
    w[t,e] <= x[t,e,2] - y[t,e,2];

# No transfers in the initial period
subto r_no_transfers_initial_period: forall <e> in E:
    w[0,e] == 0;

# Transfer to Class 3, strictly at 11 months
subto r_transfers_at_month: forall <t,e> in T*E with e !=11:
    w[t,e] == 0;

####### - BIRTHS - #######

# No births in the initial period
subto r_no_births_initial_period: forall <c> in C:
    n[0,c] == 0;

# c1 born for each class 3 that is older than 2 years
subto r_births_c1: forall <t> in august_periods:
    n[t,1] == sum <e> in E with e >= 24: x[t,e,3] * preg_index / 2;

# c2 born for each class 3 that is older than 2 years
subto r_births_c2: forall <t> in august_periods:
    n[t,2] == sum <e> in E with e >= 24: x[t,e,3] * preg_index / 2;

# Limit births for class 1 and class 2 in certain months
subto r_control_births: forall <t,c> in not_august_periods*C:
    n[t,c] == 0;

# Limit births for class 3 in all months
subto r_no_births_class_3: forall <t> in T:
    n[t,3] == 0;

subto connect_age_0_and_births: forall <t,c> in T*C with t > 0 and c != 3:
    x[t,0,c] == n[t,c];
