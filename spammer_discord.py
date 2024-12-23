import requests
import time
from datetime import datetime
from colorama import Fore, Style


# Токен аккаунта
TOKEN = "your_token_here"

# ID канала или ветки
CHANNEL_OR_THREAD_ID = "channel_id_here"

# URL для отправки сообщения
URL = f"https://discord.com/api/v9/channels/{CHANNEL_OR_THREAD_ID}/messages"

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

# Путь к файлу с сообщениями
MESSAGES_FILE = "messages.txt"

def load_messages(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            messages = [line.strip() for line in file if line.strip()]
        if not messages:
            raise ValueError("Файл с сообщениями пуст!")
        return messages
    except FileNotFoundError:
        print(f"{Fore.RED}[ОШИБКА]{Style.RESET_ALL} Файл {file_path} не найден.")
        exit(1)
    except ValueError as e:
        print(f"{Fore.RED}[ОШИБКА]{Style.RESET_ALL} {e}")
        exit(1)

# Функция отправки сообщения
def send_message(content):
    message = {"content": content}
    response = requests.post(URL, headers=HEADERS, json=message)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if response.status_code == 200:
        print(f"{Fore.GREEN}[УСПЕХ_ДАО]{Style.RESET_ALL} Сообщение отправлено: '{content}' в {current_time}")
    else:
        print(f"{Fore.RED}[ОШИБКА_ДАО]{Style.RESET_ALL} Код ошибки: {response.status_code}. Ответ: {response.text}")

# Основной цикл
def main():
    messages = load_messages(MESSAGES_FILE)
    for message in messages:
        send_message(message)
        time.sleep(31)  # Пауза 31 секунда между сообщениями, СМОТРИ ЗАДЕРЖКУ В КАНАЛЕ
    print("\nВсе сообщения отправлены. Скрипт завершен.")


# Запуск
if __name__ == "__main__":
    main()
