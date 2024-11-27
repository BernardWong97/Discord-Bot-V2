import datetime, discord
from bot.utilities.reminders import Reminder
from datetime import timedelta, datetime
from discord import ApplicationContext, Message, Interaction
from discord.ui import Modal, InputText
from discord.ext.commands import Cog
from bot.bot_instance import Bot
from config import GUILD, TIMEZONE

class ReminderTime(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @discord.message_command(name="Remind By Time", guild_ids=[GUILD])
    async def remind_time(self, 
                     ctx: ApplicationContext, 
                     message: Message
                     ):
        modal = ReminderTimeModal(bot = self.bot, message = message, title="When do you want to be reminded?")

        await ctx.send_modal(modal)

class ReminderTimeModal(Modal):
    def __init__(self, bot: Bot, message: Message, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        later = datetime.now(TIMEZONE).replace(second= 0, microsecond=0) + timedelta(minutes=1)

        self.add_item(InputText(label="Date (YYYY-MM-DD)", value=f"{later.strftime('%Y-%m-%d')}"))
        self.add_item(InputText(label="Time (HH:MM:SS) [24-Hour Format]", value=f"{later.strftime('%H:%M:%S')}"))

        self.bot = bot
        self.message = message

    async def callback(self, interaction: Interaction):
        now = datetime.now(TIMEZONE).replace(microsecond=0)

        date = self.children[0].value
        time = self.children[1].value
        
        try:
            input_time = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M:%S')
        except:
            await interaction.response.send_message('Invalid date or time format.\nPlease enter in __**YYYY-MM-DD**__ format for `Date` and __**HH:MM:SS**__ for `Time` format.', ephemeral=True)
            return
        
        target_time = input_time.replace(tzinfo=TIMEZONE)

        if target_time <= now:
            await interaction.response.send_message('Time must be in the future.', ephemeral=True)
            return

        await interaction.response.send_message(f"Reminder is set to trigger at <t:{int(target_time.timestamp())}>")

        response = await interaction.original_response()

        reminder = Reminder(user_id=interaction.user.id, response_id=response.id, message_url=self.message.jump_url, channel_id=self.message.channel.id, datetime=target_time)

        await reminder.insert(self.bot)



def setup(bot: Bot):
    bot.add_cog(ReminderTime(bot))