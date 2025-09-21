import inquirer
import importlib.util
import sys
import asyncio
from pathlib import Path

def get_projects_dirs(PROJECTS_DIR):
    if not PROJECTS_DIR.exists():
        print(f"Error: {PROJECTS_DIR} directory not found!")
        return []

    return [d for d in PROJECTS_DIR.iterdir() if d.is_dir() and d.name != "BOILERPLATE"]

def get_scripts(PROJECTS_DIR):
    scripts = []
    for project_dir in get_projects_dirs(PROJECTS_DIR):
        for file in project_dir.iterdir():
            if file.suffix == '.py' and not file.name.startswith('__'):
                scripts.append(file)
    return [f"{project_dir.name}/{f.name}" for f in sorted(scripts, key=lambda f: f.stat().st_mtime, reverse=True)]

def run_selected_script(PROJECTS_DIR, filename):
    script_path = PROJECTS_DIR / filename
    module_name = filename.replace("/", ".")[:-3]
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        if hasattr(module, 'main'):
            asyncio.run(module.main())
        elif hasattr(module, 'run'):
            module.run()
            
    except Exception as e:
        print(f"Error running {filename}: {e}")

def main():
    PROJECTS_DIR = Path("projects")
    
    scripts = get_scripts(PROJECTS_DIR)
    
    if not scripts:
        print(f"No Python files found in the {PROJECTS_DIR} directory.")
        return
    
    user_selection = inquirer.prompt([
        inquirer.List('script',
                      message="Select a project script to run",
                      choices=scripts,
                      carousel=True)
    ])

    if user_selection and user_selection['script']:
        selected_file = user_selection['script']
        print(f"\n🚀 Running: {selected_file}")
        print("-" * 40)
        run_selected_script(PROJECTS_DIR, selected_file)
    else:
        print("No script selected. Exiting.")
    

if __name__ == "__main__":
    main()