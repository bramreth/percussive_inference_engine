from midiutil import MIDIFile

def build_drums(bpm, len):
    degrees = [36, 36, 36, 36, 38]  # MIDI note number
    track = 0
    channel = 0
    time = 0  # In beats
    duration = 1  # In beats
    tempo = bpm  # In BPM
    volume = 100  # 0-127, as per the MIDI standard

    myMIDI = MIDIFile(1)
    myMIDI.addTempo(track, time, tempo)
    index = 1
    for i in range(len):
        myMIDI.addNote(track, channel, degrees[i%4], time + i, duration, volume)
        if i % 4 == 0:
            myMIDI.addNote(track, channel, degrees[4], time + i, duration, volume)
        #index = not index

    #for i, pitch in enumerate(degrees):
     #   myMIDI.addNote(track, channel, pitch, time + i, duration, volume)

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

    #https://towardsdatascience.com/finding-choruses-in-songs-with-python-a925165f94a8