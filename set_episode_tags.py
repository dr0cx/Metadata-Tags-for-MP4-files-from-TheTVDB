import os
import re
from mutagen.mp4 import MP4

def set_episode_tags(DIRECTORY, episode_data, SHOW, total_tracks):
    """
    Set episode metadata tags for MP4 files in the given directory.

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
                album = f"S{disc:02}E"

                # Check if the episode key exists in the episode_data dictionary
                if episode_key in episode_data:
                    episode_info = episode_data[episode_key]
                    episode_title = episode_info['title']
                    episode_year = episode_info['year']

                    # Path to the MP4 file
                    mp4_file_path = os.path.join(DIRECTORY, filename)

                    # Open the MP4 file for editing
                    mp4 = MP4(mp4_file_path)

                    # Update metadata tag with matched title
                    mp4['\xa9nam'] = episode_title.lstrip()  # Assuming '\xa9nam' is the title tag
                    mp4['\xa9ART'] = SHOW  # Set artist
                    mp4['\xa9day'] = episode_year  # Year
                    mp4["trkn"] = [(track, total_tracks)]  # Set track number and total tracks as a tuple
                    mp4["disk"] = [(disc, 1)]   # Set disc number
                    mp4['\xa9alb'] = album

                    # Save the changes
                    mp4.save()

                    print(f"Updated metadata for {filename} with artist: {SHOW}, disk: {disc}, track: {track}, album: {album}, year: {episode_year}, title: {episode_title}")
                else:
                    print(f"No title found for episode {episode_key} in the episode_titles dictionary")
            else:
                print(f"Unable to extract episode number from filename: {filename}")
        else:
            print(f"Not configured to work with this file extension at this time: {filename}")
            continue
