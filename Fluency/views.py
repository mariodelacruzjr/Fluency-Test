from django.shortcuts import render
from .models import Passage
from django.shortcuts import render
from django.http import JsonResponse
import speech_recognition as sr
import wave
import sys
import pyaudio
import speech_recognition as sr
import re

# Create your views here.

def display_passage(request):
    passage=Passage.objects.first()
    text="sample text"
    if request.method == 'POST':
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        RATE = 44100
        RECORD_SECONDS = 10
        p = pyaudio.PyAudio()

        # Find the default input device
        input_device_index = p.get_default_input_device_info()['index']

        # Get the input device's capabilities
        device_info = p.get_device_info_by_index(input_device_index)
        input_channels = device_info['maxInputChannels']

        audio = []
        with wave.open('output.wav', 'wb') as wf:
            wf.setnchannels(input_channels)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)

            stream = p.open(
                format=FORMAT,
                channels=input_channels,  # Use the detected number of input channels
                rate=RATE,
                input=True,
                input_device_index=input_device_index  # Use the default input device
            )

            print('Recording...')
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                wf.writeframes(data)
                audio.append(data)
            print('Done')

            stream.stop_stream()
            stream.close()

        p.terminate()

        # Convert the recorded audio to an AudioData object
        audio_data = sr.AudioData(b''.join(audio), sample_rate=RATE, sample_width=p.get_sample_size(FORMAT))

        # Convert the AudioData to text
        recognizer = sr.Recognizer()
        try:
            text = recognizer.recognize_google(audio_data)
            print("Transcription:", text)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        # Save the transcription to a text file if needed
        with open('transcription.txt', 'w') as text_file:
                text_file.write(text)
    return render(request, 'passage.html', {'passage':passage, 'text': text})

def passage_list(request):
    passages = Passage.objects.all()
    return render(request, 'passage_list.html',{'passages': passages})

def results(request):
    passage = Passage.objects.first()
    
    cleaned_passage_text = remove_punctuation(passage.text.lower())
    
    with open('transcription.txt', 'r') as text_file:
        text = text_file.read()
    
    passage_words = cleaned_passage_text.split()
    
    # Create a list of 0's with one element for each word
    checker = passage_words[:]
    
    # Split the student_text into words
    student_words = text.split()
    
    word_list = ['0' for _ in checker]
    
    for i in range(len(student_words)):
        word1 = student_words[i]
        
        for index, word in enumerate(checker):
            if word == word1 and word_list[index] == '0':
                word_list[index] = '1'
                break
    
    passage_words_and_values = zip(passage_words, word_list)
    words_said_correctly = word_list.count('1')
    
    return render(request, 'results.html', {'passage': cleaned_passage_text, 'text': text, 'words_said_correctly': words_said_correctly, 'passage_words_and_values': passage_words_and_values})


def remove_punctuation(text):
    # Use regular expression to remove non-alphanumeric characters and spaces
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

def capture_audio(request):
    text="sample text"
    if request.method == 'POST':
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        RATE = 44100
        RECORD_SECONDS = 5
        p = pyaudio.PyAudio()

        # Find the default input device
        input_device_index = p.get_default_input_device_info()['index']

        # Get the input device's capabilities
        device_info = p.get_device_info_by_index(input_device_index)
        input_channels = device_info['maxInputChannels']

        audio = []
        with wave.open('output.wav', 'wb') as wf:
            wf.setnchannels(input_channels)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)

            stream = p.open(
                format=FORMAT,
                channels=input_channels,  # Use the detected number of input channels
                rate=RATE,
                input=True,
                input_device_index=input_device_index  # Use the default input device
            )

            print('Recording...')
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                wf.writeframes(data)
                audio.append(data)
            print('Done')

            stream.stop_stream()
            stream.close()

        p.terminate()

        # Convert the recorded audio to an AudioData object
        audio_data = sr.AudioData(b''.join(audio), sample_rate=RATE, sample_width=p.get_sample_size(FORMAT))

        # Convert the AudioData to text
        recognizer = sr.Recognizer()
        try:
            text = recognizer.recognize_google(audio_data)
            text=text.lower()
            print("Transcription:", text)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        # Save the transcription to a text file if needed
        with open('transcription.txt', 'w') as text_file:
                text_file.write(text)
                

    return render(request, 'capture_audio.html', {'text': text})