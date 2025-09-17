from pydantic import BaseModel, Field
from typing import Optional, Dict
import types
import sys
import linecache
from typing import Tuple
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
import prompts


class DataGenerator(BaseModel):
    """
    Holds the generated Python code for data creation and adjusted GurobiPy model codes for each formulation.
    """
    data_generation_code: str = Field(
        description="The pure Python code that generates data. The code should have a function called 'generate_data(seed)' that returns a dictionary of data for the optimization case."
    )
    description: str = Field(description="A description of the data generator.")

    # Methods for generating data from code would be implemented here
    def generate_data_from_code(self, seed: Optional[int] = None) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Execute the data generator code and return the generated data and error info.

        Args:
            seed (Optional[int]): Optional seed for reproducibility

        Returns:
            Tuple[Dict, str]: The generated dataset instance and error info (None if no error)
        """
        error_info = None
        data = None

        if seed is None:
            seed = 42

        code_str = self.data_generation_code
        module_name = f"data_generator_{id(code_str)}"
        fake_filename = f"<data_generator_code_{id(code_str)}>"
        module = types.ModuleType(module_name)
        sys.modules[module_name] = module

        # Inject code into linecache for better traceback (like in instancialize_gurobipy_model)
        lines = code_str.splitlines(keepends=True)
        linecache.cache[fake_filename] = (
            len(code_str), None, lines, fake_filename
        )

        try:
            # Compile with fake filename to improve traceback info
            compiled_code = compile(code_str, fake_filename, 'exec')
            exec(compiled_code, module.__dict__)

            # Get the data generation function
            generate_data = getattr(module, 'generate_data', None)
            if generate_data is None:
                error_info = "No 'generate_data' function found in the data generator code."
                return None, error_info

            # Call the data generation function
            data = generate_data(seed)
            return data, None

        except Exception as exec_e:
            import traceback
            tb = ''.join(traceback.format_exception(type(exec_e), exec_e, exec_e.__traceback__))
            error_info = f"Exception during data generation:\n{tb}"
            return None, error_info
        
    def generate_data_from_code_and_debug(self, data_instructions: str, api_key: str, max_tries: int = 3, seed: Optional[int] = None):
        """
        Execute the data generator code and debug it using an LLM if it fails, up to max_tries.
        
        Args:
            data_instructions (str): Instructions about the data structure
            api_key (str): OpenAI API key for debugging
            max_tries (int): Maximum number of debugging attempts
            seed (Optional[int]): Optional seed for reproducibility
            
        Returns:
            dict: The generated dataset instance
            
        Raises:
            ValueError: If the data generation fails after max_tries attempts
        """
        tries = 0
        current_code = self.data_generation_code

        while tries < max_tries:
            data, error_info = self.generate_data_from_code(seed)
            if data is not None:
                return data, None
            
            
            if tries >= max_tries - 1:
                return None, error_info


            prompt = ChatPromptTemplate.from_messages([
                ("system",
                    """
{generate_data_generator_instructions}

Here are the format instructions for the data generator code:
{format_instructions}
"""
                ),
                ("user",
                    """Fix the following Python data generator code that encountered an error:
Error Information:
{error_info}

Original Data Generator Code:
{current_code}

Here is the data structure:
{data_structure}

Please ensure the fixed code maintains the same data structure and logic while resolving the error."""
                )
            ])

            llm = ChatOpenAI(
                api_key=api_key,
                temperature=0.2,
                model="gpt-4.1"
            )



            class DataGenCode(BaseModel):
                data_generation_code: str = Field(description="The pure Python code that generates data. The code should have a function called 'generate_data(seed)' that returns a dictionary of data for the optimization case.")

            parser = PydanticOutputParser(pydantic_object=DataGenCode)
            chain = prompt | llm | parser

            result = chain.invoke({
                "generate_data_generator_instructions": prompts.generate_data_generator_instructions,
                "current_code": current_code,
                "error_info": error_info,
                "format_instructions": parser.get_format_instructions(),
                "data_structure": data_instructions
            })

            current_code = result.data_generation_code
            self.data_generation_code = current_code
            tries += 1

    def debug_error_message(self, error_info: str, data_instructions: str, api_key: str) -> str:
        """
        Use an LLM to debug the data_generation_code given an error message and return the fixed code as a string.
        Args:
            error_info (str): The error message from a failed data generation attempt
            data_instructions (str): Instructions about the data structure
            api_key (str): OpenAI API key for debugging
        Returns:
            str: The fixed data_generation_code
        """

        class DataGenCode(BaseModel):
            data_generation_code: str = Field(description="The pure Python code that generates data. The code should have a function called 'generate_data(seed)' that returns a dictionary of data for the optimization case.")

        prompt = ChatPromptTemplate.from_messages([
            ("system",
                """
{generate_data_generator_instructions}

Here are the format instructions for the data generator code:
{format_instructions}
"""
            ),
            ("user",
                """Fix the following Python data generator code that encountered an error:
Error Information:
{error_info}

Original Data Generator Code:
{current_code}

Here is the data structure:
{data_structure}

Please ensure the fixed code maintains the same data structure and logic while resolving the error."""
            )
        ])
        llm = ChatOpenAI(
            api_key=api_key,
            temperature=0.2,
            model="gpt-4.1"
        )
        parser = PydanticOutputParser(pydantic_object=DataGenCode)
        chain = prompt | llm | parser
        result = chain.invoke({
            "generate_data_generator_instructions": prompts.generate_data_generator_instructions,
            "current_code": self.data_generation_code,
            "error_info": error_info,
            "format_instructions": parser.get_format_instructions(),
            "data_structure": data_instructions
        })
        
        self.data_generation_code = result.data_generation_code
        return result

class DataGenCode(BaseModel):
    data_generation_code: str = Field(description="The pure Python code that generates data. The code should have a function called 'generate_data(seed)' that returns a dictionary of data for the optimization case.") 