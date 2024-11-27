import re, discord
from discord import ApplicationContext, SlashCommandGroup, Interaction, SelectOption, SelectMenu, ActionRow
from discord.ui import View, Select
from discord.ext.commands import Cog
from bot.bot_instance import Bot
from config import GUILD, OWNER_ID

class Remind(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    reminder_group = SlashCommandGroup(name="reminder", description="Remind a message", guild_ids=[GUILD])        

    @reminder_group.command(name="delete", description="Delete a reminder", guild_ids=[GUILD])
    async def delete(self, 
                     ctx: ApplicationContext,
                     ):
        await ctx.defer(ephemeral=True)

        options = []

        reminders = sorted(self.bot.reminders, key=lambda x: x.datetime, reverse=True)

        for reminder in reminders:
            message_id = reminder.message_url.split('/')[-1]
            try:
                ori_message = await self.bot.get_channel(int(reminder.channel_id)).fetch_message(int(message_id))
            except discord.errors.NotFound:
                continue

            mention_pattern = re.compile(r'<@(\d+)>')

            def replace_mention(match):
                member_id = int(match.group(1))
                guild = self.bot.get_guild(GUILD)
                member = guild.get_member(member_id)
                return member.display_name

            message = mention_pattern.sub(replace_mention, str(ori_message.content))

            message_content = (message[:97] + "..") if len(message) > 100 else message
            options.append(SelectOption(label=message_content, description=reminder.datetime.strftime('%d %b %Y %I:%M:%S %p'), value=str(reminder.id)))

        if not options:
            await ctx.followup.send('No reminders to delete', ephemeral=True)
            return

        select_menu = Select(
            placeholder="Select Reminder",
            options=options[:25],
            min_values=1,
            max_values=1
        )

        select_menu.callback = self.delete_reminder
        
        select_menu_view = View()
        select_menu_view.add_item(select_menu)

        await ctx.followup.send('Which reminder do you want to delete?', wait=True, view = select_menu_view, ephemeral=True)

    async def delete_reminder(self, interaction: Interaction):
        id = int(interaction.data['values'][0])

        reminder = next((reminder for reminder in self.bot.reminders if reminder.id == id), None)

        if reminder:
            message = await self.bot.get_channel(int(reminder.channel_id)).fetch_message(int(reminder.response_id))
            await message.delete()
            response_message = (f'<@{interaction.user.id}> deleted a reminder for {reminder.message_url} on <t:{int(reminder.datetime.timestamp())}>')
        else:
            for id, command in self.bot.all_commands.items():
                if command.name == 'reminder':
                    command_id = id
                    break

            response_message = (f"There's something wrong with </reminder delete:{command_id}> command, **<@{OWNER_ID}>! FIX ME!**")

        await interaction.response.edit_message(content = response_message, view = None, delete_after=0)

        await interaction.channel.send(response_message)
    
def setup(bot: Bot):
    bot.add_cog(Remind(bot))