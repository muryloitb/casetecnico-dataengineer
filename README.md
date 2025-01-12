# Discogs Scraper

Este README fornece uma explicação detalhada e humanizada sobre o script fornecido, que realiza scraping de dados do site Discogs para coletar informações sobre artistas, álbuns e músicas. O objetivo é simplificar a execução e manutenção do script, além de facilitar sua adaptação para diferentes casos de uso.

---

## **Descrição Geral**

O script utiliza o Selenium WebDriver e o BeautifulSoup para navegar no site Discogs e extrair informações de artistas e seus álbuns. Ele é configurado para trabalhar com um gênero musical específico e coleta até 10 artistas por vez, salvando os dados em um arquivo JSONL.

---

## **Requisitos**

1. **Python 3.7+**
2. Bibliotecas Python necessárias:
   - `selenium`
   - `bs4` (BeautifulSoup)
   - `re`
   - `json`
3. **Google Chrome** instalado no sistema.
4. **ChromeDriver** compatível com a versão do Google Chrome instalada.

### **Instalação das Dependências**

Execute o comando abaixo para instalar as bibliotecas necessárias:

```bash
pip install selenium beautifulsoup4
```

---

## **Funcionamento do Script**

### **1. Configuração do Selenium**

O script utiliza o Selenium para automatizar a navegação no Discogs. O Chrome é executado no modo headless (sem interface gráfica) para maior eficiência.

### **2. Estrutura Principal do Script**

#### \*\*Função: \*\***`coletar_links_artistas`**

- Navega na página de exploração de um gênero específico.
- Coleta links dos perfis de até 10 artistas.
- Retorna uma lista de URLs dos artistas.

#### \*\*Função: \*\***`extrair_dados_artista`**

- Acessa a página de um artista e extrai:
  - Nome do artista.
  - Gêneros e estilos musicais.
  - Membros da banda (se aplicável).
  - Links para outros sites associados ao artista.
  - Dados dos álbuns (limitado a 10 álbuns).

#### \*\*Função: \*\***`extrair_dados_album`**

- Coleta detalhes de um álbum, incluindo:
  - Nome do álbum.
  - Ano de lançamento.
  - Gravadora.
  - Faixas e suas durações.

#### \*\*Função Principal: \*\***`scrape_discogs`**

- Define o gênero musical a ser explorado.
- Configura o WebDriver.
- Coleta os dados dos artistas e os salva progressivamente em um arquivo JSONL.

### **3. Formato de Saída**

Os dados coletados são salvos no formato JSONL (JSON Lines), que é ideal para grandes volumes de dados estruturados. Cada linha do arquivo representa os dados de um artista.

Exemplo de uma linha do arquivo `discogs_data.jsonl`:

```json
{
  "genre": "Rock",
  "artist_name": "The Beatles",
  "members": ["John Lennon", "Paul McCartney", "George Harrison", "Ringo Starr"],
  "artist_sites": ["https://www.thebeatles.com"],
  "albums": [
    {
      "release_year": "1969",
      "album_name": "Abbey Road",
      "label": "Apple Records",
      "tracks": [
        {"track_number": 1, "track_name": "Come Together", "duration": "4:20"},
        {"track_number": 2, "track_name": "Something", "duration": "3:03"}
      ]
    }
  ]
}
```

---

## **Como Executar**

1. Certifique-se de que o ChromeDriver está configurado corretamente e o caminho está atualizado na função `Service`:

```python
service = Service("/caminho/para/chromedriver")
```

2. Ajuste o gênero musical na função principal:

```python
genre = "Rock"  # Substitua "Rock" pelo gênero desejado.
```

3. Execute o script no terminal:

```bash
python nome_do_script.py
```

4. Verifique o arquivo de saída `discogs_data.jsonl` na pasta do script.

---

## **Erros Comuns e Soluções**

1. **Erro: ********`TimeoutException`******** ao carregar páginas**

   - A conexão pode estar lenta ou o site sobrecarregado. Tente aumentar o tempo de espera em:

   ```python
   WebDriverWait(driver, 15)
   ```

2. **Erro: Caminho do ChromeDriver inválido**

   - Certifique-se de que o ChromeDriver está instalado e o caminho correto foi fornecido na linha:

   ```python
   service = Service("/caminho/para/chromedriver")
   ```

3. **Erro ao coletar álbuns ou faixas**

   - Nem todos os álbuns possuem todas as informações. O script já trata exceções para evitar interrupções.

---

## **Considerações Finais**

- O script é projetado para capturar até 10 artistas por execução. Para aumentar este limite, ajuste o seguinte trecho:

```python
if len(artist_links) == 10:
    break
```


```

---


