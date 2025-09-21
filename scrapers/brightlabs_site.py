import asyncio
from lib.scrape import scrape_and_write_to_file
from lib.find_internal_links import find_internal_links

name = 'brightlabs_site' # /storage/{name}/scrape_{timestamp}

url_home = "https://brightlabs.staging.brightlabs.com.au/"
auth=("brightlabs", "brightlabs")

urls = [
    "https://brightlabs.staging.brightlabs.com.au/work/entain",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/epicor",
    "https://brightlabs.staging.brightlabs.com.au/work/finance",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/microsoft-sharepoint",
    "https://brightlabs.staging.brightlabs.com.au/insights/biggest-linkedin-ad-mistakes",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/print-advertising",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/pay-per-click",
    "https://brightlabs.staging.brightlabs.com.au/work/abey-australia",
    "https://brightlabs.staging.brightlabs.com.au/work/lifestyle-luxury",
    "https://brightlabs.staging.brightlabs.com.au/insights",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/craft-cms",
    "https://brightlabs.staging.brightlabs.com.au/industries/health-aged-care",
    "https://brightlabs.staging.brightlabs.com.au/work/kilikanoon-wines",
    "https://brightlabs.staging.brightlabs.com.au/industries/technology",
    "https://brightlabs.staging.brightlabs.com.au/insights/content",
    "https://brightlabs.staging.brightlabs.com.au/insights/digital-grants-incentives",
    "https://brightlabs.staging.brightlabs.com.au/work/focus-dynamics-group",
    "https://brightlabs.staging.brightlabs.com.au/work/health-aged-care",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/ui-ux-design",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/websites",
    "https://brightlabs.staging.brightlabs.com.au/insights/creative",
    "https://brightlabs.staging.brightlabs.com.au/insights?limit=18",
    "https://brightlabs.staging.brightlabs.com.au/work/vacca",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/crm-erp-integration",
    "https://brightlabs.staging.brightlabs.com.au/insights/platforms-partnerships",
    "https://brightlabs.staging.brightlabs.com.au/work/%C3%A0esthetica",
    "https://brightlabs.staging.brightlabs.com.au/careers",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/google-partner",
    "https://brightlabs.staging.brightlabs.com.au/work/united-fasteners",
    "https://brightlabs.staging.brightlabs.com.au/insights/technology",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/microsoft-dynamics-365",
    "https://brightlabs.staging.brightlabs.com.au/industries/finance",
    "https://brightlabs.staging.brightlabs.com.au/insights/digital-marketing-agencies-australia",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/search-engine-optimisation",
    "https://brightlabs.staging.brightlabs.com.au/work/technology",
    "https://brightlabs.staging.brightlabs.com.au/L8%2C%20607%20Bourke%20St%2C%20Melbourne%20VIC%203000",
    "https://brightlabs.staging.brightlabs.com.au/about/rishad-sukhia",
    "https://brightlabs.staging.brightlabs.com.au/work/ewon",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/social-media-advertising",
    "https://brightlabs.staging.brightlabs.com.au/industries",
    "https://brightlabs.staging.brightlabs.com.au/contact",
    "https://brightlabs.staging.brightlabs.com.au/work/clickview",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/campaign-creative",
    "https://brightlabs.staging.brightlabs.com.au/industries/construction-manufacturing",
    "https://brightlabs.staging.brightlabs.com.au/industries/professional-services",
    "https://brightlabs.staging.brightlabs.com.au/industries/education",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/copywriting",
    "https://brightlabs.staging.brightlabs.com.au/insights/new-website-seo-strategy",
    "https://brightlabs.staging.brightlabs.com.au/industries/government",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/google-cloud",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/ecommerce",
    "https://brightlabs.staging.brightlabs.com.au/industries/non-profit",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/shopify",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/meta-marketing-partner",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/customer-experience",
    "https://brightlabs.staging.brightlabs.com.au/terms-of-use",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/hubspot",
    "https://brightlabs.staging.brightlabs.com.au/insights/write-articles-that-generate-traffic",
    "https://brightlabs.staging.brightlabs.com.au/insights/optimising-google-ads",
    "https://brightlabs.staging.brightlabs.com.au/insights/15-ux-tips-supercharge-your-ecommerce",
    "https://brightlabs.staging.brightlabs.com.au/about/tim-mcdougall",
    "https://brightlabs.staging.brightlabs.com.au/work",
    "https://brightlabs.staging.brightlabs.com.au/work/alba-thermal-springs-and-spa",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/content-strategy",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships",
    "https://brightlabs.staging.brightlabs.com.au/work/government",
    "https://www.brightlabs.com.au/insights/Auspost-ORIA-Best-B2B-Retailer-Award",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/consultation",
    "https://brightlabs.staging.brightlabs.com.au/work/non-profit",
    "https://brightlabs.staging.brightlabs.com.au/work/life-saving-victoria",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/brand-strategy-and-design",
    "https://brightlabs.staging.brightlabs.com.au/about",
    "https://www.brightlabs.com.au/solutions/sap-business-one-ecommerce-website",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/wordpress",
    "https://brightlabs.staging.brightlabs.com.au/insights/remarketing-guide",
    "https://brightlabs.staging.brightlabs.com.au/insights/industries",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/runcloud",
    "https://brightlabs.staging.brightlabs.com.au/work/construction-manufacturing",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/social-media-management",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/video-production",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/custom-platform-app-development",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/sap",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/sap-success-factors",
    "https://brightlabs.staging.brightlabs.com.au/insights/performance-marketing",
    "https://brightlabs.staging.brightlabs.com.au/work/education",
    "https://brightlabs.staging.brightlabs.com.au/insights/news-events",
    "https://brightlabs.staging.brightlabs.com.au/privacy",
    "https://brightlabs.staging.brightlabs.com.au/work/alba-thermal-springs",
    "https://brightlabs.staging.brightlabs.com.au/",
    "https://brightlabs.staging.brightlabs.com.au/industries/lifestyle-luxury",
    "https://brightlabs.staging.brightlabs.com.au/work/iccons",
    "https://brightlabs.staging.brightlabs.com.au/about/susan-douglass",
    "https://brightlabs.staging.brightlabs.com.au/work/deadly-story",
    "https://brightlabs.staging.brightlabs.com.au/work/vetafarm",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/salesforce",
    "https://brightlabs.staging.brightlabs.com.au/work/professional-services",
    "https://brightlabs.staging.brightlabs.com.au/what-we-do/managed-services",
    "https://brightlabs.staging.brightlabs.com.au/work/legal",
    "https://brightlabs.staging.brightlabs.com.au/insights/supercharge-your-google-ads-performance",
    "https://www.brightlabs.com.au/solutions/google-cloud-platform",
    "https://brightlabs.staging.brightlabs.com.au/industries/legal",
    "https://brightlabs.staging.brightlabs.com.au/platforms-partnerships/campaign-monitor",
]

chat_system_prompt = """
You are an expert in answering questions about Bright Labs Digital Firm

Here are some relevant frequently asked questions with answers:
{retrieved_from_vector_db}

Here is the question to answer:
{question}

Use the above information to provide an accurate answer and also provide the metadata IDs from the most relevant documents.

If the information is not sufficient, respond with 'Sorry, I do not have that information /no_think'.
"""

async def main():
    # urls = await find_internal_links(
    #     url_home,
    #     max_depth=2,
    #     auth=auth
    # )
    # print(f"\nDiscovered {len(urls)} URLs:")
    # for u in urls:
    #     print(u)
    # exit()
    await scrape_and_write_to_file(
        name,
        urls,
        chat_system_prompt,
        output_format='html',
        auth=auth
    )

if __name__ == "__main__":
    asyncio.run(main())
