from lib.scrape import scrape_and_write_to_file

urls = [
    "https://abetterculture.org.au/",
]

chat_system_prompt = """
You are an expert in answering questions about A Better Culture

Here are some relevant frequently asked questions with answers:
{retrieved_from_vector_db}

Here is the question to answer:
{question}

Use the above information to provide an accurate answer and also provide the metadata IDs from the most relevant documents.

If the information is not sufficient, respond with 'Sorry, I do not have that information /no_think'.
"""

async def main():
    await scrape_and_write_to_file(
        __name__,
        urls,
        chat_system_prompt,
        output_format='html',
    )

