import argparse
import asyncio
import aiohttp
import feedparser

import tqdm

from datasets import Dataset, DatasetDict
import json

_FEED_URL = "https://www.viedemerde.fr/rss"
__DEFAULT_LIMIT = 10
__DEFAULT_OUTPUT = "dataset.json"

parser = argparse.ArgumentParser(description="Scrape VDM website RSS feed")
parser.add_argument("--limit", type=int, default=__DEFAULT_LIMIT, help="Number of pages to scrape")
parser.add_argument("--output", type=str, default=__DEFAULT_OUTPUT, help="Output file")
args = parser.parse_args()


async def fetch_anecdotes(limit):
    entries = []
    actual_page = 1

    anecdotes = []

    async with aiohttp.ClientSession() as session:
        with tqdm.tqdm(total=limit, desc="Fetching anecdotes") as pbar:
            while actual_page <= limit:
                url = f"{_FEED_URL}?page={actual_page}"
                try:
                    async with session.get(url) as resp:
                        text = await resp.text()
                        feed = feedparser.parse(text)
                        entries.extend(feed.entries)
                        for entry in entries:
                            anecdotes.append(entry.description)

                        if len(entries) == 0:
                            break

                        pbar.update(1)

                        actual_page += 1
                except (aiohttp.ClientResponseError, aiohttp.InvalidURL, aiohttp.ClientConnectorError) as e:
                    print(f"An error occurred: {e}")
                    break

    print(f"Scraped {len(anecdotes)} anecdotes")

    return anecdotes


def create_dataset(anecdotes):
    dataset = {"train": Dataset.from_dict({"text": list(anecdotes)})}
    datasets = DatasetDict(dataset)
    del dataset
    return datasets


def save_dataset(datasets):
    train = datasets["train"]
    dataset_dict = {"train": train['text']}
    with open(args.output, "w", encoding='utf-8') as f:
        json.dump(dataset_dict, f, ensure_ascii=False)


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    anecdotes = loop.run_until_complete(fetch_anecdotes(args.limit))

    dataset = create_dataset(anecdotes)
    save_dataset(dataset)

    print(f"Dataset saved to {args.output}")


if __name__ == "__main__":
    main()
