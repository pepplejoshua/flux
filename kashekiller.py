from pathlib import Path
import shutil

# definition
def rcache(path):
    for child in path.iterdir():
        if child.is_dir() and match(child.name):
            # deletes _pycache_ and all of its subdirectories, false flag notifies user of errors deleting
            shutil.rmtree(child, False)
            # != git is to ignore git folders as they shouldn't generate pycache
        elif child.is_dir() and child.name != ".git":
            rcache(child.resolve())
    return

def match(filename):
    lst = ["__pycache__", '.pytest_cache']

    for i in lst:
        if filename == i:
            return True
    return False

# usage
entries = Path('.')
rcache(entries)
