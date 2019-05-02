import librosa
import librosa.display
from music21 import stream, instrument, chord
from music21.note import Note
from midi2audio import FluidSynth
import os, time
import midi_builder


def analyse_file(filename, structure):
    # y is the time series as a numpy array
    # sr contains a default sampling rate of 22050 hz
    y, sr = librosa.load(filename)
    # tempo contains the estimated beats per minute
    # beat frames contains seperated centered frames of the beats
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    print("tempo: {:.2f}".format(tempo))

    # converts the beat frames into timestamped beat events
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    #print(beat_times)
    librosa.output.times_csv("beat_file/beat_times.csv", beat_times)

    #display graphs for analysis
    librosa.display.waveplot(y)

    midi_builder.build_drums(tempo, len(beat_times), structure)
    """
    drumPart = stream.Part()

    bass = instrument.BassDrum()
    snare = instrument.SnareDrum()
    drumPart.insert(0, bass)
    drumPart.insert(1, snare)

    i = 0

    drumMeasure = stream.Measure()
    """
    """
    C2 bass drum
    D2 snare
    E2 snare 2
    C3 tom
    D3 cowbell
    F#2 closed hi
    """
    """
    for item in beat_times:

        n = Note("A2")

        if i % 2 == 0:
            #the standard note for a kick drum
            n = chord.Chord(["C2", "F#2"])
            #n = Note("C2")
        else:
            #standard for a snare
            n = chord.Chord(["D2", "F#2"])
            #n = Note("D2")
        #assuming 4/4 this is the final beat of the bar?
        if i % 8 == 7:
            n = chord.Chord(["D2", "F#2"])
            n.volume = 120
        n.offset = item
        drumMeasure.append(n)

        i += 1
    #for item in range(len(beat_times)):
    #    drumMeasure[item].offset = beat_times[item]
    path = 'beat_file/beat_file.mid'
    print(drumMeasure.secondsMap)
    drumPart.append(drumMeasure)
    fp = drumPart.write('midi', fp=path)
    # This line actually generate the midi on my mac but there is no relevant software to read it and the opening fail
    #drumPart.show('midi')
    #while not os.path.exists(path):
    #    time.sleep(1)
    #fs = FluidSynth()
    #FluidSynth().play_midi(path)
    #fs.midi_to_audio(path, "tst.wav")
    """

#http://conference.scipy.org/proceedings/scipy2015/pdfs/brian_mcfee.pdf
#https://librosa.github.io/librosa/tutorial.html