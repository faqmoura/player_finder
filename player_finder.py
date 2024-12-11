import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import re
from urllib.parse import parse_qs, urlparse

def get_video_duration(video_id):
    try:
        # Using oEmbed to get video information without API key
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(oembed_url)
        response.raise_for_status()
        return response.json()['duration']
    except Exception as e:
        st.error(f"Error fetching video duration: {str(e)}")
        return None

def get_transcript_with_timestamps(video_id, language='en'):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript([language])
        return transcript.fetch()
    except Exception as e:
        st.error(f"Error fetching transcript: {str(e)}")
        return None

def extract_video_id(url):
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1]
    elif "youtube.com" in url:
        parsed_url = urlparse(url)
        return parse_qs(parsed_url.query)['v'][0]
    return url

def find_player_mentions(transcript_data, player_name):
    mentions = []
    if not player_name.strip():
        return mentions
    
    pattern = re.compile(player_name, re.IGNORECASE)
    
    for entry in transcript_data:
        if pattern.search(entry['text']):
            mentions.append({
                'text': entry['text'],
                'start': entry['start'],
                'duration': entry['duration']
            })
    
    return mentions

st.title("Soccer Player Mention Finder")

# Input fields
video_url = st.text_input("Enter YouTube Video URL")
player_name = st.text_input("Enter Player Name")
selected_language = st.selectbox(
    "Select Commentary Language",
    ['en', 'es', 'pt', 'fr', 'de', 'it']
)

if st.button("Find Player Mentions"):
    if video_url and player_name:
        video_id = extract_video_id(video_url)
        transcript_data = get_transcript_with_timestamps(video_id, selected_language)
        
        if transcript_data:
            mentions = find_player_mentions(transcript_data, player_name)
            
            if mentions:
                st.success(f"Found {len(mentions)} mentions of {player_name}")
                
                for idx, mention in enumerate(mentions, 1):
                    minutes = int(mention['start'] // 60)
                    seconds = int(mention['start'] % 60)
                    
                    st.markdown(f"""
                    **Mention {idx}**
                    - Time: {minutes}:{seconds:02d}
                    - Context: "{mention['text']}"
                    """)
            else:
                st.warning(f"No mentions of {player_name} found in the transcript")
    else:
        st.error("Please enter both a video URL and player name")