from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Dict, Optional

class OptimizationModelVariableType(str, Enum):
    CONTINUOUS = "continuous"
    INTEGER = "integer"
    BINARY = "binary"

class ObjectiveType(str, Enum):
    MINIMIZE = "minimize"
    MAXIMIZE = "maximize"

class ConstraintType(str, Enum):
    EQUALITY = "equality"
    LESS_EQUAL = "less_equal"
    GREATER_EQUAL = "greater_equal"

class OptimizationModelSet(BaseModel):
    symbol: str = Field(description="The symbol of the set in text")
    description: str = Field(description="Description of the set in latex text mode")
    exists_in_dataset : bool = Field(description="A boolean which indicates whether this set exists in the dataset")
    latex: str = Field(description="Simple LaTeX expression for the set")

class OptimizationModelConstraint(BaseModel):
    description: str = Field(description="Description of the constraint in latex text mode")
    expression: str = Field(description="Mathematical expression of the constraint in latex math mode")
    sets: list[str] = Field(description="List of sets over which the constraint is indexed")
    latex: str = Field(description="Simple LaTeX expression for the constraint")

class OptimizationModelObjectiveFunction(BaseModel):
    expression: str = Field(description="Mathematical expression of the objective function in latex math mode")
    direction: ObjectiveType = Field(description="Direction of optimization (minimize or maximize)")
    description: str = Field(description="Description of the objective function in math text mode")
    latex: str = Field(description="Simple LaTeX expression for the objective function")

class OptimizationModelParameter(BaseModel):
    symbol: str = Field(description="The symbol of the parameter in text. This excludes the indices")
    description: str = Field(description="Description of the parameter in latex text mode")
    sets: list[str] = Field(description="List of sets that this parameter is indexed over")
    exists_in_dataset : bool = Field(description="A boolean which indicates whether this parameter esxits in the dataset")
    latex: str = Field(description="Simple LaTeX expression for the parameter")

class OptimizationModelVariable(BaseModel):
    symbol: str = Field(description="The symbol of the variable in text. This excludes the indices")
    type: OptimizationModelVariableType
    description: str = Field(description="Description of the variable in latex text mode")
    sets: list[str] = Field(description="List of sets that this variable is indexed over")
    latex: str = Field(description="Simple LaTeX expression for the variable")

class ModelImplementation(BaseModel):
    recommendation_name: str = Field(description="Name of the recommendation being implemented")
    assumption_broken: str = Field(description="Name of the assumption being broken/modified")
    explanation: str = Field(description="Detailed explanation of the implementation")
    latex_model: str = Field(description="LaTeX representation of the modified model")
    key_differences: list[str] = Field(description="List of key differences from the original model")
    potential_benefits: list[str] = Field(description="List of potential benefits from this implementation")

class Formulation(BaseModel):
    class GurobiCode(BaseModel):
        code: str = Field(description="The GurobiPy code that implements this formulation")
    name: str = Field(description="Name of this formulation. Ensure this is unique across all formulations.")
    description: str = Field(description="Description of this formulation")
    variables: list[OptimizationModelVariable] = Field(description="Variables specific to this formulation")
    constraints: list[OptimizationModelConstraint] = Field(description="Constraints specific to this formulation")
    sets: list[OptimizationModelSet] = Field(description="Sets specific to this formulation")
    parameters: list[OptimizationModelParameter] = Field(description="Parameters specific to this formulation")
    gurobi_code: GurobiCode = Field(description="The GurobiPy code that implements this formulation")

    def to_latex(self) -> str:
        latex_parts = []
        latex_parts.append(r"\documentclass{article}")
        latex_parts.append(r"\usepackage{amsmath}")
        latex_parts.append(r"\usepackage{amssymb}")
        latex_parts.append(r"\begin{document}")
        latex_parts.append(f"\\section*{{{self.name}}}")
        latex_parts.append(f"{self.description}\n")
        if self.sets:
            latex_parts.append(r"\subsection*{Sets}")
            for set_def in self.sets:
                latex_parts.append(f"\\[{set_def.latex}\\]")
                latex_parts.append(f"{set_def.description}\n")
        if self.parameters:
            latex_parts.append(r"\subsection*{Parameters}")
            for param in self.parameters:
                latex_parts.append(f"\\[{param.latex}\\]")
                latex_parts.append(f"{param.description}\n")
        if self.variables:
            latex_parts.append(r"\subsection*{Variables}")
            for var in self.variables:
                latex_parts.append(f"\\[{var.latex}\\]")
                latex_parts.append(f"{var.description}\n")
        if hasattr(self, 'objective'):
            latex_parts.append(r"\subsection*{Objective Function}")
            latex_parts.append(f"\\[{self.objective.latex}\\]")
            latex_parts.append(f"{self.objective.description}\n")
        if self.constraints:
            latex_parts.append(r"\subsection*{Constraints}")
            for i, constraint in enumerate(self.constraints, 1):
                latex_parts.append(f"\\[{constraint.latex}\\]")
                latex_parts.append(f"{constraint.description}\n")
        latex_parts.append(r"\end{document}")
        return "\n".join(latex_parts)

class OptimizationCase(BaseModel):
    """Enhanced model to represent the optimization problem with multiple formulations."""
    name: str = Field(description="Name of the optimization problem")
    formulations: list[Formulation] = Field(default_factory=list, description="Different formulations of the same optimization problem")
    description: str = Field(description="Description of this formulation")
    dataset: Dict = Field(description="The dataset") 