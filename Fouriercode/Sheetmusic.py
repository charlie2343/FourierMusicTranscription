import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal import stft, get_window
import math

from music21 import *
import os

# Normalize the signal
#signal = signal / max(abs(signal))


BPM = 60
oct4notes = { 
             "D4": 293,
             "E4": 329,
             "C4": 261,
             "G4": 392
             }

score = []
# Load the WAV file


SAMPLING_RATE, signal = read('mhll.wav')
# Convert to mono if stereo
if len(signal.shape) > 1:
    signal = signal.mean(axis=1)

print("Sampling rate:", SAMPLING_RATE)


# Convert BPM to approximate number of samples per beat
time_interval = (60 / BPM) / 8 
#32nd note length
sample_count = time_interval * SAMPLING_RATE
resolution = 1/time_interval
# Ensure window size is appropriate (e.g., capped at 512 samples)
# sample_count = min(sample_count,5000)
print(resolution)
print(f"sample count: {sample_count}")
window = get_window("triang", sample_count)
print("Window type: ", type(window), " Window values: ", window)


# Adjust STFT to scale frequency range to 0 - 1000 Hz
def short_time_fourier_transform(signal, overlap=0.5):  # Get the window for the STFT
    nperseg = len(window)
    noverlap = int(overlap * nperseg)
    f, t, Zxx = stft(signal, SAMPLING_RATE, window=window, nperseg=nperseg, noverlap=noverlap)
    return f, t, Zxx



def getnotes():
    tolerance = 1.0  # Tolerance for frequency persistence in Hz
    frequency = 0
    count = 0
    
    for time_idx, time in enumerate(times):
        if time_idx == 0 or time_idx == len(times) - 1:
            continue
        
        #loop through timeindex and next time index and get all the amplitudes
        time_amplitudes_cur = amplitudes[:, time_idx]
        time_amplitudes_nxt = amplitudes[:, time_idx + 1]
        #get top two significant frequencies indicies
        top_indices_cur = np.argsort(time_amplitudes_cur)[-2:] 
        top_indices_nxt = np.argsort(time_amplitudes_nxt)[-2:]
        
        

        # Compare top frequencies based on indices and apply tolerance
        freq_cur = frequencies[top_indices_cur[1]]
        amp_cur = time_amplitudes_cur[top_indices_cur[1]]
        freq_nxt = frequencies[top_indices_nxt[1]]
        print(f"Time: {time:.2f}s")
        # ! prints indicies of top two freqs
        #print(f"Top indices (current): {top_indices_cur}, Top indices (next): {top_indices_nxt}")
        #  ! prints frequencies of top two
        #print(f"\n Frequencies (current): {frequencies[top_indices_cur]}, Frequencies (next): {frequencies[top_indices_nxt]}")
        # ! prints amplitud of top two
        # print(f"Amplitudes (current): {time_amplitudes_cur[top_indices_cur]}"

        # !prints the top four amplitudes
        top_indices = np.argsort(time_amplitudes_cur)[-4:]  # Get indices of top 4 amplitudes
        for idx in reversed(top_indices):  # Reverse to show the largest first
            print(f"  Frequency: {frequencies[idx]:.2f} Hz, Amplitude: {time_amplitudes_cur[idx]:.2f}")
        
        # ! if in consecutively in top 2 frequencies count increase
        # ! If not, get duration of the frequency, compare it to closest note, and append to list  
        #if freq_cur in frequencies[top_indices_nxt]:
        if np.abs(freq_cur - freq_nxt) <= resolution:
            if amp_cur > 100: 
                count += 1
        elif count != 0 or amp_cur< 210:
            print(f" \n Frequency: {freq_cur:.2f} Hz gone, Amplitude: {amp_cur:.2f}, Count: {count}")
            length = get_duration(count)
            note = comparenotes(freq_cur)
            score.append((freq_cur,note,length,time))
            count = 0
        else: 
            pass


def comparenotes(frequency): 
    min = 999
    currnote = ""
    for note in oct4notes: 
        if abs(frequency - oct4notes[note]) <= min: 
            min = abs(frequency - oct4notes[note])
            currnote = note
    return currnote
    
def get_duration(count): 
    min = 10
    closestnote = ""
    durations = {}
    time = count * (23423/48000)
    durations["whole"] = 60/BPM * 4
    durations["half"] = durations["whole"] /2 
    durations["quarter"] = durations["whole"]/4
    durations["eighth"] = durations["whole"]/8
    durations["sixteenth"] = durations["whole"]/16
    durations["32nd"] = durations["whole"]/32
    
    for note in durations: 
        if abs(time-durations[note]) < min:
            closestnote = note
            min = abs(time-durations[note])
    return closestnote

def Spectrogram(stft): 
    # Plot Frequency Spectrum (STFT Spectrogram) with Log Scaling
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(times, frequencies, 10 * np.log10(np.abs(stft) + 1e-6), shading='gouraud', cmap='inferno')

    tick_positions = np.linspace(times[0], times[-1], num=24)  # More ticks

    plt.xticks(tick_positions, [f"{tick:.1f}" for tick in tick_positions])  # Custom labels
    plt.title(f"STFT Spectrogram, Sample count: {3000}, Precision: {3000/48000}ms", fontsize = 20)
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.colorbar(label="Amplitude (dB)")
    plt.grid()
    plt.tight_layout()
    plt.show()
    


#####!!!!! Music 21 creation
def create_note(pitch, duration_type):
    n = note.Note(pitch)
    n.duration.type = duration_type
    return n

def makesheetmusic(score): 
    s = stream.Stream()
    for data in score: 
        frequency = data[0]
        note_ = data[1]
        duration = data[2]
        time = data[3]
        s.append(create_note(note_, duration))
    return s
        
        





frequencies, times, stft_result = short_time_fourier_transform(signal)

# Filter frequency range to 0 - 1000 Hz
max_freq = 1000  # Define maximum frequency for display
freq_filter = frequencies <= max_freq  # Create filter
frequencies = frequencies[freq_filter]  # Apply filter to frequencies
stft_result = stft_result[freq_filter, :]  # Apply filter to STFT result
#print(frequencies)

# Filter: Remove frequencies with amplitude > threshold
amplitudes = stft_result  # Get amplitudes
print(amplitudes)
threshold = 0.15  # Define amplitude threshold
mask = amplitudes >= threshold  # Create mask
Zxx_filtered = stft_result * mask  # Zero out high-amplitude bins
# for i in range(0,len(amplitudes)): 
#     if amplitudes[i] >= threshold:
#         filtered = stft_result[i]
        
#print(filtered)
        # Calculate the amplitudes in linear scale
amplitudes = np.abs(stft_result)


getnotes()

#print(Zxx_filtered)

#print("Max amplitude (linear):", np.max(amplitudes))

#Spectrogram(stft_result)
#Spectrogram(Zxx_filtered)
#print(score)

print(score)
Music = makesheetmusic(score)
name = input("Enter file name (without extension): ").strip()  # Remove extra spaces

# Create the full output path

output_path = os.path.expanduser(f'~/Fourier/scores/{name}')  # Expand `~` to the home directory
Music.write('musicxml', fp=output_path)
print(f"MusicXML file saved to {output_path}")


