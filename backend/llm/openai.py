from langchain_community.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from backend.config import config
from backend.database.llm_monitor import LLMMonitorSchema


class OpenAI:
    def __init__(self, model_name="gpt-3.5-turbo", temperature=0):
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = config['openai']['api_key']
        self.api_base = config['openai']['api_base']
        self.model = ChatOpenAI(model_name=model_name, temperature=temperature, openai_api_key=self.api_key,
                                openai_api_base=self.api_base)

    def generate(self, messages: list):
        result = self.model(messages)
        LLMMonitorSchema().add_llm_result(message=messages, response=result)
        return result

    def generate_with_system_message(self, system_message: str, user_message: str):
        return self.generate([SystemMessage(content=system_message), HumanMessage(content=user_message)])

    def generate_with_user_message(self, user_message: str):
        return self.generate([HumanMessage(content=user_message)]).content


class Prompt:
    @staticmethod
    def get_system_message(version: str) -> str:
        if version == "v1":
            return "你是数据库专家，根据提供的字段，生成对应的中文名称，返回json格式"
        elif version == "v2":
            return "你是数据库专家，根据提供的字段和示例数据，生成对应的中文名称，返回json格式"

class WelcomeMessage:
    @staticmethod
    def get_welcome_message(version: str) -> str:
        if version == "v1":
            return "你好，我是数据库专家，根据提供的字段，生成对应的中文名称，返回json格式"
        elif version == "v2":
            return "你好，我是数据库专家，根据提供的字段和示例数据，生成对应的中文名称，返回json格式"
        elif version == "check":
            return "你好，我是数据库专家，根据提供的字段和示例数据，生成对应的中文名称，返回json格式"
        elif version == "welcome":
            return "你好，我是数据库专家，根据提供的字段和示例数据，生成对应的中文名称，返回json格式"