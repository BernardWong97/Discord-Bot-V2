import os, discord, requests, html2markdown, urllib.parse
import warnings
from bs4 import MarkupResemblesLocatorWarning
from datetime import datetime, timedelta, timezone
from discord import Embed, ApplicationContext, Option
from discord.ext.pages import Paginator
from discord.ext.commands import Cog, Bot
from utilities.enums import MediaType, MediaFormat, MediaSeason, MediaSource, MediaStatus, Country

warnings.filterwarnings('ignore', category=MarkupResemblesLocatorWarning)

class Anime(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.API_URL = 'https://graphql.anilist.co'
        self.WEB_URL = 'https://anilist.co'

    @discord.slash_command(name="anime", description="List search anime", guild_ids=[int(os.getenv('TEST_GUILD'))], guild_only=True)
    async def list_anime(self, 
                         ctx: ApplicationContext, 
                         search: Option(str, description="Filter by search query", required=False),
                         season: Option(str, description="Filter by the season the anime was released in", choices=MediaSeason.get_choices(), required=False),
                         season_year: Option(int, description="The year of the season. Requires season argument", required=False, max_value=2100, min_value=1940),
                         format: Option(str, description="Filter by the anime's format", choices=MediaFormat.get_choices(), required=False),
                         status: Option(str, description="Filter by the anime's current release status", choices=MediaStatus.get_choices(), required=False),
                         country: Option(str, description="Filter by the anime's country of origin (ISO 3166-1 alpha-2)", required=False),
                         nsfw: Option(bool, description="Filter by if the anime's intended for 18+ adult audiences", required=False),
                         genre: Option(str, description="Filter by anime's genre", required=False),
                         source: Option(str, description="Filter by the anime's format", choices=MediaSource.get_choices(), required=False),
                         ):
        await ctx.defer()

        if season_year is not None and season is None:
            await ctx.respond("Please select a season if you are filtering season year.", ephemeral=True)

        try:
            data = await self._retrieve_anime_list(search=search, season=season, seasonYear=season_year, format=format, status=status, countryOfOrigin=country, isAdult=nsfw, genre=genre, source=source)

            if "errors" in data:
                print(data)
                await ctx.followup.send("There's something wrong with the command")
            else:
                media_list = data["media"]

                embed_list = self._generate_embeds(search, media_list)

                paginator = Paginator(pages=embed_list, timeout=600)
                await paginator.respond(ctx.interaction, ephemeral=False)
        except Exception as e:
            print(e)
            await ctx.respond("There's something wrong with the command")

    async def _retrieve_anime_list(self, **kwargs):
        query_args, media_args, values = self._populate_args(kwargs)

        query = '''
        query ($page: Int, $perPage: Int, $mediaType: MediaType{}) {{
            Page (page: $page, perPage: $perPage) {{
                media(sort: POPULARITY_DESC, type: $mediaType{}) {{
                    format
                    status(version: 2)
                    description
                    season
                    episodes
                    duration
                    countryOfOrigin
                    source(version: 3)
                    genres
                    averageScore
                    meanScore
                    popularity
                    trending
                    favourites
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
                    studios(isMain: true) {{
                        nodes {{
                            name
                            siteUrl
                        }}
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
    
    def _generate_embeds(self, search, media_list) -> list[Embed]:
        embed_list = []

        title_embed = Embed(
            title = f'{search} Anime Search Result' if search is not None else f'This Season\'s Anime List ({datetime.now(timezone(timedelta(hours=8), name="Asia/Kuala_Lumpur")).year} {MediaSeason.get_current_season()})',
            color = 0x0000FF,
            url = f'{self.WEB_URL}/search/anime?search={urllib.parse.quote(search)}' if search is not None else f'{self.WEB_URL}/search/'
        ).set_author(name = "AniList", icon_url="https://avatars.githubusercontent.com/u/18018524?s=200&v=4")

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

            if (len(media["studios"]["nodes"]) != 0):
                embed.set_author(name=media["studios"]["nodes"][0]["name"] or "Unknown", url=media["studios"]["nodes"][0]["siteUrl"] or "")
            else:
                embed.set_author(name="Unknown")

            if media["coverImage"]["medium"]:
                embed.set_thumbnail(url=media["coverImage"]["medium"])

            embed.set_image(url=media["coverImage"]["extraLarge"] or media["coverImage"]["large"] or media["coverImage"]["medium"])

            embed.add_field(name="Episodes", value=media["episodes"] if media["episodes"] is not None else "Unknown", inline=True)
            embed.add_field(name="", value="", inline=True)
            embed.add_field(name="Duration", value=f'{media["duration"]} min' if media["duration"] is not None else "Unknown", inline=True)
            embed.add_field(name="Format", value= MediaFormat.get_value(media["format"]), inline=True)
            embed.add_field(name="Country", value= Country.get_value(media["countryOfOrigin"]), inline=True)
            embed.add_field(name="Status", value= MediaStatus.get_value(media["status"]), inline=True)
            embed.add_field(name="Season", value= MediaSeason.get_value(media["season"]), inline=True)
            embed.add_field(name="Source", value= MediaSource.get_value(media["source"]), inline=True)
            embed.add_field(name="Average Score", value= f'{media["averageScore"]}%' if media["averageScore"] is not None else "Unknown", inline=True)
            embed.add_field(name="Mean Score", value= f'{media["meanScore"]}%' if media["meanScore"] is not None else "Unknown", inline=True)
            embed.add_field(name="Popularity", value= media["popularity"] if media["popularity"] is not None else "Unknown", inline=True)
            embed.add_field(name="NSFW", value= "Yes" if media["isAdult"] else "No", inline=True)

            embed.add_field(name="Genre", value=", ".join(media["genres"]), inline=False)

            start_date = self._format_date(media["startDate"])
            end_date = self._format_date(media["endDate"])

            embed.set_footer(text=f"{start_date} - {end_date}")

            if media["trailer"] and media["trailer"]["site"] == "youtube":
                video_url = f'https://www.youtube.com/watch?v={media["trailer"]["id"]}'
                embed.add_field(name="Trailer", value=f"[Youtube]({video_url})")

            embed_list.append([title_embed, embed])

        return embed_list

    def _format_date(self, date_json) -> str:
        day = f'{date_json["day"]:02d}' if date_json["day"] else "-"
        month = f'{date_json["month"]:02d}' if date_json["month"] else "-"
        year = f'{date_json["year"]:02d}' if date_json["year"] else "-"

        date_str = f"{day}/{month}/{year}"
        return date_str if date_str != '-/-/-' else 'Unknown'
    
    def _populate_args(self, kwargs: dict) -> tuple[str, str, dict]:
        data_type = {
            "search": "String",
            "season": "MediaSeason",
            "seasonYear": "Int",
            "format": "MediaFormat",
            "status": "MediaStatus",
            "countryOfOrigin": "CountryCode",
            "isAdult": "Boolean",
            "genre": "String",
            "source": "MediaSource"
        }

        query_array = [f', ${key}: {data_type[key]}' for key, value in kwargs.items() if value is not None]
        media_array = [f', {key}: ${key}' for key, value in kwargs.items() if value is not None]

        if len(query_array) == 0:
            query_array.append(f', $season: MediaSeason, $seasonYear: Int')
            media_array.append(f', season: $season, seasonYear: $seasonYear')
            kwargs['season'] = MediaSeason.get_current_season()
            kwargs['seasonYear'] = datetime.now(timezone(timedelta(hours=8), name='Asia/Kuala_Lumpur')).year

        query_args = "".join(query_array)
        media_args = "".join(media_array)

        filtered_values = {key: value.upper().replace(' ', '_') if isinstance(value, str) and value != "search" else value for key, value in kwargs.items() if value is not None}

        return (query_args, media_args, filtered_values)

def setup(bot):
    bot.add_cog(Anime(bot))