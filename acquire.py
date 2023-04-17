import dwfpy as dwf

import struct
import pyaudio

# Set up the PyAudio object
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=40000,
                output=True)

with dwf.Device() as device:
    scope = device.analog_input
    scope[0].setup(range=5.0)
    while True:
        try:
            scope.single(sample_rate=40000, buffer_size=8192, configure=True, start=True)
            samples = scope[0].get_data()

            # Define the array of audio samples
            n_samples = len(samples)

            # Convert the samples to bytes and play the audio
            chunk = struct.pack('f' * len(samples), *samples)
            stream.write(chunk)
        except:
            break

    # Close the PyAudio object
    stream.stop_stream()
    stream.close()
    p.terminate()
