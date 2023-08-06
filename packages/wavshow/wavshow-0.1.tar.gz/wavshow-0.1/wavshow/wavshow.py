#!/usr/bin/env python
import sys

import numpy
import scipy.signal
import soundfile
import matplotlib.pyplot as plt


def plotspec(wav, fs):
  freq, time, spec = scipy.signal.spectrogram(wav, fs)
  plt.imshow(10 * numpy.log10(spec), aspect="auto", interpolation="nearest", origin="lower")

  # Time axis
  locs = list(map(int, numpy.linspace(0, len(time)-1, 10)))
  plt.xticks(locs, time[locs])
  plt.xlabel("Time [s]")

  # Frequency axis
  locs = range(0, len(freq), 16)
  plt.yticks(locs, map(int, freq[locs]))
  plt.ylabel("Frequency [Hz]")

def plotwav(wav, fs):
  plt.plot(wav, "k-")
 
  xticks, strs = plt.xticks()
  plt.xticks(xticks, ["%.2f" % (x/fs) for x in xticks])

  plt.ylim(-1, 1)
  plt.xlim(0, len(wav))
  plt.xlabel("Time [s]")
  plt.ylabel("Amplitude")

  return plt.xticks()

def plot_main(wavname):
  plt.figure()

  obj = soundfile.SoundFile(wavname)
  wav = obj.read()
  fs = obj.samplerate

  is_multichannel = len(wav.shape) == 2

  if is_multichannel:
    plt.subplot(wav.shape[1], 1, 1)
    plt.title(wavname)

    for ch in range(wav.shape[1]):
      plt.subplot(wav.shape[1], 1, ch+1)
      plotwav(wav[:, ch], fs)
  else:
    plt.subplot(2, 1, 1)
    plt.title(wavname)
    plotwav(wav, fs)
    plt.subplot(2, 1, 2)
    plotspec(wav, fs)

def main():
  [plot_main(wavname) for wavname in sys.argv[1:]]
  plt.show()

if __name__ == "__main__":
  main()
