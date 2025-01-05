from typing import Any, Dict

import dotenv

dotenv.load_dotenv()

from finagentlight.llm import LLM
from finagentlight.registry import AGENT


@AGENT.register_module(force=True)
class Agent:
    def __init__(self, llm: LLM):
        self.llm = llm

    def reset(self):
        pass

    def step(self, state: Dict[str, Any]):
        pass

    def _get_messages(self, state: Dict[str, Any]):
        pass
