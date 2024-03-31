from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatLiteLLM

from salesgpt.logger import time_logger
from salesgpt.prompts import (
    SALES_AGENT_INCEPTION_PROMPT,
    STAGE_ANALYZER_INCEPTION_PROMPT,
    CUSTOMER_SERVICE_INTENT_ANALYZER_INCEPTION_PROMPT
)


class StageAnalyzerChain(LLMChain):
    """Chain to analyze which conversation stage should the conversation move into."""

    @classmethod
    @time_logger
    def from_llm(cls, llm: ChatLiteLLM, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        stage_analyzer_inception_prompt_template = STAGE_ANALYZER_INCEPTION_PROMPT
        prompt = PromptTemplate(
            template=stage_analyzer_inception_prompt_template,
            input_variables=[
                "conversation_history",
                "conversation_stage_id",
                "conversation_stages",
            ],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)


class SalesConversationChain(LLMChain):
    """Chain to generate the next utterance for the conversation."""

    @classmethod
    @time_logger
    def from_llm(
        cls,
        llm: ChatLiteLLM,
        verbose: bool = True,
        use_custom_prompt: bool = False,
        custom_prompt: str = "You've reached our customer service team. How can I assist you today?",
    ) -> LLMChain:
        """Get the response parser."""
        if use_custom_prompt:
            prompt = PromptTemplate(
                template=custom_prompt,
                input_variables=[
                    "agent_name",
                    "agent_role",
                    "company_name",
                    "company_business",
                    "company_values",
                    "conversation_purpose",
                    "conversation_type",
                    "conversation_history",
                ],
            )
        else:
            prompt = PromptTemplate(
                template=SALES_AGENT_INCEPTION_PROMPT,
                input_variables=[
                    "agent_name",
                    "agent_role",
                    "company_name",
                    "company_business",
                    "company_values",
                    "conversation_purpose",
                    "conversation_type",
                    "conversation_history",
                ],
            )
        return cls(prompt=prompt, llm=llm, verbose=verbose)


class CustomerServiceIntentAnalyzerChain(LLMChain):
    """Chain to analyze the intent of a customer service conversation."""

    @classmethod
    @time_logger
    def from_llm(cls, llm: ChatLiteLLM, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        prompt = PromptTemplate(
            template=CUSTOMER_SERVICE_INTENT_ANALYZER_INCEPTION_PROMPT,
            input_variables=[
                "conversation_history",
            ],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)