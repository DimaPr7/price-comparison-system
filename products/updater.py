from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command


def run_price_parser_job():
    print(f"[{datetime.now()}] Автоматический запуск парсера цен (интервал: 12 часов)...")
    try:
        # Программно вызываем вашу Django-команду parse_prices
        call_command("parse_prices")
    except Exception as e:
        print(f"[!] Ошибка при выполнении автоматического парсинга: {e}")


def start():
    scheduler = BackgroundScheduler()

    # Настройка запуска каждые 12 часов
    scheduler.add_job(run_price_parser_job, 'interval', hours=12)

    scheduler.start()
    print("[*] Фоновый планировщик цен успешно запущен. Интервал: каждые 12 часов.")
