import requests
import os
import re
from mutagen.mp4 import MP4

# GET data from API
API_KEY = '1234567890' # your TheTVDB api key here
SHOW_ID = '12345'  # https://thetvdb.com/series/{SHOW}/  THETVDB.COM SERIES ID = "12345"
SHOW = 'SERIES NAME' # Series Name
SEASON_INT = 5
SEASON_STR = '0' # Current Season

if SEASON_INT < 10:
    SEASON_STR = f"0{SEASON_INT}"
else:
    SEASON_STR = f"{SEASON_INT}"

# Endpoint URL for retrieving episode information
EPISODES_ENDPOINT = f'https://api.thetvdb.com/series/{SHOW_ID}/episodes/query?airedSeason={SEASON_INT}'

# Set headers with API key for authentication
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json'
}

# Make GET request to retrieve episode information
response = requests.get(EPISODES_ENDPOINT, headers=headers)

# Parse JSON response
episode_data = response.json()
print(episode_data)
# Check if request was successful
if response.status_code == 200:
    # Parse JSON response
    if 'data' in episode_data:
        # Initialize an empty dictionary to store episode titles
        episode_titles = {}
        # Extract episode titles and numbers from the API response
        for episode in episode_data['data']:
            episode_number = f"{SHOW.replace(':','')} - S{episode['airedSeason']:02d}E{episode['airedEpisodeNumber']:02d}"
            episode_title = episode.get('episodeName', 'Unknown Title')
            episode_aired = episode.get('firstAired', 'Unknown Date')
            episode_year = episode_aired.split('-')[0]
            episode_titles[episode_number] = {'title': episode_title, 'year': episode_year}

        print("Episode titles loaded successfully.")
        print(episode_titles)

    else:
        print("No episode data found in API response.")
else:
    print('Error:', response.status_code)

# WRITE metadata
# Enter YOUR directory path
DIRECTORY = rf'Z:\\DIRECTORY\\SUBDIRECTORY\\{SHOW.replace(":", "")}\\Season {SEASON_STR}'

# Assuming total_tracks represents the total number of episodes in the season
total_tracks = len(episode_titles)

# Iterate over each MP4 file in the directory
for filename in os.listdir(DIRECTORY):
    if filename.endswith(".mp4"):
        # Extract episode number from the filename
        match = re.search(r'S(\d+)E(\d+)', filename)
        if match:
            season_number = match.group(1)
            episode_number = match.group(2)
            episode_key = f"{SHOW.replace(':','')} - S{season_number}E{episode_number}"

            track = int(episode_number)
            disc = int(season_number)
            # Check if the episode key exists in the episode_titles dictionary
            if episode_key in episode_titles:
                episode_info = episode_titles[episode_key]
                episode_title = episode_info['title']
                episode_year = episode_info['year']

                # Path to the MP4 file
                mp4_file_path = os.path.join(DIRECTORY, filename)

                # Open the MP4 file for editing
                mp4 = MP4(mp4_file_path)

                # Update metadata tag with matched title
                mp4['\xa9nam'] = episode_title  # Assuming '\xa9nam' is the title tag
                mp4['\xa9ART'] = SHOW  # Set artist
                mp4['\xa9day'] = episode_year  # Year
                mp4["trkn"] = [(track, total_tracks)]  # Set track number and total tracks as a tuple
                mp4["disk"] = [(disc, 1)]   # Set disc number

                # Save the changes
                mp4.save()

                print(f"Updated metadata for {filename} with artist: {SHOW}, disk: {disc}, track: {track}, year: {episode_year}, title: {episode_title}")
            else:
                print(f"No title found for episode {episode_key} in the episode_titles dictionary")
        else:
            print(f"Unable to extract episode number from filename: {filename}")
