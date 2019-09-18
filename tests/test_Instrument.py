import os
import pyquenzer
import unittest

from mu.mel import mel
from mu.sco import old


class InstrumentTest(unittest.TestCase):
    def test_make_cadence(self):

        p_lines = ("# simple melody", "6 5 3 2", "(1 5) 2 3 2")

        pitch_name = "pitches"

        scl_lines = (
            "Imaginary perfect slendro",
            "5",
            "240.",
            "480.",
            "720.",
            "960.",
            "1200.",
        )
        scale_name = "slendro.scl"
        names = (pitch_name, scale_name)

        for name, lines in zip(names, (p_lines, scl_lines)):
            with open(name, "w") as scl:
                scl.write("\n".join(lines))

        concert_pitch = 260

        scale = mel.Mel.from_scl(scale_name, concert_pitch)

        cadence = old.Cadence(
            old.Chord(
                mel.Harmony(
                    tuple(scale[idx] if idx <= 3 else scale[idx - 1] for idx in h)
                ),
                1,
            )
            for h in ([6], [5], [3], [2], [1, 5], [2], [3], [2])
        )

        test_cadence = pyquenzer.Instrument(
            concert_pitch, scale_name, {}, (1, 2, 3, 5, 6)
        ).mk_cadence(pitch_name, 1)

        self.assertEqual(cadence, test_cadence)

        for name in names:
            os.remove(name)


if __name__ == "__main__":
    unittest.main()
