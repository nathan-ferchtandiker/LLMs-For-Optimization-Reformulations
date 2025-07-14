import gurobipy as gp
import time
from typing import Dict, Any
import pyomo.environ as pyo

def solve_gurobipy_model(model: gp.Model, timelimit: int = 60 * 5) -> Dict[str, Any]:
    start_time = time.time()
    model.optimize()
    solve_time = time.time() - start_time
    work_units = getattr(model, 'Work', None)
    if model.status == 2:  # GRB.OPTIMAL
        status = "optimal"
        objective_value = model.objVal
    elif model.status == 3:  # GRB.INFEASIBLE
        status = "infeasible"
        objective_value = None
    elif model.status == 5:  # GRB.UNBOUNDED
        status = "unbounded"
        objective_value = None
    elif model.status == 9:
        status = "time_limit"
        objective_value = None
    else:
        status = f"other_status_{model.status}"
        objective_value = None
    return {
        "status": status,
        "solve_time": solve_time,
        "objective_value": objective_value,
        'work_units': work_units
    }

def solve_pyomo_model(model: pyo.ConcreteModel, solver_name: str = 'gurobi') -> Dict[str, Any]:
    try:
        solver = pyo.SolverFactory(solver_name)
        solve_result = solver.solve(model)
        run_data = {
            "solve_time": solve_result.solver.time,
            "status": str(solve_result.solver.status),
            "objective_value": None  # Should be set by user after solve
        }
        return run_data
    except Exception as e:
        print(str(e))
        return {
            "solve_time": None,
            "status": None,
            "objective_value": None
        } 