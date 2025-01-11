# Discogs Web Scraping Project

## Description
This project is a web scraper designed to extract information about artists and albums from the Discogs website. The scraper collects data for a specified music genre and organizes it into a JSONL file. This includes details about the artists, their members, websites, albums, and tracks.

## Features
- Scrapes data for up to 10 artists in a specific genre.
- Collects up to 10 albums per artist.
- Gathers detailed information such as:
  - Artist name, members, and external links.
  - Album name, release year, label, and styles.
  - Track details (number, name, duration).
- Outputs data to a JSONL file.

## Requirements
- Python 3.7 or higher
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`

Install dependencies using:
```bash
pip install -r requirements.txt
```

## Usage
1. Clone the repository:
```bash
git clone https://github.com/your-repo-name/discogs-scraper.git
cd discogs-scraper
```

2. Update the genre in the script (default: `rock`).

3. Run the script:
```bash
python scraper.py
```

4. The output will be saved as `output.jsonl` in the project directory.

## Output Format
The data is saved in JSONL (JSON Lines) format. Each line represents a JSON object:
```jsonl
{
  "genre": "rock",
  "artist_name": "Artist Name",
  "members": ["Member 1", "Member 2"],
  "sites": ["https://artist-site.com"],
  "albums": [
    {
      "album_name": "Album Name",
      "release_year": "2023",
      "label": "Label Name",
      "tracks": [
        {
          "track_number": "1",
          "track_name": "Track Title",
          "track_duration": "3:45"
        }
      ]
    }
  ]
}
```

## Notes
- Be mindful of the site's terms of service when scraping.
- The script includes a delay between requests to prevent overwhelming the server.

## Testing
Run unit tests using:
```bash
python -m unittest discover tests
```

## License
This project is licensed under the MIT License.
