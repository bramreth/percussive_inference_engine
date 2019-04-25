import librosa
import librosa.display
from music21 import stream, instrument
from music21.note import Note
from midi2audio import FluidSynth
import os, time

def analyse_file(filename):
    # y is the time series as a numpy array
    # sr contains a default sampling rate of 22050 hz
    y, sr = librosa.load(filename)
    # tempo contains the estimated beats per minute
    # beat frames contains seperated centered frames of the beats
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    print("tempo: {:.2f}".format(tempo))

    # converts the beat frames into timestamped beat events
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    print(beat_times)
    librosa.output.times_csv("beat_file/beat_times.csv", beat_times)

    #display graphs for analysis
    librosa.display.waveplot(y)



    drumPart = stream.Part()

    bass = instrument.BassDrum()
    snare = instrument.SnareDrum()
    drumPart.insert(0, bass)
    drumPart.insert(1, snare)

    i = 0

    drumMeasure = stream.Measure()
    for item in beat_times:

        n = Note("A2")
        i = not i

        if i:
            #the standard note for a kick drum
            n = Note("C2")
            
        else:

            #standard for a snare
            n = Note("D2")
        n.offset = item
        drumMeasure.append(n)
    path = 'beat_file/beat_file.mid'
    drumPart.append(drumMeasure)
    fp = drumPart.write('midi', fp=path)
    # This line actually generate the midi on my mac but there is no relevant software to read it and the opening fail
    #drumPart.show('midi')
    #while not os.path.exists(path):
    #    time.sleep(1)
    #fs = FluidSynth()
    #FluidSynth().play_midi(path)
    #fs.midi_to_audio(path, "tst.wav")

#http://conference.scipy.org/proceedings/scipy2015/pdfs/brian_mcfee.pdf
#https://librosa.github.io/librosa/tutorial.html