# Film data capture script
This script fetches and processes movie data from The Movie Database (TMDB) for the year 2023. The data is then saved to a CSV file.

**Features**
- Fetches movies based on a specified date range
- Retrieves movies released in 2023
- Sorts movies by popularity
- Extracts essential movie information including title, release date, popularity, votes, average vote score, and genres
- Handles pagination and API rate limits
- Saves the data into a CSV file

**Requirements**
Python 3.x
requests library

**Installation**

Clone the repository:
```sh
git clone https://github.com/yourusername/movie-data-fetcher.git
cd movie-data-fetcher
```

Install the required Python packages:

```sh
pip install requests
```

**Output**
The script will create a file named Films_2023.csv in the current directory, containing the movie data for the year 2023.

**Contributing**
Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

**License**
This project is licensed under the MIT License. See the LICENSE file for details.
