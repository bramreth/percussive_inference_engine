import matplotlib.pyplot as plotter

import numpy as np

from scipy import stats

class graph_builder:

    threshold = 0.2# percent of the max energy at which we consider something a beat

    def __init__(self, audio, params, filter):
        # convert the stereo framse into left and right channels. then enumarte them before passing to the grapher
        frames = []


        plotter.title("waveform of wav file")
        #convert the list to a numpy array for easy percentile calculation
        frames = np.array(audio)
        list1, list2 = zip(*audio)
        #print(list2)
        #for i in range(len(list2)):
        #    list2[i] = abs(list2[i])

        plotter.plot(list1, list2)
        # naming the x axis
        plotter.xlabel('time in seconds')
        # naming the y axis
        plotter.ylabel('sound amplitude')
        plotter.show()

        #find the values below the 5th percentile and above the 95th. these areas of high amplitude should help us estimate a beat.
        #hopefully it should average at 2 per second.
        print(np.percentile(frames, 95))
        print(np.percentile(frames, 5))
        beats = []
        avg_dif = []
        last_i = 0
        for index in range(len(frames)-2):
            i = frames[index][0]
            val = frames[index][1]
            if val > np.amax(frames)*self.threshold\
                    and frames[index+1][1] < np.amax(frames)*self.threshold\
                    and frames[index+2][1] < np.amax(frames)*self.threshold:
                beats.append((i, val))
                avg_dif.append(i - last_i)
                last_i = i

        print(beats)
        print(avg_dif)
        print(np.percentile(np.array(avg_dif), 50))
        #this appears to give a better approximation of bpm than
        print(np.mean(np.array(avg_dif)))
        #we now need to find a value that intersects the most points possible
        self.find_bpm(beats, round(np.mean(np.array(avg_dif)), 2))

    def find_bpm(self, audio_list, starting_bpm):
        ls = []
        print(starting_bpm)
        for x, y in audio_list:

            ls.append(round(x % starting_bpm,2))
        ls = np.array(ls)
        print("starting bpm = " + str(round(x % starting_bpm,2)))
        print(ls)
        #print(stats.mode(ls))
        print(np.percentile(ls, 50))
        print("manual bpm:")
        print((len(ls)* 6) )
        ls = []