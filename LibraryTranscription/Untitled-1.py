# %%
from scipy.io.wavfile import read
import math
import numpy as np

SAMPLING_RATE, audio = read('mhll.wav')
BPM = 60

# %%
def getWindow():
    # Convert BPM to approximate number of samples per beat
    interval_seconds = (60 / BPM) / 8 
    #32nd note length
    sample_count = interval_seconds * SAMPLING_RATE
    window = {}
    window["sample_count"] = sample_count
    window["interval_seconds"]= interval_seconds
    return window

w = getWindow()

def splitAudio():
    split_audio = {}
    overlap = 0.5
    start_sample = 0

    # Assuming `w["sample_count"]` and `audio` are properly defined
    sample_count = int(w["sample_count"])

    while start_sample + sample_count <= len(audio): 
        # Slice the segment from the audio
        segment = audio[start_sample : start_sample + sample_count]

        # Create dictionary with time as key
        split_audio[start_sample / SAMPLING_RATE] = segment

        # Move start_sample by overlap
        start_sample = start_sample + int(sample_count * (1 - overlap))
        
        if start_sample + sample_count >= len(audio): 
            segment = audio[start_sample: len(audio)]
            split_audio[start_sample / SAMPLING_RATE] = segment

    return split_audio


# %%

split_audio = splitAudio()
print(split_audio)

# %% [markdown]
# ## FFT ALFORITHm

# %%
import cmath

# %%
def DFT(window): 
    numSamp = len(window)
    DFT_result = {}
    # Loop through frequencies up to Nyquist
    for freq in range(numSamp):
        # Initialize the coefficient for the frequency
        coefficient = 0
        for sample in range(numSamp): 
            # Use cmath.exp for complex exponential
            coefficient += window[sample] * cmath.exp(-2j * cmath.pi * freq / numSamp * sample)
        DFT_result[freq] = coefficient
    return DFT_result

# %%
           
def findDistance(note1, note2): 
    distance = 0
    #*not accounting for # or flats
    n1_letter_val  = ord(note1[0])
    n1_octave  = int(note1[1])
    n2_letter_val  = ord(note2[0])
    n2_octave  = int(note2[1])
    
    distance = np.abs(n1_letter_val - n2_letter_val) + 8 * np.abs(n1_octave - n2_octave)
    
    
    # print("Letter B: ", n1_letter_val, " Octave: ", n1_octave)
    # print("Letter C: ", n2_letter_val, " Octave: ", n2_octave)
    # print("Distance: ", distance)
    return distance

def findClef(score): 
    clefs = {
        "treble": "B5",
        "bass": "D3",
        "alto": "C4"
    }
    measure = 0
    min = 9999999999999
    closestClef = ""
    for clef in clefs: 
        middlenote = clefs[clef]
        for data in score:
            distance = findDistance(data[1], middlenote)
            #* emphasize close notes more
            measure += math.exp(distance)
        
        if measure <= min: 
            min = measure
            closestClef = clef
    return closestClef


def findKeySignature(): 
    keySignatures = { 
        # Key Signatures in the Treble Clef
        "C Major": ["C", "D", "E", "F", "G", "A", "B"],  # No sharps or flats
        "G Major": ["G", "A", "B", "C", "D", "E", "F#"],  # One sharp (F#)
        "D Major": ["D", "E", "F#", "G", "A", "B", "C#"],  # Two sharps (F#, C#)
        "A Major": ["A", "B", "C#", "D", "E", "F#", "G#"],  # Three sharps (F#, C#, G#)
        "E Major": ["E", "F#", "G#", "A", "B", "C#", "D#"],  # Four sharps (F#, C#, G#, D#)
        "B Major": ["B", "C#", "D#", "E", "F#", "G#", "A#"],  # Five sharps (F#, C#, G#, D#, A#)
        "F# Major": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],  # Six sharps (F#, C#, G#, D#, A#, E#)
        "C# Major": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],  # Seven sharps (F#, C#, G#, D#, A#, E#, B#)
        "F Major": ["F", "G", "A", "Bb", "C", "D", "E"],  # One flat (Bb)
        "Bb Major": ["Bb", "C", "D", "Eb", "F", "G", "A"],  # Two flats (Bb, Eb)
        "Eb Major": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],  # Three flats (Bb, Eb, Ab)
        "Ab Major": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],  # Four flats (Bb, Eb, Ab, Db)
        "Db Major": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],  # Five flats (Bb, Eb, Ab, Db, Gb)
        "Gb Major": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],  # Six flats (Bb, Eb, Ab, Db, Gb, Cb)
        "Cb Major": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"],  # Seven flats (Bb, Eb, Ab, Db, Gb, Cb, Fb
                     }
    
    for key_sig in keySignatures:
        count = 0
        min = 999
        bestKey = ""
        for data in score: 
            note = data[1]
            note_name = note[0]
            #print(note_name)
            if note_name not in keySignatures[key_sig]: 
                count += 1 
        if count <= min: 
            bestKey = key_sig
        
    return bestKey
                                                                                                         
print("Closest Clef: ", findClef(score))
print("Key Signature: ", findKeySignature())

# %% [markdown]
# ## FFT code

# %%
signal = [0,1,2,3,4,5,6,7]
frequency_resolution = 1/w["interval_seconds"]


# def fft(signal):
#     q = [0] * 2**int(math.ceil(math.log2(len(signal))))
#     for i in range(len(signal)):
#         q[i] = signal[i]
        
#     N = len(q)
#     if N == 1:
#         return q

#     even_samples = fft(q[::2])
#     odd_samples = fft(q[1::2])

#     amps = [0] * N
#     frequencies = [0] * N
#     for k in range(N // 2):
#         omega_times_odd = cmath.exp(-2j * cmath.pi * k / N) * odd_samples[k]
#         amps[k] = even_samples[k] + omega_times_odd
#         amps[k + N // 2] = even_samples[k] - omega_times_odd
#         frequencies[k] = k*frequency_resolution
#     return frequencies, amps

def fft(signal):
    # Zero-pad to the next power of 2
    q = [0] * 2**int(math.ceil(math.log2(len(signal))))
    for i in range(len(signal)):
        q[i] = signal[i]

    N = len(q)
    if N == 1:
        return q  # Base case: Return the signal itself (complex value)

    # Split into even and odd samples
    even_samples = fft(q[::2])
    odd_samples = fft(q[1::2])

    # Initialize arrays for amplitudes
    amps = [0.0 + 0.0j] * N
    for k in range(N // 2):
        omega_times_odd = cmath.exp(-2j * cmath.pi * k / N) * odd_samples[k]
        amps[k] = even_samples[k] + omega_times_odd
        amps[k + N // 2] = even_samples[k] - omega_times_odd

    return amps  # Only return the amplitudes (no frequencies)

def compute_frequencies(N, sampling_rate):
    frequency_resolution = sampling_rate / N
    return [k * frequency_resolution for k in range(N // 2)]

test = splitAudio()[0]
print("amp: ", fft(test))
print("freq: ", compute_frequencies(test, SAMPLING_RATE))

# %%
from music21 import *
import os

oct4notes = { 
             "D4": 293,
             "E4": 329,
             "C4": 261,
             "G4": 392
             }

def comparenotes(frequency): 
    min = 999
    currnote = ""
    for note in oct4notes: 
        if abs(frequency - oct4notes[note]) <= min: 
            min = abs(frequency - oct4notes[note])
            currnote = note
    return currnote


def stft(signal,threshold): 
    notes = []
    split_signal = splitAudio()
    for time_key in split_signal: 
        
        amps = fft(split_signal[time_key])
        freqs = compute_frequencies(len(amps), SAMPLING_RATE)
        top_index = np.argsort(amps)[-1]
        if amps[top_index] < threshold:
            notes.append("rest")  
        else:
            top_freq = freqs[top_index]
            notes.append(comparenotes(top_freq))
    return notes
        

def get_duration(count): 
    min = 10
    closestnote = ""
    durations = {}
    time = count * w["time_interval"]
    durations["whole"] = 60/BPM * 4
    durations["half"] = durations["whole"] /2 
    durations["quarter"] = durations["whole"]/4
    durations["eighth"] = durations["whole"]/8
    durations["16th"] = durations["whole"]/16
    durations["32nd"] = durations["whole"]/32
    durations["64th"] = durations["whole"]/64
    for length in durations: 
        if abs(time-durations[length]) < min:
            closestnote = length
            min = abs(time-durations[length])
    return closestnote

def makeScore(): 
    
    notes = stft(audio,300)
    score = []
    count = 0 
    for note_index in range(len(notes)): 
        if note_index == len(notes) - 1:
            continue
        cur_note = notes[note_index]
        next_note = notes[note_index + 1]
        if cur_note == next_note:
            count += 1
        else: 
            score.append((cur_note, get_duration(count)))
            count = 0
    return score

        
def create_note(pitch, duration_type):
    n = note.Note(pitch)
    n.duration.type = duration_type
    return n

def makesheetmusic(score): 
    s = stream.Stream()
    
    for data in score: 
        
        note_ = data[0]
        duration = data[1]
        if note_ == "rest":
            rest = note.Rest()
            rest.duration.type = duration
            s.append(rest)
        else:
            s.append(create_note(note_, duration))
    return s
    
score = makeScore()
Music = makesheetmusic(score)
name = input("Enter file name (without extension): ").strip()  # Remove extra spaces

# Create the full output path

output_path = os.path.expanduser(f'~/Fourier/scores/{name}')  # Expand `~` to the home directory
Music.write('musicxml', fp=output_path)
print(f"MusicXML file saved to {output_path}")

# %%


# %%
LEVEL =0 
twiddles = {}
signal = [0,1,2,3,4,5,6,7]
N = len(signal)
#intialize 
for sample in signal: 
    twiddles[sample] = 1
    
def getTwiddles(level, *args): 
    if len(even ) == 1: 
            return
    for list in args: 
        even = list[::2]
        odd = list[1::2]
        level += 1
        for sample in odd: 
            twiddles[sample] *= cmath.exp((-1j * cmath.pi  * 2 * level)/N)
        
        
        getTwiddles(level, even, odd)
        
def computeFFT(): 
    frequencyBins = {}
    for frequency in range(N): 
        sum = 0
        frequencyBins[frequency] = 0
        for sample in range(N): 
            frequencyBins[frequency] += signal[sample] * twiddles[sample]**frequency
    
    return frequencyBins
        
getTwiddles(LEVEL,signal)   
print(twiddles)

for freq in computeFFT(): 
    print("Frequency bin: ", freq, "value: ", computeFFT()[freq])
    
print(DFT(signal))
    


