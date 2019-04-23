import wave, struct, librosa_analysis
#http://doc.sagemath.org/html/en/reference/misc/sage/media/wav.html
class InputHandler:
    params = []
    stereo_audio = []
    audio = []
    # how many wav readings we will ignore
    filter = 1000
    sample_len = 15
    samples = 300

    def __init__(self, args):
        print(args.target)
        print(args.test)
        self.analyse_target(args.target)
        #self.validate_target(args.target)

    #use librosa for feature extraction and anlysis
    def analyse_target(self, target):
        librosa_analysis.analyse_file(target)
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

        # only record the middle 10 seconds of audio
        midpoint = waveFile.getnframes() / 2

        while waveFile.tell() < midpoint + (self.params[2] * self.sample_len):#waveFile.getnframes():
            if waveFile.tell() >  midpoint - (self.params[2] *  self.sample_len):
                decoded = struct.unpack(fmt, waveFile.readframes(1))
                #waveFile.setpos(waveFile.tell() + self.filter-1)
                #print(decoded)
                self.stereo_audio.append(decoded)
            else:
                waveFile.setpos(waveFile.tell() + 1)
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
        
        
        rock you like a hurricane should be around 120 bpm, so i should see around 2 peaks a second
        """
        waveFile.close()
        self.sanitise_audio(self.stereo_audio)

    # read this!! https://askmacgyver.com/blog/tutorial/how-to-implement-tempo-detection-in-your-application

    #https://stackoverflow.com/questions/8200010/analyzing-audio-to-create-guitar-hero-levels-automatically
    def sanitise_audio(self, stereo_signal):
        # step 1: convert to mono, downsample to
        modulus = round(len(stereo_signal)/self.samples)
        print(len(stereo_signal))

        print(modulus)
        for count, frames in enumerate(stereo_signal):
            if count % modulus == 0:
                #print(count)
                val = int((frames[0] + frames[1])/2)
                self.audio.append((round(count/self.params[2], 3), val))
        print(self.audio)
        print(len(self.audio))
        # step 2: low pass filter audio
        # step 3: trim song
        # step 4: down sample the data to a reasonable number of units


        # step 5: normalise the data

        nomalised_audio = []
        for i, v in self.audio:
            nomalised_audio.append((i, abs(v)))
        self.audio = nomalised_audio
        print(nomalised_audio)
        pass

    def get_audio(self):
        return self.audio

    def get_stereo(self):
        return self.stereo_audio

    def get_params(self):
        return self.params

    def get_filter(self):
        return self.filter

    #http://werner.yellowcouch.org/Papers/bpm04/ paper on bpm detection
    #https://stackoverflow.com/questions/8635063/how-to-get-bpm-and-tempo-audio-features-in-python/37489967

    """
    info for cutoff filters
    https://stackoverflow.com/questions/24920346/filtering-a-wav-file-using-python
    """