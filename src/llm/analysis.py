from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from models.core import AnalysisResult


def run_analysis(problem_description: str, model_latex: str, api_key: str) -> AnalysisResult:
    """
    Send a prompt to DeepSeek and get back analysis with assumptions and recommendations.
    """
    analysis_result_parser = PydanticOutputParser(pydantic_object=AnalysisResult)
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", 
    """You are an expert in optimization modeling. You need to improve the efficiency of this optimization model. \
    To achieve this, you need to propose several new sets of decision variables. \
    For each new proposition, you should look at the implicit assumptions made by the given optimization model and check whether they actually need to hold or can be relaxed. \
    Please list all assumptions and mention which ones could be relaxed and which ones should be kept.\n\n    Here are some propositions on how optimization models can be made more efficient by changing decision variables:\n    - aggregate variables representing groups of variables instead of individual instances in cases where decisions of individual instances are not important to can be derived in post-processing:\n    - delete fixed variables,\n    - replace redundant variables which can usually be detected through strict equalities between variables,\n    - change semantics of variables by changing the definition of it such that the underling problem can still be solved. Note that the application of pre- and post-processing is allowexd, but not required.\n    - integer relaxation may be used if the problem context logically guarantees that the optimal objective value does not change,\n    - find an alternative problem structure\n    - removing an index from binary variables by indicating the level instead of individual assignments\n                \n    {format_instructions}\n    """),
        ("user", 
    """Analyze the following optimization case and provide a list of assumptions made in the model.\n    Here is a description of the optimization problem:\n    {problem_description}\n\n    Here is an associated optimization model in LaTeX format:\n    {model_latex}\n    """)
    ])
    model = ChatOpenAI(
        api_key=api_key, 
        base_url="https://api.openai.com/v1",
        model_name="o3-2025-04-16",
    )
    chain = prompt_template | model | analysis_result_parser
    result = chain.invoke({
        "problem_description": problem_description,
        "model_latex": model_latex,
        "format_instructions": analysis_result_parser.get_format_instructions()
    })
    return result 