from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pydub import AudioSegment

# Set up the authentication
authenticator = IAMAuthenticator('2mhLqtl5oe2-Kclhyg1C79xpG9sulTy1WFcWUkzutLHa')  # Replace <api_key> with your API key
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url('https://api.us-south.text-to-speech.watson.cloud.ibm.com/instances/77edba93-33f3-4dda-ac24-e284b479a245')  # Replace <service_url> with your service URL

# Set the input text
input_text = """
Virtual agent: Hello, how can I assist you today?
Caller: I believe there has been a fraudulent transaction on my credit card.
Virtual agent: I'm sorry to hear that. To investigate the matter, I will need some details. Please provide your full name, credit card number, and the transaction details that you suspect are fraudulent.
Caller: My name is Alex Smith, my credit card number is XXXX-XXXX-XXXX-1234, and there was a transaction of $500 at an unknown online store.
Virtual agent: Thank you for providing the information, Alex. I will immediately flag this transaction as suspicious and initiate an investigation. We will contact you shortly with further updates and assist you in resolving this issue. Is there anything else I can help you with?
"""

# Split the input text into agent and caller parts
parts = input_text.strip().split("\n")
print(" ")
print(" ")
print("Transctipts Sample")
# Set the voice parameters
voice_params = {
    "virtual agent": {"voice": "en-US_AllisonVoice"},
    "caller": {"voice": "en-US_MichaelV2Voice"}
}

# Generate audio for each part
audio_files = []
for i, part in enumerate(parts):
    print(i)
    print(part)
    role, text = part.split(":", 1)
    role = role.strip().lower()
    # Determine the voice based on the role
    voice = voice_params[role]["voice"]
    # print(voice)
    # Synthesize speech
    response = text_to_speech.synthesize(text, accept='audio/wav', voice=voice).get_result()
    # Save the audio to a file
    output_file = f"output_{i}.wav"
    with open(output_file, "wb") as audio_file:
        audio_file.write(response.content)
    audio_files.append(output_file)
    # break
# print("Audio files generated:", audio_files)

# audio_files=['output_0.wav', 'output_1.wav', 'output_2.wav', 'output_3.wav', 'output_4.wav', 'output_5.wav', 'output_6.wav', 'output_7.wav', 'output_8.wav', 'output_9.wav', 'output_10.wav', 'output_11.wav', 'output_12.wav']

# Initialize an empty AudioSegment object
combined_audio = AudioSegment.silent(duration=0)

# Iterate over the audio files and append them to the combined_audio object
for file in audio_files:
    audio_segment = AudioSegment.from_file(file)
    combined_audio += audio_segment

# Export the combined audio to a file
combined_audio.export("combined_audio.wav", format="wav")
