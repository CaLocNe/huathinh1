#!/usr/bin/env python3
import os
import threading
import logging
from telegram import Update, BotCommand, MenuButtonCommands
from telegram.ext import Updater, CommandHandler, CallbackContext
from colorama import init as colorama_init, Fore, Style

# === CÀI ĐẶT LOGGING ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)
logging.getLogger('telegram').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)

# === INIT COLORAMA ===
colorama_init()

# === CẤU HÌNH TOKEN ===
TOKEN = '7942157317:AAHoV2G1b8EBCMR9YElezIlFmro9Zfq4E2I'

# === CHỨC NĂNG BOT ===

def clear_cmd(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        for i in range(message_id - 1, message_id - 20, -1):
            try:
                context.bot.delete_message(chat_id=chat_id, message_id=i)
            except:
                continue
    except Exception as e:
        print("Lỗi khi xoá:", e)

def mua_cmd(update: Update, context: CallbackContext):
    update.message.reply_text(
        "CÁC GÓI MOD SKIN\n"
        "7 Day - 29k\n"
        "15 Day - 49k\n"
        "Chọn Gói Muốn Mua (/7day hoặc /15day) Rồi Chuyển Khoản Qua Mã QR Được Gửi Để Nhận IP, Port.\n"
        "Sau Đó Gửi IDGame Cho @gthinhh Để Được Duyệt ID Vào Mod Nhé!"
    )

def day7_cmd(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    try:
        with open("7day.jpg", "rb") as photo:
            context.bot.send_photo(chat_id=chat_id, photo=photo, caption="Gói 7 ngày - 29k\nQuét mã QR để thanh toán nhé!")
    except Exception as e:
        update.message.reply_text("Không tìm thấy ảnh hoặc có lỗi xảy ra.")
        print("Lỗi gửi ảnh 7day:", e)

def day15_cmd(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    try:
        with open("15day.jpg", "rb") as photo:
            context.bot.send_photo(chat_id=chat_id, photo=photo, caption="Gói 15 ngày - 49k\nQuét mã QR để thanh toán nhé!")
    except Exception as e:
        update.message.reply_text("Không tìm thấy ảnh hoặc có lỗi xảy ra.")
        print("Lỗi gửi ảnh 15day:", e)

def start_cmd(update: Update, context: CallbackContext):
    user = update.effective_user.first_name
    update.message.reply_text(f"Xin Chào {user}!\nCảm Ơn Bạn Đã Ghé Thăm!!!")

def status_cmd(update: Update, context: CallbackContext):
    update.message.reply_text("Bot Đang Hoạt Động, Nhưng Chưa Có Chức Năng =)))")

def info_cmd(update: Update, context: CallbackContext):
    update.message.reply_text("Status: Hoạt Động\nVer: 0.1\nAuthor: GThinhh\nSupport: @gthinhh")

def help_cmd(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Danh Sách Lệnh\n"
        "/start   - Khởi Động Lại\n"
        "/status  - Trạng Thái Bot\n"
        "/help    - Hướng Dẫn\n"
        "/info    - Thông Tin Bot\n"
        "/clear   - Xoá Tin Nhắn\n"
        "/mua     - Mua Mod\n"
    )

# === HÀM IN STATUS TRÊN TERMINAL ===
def print_status(token, username, online):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"API: {token}")
    print(f"Username: {username}")
    if online:
        print(f"Status: {Fore.GREEN}ONLINE{Style.RESET_ALL} ⚡️")
    else:
        print(f"Status: {Fore.RED}OFFLINE{Style.RESET_ALL}")

# === MAIN ===
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_cmd))
    dp.add_handler(CommandHandler("status", status_cmd))
    dp.add_handler(CommandHandler("help", help_cmd))
    dp.add_handler(CommandHandler("info", info_cmd))
    dp.add_handler(CommandHandler("clear", clear_cmd))
    dp.add_handler(CommandHandler("mua", mua_cmd))
    dp.add_handler(CommandHandler("7day", day7_cmd))
    dp.add_handler(CommandHandler("15day", day15_cmd))

    me = updater.bot.get_me()
    username = me.username

    updater.bot.set_my_commands([
        BotCommand("start", "Khởi Động Lại"),
        BotCommand("status", "Trạng Thái Bot"),
        BotCommand("help", "Hướng Dẫn"),
        BotCommand("info", "Thông Tin Bot"),
        BotCommand("clear", "Xoá Tin Nhắn"),
        BotCommand("mua", "Mua Mod"),
        BotCommand("7day", "Gói 7 Ngày"),
        BotCommand("15day", "Gói 15 Ngày")
    ])
    updater.bot.set_chat_menu_button(menu_button=MenuButtonCommands(type="commands"))

    updater.start_polling()
    online = True
    print_status(TOKEN, username, online)

    try:
        while True:
            cmd = input().strip().lower()
            if cmd == "sp" and online:
                updater.stop()
                online = False
                print_status(TOKEN, username, online)
            elif cmd == "str" and not online:
                updater.start_polling()
                online = True
                print_status(TOKEN, username, online)
            elif cmd == "exit":
                break
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        if online:
            updater.stop()
        print_status(TOKEN, username, False)
        print("Bot đã dừng. Bye!")

if __name__ == "__main__":
    main()
