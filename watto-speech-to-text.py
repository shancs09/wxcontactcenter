import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
import threading
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Set up the authentication
authenticator = IAMAuthenticator('EVbgkVy_v-9PfBfZvHukYnW9bbq1-OGen1qA4taporwV')  # Replace <api_key> with your API key
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url('https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/a2fb20ab-8b68-4ba2-b88a-34a972e0afa3')  # Replace <service_url> with your service URL

# Set the audio file path
audio_file = '/Users/shan/Documents/Assets Backup/Watsonx-Support Ticket Insights/combined_audio.wav'  # Replace with your audio file path

model = speech_to_text.get_model('en-US_BroadbandModel').get_result()
print(json.dumps(model, indent=2))

with open(join(dirname(__file__), '/Users/shan/Documents/Assets Backup/Watsonx-Support Ticket Insights/output_0.wav'),
          'rb') as audio_file:
    print(json.dumps(
        speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/wav',
            timestamps=True,
            word_confidence=True).get_result(),
        indent=2))


# Perform transcription
with open(audio_file, 'rb') as audio_file:
    response = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/wav',
        model='en-US_BroadbandModel',
        continuous=True
    ).get_result()

# Extract the transcriptions from the response
transcriptions = [result['alternatives'][0]['transcript'] for result in response['results']]

# # Print the transcriptions
# for transcription in transcriptions:
#     print(transcription)

# Create a dictionary to store transcriptions
data = {
    'transcriptions': transcriptions
}

# Save transcriptions to a JSON file
output_file = 'transcriptions.json'
with open(output_file, 'w') as f:
    json.dump(data, f, indent=4)

print('Transcriptions saved to', output_file)