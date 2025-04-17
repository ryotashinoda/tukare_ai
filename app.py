# app.py
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import librosa
import soundfile as sf
import numpy as np
import pandas as pd
import io

st.set_page_config(page_title="🎙 疲労チェックAI", layout="centered")
st.title("🎙 声で疲労チェックAI")

# UI for recording audio
audio_bytes = audio_recorder(
    sample_rate=44100,
    text="Click to record",
    recording_color="#e8662c",
    neutral_color="#6aa36f",
    icon_name="microphone",
    icon_size=50,
)

# Display the recorded audio
if audio_bytes:
    st.success("録音完了！")

    st.audio(audio_bytes, format="audio/wav")

    # convert bytes to numpy array
    audio_buffer = io.BytesIO(audio_bytes)
    y, sr = sf.read(audio_buffer, dtype='float32')
    if (y.ndim > 1):
        y = y[:, 0]

    st.write(f"サンプルレート: {sr} Hz")
    st.write(f"録音時間: {len(y) / sr:.2f} 秒")

    # Plot the waveform
    step = 100
    x_sec = np.arange(0, len(y), step) / sr
    y_down = y[::step]
    
    df = pd.DataFrame({"Time(s)": x_sec, "Amplitude": y_down})  
    st.line_chart(df.set_index("Time(s)"))

else:
    st.info("録音してみましょう！")