import json
from typing import Any

from pydantic import BaseModel, Field

from magnet.tasks.output_format import OutputFormat
from magnet.tasks.task_output import TaskOutput
from magnet.types.usage_metrics import UsageMetrics


class NetOutput(BaseModel):
    """Class that represents the result of a net."""

    raw: str = Field(description="Raw output of net", default="")
    pydantic: BaseModel | None = Field(
        description="Pydantic output of Net", default=None
    )
    json_dict: dict[str, Any] | None = Field(
        description="JSON dict output of Net", default=None
    )
    tasks_output: list[TaskOutput] = Field(
        description="Output of each task", default=[]
    )
    token_usage: UsageMetrics = Field(
        description="Processed token summary", default_factory=UsageMetrics
    )

    @property
    def json(self) -> str | None:  # type: ignore[override]
        if self.tasks_output[-1].output_format != OutputFormat.JSON:
            raise ValueError(
                "No JSON output found in the final task. Please make sure to set the output_json property in the final task in your net."
            )

        return json.dumps(self.json_dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert json_output and pydantic_output to a dictionary."""
        output_dict = {}
        if self.json_dict:
            output_dict.update(self.json_dict)
        elif self.pydantic:
            output_dict.update(self.pydantic.model_dump())
        return output_dict

    def __getitem__(self, key):
        if self.pydantic and hasattr(self.pydantic, key):
            return getattr(self.pydantic, key)
        if self.json_dict and key in self.json_dict:
            return self.json_dict[key]
        raise KeyError(f"Key '{key}' not found in NetOutput.")

    def __str__(self):
        if self.pydantic:
            return str(self.pydantic)
        if self.json_dict:
            return str(self.json_dict)
        return self.raw
