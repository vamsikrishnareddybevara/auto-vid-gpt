from TTS.api import TTS
import re

# Init TTS
tts = TTS("tts_models/en/vctk/vits")

base_path = "./audios/"


def text_to_audio(text, voice, file_name, type):
    # Text to speech to a file

    new_file_name = str(" ".join(line.strip() for line in file_name.splitlines()))
    single_line_text = str(" ".join(line.strip() for line in text.splitlines()))
    print("Sentence - ", single_line_text)
    audio_file_name = str(
        re.sub(
            r"\?|\!|\,|\'|\"|\:|\/|\.|\\+",
            "",
            (single_line_text if (type == "videos") else new_file_name),
        )
        + ".wav"
    ).replace(" ", "")
    tts.tts_to_file(
        text=single_line_text,
        speaker="p317" if (voice == "male") else "p270",
        file_path=base_path + audio_file_name,
    )
    return audio_file_name
