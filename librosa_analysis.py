import librosa
import librosa.display

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


#http://conference.scipy.org/proceedings/scipy2015/pdfs/brian_mcfee.pdf
#https://librosa.github.io/librosa/tutorial.html