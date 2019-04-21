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
        """
        for i, val in frames:
            #if val > np.percentile(frames, 98):
            if val > np.amax(frames)*self.threshold:
                beats.append((i, val))
                avg_dif.append(i - last_i)
                last_i = i
            else
        """

        print(beats)
        print(avg_dif)
        print(np.percentile(np.array(avg_dif), 50))
        #this appears to give a better approximation of bpm than
        print(np.mean(np.array(avg_dif)))
        #we now need to find a value that intersects the most points possible in
        """
        methods to interpolate thebeatpoints:
        i need to take a variety of valid beats as starting points, then apply a beat near the mean 
        rate. the beat that intersects the most valid point
        
        we will need an error value for whether the beat is at the right point.
        
        it seems reasonable to say this should be our smallest time increment we are measuring.
        i believe at the moment this is 0.02 seconds, however will need calculating dynamically
        """
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
        #i think i can do something clever with modulus. if i find the right bpm,
        #most of the numbers should settle on the same value with the right modulus
        #i just need to figure out what that value is.
        #if we jsut mode every value in the list by the same amount and tally up the modally mosy
        #frequent value , then tweak the starting bpm till a best fit is found


        #using percentiles to detect beats doesn't work because i will always have the same number of beats. i need a
        #threshold

        """
        when checking if values are within the threshold, we want to asses both the current value and the following two,
        making sure the first value iis valid and the second two arent.
        """
