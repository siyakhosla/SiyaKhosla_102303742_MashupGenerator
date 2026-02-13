from pydub import AudioSegment

AudioSegment.converter = "ffmpeg"
AudioSegment.ffprobe   = "ffprobe"
import streamlit as st
import os
from yt_dlp import YoutubeDL
from pydub import AudioSegment

st.title("🎵 Mashup Generator")

singer = st.text_input("Singer Name")
num = st.number_input("Number of Videos", min_value=1, step=1)
duration = st.number_input("Duration (seconds)", min_value=5, step=1)
filename = st.text_input("Output File Name", value="mashup.mp3")

if st.button("Generate Mashup"):

    os.makedirs("downloads", exist_ok=True)

    opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }

    search = f"ytsearch{num}:{singer}"

    with YoutubeDL(opts) as ydl:
        ydl.download([search])

    final = AudioSegment.empty()

    for file in os.listdir("downloads"):
        audio = AudioSegment.from_file("downloads/" + file)
        final += audio[:duration * 1000]

    final.export(filename, format="mp3")

    st.success("Mashup created successfully!")

    with open(filename, "rb") as f:
        st.download_button(
            label="Download Mashup",
            data=f,
            file_name=filename,
            mime="audio/mpeg"
        )
