import numpy as np
import librosa
from music21 import stream, note, environment




# Load an audio file
signal, sr = librosa.load('song.wav', sr=None)

# Perform Fourier Transform
fft_result = np.fft.fft(signal)
fft_freq = np.fft.fftfreq(len(signal), 1 / sr)

# Extract Fundamental Frequencies (simple example)
dominant_freqs = fft_freq[np.abs(fft_result).argsort()[-10:]]  # Top 10 frequencies

# Create Sheet Music
melody = stream.Stream()
for freq in dominant_freqs:
    if freq > 0:  # Ignore negative frequencies
        try:
            pitch_name = note.Note().pitch.frequencyToName(freq)  # Map to note
            melody.append(note.Note(pitch_name))
        except:
            pass

# Save as MusicXML
melody.show()
#melody.write('musicxml', fp='output.xml')
