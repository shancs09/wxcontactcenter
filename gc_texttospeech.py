from google.cloud import texttospeech

# Create a client
client = texttospeech.TextToSpeechClient()

# Set the input text
input_text = """
Virtual agent: Hello! How may I assist you today?
Caller: I'd like to open a new savings account.
Virtual agent: Certainly! Before we proceed, may I have your full name, please?
Caller: Mary Johnson.
Virtual agent: Thank you, Mary. Can you also provide a valid phone number?
Caller: Sure, it's 555-123-4567.
Virtual agent: Great. To proceed with the account opening, we'll need some additional information. Could you please confirm your date of birth?
Caller: December 3, 1990.
Virtual agent: Perfect. Now, for security purposes, could you provide your mother's maiden name?
Caller: Smith.
Virtual agent: Thank you, Mary. I have all the necessary details. A new savings account will be created for you shortly, and the account information will be sent to mary.johnson@example.com. Is there anything else you'd like to inquire about?
Caller: No, that's it. Thank you!
Virtual agent: You're welcome! If you have any further questions, feel free to reach out. Have a wonderful day!
"""

# Set the voice parameters
voice_params = {
    "en-US": {
        "virtual_agent": {"name": "en-US-Wavenet-D", "gender": "MALE"},
        "caller": {"name": "en-US-Wavenet-B", "gender": "FEMALE"}
    }
}

# Split the input text into agent and caller parts
parts = input_text.strip().split("\n")

# Generate audio for each part
audio_files = []
for i, part in enumerate(parts):
    role, text = part.split(":", 1)
    role = role.strip().lower()

    # Determine the voice based on the role
    voice_name = voice_params["en-US"][role]["name"]
    voice_gender = voice_params["en-US"][role]["gender"]

    # Set the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name=voice_name, ssml_gender=voice_gender
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

    # Synthesize speech
    synthesis_input = texttospeech.SynthesisInput(text=text.strip())
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # Save the audio to a file
    output_file = f"output_{i}.wav"
    with open(output_file, "wb") as f:
        f.write(response.audio_content)
    audio_files.append(output_file)

print("Audio files generated:", audio_files)
