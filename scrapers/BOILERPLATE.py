import asyncio
from lib.scrape import scrape_and_write_to_file
from lib.find_internal_links import find_internal_links

name = 'xxxx' # /storage/{name}/scrape_{timestamp}

urls = [
    "https://XXXX",
]

chat_system_prompt = """
You are an expert in answering questions about Xxxx

Here are some relevant frequently asked questions with answers:
{retrieved_from_vector_db}

Here is the question to answer:
{question}

Use the above information to provide an accurate answer and also provide the metadata IDs from the most relevant documents.

If the information is not sufficient, respond with 'Sorry, I do not have that information /no_think'.
"""

async def main():
    urls = await find_internal_links(urls[0], max_depth=2)
    print(f"\nDiscovered {len(urls)} URLs:")
    for u in urls:
        print(u)
    exit()

    await scrape_and_write_to_file(
        name,
        urls,
        chat_system_prompt,
        output_format='html',
    )

if __name__ == "__main__":
    asyncio.run(main())
