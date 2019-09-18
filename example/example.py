import pyquenzer

concert_pitch = 260
scale = "scales/example-gamelan.scl"
samples = {
    261.626: ["samples/c0.wav", "samples/c1.wav"],
    349.228: ["samples/f0.wav", "samples/f1.wav"],
    440: ["samples/a0.wav", "samples/a1.wav"],
}
scale_decodex = (1, 2, 3, 5, 6)

my_instrument = pyquenzer.Instrument(
    concert_pitch,
    scale,
    samples,
    scale_decodex=scale_decodex,
    nchannels=2,
    overlap=0.5,
    volume=1.2,
)


if __name__ == "__main__":
    my_instrument("output/example0", "pitches/example0", "rhythms/example0")
    my_instrument("output/example1", "pitches/example1", 0.25)
