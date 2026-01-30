# DTMF-Signal-Generator-Decoder-Noise-Robustness-Analysis
This project implements a complete DTMF (Dual-Tone Multi-Frequency) communication system simulation. It covers signal generation, quantization, frequency-domain analysis, and advanced noise filtering techniques.

# Key Features
Dual-Tone Generation: Synthesizes standard keypad tones using additive sine wave synthesis.

Quantization: Signals are processed in 16-bit PCM format (int16), ensuring compatibility with standard .wav audio files.

Fourier Analysis: Utilizes Fast Fourier Transform (FFT) for precise frequency identification of dual tones.

Robustness Stress Test: Includes an automated loop to determine the system's "Breaking Point" (Threshold) under increasing Additive White Gaussian Noise (AWGN).

Digital Filtering: Features a 5th-order Butterworth Band-pass Filter to isolate DTMF frequencies (600Hz - 1750Hz) and suppress out-of-band interference.

# Visualizations
The script provides detailed plots to analyze the signal's life cycle:

Time Domain: Observation of the interference pattern between dual frequencies.

Frequency Domain: Identifying peak magnitudes via FFT.

Spectrogram: A time-frequency mapping that shows the chronological sequence of the dialed number.

Filter Analysis: Comparison of raw noisy spectra vs. filtered spectra.

# Necessary Libraries
Matplotlib

Scipy

# Usage
Place specialized_functions.py and code.py in the same directory.

The specialized_functions.py contains the core engine (Decoding, Filtering, Synthesis).

Run code.py to execute the full analysis, including noise tests and visualizations.
