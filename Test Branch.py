from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, CompositeAudioClip
import requests
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import conf

def create_subtitles(quote, video_duration, subtitle_duration):
    subtitle_segments = []
    start_time = 0

    while start_time < video_duration:
        end_time = min(start_time + subtitle_duration, video_duration)
        subtitle_text = quote[start_time:end_time]
        subtitle_segment = f"{start_time:.3f} --> {end_time:.3f}\n{subtitle_text}\n\n"
        subtitle_segments.append(subtitle_segment)
        start_time += subtitle_duration

    return ''.join(subtitle_segments)


# Fetch quote and author from API
response = requests.get("https://stoic-quotes.com/api/quote").json()
quote, author = response["text"], response["author"]

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"

headers = {
  "Accept": "audio/mp3",
  "Content-Type": "application/json",
  "xi-api-key": conf.API_KEY
}

data = {
  "text": quote,
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)
with open('Voice.mp3', 'wb') as f:
    f.write(response.content)

# Load video and music
voice_audio = AudioSegment.from_file("Voice.mp3")
voice_duration = voice_audio.duration_seconds + 1
clip = VideoFileClip("materials/Footage.mp4").subclip(0, voice_duration)
audio = AudioSegment.from_file("materials/Music.mp3").subclip(0, voice_duration)
lowered_audio = audio - 20  # Adjust the volume level as needed

# Trim video, music, and voice clips to match the length of the voice file
new_audio = CompositeAudioClip([lowered_audio, voice_audio])
clip = clip.set_audio(new_audio)

# Convert audio to WAV format
voice_audio.export("Voice.wav", format="wav")

# Transcribe the voice audio to text
recognizer = sr.Recognizer()
with sr.AudioFile("Voice.wav") as source:
    audio = recognizer.record(source)
text = recognizer.recognize_google(audio)

# Generate the SRT content for each segment
segments = split_on_silence(voice_audio, min_silence_len=500, silence_thresh=-40)
start_index = 1
start_time = 0
srt_string = ""

# Save segments as temporary files
audio_paths = []
for i, segment in enumerate(segments):
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    segment.export(temp_file.name, format="wav")
    audio_paths.append(temp_file.name)

    end_time = start_time + len(segment) / 1000.0
    start_time_str = format(start_time, ".3f").replace(".", ",")
    end_time_str = format(end_time, ".3f").replace(".", ",")
    srt_entry = f"{start_index}\n{start_time_str} --> {end_time_str}\n{text}\n\n"
    srt_string += srt_entry
    start_index += 1
    start_time = end_time

# Save the SRT string to a file
srt_path = "subtitles.srt"
with open(srt_path, "w") as f:
    f.write(srt_string)
print("Subtitles SRT file saved:", srt_path)

# Read the contents of the SRT file
with open(srt_path, "r") as f:
    subtitles = f.read()

# Determine font size based on the length of the quote
quote_length = len(quote)
fontsize = max(90 - int(quote_length / 5), 10)  # Adjust the values to your preference
print(f"Font size: {fontsize}")
print(f"Quote length: {quote_length}")

# Split the quote into multiple lines
quote_lines = []
current_line = ""
words = quote.split(" ")
for word in words:
    if len(current_line + " " + word) <= 20:  # Adjust the value to your preference
        current_line += " " + word
    else:
        quote_lines.append(current_line.strip())
        current_line = word
quote_lines.append(current_line.strip())

# Create a TextClip for each line of the quote
quote_clips = []
for i, line in enumerate(quote_lines):
    text_clip = TextClip(
        line,
        fontsize=fontsize,
        font="Arial",
        color="white",
        stroke_width=1,
        stroke_color="black",
        method="caption",
        align="center",
        size=clip.size,
    ).set_duration(voice_duration).set_start(0)
    quote_clips.append(text_clip)

# Create a video clip with the subtitles
subtitle_duration = 1  # 1 second per subtitle
video_duration = voice_duration  # Duration of the video matches the voice audio clip

subtitles_clip = TextClip(
    subtitles,
    fontsize=fontsize,
    font="Arial",
    color="white",
    stroke_width=1,
    stroke_color="black",
    method="caption",
    align="center",
    size=clip.size,
).set_duration(voice_duration).set_start(0)

# Overlay the quote clips and subtitles on the video clip
video_with_quotes = CompositeVideoClip([clip] + quote_clips + [subtitles_clip])

# Set the audio of the video with quotes to the combined audio
video_with_quotes = video_with_quotes.set_audio(new_audio)

# Export the final video with quotes
video_with_quotes.write_videofile("output/video_with_quotes.mp4", codec="libx264", audio_codec="aac", fps=clip.fps)
