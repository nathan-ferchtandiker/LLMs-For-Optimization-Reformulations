# Prompt templates and instructions for LLM interactions

generate_data_generator_instructions = """
You are an expert in Python programming and data generation for optimization problems.
Your task is to generate Python code that creates random data for the given optimization model's sets and parameters. The dataset should be large, such that the optimization solver wll take a few seconds to solve it.
"""

generate_gurobipy_instructions = """
- Use the GurobiPy Python API (import gurobipy as gp, from gurobipy import GRB).
- Define all sets, parameters, variables, constraints, and the objective function as described in the model context and data structure.
- Access all data using the provided Python dictionary (data), using bracket notation (e.g., data[\"set_name\"], data[\"param_name\"], data[\"param_name\"][i][j]).
- Use clear and descriptive variable and constraint names.
- Add comments explaining each part of the model.
- Ensure the model is complete and can be solved with model.optimize().
- Do not include any code for data input/output or reading from files.
- The code should be a single Python function that takes a data dictionary as input and returns a GurobiPy model object.

Example function signature:
def generate_gurobipy_model(data: dict) -> "gurobipy.Model":
    # your code here

"""

data_object_description = """
The dataset is a Python dictionary where all keys are strings. It contains all sets and parameters required by the optimization model. 
- Sets are represented as lists of strings, even if the key is an integer.
- Parameters are represented as either single values, dictionaries (for indexed parameters), or nested dictionaries (for multi-indexed parameters).
- All data is accessible using bracket notation, e.g., data[\"set_name\"], data[\"param_name\"], or data[\"param_name\"][i][j].
- The structure and required fields of the dataset are determined by the model's data description.
"""

data_instructions = f"""
1. Generate appropriate random data for all sets and parameters described in the model.
2. Follow these guidelines:
   - Use random and numpy for data generation
   - Include appropriate type hints
   - Add clear comments explaining the data generation logic
   - Ensure all required fields from the dataset class are populated
   - Make the data generation deterministic when a seed is provided
3. The datasets returned by the function should be small 
4. Try to maintain simple relationships between the datapoints
5. All keys must be strings at all levels
6. When sampling random numerical values, make the range small relative to the value. For example, if the sample mean is 100, the range should be 98-102.
7. Include symmetry in the dataset. Some values should be the same intentionally.
8. Do not make the dataset sparse.
9. 

Here is the description of the dataset
{data_object_description}


Here is a template for the code:

import random
import numpy as np


def generate_data(seed=42):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        
    data ={{}} # dictionary with strings as keys

    
    return data

"""

formulation_instructions = f"""
Key requirements:
1. Create a clear and descriptive name for the formulation.
2. Provide a detailed description of the formulation.
3. Define all necessary variables with appropriate types and descriptions.
4. Define all constraints with clear descriptions and expressions.
5. Ensure all code is well-structured, efficient, and includes comments.
6. Use the provided data explanation to infer set and parameter references in the dataset.
7. The dataset is a JSON dictionary; access data using bracket notation only, without default values.
8. Always use the exact keys from the data explanation when accessing data.
9. For dictionary parameters, use nested dictionary access for multi-indexed parameters (e.g., data['param'][i][j]).
10. For single-indexed parameters, use string keys.
11. Never hardcode values or use keys that do not exist in the data.

Here is the description of the dataset
{data_object_description}

Here is the description of the code to generate the GurobiPy model
{generate_gurobipy_instructions}



Please ensure the formulation is complete and implementable in GurobiPy.
""" 