import wave, struct, array, os
#http://doc.sagemath.org/html/en/reference/misc/sage/media/wav.html
class InputHandler:
    params = []
    stereo_audio = []
    # how many wav readings we will ignore
    filter = 1000
    def __init__(self, args):
        print(args.target)
        print(args.test)
        self.validate_target(args.target)

    # take the input
    def validate_target(self, target):
        waveFile = wave.open(target, 'r')

        length = waveFile.getnframes()

        # print details
        self.params = waveFile.getparams()
        print(self.params)

        # track length = nframes / framerate
        track_length = self.params[3] / self.params[2]
        print(track_length)

        #this calculates the size of a sample, to parse the binary data to two signed itnegers
        sizes = {1: 'B', 2: 'h', 4: 'i'}
        channels = waveFile.getnchannels()
        fmt_size = sizes[waveFile.getsampwidth()]
        fmt = "<" + fmt_size * channels


        # save the values read from the wav as tuples in a list, this is very expensive and needs improvement. see:
        # https://stackoverflow.com/questions/5804052/improve-speed-of-reading-and-converting-from-binary-file
        # https://www.cameronmacleod.com/blog/reading-wave-python

        # only record the first 6 seconds of audio
        while waveFile.tell() < self.params[2] * 6:#waveFile.getnframes():
            decoded = struct.unpack(fmt, waveFile.readframes(1))
            waveFile.setpos(waveFile.tell() + self.filter-1)
            #print(decoded)
            self.stereo_audio.append(decoded)
        #print(self.stereo_audio)

        """
        
        Bram's assumptions about the data from wav files.
        so they are the status of a wave at a certain time across the left and right stereo channels.
        the wave must have a minimum and a maximum. they appear to be at a fixed framerate, so i should
        be able to multiply the current frame by the rate and obtain the time that value was at. 
        
        the numbers are very similar due to me not having much stereo going on.
        
        it seems safe to assume larger nmbers are peaks? i should be able to find turning points and mark them
        as potential beats. then interpolate these beats over time.
        
        here is some beat detection with numpy
        https://stackoverflow.com/questions/12344951/detect-beat-and-play-wav-file-in-a-synchronised-manner
        
        """
        waveFile.close()

    def get_stereo(self):
        return self.stereo_audio

    def get_params(self):
        return self.params

    def get_filter(self):
        return self.filter