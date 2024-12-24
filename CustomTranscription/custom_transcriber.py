from scipy.io.wavfile import read
import math
import numpy as np

import os

# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the relative path to the 'mhll.wav' file
audio_file_path = os.path.join(script_dir, 'mhll.wav')

# Read the audio file
SAMPLING_RATE, audio = read(audio_file_path)
BPM = 60

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
time_interval = w["interval_seconds"]

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



# split_audio = splitAudio()
# print(split_audio)

import cmath


frequency_resolution = 1/w["interval_seconds"]



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
amps = fft(test)
print("amp: ", len(amps))
print("freq: ", len(compute_frequencies(len(amps*2), SAMPLING_RATE)))






##!!!;SD:LFKJSDL:F
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
        freqs = compute_frequencies(len(amps*2), SAMPLING_RATE)
        top_index = np.argsort(amps)[-1]
        if amps[top_index] < threshold:
            notes.append("rest")  
        else:
            top_freq = freqs[top_index]
            print("time: ", time_key, "freq: ",top_freq)
            notes.append(comparenotes(top_freq))
    return notes

stft(audio, 300)

def get_duration(count): 
    min = 10
    closestnote = ""
    durations = {}
    time = count * w["interval_seconds"]
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
    
# score = makeScore()
# Music = makesheetmusic(score)
# name = input("Enter file name (without extension): ").strip()  # Remove extra spaces

# # Create the full output path

# output_path = os.path.expanduser(f'~/Fourier/scores/{name}')  # Expand `~` to the home directory
# Music.write('musicxml', fp=output_path)
# print(f"MusicXML file saved to {output_path}")