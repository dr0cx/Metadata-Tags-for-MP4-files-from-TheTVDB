import requests
import os
import re
from mutagen.mp4 import MP4

# GET data from API
API_KEY = '1234567890' # your TheTVDB api key here
SHOW_ID = '12345'  # https://thetvdb.com/series/{SHOW}/  THETVDB.COM SERIES ID = "12345"
SHOW = 'SERIES NAME' # Series Name
SEASON = '5' # Season Number
 #I need to format SEASON to handle single digits and double digits

# Endpoint URL for retrieving episode information
EPISODES_ENDPOINT = f'https://api.thetvdb.com/series/{SHOW_ID}/episodes/query?airedSeason={SEASON}'

# Set headers with API key for authentication
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json'
}

# Make GET request to retrieve episode information
response = requests.get(EPISODES_ENDPOINT, headers=headers)

# Parse JSON response
episode_data = response.json()

# Check if request was successful
if response.status_code == 200:

    if 'data' in episode_data:
        # Initialize an empty dictionary to store episode titles
        episode_titles = {}

        # Extract episode titles and numbers from the API response
        for episode in episode_data['data']:
            episode_number = f"{SHOW.replace(':','')} - S{episode['airedSeason']:02d}E{episode['airedEpisodeNumber']:02d}"
            episode_titles[episode_number] = episode.get('episodeName', 'Unknown Title')

        print("Episode titles loaded successfully.")
    else:
        print("No episode data found in API response.")
else:
    print('Error:', response.status_code)

# WRITE metadata
 #I need to format SEASON to handle single digits and double digits
DIRECTORY = rf'Z:\\DIRECTORY\\SUBDIRECTORY\\{SHOW.replace(":", "")}\\Season 0{SEASON}'

# Iterate over each MP4 file in the directory
for filename in os.listdir(DIRECTORY):
    if filename.endswith(".mp4"):
        # Extract episode number from the filename
        match = re.search(r'S(\d+)E(\d+)', filename)

        if match:
            season_number = match.group(1)
            episode_number = match.group(2)
            episode_key = f"{SHOW.replace(':','')} - S{season_number}E{episode_number}"

            # Check if the episode key exists in the episode_titles dictionary
            if episode_key in episode_titles:
                episode_title = episode_titles[episode_key]

                # Path to the MP4 file
                mp4_file_path = os.path.join(DIRECTORY, filename)

                # Open the MP4 file for editing
                mp4 = MP4(mp4_file_path)

                # Update metadata tag with matched title
                mp4['\xa9nam'] = episode_title  # SET TITLE
                mp4['\xa9ART'] = SHOW  # SET ARTIST

                # Save the changes
                mp4.save()

                print(f"Updated metadata for {filename} with title: {episode_title}")
            else:
                print(f"No title found for episode {episode_key} in the episode_titles dictionary")
        else:
            print(f"Unable to extract episode number from filename: {filename}")
