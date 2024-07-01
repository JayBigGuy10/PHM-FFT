import pyaudio
import numpy as np
import pyfftw
from collections import Counter
import matplotlib.pyplot as plt

# Parameters
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate (44.1 kHz)
CHUNK = 4096  # Size of audio chunks to read

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open a stream with the desired parameters
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# ----------- Load MP3 file
from pydub import AudioSegment
audio_file = "3.mp3"
audio_segment = AudioSegment.from_file(audio_file)

# Convert audio segment to raw audio data
samples = np.array(audio_segment.get_array_of_samples())
sample_rate = audio_segment.frame_rate

# Process the audio data in chunks
num_chunks = len(samples) // CHUNK
notes = []
# ------------ End Load MP3

print("Recording...")

prev_note = 0

note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
A4 = 440.0  # Frequency of A4
C0 = A4 * np.power(2, -4.75)

def freq_to_note_name(freq):
    if freq == 0:
        return None
    note_num = 12 * np.log2(freq / C0)
    note = int(round(note_num)) % 12
    return note_names[note]

# Simplified chord dictionary
chord_dict = {
    ('C', 'E', 'G'): 'C Major',
    ('D', 'F#', 'A'): 'D Major',
    ('E', 'G#', 'B'): 'E Major',
    ('F', 'A', 'C'): 'F Major',
    ('G', 'B', 'D'): 'G Major',
    ('A', 'C#', 'E'): 'A Major',
    ('B', 'D#', 'F#'): 'B Major',
    ('C', 'D#', 'G'): 'C Minor',
    ('D', 'F', 'A'): 'D Minor',
    ('E', 'G', 'B'): 'E Minor',
    ('F', 'G#', 'C'): 'F Minor',
    ('G', 'A#', 'D'): 'G Minor',
    ('A', 'C', 'E'): 'A Minor',
    ('B', 'D', 'F#'): 'B Minor'
}

def identify_chord(notes):
    notes = tuple(sorted(notes))
    return chord_dict.get(notes, "Unknown")

try:
    #Audio Stream
    #while True:
        # Read a chunk of audio data
    #    data = stream.read(CHUNK)
    #    audio_data = np.frombuffer(data, dtype=np.int16)
    #end audio stream

    #Mp3 file
    for i in range(num_chunks):
        # Get the current chunk
        audio_data = samples[i * CHUNK:(i + 1) * CHUNK]
    #end mp3 file

        # Perform FFT using FFTW
        fft_result = pyfftw.interfaces.numpy_fft.fft(audio_data)
        fft_freq = np.fft.fftfreq(len(fft_result), 1.0 / RATE)

        # Get the magnitude of the FFT
        magnitude = np.abs(fft_result)
        #print(magnitude)

        # Find the peak frequency
        peak_index = np.argmax(magnitude)
        peak_freq = abs(fft_freq[peak_index])

        # Threshold to consider significant peaks
        threshold = np.max(magnitude) * 0.3
        significant_indices = np.where(magnitude > threshold)[0]

        # Find peak frequencies and their magnitudes
        peak_freqs = [(abs(fft_freq[i]), magnitude[i]) for i in significant_indices]

        # Sort peaks by magnitude (loudest first)
        peak_freqs.sort(key=lambda x: x[1], reverse=True)

        # Use a dictionary to keep the loudest example of each note
        loudest_notes = {}
        for freq, mag in peak_freqs:
            note = freq_to_note_name(freq)
            if note and (note not in loudest_notes or mag > loudest_notes[note][0]):
                loudest_notes[note] = (int(mag),int(freq))

        loudest_notes_sorted = sorted(loudest_notes.items(), key=lambda x: x[0], reverse=True)
        peak_notes = [(note,mag) for note, mag in loudest_notes_sorted[:12]]

        # Get the loudest frequencies
        #top_freqs = peak_freqs[:8]

        # Map peak frequencies to notes
        #peak_notes = [(freq_to_note_name(freq),int(mag),int(freq)) for freq, mag in top_freqs if freq_to_note_name(freq)]

        # Map peak frequencies to notes
        #peak_notes = [freq_to_note_name(freq) for freq in peak_freqs if freq_to_note_name(freq)]
        # Identify the most common notes (top 3 for simplicity)
        #note_counts = Counter(peak_notes)
        #common_notes = [note for note, count in note_counts.most_common(3)]

        # Identify chord from loudest notes
        #chord = identify_chord(peak_notes)

        #if chord is not "Unknown":
        if magnitude[peak_index] > 1000000 and peak_freq > 50:
            #10000 for stream

            #print(peak_notes)
            print(f"Detected Notes: {str(peak_notes):<85}, Peak Frequency: {peak_freq:7.2f} Hz") 

            plt.plot(fft_freq[:len(fft_freq)//2], magnitude[:len(magnitude)//2])
            plt.xlim(0,500)
            plt.ylim(0,10000000)
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Magnitude")
            plt.title("FFT of MP3 File: "+ audio_file +" from " + str(i * CHUNK)+" to "+str((i + 1) * CHUNK))
            plt.show()

        # if note is not prev_note and note > 0 and peak_index > 100:
            
        #     note_name = note_names[note]

        #     print(f"Peak Frequency: {peak_freq:.2f} Hz, Note: {note_name}, Magnitude: {peak_index}")

        #     prev_note = note

except KeyboardInterrupt:
    pass

print("Finished recording")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()
