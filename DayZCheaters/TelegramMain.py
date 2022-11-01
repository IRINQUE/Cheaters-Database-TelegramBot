# Самое важное(Импорты)
from email import message
from aiogram import *
import sqlite3
import time
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.types import InputMedia, ContentType, PreCheckoutQuery, successful_payment, ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from discord import VerificationLevel # Для States

# Прописываем данные
storage = MemoryStorage()
bot = Bot(token="5758494936:AAGtM5mI0mx1U79sZkrJFSreAsvXrpZhQ1c")
dp = Dispatcher(bot, storage=storage)
Database = "CheatersDatabase.db"
wait = 3
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,)

#Клавиатуры
ChooseMode = types.InlineKeyboardMarkup(row_width=2)
UserMode = types.InlineKeyboardButton("🎮 ИГРОК 🎮", callback_data="User")
AdminMode = types.InlineKeyboardButton("💻 АДМИН 💻", callback_data="Admin")
ChooseMode.add(UserMode, AdminMode)

Return = types.InlineKeyboardMarkup(row_width=1)
Back = types.InlineKeyboardButton("❌ ОТМЕНА ❌", callback_data="back")
Return.add(Back)

Cancel = types.InlineKeyboardMarkup(row_width=1)
CancelB = types.InlineKeyboardButton("❌ ОТМЕНА ❌", callback_data="cancel")
Cancel.add(CancelB)

MainMenuAdmin = types.InlineKeyboardMarkup()
CheckNickname = types.InlineKeyboardButton("🔎 ПРОВЕРИТЬ НИК", callback_data="checknickname")
CheckID = types.InlineKeyboardButton("🔎 ПРОВЕРИТЬ ID", callback_data="checkid")
AddCheater = types.InlineKeyboardButton("➕ ДОБАВИТЬ ЧИТЕРА", callback_data="addcheater")
GroupLink = types.InlineKeyboardButton("💭 БЕСЕДА", url="https://t.me/+ySkQY4LKT2szYmQy")
MainMenuAdmin.add(CheckNickname, CheckID)
MainMenuAdmin.add(AddCheater)
MainMenuAdmin.add(GroupLink)

MainMenu = types.InlineKeyboardMarkup()
CheckNickname = types.InlineKeyboardButton("🔎 ПРОВЕРИТЬ НИК", callback_data="checknickname")
CheckID = types.InlineKeyboardButton("🔎 ПРОВЕРИТЬ ID", callback_data="checkid")
GroupLink = types.InlineKeyboardButton("💭 БЕСЕДА", url="https://t.me/+ySkQY4LKT2szYmQy")
MainMenu.add(CheckNickname, CheckID)
MainMenu.add(GroupLink)


#States
class AddCheater(StatesGroup):
    SteamID = State()
    Nickname = State()

class Verefication(StatesGroup):
    Code = State()

class CheckNick(StatesGroup):
    Nickname = State()

class CheckID(StatesGroup):
    ID = State()

# Админ команды
@dp.message_handler(commands=["changepassword"])
async def editculture1(message: types.Message):
    args = message.get_args().split()
    connect = sqlite3.connect(Database)
    cursor = connect.cursor()
    password = cursor.execute("SELECT admin_password FROM data").fetchone()[0]
    if password == args[0]:
        cursor.execute("""UPDATE data SET admin_password = ?""", (args[1],))
        cursor.close()
        connect.commit()
        connect.close()
    else:
        print("Ошибка...")

@dp.message_handler(commands=["stats"])
async def editculture1(message: types.Message):
    args = message.get_args().split()
    connect = sqlite3.connect(Database)
    cursor = connect.cursor()
    users = cursor.execute("SELECT id FROM users").fetchall()
    cheaters =cursor.execute("SELECT id FROM cheaters").fetchall()
    cursor.close()
    connect.commit()
    connect.close()
    await bot.send_message(message.from_user.id, f"*В боте сейчас: {len(users)}\nОбнаружено читеров: {len(cheaters)}*", parse_mode="Markdown")

# Стартовое сообщение:
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    global message1
    user_name = types.User.get_current()
    connect = sqlite3.connect(Database)
    cursor = connect.cursor()
    check = cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (message.from_user.id,)).fetchall()
    # Если человека нет в базе данных
    if not bool(len(check)):
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (message.from_user.id,))
        cursor.execute("UPDATE users SET user_name = ? WHERE user_id = ?", (user_name['username'], message.from_user.id))
        cursor.close()
        connect.commit()
        connect.close()
        message1 = await bot.send_message(message.from_user.id, f"👋 Приветствуем, @{message.from_user.first_name}!\n\nБот *позволяет:*\n┏ Проверить *SteamID* игрока! _(Для всех)_\n┣ Позволяет проверить *игровой ник* _(Для всех)_\n┣ Внести *SteamID* в общую базу данных. _(Для Админов)_\n┣ Внести *Игровой Ник* в общую базу данных. _(Для Админов)_\n┣ Зайти в общую *беседу*! _(Для всех)_\n┗*Бот создан @irinquechannel*\n\n*Выберите режим бота:*", parse_mode="Markdown", reply_markup=ChooseMode)

    # Если роль человека - Игрок
    elif bool(len(check)) and cursor.execute("SELECT user_role FROM `users` WHERE `user_id` = ?", (message.from_user.id,)).fetchone()[0] == "User":
        role = cursor.execute("SELECT user_role FROM `users` WHERE `user_id` = ?", (message.from_user.id,)).fetchone()[0]
        usermessage = await bot.send_message(message.from_user.id, f"👋 *С возвращением*, @{message.from_user.first_name}!\nВаш статус: *Игрок*\n\n*Бот создан @irinquechannel*", parse_mode="Markdown")
        cursor.close()
        connect.commit()
        connect.close()
        await usermessage.edit_text("*ГЛАВНОЕ* МЕНЮ БОТА:\n\n┏*🔎 ПРОВЕРИТЬ НИК* - Проверка по *нику* _(Вводите ник точно)_\n┣*🔎 ПРОВЕРИТЬ ID* - Проверка по *SteamID*\n┗*💭 БЕСЕДА* - Беседа игроков *DayZ*", parse_mode="Markdown", reply_markup=MainMenu)


    # Если роль человека - Проверка
    elif bool(len(check)) and cursor.execute("SELECT user_role FROM `users` WHERE `user_id` = ?", (message.from_user.id,)).fetchone()[0] == "Verification":
        role = cursor.execute("SELECT user_role FROM `users` WHERE `user_id` = ?", (message.from_user.id,)).fetchone()[0]
        vermessage = await bot.send_message(message.from_user.id, f"👋 *С возвращением*, @{message.from_user.first_name}!\nВаш статус: *Проверка*\n\n*Бот создан @irinquechannel*", parse_mode="Markdown")
        cursor.close()
        connect.commit()
        connect.close()
        await vermessage.message.edit_text("*ГЛАВНОЕ* МЕНЮ БОТА:\n\n┏*🔎 ПРОВЕРИТЬ НИК* - Проверка по *нику* _(Вводите ник точно)_\n┣*🔎 ПРОВЕРИТЬ ID* - Проверка по *SteamID*\n┗*💭 БЕСЕДА* - Беседа игроков *DayZ*", parse_mode="Markdown", reply_markup=MainMenu)


    # Если роль человека - Админ
    elif bool(len(check)) and cursor.execute("SELECT user_role FROM `users` WHERE `user_id` = ?", (message.from_user.id,)).fetchone()[0] == "Admin":
        role = cursor.execute("SELECT user_role FROM `users` WHERE `user_id` = ?", (message.from_user.id,)).fetchone()[0]
        adminmessage = await bot.send_message(message.from_user.id, f"👋 *С возвращением*, @{message.from_user.first_name}!\nВаш статус: *Админ*\n\n*Бот создан @irinquechannel*", parse_mode="Markdown")
        cursor.close()
        connect.commit()
        connect.close()
        time.sleep(5)
        await adminmessage.edit_text(text='*АДМИН* МЕНЮ БОТА:\n\n┏*🔎 ПРОВЕРИТЬ НИК* - Проверка по *нику* _(Вводите ник точно)_\n┣*🔎 ПРОВЕРИТЬ ID* - Проверка по *SteamID*\n┣*➕ ДОБАВИТЬ ЧИТЕРА* - Заполнить *форму* и *Добавить* в БД\n┗*💭 БЕСЕДА* - Беседа игроков *DayZ*', parse_mode="Markdown", reply_markup=MainMenuAdmin)

@dp.callback_query_handler(lambda call: True)
async def calls(call, state: FSMContext):
    connect = sqlite3.connect(Database)
    cursor = connect.cursor()
    # Делаем статус Юзер
    if call.data == "User":
        cursor.execute("UPDATE users SET user_role = ? WHERE user_id = ?", ("User", call.from_user.id))
        cursor.close()
        connect.commit()
        connect.close()
        await call.message.edit_text("*ГЛАВНОЕ* МЕНЮ БОТА:\n\n┏*🔎 ПРОВЕРИТЬ НИК* - Проверка по *нику* _(Вводите ник точно)_\n┣*🔎 ПРОВЕРИТЬ ID* - Проверка по *SteamID*\n┗*💭 БЕСЕДА* - Беседа игроков *DayZ*", parse_mode="Markdown", reply_markup=MainMenu)
    # Делаем статус Админ
    if call.data == "Admin":
        cursor.execute("UPDATE users SET user_role = ? WHERE user_id = ?", ("Verification", call.from_user.id))
        cursor.close()
        connect.commit()
        connect.close()
        await call.message.edit_text("Для того, чтобы получить *права администратора*, нужно ввести *код*! _(Код можно получить, написав создателю и предоставив доказательства администрирования сервера)_\n\n*Введите код:*", parse_mode="Markdown", reply_markup=Return)
        await Verefication.Code.set()
        @dp.message_handler(content_types=['text'], state=Verefication.Code)
        async def check_messages(message: types.Message, state: FSMContext):
            connect = sqlite3.connect(Database)
            cursor = connect.cursor()
            password = cursor.execute("SELECT admin_password FROM data").fetchone()[0]
            if message.text == password:
                accept = await message.answer("✅ Код введен *Верно!*\n_(Доступ одобрен)_", parse_mode="Markdown")
                await state.finish()
                time.sleep(1)
                await accept.edit_text(text='*АДМИН* МЕНЮ БОТА:\n\n┏*🔎 ПРОВЕРИТЬ НИК* - Проверка по *нику* _(Вводите ник точно)_\n┣*🔎 ПРОВЕРИТЬ ID* - Проверка по *SteamID*\n┣*➕ ДОБАВИТЬ ЧИТЕРА* - Заполнить *форму* и *Добавить* в БД\n┗*💭 БЕСЕДА* - Беседа игроков *DayZ*', parse_mode="Markdown", reply_markup=MainMenuAdmin)
                cursor.execute("UPDATE users SET user_role = ? WHERE user_id = ?", ("Admin", call.from_user.id))
                cursor.close()
                connect.commit()
                connect.close()
                
        @dp.callback_query_handler(lambda call: True, state=Verefication)
        async def process_callback(call: types.CallbackQuery, state: FSMContext):
            if call.data == "back":
                connect = sqlite3.connect(Database)
                cursor = connect.cursor()
                await state.reset_state(with_data=False)
                await call.message.edit_text(f"👋 Приветствуем, @{call.from_user.first_name}!\n*Добро пожаловать* в моего бота!\n\nБот *позволяет:*\n┏ Проверить *SteamID* игрока! _(Для всех)_\n┣ Позволяет проверить *игровой ник* _(Для всех)_\n┣ Внести *SteamID* в общую базу данных. _(Для Админов)_\n┣ Внести *Игровой Ник* в общую базу данных. _(Для Админов)_\n┣ Зайти в общую *беседу*! _(Для всех)_\n┗*Бот создан @irinquechannel*\n\n*Выберите режим бота:*", parse_mode="Markdown", reply_markup=ChooseMode)
                cursor.execute("UPDATE users SET user_role = ? WHERE user_id = ?", ("None", call.from_user.id))
                cursor.close()
                connect.commit()
                connect.close()
                                        
    # ПРОВЕРКА НИКОВ И STEAM ID + ВНОС В БД
    if call.data == "addcheater":
        connect = sqlite3.connect(Database)
        cursor = connect.cursor()
        user_name = types.User.get_current()
        cursor.execute("INSERT INTO cheaters (reporter) VALUES (?)", (user_name["username"],))
        await AddCheater.SteamID.set()
        await call.message.edit_text("Введите *SteamID* читера: 📲", parse_mode="Markdown")
        cursor.close()
        connect.commit()
        connect.close()
        @dp.message_handler(content_types=['text'], state=AddCheater.SteamID)
        async def get_steamid(message: types.Message, state: FSMContext):
            connect = sqlite3.connect(Database)
            cursor = connect.cursor()
            cursor.execute("UPDATE cheaters SET steam_id = ? WHERE reporter = ?", (message.text, user_name['username']))
            await bot.send_message(message.from_user.id, "Введите *Никнейм* читера: 📝", parse_mode="Markdown")
            await AddCheater.next()
            cursor.close()
            connect.commit()
            connect.close()
        @dp.message_handler(content_types=['text'], state=AddCheater.Nickname)
        async def get_steamid(message: types.Message, state: FSMContext):
            connect = sqlite3.connect(Database)
            cursor = connect.cursor()
            cursor.execute("UPDATE cheaters SET nickname = ? WHERE reporter = ?", (message.text.lower(), user_name['username']))
            await bot.send_message(message.from_user.id, "Данные внесены *успешно!* ✅", parse_mode="Markdown")
            await state.finish()
            await message.answer('*АДМИН* МЕНЮ БОТА:\n\n┏*🔎 ПРОВЕРИТЬ НИК* - Проверка по *нику* _(Вводите ник точно)_\n┣*🔎 ПРОВЕРИТЬ ID* - Проверка по *SteamID*\n┣*➕ ДОБАВИТЬ ЧИТЕРА* - Заполнить *форму* и *Добавить* в БД\n┗*💭 БЕСЕДА* - Беседа игроков *DayZ*', parse_mode="Markdown", reply_markup=MainMenuAdmin)
            cursor.close()
            connect.commit()
            connect.close()

    # Проверка игрового никнейма
    if call.data == "checknickname":
        connect = sqlite3.connect(Database)
        cursor = connect.cursor()
        await bot.send_message(call.from_user.id, "Введите *никнейм* человека, которого нужно проверить 📠", parse_mode="Markdown")
        await CheckNick.Nickname.set()
        @dp.message_handler(content_types=['text'], state=CheckNick.Nickname)
        async def check_nickname(message: types.Message, state: FSMContext):
            result_id = cursor.execute("SELECT steam_id FROM cheaters WHERE nickname = ?", (message.text.lower(),)).fetchone()
            if bool(result_id):
                await bot.send_message(message.from_user.id, f"*Результаты Поиска:*\n➤ Игровой Никнейм: *{message.text}*\n➤ SteamID: *{result_id[0]}*\n➤ Результат: *Игрок - Читер ❌*", parse_mode="Markdown")
                await state.finish()
            else:
                await bot.send_message(message.from_user.id, f"*Результаты Поиска:*\n➤ Игровой Никнейм: *{message.text}*\n➤ SteamID: *Не найден*\n➤ Результат: *Игрок - Честный ✅*", parse_mode="Markdown")
                await state.finish()

    # Проверка SteamID
    if call.data == "checkid":
        connect = sqlite3.connect(Database)
        cursor = connect.cursor()
        await bot.send_message(call.from_user.id, "Введите *SteamID* человека, которого нужно проверить 📠", parse_mode="Markdown")
        await CheckID.ID.set()
        @dp.message_handler(content_types=['text'], state=CheckID.ID)
        async def check_id(message: types.Message, state: FSMContext):
            result_nickname = cursor.execute("SELECT nickname FROM cheaters WHERE steam_id = ?", (message.text,)).fetchone()
            result_steamid = cursor.execute("SELECT steam_id FROM cheaters WHERE nickname = ?", (message.text.lower(),)).fetchone()

            if bool(result_nickname):
                await bot.send_message(message.from_user.id, f"*Результаты Поиска:*\n➤ Игровой Никнейм: *{result_nickname[0]}*\n➤ SteamID: *{message.text}*\n➤ Результат: *Игрок - Читер ❌*", parse_mode="Markdown")
                await state.finish()
            else:
                await bot.send_message(message.from_user.id, f"*Результаты Поиска:*\n➤ Игровой Никнейм: *Не найден*\n➤ SteamID: *{message.text}*\n➤ Результат: *Игрок - Честный ✅*", parse_mode="Markdown")
                await state.finish()

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)