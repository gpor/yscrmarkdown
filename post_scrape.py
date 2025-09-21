import inquirer
import importlib.util
import sys
import asyncio
from pathlib import Path

PARENT_DIR = Path("post_scrape")

def get_scrape_files():
    if not PARENT_DIR.exists():
        print(f"Error: {PARENT_DIR} directory not found!")
        return []
    
    files = []
    for file in PARENT_DIR.iterdir():
        if file.suffix == '.py' and not file.name.startswith('__') and not file.name == 'BOILERPLATE.py':
            files.append(file)

    return [f.name for f in sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)]

def run_selected_script(filename):
    """Import and run the selected script."""
    script_path = PARENT_DIR / filename
    module_name = filename[:-3]  # Remove .py extension
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        if hasattr(module, 'main'):
            asyncio.run(module.main())
        elif hasattr(module, 'run'):
            module.run()
        # else:
        #     print(f"Script {filename} executed successfully")
            
    except Exception as e:
        print(f"Error running {filename}: {e}")

def main():
    print("🔍 Scrape Script Selector")
    print("=" * 30)
    
    files = get_scrape_files()
    
    if not files:
        print(f"No Python files found in the {PARENT_DIR} directory.")
        return
    
    questions = [
        inquirer.List('script',
                     message="Select a scraper script to run",
                     choices=files,
                     carousel=True)
    ]
    
    answers = inquirer.prompt(questions)
    
    if answers and answers['script']:
        selected_file = answers['script']
        print(f"\n🚀 Running: {selected_file}")
        print("-" * 40)
        run_selected_script(selected_file)
    else:
        print("No script selected. Exiting.")

if __name__ == "__main__":
    main()


