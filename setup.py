import os

folders = [
    "data/raw",
    "data/processed",
    "notebooks",
    "assets"
]

files = [
    "app.py",
    "requirements.txt",
    "README.md"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    with open(file, "w", encoding="utf-8") as f:
        if file == "README.md":
            f.write(
                "# Weathif: Local Climate Storyteller\n\n"
                "A Python-powered tool to simulate 'What If' local climate changes."
            )
        elif file == "requirements.txt":
            f.write(
                "pandas\nnumpy\nmatplotlib\nstreamlit\nrequests\ngeopandas\nrasterio\n"
            )
        else:
            f.write("")

print("✅ Project structure created.")
