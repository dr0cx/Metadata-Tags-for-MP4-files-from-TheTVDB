import requests

def get_show_data(API_KEY, SHOW_ID, show_data):

    # Initialize show_data
    show_data[SHOW_ID] = {
        "name": '',
        "total_seasons": 0
    }

    # Make a request to fetch the JSON data
    url = f"https://api.thetvdb.com/series/{SHOW_ID}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract series name
        series_name = data["data"]["seriesName"]

        # Calculate the total number of seasons
        total_seasons = int(data["data"]["season"])

        # Update the show_data dictionary with series name, total seasons, and Specials presence
        show_data[SHOW_ID] = {
            "name": series_name,
            "total_seasons": total_seasons
        }
    else:
        # Handle request errors
        print("Error:", response.status_code)
