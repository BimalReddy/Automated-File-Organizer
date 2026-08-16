```markdown
# 📂 Automated File Organizer

A lightweight, real-time Python background utility that watches a designated folder (such as your `Downloads` directory) and automatically sorts incoming files into organized subfolders based on user-defined extension rules.

---

## ✨ Features

- **Real-Time Monitoring:** Uses OS-level events via the `watchdog` library to detect new files instantaneously.
- **Configurable Rules:** Define your own folder mappings via a simple `config.json` file—no code changes required.
- **Collision Resolution:** Automatically renames incoming duplicate files instead of overwriting your existing data.
- **Large File Ready:** Intelligently waits for large file transfers (like 4K videos or huge archives) to finish writing to the disk before attempting to move them.
- **Browser Download Safe:** Ignores partial browser download extensions until the transfer completely finishes.

---

## 🛠️ Project Structure

```text
automated_file_organizer/
├── src/
│   ├── __init__.py
│   ├── main.py             # CLI entry point
│   ├── watcher.py          # Watchdog file observer logic
│   ├── sorter.py           # Core file sorting and moving engine
│   └── config_parser.py    # JSON rule parser and validator
├── tests/
│   ├── __init__.py
│   ├── test_sorter.py
│   └── test_config.py
├── config.example.json    Configuration template
├── requirements.txt         Third-party dependencies
├── README.md               # Project documentation
└── .gitignore

```

---

## 🚀 Getting Started

### 1. Prerequisites

Make sure you have **Python 3.8+** installed on your system.

### 2. Installation

Clone the repository to your local machine and set up a virtual environment:

```bash
git clone [https://github.com/BimalReddy/Automated-File-Organizer.git](https://github.com/YOUR_USERNAME/Automated_
-File-Organizer.git)
cd automated_file_organizer

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### 3. Configuration

1. Copy the example configuration file to create your own:
```bash
cp config.example.json config.json

```


2. Open `config.json` in your favorite text editor and set your `watch_directory` path and preferred sorting categories:
```json
{
    "watch_directory": "/Users/yourname/Downloads",
    "default_folder": "Others",
    "rules": {
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "PDFs": [".pdf"],
        "Archives": [".zip", ".tar", ".gz"]
    }
}

```


*(Note: Remember to change the `watch_directory` path to match your actual folder path.)*

---

## 💻 Usage

Run the script from the project root using the configuration file:

```bash
python src/main.py -c config.json

```

The script will begin running in the foreground, outputting its actions to the console. To stop the organizer, simply press `Ctrl + C` in your terminal.

---