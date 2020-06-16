from asyncio import TimeoutError

from structures import MyBot

bot = MyBot(command_prefix=';')

@bot.event
async def on_ready():
    print("I'M READY!")

@bot.command(name="hello")
async def hello_command(ctx):
    ph = {"author": ctx.author.mention}

    initial_reference = ctx.get_reference("initial-message")
    final_reference = ctx.get_reference("final-message")
    timeout_reference = ctx.get_reference("timeout-message")

    await ctx.send(initial_reference, place_holder=ph)
    
    def check(message):
        return message.channel == ctx.channel and message.author == ctx.author
    
    try:
        response = await bot.wait_for("message", timeout=30, check=check)
    except TimeoutError:
        await ctx.send(timeout_reference, place_holder=ph)
    else:
        await ctx.send(final_reference, place_holder=ph)

@bot.command(name="change")
async def change_command(ctx, language: str):
    ph = {"language": language}

    success_reference = ctx.get_reference("success-message")
    unsuccess_reference = ctx.get_reference("unsuccess-message")

    if language in bot.languages:
        bot.language = language
        await ctx.send(success_reference, place_holder=ph)
    else:
        await ctx.send(unsuccess_reference, place_holder=ph)

bot.run("")
