import os

import dotenv

dotenv.load_dotenv()

from finagentlight.llm import LLM
from finagentlight.utils.llm_config import LLMConfig
from finagentlight.utils.message import Message, TextContent

if __name__ == '__main__':
    # Create an LLMConfig object
    config = LLMConfig(
        model='claude-3-5-sonnet-20241022',
        api_key=os.environ.get('CLAUDE_API_KEY'),
    )

    # Create an LLM object
    llm = LLM(config)

    content = [TextContent(text='Hello, how are you?')]
    message = Message(role='user', content=content)
    messages = [message]

    params: dict = {
        'messages': llm.format_messages_for_llm(messages),
        'tools': [],
    }

    response = llm.completion(**params)
    print(response)
