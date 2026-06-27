import os
import random
TOKEN = os.getenv("TOKEN")

from datetime import datetime, timedelta, timezone
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ==========================
# НАСТРОЙКИ
# ==========================

MAPS = [
    "E-District",
    "Storm Point",
    "World's Edge"
]

ROTATION = timedelta(hours=4, minutes=30)

# UTC+3
MSK = timezone(timedelta(hours=3))

# Известная смена карт
REFERENCE_TIME = datetime(
    2026,
    6,
    27,
    11,
    0,
    tzinfo=MSK
)

# В этот момент активной стала первая карта из списка MAPS
REFERENCE_MAP_INDEX = 0


# ==========================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================

def get_current_rotation():
    now = datetime.now(MSK)
    delta = now - REFERENCE_TIME
    rotations = int(delta.total_seconds() // ROTATION.total_seconds())
    current_index = (REFERENCE_MAP_INDEX + rotations) % len(MAPS)
    last_change = REFERENCE_TIME + rotations * ROTATION
    next_change = last_change + ROTATION
    remain = next_change - now
    return (
        now,
        current_index,
        remain,
        next_change
    )

def format_timedelta(td):
    total = int(td.total_seconds())
    if total < 0:
        total = 0
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h}ч {m}м {s}с"

# ==========================
# КОМАНДА /карта
# ==========================

async def map_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now, current_index, remain, next_change = get_current_rotation()
    text = ""
    text += f"🗺 Текущая карта: {MAPS[current_index]}\n"
    text += f"⏳ До смены: {format_timedelta(remain)}\n\n"
    text += "📅 Дальнейшее расписание:\n"
    change = next_change
    for i in range(1, 7):
        idx = (current_index + i) % len(MAPS)
        text += (
            f"{change.strftime('%d.%m %H:%M')} — "
            f"{MAPS[idx]}\n"
        )
        change += ROTATION
    await update.message.reply_text(text)

# ==========================
# КОМАНДА /шиз
# ==========================

async def shiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    percent = random.randint(0, 100)
    if percent <= 19:
        emoji = "🥹"      # 0-19
    elif percent <= 39:
        emoji = "🥸"      # 20-39
    elif percent <= 59:
        emoji = "👺"      # 40-59
    elif percent <= 79:
        emoji = "💀"      # 60-79
    else:
        emoji = "🤡"      # 80-100

    await update.message.reply_text(
        f"🧠 Ты шиз на {percent}% {emoji}"
    )

# ==========================
# КОМАНДА /прайм
# ==========================

async def prime_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    percent = random.randint(0, 100)
    if percent <= 19:
        emoji = "👎"      # 0-19
    elif percent <= 39:
        emoji = "🤏"      # 20-39
    elif percent <= 59:
        emoji = "👍"      # 40-59
    elif percent <= 79:
        emoji = "✊"      # 60-79
    else:
        emoji = "💪"      # 80-100

    await update.message.reply_text(
        f"🔥 Ты в прайме на {percent}% {emoji}"
    )
    
# ==========================
# ЗАПУСК
# ==========================

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("map", map_command))
    app.add_handler(CommandHandler("shiz", shiz_command))
    app.add_handler(CommandHandler("prime", prime_command))
    app.run_polling()

if __name__ == "__main__":
    main()
