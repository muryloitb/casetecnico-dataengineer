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

        # Gênero
        genre_element = artist_soup.select_one("a[href*='/genre/']")
        genre = genre_element.text.strip() if genre_element else "Desconhecido"

        # Estilos
        styles_elements = artist_soup.select("a[href*='/style/']")
        styles = [style.text.strip() for style in styles_elements]

        # Coletar álbuns do artista (limitado a 10)
        albums = []
        album_elements = artist_soup.select(".release-item")[:10]
        for album_element in album_elements:
            album_data = extrair_dados_album(BeautifulSoup(str(album_element), "html.parser"))
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

def extrair_dados_album(album_soup):
    """Extrai os dados de um álbum, incluindo nome, ano de lançamento, gravadora e faixas."""
    try:
        # Nome do álbum
        album_name = album_soup.select_one("h1.MuiTypography-headLineXL.title_1q3xW").text.strip() if album_soup.select_one("h1.MuiTypography-headLineXL.title_1q3xW") else "Desconhecido"

        # Ano de lançamento
        release_year = album_soup.select_one("time").get("datetime", "Desconhecido") if album_soup.select_one("time") else "Desconhecido"

        # Gravadora
        label_element = album_soup.select_one("span.MuiTypography-labelSmall.css-1kybk0l a")
        label = label_element.text.strip() if label_element else "Desconhecido"

        # Faixas
        tracks = []
        track_elements = album_soup.select("tr[data-track-position]")
        for track_element in track_elements:
            track_title = track_element.select_one("span.trackTitle_CTKp4").text.strip() if track_element.select_one("span.trackTitle_CTKp4") else "Desconhecido"
            written_by = [
                composer.text.strip() for composer in track_element.select("span.link_15cpV a")
            ]
            tracks.append({
                "track_title": track_title,
                "written_by": written_by
            })

        return {
            "album_name": album_name,
            "release_year": release_year,
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

