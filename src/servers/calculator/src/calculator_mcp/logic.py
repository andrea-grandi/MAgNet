import statistics

from .models import (
    ArithmeticInput, ArithmeticOutput,
    StatisticsInput, StatisticsOutput
)


def compute_arithmetic(req: ArithmeticInput) -> ArithmeticOutput:
    """Execute arithmetic operations."""

    nums = req.numbers
    op = req.operation

    if op == "add":
        result = sum(nums)
    elif op == "subtract":
        result = nums[0] - sum(nums[1:])
    elif op == "multiply":
        result = 1
        for n in nums:
            result *= n
    elif op == "divide":
        result = nums[0]
        for n in nums[1:]:
            if n == 0:
                raise ValueError("Division by zero")
            result /= n
    else:
        raise ValueError(f"Unsupported operation: {op}")

    return ArithmeticOutput(
        result=round(result, 6),
        confidence=1.0,
        trace_id=req.trace_id
    )


def compute_statistics(req: StatisticsInput) -> StatisticsOutput:
    """Execute basic statistical calculations."""
    
    nums = req.numbers
    metric = req.metric

    if metric == "mean":
        value = statistics.mean(nums)
    elif metric == "median":
        value = statistics.median(nums)
    elif metric == "stdev":
        value = statistics.stdev(nums)
    elif metric == "variance":
        value = statistics.variance(nums)
    else:
        raise ValueError(f"Unsupported metric: {metric}")

    return StatisticsOutput(
        value=round(value, 6),
        confidence=0.98,
        trace_id=req.trace_id
    )
