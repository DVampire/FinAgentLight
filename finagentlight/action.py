from dataclasses import dataclass

from finagentlight.utils.metaclass import Action


@dataclass
class MarketIntelligenceAction(Action):
    market_intelligence_analysis: str
    market_intelligence_summary: str
    action: str = 'Summary'

    @property
    def message(self) -> str:
        return (
            f'Market Intelligence Analysis: {self.market_intelligence_analysis}\n'
            + f'Market Intelligence Summary: {self.market_intelligence_summary}'
        )

    def __str__(self) -> str:
        ret = '**MarketIntelligenceAction**\n'
        ret += f'Market Intelligence Analysis: {self.market_intelligence_analysis}\n'
        ret += f'Market Intelligence Summary: {self.market_intelligence_summary}'
        return ret


@dataclass
class DecisionMakingAction(Action):
    decision_making_analysis: str
    decision_making_reasoning: str
    decision_making_decision: str
    action: str = 'Decision'

    @property
    def message(self) -> str:
        return (
            f'Decision Making Analysis: {self.decision_making_analysis}\n'
            + f'Decision Making Reasoning: {self.decision_making_reasoning}\n'
            + f'Decision Making Decision: {self.decision_making_decision}'
        )

    def __str__(self) -> str:
        ret = '**DecisionMakingAction**\n'
        ret += f'Decision Making Analysis: {self.decision_making_analysis}\n'
        ret += f'Decision Making Reasoning: {self.decision_making_reasoning}\n'
        ret += f'Decision Making Decision: {self.decision_making_decision}'
        return ret
