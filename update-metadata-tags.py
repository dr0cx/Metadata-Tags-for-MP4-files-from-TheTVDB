from clear_tags import clear_tags
from get_episode_tags import get_episode_tags
from set_episode_tags import set_episode_tags

# Constants
# GET data from API
API_KEY = '1234567890' # your TheTVDB api key here
SHOW_ID = '12345'  # https://thetvdb.com/series/{SHOW}/  THETVDB.COM SERIES ID = "12345"
SHOW = 'SERIES NAME' # Series Name
SEASON_INT = 0          # Starting Season
SEASON_STR = '0'
SEASON_TOTAL = 2        # total number of seasons
SEASON_TOTAL += 1       # increment season total to work with for loop


# Loop over each season
for SEASON_INT in range(SEASON_INT, SEASON_TOTAL):
    SEASON_STR = f"{SEASON_INT:02d}"
    DIRECTORY = rf'F:\\PLEX\\SERIES\\{SHOW.replace(":", "")}\\Season {SEASON_STR}'
    clear_tags(DIRECTORY)

    # Endpoint URL for retrieving episode information
    EPISODES_ENDPOINT = f'https://api.thetvdb.com/series/{SHOW_ID}/episodes/query?airedSeason={SEASON_INT}'

    # Initialize an empty dictionary to store episode titles
    episode_titles = {}

    # get episode data
    episode_data = get_episode_tags(API_KEY, EPISODES_ENDPOINT, SHOW, episode_titles)


    # Assuming total_tracks represents the total number of episodes in the season
    total_tracks = len(episode_titles)

    # Iterate over each MP4 file in the directory
    # WRITE data to tag metadata
    set_episode_tags(DIRECTORY, episode_titles, SHOW, total_tracks, episode_data)
