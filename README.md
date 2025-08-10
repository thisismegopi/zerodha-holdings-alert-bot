# zerodha-holdings-alert-bot

## 📋 Prerequisites

-   [UV](https://docs.astral.sh/uv/getting-started/installation/) Python package and project manager
-   Python 3.10 or higher

## 🛠️ Installation

1. **Clone this repository:**

    ```bash
    $ git clone https://github.com/thisismegopi/zerodha-holdings-alert-bot.git
    $ cd zerodha-holdings-alert-bot
    ```

2. **Install dependencies using uv:**

    ```bash
    $ uv sync
    ```

## 🛠️ Create Environment variable file (.env)

```env
API_KEY="" # Replace with your kite app API key
API_SECRET="" # Replace with your kite app secret API key key
REQUEST_TOKEN="" # Replace with your kite app request token generated from the login url
ACCESS_TOKEN="" # Replace with your kite app access token generated from the request token (used to make API calls)

# Telegram Bot Configuration
CHAT_ID=""  # Replace with your actual chat ID
TELEGRAM_BOT_TOKEN=""  # Replace with your actual bot token
```

## 🎮 Usage

```bash
$ uv run main.py
```
