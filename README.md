# VDM Anecdotes RSS Scraper

This project is a simple Python script that scrapes anecdotes from the VDM website's RSS feed and creates a dataset of
the anecdotes.

## Requirements

- Python 3.7+
- aiohttp
- asyncio
- feedparser
- tqdm
- datasets

## Installation

1. Clone the repository:

     ```bash
    git clone https://github.com/PLOTFINDER/vdm-dataset.git
    cd vdm-dataset
     ```

2. Install the dependencies:

     ```bash
    pip install -r requirements.txt
     ```

## Usage

You can run the script with the following command:

```bash
    python main.py --limit <number_of_pages> --output <output_file>
```

- `--limit`: The number of pages to scrape (default is 10).
- `--output`: The output file where the scraped anecdotes will be saved (default is "dataset.json").

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
