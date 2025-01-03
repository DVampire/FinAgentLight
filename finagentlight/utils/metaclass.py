from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import ClassVar

from litellm import ModelResponse
from pydantic import BaseModel

from finagentlight.utils.llm_metrics import LLMMetrics


class ToolCallMetadata(BaseModel):
    # See https://docs.litellm.ai/docs/completion/function_call#step-3---second-litellmcompletion-call
    function_name: str  # Name of the function that was called
    tool_call_id: str  # ID of the tool call

    model_response: ModelResponse
    total_calls_in_response: int


class EventSource(str, Enum):
    AGENT = 'agent'
    USER = 'user'
    ENVIRONMENT = 'environment'


@dataclass
class Event:
    @property
    def message(self) -> str | None:
        if hasattr(self, '_message'):
            return self._message  # type: ignore[attr-defined]
        return ''

    @property
    def id(self) -> int:
        if hasattr(self, '_id'):
            return self._id  # type: ignore[attr-defined]
        return -1

    @property
    def timestamp(self):
        if hasattr(self, '_timestamp') and isinstance(self._timestamp, str):
            return self._timestamp

    @timestamp.setter
    def timestamp(self, value: datetime) -> None:
        if isinstance(value, datetime):
            self._timestamp = value.isoformat()

    @property
    def source(self) -> EventSource | None:
        if hasattr(self, '_source'):
            return self._source  # type: ignore[attr-defined]
        return None

    @property
    def cause(self) -> int | None:
        if hasattr(self, '_cause'):
            return self._cause  # type: ignore[attr-defined]
        return None

    @property
    def timeout(self) -> int | None:
        if hasattr(self, '_timeout'):
            return self._timeout  # type: ignore[attr-defined]
        return None

    @timeout.setter
    def timeout(self, value: int | None) -> None:
        self._timeout = value

        # Check if .blocking is an attribute of the event
        if hasattr(self, 'blocking'):
            # .blocking needs to be set to True if .timeout is set
            self.blocking = True

    # optional metadata, LLM call cost of the edit
    @property
    def llm_metrics(self) -> LLMMetrics | None:
        if hasattr(self, '_llm_metrics'):
            return self._llm_metrics  # type: ignore[attr-defined]
        return None

    @llm_metrics.setter
    def llm_metrics(self, value: LLMMetrics) -> None:
        self._llm_metrics = value

    # optional field
    @property
    def tool_call_metadata(self) -> ToolCallMetadata | None:
        if hasattr(self, '_tool_call_metadata'):
            return self._tool_call_metadata  # type: ignore[attr-defined]
        return None

    @tool_call_metadata.setter
    def tool_call_metadata(self, value: ToolCallMetadata) -> None:
        self._tool_call_metadata = value


@dataclass
class Action(Event):
    runnable: ClassVar[bool] = False
