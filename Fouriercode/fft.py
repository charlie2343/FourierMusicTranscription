import cmath
import time
from scipy.io.wavfile import read

audio = [0,1,2,3,4,5,6,7]
#SAMPLING_RATE, audio = read("mhll.wav")

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
    # evenSamples
    # for i in range(0, len(window)): 
    #     if i % 2 ==0: 
    #         evenSamples = window[i] 
    #     oddSamples = window[1]
    FFT_result = {}
    even = 0
    odd = 0
    # Loop through frequencies up to Nyquist
    for freq in range(4):
        # Initialize the coefficient for the frequency
        even =0
        odd = 0
        for sample in range(4): 
            # Use cmath.exp for complex exponential
            even += window[sample*2] * cmath.exp(-2j * cmath.pi * freq / 4 * sample)
            odd += window[sample*2 +1] * cmath.exp(-2j * cmath.pi * freq / 4 * sample)
        
        FFT_result[freq] = even + cmath.exp(-1j * cmath.pi * freq/4) * odd
        FFT_result[freq+4] = even + odd * cmath.exp(-1j * cmath.pi * (freq+4)/4)
    
    # for freq in range(4): 
    #     for sample in range(4): 
    #         # Use cmath.exp for complex exponential
    #         coefficient += second[sample] * cmath.exp(-2j * cmath.pi * freq / 4 * sample)
    #     DFT_result[freq] += coefficient
    #     DFT_result[freq+4] -= coefficient
    return FFT_result

def pairFreq(): 
    firsthalf = audio[slice(0,len(audio))/2]
    secondhalf = sdf

print(DFT(audio))
print(FFTtest(audio))
