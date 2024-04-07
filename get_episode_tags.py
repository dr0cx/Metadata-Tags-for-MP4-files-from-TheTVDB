import requests

def get_episode_tags(API_KEY, EPISODES_ENDPOINT, SHOW, episode_titles):
    """
    Retrieve episode information from the API and parse the JSON response.

    Args:
        EPISODES_ENDPOINT (str): The endpoint URL for retrieving episode information.
        SHOW (str): The name of the TV show.

    Returns:
        dict: A dictionary containing episode titles and years, indexed by episode numbers.
              Returns an empty dictionary if no episode data is found or if there's an error.
    """
    # Set headers with API key for authentication
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }

    # Make GET request to retrieve episode information
    response = requests.get(EPISODES_ENDPOINT, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        # Parse JSON response
        episode_data = response.json()
        if 'data' in episode_data:
            # Extract episode titles and numbers from the API response
            for episode in episode_data['data']:
                episode_number = f"{SHOW.replace(':','')} - S{episode['airedSeason']:02d}E{episode['airedEpisodeNumber']:02d}"
                episode_title = episode.get('episodeName', 'Unknown Title')
                episode_aired = episode.get('firstAired', 'Unknown Date')
                episode_year = episode_aired.split('-')[0]
                episode_titles[episode_number] = {
                    "title": episode_title,
                    "year": episode_year
                }

            print("Episode titles loaded successfully.")
        else:
            print("No episode data found in API response.")
    else:
        print('Error:', response.status_code)

    return episode_titles
