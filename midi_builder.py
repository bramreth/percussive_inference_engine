from midiutil import MIDIFile
from enum import Enum
import random
# enums for drum midi notes
KICK = 36
SNARE = 38
CLOSED_HI = 42
OPEN_HI = 46
LOW_TOM = 45
HIGH_TOM = 48
COWBELL = 50
CRASH = 49
SILENCE = 0
KICK_SNARE = 1

BASIC_TRACK_1 = [KICK, SILENCE, SNARE, SILENCE, KICK, KICK, SNARE, SILENCE]
BASIC_TRACK_2 = [KICK, SILENCE, SNARE, KICK, KICK, SILENCE, SNARE, SILENCE]

BASIC_TRACK_SLOW = [KICK, SILENCE, SNARE, SILENCE, KICK, SILENCE, SILENCE, SILENCE]

BASIC_TRACK_HIGH = [CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI]
BASIC_TRACK_HIGH_ACC = [CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, CLOSED_HI, OPEN_HI, CLOSED_HI]


COMPONENT_LOW_1 = [KICK, SILENCE, KICK, SILENCE]
COMPONENT_LOW_2 = [KICK, SILENCE, SNARE, SILENCE]
COMPONENT_LOW_3 = [KICK, KICK, SNARE, SILENCE]
COMPONENT_LOW_4 = [KICK, SILENCE, SNARE, KICK]
track = 0
channel = 0
time = 0  # In beats
duration = 0.5  # In beats
volume = 80 # 0-127, as per the MIDI standard


def build_drums(bpm, len, structure, audio):
    degrees = [KICK, KICK, KICK, KICK, SNARE]  # MIDI note number
    track = 0
    channel = 0
    time = 0  # In beats
    duration = 1  # In beats
    tempo = bpm  # In BPM

    myMIDI = MIDIFile(1)
    myMIDI.addTempo(track, time, tempo)
    index = 1

    if structure:
        start = 0
        last_time = 0
        verses = {}

        # find the overall song energy for volume analysis
        overall_energy = overall_volume_analysis(audio)
        print("average audio energy: " + str(overall_energy))

        for item in structure:
            key = next(iter(item))

            energy = volume_analysis(last_time, item[key], audio)
            print(str(key) + " energy is " + str(energy))
            section_energy = int(volume + (((energy / overall_energy) - 1) * 40))
            print(section_energy)
            time_converted = int(bpm / 60 * item[key])
            if key not in verses.keys():
                verses[key] = [gen_loop_low(), gen_loop_high()]
                backup_section(verses, tempo, key, section_energy)
            #generate_track_from_source(myMIDI, start, time_converted, verses[key][0], verses[key][1], section_energy)
            start = time_converted
            last_time = item[key]
    else:
        print("without a structure file no volumetric analysis is availiable")
        generate_unique_track(myMIDI, time, len)
        with open("beat_file/beat_file.mid", "wb") as output_file:
            myMIDI.writeFile(output_file)

    with open("beat_file/beat_file.mid", "wb") as output_file:
        myMIDI.writeFile(output_file)

# return the mean amplitude in a given time for volumetric analysis
def overall_volume_analysis(audio):
    sum = 0
    count = 0
    for index, value in audio:
        sum += value
        count += 1
    if count == 0:
        return 0
    return sum / count

#takes the analysed wav file and returns the average volume in a given period
def volume_analysis(start, end, audio):
    sum = 0
    count = 0
    for index, value in audio:
        if start < index < end:
            sum += value
            count += 1
    if count == 0:
        return 0
    return sum / count


def backup_section(verses, tempo, key, volume_in):
    sectionMIDI = MIDIFile(1)
    sectionMIDI.addTempo(track, time, tempo)
    generate_track_from_source(sectionMIDI, 0, 8, verses[key][0], verses[key][1], volume_in)
    with open("beat_file/"+key+".mid", "wb") as output_file:
        sectionMIDI.writeFile(output_file)


def gen_loop_low():
    track = []
    kick_chance = 60
    for i in range(8):
        choice = random.randint(1, 100)
        if i % 4 == 0:
            # main beat
            if choice < kick_chance:
                track.append(KICK)
            elif choice < 80:
                track.append(KICK_SNARE)
            else:
                track.append(SNARE)
        elif choice < 30:
            track.append(SILENCE)
        elif choice < 50:
            track.append(KICK)
        elif choice < 70:
            track.append(SNARE)
        elif choice < 90:
            track.append(KICK_SNARE)
        elif choice < 95:
            track.append(LOW_TOM)
        elif choice < 100:
            track.append(HIGH_TOM)
        else:
            track.append(COWBELL)
            #the one in a hundred is on purpose
    return track

def gen_loop_high():
    track = []
    open_chance = 20
    for i in range(8):
        choice = random.randint(1, 100)
        if i % 4 == 0:
            # main beat
            if choice <= open_chance:
                track.append(OPEN_HI)
            else:
                track.append(CLOSED_HI)
        elif choice < 50:
            track.append(SILENCE)
        elif choice < 90:
            track.append(CLOSED_HI)
        elif choice < 100:
            track.append(OPEN_HI)
        else:
            track.append(CRASH)
    return track

"""
def find_drum_def(MIDI_FILE, time_start, time_end):
    t = [KICK, SNARE, CLOSED_HI, OPEN_HI, LOW_TOM, COWBELL, HIGH_TOM, CRASH, SILENCE]
    for i in range((time_end - time_start) * 2):
        if t[i % 9] != 0:
            MIDI_FILE.addNote(track, channel, t[i % 9], time_start + i / 2, duration, volume)
"""

def generate_unique_track(MIDI_FILE, time_start, time_end):
    print("start: " + str(time_start))
    print("end: " + str(time_end))
    track_low = gen_loop_low()
    track_hi = gen_loop_high()
    for i in range((time_end - time_start) * 2):
        if track_hi[i % 8] != 0:
            MIDI_FILE.addNote(track, channel, track_hi[i % 8], time_start + i / 2, duration, volume)
        if track_low[i % 8] == 1:
            # snare and kick
            MIDI_FILE.addNote(track, channel, SNARE, time_start + i / 2, duration, volume)
            MIDI_FILE.addNote(track, channel, KICK, time_start + i / 2, duration, volume)
        elif track_low[i % 8] != 0:
            MIDI_FILE.addNote(track, channel, track_low[i % 8], time_start + i / 2, duration, volume)


def generate_track_from_source(MIDI_FILE, time_start, time_end, track_low, track_hi, volume_in):
    print("start: " + str(time_start))
    print("end: " + str(time_end))
    # volume analysis, main beats are louder
    beat_volume = volume_in
    for i in range((time_end - time_start) * 2):
        beat_volume = volume_in
        if i % 8 != 0:
            beat_volume -= 20
        if track_hi[i % 8] != 0:
            MIDI_FILE.addNote(track, channel, track_hi[i % 8], time_start + i / 2, duration, volume_in)
        if track_low[i % 8] == 1:
            # snare and kick
            MIDI_FILE.addNote(track, channel, SNARE, time_start + i / 2, duration, beat_volume)
            MIDI_FILE.addNote(track, channel, KICK, time_start + i / 2, duration, beat_volume)
        elif track_low[i % 8] != 0:
            MIDI_FILE.addNote(track, channel, track_low[i % 8], time_start + i / 2, duration, beat_volume)


def generate_track(MIDI_FILE, time_start, time_end, type):
    #doubling and dividing the range lets us use 8th notes in our patterns
    track_hi = []
    track_low = []
    if type == 1:
        track_hi = BASIC_TRACK_HIGH_ACC
        track_low = BASIC_TRACK_1
    elif type == 2:
        track_hi = BASIC_TRACK_HIGH
        track_low = BASIC_TRACK_2
    elif type == 3:
        track_hi = BASIC_TRACK_HIGH_ACC
        track_low = BASIC_TRACK_SLOW

    for i in range((time_end - time_start) * 2):
        if track_hi[i % 8] != 0:
            MIDI_FILE.addNote(track, channel, track_hi[i % 8], time_start + i / 2, duration, volume)
        if track_low[i % 8] == 1:
            # snare and kick
            MIDI_FILE.addNote(track, channel, SNARE, time_start + i / 2, duration, volume)
            MIDI_FILE.addNote(track, channel, KICK, time_start + i / 2, duration, volume)
        elif track_low[i % 8] != 0:
            MIDI_FILE.addNote(track, channel, track_low[i % 8], time_start + i / 2, duration, volume)
    #https://towardsdatascience.com/finding-choruses-in-songs-with-python-a925165f94a8

    #http: // learndrumsforfree.com / 2015 / 07 / 10 - basic - rock - drum - beats /