from pydub import AudioSegment
import numpy as np
import pyfftw
import matplotlib.pyplot as plt

# Function to convert frequency to musical note
def frequency_to_note(freq):
    A4 = 440.0  # Frequency of A4
    C0 = A4 * np.power(2, -4.75)
    note_num = 12 * np.log2(freq / C0)
    note = int(round(note_num)) % 12
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return note_names[note]

# Load MP3 file
audio_file = "2.mp3"
audio_segment = AudioSegment.from_file(audio_file)

# Convert audio segment to raw audio data
samples = np.array(audio_segment.get_array_of_samples())
sample_rate = audio_segment.frame_rate

# Perform FFT using FFTW
fft_result = pyfftw.interfaces.numpy_fft.fft(samples)
fft_freq = np.fft.fftfreq(len(fft_result), 1.0 / sample_rate)

# Get the magnitude of the FFT
magnitude = np.abs(fft_result)

# Find the peak frequency
peak_index = np.argmax(magnitude)
peak_freq = abs(fft_freq[peak_index])

# Convert peak frequency to musical note
note_name = frequency_to_note(peak_freq)

print(f"Peak Frequency: {peak_freq:.2f} Hz, Note: {note_name}")

# Optionally, plot the FFT result
plt.plot(fft_freq[:len(fft_freq)//2], magnitude[:len(magnitude)//2])
plt.xlim(0,500)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("FFT of MP3 File: "+ audio_file)
plt.show()
