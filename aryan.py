import telebot #Owner @team_sad001 Kuchh Bhi Chenge Kiya To Pakka Error Aayega Aur Phone Hack Ho Jayega 
import os
import random
from datetime import datetime, timedelta

TOKEN = '7762178800:AAEgqhx3_m5i0XEqxZ3vcc-hGlgTeArSja8'
OWNER_IDS = [5408005513]

bot = telebot.TeleBot(TOKEN)

KEYS_FILE = 'keys.txt'
USED_KEYS_FILE = 'used_keys.txt'

def is_user_authorized(user_id):
    if not os.path.exists(USED_KEYS_FILE):
        return False
    with open(USED_KEYS_FILE, 'r') as f:
        for line in f:
            try:
                record = eval(line.strip())
                if record['user_id'] == user_id:
                    if datetime.now() < datetime.fromisoformat(record['valid_until']):
                        return True
            except:
                continue
    return False

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('馃殌 Start Attack', '鉁� My Account')
    markup.row('馃攼馃攽 Buy Key', '馃毄 Trial')
    bot.send_message(message.chat.id, "*Welcome to Attack Bot!*", parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == '馃毄 Trial')
def trial(message):
    user_id = message.from_user.id
    if not is_user_authorized(user_id):
        expiry = datetime.now() + timedelta(minutes=10)
        with open(USED_KEYS_FILE, 'a') as f:
            f.write(f"{{'user_id': {user_id}, 'valid_until': '{expiry.isoformat()}', 'key': 'trial'}}\n")
        bot.send_message(message.chat.id, "*Trial activated for 10 minutes.*", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "*You already have access.*", parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == '鉁� My Account')
def my_account(message):
    user_id = message.from_user.id
    if is_user_authorized(user_id):
        bot.send_message(message.chat.id, "*Access: Active 鉁�*", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "*Access: Inactive 鉂�*\n\n*Buy Key to activate.*\n\n"
                                          "*KEY PRICE LIST* 馃攼\n"
                                          "鈴� 1 HOUR = 鈧�10\n"
                                          "鈴� 1 DAY = 鈧�99\n"
                                          "鈴� 7 DAYS = 鈧�399\n\n"
                                          "*Contact Owner 馃憠 @team_sad001*", parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == '馃攼馃攽 Buy Key')
def handle_buy_key(message):
    bot.send_message(message.chat.id,
                     "*KEY PRICE LIST* 馃攼\n"
                     "鈴� 1 HOUR = 鈧�10\n"
                     "鈴� 1 DAY = 鈧�99\n"
                     "鈴� 7 DAYS = 鈧�399\n\n"
                     "*Contact Owner 馃憠 @team_sad001 to buy key.*", parse_mode='Markdown')

@bot.message_handler(commands=['key'])
def generate_key(message):
    if message.from_user.id not in OWNER_IDS:
        bot.send_message(message.chat.id, "*Only owner can generate keys.*", parse_mode='Markdown')
        return

    parts = message.text.strip().split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.send_message(message.chat.id, "*Usage:* /key <amount>\nExample: /key 10", parse_mode='Markdown')
        return

    price = int(parts[1])
    duration = None
    if price == 10:
        duration = timedelta(hours=1)
    elif price == 99:
        duration = timedelta(days=1)
    elif price == 399:
        duration = timedelta(days=7)
    else:
        bot.send_message(message.chat.id, "*Invalid price. Use 10, 99, or 399.*", parse_mode='Markdown')
        return

    key = f"{price}-" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
    with open(KEYS_FILE, 'a') as f:
        f.write(f"{key}|{duration.total_seconds()}\n")
    bot.send_message(message.chat.id, f"*Key Generated:* `{key}`\n*Valid For:* {duration}", parse_mode='Markdown')

@bot.message_handler(commands=['redeem'])
def redeem_start(message):
    bot.send_message(message.chat.id, "*Send your key to activate:*", parse_mode='Markdown')
    bot.register_next_step_handler(message, process_redeem)

def process_redeem(message):
    user_id = message.from_user.id
    key_input = message.text.strip()

    if not os.path.exists(KEYS_FILE):
        bot.send_message(message.chat.id, "*No keys available.*", parse_mode='Markdown')
        return

    with open(KEYS_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    found = None
    for line in lines:
        if line.startswith(key_input):
            key, seconds = line.split('|')
            found = (key, float(seconds))
            break

    if not found:
        bot.send_message(message.chat.id, "*Invalid or already used key.*", parse_mode='Markdown')
        return

    # remove key
    with open(KEYS_FILE, 'w') as f:
        for line in lines:
            if not line.startswith(key_input):
                f.write(line + "\n")

    expiry = datetime.now() + timedelta(seconds=found[1])
    with open(USED_KEYS_FILE, 'a') as f:
        f.write(f"{{'user_id': {user_id}, 'valid_until': '{expiry.isoformat()}', 'key': '{key_input}'}}\n")

    bot.send_message(message.chat.id, "*Key redeemed successfully. Access granted!*", parse_mode='Markdown')

@bot.message_handler(commands=['cancelkey'])
def cancel_key(message):
    if message.from_user.id not in OWNER_IDS:
        bot.send_message(message.chat.id, "*Only owner can cancel keys.*", parse_mode='Markdown')
        return

    bot.send_message(message.chat.id, "*Send the redeemed key to cancel:*", parse_mode='Markdown')
    bot.register_next_step_handler(message, process_cancel_key)

def process_cancel_key(message):
    key = message.text.strip()
    if not os.path.exists(USED_KEYS_FILE):
        bot.send_message(message.chat.id, "*No keys redeemed yet.*", parse_mode='Markdown')
        return

    with open(USED_KEYS_FILE, 'r') as f:
        lines = f.readlines()

    with open(USED_KEYS_FILE, 'w') as f:
        for line in lines:
            if key not in line:
                f.write(line)

    bot.send_message(message.chat.id, f"*Key '{key}' cancelled successfully.*", parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == '馃殌 Start Attack')
def attack(message):
    user_id = message.from_user.id
    if not is_user_authorized(user_id):
        bot.send_message(message.chat.id,
                         "*Access Denied.* 鉂孿n\n"
                         "*KEY PRICE LIST* 馃攼\n"
                         "鈴� 1 HOUR = 鈧�10\n"
                         "鈴� 1 DAY = 鈧�99\n"
                         "鈴� 7 DAYS = 鈧�399\n\n"
                         "*Contact Owner 馃憠 @team_sad001 to buy key.*", parse_mode='Markdown')
        return

    bot.send_message(message.chat.id, "*Send Target IP:*", parse_mode='Markdown')
    bot.register_next_step_handler(message, get_ip)

def get_ip(message):
    ip = message.text.strip()
    bot.send_message(message.chat.id, "*Send Port:*", parse_mode='Markdown')
    bot.register_next_step_handler(message, get_port, ip)

def get_port(message, ip):
    port = message.text.strip()
    bot.send_message(message.chat.id, "*Send Duration (seconds):*", parse_mode='Markdown')
    bot.register_next_step_handler(message, confirm_attack, ip, port)

def confirm_attack(message, ip, port):
    duration = message.text.strip()
    username = message.from_user.first_name
    msg = (
        "*Attack started 馃挜馃Ж*\n\n"
        f"*User:* {username}\n"
        f"*Host:* {ip}\n"
        f"*Port:* {port}\n"
        f"*Time:* {duration} seconds\n\n"
        "Owner 馃憠 @team_sad001"
    )
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')

bot.polling()