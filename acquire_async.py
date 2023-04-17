import dwfpy as dwf
import struct
import pyaudio
import threading
import queue

# Set up the PyAudio object
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=40000,
                output=True,
                stream_callback=None)

# Set up the analog input device and buffer
with dwf.Device() as device:
    scope = device.analog_input
    scope[0].setup(range=5.0)

    # Set up the audio buffer and thread
    audio_buffer = queue.Queue(maxsize=10)
    stop_event = threading.Event()

    def audio_thread():
        while not stop_event.is_set():
            try:
                scope.single(sample_rate=40000, buffer_size=8192, configure=True, start=True)
                samples = scope[0].get_data()
                audio_buffer.put(samples)
            except:
                break

    audio_writer_running = False

    def audio_writer():
        global audio_writer_running
        while not stop_event.is_set():
            try:
                samples = audio_buffer.get(timeout=0.1)
                chunk = struct.pack('f' * len(samples), *samples)
                stream.write(chunk)
            except queue.Empty:
                pass
            except:
                break
        audio_writer_running = False

    def start_audio_writer():
        global audio_writer_running
        if not audio_writer_running:
            audio_writer_running = True
            threading.Thread(target=audio_writer, daemon=True).start()

    # Start the audio thread and writer
    threading.Thread(target=audio_thread, daemon=True).start()
    stream.start_stream()

    while True:
        start_audio_writer()
        if stop_event.wait(timeout=0.1):
            break

# Stop the audio stream and close the PyAudio object
stream.stop_stream()
stream.close()
p.terminate()
