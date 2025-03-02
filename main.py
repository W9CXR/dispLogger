import sys
import pyaudio
import audioop
import speech_recognition as sr
import sqlite3
import datetime

RECORD_SECONDS = 5
CHUNK = 1024 
RATE = 44100
AUDIO_THRESHOLD = 1500

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

    # Constantly monitors the mic line for audio level over the disignated threshold (set at func runtime)
    while True:
        audioLevel = audioop.rms(stream.read(CHUNK), 2)

        # print(audioLevel)

        if audioLevel > thresholdLevel:
            break
        else:
            pass

    # Closes everything cleanly (or so I'm told by docs (...reddit))
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

def insertDispatch(units, callType, location, timeout):
    # Database setup (will also create a new db called "records" if one doesn't already exist)
    con = sqlite3.connect("records.db")
    cur = con.cursor()

    # This just creates a table if this is the first time the local db has been created
    try:
        cur.execute("CREATE TABLE dispatches(units, callType, location, timeout)")
    except:
        pass

    # Spits data into... well database
    cur.execute(f"""
        INSERT INTO dispatches VALUES
        ('{units}', '{callType}', '{location}', '{timeout}')
    """)

    # db cleanup and closeout
    con.commit()
    con.close()

# Function to run loop... may need to be removed later for startup script to work
if __name__ == "__main__":
    print("Program started, listening on default mic")
    # Loops for... well all time
    while True:
        listenForAudio(AUDIO_THRESHOLD)
        print("Audio detected")
        recorded_text = recordAndTranscribe()
        if recorded_text:
            # Storing all data in units for testing, will fix later (see TODO)
            insertDispatch(recorded_text, "Placeholder", "Placeholder", datetime.datetime.now())