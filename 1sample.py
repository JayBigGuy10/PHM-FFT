from pydub import AudioSegment
import numpy as np
import pyfftw
import matplotlib.pyplot as plt

# Function to convert frequency to musical note
def frequency_to_note(freq):
    A4 = 440.0  # Frequency of A4
    C0 = A4 * np.power(2, -4.75)
    if freq == 0:
        return " "
    else:
        note_num = 12 * np.log2(freq / C0)
        note = int(round(note_num)) % 12
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return note_names[note]

# Load MP3 file
audio_file = "3.mp3"
audio_segment = AudioSegment.from_file(audio_file)

# Convert audio segment to raw audio data
samples = np.array(audio_segment.get_array_of_samples())
sample_rate = audio_segment.frame_rate

# Define chunk size
CHUNK_SIZE = 1024

# Process the audio data in chunks
num_chunks = len(samples) // CHUNK_SIZE
notes = []

for i in range(num_chunks):
    # Get the current chunk
    chunk = samples[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE]

    # Perform FFT using FFTW
    fft_result = pyfftw.interfaces.numpy_fft.fft(chunk)
    fft_freq = np.fft.fftfreq(len(fft_result), 1.0 / sample_rate)

    # Get the magnitude of the FFT
    magnitude = np.abs(fft_result)

    # Find the peak frequency
    peak_index = np.argmax(magnitude)
    peak_freq = abs(fft_freq[peak_index])

    # Convert peak frequency to musical note
    note_name = frequency_to_note(peak_freq)
    notes.append(note_name)

    print(f"Chunk {i + 1}/{num_chunks}: Peak Frequency: {peak_freq:.2f} Hz, Note: {note_name}")

# Optionally, plot the results
plt.plot(range(num_chunks), [frequency_to_note(abs(np.fft.fftfreq(len(pyfftw.interfaces.numpy_fft.fft(samples[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE])), 1.0 / sample_rate)[np.argmax(np.abs(pyfftw.interfaces.numpy_fft.fft(samples[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE])))])) for i in range(num_chunks)], marker='o')
plt.xlabel("Chunk Number")
plt.ylabel("Note")
plt.title("Detected Notes per Chunk "+audio_file)
plt.show()
