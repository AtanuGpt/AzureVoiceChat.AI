# https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/python/console/speech_sample.py

import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from langchain_openai import OpenAI

load_dotenv()

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

llm = OpenAI(api_key=OPENAI_API_KEY)

speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
speech_config.speech_recognition_language = "en-US"

audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

print("You can speak now. I am listening ...")

speech_recognition_result = speech_recognizer.recognize_once_async().get()

if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
    output = speech_recognition_result.text

    print (output) #User question

    result = llm.invoke(output)

    print (result) # AI Answer
 
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesizar_result = speech_synthesizer.speak_text_async(result).get()

elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))

elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
