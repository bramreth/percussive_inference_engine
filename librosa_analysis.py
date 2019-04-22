import librosa

def analyse_file(filename):
    y, sr = librosa.load(filename)
    tempo, bpm = librosa.beat.beat_track(y=y, sr=sr)

    print("tempo: {:.2f}".format(tempo))

analyse_file("test_input_wavs/sandman_test.wav")

#http://conference.scipy.org/proceedings/scipy2015/pdfs/brian_mcfee.pdf
#https://librosa.github.io/librosa/tutorial.html