from video_creation import create_video


async def handle_response(ctx, message):
    p_message = message

    await create_video(topic=p_message, ctx=ctx)
