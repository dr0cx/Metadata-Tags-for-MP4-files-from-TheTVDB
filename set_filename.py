import os
import re
from mutagen.mp4 import MP4

def set_filename(DIRECTORY, episode_data, SHOW, total_tracks):
    """
    Set filename to format SHOW - SxxExx.mp4

    Args:
    - DIRECTORY: The directory containing the MP4 files.
    - SHOW: The name of the TV show.
    - total_tracks: Total number of tracks in the season.
    - episode_data: Dictionary containing episode data retrieved from the API.
    """

    # Iterate over each MP4 file in the directory
    for filename in os.listdir(DIRECTORY):
        if filename.endswith(".mp4"):
            # Extract episode number from the filename
            match = re.search(r'S(\d+)E(\d+)', filename.upper())
            if match:
                season_number = match.group(1)
                episode_number = match.group(2)
                episode_key = f"{SHOW.replace(':','')} - S{season_number}E{episode_number}"

                track = int(episode_number)
                disc = int(season_number)

                # Path to the MP4 file
                mp4_file_path = os.path.join(DIRECTORY, filename)

                # Construct new filename
                new_filename = f"{SHOW.replace(':','')} - S{disc:02}E{track:02}.mp4"

                # Rename the file
                os.rename(mp4_file_path, os.path.join(DIRECTORY, new_filename))

                print(f"Renamed {filename} to {new_filename}")

            else:
                print(f"No title found for episode {episode_key} in the episode_titles dictionary")
        else:
            print(f"Not configured to work with this file extension at this time: {filename}")
            continue
