import matplotlib as plt
import numpy as np

class Analyzer: 
    
    def __init__(self,):
        
        self.max = 0
        self.notes = {}
        
        
    def get_duration(count, samplecount,BPM): 
        max = 10
        closestnote = ""
        durations = {}
        time = count * (samplecount/48000)
        durations["whole"] = 60/BPM * 4
        durations["half"] = durations["whole"] /2 
        durations["quarter"] = durations["whole"]/4
        durations["eigth"] = durations["whole"]/8
        durations["sixteenth"] = durations["whole"]/16
        durations["thirty2nd"] = durations["whole"]/32
        
        for note in durations: 
            if abs(time-durations[note]) < max:
                closestnote = note
                max = abs(time-durations[note])
        return closestnote
    
    def get_note(frequency): 
        max = 80
        currnote = ""
        for note in oct4notes: 
            if abs(frequency - oct4notes[note]) <= max: 
                max = abs(frequency - oct4notes[note])
                currnote = note
        return currnote
    
    def Spectogram(times, frequencies, stft_result): 
    # Plot Frequency Spectrum (STFT Spectrogram) with Log Scaling
        plt.figure(figsize=(10, 6))
        plt.pcolormesh(times, frequencies, 10 * np.log10(np.abs(stft_result) + 1e-6), shading='gouraud', cmap='inferno')

        tick_positions = np.linspace(times[0], times[-1], num=24)  # More ticks

        plt.xticks(tick_positions, [f"{tick:.1f}" for tick in tick_positions])  # Custom labels
        plt.title("STFT Spectrogram (0-1000 Hz, Log-Scaled Amplitude)")
        plt.xlabel("Time (s)")
        plt.ylabel("Frequency (Hz)")
        plt.colorbar(label="Amplitude (dB)")
        plt.grid()
        plt.tight_layout()
        plt.show()
