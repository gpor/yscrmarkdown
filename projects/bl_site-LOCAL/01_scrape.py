from lib.scrape import scrape_and_write_to_file
from lib.find_internal_links import find_internal_links

urls = [
    'http://localhost:3040/',
    'http://localhost:3040/about',
    "http://localhost:3040/services/content-strategy",
    # "http://localhost:3040/services/copywriting",
    'http://localhost:3040/about',
    'http://localhost:3040/careers',
    'http://localhost:3040/contact',
]


chat_system_prompt = """
You are an expert in answering questions about Bright Labs Digital Agency

Here are some relevant frequently asked questions with answers:
{retrieved_from_vector_db}

Here is the question to answer:
{question}

Use the above information to provide an accurate answer and also provide the metadata IDs from the most relevant documents.

If the information is not sufficient, respond with 'Sorry, I do not have that information /no_think'.
"""

async def main():
    await scrape_and_write_to_file(
        __name__.split('.')[0],
        urls,
        chat_system_prompt,
        'yaml',
        js_walker="bl_site",
    )
