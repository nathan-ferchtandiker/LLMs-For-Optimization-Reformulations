from pyomo.environ import *

model = AbstractModel()

# Sets
model.P = Set()  # set of all simple paths from supplier to beneficiary camps
model.K = Set()  # set of commodities
model.L = Set()  # set of nutrients
model.N_B = Set()  # set of beneficiary camps

# Parameters
model.cpk = Param(model.P, model.K)  # cost of shipping one kg of commodity k along path p
model.nutval = Param(model.K, model.L)  # nutrient content per kg of commodity
model.nutreq = Param(model.L)  # per-person requirement for nutrient
model.dem = Param(model.N_B)  # number of beneficiaries at camp j
model.e = Param(model.N_B, model.P)  # 1 if path p ends at camp j, 0 otherwise

# Variables
model.x = Var(model.P, model.K, domain=NonNegativeReals)  # amount (kg) of commodity shipped along path
model.R = Var(model.K, domain=NonNegativeReals)  # ration size (kg per person) of commodity

def objective_rule(model):
    return sum(model.cpk[p, k] * model.x[p, k] for p in model.P for k in model.K)
model.total_cost = Objective(rule=objective_rule, sense=minimize)

def delivery_constraint_rule(model, j, k):
    return sum(model.e[j, p] * model.x[p, k] for p in model.P) >= model.dem[j] * model.R[k]
model.delivery_constraint = Constraint(model.N_B, model.K, rule=delivery_constraint_rule)

def nutrition_constraint_rule(model, l):
    return sum(model.nutval[k, l] * model.R[k] for k in model.K) >= model.nutreq[l]
model.nutrition_constraint = Constraint(model.L, rule=nutrition_constraint_rule)


data = DataPortal()
data.load(filename='data.dat')
instance = model.create_instance(data)
solver = SolverFactory('glpk')
results = solver.solve(instance, tee=True)
print(results)