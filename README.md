# Web Scraper — Catálogo de Livros

Script de coleta de dados de páginas públicas para praticar **web scraping, parsing de HTML e análise de dados**.

**Stack:** Python · Requests · Beautiful Soup · lxml · Pandas

## O que faz
- Coleta dados do site educacional [Books to Scrape](https://books.toscrape.com/).
- Extrai título, preço, avaliação e disponibilidade de livros.
- Percorre múltiplas páginas (até cinco por padrão).
- Normaliza notas, exporta `output/books.csv` e registra `output/scraper_log.json`.
- Exibe uma pequena análise de preços e avaliações no terminal.

## Executar
```bash
git clone https://github.com/fgscarvalho37-a11y/web-scraper.git
cd web-scraper
pip install requests beautifulsoup4 lxml pandas
python scraper.py
```

## Estrutura
- `scraper.py` — coleta, transformação, exportação e logs.
- `output/books.csv` — exemplo de dados coletados.
- `output/scraper_log.json` — exemplo de registro da execução.

> Use apenas em páginas que permitam coleta; respeite limites de requisições, termos do site e privacidade. O alvo deste exercício é um site criado para scraping.

**Status:** Estudo prático de automação de dados.

Desenvolvido por [Felipe Gomes](https://github.com/fgscarvalho37-a11y).