from get_show_data import get_show_data
from clear_tags import clear_tags
from get_episode_tags import get_episode_tags
from set_episode_tags import set_episode_tags

# Constants
# GET data from API
API_KEY = '1234567890' # your TheTVDB api key here
SHOW_ID = '12345'  # Manually enter from https://thetvdb.com/series/{SHOW}/  THETVDB.COM SERIES ID = "12345"

# Initialize an empty dictionary to store episode titles
episode_titles = {}

# Initialize an empty dictionary to store series name and seasons
show_data = {}

get_show_data(API_KEY, SHOW_ID, show_data)

# Retrieve series name from show_data
SHOW = show_data[SHOW_ID]["name"]

# Assume there is a season 0.
# If no season 0 exists in TheTVDB or if no season 0 exists in user Directory,
# The For loop will continue to the next iteration
SEASON_INT = 0

# Retrieve the total number of seasons (SEASON_TOTAL) from show_data
SEASON_TOTAL = show_data[SHOW_ID]["total_seasons"]

# Loop over each season
for SEASON_INT in range(SEASON_INT, SEASON_TOTAL + 1):
    SEASON_STR = f"{SEASON_INT:02d}"

    try:
        DIRECTORY = rf'Z:\\DIRECTORY\\SUBDIRECTORY\\{SHOW.replace(":", "")}\\Season {SEASON_STR}'
        clear_tags(DIRECTORY)

        # Endpoint URL for retrieving episode information
        EPISODES_ENDPOINT = f'https://api.thetvdb.com/series/{SHOW_ID}/episodes/query?airedSeason={SEASON_INT}'

        # get episode data
        episode_data = get_episode_tags(API_KEY, EPISODES_ENDPOINT, SHOW, episode_titles)

        # Assuming total_tracks represents the total number of episodes in the season
        total_tracks = len(episode_titles)

        # Iterate over each MP4 file in the directory
        # WRITE data to tag metadata
        set_episode_tags(DIRECTORY, episode_data, SHOW, total_tracks)

    except FileNotFoundError:
        print(f"Season {SEASON_INT} not found for {SHOW}. Skipping...")
        continue
