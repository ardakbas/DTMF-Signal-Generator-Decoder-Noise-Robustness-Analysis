import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import specialized_functions as sf
from os import remove

#Maximum frequency for the number in the phone is 1633. To satisfy Nyquist criterion(fs>2*fmax), it must be 3266 at least.
#To keep things standirdized, f_s = 8000.
#T denotes passing time when grabbed to the number buttons.

f_s = 8000
T = 0.5
N = 4000
time_arr = np.linspace(0,T,N)


keypad_frequencies = {"1":(sf.low_frequencies[0],sf.high_frequencies[0]), "2":(sf.low_frequencies[0],sf.high_frequencies[1]),
                    "3":(sf.low_frequencies[0],sf.high_frequencies[2]), "4":(sf.low_frequencies[1],sf.high_frequencies[0]), 
                    "5":(sf.low_frequencies[1],sf.high_frequencies[1]), "6":(sf.low_frequencies[1],sf.high_frequencies[2]),
                    "7":(sf.low_frequencies[2],sf.high_frequencies[0]), "8":(sf.low_frequencies[2],sf.high_frequencies[1]),
                    "9":(sf.low_frequencies[2],sf.high_frequencies[2]), "0":(sf.low_frequencies[3],sf.high_frequencies[1])}

#We generate a composite signal for digit "5" by summing two sine waves corresponding to its row and column frequencies. 
#The signal is normalized to stay within the [-1, 1] range and then quantized to 16-bit Integer format for audio storage.

f_low = keypad_frequencies["5"][0]
f_high = keypad_frequencies["5"][1]
low_signal = np.sin(2*np.pi*f_low*time_arr)
high_signal = np.sin(2*np.pi*f_high*time_arr)
total_signal = low_signal + high_signal
normalized_total = total_signal/2

#Visualization of the first 100 samples in the time domain
plt.plot(time_arr[0:100],normalized_total[0:100])
plt.title("First 100 Elements of Signal")
plt.xlabel("Time")
plt.ylabel("Magnitude")
plt.xlim(0,0.0125)
plt.grid()
plt.tight_layout()
plt.show()

#There is quantization to ensure valid data type into 'write' function. 
#Multiplying 32767 corresponds to magnitude. 
quantized = np.int16(normalized_total*32767)
write("Soundof5.wav",8000,quantized)

#To analyze frequencies, there is Fourier transformed version.
#There is also scaling in terms of frequency for x domain.
f_dom_quantized = np.fft.fft(normalized_total)
f_dom_abs_quantized = np.abs(f_dom_quantized)[:N//2]/(N/2)
freq_arr = np.fft.fftfreq(N,1/f_s)[:N//2]

#Frequency domain representation of digit '5
plt.plot(freq_arr,f_dom_abs_quantized)
plt.title("Magnitude with Respect to Frequencies")
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.grid()
plt.show()

#Creating a phone number and saving
given_num = sf.generate_full_tone("55588899922", f_s, T)
write("Given_Num.wav", f_s, given_num)

#Extracting the number created
solved_num = sf.find_phone_num("Given_Num.wav",T)
print(solved_num)  

#Testing the capability of solving with some noise
noise1 = np.float16(np.random.normal(0, 500, len(given_num)))
noisy_signal = np.float32(given_num + noise1)
noisy_signal = np.clip(noisy_signal,-32768,32767).astype(np.int16)
write("Noisy_signal.wav",f_s, noisy_signal)
solved_noisy_signal = sf.find_phone_num("Noisy_signal.wav",T)
print(f"Your noisy signal's number is {solved_noisy_signal}")

#Testing with more noise
noise2 = np.float32(np.random.normal(0,30000,len(given_num)))
noisy_signal_2 = np.float32(given_num + noise2)
noisy_signal_2 = np.clip(noisy_signal_2,-32768,32767).astype(np.int16)
write("noisy_signal_2.wav",f_s,noisy_signal_2)
solved_noisy_signal_2 = sf.find_phone_num("noisy_signal_2.wav",T)
print(solved_noisy_signal_2)

#Testing with the values up to 50000
threshold_ = False
for i in range(0,50000,500):
    noise = np.float32(np.random.normal(0,i,len(given_num)))
    noisy_signal_3 = np.float32(noise + given_num)
    noisy_signal_3 = np.clip(noisy_signal_3,-32768,32767).astype(np.int16)
    write("Trial.wav",f_s,noisy_signal_3)
    solved_noisy_signal_ = sf.find_phone_num("Trial.wav",T)
    i = -1
    if solved_noisy_signal_ != solved_num:
        print(f"Threshold is {i}")
        threshold_ = True
        break
if i == True: print("Successfully tested.")

remove("Trial.wav")
    
#Spectogram visualization
plt.specgram(noisy_signal_3, Fs=f_s, NFFT=1024, noverlap=512)
plt.title("Phone Number's Spectogram")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.colorbar(label="Density (dB)")
plt.ylim(600, 1800) 
plt.show()

#Testing filter_signal function and comparison with unfiltered, raw noisy version with using graph 
#Also, there is no changing in dominant frequencies after filtering
filtered_noisy_signal_2 = sf.filter_signal(noisy_signal_2,f_s,600,1700,5)
filtered_noisy_signal_2 = np.clip(filtered_noisy_signal_2,-32768,32767).astype(np.int16)
write("noisy_signal_2_filtered.wav",f_s,filtered_noisy_signal_2)

f_filtered = np.abs(np.fft.fft(filtered_noisy_signal_2)[:int(len(noisy_signal_2)/2)]/(len(noisy_signal_2)/2))
f_noisy = np.abs(np.fft.fft(noisy_signal_2)[:int(len(noisy_signal_2)/2)]/(len(noisy_signal_2)/2))
freq_axis = np.fft.fftfreq(len(noisy_signal_2), 1/f_s)[:len(noisy_signal_2)//2]

plt.plot(freq_axis,f_noisy, c = "blue", label = "Noisy Signal")
plt.plot(freq_axis, f_filtered, c = "red", label = "Filtered Noisy Data")
plt.legend()
plt.title("Filtered vs Raw Noisy Data in Frequency Domain")
plt.xlabel("Frequencies")
plt.ylabel("Magnitudes")
plt.show()


