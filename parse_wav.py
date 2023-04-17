import wave

# Open the WAV file
with wave.open('example.wav', 'rb') as wav_file:
    # Get the number of audio channels
    num_channels = wav_file.getnchannels()

    # Get the sample rate of the audio
    sample_rate = wav_file.getframerate()

    # Get the number of audio frames
    num_frames = wav_file.getnframes()

    # Read the audio data from the file into a bytes object
    raw_audio_data = wav_file.readframes(num_frames)

    # Convert the bytes object to a list of integer samples
    samples = list(wave.struct.unpack(f"{num_frames * num_channels}h", raw_audio_data))

# Print out the extracted values
print(f"Number of channels: {num_channels}")
print(f"Sample rate: {sample_rate}")
print(f"Number of frames: {num_frames}")
print(f"Samples: {samples}")
