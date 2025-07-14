from pyomo.environ import *

model = AbstractModel()

# Sets
model.N = Set()  # All nodes
model.A = Set(dimen=2)  # Arcs
model.K = Set()  # Commodities
model.L = Set()  # Nutrients

# Subsets
model.N_S = Set(within=model.N)  # Supplier nodes
model.N_T = Set(within=model.N)  # Transshipment nodes
model.N_B = Set(within=model.N)  # Beneficiary camp nodes

# Parameters
model.c = Param(model.A, model.K)  # Shipping cost per kg of commodity k along arc (i,j)
model.nutval = Param(model.K, model.L)  # Nutrient content per kg of commodity
model.nutreq = Param(model.L)  # Per-person nutrient requirement
model.dem = Param(model.N_B)  # Number of beneficiaries at each camp

# Variables
model.y = Var(model.A, model.K, domain=NonNegativeReals)  # Amount shipped
model.R = Var(model.K, domain=NonNegativeReals)  # Ration size per person

# Objective: Minimize total cost
def total_cost_rule(model):
    return sum(model.c[i,j,k] * model.y[i,j,k] for (i,j) in model.A for k in model.K)
model.total_cost = Objective(rule=total_cost_rule, sense=minimize)

# Constraints
# Flow conservation at transshipment nodes
def flow_conservation_rule(model, j, k):
    if j in model.N_T:
        inflow = sum(model.y[i,j,k] for (i,jj) in model.A if jj == j)
        outflow = sum(model.y[j,m,k] for (jj,m) in model.A if jj == j)
        return inflow - outflow == 0
    else:
        return Constraint.Skip
model.flow_conservation = Constraint(model.N, model.K, rule=flow_conservation_rule)

# Ensure camps receive required ration quantities
def ration_fulfillment_rule(model, j, k):
    if j in model.N_B:
        return sum(model.y[i,j,k] for (i,jj) in model.A if jj == j) >= model.dem[j] * model.R[k]
    else:
        return Constraint.Skip
model.ration_fulfillment = Constraint(model.N, model.K, rule=ration_fulfillment_rule)

# Ensure minimum nutritional content per person
def nutrition_requirement_rule(model, l):
    return sum(model.nutval[k,l] * model.R[k] for k in model.K) >= model.nutreq[l]
model.nutrition_requirement = Constraint(model.L, rule=nutrition_requirement_rule)

data = DataPortal()
data.load(filename='data.dat')
instance = model.create_instance(data)
solver = SolverFactory('glpk')
results = solver.solve(instance, tee=True)
print(results)