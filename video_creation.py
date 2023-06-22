import openai
from media import get_stock_video
from tts import text_to_audio
import re
from timestamps import audio_to_timestamps
from main import generate_video
import asyncio
from discord.ui import Button, View
import discord
from video_script import get_video_script
from images_creation import generate_images
from clean_data import remove_files_and_folders
import json

PEXELS_API_KEY = "JjFJ2eQuHVX6KZypkccCzuPPZCiBHGQoinIUZFcRFosBU3GSm9Stl6IS"

from pexelsapi.pexels import Pexels

openai.organization = "org-7iXwOHzScsZkPTRhBL4Prh4N"
openai.api_key = "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"


async def send_reply(ctx, data):
    reply = await ctx.send(data)
    return reply


async def generate_stock_videos(segments, ctx, time_stamps):
    print("Generating stock videos...")
    stock_videos_message = await send_reply(ctx, "🔉 Generating stock videos - 0%")
    video_file_names = []
    asyncio.sleep(0)
    segments_finished = 0
    for segment in segments:
        asyncio.sleep(0)
        segments_finished += 1
        await stock_videos_message.edit(
            content="📽️ Generating stock videos - "
            + (str(round((segments_finished / len(segments)) * 100)))
            + "%"
        )
        file_name = get_stock_video(
            re.sub(r"\"", "", segment["sentence"]), segment["keywords"]
        )
        video_file_names.append(file_name)

    print("📽️ Generating video...")
    asyncio.sleep(0)

    await generate_video(
        time_stamps=time_stamps, ctx=ctx, type="videos", file_names=video_file_names
    )


async def generate_stock_images(segments, ctx, time_stamps):
    print("Generating stock images...")
    stock_images_message = await send_reply(ctx, "🖼️ Generating images - 0%")
    image_file_names = []
    asyncio.sleep(0)
    segments_finished = 0

    for segment in segments:
        asyncio.sleep(0)
        segments_finished += 1
        await stock_images_message.edit(
            content="🖼️ Generating images - "
            + (str(round((segments_finished / len(segments)) * 100)))
            + "%"
        )
        file_name = generate_images(
            re.sub(r"\"", "", segment["sentence"]), segment["query"]
        )
        image_file_names.append(file_name)

    print("📽️ Generating video...", image_file_names)
    asyncio.sleep(0)

    await generate_video(
        time_stamps=time_stamps, ctx=ctx, type="images", file_names=image_file_names
    )


async def generate_audio_data(ctx, voice, segments, type):
    audio_message = await send_reply(ctx, " 🔉  Generating audio - 0%")
    with open("./segments.json", "w") as json_file:
        json.dump(segments, json_file)
    audio_file_names = []
    segments_finished = 0
    for segment in segments:
        asyncio.sleep(0)
        file_name = segment["query"] if (type == "images") else ""
        audio_file_name = text_to_audio(
            text=re.sub(r"\?|\!|\,|\'|\"|\:|\/|\.|\\+", "", segment["sentence"]),
            voice=voice,
            file_name=file_name,
            type=type,
        )
        segments_finished += 1
        print("segments_finished", segments_finished, "segments", len(segments))
        await audio_message.edit(
            content=" 🔉  Generating audio - "
            + (str(round((segments_finished / len(segments)) * 100)))
            + "%"
        )
        audio_file_names.append(audio_file_name)
    segments_finished = 0

    print("Identifying timestamps for video editing...")
    asyncio.sleep(0)

    time_stamps = await audio_to_timestamps(audio_file_names, ctx=ctx)

    if type == "videos":
        await generate_stock_videos(ctx=ctx, segments=segments, time_stamps=time_stamps)
    else:
        await generate_stock_images(ctx=ctx, segments=segments, time_stamps=time_stamps)
        print("generate_stock_images")


async def get_voice_type(ctx, topic, duration, segments, type):
    print("duration", duration, "topic", topic)

    async def button_callback(interaction):
        print(
            "interaction", interaction.data, interaction.id, interaction.message.content
        )
        await interaction.response.send_message(
            "Voice selected - "
            + ("👨" if (interaction.data["custom_id"] == "male") else "👩")
        )
        # self.disable_all_items()
        asyncio.sleep(0)
        await generate_audio_data(
            ctx=ctx, voice=interaction.data["custom_id"], segments=segments, type=type
        )

    button1 = Button(
        label="Male", style=discord.ButtonStyle.green, emoji="👨", custom_id="male"
    )

    button1.callback = button_callback
    button2 = Button(
        label="Female",
        style=discord.ButtonStyle.blurple,
        emoji="👩",
        custom_id="female",
    )
    button2.callback = button_callback

    view = View()

    view.add_item(button1)
    view.add_item(button2)
    await ctx.send("Choose audio voice 🔊", view=view)

    print("Generating audio...", int(duration))
    asyncio.sleep(0)


async def get_asset_type(ctx, topic, duration):
    print("duration", duration, "topic", topic)

    async def button_callback(interaction):
        print(
            "interaction",
            interaction.data,
            interaction.id,
            interaction.message.content,
        )
        await interaction.response.send_message(
            "Asset type selected - " + interaction.data["custom_id"]
        )
        await send_reply(ctx, data="Generating data...")
        # self.disable_all_items()
        segments = await get_video_script(
            topic, int(duration), ctx, asset_type=interaction.data["custom_id"]
        )
        await get_voice_type(
            ctx=ctx,
            duration=duration,
            topic=topic,
            segments=segments,
            type=interaction.data["custom_id"],
        )

        print("generate_stock_images")

    button1 = Button(
        label="Images", style=discord.ButtonStyle.green, emoji="🖼️", custom_id="images"
    )

    button1.callback = button_callback
    button2 = Button(
        label="Stock videos",
        style=discord.ButtonStyle.blurple,
        emoji="📽️",
        custom_id="videos",
    )
    button2.callback = button_callback

    view = View()

    view.add_item(button1)
    view.add_item(button2)
    await ctx.send("Choose assets 🧬", view=view)


async def video_duration(ctx, topic):
    async def button_callback(interaction):
        print(
            "interaction",
            interaction.data,
            interaction.id,
            interaction.message.content,
            # "self",
            # self,
        )
        await interaction.response.send_message(
            "Duration selected - " + interaction.data["custom_id"] + " min"
        )
        # self.disable_all_items()

        await get_asset_type(
            topic=topic, ctx=ctx, duration=interaction.data["custom_id"]
        )
        asyncio.sleep(0)

    button1 = Button(
        label="1 min", style=discord.ButtonStyle.green, emoji="😍", custom_id="1"
    )

    button1.callback = button_callback
    button2 = Button(
        label="3 min",
        style=discord.ButtonStyle.blurple,
        emoji="😁",
        custom_id="3",
    )
    button2.callback = button_callback

    button3 = Button(
        label="5 min", style=discord.ButtonStyle.grey, emoji="😎", custom_id="5"
    )
    button3.callback = button_callback

    view = View()

    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    await ctx.send("Choose video duration ⌚", view=view)


async def create_video(topic, ctx):
    remove_files_and_folders("./audios")
    remove_files_and_folders("./images")
    remove_files_and_folders("./stock-videos")
    await video_duration(ctx, topic)
