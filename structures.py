from discord.ext.commands import Context, Bot
from discord import Message

from json import load

with open("languages.json", encoding="UTF-8") as file:
    content = load(file)

REFERENCE_NOT_FOUND = "Reference not found for this message."

bot_language = "pt-br"


class MyContext(Context):
    def get_language(self) -> str:
        return bot_language
    
    def get_reference(self, name: str) -> dict:
        return content[self.invoked_with][name]

    async def send(self, reference: dict, *, place_holder: dict={}):
        language = self.get_language()
        message = reference.pop(language, {})

        content = message.pop("content", REFERENCE_NOT_FOUND).format(**place_holder)
        embed = message.pop("embed", None)

        await super().send(content=content, embed=embed)


class MyBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.languages = ["pt-br", "english"]
    
    @property
    def language(self) -> str:
        return bot_language

    @language.setter
    def language(self, value):
        global bot_language
        bot_language = value
    
    async def process_commands(self, message: Message):
        if message.author.bot:
            return

        ctx = await self.get_context(message, cls=MyContext)
        await self.invoke(ctx)
