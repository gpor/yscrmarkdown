import asyncio
from lib.scrape import scrape_to_cleaned_html

name = 'thelook' # /storage/{name}/scrape_{timestamp}

urls = [
    "https://thelookortho.com.au",
]

chat_system_prompt = """
You are an expert in answering questions about The Look Orthodontists

Here are some relevant frequently asked questions with answers: {retrieved_from_vector_db}

Here is the question to answer: {question} /no_think
"""

async def main():
    await scrape_to_cleaned_html(name, urls, chat_system_prompt)

if __name__ == "__main__":
    asyncio.run(main())
