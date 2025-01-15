import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import json
import re

def coletar_links_artistas(driver, base_url, genre):
    """Coleta os links dos artistas da página de gênero do Discogs."""

    genre_url = f"{base_url}/explore?genre={genre}"
    driver.get(genre_url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".card.card_large a[href]")
            )
        )
    except TimeoutException:
        print("Erro: Tempo limite ao carregar a página principal.")
        return []

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")

    artist_links = []
    for artist_element in soup.select(".card.card_large a[href]"):
        href = artist_element.get("href")
        if href and "/artist/" in href:
            artist_links.append(base_url + href)
        if len(artist_links) == 10:  # Limitar a 10 artistas
            break

    return artist_links

def extrair_dados_artista(driver, artist_url):
    """Extrai os dados de um artista, incluindo nome, gênero, membros e álbuns."""

    try:
        print(f"Acessando artista: {artist_url}")
        driver.get(artist_url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

        artist_soup = BeautifulSoup(driver.page_source, "html.parser")

        # Nome do artista
        artist_name = artist_soup.select_one("h1").text.strip() if artist_soup.select_one("h1") else "Desconhecido"

        # Coletar sites do artista
        artist_sites = [
            {
                "name": site.text.strip(),
                "url": site.get("href").strip(),
            }
            for site in artist_soup.select("a.link_1ctor.link_3fSf-")
        ]

        # Coletar membros do artista
        members = []
        for member in artist_soup.select("a.link_1ctor span"):
            name = member.text.strip()
            is_active = "strikeThrough_3twT1" not in member.get("class", [])
            members.append({
                "name": name,
                "active": is_active
            })

        # Gênero e estilos
        genres_styles = artist_soup.select(".profile h3 + ul li")
        genre = genres_styles[0].text.strip() if genres_styles else "N/A"
        styles = [g.text.strip() for g in genres_styles[1:]] if len(genres_styles) > 1 else []

        # Coletar álbuns do artista (limitado a 10)
        albums = []
        album_elements = artist_soup.select(".release-item")[:10]
        for album_element in album_elements:
            album_data = extrair_dados_album(driver, album_element)
            if album_data:
                albums.append(album_data)

        artist_data = {
            "artist_name": artist_name,
            "artist_sites": artist_sites,
            "members": members,
            "genre": genre,
            "styles": styles,
            "albums": albums,
        }

        return artist_data

    except Exception as e:
        print(f"Erro ao acessar dados do artista {artist_url}: {e}")
        return None

def extrair_dados_album(driver, album_element):
    """Extrai os dados de um álbum, incluindo nome, ano de lançamento, gravadora e faixas."""

    try:
        album_name = album_element.select_one(".title").text.strip() if album_element.select_one(".title") else "Desconhecido"
        album_url = base_url + album_element.select_one(".title a")["href"] if album_element.select_one(".title a") else None
        release_year_match = re.search(r"\d{4}", album_element.text)
        release_year = release_year_match.group(0) if release_year_match else "Desconhecido"
        label = "N/A"
        tracks = []

        if album_url:
            # Detalhes do álbum
            print(f"Acessando álbum: {album_url}")
            driver.get(album_url)
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tracklist_track"))
            )

            album_soup = BeautifulSoup(driver.page_source, "html.parser")
            label_elem = album_soup.select_one(".label_and_cat h4")
            label = label_elem.text.strip() if label_elem else "N/A"

            # Coletar faixas
            for track_number, track_element in enumerate(
                    album_soup.select(".tracklist_track .track_title"), start=1
            ):
                duration_elem = track_element.find_next_sibling(".track_duration")
                duration = duration_elem.text.strip() if duration_elem else "N/A"
                tracks.append(
                    {
                        "track_number": track_number,
                        "track_name": track_element.text.strip(),
                        "duration": duration,
                    }
                )

        return {
            "release_year": release_year,
            "album_name": album_name,
            "label": label,
            "tracks": tracks,
        }

    except Exception as e:
        print(f"Erro ao acessar detalhes do álbum: {e}")
        return None

def scrape_discogs():
    base_url = "https://www.discogs.com/pt_BR"
    genre = "Rock"  # Substitua "Rock" pelo gênero desejado

    # Configurar o Selenium WebDriver
    service = Service("/usr/local/bin/chromedriver")  # Ajuste o caminho conforme necessário
    options = Options()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    )
    options.add_argument("--headless")  # Executar o Chrome em modo headless
    driver = webdriver.Chrome(service=service, options=options)

    try:
        artist_links = coletar_links_artistas(driver, base_url, genre)
        if not artist_links:
            print("Nenhum artista encontrado.")
            return

        for artist_url in artist_links:
            artist_data = extrair_dados_artista(driver, artist_url)
            if artist_data:
                # Salvar progressivamente no formato JSONL
                with open("discogs_data.jsonl", "a", encoding="utf-8") as file:
                    file.write(json.dumps(artist_data, ensure_ascii=False) + "\n")

                print(f"Dados do artista {artist_data['artist_name']} salvos.")

    finally:
        # Fechar o navegador
        driver.quit()

    print("Dados completos salvos em discogs_data.jsonl")

if __name__ == "__main__":
    scrape_discogs()


