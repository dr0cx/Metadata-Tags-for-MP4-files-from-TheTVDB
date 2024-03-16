import os
from mutagen.mp4 import MP4

def clear_tags(directory):
    """
    Clear metadata tags for each MP4 file in the specified directory.

    Args:
        directory (str): The directory containing MP4 files.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            # Open the MP4 file for editing
            mp4_file_path = os.path.join(directory, filename)
            mp4 = MP4(mp4_file_path)

            # Clear metadata tags
            mp4['\xa9nam'] = ''
            mp4['\xa9ART'] = ''
            mp4['\xa9day'] = ''
            mp4["trkn"] = []
            mp4["disk"] = []

            # Save the changes
            mp4.save()

            print(f"Cleared metadata tags for {filename}")