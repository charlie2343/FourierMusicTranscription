import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal import stft, get_window
import math

from music21 import *
import os




##!!WINDOW calculation
SAMPLING_RATE, signal = read('mhll.wav')
# Convert to mono if stereo
if len(signal.shape) > 1:
    signal = signal.mean(axis=1)

print("Sampling rate:", SAMPLING_RATE)


# Convert BPM to approximate number of samples per beat
time_interval = 0.0625 # 1/16th note length
#32nd note length
sample_count = time_interval * SAMPLING_RATE
resolution = 1/time_interval
# Ensure window size is appropriate (e.g., capped at 512 samples)
sample_count = 3000
print(resolution)
print(f"sample count: {sample_count}")
window = get_window("triang", sample_count)
print("Window type: ", type(window), " Window values: ", window)


# Adjust STFT to scale frequency range to 0 - 1000 Hz
def short_time_fourier_transform(signal, overlap=0):  # Get the window for the STFT
    nperseg = len(window)
    noverlap = int(overlap * nperseg)
    f, t, Zxx = stft(signal, SAMPLING_RATE, window=window, nperseg=nperseg, noverlap=noverlap)
    return f, t, Zxx


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

def filterTopNotes(frequencies, times, Zxx, threshold): 
    top_notes = []
    for time_idx, time in enumerate(times):
        freq_amplitudes = np.abs(Zxx[:, time_idx])
        top_index = np.argsort(freq_amplitudes)[-1:]
        if freq_amplitudes[top_index] < threshold:
            top_notes.append("rest")
        else: 
            top_notes.append(comparenotes(frequencies[top_index]))
    return top_notes

BPM = 60

def get_duration(count): 
    min = 10
    closestnote = ""
    durations = {}
    time = count * time_interval
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
    frequencies, times, stft_result = short_time_fourier_transform(signal)
    notes = filterTopNotes(frequencies, times, stft_result, 300)
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

print("Score: ", makeScore())



##MUSIC21 
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

def Signal():
    # Plot Time-Domain Signal
    time = np.arange(0, len(signal)) / SAMPLING_RATE
    plt.figure()
    plt.plot(time, signal)
    plt.title("Time-Domain Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()
    
##################RUNNING THE CODE##################
score = makeScore()
Music = makesheetmusic(score)
name = input("Enter file name (without extension): ").strip()  # Remove extra spaces

# Create the full output path

output_path = os.path.expanduser(f'~/Fourier/scores/{name}')  # Expand `~` to the home directory
Music.write('musicxml', fp=output_path)
print(f"MusicXML file saved to {output_path}")

#Signal()