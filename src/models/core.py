from pydantic import BaseModel, Field
from typing import List

class Assumption(BaseModel):
    name: str = Field(description="The name of the assumption")
    description: str = Field(description="Detailed description of the assumption")
    breakable: bool = Field(description="Whether this assumption can be broken or modified")
    reasoning: str = Field(description="Explanation of why this assumption was made")

class Recommendation(BaseModel):
    name: str = Field(description="The name of the recommendation")
    description: str = Field(description="Detailed description of the recommendation")
    assumption_name: str = Field(description="Name of the assumption this recommendation relates to")
    reasoning: str = Field(description="Explanation of why this recommendation was made")
    suggested_change: str = Field(description="Specific change being recommended")

class AnalysisResult(BaseModel):
    assumptions: list[Assumption] = Field(description="List of assumptions made in the analysis")
    recommendations: list[Recommendation] = Field(description="List of recommendations based on the analysis")
    reasoning: str = Field(description="Overall reasoning for the analysis results")

    def get_breakable_assumptions(self) -> list[Assumption]:
        """Returns a list of assumptions that can be broken or modified."""
        return [assumption for assumption in self.assumptions if assumption.breakable]

    def get_breakable_recommendations(self) -> list[Recommendation]:
        """Returns a list of recommendations related to breakable assumptions."""
        breakable_assumption_names = {assumption.name for assumption in self.get_breakable_assumptions()}
        return [rec for rec in self.recommendations if rec.assumption_name in breakable_assumption_names]

    def get_breakable_analysis_result(self) -> 'AnalysisResult':
        """Returns a new AnalysisResult containing only breakable assumptions and their related recommendations."""
        breakable_assumptions = self.get_breakable_assumptions()
        breakable_recommendations = self.get_breakable_recommendations()
        return AnalysisResult(
            assumptions=breakable_assumptions,
            recommendations=breakable_recommendations,
            reasoning=f"Analysis focusing on breakable assumptions: {self.reasoning}"
        ) 