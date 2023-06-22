import whisper
import asyncio
from moviepy.editor import (
    AudioFileClip,
)
import json

model = whisper.load_model("small")


audio_file_path = "./audios/"


async def send_reply(ctx, data):
    reply = await ctx.send(data)
    return reply


async def audio_to_timestamps(audio_file_names, ctx):
    audio_time_stamps = []
    start_time = 0
    finished_files = 0

    sync_message = await send_reply(ctx, "🤖 Syncing audio and script...")

    for audio_filename in audio_file_names:
        asyncio.sleep(0)

        result = model.transcribe(
            audio_file_path + audio_filename, word_timestamps=True
        )
        audio = AudioFileClip(audio_file_path + audio_filename)
        finished_files += 1
        await sync_message.edit(
            content="🤖 Syncing audio and script - "
            + (str(round((finished_files / len(audio_file_names)) * 100)))
            + "%"
        )

        print("time stamp result", result)
        segments = result["segments"]
        words = []

        for segment in segments:
            words.extend([*segment["words"]])
        # audio_time_stamps.extend([*words])

        last_item = len(words) - 1
        for i, segment in enumerate(words):
            audio_time_stamps.append(
                {
                    "word": segment["word"],
                    "start": segment["start"] + start_time,
                    "end": start_time + audio.duration - 0.5
                    if last_item == i
                    else segment["end"] + start_time,
                }
            )
        start_time += audio.duration

    print("audio_time_stamps", audio_time_stamps)

    return audio_time_stamps
