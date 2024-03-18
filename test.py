import os, wave, sys
import numpy as np
# %pip install matplotlib
import matplotlib.pyplot as plt
# %pip install scipy
from scipy import signal
from scipy.io.wavfile import read, write
from scipy.signal import spectrogram
from scipy.io import wavfile
from sklearn.decomposition import FastICA

def get_wav_files_in_current_directory(directory):
    wav_files = [f"{directory}\\{file}" for file in os.listdir(directory) if file.endswith('.wav')]
    return wav_files

wav_files_in_current_directory = get_wav_files_in_current_directory(".\\sounds\\OriginalSounds")

def plot_waveform_and_spectrogram(wav_file):
    plt.rcParams["figure.figsize"] = [10, 6]
    plt.rcParams["figure.autolayout"] = True

    # Read the WAV file
    sample_rate, audio = read(wav_file)
    
    # Plot waveform
    plt.subplot(2, 1, 1)
    plt.plot(audio)
    plt.title("Waveform: " + wav_file)
    plt.ylabel("Amplitude")
    plt.xlabel("Time")

    # Plot spectrogram
    plt.subplot(2, 1, 2)
    plt.specgram(audio, Fs=sample_rate)
    plt.title("Spectrogram: " + wav_file)
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [sec]")

    plt.show()

print(wav_files_in_current_directory)

# הצגת ספקטרוגרמה של כל קובץ קול בתיקייה הנוכחית
for wav_file in wav_files_in_current_directory:
    plot_waveform_and_spectrogram(wav_file)

random_matrix = np.random.uniform(0.5, 2.5, size=(6, 6))
print(f"random mixing matrix: {random_matrix}")

mixed_audio_names = []

# Reading and saving the mixed signals
for idx, audio_file in enumerate(wav_files_in_current_directory):
    # Reading the audio from the file
    sample_rate, audio_data = read(audio_file)
    
    # Reshaping the array to a matrix
    reshaped_audio = np.reshape(audio_data, (-1, 1))
    reshaped_random_matrix = np.reshape(random_matrix, (1, -1))

    # Multiplying the audio by the mixing matrix
    mixed_audio = np.dot(reshaped_audio, reshaped_random_matrix)

    # Setting a new file name
    output_file = f".\\sounds\\MixedSounds\\mixed_audio_{idx}.wav"

    new_audio = wave.open(output_file, 'w')
    new_audio.setnchannels(1)
    new_audio.setsampwidth(2)
    new_audio.setframerate(sample_rate)
    new_audio.setcomptype('NONE', 'Not Compressed')
    new_audio.writeframes(mixed_audio.tobytes())
    new_audio.close()

    mixed_audio_names.append(output_file)
    
    print(f"Mixed audio from file {audio_file} was successfully saved in file {output_file}")

    mixed_audio_names = []

# Reading and saving the mixed signals
for idx, audio_file in enumerate(wav_files_in_current_directory):
    # Reading the audio from the file
    sample_rate, audio_data = read(audio_file)
    
    # Reshaping the array to a matrix
    reshaped_audio = np.reshape(audio_data, (-1, 1))
    reshaped_random_matrix = np.reshape(random_matrix, (1, -1))

    # Multiplying the audio by the mixing matrix
    mixed_audio = np.dot(reshaped_audio, reshaped_random_matrix)

    # Setting a new file name
    output_file = f".\\sounds\\MixedSounds\\mixed_audio_{idx}.wav"

    new_audio = wave.open(output_file, 'w')
    new_audio.setnchannels(1)
    new_audio.setsampwidth(2)
    new_audio.setframerate(sample_rate)
    new_audio.setcomptype('NONE', 'Not Compressed')
    new_audio.writeframes(mixed_audio.tobytes())
    new_audio.close()

    mixed_audio_names.append(output_file)
    
    print(f"Mixed audio from file {audio_file} was successfully saved in file {output_file}")

# ה. הפעלת ICA לפרידת האותות
    
# Compute ICA
ica = FastICA(n_components=6, whiten="arbitrary-variance")
S_ = ica.fit_transform(X)  # Reconstruct signals
A_ = ica.mixing_  # Get estimated mixing matrix


# ica = FastICA(n_components=6)
# ica.fit(mixed_audio.T)
# reconstructed_sources = ica.transform(mixed_audio.T).T

for i, reconstructed_source in enumerate(reconstructed_sources):
    # Setting a new file name
    output_file = f".\\reconstructed_source{i+1}.wav"

    new_audio = wave.open(output_file, 'w')
    new_audio.setnchannels(1)
    new_audio.setsampwidth(2)
    new_audio.setframerate(sample_rate)
    new_audio.setcomptype('NONE', 'Not Compressed')
    new_audio.writeframes(reconstructed_source.tobytes())
    new_audio.close()

for i in range(6):
    plot_waveform_and_spectrogram(f".\\reconstructed_source{i+1}.wav")