# Stoic Quotes Video Generator
🎥 This Python script generates a video with a stoic quote overlay using Stoic Quotes API, text-to-speech conversion, and video editing capabilities. The resulting video includes a synchronized voiceover, subtitles, and background music.

### Prerequisites
To run this script, you need to have the following dependencies installed:

- moviepy 
- requests
- srt 
#### You can install these dependencies using pip:
```pip install moviepy requests srt```
#### Usage
1.Clone the repository:
```git clone https://github.com/your-username/your-repo.git```

2.Navigate to the project directory:
```cd your-repo```

3.Replace the placeholder values in the code:
- API.Api_Key with your API key for the Eleven Labs Text-to-Speech API.
- API.DEEPGRAM_API_KEY with your API key for the Deepgram API.

4.Run the script:
```python main.py```

5.Wait for the script to generate the video. The final video will be saved as output/final_clip.mp4.

## Acknowledgements
This script utilizes the following APIs and libraries:

- Stoic Quotes API (https://stoic-quotes.com/api) - Provides stoic quotes for the video overlay.
- Eleven Labs Text-to-Speech API (https://api.elevenlabs.io/v1/text-to-speech) - Converts the quote text to voice.
- Deepgram API (https://api.deepgram.com/v1/listen) - Generates word-level timestamps for the subtitle overlay.
- moviepy - Python library for video editing and manipulation.
- requests - Python library for making HTTP requests.
- srt - Python library for parsing and generating SubRip subtitle files.

## Credits
This project was created by Abdirahman and inspired by the stoic philosophy. Contributions, suggestions, and bug reports are welcome! 😊

📝 Note: The video materials used in this script are not included in the repository. Make sure to replace materials/Footage.mp4 and materials/Music.mp3 with your desired video and audio files.

Enjoy creating your own stoic quote videos! 🎬
