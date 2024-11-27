import datetime, discord
from bot.utilities.reminders import Reminder
from datetime import datetime, timedelta
from discord import ApplicationContext, Message, Interaction
from discord.ui import Modal, InputText
from discord.ext.commands import Cog
from bot.bot_instance import Bot
from config import GUILD, TIMEZONE

class ReminderDuration(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @discord.message_command(name="Remind By Duration", guild_ids=[GUILD])
    async def remind_duration(self, 
                     ctx: ApplicationContext, 
                     message: Message
                     ):
        modal = ReminderDurationModal(bot = self.bot, message = message, title="How long later you want to be reminded?")

        await ctx.send_modal(modal)

class ReminderDurationModal(Modal):
    def __init__(self, bot: Bot, message: Message, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(InputText(label="Seconds", value="0"))
        self.add_item(InputText(label="Minutes", value="0"))
        self.add_item(InputText(label="Hours", value="0"))
        self.add_item(InputText(label="Days", value="0"))

        self.bot = bot
        self.message = message

    async def callback(self, interaction: Interaction):
        now = datetime.now(TIMEZONE).replace(microsecond=0)

        seconds = self.children[0].value
        minutes = self.children[1].value
        hours = self.children[2].value
        days = self.children[3].value

        if not seconds.isdigit() or not minutes.isdigit() or not hours.isdigit() or not days.isdigit():
            await interaction.response.send_message('Invalid input. Please enter numbers only.', ephemeral=True)
            return

        total_duration = timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours), days=int(days))

        if total_duration.total_seconds() <= 0:
            await interaction.response.send_message('Duration must be greater than 0.', ephemeral=True)
            return

        target_time = now + total_duration

        await interaction.response.send_message(f"Reminder is set to trigger at <t:{int(target_time.timestamp())}>")

        response = await interaction.original_response()

        reminder = Reminder(user_id=interaction.user.id, response_id=response.id, message_url=self.message.jump_url, channel_id=self.message.channel.id, datetime=target_time)

        await reminder.insert(self.bot)

def setup(bot: Bot):
    bot.add_cog(ReminderDuration(bot))