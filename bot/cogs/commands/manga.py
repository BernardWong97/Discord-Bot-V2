import discord, requests, html2markdown, urllib.parse, warnings, calendar
from loguru import logger
from bs4 import MarkupResemblesLocatorWarning
from datetime import datetime
from discord import Embed, ApplicationContext, Option, OptionChoice
from discord.ext.pages import Paginator
from discord.ext.commands import Cog
from bot.bot_instance import Bot
from bot.utilities.enums import MediaFormat, MediaSource, MediaStatus, Country
from config import GUILD, OWNER_ID, TIMEZONE

warnings.filterwarnings('ignore', category=MarkupResemblesLocatorWarning)

class Manga(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.API_URL = 'https://graphql.anilist.co'
        self.WEB_URL = 'https://anilist.co'

    @discord.slash_command(name="manga", description="List search manga", guild_ids=[GUILD])
    async def list_manga(self, 
                         ctx: ApplicationContext,
                         format: Option(str, description="Filter by the manga's format", choices=MediaFormat.get_choices(), required=False),
                         status: Option(str, description="Filter by the manga's current release status", choices=MediaStatus.get_choices(), required=False),
                         country: Option(str, description="Filter by the manga's country of origin (ISO 3166-1 alpha-2)", required=False),
                         nsfw: Option(bool, description="Filter by if the manga's intended for 18+ adult audiences", required=False),
                         genre: Option(str, description="Filter by manga's genre", required=False),
                         source: Option(str, description="Filter by the manga's source", choices=MediaSource.get_choices(), required=False),
                         month: Option(int, description="Filter by the month the manga was released in", required=False, choices=[OptionChoice(name=month_name, value=i) for i, month_name in enumerate(calendar.month_name) if i != 0]),
                         year: Option(int, description="Filter by the year the manga was released in", required=False, max_value=2100, min_value=1940),
                         search: Option(str, description="Filter by search query", required=False)
                         ):
        await ctx.defer()

        try:
            params = {"search": search, "year": year, "month": month, "format": format, "status": status, "genre": genre, "countryOfOrigin": country, "isAdult": nsfw, "source": source}
            data = await self._retrieve_media_list(params.copy())

            if "errors" in data:
                logger.error(data)

                for id, command in self.bot.all_commands.items():
                    if command.name == 'manga':
                        command_id = id
                        break
                    
                await ctx.followup.send(f"There's something wrong with </manga:{command_id}> command, **<@{OWNER_ID}>! FIX ME!**")
            else:
                media_list = data["media"]

                embed_list = self._generate_embeds(params, media_list)

                if len(embed_list) > 0:
                    paginator = Paginator(pages=embed_list, timeout=600)
                    await paginator.respond(ctx.interaction, ephemeral=False)
                else:
                    no_item_embed = Embed(
                        title = f'No Manga Found',
                        color = 0x0000FF,
                        url = f'{self.WEB_URL}/search/manga'
                    ).set_author(name = "AniList", icon_url="https://avatars.githubusercontent.com/u/18018524?s=200&v=4")

                    for key, value in params.items():
                        if value is not None:
                            no_item_embed.add_field(name=key, value=str(value), inline=True)

                    await ctx.followup.send(embed=no_item_embed)
        except MangaException as e:
            await ctx.respond(e)
        except Exception as e:
            logger.error(e)

            for id, command in self.bot.all_commands.items():
                if command.name == 'manga':
                    command_id = id
                    break
                
            await ctx.followup.send(f"There's something wrong with </manga:{command_id}> command, **<@{OWNER_ID}>! FIX ME!**")

    async def _retrieve_media_list(self, params: dict):
        query_args, media_args, values = self._populate_args(params)

        query = '''
        query ({}) {{
            Page (page: 1, perPage: 50) {{
                media(sort: POPULARITY_DESC, type: MANGA{}) {{
                    format
                    status(version: 2)
                    description
                    chapters
                    volumes
                    countryOfOrigin
                    source(version: 3)
                    genres
                    averageScore
                    meanScore
                    popularity
                    isAdult
                    siteUrl
                    title {{
                        romaji(stylised: true)
                        english(stylised: true)
                        native(stylised: true)
                    }}
                    startDate {{
                        year
                        month
                        day
                    }}
                    endDate {{
                        year
                        month
                        day
                    }}
                    trailer {{
                        id
                        site
                    }}
                    coverImage {{
                        extraLarge
                        large
                        medium
                        color
                    }}
                }}
            }}
        }}
        '''.format(query_args, media_args)

        response = requests.post(self.API_URL, json={'query': query, 'variables': values})

        data = response.json()

        if "errors" in data:
            return data
        else:
            return data["data"]["Page"]
    
    def _generate_embeds(self, params, media_list) -> list[Embed]:
        embed_list = []

        title_embed = Embed(
            title = f'This Year\'s Manga List ({datetime.now(TIMEZONE).year})' if all(value is None for value in params.values()) else 'Manga Search Result',
            color = 0x0000FF,
            url = f'{self.WEB_URL}/search/manga?search={urllib.parse.quote(params["search"])}' if params["search"] is not None else f'{self.WEB_URL}/search/manga'
        ).set_author(name = "AniList", icon_url="https://avatars.githubusercontent.com/u/18018524?s=200&v=4")

        for key, value in params.items():
            if value is not None:
                title_embed.add_field(name=key, value=str(value), inline=True)

        for media in media_list:
            romanji = media["title"]["romaji"]
            english = media["title"]["english"]

            description = f"{romanji}\n{english}\n\n" if romanji and english else english or ""
            description += f"\n\n{html2markdown.convert(media['description'])}" if media['description'] is not None else ""

            embed = Embed(
                title = media["title"]["native"] or media["title"]["romanji"] or media["title"]["english"],
                colour = int(media["coverImage"]["color"][1:], 16) if media["coverImage"]["color"] else 0xFF00FF,
                url = media["siteUrl"],
                description = description
            )

            if media["coverImage"]["medium"]:
                embed.set_thumbnail(url=media["coverImage"]["medium"])

            embed.set_image(url=media["coverImage"]["extraLarge"] or media["coverImage"]["large"] or media["coverImage"]["medium"])

            embed.add_field(name="Chapters", value=media["chapters"] if media["chapters"] is not None else "Unknown", inline=True)
            embed.add_field(name="", value="", inline=True)
            embed.add_field(name="Volumes", value=media["volumes"] if media["volumes"] is not None else "Unknown", inline=True)
            embed.add_field(name="Format", value= MediaFormat.get_value(media["format"]), inline=True)
            embed.add_field(name="Country", value= Country.get_value(media["countryOfOrigin"]), inline=True)
            embed.add_field(name="Status", value= MediaStatus.get_value(media["status"]), inline=True)
            embed.add_field(name="Source", value= MediaSource.get_value(media["source"]), inline=True)
            embed.add_field(name="Average Score", value= f'{media["averageScore"]}%' if media["averageScore"] is not None else "Unknown", inline=True)
            embed.add_field(name="Mean Score", value= f'{media["meanScore"]}%' if media["meanScore"] is not None else "Unknown", inline=True)
            embed.add_field(name="Popularity", value= media["popularity"] if media["popularity"] is not None else "Unknown", inline=True)
            embed.add_field(name="", value="", inline=True)
            embed.add_field(name="NSFW", value= "Yes :underage:" if media["isAdult"] else "No", inline=True)
            embed.add_field(name="Genre", value="\n".join(media["genres"]), inline=True)

            start_date = self._format_date(media["startDate"])
            end_date = self._format_date(media["endDate"])

            embed.set_footer(text=f"{start_date} - {end_date}")

            if media["trailer"] and media["trailer"]["site"] == "youtube":
                embed.add_field(name='', value='', inline=True)
                video_url = f'https://www.youtube.com/watch?v={media["trailer"]["id"]}'
                embed.add_field(name="Trailer", value=f"[Youtube :tv:]({video_url})", inline=True)

            embed_list.append([title_embed, embed])

        return embed_list

    def _format_date(self, date_json) -> str:
        day = f'{date_json["day"]:02d}' if date_json["day"] else "?"
        month = f'{date_json["month"]:02d}' if date_json["month"] else "?"
        year = f'{date_json["year"]:02d}' if date_json["year"] else "?"

        date_str = f"{day}/{month}/{year}"
        return date_str if date_str != '?/?/?' else 'Unknown'
    
    def _populate_args(self, kwargs: dict) -> tuple[str, str, dict]:
        data_type = {
            "search": "String",
            "startDate_greater": "FuzzyDateInt",
            "startDate_lesser": "FuzzyDateInt",
            "format": "MediaFormat",
            "status": "MediaStatus",
            "countryOfOrigin": "CountryCode",
            "isAdult": "Boolean",
            "genre": "String",
            "source": "MediaSource"
        }

        query_array = [f'${key}: {data_type[key]}' for key, value in kwargs.items() if value is not None and key != "year" and key != "month"]
        media_array = [f', {key}: ${key}' for key, value in kwargs.items() if value is not None and key != "year" and key != "month"]

        if kwargs["countryOfOrigin"] is not None and Country.get_value(kwargs["countryOfOrigin"]) == "Unknown":
            raise MangaException(f'`{kwargs["countryOfOrigin"]}` is not a valid country code')
        
        if kwargs["year"] is not None:
            start_date = f'{kwargs["year"]}'.ljust(8, '0')
            end_date = f'{kwargs["year"] + 1}'.ljust(8, '0')

            if kwargs["month"] is not None:
                start_date = f'{kwargs["year"]}{kwargs["month"]}'.ljust(8, '0')
                end_date = f'{kwargs["year"] + 1}{kwargs["month"]}'.ljust(8, '0')
                del kwargs["month"]
            
            query_array.append(f'$startDate_greater: FuzzyDateInt, $startDate_lesser: FuzzyDateInt')
            media_array.append(f', startDate_greater: $startDate_greater, startDate_lesser: $startDate_lesser')
            del kwargs["year"]

            kwargs["startDate_greater"] = int(start_date)
            kwargs["startDate_lesser"] = int(end_date)
        elif kwargs["month"] is not None:
            this_year = datetime.now(TIMEZONE).year
            end_year = this_year + 1
            end_month = kwargs["month"] + 1
            
            if kwargs["month"] == 12:
                end_year += 1
                end_month = 1

            start_date = f'{this_year}{kwargs["month"]:02d}'.ljust(8, '0')
            end_date = f'{end_year}{end_month:02d}'.ljust(8, '0')
            query_array.append(f'$startDate_greater: FuzzyDateInt, $startDate_lesser: FuzzyDateInt')
            media_array.append(f', startDate_greater: $startDate_greater, startDate_lesser: $startDate_lesser')
            del kwargs["month"]

            kwargs["startDate_greater"] = int(start_date)
            kwargs["startDate_lesser"] = int(end_date)
        elif kwargs["search"] is None:
            this_year = datetime.now(TIMEZONE).year
            start_date = f'{this_year}'.ljust(8, '0')
            end_date = f'{this_year + 1}'.ljust(8, '0')

            query_array.append(f'$startDate_greater: FuzzyDateInt, $startDate_lesser: FuzzyDateInt')
            media_array.append(f', startDate_greater: $startDate_greater, startDate_lesser: $startDate_lesser')
            kwargs["startDate_greater"] = int(start_date)
            kwargs["startDate_lesser"] = int(end_date)

        if len(query_array) == 0:
            query_array.append(f'$startDate_greater: FuzzyDateInt, $startDate_lesser: FuzzyDateInt')
            media_array.append(f', startDate_greater: $startDate_greater, startDate_lesser: $startDate_lesser')
            kwargs['startDate_greater'] = int(f"{datetime.now(TIMEZONE).year}".ljust(8, '0'))
            kwargs['startDate_lesser'] = int(f"{datetime.now(TIMEZONE).year + 1}".ljust(8, '0'))

        query_args = ", ".join(query_array)
        media_args = "".join(media_array)

        filtered_values = {key: value.upper().replace(' ', '_') if isinstance(value, str) and value != "search" else value for key, value in kwargs.items() if value is not None}

        return (query_args, media_args, filtered_values)

def setup(bot: Bot):
    bot.add_cog(Manga(bot))

class MangaException(Exception):
    pass