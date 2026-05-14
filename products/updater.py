from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command


def run_price_parser_job():
    print(f"[{datetime.now()}] Automatic price parser run (interval: 12 hours)...")
    try:
        call_command("parse_prices")
    except Exception as e:
        print(f"[!] Error during automatic parsing: {e}")


def start():
    scheduler = BackgroundScheduler()

    scheduler.add_job(run_price_parser_job, "interval", hours=12)

    scheduler.start()
    print("[*] Price scheduler started successfully. Interval: 12 hours.")