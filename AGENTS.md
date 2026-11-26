# AGENTS.md - ffxiv_makeplace_price_tool

A Python CLI that totals what a MakePlace house's furniture costs on the market board: it reads a house's item list from the MakePlace app, looks the items up in `data/items_db.json`, and fetches their prices from Universalis. How to use it is in [README.md](README.md).

## Running it

- **Python 3.14 and Poetry:** `poetry install`, then copy `.env.example` to `.env` and fill it in (where MakePlace keeps its saves, and whether and where to write a price list).
- **Run:** `poetry run python app.py <house> [data center[/world]] [gil cutoff]`, or `./run <house> …`. `poetry run python app.py list` lists the saved houses.
- **Code:** `app.py` is the entry point, and the rest is in `src/`. There are no tests yet.

## Tickets and branches

Tickets live in `lavaskin/ffxiv-hub` (labelled `price tool`), whose `CONTRIBUTING.md` has the rules every FFXIV repo shares. Branches are `feature/<n>-<desc>` off `dev`, and pull requests go into `dev`. The default branch is `master`, not `main`.

The repo is public, so anyone can open an issue here: a player's issue stays open here, and the hub's ticket for the work links to it.
