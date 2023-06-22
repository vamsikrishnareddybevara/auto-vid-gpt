import discord
import responses
from threading import Timer
from discord.ext import commands
from discord.ui import Button, View


async def button_callback(interaction):
    await interaction.response.send_message("You clicked the button!")


async def send_message(ctx, message):
    try:
        response = await responses.handle_response(ctx, message)
        await message.author.send(response)
        # Send a message with our View class that contains the button

        # button1 = Button(
        #     label="Portrait",
        #     style=discord.ButtonStyle.green,
        #     emoji="😍",
        #     # button_callback=button_callback,
        # )

        # button1.callback = button_callback
        # button2 = Button(
        #     label="Landscape",
        #     style=discord.ButtonStyle.red,
        #     emoji="😁",
        #     # button_callback=button_callback,
        # )
        # button2.callback = button_callback

        # view = View()

        # view.add_item(button1)
        # view.add_item(button2)
        # await ctx.send("This is a button!", view=view)
        # await ctx.send(response)

        # r = Timer(1.0, message.author.send, (()"hello"))
        # t = Timer(3, message.author.send, "python")
        # r.start()
        # t.start()
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = "MTExNjMyNDAzOTQ5Mzk0NzQ0Mw.GEEiEd.FLWAYO3vRV6riDIiLkcUtpQkMnOdgkvx9ti7nk"
    # client = discord.Client(intents=discord.Intents.default())
    bot = commands.Bot(command_prefix="$", intents=discord.Intents.default())

    @bot.event
    async def on_ready():
        print(f"Bot is running")

    @bot.event
    async def on_button_click(interaction):
        print("on button click", interaction.data)

    @bot.command(pass_context=True)
    async def topic(ctx, message):
        print(ctx, message)
        # if message.author == client.user:
        #     return
        # username = str(message.author)
        # user_message = str(message.content)
        # channel = str(message.channel)

        # print(f"{username} said: '{user_message}' ({channel})")

        # if user_message[0] == "?":
        #     user_message = user_message[1:]
        await send_message(
            ctx,
            message,
        )

    # else:
    #     await send_message(
    #         message,
    #         user_message,
    #     )

    bot.run(TOKEN)
    # client.run(TOKEN)


run_discord_bot()
