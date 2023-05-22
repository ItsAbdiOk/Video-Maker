from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, CompositeAudioClip, AudioFileClip
import requests

def load_video_and_music(video_file_path, audio_file_path):
    clip = VideoFileClip(video_file_path).subclip(0, 10)
    audio = AudioFileClip(audio_file_path).subclip(0, 10)
    new_audio = CompositeAudioClip([audio])
    clip.audio = new_audio
    return clip

def create_text_overlay(duration):
    response = requests.get("https://stoic-quotes.com/api/quote").json()
    quote, author = response["text"], response["author"]
    max_chars_per_line = 30  # Maximum characters per line
    lines = [quote[i:i+max_chars_per_line] for i in range(0, len(quote), max_chars_per_line)]
    quote_multiline = "\n".join(lines)
    fontsize = calculate_font_size(quote)
    text = TextClip(quote_multiline, fontsize=fontsize, color='white', align='center', method='caption', interline=fontsize).set_duration(duration)
    return text



def calculate_font_size(quote):
    quote_length = len(quote)
    fontsize = max(90 - int(quote_length / 5), 10)
    return fontsize

def calculate_text_position(clip, text):
    text_x = int((clip.w - text.w) / 2)
    text_y = int(clip.h / 3 - text.h / 2)  # Adjust the y-coordinate to the top 2/3 of the frame
    text = text.set_position((text_x, text_y))
    return text

def render_and_save_video(clip, text, overlay_start, overlay_end, output_file):
    final = CompositeVideoClip([clip, text.set_start(overlay_start).set_end(overlay_end)])
    final.write_videofile(output_file)

# Usage example:
video_file_path = "materials/Footage.mp4"
output_file_path = "materials/final_clip.mp4"
audio_file_path = "materials/Music.mp3"
overlay_duration = 8
overlay_start = 1
overlay_end = overlay_start + overlay_duration

clip = load_video_and_music(video_file_path, audio_file_path)
text_overlay = create_text_overlay(overlay_duration)
text_with_position = calculate_text_position(clip, text_overlay)
render_and_save_video(clip, text_with_position, overlay_start, overlay_end, output_file_path)
