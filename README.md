# pyquenzer

*pyquenzer* is a [Python](https://www.python.org) module to sequenze and retune short audio samples. Its main purpose is to offer an easy and simple way to generate melodies and chords with different tunings. *pyquenzer* uses the music computer system [csound](https://csound.com/) to sequenze and retune audio samples.


## dependencies

- music computing system [csound](https://csound.com/)
- Python library [mu](https://github.com/uummoo/mu)


## usage (see [example](https://github.com/uummoo/pyquenzer/tree/master/example/example.py)

For generating WAV - files, its necessary to define an **Instrument** first. This **Instrument** contains details about the synthesisation process. In the next step one may pass arguments about the content (pitch and rhythm) that shall be synthesised to the previously defined **Instrument**.

### 1. Defining an instrument.

Load the respective module.

```python
import pyquenzer
```

Define the [concert pitch](https://en.wikipedia.org/wiki/Concert_pitch) in [Hertz](https://en.wikipedia.org/wiki/Hertz). The concert pitch is indicating the frequency of **the first pitch of a scale**.

```python
concert_pitch = 260
```

Define the path of the scale that you want to use. The scale has to be written in the popular [scl format](http://huygens-fokker.org/scala/scl_format.html). In [example/scales](https://github.com/uummoo/pyquenzer/tree/master/example/scales) you can find some scl files. They are taken from [the scl files archive](www.huygens-fokker.org/docs/scales.zip) of the [Huygens-Fokker instituion](http://huygens-fokker.org/).

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

Define (optionally) the *scale_decodex* argument. The *scale_decodex* argument has to contain as many entries as there are pitches in the used scale. Every entry represents one scale degree. If no *scale_decodex* is specified by the user, every scale degree is represented by its position (the *scale-decodex* of a hepatatonic scale would automatically be defined as (1, 2, 3, 4, 5, 6, 7) and the *scale_decodex* of a pentatonic scale as (1, 2, 3, 4, 5)).

```python
scale_decodex = (1, 2, 3, 5, 6)  # notation style similar to the Javanese 'notasi Kepatihan' thats skips the 4
```

Initialise an **Instrument** - object. Besides

* *concert_pitch*
* *scale*
* *samples*
* *scale_decodex*

the **Instrument** class also provides additional optional arguments:

- *nchannels*: Shall be **1** if the used samples are **mono** and **2** if the used samples are **stereo**
- *overlap*: determines how long two following notes of a melody are overlapping (in seconds)
- *volume*: factor to adjust the volume of every sample
- *release*: indicates the duration of a linear envelope that releases the sound of each sample (in seconds)
- *reverb-volume*: volume of the reverb channel

```python
my_instrument = pyquenzer.Instrument(
    concert_pitch, scale, samples, scale_decodex=scale_decodex, nchannels=2, overlap=0.5, volume=1.2
)
```

### 2. Rendering WAV - files.

To render WAV files call the *Instrument* object with:

1. The path/name of the resulting WAV file

2. The path to the pitch file

*Pitch files* are text files that describe the pitch of each event. For more details of the needed form study the examples [here](https://github.com/uummoo/pyquenzer/tree/master/example/pitches).

3. The path to the rhythm file

*Rhythm files* are text files that describe the duration of each event. For more details of the needed form study the examples [here](https://github.com/uummoo/pyquenzer/tree/master/example/rhythms).

```python
my_instrument("output/example0", "pitches/example0", "rhythms/example0")
```

A rhythm file can also be replaced by a *floating point number*. In this case the rhythmic duration of every resulting tone/chord is equal (*0.25* seconds in the example below).

```python
my_instrument("output/example1", "pitches/example1", 0.25)
```


installation:
-------------

First install all necessary dependencies. Then download *pyquenzer* via git and install it with [pip](https://pypi.org/project/pip/):

```sh
  $ git clone "https://github.com/uummoo/pyquenzer"
  $ cd pyquenzer/
  $ pip3 install -r requirements.txt
  $ pip3 install .
```

To test if everything works well one may try (inside the *example* - directory):

```sh
  $ python3 example.py
```
