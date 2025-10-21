
from pydantic import BaseModel, Field
from typing import List, Optional


class CodeGenerationInput(BaseModel):
    """Input for code generation."""
    description: str = Field(..., description="Description of the code to generate")
    language: str = Field(default="python", description="Programming language")
    
    
class CodeGenerationOutput(BaseModel):
    """Output for code generation."""
    code: str = Field(..., description="Generated code")
    explanation: str = Field(..., description="Explanation of the code")


class CodeReviewInput(BaseModel):
    """Input for code review."""
    code: str = Field(..., description="Code to review")
    language: str = Field(default="python", description="Programming language")
    
    
class CodeReviewOutput(BaseModel):
    """Output for code review."""
    issues: List[str] = Field(..., description="List of issues found")
    suggestions: List[str] = Field(..., description="List of suggestions")
    quality_score: int = Field(..., description="Quality score from 1-10")


class CodeDebugInput(BaseModel):
    """Input for code debugging."""
    code: str = Field(..., description="Code with potential bugs")
    error_message: Optional[str] = Field(None, description="Error message if available")
    language: str = Field(default="python", description="Programming language")
    
    
class CodeDebugOutput(BaseModel):
    """Output for code debugging."""
    issues_found: List[str] = Field(..., description="Issues identified")
    fixed_code: str = Field(..., description="Fixed code")
    explanation: str = Field(..., description="Explanation of fixes")
