from TTS.api import TTS

def synthesise(text, file_path):

    model_name = "tts_models/en/vctk/vits"

    tts = TTS(model_name, progress_bar=True)

    speaker = tts.speakers[40]
    tts.tts_to_file(text=text, speaker=speaker, file_path=file_path)

if __name__ == "__main__":

    with open('The SEC Cracks Down on Crypto.txt', 'r') as f:
        text = f.read()

    synthesise(text, "The SEC Cracks Down on Crypto.wav")
