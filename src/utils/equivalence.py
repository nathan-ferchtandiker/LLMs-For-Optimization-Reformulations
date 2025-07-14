import pyomo.environ as pyo
from models.optimization import Formulation

def get_objective_value(model: pyo.ConcreteModel):
    objectives = list(model.component_objects(pyo.Objective))
    return pyo.value(objectives[0])

def check_equivalence(main_formulation: Formulation, other_formulations: list, list_of_datasets: list):
    tolerance = 1e-6
    equivalence_results = {}
    run_data = {form.name: [] for form in other_formulations}
    datasets = {}
    for i, data in enumerate(list_of_datasets):
        main_model = main_formulation.instancialize_pyomo_model(data)
        solver = pyo.SolverFactory('gurobi')
        main_results = solver.solve(main_model)
        data_info = {
            "is_feasible": main_results.solver.status == 'ok',
            "is_infeasible": main_results.solver.status == 'infeasible',
            "is_unbounded": main_results.solver.status == 'unbounded',
            "data": data
        }
        datasets[i] = data_info
        for formulation in other_formulations:
            if formulation.name not in equivalence_results:
                equivalence_results[formulation.name] = True
            other_model = formulation.instancialize_pyomo_model(data)
            other_results = solver.solve(other_model)
            if main_results.solver.status != other_results.solver.status:
                equivalence_results[formulation.name] = False
                continue
            if main_results.solver.status == 'infeasible' and other_results.solver.status == 'infeasible':
                continue
            if main_results.solver.status == 'unbounded' and other_results.solver.status == 'unbounded':
                continue
            if main_results.solver.status == 'ok' and other_results.solver.status == 'ok':
                if abs(main_results.problem.lower_bound - other_results.problem.lower_bound) >= tolerance:
                    equivalence_results[formulation.name] = False
                    continue
            else:
                equivalence_results[formulation.name] = False
                continue
            run_info = {
                "run_number": i,
                "solve_time": other_results.solver.time,
                "status": other_results.solver.status,
                "objective_value": get_objective_value(other_model) if other_results.solver.status == 'ok' else None
            }
            run_data[formulation.name].append(run_info)
    return equivalence_results, run_data, datasets 