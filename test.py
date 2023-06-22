from moviepy.editor import (
    VideoFileClip,
    CompositeVideoClip,
    TextClip,
    ImageClip,
    ColorClip,
)

import asyncio
from PIL import Image
from moviepy.video.fx.resize import resize


async def send_reply(ctx, data):
    reply = await ctx.send(data)
    return reply


ukulele = VideoFileClip("./test.mp4")

color_clip = ColorClip(
    size=(1080, 1920),
    color=[0, 0, 0],
).set_duration(10)


txt_clip = TextClip(
    txt="hELLO",
    fontsize=75,
    color="yellow",
    font="Montserrat",
    bg_color="black"
    # stroke_color="blue",
)


imageclip = (
    ImageClip("./dummy.png")
    .set_position("center")
    .set_start(0)
    .set_duration(7)
    .resize(height=1920, width=1080)
)


final_video = CompositeVideoClip([color_clip, txt_clip]).set_duration(5).set_fps(24)
final_video.write_videofile("./ukulele_test.mp4")
