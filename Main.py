from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, CompositeAudioClip, AudioFileClip
import requests
import conf

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
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
# Load video and music
Voice = AudioFileClip("Voice.mp3")
voice_duration = Voice.duration + 1 
clip = VideoFileClip("materials/Footage.mp4").subclip(0, voice_duration)
audio = AudioFileClip("materials/Music.mp3").subclip(0, voice_duration)
lowered_audio = audio.volumex(0.3)
# Trim video, music, and voice clips to match the length of the voice file
new_audio = CompositeAudioClip([lowered_audio, Voice])
clip.audio = new_audio
#Generate the voice Over


# Define the duration of the text overlay
overlay_duration = voice_duration

# Define the start and end times for the text overlay
overlay_start = 0
overlay_end = overlay_start + overlay_duration

# Create a text clip with the desired text


# Determine font size based on the length of the quote
quote_length = len(quote)
fontsize = max(90 - int(quote_length / 5), 10)  # Adjust the values to your preference
print(f"Font size: {fontsize}")
print(f"Quote length: {quote_length}")

# Split the quote into multiple lines with a minimum of 4 words per line
words = quote.split()
lines = []
line = ""
for word in words:
    if len(line) + 1 <= 17:
        line += word + " "
    else:
        lines.append(line.strip())
        line = word + " "
if line:
    lines.append(line.strip())
quote_multiline = "\n".join(lines)

text = TextClip(quote_multiline, fontsize=fontsize, color='white', align='center').set_duration(overlay_duration)

# Calculate the position to center the text
text_x = int((clip.w - text.w) / 2)
text_y = int(clip.h / 3 - text.h / 2)  # Adjust the y-coordinate to the top 2/3 of the frame
text = text.set_position((text_x, text_y))

# Render and save the final video with the text overlay
final = CompositeVideoClip([clip, text.set_start(overlay_start).set_end(overlay_end)])
final.write_videofile("materials/final_clip.mp4")