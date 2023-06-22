import openai
import asyncio
import json


from dotenv import load_dotenv
import os

load_dotenv()

openai.organization = os.getenv("OPEN_AI_KEY")
openai.api_key = os.getenv("OPEN_AI_ORGANIZATION")


durations_vs_words = {1: "200", 3: "400", 5: "600"}


async def send_reply(ctx, data):
    reply = await ctx.send(data)
    return reply


async def get_video_script(topic, duration, ctx, asset_type="videos"):
    print("num of words", durations_vs_words[duration])

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": (
                    "Give me data for a youtube script in minimum of "
                    + durations_vs_words[duration]
                    + " words about the topic: "
                    + topic
                    + '. Include texts like welcome back to our channel etc. No new lines characters. No quotations. No special characters like , or ? or ! or \\ or " etc. Make sure the data is a single paragraph. '
                    # + ". Give me the response in a json which only contains two properties, the data property which is a string which contains the actual data and the chunks property"
                ),
            }
        ],
    )

    print("completion", completion)
    completion_data = json.loads(str(completion.choices[0].message))["content"]

    print("Completion", completion_data, type(completion_data), len(completion_data))
    await send_reply(ctx, data="🧠 Processing the script...")

    content = (
        "Data: "
        + completion_data
        + ". Truncate the above data into sentences and return a json response with data and sentences properties. Make sure both properties are seperated by a comma. The data property which is the entire string and each sentence should have a sentence property and "
        + (
            " keywords property which should be 3 unique words that explains the end result of each sentence, which I want to use to query stock video related to the sentence. object properties are content and keywords. The keywords should only convey the meaning of the content. Keywords should contain a verb and it should not be sensitive words."
            if (asset_type == "videos")
            else "the query property should always contains two words. One word should always be the name of the person from the sentence and the other word should be any verb or any adjective from the sentence."
        )
        + " No special characters in the response like ? and no other special characters other than alphabets and numbers."
    )

    final = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )

    final = json.loads(str(final))
    final = json.loads(final["choices"][0]["message"]["content"])

    print("final", final)
    print("data", final["data"], len(final["data"]))

    await send_reply(ctx, data="Script - " + final["data"])
    with open("./content.json", "w") as json_file:
        json.dump(final, json_file)
    # segments = json.loads(str(completion_data["chunks"]))
    segments = final["sentences"]

    return segments
