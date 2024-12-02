from loguru import logger
from typing import List
from discord import OptionChoice
from tcgdexsdk import TCGdex
from tcgdexsdk.enums import Language
from tcgdexsdk.models.Serie import Serie
from tcgdexsdk.models.Set import Set

class PokedexService:
    def __init__(self):
        self.sdk: TCGdex = TCGdex(Language.EN)
        self.series: Serie | None = None
        self.sets: List[Set] = []

    async def get_all_data(self):
        await self.get_series()
        await self.get_sets()

    async def get_series(self):
        logger.info("Fetching series...")
        self.series = await self.sdk.serie.get("tcgp")
        logger.success("Series fetched successfully!")
    
    async def get_sets(self):
        logger.info("Fetching sets...")

        for set in self.series.sets:
            set_full = await set.get_full_set()
            self.sets.append(set_full)

        logger.success("Sets fetched successfully!")
    
    def get_set_choices(self):
        return [OptionChoice(name=set.name, value=set.id) for set in self.sets]
    
    def get_card_choices(self, set_id: str):
        set = next((set for set in self.sets if set.id == set_id), None)

        if not set:
            return []
        
        return [OptionChoice(name=f"{card.name} [{card.id}]", value=card.id) for card in set.cards]
        