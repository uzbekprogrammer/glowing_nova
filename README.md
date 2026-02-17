# 🇺🇿 Uzbekistan Region Bot

A professional Telegram Bot built with Python to facilitate user submissions based on regional data of Uzbekistan. This bot features an interactive selection flow for Regions and Districts, followed by a secure file upload system.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Aiogram](https://img.shields.io/badge/Aiogram-3.x-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![SQLite](https://img.shields.io/badge/SQLite-Async-green)

## ✨ Features

- **Interactive Selection**: User-friendly Inline Keyboards to select from all 14 administrative regions and their districts in Uzbekistan.
- **State Management**: Robust FSM (Finite State Machine) to guide users through the submission process step-by-step.
- **File Handling**: Securely accepts Documents and Photos, saving them with unique identifiers to prevent overwriting.
- **Database Integration**: Asynchronous SQLite database (via SQLAlchemy) to store submission metadata.
- **Clean Architecture**: Modular code structure separating handlers, states, data, and database logic.
- **Logging**: Comprehensive logging for monitoring and debugging.

## 🛠 Tech Stack

- **Framework**: [aiogram 3.x](https://docs.aiogram.dev/en/latest/) (Asynchronous framework for Telegram Bot API)
- **Database ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (AsyncIO support)
- **Database Driver**: [aiosqlite](https://github.com/omnilib/aiosqlite)
- **Environment Management**: [python-dotenv](https://github.com/theskumar/python-dotenv)

## 🚀 Getting Started

Follow these steps to set up and run the bot locally.

### Prerequisites

- Python 3.10 or higher
- A Telegram Bot Token (get it from [@BotFather](https://t.me/BotFather))

### Installation

1.  **Clone the repository** (if using git):
    ```bash
    git clone <repository_url>
    cd glowing-nova
    ```

2.  **Create a virtual environment**:
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  Create a `.env` file in the root directory.
2.  Add your Bot Token:

    ```env
    BOT_TOKEN=123456789:ABCdefGhIjkLmNoPqRsTuVwXyZ
    ```

## 🏃‍♂️ Usage

1.  **Run the bot**:
    ```bash
    python main.py
    ```

2.  **Interact with the bot**:
    - Open your bot in Telegram.
    - Send `/start`.
    - Select a **Region**.
    - Select a **District**.
    - Upload a **File** (Photo or Document).
    - Receive a confirmation message!

## 📂 Project Structure

```
glowing-nova/
├── data/
│   └── locations.py       # Helper data: Regions and Districts
├── database/
│   ├── core.py            # Database engine and session setup
│   └── models.py          # SQLAlchemy models (UserSubmission)
├── handlers/
│   └── submission.py      # Bot command and callback handlers
├── states/
│   └── submission.py      # FSM State definitions
├── uploads/               # Directory where user files are saved
├── .env                   # Environment variables (Token)
├── .gitignore             # Git ignore file
├── main.py                # Entry point of the application
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## 📄 Database

The bot automatically creates a `bot.db` SQLite database file in the root directory upon first run.
The `user_submissions` table stores:
- `id`
- `user_id`
- `region`
- `district`
- `file_name`
- `file_path`
- `timestamp`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open-source and available for use.
