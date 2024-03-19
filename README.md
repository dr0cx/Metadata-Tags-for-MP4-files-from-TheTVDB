# Metadata Tags for MP4 files from TheTVDB
 python script to populate Title and Artist metadata tags in MP4 files

# Constraints
- Currently this is designed when shows follow the standard Plex directory and naming conventions
    - DIRECTORY FOR TV SHOWS
        - SUBDIRECTORY Named "Actual Show Name" (where the name is identical as listed on TheTVDB)
            - SUBDIRECTORY NAMED "Season xx" (where the xx is a number, with 00 being the season for Specials)
                - MP4 files where file is named "Actual Show Name - SxxExx.mp4"

# How to use
- Place files in some directory on your machine
- Line 33 of update_metadata_tags.py, enter the correct path to your series directory
- Navigate to TheTVDB:
    - Create an account
    - At the bottom of the page in the About section, click the link for API
    - Click the "Get Started" button
    - Enter Personal use in all three text fields
    - Get your API key
    - Copy API key value and paste it into update_metadata_tags.py line 8, API_KEY
- search TheTVDB for the series you want
    - Click on the series name
    - Find the numeric id on the table row "TheTVDB.com Series ID"
    - Copy the numeric value and paste it into update_metadata_tags.py line 9, SHOW_ID
- Use VS Code Terminal, type
    - python update_metadata_tags.py

# Potential future updates to reduce manual intervention
- Read directory to load list of show names into a dictonary series_directory { "show_name": {series folder name}, "show_id": {placeholder for function to get series_id from TheTVDB} }
- Use API agasint series_directory[iterator]["show_name"] to get SHOW_ID for each show
- Function to determine Season folder with the most recently added episode
- Determine if the recently added episode is within the past week
- Only update the tags for most recent episode
- This will require some way to differentiate betwen a show added in its entirety vs a show that is updtaed one episode at a time

# TODOs COMPLETED
- Function to count total number of seasons
    - Improved: Get show name from API
    - Get season total from API
    - COMPLETED
- Move API portion to a function
    - get_episode_tags.py
    - COMPLETED
- Move metadata write portion to function
    - clear_tags.py
    - set_episode_tags.py
    - COMPLETED
- Build out for more metadata tags. Track (episode), Disc (season), Year, Album (Season name if applicable), etc
    - COMPLETED
