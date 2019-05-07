import wave, struct, librosa_analysis, verse_detector, yaml

class InputHandler:
    params = []
    stereo_audio = []
    audio = []
    # how many wav readings we will ignore
    filter = 1000
    sample_len = 15
    samples = 300
    view = False

    def __init__(self, args):
        print("target input song file: " + str(args.target))
        print("whether or not we are in test mode (verbosity): " + str(args.test))
        print("whether or not we want to view the input's chroma: " + str(args.view))
        print("a structure file: " + str(args.structure))

        if args.view:
            # view the chroma of the output file
            self.view = args.view
            self.view_chroma(args.target)
            self.validate_target(args.target)
        elif args.structure:
            # we need to run an analysis to get the volume at specific parts of the track
            # take the mean of all wav values over an interval, compare to others to decide on velocity of the drum file
            self.grab_sanitised_audio(args.target)
            structure = self.load_yaml(args.structure)
            self.analyse_target(args.target, structure, self.audio)
        else:
            self.grab_sanitised_audio(args.target)
            self.analyse_target(args.target, [], self.audio)

    def view_chroma(self, target):
        verse_detector.show_details(target)

    # apply the imported structure to the output midi file
    def analyse_target(self, target, structure, audio):
        librosa_analysis.analyse_file(target, structure, audio)

    def load_yaml(self, path):
        with open(path, 'r') as stream:
            try:
                print("yaml successful load")
                #print(yaml.safe_load(stream))
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def grab_sanitised_audio(self, target):
        waveFile = wave.open(target, 'r')

        length = waveFile.getnframes()
        self.params = waveFile.getparams()
        # track length = nframes / framerate
        track_length = self.params[3] / self.params[2]

        # this method of extraction can be found here:
        # https://www.cameronmacleod.com/blog/reading-wave-python
        sizes = {1: 'B', 2: 'h', 4: 'i'}
        channels = waveFile.getnchannels()
        fmt_size = sizes[waveFile.getsampwidth()]
        fmt = "<" + fmt_size * channels

        while waveFile.tell() < waveFile.getnframes():
            decoded = struct.unpack(fmt, waveFile.readframes(1))
            self.stereo_audio.append(decoded)

        waveFile.close()
        self.sanitise_audio(self.stereo_audio)
        print(self.audio)

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

        # this calculates the size of a sample, to parse the binary data to two signed itnegers
        sizes = {1: 'B', 2: 'h', 4: 'i'}
        channels = waveFile.getnchannels()
        fmt_size = sizes[waveFile.getsampwidth()]
        fmt = "<" + fmt_size * channels
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
        waveFile.close()
        self.sanitise_audio(self.stereo_audio)

    def sanitise_audio(self, stereo_signal):
        # step 1: convert to mono, downsample to
        modulus = round(len(stereo_signal)/self.samples)

        for count, frames in enumerate(stereo_signal):
            if count % modulus == 0:
                #print(count)
                val = int((frames[0] + frames[1])/2)
                self.audio.append((round(count/self.params[2], 3), val))
        # step 2: low pass filter audio
        # step 3: trim song
        # step 4: down sample the data to a reasonable number of units
        # step 5: normalise the data

        nomalised_audio = []
        for i, v in self.audio:
            nomalised_audio.append((i, abs(v)))
        self.audio = nomalised_audio

    def get_audio(self):
        return self.audio

    def get_stereo(self):
        return self.stereo_audio

    def get_params(self):
        return self.params

    def get_filter(self):
        return self.filter