import whisper

# Load the model

def speach_to_text(audio):
    model = whisper.load_model("large")

    # Transcribe the audio file
    result = model.transcribe("russian_audio.mp3",)

    # Print the transcription
    print(result["text"])
    return result["text"]