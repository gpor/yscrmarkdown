from lib.scrape import get_scrape_dir


if __name__ == "__main__":
    parent_dir, scrape_dir = get_scrape_dir("example")
    print(f"parent_dir = {parent_dir}")
    print(parent_dir.exists())
    print(f"scrape_dir = {scrape_dir}")
    print(scrape_dir.exists())
