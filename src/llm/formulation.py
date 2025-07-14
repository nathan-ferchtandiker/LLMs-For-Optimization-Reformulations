from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from models.optimization import Formulation
from models.core import AnalysisResult
from llm.prompts import formulation_instructions
import concurrent.futures


def generate_formulation_from_context(model_context: str, dataset_description: str, api_key: str) -> Formulation:
    try:
        parser = PydanticOutputParser(pydantic_object=Formulation)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in mathematical optimization and GurobiPy modeling.\nGenerate a formulation for the given optimization problem.\n\n{formulation_instructions}\n\nThe JSON must follow this schema:\n{format_instructions}\n\n"""),
            ("user", """Generate a formulation based on the following model context:\n{model_context}\n\nHere is the data description:\n{data_structure}\n\nPlease ensure the formulation is complete and implementable in GurobiPy.\n""")
        ])
        llm = ChatOpenAI(api_key=api_key, temperature=0.2, model="gpt-4.1")
        chain = prompt_template | llm | parser
        formulation = chain.invoke({
            "formulation_instructions": formulation_instructions,
            "model_context": model_context,
            "format_instructions": parser.get_format_instructions(),
            "data_structure": dataset_description
        })
        return formulation
    except Exception as e:
        print(f"Failed to generate formulation: {str(e)}")


def generate_formulations_from_recommendations(analysis_result: AnalysisResult, original_formulation: Formulation, dataset_explanation: str, api_key: str):
    try:
        formulations = []
        def generate_for_recommendation(recommendation):
            return generate_formulation_from_context(
                model_context=f"""
                Original formulation: {original_formulation.to_latex()}
                \nRecommended change: {recommendation.suggested_change}
                \nDescription: {recommendation.description}
                \nReasoning: {recommendation.reasoning}
                """,
                dataset_description=dataset_explanation,
                api_key=api_key
            )
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_rec = {
                executor.submit(generate_for_recommendation, recommendation): recommendation
                for recommendation in analysis_result.recommendations
            }
            for future in concurrent.futures.as_completed(future_to_rec):
                try:
                    formulations.append(future.result())
                except Exception as exc:
                    print(f"Recommendation {future_to_rec[future]} generated an exception: {exc}")
        return formulations
    except Exception as e:
        import traceback
        raise ValueError(f"Failed to generate formulations: {str(e)}\n{traceback.format_exc()}") 