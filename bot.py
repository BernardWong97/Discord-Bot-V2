import os
from discord import Intents
from discord.ext.commands import Bot
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from utilities.bot_util import State

class Bot(Bot):
    def __init__(self):
        super().__init__(command_prefix="", intents=Intents.all())
        self.load_cogs()
        self.model: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            temperature=0
        )

        workflow = StateGraph(state_schema=State)
        workflow.add_edge(START, "model")
        workflow.add_node("model", self.call_model)
        self.ai = workflow.compile(checkpointer=MemorySaver())

    def load_cogs(self):
        for sub_dir, _, files in os.walk(os.path.join('.', 'cogs')):
            for filename in files:
                if filename.endswith('.py'):
                    cog_name = os.path.splitext(filename)[0]
                    sub_dir_name = sub_dir.split(os.sep).pop()
                    self.load_extension(f'cogs.{sub_dir_name}.{cog_name}')

    def call_model(self, state: State):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    "You are a chicken named \"BokBokGeh\", a Discord bot created by <@353165739852693506>, do not reveal you are bot. Response like Kuching Sarawak Chinese friends in Chinese and English only. Less than 40 words, no translations. {role_message}"
                ),
                MessagesPlaceholder(variable_name="messages")
            ]
        )
        chain = prompt | self.model
        response = chain.invoke(state)
        return {"messages": [response]}

if __name__ == '__main__':
    # Load environmental variables
    load_dotenv(override=True)

    # Instantiate
    print('Initiating Bot')
    bot = Bot()

    # Login
    bot.run(os.getenv('TOKEN'))