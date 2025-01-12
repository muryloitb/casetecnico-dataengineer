import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import re


def scrape_discogs():
    base_url = "https://www.discogs.com/pt_BR"
    genre_url = f"{base_url}/explore?genre=Rock"  # Substitua "Rock" pelo gênero desejado

    # Configurar o Selenium WebDriver
    service = Service('/usr/local/bin/chromedriver')  # Certifique-se de que o chromedriver está no PATH ou ajuste o caminho
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    #options.add_argument('--headless')  # Executar o Chrome em modo headless (sem interface gráfica)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Acessar a página do gênero
        driver.get(genre_url)
        time.sleep(random.uniform(2, 5))  # Aguardar a página carregar

        # Aguarde o carregamento da página inicial
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card.card_large a[href]")))

        # Obter o conteúdo HTML após o carregamento
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Coletar links dos artistas
        artist_links = []
        for artist in soup.select(".card.card_large a[href]"):
            href = artist.get("href")
            if href and "/artist/" in href:
                artist_links.append(base_url + href)
            if len(artist_links) == 10:  # Limitar a 10 artistas
                break

        if not artist_links:
            print("Nenhum artista encontrado.")
            return

        data = []

        for artist_url in artist_links:
            try:
                print(f"Acessando artista: {artist_url}")
                driver.get(artist_url)
                time.sleep(random.uniform(2, 5))  # Aguardar a página carregar
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

                artist_soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Nome do artista
                artist_name = artist_soup.select_one("h1").text.strip() if artist_soup.select_one("h1") else "Desconhecido"

                # Gênero e estilos
                genres_styles = artist_soup.select(".profile h3 + ul li")
                genre = genres_styles[0].text.strip() if genres_styles else "N/A"
                styles = [g.text.strip() for g in genres_styles[1:]] if len(genres_styles) > 1 else []

                # Membros do artista
                members = [m.text.strip() for m in artist_soup.select(".artist-members a")] or ["N/A"]

                # Sites do artista
                artist_sites = [s.text.strip() for s in artist_soup.select(".links a")] or ["N/A"]

                # Coletar álbuns do artista
                albums = []
                album_elements = artist_soup.select(".release-item")[:10]
                if not album_elements:
                    print(f"Nenhum álbum encontrado para o artista {artist_name}.")

                for album in album_elements:
                    album_name = album.select_one(".title").text.strip() if album.select_one(".title") else "Desconhecido"
                    album_url = base_url + album.select_one(".title a")["href"] if album.select_one(".title a") else None
                    release_year = re.search(r"\d{4}", album.text).group(0) if re.search(r"\d{4}", album.text) else "Desconhecido"
                    label = "N/A"
                    tracks = []

                    # Detalhes do álbum
                    if album_url:
                        try:
                            print(f"Acessando álbum: {album_url}")
                            driver.get(album_url)
                            time.sleep(random.uniform(2, 5))  # Aguardar a página carregar
                            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "tracklist_track")))
                            album_soup = BeautifulSoup(driver.page_source, 'html.parser')
                            label = album_soup.select_one(".label_and_cat h4").text.strip() if album_soup.select_one(".label_and_cat h4") else "N/A"

                            # Coletar faixas
                            for track_number, track in enumerate(album_soup.select(".tracklist_track .track_title"), start=1):
                                track_name = track.text.strip()
                                duration = track.find_next_sibling(".track_duration").text.strip() if track.find_next_sibling(".track_duration") else "N/A"
                                tracks.append({"track_number": track_number, "track_name": track_name, "duration": duration})

                        except Exception as e:
                            print(f"Erro ao acessar detalhes do álbum: {e}")

                    albums.append({
                        "release_year": release_year,
                        "album_name": album_name,
                        "label": label,
                        "tracks": tracks,
                        "styles": styles
                    })

                artist_data = {
                    "genre": genre,
                    "artist_name": artist_name,
                    "members": members,
                    "artist_sites": artist_sites,
                    "albums": albums
                }

                data.append(artist_data)

                # Salvar progressivamente no formato JSONL
                with open("discogs_data.jsonl", "a", encoding="utf-8") as file:
                    file.write(json.dumps(artist_data, ensure_ascii=False) + "\n")

                print(f"Dados do artista {artist_name} salvos.")

            except Exception as e:
                print(f"Erro ao acessar dados do artista: {e}")

    finally:
        # Fechar o navegador
        driver.quit()

    print("Dados completos salvos em discogs_data.jsonl")

if __name__ == "__main__":
    scrape_discogs()
