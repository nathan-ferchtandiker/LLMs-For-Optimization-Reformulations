import os
import json
import time
from dotenv import load_dotenv
from llm.formulation import generate_formulation_from_context, generate_formulations_from_recommendations
from llm.generator import generate_data_generator
from llm.analysis import run_analysis
from utils.json_utils import json_structure_types_match
from models.optimization import Formulation


def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    case_name = "world_food_program"  # Replace with your case name
    case_path = f"./datasets/{case_name}"
    trials_folder = f'../trials/final/{case_name}'
    os.makedirs(f"{trials_folder}/formulations", exist_ok=True)
    os.makedirs(f"{trials_folder}/synthetic_datasets", exist_ok=True)

    # Load dataset and descriptions
    with open(f'{case_path}/large_data.json', 'r', encoding='utf-8') as f:
        large_dataset = json.load(f)
    with open(f"{case_path}/dataset_description.txt", "r", encoding='utf-8') as f:
        dataset_description = f.read()
    with open(f"{case_path}/inefficient model.tex", "r", encoding='utf-8') as f:
        model_latex = f.read()
    with open(f"{case_path}/detailed description.txt", "r", encoding='utf-8') as f:
        model_detailed_description = f.read()

    model_context = f"""
    ## Problem Description
    {model_detailed_description}

    ## Mathematical Formulations

    {model_latex}
    """

    # Generate initial formulation
    original_formulation = generate_formulation_from_context(
        model_context,
        dataset_description,
        api_key
    )

    # Generate and debug data generator
    data_generator = generate_data_generator(dataset_description, model_context, api_key)
    debug_dataset, dataset_error = data_generator.generate_data_from_code_and_debug(dataset_description, api_key)
    assert(debug_dataset is not None)
    with open(f"{trials_folder}/data_generator.json", "w") as f:
        json.dump(data_generator.model_dump(), f, indent=2)

    tries = 0
    status, mismatches = json_structure_types_match(debug_dataset, large_dataset)
    while not status and tries < 3:
        error_message = f"""
        The structure of the JSON data does not match the expected format.
        {mismatches}
        """
        data_generator.debug_error_message(error_message, dataset_description, api_key)
        debug_dataset, error_info = data_generator.generate_data_from_code()
        status, mismatches = json_structure_types_match(debug_dataset, large_dataset)
        tries += 1
    if not status:
        raise Exception("The generated dataset does not match the expected structure after 3 attempts.")

    # Analyze and create reformulations
    analysis_result = run_analysis(model_detailed_description, original_formulation.to_latex(), api_key)
    new_formulations = generate_formulations_from_recommendations(
        analysis_result=analysis_result,
        original_formulation=original_formulation,
        dataset_explanation=dataset_description,
        api_key=api_key
    )

    # Debug and evaluate formulations
    print(original_formulation.name)
    model, error_info = original_formulation.instancialize_gurobipy_model_and_debug(debug_dataset, dataset_description, api_key)
    if error_info is not None:
        print(error_info)
    for formulation in new_formulations + [original_formulation]:
        if not formulation.has_data_coverage():
            continue
        print(formulation.name)
        model, error_info = formulation.instancialize_gurobipy_model_and_debug(debug_dataset, dataset_description, api_key)
        if error_info is not None:
            print(error_info)

    # Generate small datasets for evaluation
    small_datasets = [data_generator.generate_data_from_code(seed=i)[0] for i in range(20)]
    for i, data in enumerate(small_datasets):
        with open(f"{trials_folder}/synthetic_datasets/data_{i}.json", "w") as f:
            json.dump(data, f, indent=2)
    with open(f"{trials_folder}/formulations/original.json", "w") as f:
        json.dump(original_formulation.model_dump(), f, indent=2)
    for formulation in new_formulations:
        with open(f"{trials_folder}/formulations/{formulation.name}.json", "w") as f:
            json.dump(formulation.model_dump(), f, indent=2)

    print("Workflow complete. Results saved in trials directory.")

if __name__ == "__main__":
    main() 