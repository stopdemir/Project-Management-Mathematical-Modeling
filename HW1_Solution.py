from pulp import *

def question1(H,N,h,A,a,D,M):

    period=list(range(1,H+1))
    product=list(range(1,N+1))
    production = LpVariable.dicts("Prod", ((per, pro) for per in period for pro in product), lowBound=0, cat='Integer')
    inventory = LpVariable.dicts("Inv", ((per, pro) for per in period for pro in product), lowBound=0, cat='Integer')
    product_status = LpVariable.dicts("Pro", ((per, pro) for per in period for pro in product), lowBound=0, cat='Binary')
    factory_status = LpVariable.dicts("Fac",period,0,cat='Binary')
    model = pulp.LpProblem("lot_sizing_problemHW1", pulp.LpMinimize)
    model += pulp.lpSum([inventory[per,pro] * h for per in period for pro in product]
                        + [factory_status[per] * A for per in period]
                        + [product_status[per,pro] * a[pro-1] for per in period for pro in product])
    for per in period: 
        for pro in product:
            if per==1:
                model += inventory[per,pro] == production[per,pro] - D[pro-1][per-1]
            else:
                model += inventory[per,pro] == inventory[per-1,pro] + production[per,pro] - D[pro-1][per-1]
        
    for per in period:
        for pro in product:
            model += production[per,pro] <= M * product_status[per,pro]
            model += product_status[per,pro] <= factory_status[per]
        
    model.solve()

    
    return pulp.value(model.objective)

def question2(H,N,h,A,a,D,M,C):

    period=list(range(1,H+1))
    product=list(range(1,N+1))
    production = LpVariable.dicts("Prod", ((per, pro) for per in period for pro in product), lowBound=0, cat='Integer')
    inventory = LpVariable.dicts("Inv", ((per, pro) for per in period for pro in product), lowBound=0, cat='Integer')
    product_status = LpVariable.dicts("Pro", ((per, pro) for per in period for pro in product), lowBound=0, cat='Binary')
    factory_status = LpVariable.dicts("Fac",period,0,cat='Binary')
    model = pulp.LpProblem("lot_sizing_problemHW2", pulp.LpMinimize)
    model += pulp.lpSum([inventory[per,pro] * h for per in period for pro in product]
                        + [factory_status[per] * A for per in period]
                        + [product_status[per,pro] * a[pro-1] for per in period for pro in product])   
    for per in period: 
        for pro in product:
            if D[pro-1][per-1]<0:
                D[pro-1][per-1]=0
            if per==1:
                model += inventory[per,pro] == production[per,pro] - D[pro-1][per-1]
            else:
                model += inventory[per,pro] == inventory[per-1,pro] + production[per,pro] - D[pro-1][per-1]
        
    for per in period:
        for pro in product:
            model += production[per,pro] <= M * product_status[per,pro]
            model += product_status[per,pro] <= factory_status[per]
        model += pulp.lpSum([production[per,pro] for pro in product]) <= C
    model.solve()

    return pulp.value(model.objective)
