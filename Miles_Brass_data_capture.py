import requests
import csv
from datetime import date, datetime, timedelta


# Function to fetch movie data for a specific date range -> 2023 in this case
def fetch_movies_by_date_range(start_date, end_date, api_key):
    # API endpoint for discovering movies
    url = "https://api.themoviedb.org/3/discover/movie"

    # Set up headers for API request
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Set up parameters for API request
    params = {
        'with_original_language': 'en',
        'include_adult': 'false',
        'include_video': 'false',
        'sort_by': 'popularity.desc',
        'primary_release_date.gte': start_date,
        'primary_release_date.lte': end_date,
        'page': 1
    }

    # Dictionary to translate genre IDs to genre names
    genres_dict = {
        28: "Action",
        12: "Adventure",
        16: "Animation",
        35: "Comedy",
        80: "Crime",
        99: "Documentary",
        18: "Drama",
        10751: "Family",
        14: "Fantasy",
        36: "History",
        27: "Horror",
        10402: "Music",
        9648: "Mystery",
        10749: "Romance",
        878: "Science Fiction",
        10770: "TV Movie",
        53: "Thriller",
        10752: "War",
        37: "Western"
    }

    all_films = []
    while True:
        # Make API request
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Process each film in the response
        for film in data.get('results', []):
            # Extract relevant information from each film -> title,
            # release date, popularity, votes, average vote score, and genre
            title = film.get('title')
            release_date = film.get('release_date')
            popularity = film.get('popularity')
            votes = film.get('vote_count')
            votes_average = film.get('vote_average')
            genre = film.get('genre_ids')

            # Translate genre IDs to genre names
            temp_genre_list = []
            for id in genre:
                temp_genre_list.append(genres_dict[id])
            translated_genres = ", ".join(temp_genre_list)

            # Convert release_date to datetime object
            try:
                release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
            except ValueError:
                continue  # Skip if the date format is incorrect

            # Data validation
            # This is to check data type & if entries are blank
            if not isinstance(title, str) or not title:
                print(f"Skipping entry due to invalid title: {title}")
                continue
            elif not isinstance(popularity, (int, float)) or not popularity:
                popularity = "No data"
            elif not isinstance(votes, (int, float)):
                votes = "No data"
            elif not isinstance(votes_average, (int, float)) or not votes_average:
                votes_average = "No data"
            elif not isinstance(translated_genres, str) or not translated_genres:
                popularity = "No data"

            # Add film data to the list
            all_films.append({
                'title': title,
                'release_date': release_date,
                'popularity': popularity,
                'votes': votes,
                'votes_average': votes_average,
                'genre': translated_genres
            })

        # Break the loop if we've reached the last page or the 500th page
        if params['page'] >= data['total_pages'] or params['page'] >= 500:
            break

        # Move to the next page
        params['page'] += 1

    return all_films

# API key for authentication
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZmZhMGQ4Mzg4NTQxZGI3YzE5NDMxMGE2ZTgxZjIzZSIsIm5iZiI6MTcxOTc4NDEyNi4wODI3NzUsInN1YiI6IjY2N2ViYzM2NGM2MmJmZjgwNDdkZTEzYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.okA8bVeTnrgIG0nt-MFh7I7fWyF1yEeU4pUilYR_35w"
all_film_data = []

# Fetch data for each month in 2023 -> breaking into months prevents the API
# request limit being reached
for month in range(1, 13):
    start_date = datetime(2023, month, 1)
    if month == 12:
        end_date = datetime(2023, 12, 31)
    else:
        end_date = datetime(2023, month + 1, 1) - timedelta(days=1)

    all_film_data.extend(fetch_movies_by_date_range(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), api_key))

# Write collected data to a CSV file
csv_filename = 'Films_2023.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'release_date', 'popularity', 'votes', 'votes_average', 'genre']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for movie in all_film_data:
        writer.writerow(movie)

print(f"Film data has been written to {csv_filename}.")
