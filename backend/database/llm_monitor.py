import json

from backend.config import db
from datetime import datetime
from langchain_core.messages import (
    BaseMessage
)
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

class LLMMonitor(db.Model):
    __tablename__ = 'llm_monitor'
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text)
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LLMMonitorSchema:

    def add_llm_result(self, message: list, response: BaseMessage) -> None:
        prompt = [i.content for i in message if type(i) == HumanMessage]
        llm_monitor = LLMMonitor(prompt=json.dumps(prompt,ensure_ascii=False), response=response.content)
        db.session.add(llm_monitor)
        db.session.commit()
