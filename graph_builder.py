import matplotlib.pyplot as plotter


class graph_builder:

    def __init__(self, stereo_frames, params, filter):
        # convert the stereo framse into left and right channels. then enumarte them before passing to the grapher
        l_frames = []
        r_frames = []

        for count, frames in enumerate(stereo_frames):
            print("item: " + str(round(count/params[2]*filter, 2)) + " l: " + str(frames[0])+ " r: " + str(frames[1]))
            l_frames.append((round(count/params[2]*filter, 2), frames[0]))
            r_frames.append((round(count / params[2] * filter, 2), frames[1]))

        plotter.title("waveform of wav file")
        list1, list2 = zip(*l_frames)

        plotter.plot(list1, list2)
        # naming the x axis
        plotter.xlabel('time in seconds')
        # naming the y axis
        plotter.ylabel('sound amplitude')
        plotter.show()
