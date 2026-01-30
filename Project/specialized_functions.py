import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write, read
from scipy import signal

low_frequencies = np.array([697,770,852,941])
high_frequencies = np.array([1209,1336,1477,1633])


keypad_frequencies = {"1":(low_frequencies[0],high_frequencies[0]), "2":(low_frequencies[0],high_frequencies[1]),
                    "3":(low_frequencies[0],high_frequencies[2]), "4":(low_frequencies[1],high_frequencies[0]), 
                    "5":(low_frequencies[1],high_frequencies[1]), "6":(low_frequencies[1],high_frequencies[2]),
                    "7":(low_frequencies[2],high_frequencies[0]), "8":(low_frequencies[2],high_frequencies[1]),
                    "9":(low_frequencies[2],high_frequencies[2]), "0":(low_frequencies[3],high_frequencies[1])}


def find_dominant_frequencies(your_data, freq_arr):

    """
    Identifies peak frequency components within the low and high DTMF frequency groups.

    :param your_data: The magnitude values.
    :param freq_arr: Frequency array for 
    
    """

    mask1 = (freq_arr >= 600) & (freq_arr <= 1000)
    idx1 = np.argmax(your_data[mask1])
    detected_freq_1 = freq_arr[mask1][idx1]

    mask2 =  (freq_arr >= 1100) & (freq_arr <= 1700)
    idx2 = np.argmax(your_data[mask2])
    detected_freq_2 = freq_arr[mask2][idx2]

    idx1 = np.argmin(np.abs((low_frequencies - detected_freq_1)))
    idx2 = np.argmin(np.abs((high_frequencies - detected_freq_2)))

    return low_frequencies[idx1], high_frequencies[idx2]


def generate_tone(key, f_s, duration):

    """
    This function aims to create the audio for key.

    :param key: This parameter is used for only 1 digit (0-9).
    :param f_s: Sampling rate in hertz
    :param duration: This parameter denotes the passing time when grabbed to digit.
    
    """

    freq1 = keypad_frequencies[key][0]
    freq2 = keypad_frequencies[key][1]

    time_arr = np.linspace(0,duration,int(duration*f_s))
    total_normalized = (np.sin(2*np.pi*freq1*time_arr) + np.sin(np.pi*2*freq2*time_arr)) /2
    quantized_tone = np.int16(total_normalized*32767)

    quiet_samples = int(f_s*0.1)
    quietness  = np.zeros(quiet_samples, dtype= np.int16)

    full_tone = np.concatenate([quantized_tone,quietness])

    return full_tone

def generate_full_tone(yournum, f_s, duration):

    """
    This function is used for creating phone number voice with 11 digit.

    :param yournum: Your phone number
    :param f_s: Sampling rate in hertz
    :param duration: The passing time when grabbed to digit
    """

    inst_tone = np.array([],dtype=np.int16)

    for i in yournum:
        inst_tone = np.concatenate([inst_tone,generate_tone(i,f_s,duration)])

    return inst_tone
    
def get_key_from_frequencies(low, high):
    """    
    This function is created to extract the digit which corresponds to given values from the key pad.

    :param low: Value of dominant low frequency
    :param high: Value of dominant high frequency
    """


    for key ,(f_low, f_high) in keypad_frequencies.items():
        if (f_low == low) and (f_high == high):
            return key
    return "" 

def find_phone_num(file_extension,duration):

    """
    This function is created to extract the phone number from given audio file.

    :param file_extension: File location of calling number
    :param duration: Time interval between 2 digit
    """


    f_s, signal= read(file_extension)

    yournum = ""

    N_voice = int(f_s*duration)
    N_quiet = int(f_s*0.1)
    N_block = N_voice + N_quiet
    total_time = len(signal)

    freq_arr = np.fft.fftfreq(N_voice,1/f_s)[:N_voice//2]

    for i in range(0, total_time, N_block):
        
        melody1 = signal[i:i+N_voice]
        melody1 = np.abs(np.fft.fft(melody1))[:N_voice//2]/(N_voice/2)

        freq1, freq2 = find_dominant_frequencies(melody1,freq_arr)    

        key = get_key_from_frequencies(freq1, freq2)

        yournum += key
    
    return yournum


def filter_signal(your_data, f_s,cut_low, cut_high,order):
    """
    This function is designed for preventing the frequencies that cannot be in given audio in the context of DTMF. 
    
    :param your_data: Raw data
    :param f_s: Sampling rate in hertz
    :param cut_low: Low cut off frequency 
    :param cut_high: High cut off frequency
    :param order: Degree of filter
    """

    w_low = cut_low /(f_s/2)
    w_high = cut_high/(f_s/2)

    b,a = signal.butter(order, [w_low, w_high], 'band')

    return signal.filtfilt(b, a, your_data)


    