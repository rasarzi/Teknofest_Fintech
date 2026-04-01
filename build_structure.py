from pathlib import Path

def create_project_structure():
    base_dir = Path("project_structure")
    subfolders = ["raw", "clean", "structured", "feature", "insight"]
    
    base_dir.mkdir(parents=True, exist_ok=True)
    
    for folder in subfolders:
        folder_path = base_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Create a hidden .gitkeep file so GitHub tracks the empty folder
        keep_file = folder_path / ".gitkeep"
        keep_file.touch(exist_ok=True)
        
        print(f"Created directory: {folder_path}")

if __name__ == "__main__":
    create_project_structure()