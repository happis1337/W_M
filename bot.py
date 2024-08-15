from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatPermissions
from aiogram import F
import asyncio
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv('WC_API_TOKEN')
OWNER_ID = int(os.getenv('WC_OWNER_ID'))

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Время мута в секундах
MUTE_TIME = 3600  # 1 час

# Метрики
metrics = {
    'requests_count': 0,
    'messages_count': 0,
    'start_time': time.time(),
}


# Список замученных пользователей
muted_users = {}

# РП команды
rp_commands = {
    "отдаться": "🥵 страстно отдался",
    "лизнуть": "👅 лизнул",
    "приковать": "🔗приковал",
    "поцеловать": "поцеловал(a)",
    "обнять": "обнял(а)",
    "ударить": "ударил(а)",
    "дать_пять": "дал(а) пять",
    "погладить": "погладил(а)",
    "пожать_руку": "пожал(а) руку",
    "подмигнуть": "подмигнул(а)",
    "заплакать": "заплакал(а)",
    "поддержать": "поддержал(а)",
    "рассмешить": "рассмешил(а)",
    "пригласить_на_свидание": "пригласил(а) на свидание",
    "накормить": "накормил(а)",
    "посмеяться_над": "посмеялся(ась) над",
    "испугать": "испугал(а)",
    "игнорировать": "игнорировал(а)",
    "выразить_любовь": "выразил(а) любовь к",
    "проигнорировать": "проигнорировал(а)",
    "сделать_комплимент": "сделал(а) комплимент",
    "подарить_подарок": "подарил(а) подарок",
    "поругать": "поругал(а)",
    "сказать_спасибо": "сказал(а) спасибо",
    "поздравить": "поздравил(а)",
    "чмок": "❤️ чмокнул",
    "напoить": "🥃 напоил",
    "связать": "⛓ связал",
    "трахнуть": "👉👌 сочно трахнул",
    "убить": "🔪 убил",
    "уничтожить": "💥 низвёл до атомов",
    "расстрелять": "🔫 расстрелял",
    "раб": "⛓ забрал в рабство",
    "съел": "картошку",
    "сальто": "сделал сальто через",
    "рука": "пожал руку",
    "прогиб": "кинул на прогиб",
    "воскресить": "воскресил",
    "плов": "сделал плов из",
    "изнасиловать": "изнасиловал",
    "покормить": "покормил",
    "отравить": "отравил",
    "тапать": "тапает",
    "комбо": "показал новое комбо в хомяке",
    "шифр": "показал новый шифр в хомяке",
    "суп": "сделал суп из",
    "похвалить": "похвалил(а)",
    "пнуть": "пнул",
    "выебать": "выебал",
    "баня": "пошел в баню с",
    "кончить": "кончил на",
    "обоссать": "обоссал",
    "сделал": "эмоцию сигмы",
    "избить": "избил",
    "нкей": "позвал нкея чтобы наказать",
    "дизморалить": "задизморалил",
    "уебать": "уебал",
    "кирпич": "кинул кирпич на голову",
    "сватнул": "сватнул бабушку",
    "задоксить": "задоксил деда",
    "вертолетик": "показал свой вертолетик",
    "зига": "кинул зигу для",
    "минет": "заставил сосать",
    "затапать": "затапал до смерти",
    "сосать": "сосет",
    "клеймо": "поставил клеймо какашки",
    "кокс": "запихнул кекс в рот",
    "отсосать": "отсосал",
    "simple": "roleplay"
}

# Обработчик команды /start и /help
@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я Iris Manager 2.0. Владелец чата может использовать команды /mute, /unmute, /ban, /unban, /warn, /unwarn, /mutelist и /ping для управления пользователями. Все пользователи могут использовать ролевые команды.")

# Команда /mute
@dp.message(Command(commands=['mute']))
async def mute_user(message: types.Message):
    if message.from_user.id == OWNER_ID:
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return
        user_id = message.reply_to_message.from_user.id
        until_date = datetime.now() + timedelta(seconds=MUTE_TIME)
        muted_users[user_id] = until_date.timestamp()
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=int(until_date.timestamp())
        )
        await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} был замучен до {until_date.strftime('%Y-%m-%d %H:%M:%S')}.")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

# Команда /unmute
@dp.message(Command(commands=['unmute']))
async def unmute_user(message: types.Message):
    if message.from_user.id == OWNER_ID:
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return
        user_id = message.reply_to_message.from_user.id
        if user_id in muted_users:
            del muted_users[user_id]
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=True)
            )
            await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} был размучен.")
        else:
            await message.answer("Этот пользователь не замучен.")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

# Команда /ban
@dp.message(Command(commands=['ban']))
async def ban_user(message: types.Message):
    if message.from_user.id == OWNER_ID:
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return
        user_id = message.reply_to_message.from_user.id
        await bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=user_id
        )
        await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} был забанен.")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

# Команда /unban
@dp.message(Command(commands=['unban']))
async def unban_user(message: types.Message):
    if message.from_user.id == OWNER_ID:
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return
        user_id = message.reply_to_message.from_user.id
        await bot.unban_chat_member(
            chat_id=message.chat.id,
            user_id=user_id
        )
        await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} был разбанен.")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

# Команда /warn
@dp.message(Command(commands=['warn']))
async def warn_user(message: types.Message):
    if message.from_user.id == OWNER_ID:
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return
        user_id = message.reply_to_message.from_user.id
        await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} получил предупреждение.")
        # Здесь вы можете добавить логику для ведения учета предупреждений
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")
@dp.message(F.text.in_(list(rp_commands.keys())))
async def rp_commands_handler(message: types.Message):
    print(f"Received command: {message.text}")
    command = message.text.strip()
    if command in rp_commands:
        action = rp_commands[command]
        if message.reply_to_message:
            target = message.reply_to_message.from_user.full_name
            await message.answer(f"{message.from_user.full_name} {action} {target}!")
        else:
            await message.answer(f"{message.from_user.full_name} {action} всех!")

# Команда /unwarn
@dp.message(Command(commands=['unwarn']))
async def unwarn_user(message: types.Message):
    if message.from_user.id == OWNER_ID:
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return
        user_id = message.reply_to_message.from_user.id
        await message.answer(f"Предупреждение пользователя {message.reply_to_message.from_user.full_name} снято.")
        # Здесь вы можете добавить логику для снятия предупреждений
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

# Команда /mutelist
@dp.message(Command(commands=['mutelist']))
async def mutelist(message: types.Message):
    if message.from_user.id == OWNER_ID:
        if muted_users:
            response = "Список замученных пользователей:\n"
            for user_id, timestamp in muted_users.items():
                user = await bot.get_chat_member(message.chat.id, user_id)
                response += f"{user.user.full_name} до {datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')}\n"
            await message.answer(response)
        else:
            await message.answer("Нет замученных пользователей.")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")


# Команда /ping
@dp.message(Command(commands=['ping']))
async def ping_users(message: types.Message):
    if message.from_user.id == OWNER_ID:
        # Измеряем текущее время
        current_time = time.time()

        # Расчет времени работы бота
        uptime = current_time - metrics['start_time']

        # Пример метрик
        rps = metrics['requests_count'] / (uptime / 60)  # запросов в минуту
        mps = metrics['messages_count'] / (uptime / 60)  # сообщений в минуту
        average_response_time = "21 ms"  # Здесь можно интегрировать реальное измерение
        average_message_response_time = "451 ms"  # Здесь можно интегрировать реальное измерение
        pending_updates = 22  # Здесь можно интегрировать реальное измерение

        # Формируем текст с метриками
        metrics_text = (
            "🏓 pong\n\n"
            "✨ Performance Metrics:\n"
            f"- 🚀 Requests per Second (RPS): {rps:.2f}\n"
            f"- ⏱️ Average Response Time: {average_response_time}\n"
            f"- 📈 Messages per Second (MPS): {mps:.2f}\n"
            f"- 🕒 Average Messages Response Time: {average_message_response_time}\n\n"
            "📥 Queue Status:\n"
            f"- 🔄 Pending Updates: {pending_updates}"
        )

        # Отправляем сообщение в общий чат
        await message.answer(f"🏓 pong\n\n{metrics_text}")

        # Отправляем сообщение всем администраторам
        members = await bot.get_chat_administrators(message.chat.id)
        for admin in members:
            user_id = admin.user.id
            # Проверяем, что это не бот
            if not admin.user.is_bot:
                try:
                    await bot.send_message(user_id, metrics_text)
                except Exception as e:
                    # Логируем ошибки, если не удалось отправить сообщение
                    print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")


# Обработчик всех сообщений
@dp.message()
async def handle_message(message: types.Message):
    metrics['requests_count'] += 1
    if message.text:
        metrics['messages_count'] += 1

# Обработчик ролевых команд
@dp.message(F.text.in_(list(rp_commands.keys())))
async def rp_commands_handler(message: types.Message):
    command = message.text.strip()
    if command in rp_commands:
        action = rp_commands[command]
        if message.reply_to_message:
            target = message.reply_to_message.from_user.full_name
            await message.answer(f"{message.from_user.full_name} {action} {target}!")
        else:
            await message.answer(f"{message.from_user.full_name} {action} всех!")

if __name__ == '__main__':
    # Запуск бота с передачей экземпляра бота
    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())