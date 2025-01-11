# Discogs Artist & Album Scraper

Este projeto é um scraper desenvolvido em Python para extrair informações de artistas e álbuns de um gênerio musical específico no site [Discogs](https://www.discogs.com/). Ele utiliza as bibliotecas `requests` e `BeautifulSoup` para realizar o web scraping e coleta dados como nome do artista, membros, sites relacionados, informações de álbuns e faixas.

---

## Funcionalidades

O código executa as seguintes tarefas:
1. **Coleta de Artistas**: Extrai links de artistas em uma página de um gênero específico no Discogs.
2. **Coleta de Detalhes do Artista**:
   - Nome do artista.
   - Membros da banda (se aplicável).
   - Links para sites relacionados ao artista.
3. **Coleta de Álbuns**:
   - Nome do álbum.
   - Ano de lançamento.
   - Gravadora.
   - Lista de faixas, incluindo número, nome e duração.
4. **Exportação dos Dados**: Os dados coletados são salvos em um arquivo JSONL (`output.jsonl`).

---

## Requisitos

Certifique-se de ter o Python 3.x instalado, além das seguintes bibliotecas:
- `requests`
- `BeautifulSoup` (do pacote `bs4`)
- `json`
- `re`
- `time`

Instale as bibliotecas necessárias com o comando:
```bash
pip install requests beautifulsoup4
```

---

## Estrutura do Código

- **`BASE_URL` e `HEADERS`**: Contêm a URL base e o cabeçalho para simular um navegador.
- **Função `scrape_artist_data`**:
  - Recebe a URL de um gênero, o número máximo de artistas e álbuns para coletar.
  - Extrai informações dos artistas e seus álbuns.
- **Função `save_to_jsonl`**:
  - Salva os dados extraídos em formato JSONL.
- **Execução Principal (`__main__`)**:
  - Define o gênero desejado.
  - Executa a função de scraping e salva os resultados.

---

## Como Usar

1. **Configurar o Gênero**:
   Altere a variável `genre` para o gênero musical que deseja explorar. Exemplo:
   ```python
   genre = "rock"
   ```
   Isso irá gerar dados de artistas e álbuns relacionados ao gênero **Rock**.

2. **Executar o Script**:
   Execute o script no terminal:
   ```bash
   python scraper.py
   ```

3. **Visualizar os Dados**:
   Após a execução, os dados serão salvos no arquivo `output.jsonl`. Cada linha do arquivo é um registro JSON representando um artista e suas informações.

---

## Exemplo de Estrutura de Dados Extraídos

```json
{
  "genre": "rock",
  "artist_name": "The Beatles",
  "members": ["John Lennon", "Paul McCartney", "George Harrison", "Ringo Starr"],
  "sites": ["https://www.thebeatles.com"],
  "albums": [
    {
      "album_name": "Abbey Road",
      "release_year": "1969",
      "label": "Apple Records",
      "tracks": [
        {
          "track_number": "1",
          "track_name": "Come Together",
          "track_duration": "4:20"
        },
        {
          "track_number": "2",
          "track_name": "Something",
          "track_duration": "3:03"
        }
      ]
    }
  ]
}
```

---


