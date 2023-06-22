from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
    vfx,
    ColorClip,
)
from discord import File
import asyncio
from text_animation import get_text_clips
import re
import os


async def send_reply(ctx, data):
    reply = await ctx.send(data)
    return reply


async def send_video(ctx, video):
    await ctx.send(file=video)


n = 3


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i : i + n]


async def generate_video(
    time_stamps,
    ctx,
    type,
    file_names,
):
    # print("video_time_stamps", file_names, "time_stamps", time_stamps)
    render_video_message = await send_reply(ctx, "📽️ Rendering video...")

    assets = []
    audios = []
    start_time = 0
    for file_name in file_names:
        audio = AudioFileClip("./audios/" + re.sub(r"mp4|jpg+", "wav", file_name))
        # print("audio start", start_time, "audio end", start_time + audio.duration)
        audio = audio.set_start(start_time).set_end(start_time + audio.duration)
        audios.append(audio)

        if type == "videos":
            assets.append(
                VideoFileClip(
                    filename="./stock-videos/" + file_name,
                    audio=False,
                )
                .set_start(start_time)
                .set_end(start_time + audio.duration)
                .fx(vfx.fadein, 0.25)
                .fx(vfx.fadeout, 0.25)
                .resize(height=1920, width=1080)
            )
        else:
            is_image_file = os.path.isfile(
                "./images/" + re.sub(r".mp4|.jpg+", "", file_name) + "/000001.jpg"
            )
            image_path = (
                "./images/"
                + re.sub(r".mp4|.jpg+", "", file_name)
                + ("/000001.jpg" if (is_image_file) else "/000001.png")
            )

            print("is_image_file", is_image_file, "image_path", image_path)
            assets.append(
                ImageClip(image_path)
                .set_start(start_time)
                .set_end(start_time + audio.duration)
                .set_position("center")
                .resize(height=1920, width=1080)
            )
        start_time = start_time + audio.duration

    txt_clips = get_text_clips(time_stamps=time_stamps)
    # txt_clips = []
    # for item in time_stamps:
    # txt_clip = TextClip(
    #     txt=item["word"],
    #     fontsize=75,
    #     color="yellow",
    #     font="Montserrat",
    #     bg_color="black"
    #     # stroke_color="blue",
    # )
    #     txt_clip = (
    #         txt_clip.set_position(("center", 1400))
    #         .set_start(item["start"] - 0.25)
    #         .set_end(item["end"] - 0.25)
    #     )

    #     txt_clips.append(txt_clip)

    # w, h = moviesize = assets.size

    # FINAL ASSEMBLY
    final_audio = CompositeAudioClip([*audios])
    asyncio.sleep(0)

    # chunks = list(divide_chunks([*assets, *txt_clips], 3))
    # print("chunks", chunks)

    # chunk_videos = []
    # for chunk in chunks:
    #     chunk_videos.append(CompositeVideoClip([*chunk]))
    #     asyncio.sleep(0)

    color_clip = color_clip = ColorClip(
        size=(1080, 1920),
        color=[0, 0, 0],
    ).set_duration(final_audio.duration)
    final_video = (
        CompositeVideoClip([color_clip, *assets, *txt_clips])
        .set_audio(final_audio)
        .set_fps(24)
    )

    final_video

    print("Rendering video...")
    asyncio.sleep(0)

    final_video.write_videofile(
        "ai-video.mp4",
    )
    video = File("./ai-video.mp4")
    await send_video(ctx, video)
    await send_reply(ctx, "Video created successfully!")
