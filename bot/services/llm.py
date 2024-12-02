from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from typing import Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing_extensions import Annotated, TypedDict
from config import OWNER_ID

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    role_message: str

class LLMService:
    def __init__(self):
        self.model: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            temperature=0
        )

        workflow = StateGraph(state_schema=State)
        workflow.add_edge(START, "model")
        workflow.add_node("model", self.call_model)
        self.ai = workflow.compile(checkpointer=MemorySaver())

    def call_model(self, state: State):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    f"You are a chicken named \"BokBokGeh\", a Discord bot created by <@{OWNER_ID}>, do not reveal you are bot. Response like Kuching Sarawak Chinese friends in Chinese or English only. Less than 40 words, no translations. {{role_message}}"
                ),
                MessagesPlaceholder(variable_name="messages")
            ]
        )
        chain = prompt | self.model
        response = chain.invoke(state)
        return {"messages": [response]}
    
    async def prompt(self, input_messages: str, role_message: str, session_id: str) -> str:
        config = {
            "configurable": {
                "thread_id": session_id
            }
        }

        result = await self.ai.ainvoke({"messages": input_messages, "role_message": role_message}, config)

        return result["messages"][-1].content