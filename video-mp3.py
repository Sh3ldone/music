import streamlit as st
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os
import tempfile
import shutil
import base64

def video_to_mp3(video_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    output_path = "output.mp3"
    audio_clip.write_audiofile(output_path, codec="mp3")
    # Close the clips to release the file handles
    audio_clip.close()
    video_clip.close()
    return output_path

# Function to generate a download link
def get_binary_file_downloader_html(file_path, file_label):
    with open(file_path, 'rb') as file:
        data = file.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:audio/mp3;base64,{b64}" download="{file_label}.mp3" class="btn btn-success">Download {file_label}.mp3</a>'

# Streamlit UI with added styling
st.set_page_config(
    page_title="Video to MP3 Converter",
    page_icon="🎵",
    layout="centered",
)

# Custom CSS styles
custom_css = """
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        border: none;
    }
    .stFileUploader {
        padding: 16px;
        border: 2px dashed #aaaaaa;
        border-radius: 8px;
        text-align: center;
    }
    .stFileUploader>div {
        padding: 8px;
    }
"""

st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

st.title("Video to MP3 Converter")

# File uploader with style
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mkv"], key="file_uploader")

if uploaded_file is not None:
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Save the uploaded video file to the temporary directory
    video_path = os.path.join(temp_dir, uploaded_file.name)
    with open(video_path, "wb") as video_file:
        video_file.write(uploaded_file.read())

    # Display the video
    st.video(uploaded_file, format="video/mp4", start_time=0)

    # Convert button with style
    if st.button("Convert to MP3", key="convert_button"):
        try:
            # Convert video to mp3
            mp3_file_path = video_to_mp3(video_path)

            # Provide download link with style
            st.success("Conversion successful! Click below to download your MP3 file.")
            st.markdown(get_binary_file_downloader_html(mp3_file_path, 'Download'), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")

        finally:
            # Clean up: Close the clips and remove the temporary directory after processing
            shutil.rmtree(temp_dir, ignore_errors=True)


