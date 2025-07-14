from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from models.data_generator import DataGenerator
from llm.prompts import generate_data_generator_instructions, data_instructions


def generate_data_generator(dataset_description: str, model_context: str, api_key: str) -> DataGenerator:
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", f"""
{{generate_data_generator_instructions}}
         
{{data_instructions}}

# Format Instructions
{{format_instructions}}

"""),
        ("user", """
Problem Context
{model_context}

The code should define a function that returns an instance of the dataset class defined in:
{dataset_description}
""")
    ])
    llm = ChatOpenAI(
        api_key=api_key, 
        model="o3-2025-04-16"
    )
    parser = PydanticOutputParser(pydantic_object=DataGenerator)
    chain = prompt_template | llm | parser
    data_generator = chain.invoke({
        "generate_data_generator_instructions": generate_data_generator_instructions,
        "model_context": model_context,
        "dataset_description": dataset_description,
        "data_instructions": data_instructions,
        "format_instructions": parser.get_format_instructions()
    })
    return data_generator 