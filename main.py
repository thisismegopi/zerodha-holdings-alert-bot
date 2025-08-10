import os
from dotenv import load_dotenv
import logging
from kiteconnect import KiteConnect
import schedule
import time
from datetime import datetime, timedelta
import requests

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
REQUEST_TOKEN = os.getenv("REQUEST_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


class Kite:
    def __init__(self, api_key, api_secret, request_token, access_token=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.request_token = request_token

        self.kite = KiteConnect(api_key=self.api_key)

        if access_token is not None:
            print("\nAccess token provided, setting it directly.")
            self.kite.set_access_token(access_token)
            print("\nKite Connect initialized with provided access token.")
            # print(f"\nAccess Token: {self.kite.access_token}")
        else:
            print(
                "\nNo access token provided, generating a new one using request token."
            )
            t = self.kite.generate_session(
                request_token=self.request_token, api_secret=self.api_secret
            )["access_token"]

            self.kite.set_access_token(t)
            print("\nKite Connect initialized successfully.")
            # print(f"\nAccess Token: {self.kite.access_token}")


class Job:
    def __init__(self, runner_function: callable):
        self.runner_function = runner_function
        self.schedule = schedule

    def schedule_market_jobs(self):
        start_time = datetime.strptime("09:15", "%H:%M")
        end_time = datetime.strptime("15:30", "%H:%M")
        current = start_time
        while current <= end_time:
            # Schedule the job every 30 minutes
            self.schedule.every().day.at(current.strftime("%H:%M")).do(
                self.runner_function
            )

            print(f"Scheduling job at {current.strftime('%H:%M')}")
            current += timedelta(minutes=30)

    def run(self):
        while True:
            self.schedule.run_pending()
            time.sleep(1)


kite = Kite(
    api_key=API_KEY,
    api_secret=API_SECRET,
    request_token=REQUEST_TOKEN,
    access_token=ACCESS_TOKEN,
)


def runner_function():
    print(f"Running task at {datetime.now().strftime('%H:%M:%S')}")
    holdings = kite.kite.holdings()

    sorted_holdings = sorted(
        holdings, key=lambda x: x["day_change_percentage"], reverse=True
    )
    top_5 = sorted_holdings[:5]  # Top 5 highest scoring
    bottom_5 = sorted_holdings[-5:]  # Last 5 lowest scoring

    text = f"Your holdings as of {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    text += "📈 *Top 5 Gainers* 📈\n\n"
    for holding in top_5:
        text += f"🟢 {holding['tradingsymbol']}: `{round(holding['day_change_percentage'], 2)}%`\n"

    text += "\n📉 *Top 5 Loosers* 📉\n\n"
    for holding in bottom_5:
        text += f"🔴 {holding['tradingsymbol']}: `{round(holding['day_change_percentage'], 2)}%`\n"

    data = requests.get(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}&parse_mode=Markdown"
    )
    if data.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {data.status_code}")


job = Job(runner_function=runner_function)
job.schedule_market_jobs()
job.run()
