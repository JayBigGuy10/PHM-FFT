import pyaudio
import numpy as np
import pyfftw

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

        # Find the peak frequency
        peak_index = np.argmax(magnitude)
        peak_freq = abs(fft_freq[peak_index])

        # Convert peak frequency to musical note (simplified)
        A4 = 440.0  # Frequency of A4
        C0 = A4 * np.power(2, -4.75)
        note_num = 12 * np.log2(peak_freq / C0)

        try:
            note = int(round(note_num)) % 12
        except:
            note = 0

        if note is not prev_note and note > 0 and peak_index > 100:
            note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            note_name = note_names[note]

            print(f"Peak Frequency: {peak_freq:.2f} Hz, Note: {note_name}, Magnitude: {peak_index}")

            prev_note = note

except KeyboardInterrupt:
    pass

print("Finished recording")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()
