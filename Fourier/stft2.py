import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal import stft, get_window

# Load the WAV file
sampling_rate, signal = read('mhll.wav')

print("Sampling rate:", sampling_rate)

# Convert to mono if stereo
if len(signal.shape) > 1:
    signal = signal.mean(axis=1)

# Normalize the signal
signal = signal / max(abs(signal))


# Perform Short-Time Fourier Transform
def short_time_fourier_transform(signal, bpm):
    window = get_interval(bpm)  # Get the window for the STFT
    f, t, Zxx = stft(signal, sampling_rate, window=window, nperseg=len(window))
    return f, t, Zxx

# Function to compute a window based on BPM
def get_interval(bpm):
    # Convert BPM to the number of samples per beat
    beat_interval_seconds = 60 / bpm
    sample_count = int(beat_interval_seconds * sampling_rate)
    # Create a triangular window
    window = get_window("triang", sample_count)
    return window


# Compute STFT
bpm = 120  # Set desired BPM
Zxx_filtered = []
frequencies, times, stft_result = short_time_fourier_transform(signal, bpm)






def Spectogram(): 
    # Plot Frequency Spectrum (STFT Spectrogram) with Log Scaling
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(times, frequencies, 10 * np.log10(np.abs(stft_result) + 1e-6), shading='gouraud', cmap='inferno')

    tick_positions = np.linspace(times[0], times[-1], num=24)  # More ticks

    plt.xticks(tick_positions, [f"{tick:.1f}" for tick in tick_positions])  # Custom labels
    plt.title(f"STFT Spectrogram, Sample count: {3000}, Precision: {3000/48000}ms", fontsize = 20)
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.colorbar(label="Amplitude (dB)")
    plt.grid()
    plt.tight_layout()
    plt.show()
    
def Signal():
    # Plot Time-Domain Signal
    time = np.arange(0, len(signal)) / sampling_rate
    plt.figure()
    plt.plot(time, signal)
    plt.title("Time-Domain Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()

def filter():    
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
    


#filter()
#Spectogram()
Signal()





