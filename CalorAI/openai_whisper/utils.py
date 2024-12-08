# import whisper
# import warnings

# # Suppress specific FutureWarnings from torch
# warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

# def speech_to_text(audio, device="cuda"):
#     """
#     Transcribes an audio file using the Whisper model.
    
#     Args:
#         audio (str): Path to the audio file.
#         device (str): Device to load the model on ('cuda' or 'cpu').
    
#     Returns:
#         str: Transcribed text from the audio.
#     """
#     # Load the Whisper model
#     model = whisper.load_model("small", device=device)
    
#     # Transcribe the audio file
#     result = model.transcribe(audio)
    
#     # Return the transcribed text
#     return result["text"]

# # # Example usage
# # if __name__ == "__main__":
# #     audio_file = "path_to_audio_file.mp3"
# #     transcription = speech_to_text(audio_file)
# #     print(f"Transcription: {transcription}")
