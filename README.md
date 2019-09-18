# pyquenzer

*pyquenzer* is a [Python3](https://www.python.org) module to sequenze and retune short audio samples. Its main purpose is to offer an easy and simple way to generate melodies and chords with different tunings. *pyquenzer* uses the music computer system [csound](https://csound.com/) to sequenze and retune audio samples.


## dependencies
    * music computing system [csound](https://csound.com/)
    * Python library [mu](https://github.com/uummoo/mu)


## usage

### 1. Defining an instrument.


Load the respective module.

```python
import pyquenzer
```

Define the [concert pitch](https://en.wikipedia.org/wiki/Concert_pitch) in [Hertz](https://en.wikipedia.org/wiki/Hertz). The concert pitch is indicating the frequency of **the first pitch of a scale**.

```python
concert_pitch = 260
```

Define the path to the scale that a particular instrument is supposed to use. The scale has to be written in the popular [scl format](http://huygens-fokker.org/scala/scl_format.html). [example/scales](https://github.com/uummoo/pyquenzer/example/scales) already provides different scl files. They are taken from [the scl files archive](www.huygens-fokker.org/docs/scales.zip) of the [Huygens-Fokker instituion](http://huygens-fokker.org/).

```python
scale = "scales/example-gamelan.scl"
```

Make the *samples* dictionary. This dictionary contains the paths of all audio samples that shall be used to synthesise WAV files later. Every entry contains two elements:
    1. an estimated frequency in Hertz
    2. a list containing the paths of all corresponding samples

```python
samples = {
    261.626: ["samples/c0.wav", "samples/c1.wav"],
    349.228: ["samples/f0.wav", "samples/f1.wav"],
    440: ["samples/a0.wav", "samples/a1.wav"],
}
```

Define (optionally) the *scale_decodex* argument.

```python
scale_decodex = (1, 2, 3, 5, 6)
```

Initialise an **Instrument** - object. Besides *concert_pitch*, *scale*, *scale_decodex* and *samples* the **Instrument** class also provides additional optional arguments:
    * *nchannels*: Shall be **1** if the used samples are **mono** and **2** if the used samples are **stereo**
    * *overlap*: how long two following notes of a melody may overlap (in seconds)
    * *volume*: factor to adjust the volume of every sample
    * *release*: pass
    * *reverb-volume*: volume of the reverb channel

```python
my_instrument = pyquenzer.Instrument(
    concert_pitch, scale, samples, scale_decodex=scale_decodex, nchannels=2, overlap=0.5, volume=1.2
)
```

### 2. Rendering a WAV - file.

To render WAV files call the *Instrument* object with:
    1. The path/name of the resulting WAV file
    2. The path to the pitch file
    3. The path to the rhythm file

```python
my_instrument("output/example0", "pitches/example0", "rhythms/example0")
```
A rhythm file can also be replaced by a *floating point number*. In this case every resulting tone/chord has the same rhythmic duration.

```python
my_instrument("output/example1", "pitches/example1", 0.25)
```


installation:
-------------
```sh
  $ git clone "https://github.com/uummoo/pyquenzer"
  $ cd pyquenzer/
  $ pip3 install -r requirements.txt
  $ pip3 install .
```

To test if everything works well, one may try (inside the *example* - directory):

```sh
  $ python3 example.py
```
