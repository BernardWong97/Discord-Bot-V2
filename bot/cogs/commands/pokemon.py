import re
from typing import cast
from typing import List
from discord import Embed, Option, ApplicationContext, utils, AutocompleteContext, SlashCommandGroup
from discord.ext.pages import Paginator
from discord.ext.commands import Cog
from bot.bot_instance import Bot
from tcgdexsdk.enums import Extension, Quality
from tcgdexsdk.models.Set import Set
from tcgdexsdk.models.CardResume import CardResume
from config import GUILD

def _get_set_filter(ctx: AutocompleteContext):
    bot = cast(Bot, ctx.bot)
    return bot.pokedex.get_set_choices()

def _get_card_filter(ctx: AutocompleteContext):
    bot = cast(Bot, ctx.bot)
    return bot.pokedex.get_card_choices(ctx.options.get("set"))

class Pokemon(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    pokemon_group = SlashCommandGroup(name="pokemon", description="Look up any details about Pokémon TCG Pocket", guild_ids=[GUILD])
    set_sub_group = pokemon_group.create_subgroup(name="sets", description="Look up any details about Pokémon TCG Pocket Sets", guild_ids=[GUILD])
    card_sub_group = pokemon_group.create_subgroup(name="cards", description="Look up any details about Pokémon TCG Pocket Cards", guild_ids=[GUILD])

    @pokemon_group.command(name="update", description="Update Pokémon TCG Pocket data", guild_ids=[GUILD])
    async def update(self, ctx: ApplicationContext):
        await ctx.defer()

        await self.bot.pokedex.get_all_data()

        await ctx.followup.send("Pokémon TCG Pocket data has been updated.")

    @set_sub_group.command(name="list", description="List Pokémon TCG Pocket Sets", guild_ids=[GUILD])
    async def list_sets(self, 
                      ctx: ApplicationContext, 
                      ):
        await ctx.defer()

        sets = self.bot.pokedex.sets
        iconUrl = self.bot.pokedex.series.get_logo_url(Extension.PNG)

        embed_list = self._generate_set_embeds(iconUrl, sets)

        if len(embed_list) > 0:
            paginator = Paginator(pages=embed_list, timeout=600)
            await paginator.respond(ctx.interaction, ephemeral=False)
        else:
            no_item_embed = Embed(
                title = "No Pokémon TCG Pocket Sets found",
                color = 0x0000FF,
                url = "https://www.tcgdex.net/database/Pok%C3%A9mon-TCG-Pocket"
            ).set_author(name = "Pokémon TCG Pocket", icon_url=iconUrl)

            await ctx.followup.send(embed=no_item_embed, wait=True)

    @set_sub_group.command(name="get", description="Retrieve a Pokémon TCG Pocket Set", guild_ids=[GUILD])
    async def get_set(self, 
                      ctx: ApplicationContext, 
                      set: Option(str, description="Filter by set", autocomplete=utils.basic_autocomplete(_get_set_filter), required=True)
                      ):
        await ctx.defer()

        if set not in (set.id for set in self.bot.pokedex.sets):
            await ctx.followup.send("Please select from the options provided.")
            return

        set_full = next((iter_set for iter_set in self.bot.pokedex.sets if iter_set.id == set), None)
        
        embed = self._generate_set_embed(set_full)

        await ctx.followup.send(embed=embed, wait=True)

    @card_sub_group.command(name="list", description="List Pokémon TCG Pocket Cards", guild_ids=[GUILD])
    async def list_cards(self, 
                      ctx: ApplicationContext, 
                      set: Option(str, description="Filter by set", autocomplete=utils.basic_autocomplete(_get_set_filter), required=True)
                      ):
        await ctx.defer()

        if set not in (set.id for set in self.bot.pokedex.sets):
            await ctx.followup.send("Please select from the options provided.")
            return
        
        set_full = next((iter_set for iter_set in self.bot.pokedex.sets if iter_set.id == set), None)
        
        embed_list = self._generate_card_embeds(set_full)

        if len(embed_list) > 0:
            paginator = Paginator(pages=embed_list, timeout=600)
            await paginator.respond(ctx.interaction, ephemeral=False)
        else:
            no_item_embed = Embed(
                title = "No Pokémon TCG Pocket Cards found",
                color = 0x0000FF,
                url = "https://www.tcgdex.net/database/Pok%C3%A9mon-TCG-Pocket/" + set_full.name.replace(" ", "-")
            ).set_author(name = "Pokémon TCG Pocket", icon_url=set_full.get_logo_url(Extension.PNG))

            await ctx.followup.send(embed=no_item_embed, wait=True)

    @card_sub_group.command(name="get", description="Retrieve a Pokémon TCG Pocket Card", guild_ids=[GUILD])
    async def get_card(self, 
                      ctx: ApplicationContext, 
                      set: Option(str, description="Filter by set", autocomplete=utils.basic_autocomplete(_get_set_filter), required=True)
                      ):
        await ctx.defer()

        if set not in (set.id for set in self.bot.pokedex.sets):
            await ctx.followup.send("Please select from the options provided.")
            return
        
        set_full = next((iter_set for iter_set in self.bot.pokedex.sets if iter_set.id == set), None)
        
        embed_list = self._generate_card_embeds(set_full)

        if len(embed_list) > 0:
            paginator = Paginator(pages=embed_list, timeout=600)
            await paginator.respond(ctx.interaction, ephemeral=False)
        else:
            no_item_embed = Embed(
                title = "No Pokémon TCG Pocket Cards found",
                color = 0x0000FF,
                url = "https://www.tcgdex.net/database/Pok%C3%A9mon-TCG-Pocket/" + set_full.name.replace(" ", "-")
            ).set_author(name = "Pokémon TCG Pocket", icon_url=set_full.get_logo_url(Extension.PNG))

            await ctx.followup.send(embed=no_item_embed, wait=True)

    @card_sub_group.command(name="id", description="Retrieve a Pokémon TCG Pocket Card by ID", guild_ids=[GUILD])
    async def get_card_by_id(self, 
                      ctx: ApplicationContext,
                      id: Option(str, description="Filter by card ID", required=True)
                      ):
        await ctx.defer()

        found = False

        for set in self.bot.pokedex.sets:
            card = next((iter_card for iter_card in set.cards if iter_card.id == id), None)

            if card:
                embed = self._generate_card_embed(card)
                await ctx.followup.send(embed=embed, wait=True)
                found = True
                break

        if not found:
            await ctx.followup.send(f"Card by ID `{id}` not found.")

    def _generate_set_embed(self, set: Set) -> Embed:
        embed = Embed(
                title = set.name,
                color = 0xFF00FF
            )

        embed.set_image(url=set.get_logo_url(Extension.PNG))
        embed.set_thumbnail(url=set.get_symbol_url(Extension.PNG))
        embed.set_author(name = "Pokémon TCG Pocket", icon_url=self.bot.pokedex.series.get_logo_url(Extension.PNG))

        embed.add_field(name="Release Date", value=set.releaseDate if set.releaseDate else "Unknown", inline=False)
        embed.add_field(name="Series", value=set.serie.name if set.serie else "Unknown", inline=False)
        embed.add_field(name="Card Count", value=str(set.cardCount.total) if set.cardCount else "Unknown", inline=False)

        return embed

    def _generate_set_embeds(self, sets: List[Set]) -> List[Embed]:
        embed_list = []

        title_embed = Embed(
            title="List of Pokémon TCG Pocket Sets",
            color=0x0000FF,
            url = "https://www.tcgdex.net/database/Pok%C3%A9mon-TCG-Pocket"
        ).set_author(name = "Pokémon TCG Pocket", icon_url=self.bot.pokedex.series.get_logo_url(Extension.PNG))

        for set in sets:
            embed = self._generate_set_embed(set)

            embed_list.append([title_embed, embed])

        return embed_list
    
    def _generate_card_embed(self, card: CardResume) -> Embed:
        embed = Embed(
            title = card.name,
            description = "ID: " + card.id if card.id else "Unknown ID",
            color = 0xFF00FF
        )

        embed.set_image(url=card.get_image_url(Quality.HIGH, Extension.PNG))
        embed.set_author(name = "Pokémon TCG Pocket", icon_url=self.bot.pokedex.series.get_logo_url(Extension.PNG))

        return embed

    def _generate_card_embeds(self, set: Set) -> List[Embed]:
        embed_list = []

        title_embed = Embed(
            title=f"List of Pokémon TCG Pocket {set.name} Cards",
            color=0x0000FF,
            url = "https://www.tcgdex.net/database/Pok%C3%A9mon-TCG-Pocket/" + set.name.replace(" ", "-")
        ).set_author(name = "Pokémon TCG Pocket", icon_url=set.get_logo_url(Extension.PNG))

        for card in set.cards:
            embed = self._generate_card_embed(card)
            
            embed_list.append([title_embed, embed])

        return embed_list
    
def setup(bot: Bot):
    bot.add_cog(Pokemon(bot))