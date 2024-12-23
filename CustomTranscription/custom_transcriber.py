# import libraries for reading
from scipy.io.wavfile import read
import math
# 
# read in file
SAMPLING_RATE, audio = read("mhll.wav")
# 
# Break into windows based on BPM
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
# windows should have length, sample count
#

#Create windows from window function
w = getWindow()
# for sample in audio: 
#     startSample = 0
    
#     go from starttime to window[sample_count]
#     save data in new list
#     add data to new segmented dict^2 representing audio file
#     ([ time1: window array 1, 
#         time2: window array 2])
#         starttime = startime + window *overlap
#     return split_audio

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

# Call the function
split_audio = splitAudio()
#print("Split Audio: ", split_audio)


#Create DFT
import cmath  # Use cmath for complex number calculations

def DFT(window): 
    numSamp = len(window)
    DFT_result = {}
    # Loop through frequencies up to Nyquist
    for freq in range(int(numSamp / 2) - 1):
        # Initialize the coefficient for the frequency
        coefficient = 0
        for sample in range(numSamp): 
            # Use cmath.exp for complex exponential
            coefficient += window[sample] * cmath.exp(-2j * cmath.pi * freq / numSamp * sample)
        DFT_result[freq] = coefficient
    return DFT_result

# Assuming split_audio and w are correctly defined
dft = DFT(split_audio[13.375])
print(dft)

#     #
# #s
# #create StFT array from dft on split audio
# Stft_result = {}
# for time in split_audio: 
#     #list of dicts
#     stft_result.add(time: DFT(segment, Window))
    
#
#
#

#
#
#
#
