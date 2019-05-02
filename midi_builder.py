from midiutil import MIDIFile
from enum import Enum

# enums for drum midi notes
KICK = 36
SNARE = 38
CLOSED_HI = 42
OPEN_HI = 46
LOW_TOM = 45
MID_TOM = 48
HIGH_TOM = 50
CRASH = 49
SILENCE = 0

BASIC_TRACK_1 = [KICK, SILENCE, SNARE, SILENCE, KICK, KICK, SNARE, SILENCE]
BASIC_TRACK_2 = [KICK, SILENCE, SNARE, KICK, KICK, SILENCE, SNARE, SILENCE]
BASIC_TRACK_HIGH = [CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI]
BASIC_TRACK_HIGH_ACC = [CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, OPEN_HI]

track = 0
channel = 0
time = 0  # In beats
duration = 1  # In beats
volume = 100 # 0-127, as per the MIDI standard

def build_drums(bpm, len, estimated_start):
    degrees = [KICK, KICK, KICK, KICK, SNARE]  # MIDI note number
    track = 0
    channel = 0
    time = 0  # In beats
    duration = 1  # In beats
    tempo = bpm  # In BPM

    myMIDI = MIDIFile(1)
    myMIDI.addTempo(track, time, tempo)
    index = 1

    """
    est chorus
    
    print("Best chorus found at {0:g} min {1:.2f} sec".format(
        chorus_start // 60, chorus_start % 60))
        this is measured as time in seconds, requires converting to a beat number
        
        bpm
        120 pm is 2 beats per second
        bpm / 60 * time
    """
    start_time = bpm / 60 * estimated_start
    print(len)
    if estimated_start:
        generate_track(myMIDI, time, int(start_time), 1)
        generate_track(myMIDI, int(start_time), len, 2)
    else:
        #generate_track(myMIDI, time, time + int(len/2), 1)
       # generate_track(myMIDI, int(len/2), len, 2)
        generate_track(myMIDI, time, len, 2)

    """
    for i in range(len):
        myMIDI.addNote(track, channel, degrees[i%4], time + i, duration, volume)
        if i % 4 == 0:
            myMIDI.addNote(track, channel, degrees[4], time + i, duration, volume)
        myMIDI.addNote(track, channel, CLOSED_HI, time + i, duration, volume)
        #index = not index

    #for i, pitch in enumerate(degrees):
     #   myMIDI.addNote(track, channel, pitch, time + i, duration, volume)
    """
    with open("beat_file/beat_file.mid", "wb") as output_file:
        myMIDI.writeFile(output_file)
    """
    needed features
    emphasising beats
    tone, speed, volume
    choosing percussion https://www.edb.gov.hk/attachment/tc/curriculum-development/kla/arts-edu/nss/gm_drumlist_8050.pdf
    ---
    silence
    solos 
    genre
    memory of creative space
    chorus analysis
    inflection
    fear
    """

def generate_track(MIDI_FILE, time_start, time_end, type):
    #doubling and dividing the range lets us use 8th notes in our patterns
    if type == 1:
        print(time_start)

        for i in range((time_end - time_start) * 2):
            if BASIC_TRACK_1[i % 8] != 0:
                MIDI_FILE.addNote(track, channel, BASIC_TRACK_1[i % 8], time_start + i / 2, duration, volume)
            if BASIC_TRACK_HIGH_ACC[i % 8] != 0:
                MIDI_FILE.addNote(track, channel, BASIC_TRACK_HIGH_ACC[i % 8], time_start + i / 2, duration, volume)
    elif type == 2:
        print(time_start)
        for i in range((time_end - time_start) * 2):
            if BASIC_TRACK_2[i % 8] != 0:
                MIDI_FILE.addNote(track, channel, BASIC_TRACK_2[i % 8], time_start + i/2, duration, volume)
            if BASIC_TRACK_HIGH[i % 8] != 0:
                MIDI_FILE.addNote(track, channel, BASIC_TRACK_HIGH[i % 8], time_start + i/2, duration, volume)

    #https://towardsdatascience.com/finding-choruses-in-songs-with-python-a925165f94a8

    #http: // learndrumsforfree.com / 2015 / 07 / 10 - basic - rock - drum - beats /