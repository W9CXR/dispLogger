import sys
import pyaudio
import audioop
import speech_recognition as sr

# TODO
# Add database for logged calls
# API endpoint to retrive calls

RECORD_SECONDS = 5
CHUNK = 1024 
RATE = 44100

# Listens for audio on the mic line
def listenForAudio(thresholdLevel):
    audioLevel = 0

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                    channels=1 if sys.platform == 'darwin' else 2,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)

    while True:
        audioLevel = audioop.rms(stream.read(CHUNK), 2)

        # print(audioLevel)

        if audioLevel > thresholdLevel:
            break
        else:
            pass

    stream.close()
    p.terminate()

    return(0)

# Speech processing transcription
def recordAndTranscribe():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        error = "Could not understand audio"
        return error
    except sr.RequestError as e:
        error = "Could not request results from Google Speech Recognition service; {0}".format(e)
        return error

if __name__ == "__main__":
    print("Program started, listening on default mic")
    while True:
        listenForAudio(1500)
        print("Audio detected")
        recorded_text = recordAndTranscribe()
        if recorded_text:
            # Process the recorded text as needed
            print("Transcription:", recorded_text)