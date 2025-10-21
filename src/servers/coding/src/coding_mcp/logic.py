
from .models import (
    CodeGenerationInput,
    CodeGenerationOutput,
    CodeReviewInput,
    CodeReviewOutput,
    CodeDebugInput,
    CodeDebugOutput
)


def generate_code(req: CodeGenerationInput) -> CodeGenerationOutput:
    """Generate code based on description."""
    
    # Placeholder implementation - in a real scenario, this could use an LLM
    templates = {
        "python": {
            "hello_world": 'print("Hello, World!")',
            "fibonacci": '''def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)''',
            "default": f'''# Generated code for: {req.description}
def main():
    # TODO: Implement {req.description}
    pass

if __name__ == "__main__":
    main()'''
        }
    }
    
    # Simple keyword matching
    description_lower = req.description.lower()
    if "hello" in description_lower or "world" in description_lower:
        code = templates.get(req.language, {}).get("hello_world", "")
        explanation = "Simple hello world program"
    elif "fibonacci" in description_lower:
        code = templates.get(req.language, {}).get("fibonacci", "")
        explanation = "Recursive fibonacci implementation"
    else:
        code = templates.get(req.language, {}).get("default", "")
        explanation = f"Template code structure for {req.description}"
    
    return CodeGenerationOutput(
        code=code,
        explanation=explanation
    )


def review_code(req: CodeReviewInput) -> CodeReviewOutput:
    """Review code and provide feedback."""
    
    issues = []
    suggestions = []
    score = 10
    
    # Basic code quality checks
    if len(req.code.strip()) == 0:
        issues.append("Empty code provided")
        score = 1
        return CodeReviewOutput(issues=issues, suggestions=["Provide actual code"], quality_score=score)
    
    lines = req.code.split('\n')
    
    # Check for basic quality indicators
    if req.language == "python":
        # Check for docstrings
        if '"""' not in req.code and "'''" not in req.code:
            issues.append("Missing docstrings")
            suggestions.append("Add docstrings to functions and classes")
            score -= 2
        
        # Check for type hints
        if "def " in req.code and "->" not in req.code:
            suggestions.append("Consider adding type hints to functions")
            score -= 1
        
        # Check line length
        for i, line in enumerate(lines, 1):
            if len(line) > 100:
                issues.append(f"Line {i} exceeds 100 characters")
                score -= 1
                break
    
    # Check for comments
    comment_count = sum(1 for line in lines if line.strip().startswith('#'))
    if len(lines) > 10 and comment_count == 0:
        suggestions.append("Add comments to explain complex logic")
        score -= 1
    
    if not issues:
        issues.append("No major issues found")
    
    if not suggestions:
        suggestions.append("Code looks good!")
    
    return CodeReviewOutput(
        issues=issues,
        suggestions=suggestions,
        quality_score=max(1, min(10, score))
    )


def debug_code(req: CodeDebugInput) -> CodeDebugOutput:
    """Debug code and suggest fixes."""
    
    issues_found = []
    fixed_code = req.code
    explanation = ""
    
    if req.error_message:
        issues_found.append(f"Error reported: {req.error_message}")
    
    # Common bug patterns
    if req.language == "python":
        # Check for common indentation issues
        if "\t" in req.code and "    " in req.code:
            issues_found.append("Mixed tabs and spaces")
            fixed_code = req.code.replace("\t", "    ")
            explanation += "Replaced tabs with spaces for consistency. "
        
        # Check for missing colons
        lines = req.code.split('\n')
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(('def ', 'class ', 'if ', 'for ', 'while ', 'elif ', 'else', 'try:', 'except')):
                if not stripped.endswith(':') and not stripped.endswith(':\\'):
                    issues_found.append(f"Missing colon at line {i+1}")
        
        # Check for undefined variables (basic check)
        if "NameError" in (req.error_message or ""):
            issues_found.append("Possible undefined variable")
            explanation += "Check variable names and ensure they are defined before use. "
    
    if not issues_found:
        issues_found.append("No obvious bugs detected with static analysis")
        explanation = "Code appears syntactically correct. Runtime testing recommended."
    else:
        if not explanation:
            explanation = "Fixed common issues. Please test thoroughly."
    
    return CodeDebugOutput(
        issues_found=issues_found,
        fixed_code=fixed_code,
        explanation=explanation
    )
