import cmath
import time
from scipy.io.wavfile import read

#audio = [0,1,2,3,4,5,6,7]
SAMPLING_RATE, audio = read("mhll.wav")

def fft(): 
    split_data = []
    even = []   
    odd = []
    for index, data in enumerate(audio): 
        if index % 2== 0: 
            even.append(data)
        else: 
            odd.append(data)
    split_data.append(even)
    split_data.append(odd)
     
    print(split_data)


def DFT(window): 
    start = time.time()
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
    end = time.time()
    print(f"Elapsed time: {start-end}")
    return DFT_result

def FFTtest(window): 
    first = window[0]
    second = window[1]
    DFT_result = {}
    # Loop through frequencies up to Nyquist
    for freq in range(4):
        # Initialize the coefficient for the frequency
        coefficient = 0
        for sample in range(4): 
            # Use cmath.exp for complex exponential
            coefficient += first[sample] * cmath.exp(-2j * cmath.pi * freq / 4 * sample)
        DFT_result[freq] = coefficient
        DFT_result[freq+4] = coefficient
    for freq in range(4): 
        for sample in range(4): 
            # Use cmath.exp for complex exponential
            coefficient += second[sample] * cmath.exp(-2j * cmath.pi * freq / 4 * sample)
        DFT_result[freq] += coefficient
        DFT_result[freq+4] -= coefficient
    return DFT_result

def pairFreq(): 
    firsthalf = audio[slice(0,len(audio))/2]
    secondhalf = sdf

print(DFT(audio))

