import bisect
import itertools
import os

from mu.sco import old
from mu.mel import mel
from mu.mel import shortwriting as sw


class Instrument(object):
    def __init__(
        self,
        concert_pitch: float,
        scale: str,
        samples: dict,
        scale_decodex: tuple = None,
        nchannels: int = 1,
        overlap: float = 0,
        volume: float = 1,
        release: float = 0.1,
        reverb_volume: float = 0.4,
    ):
        try:
            assert nchannels in (1, 2)
        except AssertionError:
            msg = "{0} Channels entered. "
            msg += "Only Mono or Stereo files are allowed! ".format(nchannels)
            msg += "(nchannels = 1 or nchannels = 2)."
            raise ValueError(msg)

        scale = mel.Mel.from_scl(scale, concert_pitch)
        len_scale = len(scale)
        if not scale_decodex:
            scale_decodex = tuple(range(1, len_scale))

        len_scale_decodex = len(scale_decodex)

        try:
            assert len_scale - 1 == len_scale_decodex
        except AssertionError:
            msg = "Scale and scale_decodex have to be equally long! "
            msg += "Scale has {0} pitches and scale_decodex {1} pitches.".format(
                len_scale, len_scale_decodex
            )
            raise ValueError(msg)

        self.__concert_pitch = concert_pitch
        self.__scale_decodex = scale_decodex
        self.__scale = scale

        self.__decodex = {
            "{0}".format(scale_index): p for scale_index, p in zip(scale_decodex, scale)
        }
        self.__samples = {freq: itertools.cycle(samples[freq]) for freq in samples}
        self.__nchannels = nchannels
        self.__overlap = overlap
        self.__volume = volume
        self.__release = release
        self.__reverb_volume = reverb_volume

    @property
    def concert_pitch(self) -> float:
        return self.__concert_pitch

    @property
    def scale(self) -> float:
        return self.__scale

    @property
    def scale_decodex(self) -> float:
        return self.__scale_decodex

    @property
    def samples(self) -> dict:
        return self.__samples

    @property
    def overlap(self) -> float:
        return self.__overlap

    @property
    def nchannels(self) -> int:
        return self.__nchannels

    @property
    def volume(self) -> int:
        return self.__volume

    @property
    def release(self) -> int:
        return self.__release

    @property
    def reverb_volume(self) -> int:
        return self.__reverb_volume

    def find_sample(self, pitch: mel.SimplePitch) -> tuple:
        """Return tuple containing sample name and factor"""
        pf = pitch.freq
        frequencies = tuple(self.samples)
        sidx = bisect.bisect(frequencies, pf) - 1
        frequency = frequencies[sidx]
        return next(self.samples[frequency]), pf / frequency

    def mk_cadence(self, scale_functions: str, rhythm: str) -> old.Cadence:
        def make_pitches(scale_functions) -> mel.Cadence:
            return sw.translate_from_file(scale_functions, self.__decodex)

        def make_rhythms(rhythm) -> tuple:
            typr = type(rhythm)
            if typr == int or typr == float:
                return tuple(rhythm for i in range(len(harmonies)))
            elif typr == str:
                with open(rhythm, "r") as r:
                    lines = tuple(l for l in r.read().splitlines() if l)
                    rhythm = " ".join(tuple(l for l in lines if l[0] != "#"))
                    rhythm = rhythm.split(" ")
                    rhythm = tuple(float(n) for n in rhythm if n)
                return rhythm
            elif typr == tuple:
                assert len(rhythm) == len(harmonies)
                return rhythm
            else:
                msg = "Unknown TYPE '{0}' for argument rhythm.".format(typr)
                raise ValueError(msg)

        harmonies = make_pitches(scale_functions)
        rhythms = make_rhythms(rhythm)
        return old.Cadence(old.Chord(h, r) for h, r in zip(harmonies, rhythms))

    def mk_orc(self) -> str:
        lines = (
            r"0dbfs=1",
            r"gaSend init 0",
            r"instr 1",
            r"asig diskin2 p4, p5, 0, 0, 6, 4",
            r"kenv linseg 1, p3 - p7, 1, p7, 0",
            r"asig = asig * kenv * p6",
            r"out asig",
            r"gaSend = gaSend + (asig * 0.1)",
            r"endin",
            r"instr 2",
            r"kroomsize init 0.7",
            r"kHFDamp init 0.5",
            r"aRvbL, aRvbR freeverb gaSend, gaSend, kroomsize, kHFDamp",
            r"out (aRvbL + aRvbR) * " + str(self.reverb_volume),
            r"clear gaSend",
            r"endin",
        )

        if self.nchannels == 2:
            lines = list(lines)
            lines[3] = r"asig, asig1 diskin2 p4, p5, 0, 0, 6, 4"
            lines = tuple(lines)

        return "\n".join(lines)

    def mk_sco(self, cadence: old.Cadence) -> str:
        lines = []
        abs_start = cadence.delay.convert2absolute()
        for event, start in zip(cadence, abs_start):
            if event.pitch and event.pitch != mel.TheEmptyPitch:
                duration = float(event.delay) + self.overlap
                release = self.release if self.release < duration else duration - 0.0001
                line = r"i1 {0} {1} ".format(start, duration)
                for pi in tuple(p for p in event.pitch if p != mel.TheEmptyPitch):
                    sample_name, factor = self.find_sample(pi)
                    final_line = '{0} "{1}" {2} {3} {4}'.format(
                        line, sample_name, factor, self.volume, release
                    )
                    lines.append(final_line)
        complete_duration = float(cadence.duration + 5)
        lines.append("i2 0 {0}".format(complete_duration))
        return "\n".join(lines)

    def __call__(self, name: str, scale_functions: str, rhythm: str) -> None:
        sfname = "{0}.wav".format(name)
        fname = "csoundsynth"
        orc_name = "{0}.orc".format(fname)
        sco_name = "{0}.sco".format(fname)

        cadence = self.mk_cadence(scale_functions, rhythm)
        orc = self.mk_orc()
        sco = self.mk_sco(cadence)

        if sco:
            with open(orc_name, "w") as f:
                f.write(orc)
            with open(sco_name, "w") as f:
                f.write(sco)
            cmd0 = "csound --format=double -k 96000 -r 96000 -o {0} ".format(sfname)
            cmd1 = "{0} {1}".format(orc_name, sco_name)
            cmd = cmd0 + cmd1
            os.system(cmd)
            os.remove(orc_name)
            os.remove(sco_name)
