import os
from bot import Bot
from discord import Message
from langchain_core.messages import HumanMessage
from utilities.database import retrieve_data


async def prompt(bot: Bot, message: Message) -> str:
    config = {
        "configurable": {
            "thread_id": message.author.id
        }
    }

    role_message = "Reply like you are willing to help."

    result = await retrieve_data(f'SELECT * FROM {os.getenv("MYSQL_QUOTE_TABLE")} WHERE member_id = {message.author.id};')

    quote_messages = []

    for row in result:
        _, _, quote = row

        if quote is not None:
            quote_messages.append("\"" + quote + "\"")

    result = await retrieve_data(f'SELECT role_message FROM {os.getenv("MYSQL_MEMBER_TABLE")} WHERE id = {message.author.id};')

    if len(result) > 0:
        role_message = result[0][0]

    if len(quote_messages) > 0:
        role_message += f" Here are some examples that you will reply: "
        role_message += ", ".join(quote_messages)

    input_messages = [HumanMessage(content=message.content)]
    output = bot.ai.invoke({"messages": input_messages, "role_message": role_message}, config)

    return output["messages"][-1].content