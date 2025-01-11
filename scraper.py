import requests
from bs4 import BeautifulSoup
import json
import re
from time import sleep

# Base URL for Discogs (with Portuguese localization)
BASE_URL = "https://www.discogs.com/pt_BR"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

# Function to scrape artist information
def scrape_artist_data(genre_url, max_artists=10, max_albums=10):
    artists_data = []
    page_number = 1

    while len(artists_data) < max_artists:
        response = requests.get(f"{genre_url}?page={page_number}", headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract artist links
        artist_links = soup.select("a[href*='/artist/']")
        if not artist_links:
            print("No more artist links found. Ending scraping.")
            break

        for artist_link in artist_links:
            if len(artists_data) >= max_artists:
                break

            artist_url = BASE_URL + artist_link['href']
            artist_page = requests.get(artist_url, headers=HEADERS)
            artist_soup = BeautifulSoup(artist_page.content, "html.parser")

            try:
                # Extract artist details
                artist_name = artist_soup.find("h1", class_="title").get_text(strip=True)
                genre = genre_url.split("/")[-1]

                # Extract members
                members = [member.get_text(strip=True) for member in artist_soup.select(".profile .link")]

                # Extract sites
                sites = [site['href'] for site in artist_soup.select("a.external")]

                # Collect album data
                albums = []
                album_links = artist_soup.select("a[href*='/release/']")[:max_albums]

                for album_link in album_links:
                    album_url = BASE_URL + album_link['href']
                    album_page = requests.get(album_url, headers=HEADERS)
                    album_soup = BeautifulSoup(album_page.content, "html.parser")

                    album_name = album_soup.find("h1", class_="title").get_text(strip=True)
                    release_year = album_soup.find("span", class_="release-year").get_text(strip=True) if album_soup.find("span", class_="release-year") else "Unknown"
                    label = album_soup.find("a", href=re.compile("/label/")).get_text(strip=True) if album_soup.find("a", href=re.compile("/label/")) else "Unknown"

                    # Tracks data
                    tracks = []
                    for track in album_soup.select(".tracklist_track"):
                        track_number = track.select_one(".tracklist_track_pos").get_text(strip=True) if track.select_one(".tracklist_track_pos") else "Unknown"
                        track_name = track.select_one(".tracklist_track_title").get_text(strip=True) if track.select_one(".tracklist_track_title") else "Unknown"
                        track_duration = track.select_one(".tracklist_track_duration").get_text(strip=True) if track.select_one(".tracklist_track_duration") else "Unknown"
                        tracks.append({
                            "track_number": track_number,
                            "track_name": track_name,
                            "track_duration": track_duration
                        })

                    albums.append({
                        "album_name": album_name,
                        "release_year": release_year,
                        "label": label,
                        "tracks": tracks
                    })

                artists_data.append({
                    "genre": genre,
                    "artist_name": artist_name,
                    "members": members,
                    "sites": sites,
                    "albums": albums
                })

            except Exception as e:
                print(f"Error processing artist: {artist_link['href']} - {e}")

            # Delay to avoid overwhelming the server
            sleep(2)

        page_number += 1

    return artists_data

# Save data to JSONL file
def save_to_jsonl(data, filename="output.jsonl"):
    with open(filename, "w", encoding="utf-8") as f:
        for entry in data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# Main execution
if __name__ == "__main__":
    genre = "rock"  # Example genre
    genre_url = f"{BASE_URL}/genre/{genre}"

    print("Scraping data... This may take a while.")
    data = scrape_artist_data(genre_url)

    print(f"Saving data to JSONL file.")
    save_to_jsonl(data)

    print("Scraping complete. Data saved to output.jsonl.")

    save_to_jsonl(data)

    print("Scraping complete. Data saved to output.jsonl.")
