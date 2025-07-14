from pydantic import BaseModel, Field
from typing import Optional, Dict

class DataGenerator(BaseModel):
    """
    Holds the generated Python code for data creation and adjusted GurobiPy model codes for each formulation.
    """
    data_generation_code: str = Field(
        description="The pure Python code that generates data. The code should have a function called 'generate_data(seed)' that returns a dictionary of data for the optimization case."
    )
    description: str = Field(description="A description of the data generator.")

    # Methods for generating data from code would be implemented here

class DataGenCode(BaseModel):
    data_generation_code: str = Field(description="The pure Python code that generates data. The code should have a function called 'generate_data(seed)' that returns a dictionary of data for the optimization case.") 