# PLFM Group Website

Source for the [PLFM group website](https://plfm.epfl.ch) at EPFL.

## Dependencies

- [Pelican](https://getpelican.com/) — Python static site generator

## Project Structure

```
plfm-web/
├── content/
│   └── pages/          # Site pages (home, people, seminar) in Markdown
├── templates/          # Jinja2 HTML templates
├── static/
│   ├── css/            # Stylesheets
│   └── images/         # Photos and other images
├── data/
│   ├── people.yaml     # Faculty and affiliate data (edit directly)
│   └── publications.json  # Generated from publications.bib (do not edit)
├── publications.bib    # BibTeX source for publications
├── scripts/
│   └── bib2json.py     # Converts publications.bib → data/publications.json
├── pelicanconf.py      # Pelican configuration (dev)
└── publishconf.py      # Pelican configuration (production)
```

## Setup

Use of a Python virtual environment is recommended.

On the first session, create the virtual environment and install dependencies.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On subsequent sessions, just activate the virtual environment before running any commands:

```bash
source .venv/bin/activate
```

## Building

Run a local dev server with live reload:

```bash
pelican --autoreload --listen
```

Build for production:

```bash
pelican -s publishconf.py
```

Output goes to `output/`. Run `make clean` to remove it.

## Publishing

```bash
make deploy
```

This builds the site and uploads the output to `ic-ftps.epfl.ch` via `lftp`. You will be prompted for your EPFL username and password.
