import pyaudio
import numpy as np
import pyfftw
from collections import Counter

# Parameters
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate (44.1 kHz)
CHUNK = 1024  # Size of audio chunks to read

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open a stream with the desired parameters
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

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
    while True:
        # Read a chunk of audio data
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)

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
        threshold = np.max(magnitude) * 0.1
        significant_indices = np.where(magnitude > threshold)[0]

        # Find peak frequencies
        peak_freqs = [abs(fft_freq[i]) for i in significant_indices]

        # Map peak frequencies to notes
        peak_notes = [freq_to_note_name(freq) for freq in peak_freqs if freq_to_note_name(freq)]
        #print(peak_notes)

        # Identify the most common notes (top 3 for simplicity)
        note_counts = Counter(peak_notes)
        common_notes = [note for note, count in note_counts.most_common(3)]

        # Identify chord from common notes
        chord = identify_chord(common_notes)

        #if chord is not "Unknown":
        if magnitude[peak_index] > 10000 and peak_freq > 50:
            print(f"Detected Notes: {str(common_notes):<20}, Chord: {chord}, Peak Frequency: {peak_freq:10.2f} Hz, Magnitude: {magnitude[peak_index]:.2f}") 

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
