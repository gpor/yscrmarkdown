from lib.scrape import scrape_and_write_to_file

urls = [
    "https://abetterculture.org.au/people/dr-nicole-higgins",
    "https://abetterculture.org.au/people/david-clarke",
    "https://abetterculture.org.au/people/komal-daredia",
    "https://abetterculture.org.au/people/ms-helen-szoke-ao",
    "https://abetterculture.org.au/news-resources/strategy-proposal",
    "https://abetterculture.org.au/people/dr-elise-buisson",
    "https://abetterculture.org.au/people/karen-grace",
    "https://abetterculture.org.au/news-resources?limit=6&page=1&resourcetag=reports&sort=desc&type=resources",
    "https://abetterculture.org.au/people/dr-jillan-farmer",
    "https://abetterculture.org.au/news-resources?tab=updates",
    "https://abetterculture.org.au/about-us",
    "https://abetterculture.org.au/news-resources/working-group-drafts",
    "https://abetterculture.org.au/news-resources/consolidated-wg-report",
    "https://abetterculture.org.au/contact-us",
    "https://abetterculture.org.au/people/dr-louis-peachey",
    "https://abetterculture.org.au/news-resources?resourcetag=reports",
    "https://abetterculture.org.au/news-resources?limit=6&page=1&sort=desc&type=resources",
    "https://abetterculture.org.au/news-resources",
    "https://abetterculture.org.au/privacy",
    "https://abetterculture.org.au/news-resources?tab=resources",
    "https://abetterculture.org.au/",
    "https://abetterculture.org.au/news-resources/chat",
    "https://abetterculture.org.au/people/maddie-roberts",
    "https://abetterculture.org.au/news-resources?tab=news",
    "https://abetterculture.org.au/news-resources/curriculum",
    "https://abetterculture.org.au/environmental-scan?page=1&sort=desc",
    "https://abetterculture.org.au/people/dr-karen-stringer",
    "https://abetterculture.org.au/environmental-scan",
    "https://abetterculture.org.au/news-resources/cultural-safety",
    "https://abetterculture.org.au/about-us/reference-groups",
    "https://abetterculture.org.au/people/jade-rameka",
    "https://abetterculture.org.au/people/judy-finn",
    "https://abetterculture.org.au/people/dr-clare-skinner",
    "https://abetterculture.org.au/news-resources?tab=newsletters",
    "https://abetterculture.org.au/about-us/working-groups",
    "https://abetterculture.org.au/terms",
    "https://abetterculture.org.au/people/dr-sarah-jane-springer",
    "https://abetterculture.org.au/people/dr-carly-dober",
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

