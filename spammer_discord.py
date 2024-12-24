import requests
import time
from datetime import datetime
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

from manager_gpt import GptClient

# ID канала или ветки
#CHANNEL_OR_THREAD_ID = "1319450142914646069"

CHANNEL_OR_THREAD_ID = "1320853576221851686" 

# URL для отправки сообщения
URL = f"https://discord.com/api/v9/channels/{CHANNEL_OR_THREAD_ID}/messages"

# Путь к файлу с токенами
TOKENS_FILE = "tokens.txt"

# Путь к файлу с сообщениями
MESSAGES_FILE = "messages.txt"

# Прокси-сервер в формате login:password:ip:port (если используется)
PROXY = "user161722:e61ra0@146.247.105.132:7547"

# Настройка прокси для requests
proxies = {
    "http": f"http://{PROXY}",
    "https": f"http://{PROXY}",
}

# Интервал между сообщениями (в секундах)
MESSAGE_INTERVAL = 35


def load_tokens(file_path):
    """Загружает токены из файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            tokens = [line.strip() for line in file if line.strip()]
        if not tokens:
            raise ValueError("Файл с токенами пуст!")
        return tokens
    except FileNotFoundError:
        print(f"{Fore.RED}[ОШИБКА]{Style.RESET_ALL} Файл {file_path} не найден.")
        exit(1)
    except ValueError as e:
        print(f"{Fore.RED}[ОШИБКА]{Style.RESET_ALL} {e}")
        exit(1)


def load_messages(file_path):
    """Загружает сообщения из файла."""
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


def send_message(content, token):
    """Отправляет сообщение с указанным токеном."""
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    message = {"content": content}
    try:
        response = requests.post(URL, headers=headers, json=message, proxies=proxies)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if response.status_code == 200:
            print(f"{Fore.GREEN}[УСПЕХ_ДАО]{Style.RESET_ALL} Сообщение отправлено: '{content}' в {current_time}")
        else:
            print(f"{Fore.RED}[ОШИБКА_ДАО]{Style.RESET_ALL} Код ошибки: {response.status_code}. Ответ: {response.text}")
    except requests.exceptions.ProxyError as e:
        print(f"{Fore.RED}[ОШИБКА_ПРОКСИ]{Style.RESET_ALL} Проблема с прокси-сервером: {e}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[ОШИБКА_СЕТИ]{Style.RESET_ALL} Проблема с запросом: {e}")


def process_account(token, messages):
    """Отправляет все сообщения с одного аккаунта."""
    for i, message in enumerate(messages):
        print(f"{Fore.CYAN}[ИНФО]{Style.RESET_ALL} Отправка сообщения '{message}' с аккаунта {token[:10]}...")
        send_message(message, token)
        if i < len(messages) - 1:  # Таймер между сообщениями
            time.sleep(MESSAGE_INTERVAL)

def process_account_gpt(token, message):
    """Отправляет все сообщения с одного аккаунта."""
    print(f"{Fore.CYAN}[ИНФО]{Style.RESET_ALL} Отправка сообщения '{message}' с аккаунта {token[:10]}...")
    send_message(message, token)
    time.sleep(MESSAGE_INTERVAL)

import questionary

def main():
    """Основной цикл работы."""
    tokens = load_tokens(TOKENS_FILE)
    choice = questionary.select(
        "Выберите источник сообщений",
        choices=[
            "1. Из файла",
            "2. Генерация с помощью ChatGPT",
            "0. Выход",
        ],
        instruction="(Используйте стрелки для переключения)",
        pointer="🥎",
    ).ask()
    match choice.split(".")[0]:

        case "0":
            print("Выход из программы...")
            return  # Завершаем выполнение программы
        
        case "1":
            messages = load_messages(MESSAGES_FILE)
            print(f"Найдено {len(tokens)} аккаунтов и {len(messages)} сообщений из файла.")

            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = [
                    executor.submit(process_account, token, messages)
                    for token in tokens
                ]
                # Ждем завершения всех потоков
                for future in futures:
                    future.result()
        case "2":
            client = GptClient(role="assistant")
            #print("Введите количество сообщений: ")
            cur_count = 0
            count = int(input("Ввведите количество сообщений: "))
            for token in tokens:
                for i in range(count):
                    print(cur_count, count)
                    message = client.get_message() # Генерация одного сообщения
                    process_account_gpt(token, message)
                    cur_count += 1
                    time.sleep(15)
        # Создаем пул потоков для одновременной отправки
        case _:
            print("Выбран неизвестный вариант")


    print("\nВсе сообщения отправлены. Скрипт завершен.")
    return

# Запуск
if __name__ == "__main__":
    main()
