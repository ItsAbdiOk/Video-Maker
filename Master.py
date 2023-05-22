from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, CompositeAudioClip, AudioFileClip
import requests
import srt
import API

def get_stoic_quote():
    response = requests.get("https://stoic-quotes.com/api/quote").json()
    quote, author = response["text"], response["author"]
    return quote, author

def generate_voice_file(quote):
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
    headers = {
        "Accept": "audio/mp3",
        "Content-Type": "application/json",
        "xi-api-key": API.Api_Key
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

def generate_video_with_text_overlay(quote):
    # Load video and music
    Voice = AudioFileClip("Voice.mp3")
    voice_duration = Voice.duration + 1 
    clip = VideoFileClip("materials/Footage.mp4").subclip(0, voice_duration)
    audio = AudioFileClip("materials/Music.mp3").subclip(0, voice_duration)
    lowered_audio = audio.volumex(0.3)

    # Trim video, music, and voice clips to match the length of the voice file
    new_audio = CompositeAudioClip([lowered_audio, Voice])
    clip.audio = new_audio

    # Read the SRT file and extract subtitle timings and text
    subtitles = []
    with open('output.srt', 'r') as f:
        subtitle_generator = srt.parse(f.read())
        for subtitle in subtitle_generator:
            start_time = subtitle.start.total_seconds()
            end_time = subtitle.end.total_seconds()
            text = subtitle.content
            subtitles.append((start_time, end_time, text))

    # Create text clips for each subtitle and position them at the center
    text_clips = []
    for subtitle in subtitles:
        start_time, end_time, text = subtitle
        duration = end_time - start_time
        fontsize = calculate_fontsize(text)
        text_clip = TextClip(text, fontsize=fontsize, color='white', align='center').set_duration(duration)
        text_clip = text_clip.set_position('center')
        text_clip = text_clip.set_start(start_time).set_end(end_time)
        text_clips.append(text_clip)

    # Overlay the text clips onto the video
    final = CompositeVideoClip([clip] + text_clips)
    final.write_videofile("output/final_clip.mp4")

def calculate_fontsize(text):
    quote_length = len(text)
    fontsize = max(90 - int(quote_length / 5), 10)  # Adjust the values to your preference
    return fontsize

def generate_SRT_file():
    url = "https://api.deepgram.com/v1/listen?tier=nova&version=latest&language=en&detect_language=false&punctuate=true&profanity_filter=false"
    payload = open('Voice.mp3', 'rb').read()
    headers = {
        "accept": "audio/mp3",
        "content-type": "audio/mp3",
        "Authorization": API.DEEPGRAM_API_KEY
    }
    response = requests.post(url, data=payload, headers=headers)
    data = response.json()
    # Extract word-level information from the response
    words = data['results']['channels'][0]['alternatives'][0]['words']
    # Create the SRT file content with word-level timestamps
    srt_content = ""
    for i, word in enumerate(words):
        start_timestamp = format_timestamp(word['start'])
        end_timestamp = format_timestamp(word['end'])
        word_text = word['punctuated_word']
        srt_content += "{}\n{} --> {}\n{}\n\n".format(i+1, start_timestamp, end_timestamp, word_text)
    # Save the SRT content to a file
    with open('output.srt', 'w') as f:
        f.write(srt_content)

    print("SRT file generated successfully.")
# Helper function to format timestamps in HH:MM:SS,mmm format
def format_timestamp(timestamp):
    hours = int(timestamp / 3600)
    minutes = int((timestamp % 3600) / 60)
    seconds = int(timestamp % 60)
    milliseconds = int((timestamp % 1) * 1000)
    return "{:02d}:{:02d}:{:02d},{:03d}".format(hours, minutes, seconds, milliseconds)

# Main program
quote, author = get_stoic_quote()
generate_voice_file(quote)
generate_SRT_file()
generate_video_with_text_overlay(quote)
