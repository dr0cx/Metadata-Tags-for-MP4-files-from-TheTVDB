import os
from mutagen.mp4 import MP4

def clear_tags(directory):
    """
    Clear all metadata tags for each MP4 file in the specified directory.

    Args:
        directory (str): The directory containing MP4 files.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            try:
                # Open the MP4 file for editing
                mp4_file_path = os.path.join(directory, filename)
                mp4 = MP4(mp4_file_path)

                # Delete all metadata tags
                mp4.delete()

                # Save the changes
                mp4.save()
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
    print(f"Cleared all metadata tags for {directory}")
