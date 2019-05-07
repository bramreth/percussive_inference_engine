import librosa
import librosa.display
from music21 import stream, instrument, chord
from music21.note import Note
from midi2audio import FluidSynth
import os, time
import midi_builder


def analyse_file(filename, structure, audio):
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

    midi_builder.build_drums(tempo, len(beat_times), structure, audio)