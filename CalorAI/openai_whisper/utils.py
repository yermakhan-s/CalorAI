import whisper
import warnings

warnings.filterwarnings("ignore", category=FutureWarning, module="torch")
# Load the model

def speach_to_text(audio):
    model = whisper.load_model("small")

    # Transcribe the audio file
    result = model.transcribe(audio)

    # Print the transcription
    print(result["text"])
    return result["text"]