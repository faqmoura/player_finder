# Soccer Player Mention Finder

A simple Streamlit application that allows users to find mentions of soccer players in YouTube video transcripts. The app retrieves the transcript of a specified video and searches for the player's name, providing the estimated timestamps of their mentions in the video.

## Features

- Retrieve YouTube video transcripts with timestamps.
- Search for player names in the transcript.
- Display the estimated time (minutes:seconds) when the player is mentioned.
- Supports multiple commentary languages.

## Requirements

To run this application, you need the following Python packages:

- `streamlit`
- `youtube-transcript-api`
- `requests`

You can install these dependencies using pip:

```bash
pip install -r requirements.txt
