import subprocess

def run_processes():
    python_files = ['Crawl.py', 'Load.py', 'Classify.py']

    # Run each Python file in sequence
    for file in python_files:
        try:
            print(f"Running {file}...")
            subprocess.run(['python', file], check=True)
            print(f"{file} executed successfully.\n")
        except subprocess.CalledProcessError as e:
            print(f"Error executing {file}: {e}")
            break

run_processes()