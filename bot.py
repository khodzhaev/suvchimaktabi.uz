from math import ceil
import requests
from aiogram import types, Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.filters.state import State, StatesGroup
import datetime

import json


SERVER_ADDRESS = "https://suvchimaktabi.uz/"
API_ADDRESS = SERVER_ADDRESS  + "api/"
CERTIFICATE_DOWNLOAD_ADDRESS = SERVER_ADDRESS + "media/certificate/"


TOKEN = "6139808892:AAF39RHY-hJw3ah6dsE3jOx5o-md1-EGwTQ"
CHANNEL_USERNAME= "suvchilar_maktabi"


def chunk(arr, size):
    return list(map(lambda x: arr[x * size:x*size+size], list(range(0, ceil(len(arr)/ size)))))


def request_server(addr, data):
    data = json.dumps(data)
    response = requests.post(API_ADDRESS + addr, data=data)

    return json.loads(response.json())


bot = Bot(TOKEN, parse_mode="html")
storage = RedisStorage2()
dp = Dispatcher(bot, storage=storage)


async def is_user_subscribed(user_id, channel_username):
        chat_member = await bot.get_chat_member(chat_id="@" + channel_username, user_id=user_id)
        if  chat_member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False



class Form(StatesGroup):
    phone = State()
    fio = State()
    region = State()
    district = State()
    birthday = State()
    gender = State()
    company = State()
    activity = State()
    job = State()




async def checker(response, state:FSMContext, chat_id, type=None, message_id=None):
    back_button = types.ReplyKeyboardMarkup(
                keyboard=[
                    [
                        types.KeyboardButton(text="🔙 Ортга")
                    ]
                ]
    , resize_keyboard=True)

    if response["status"] == "start":
        if response["student"]["phone"] is None or response["student"]["phone"] == '':
            text = "📱 <b>Raqam yuborish</b> tugmasini bosib raqamingini jo'nating"
            markup = types.ReplyKeyboardMarkup(keyboard=[
                [
                    types.KeyboardButton(text="📱 Raqam yuborish", request_contact=True)
                ]
            ], resize_keyboard=True)
            await Form.phone.set()


        elif response["student"]["fio"] is None or response["student"]["fio"] == '':

            text = "✍️ Ism Familyangizni F.I.SH formatda kiriting.\n Misol Uchun Azimov Azizbek Aziz o'g'li"
            markup = back_button

            await Form.fio.set()

        
        elif response["student"]["region"] is None or response["student"]["region"] == '':
            text = "📍 Viloyatingizni tanlang:"
            buttons = []
            for region in response["regions"]:
                buttons.append(
                    types.InlineKeyboardButton(text=region["title"], callback_data=f"selected_region_{region['id']}")
                )
            await Form.region.set()

            markup = types.InlineKeyboardMarkup(inline_keyboard=chunk([*buttons], 2))

        elif response["student"]["district"] is None or response["student"]["district"] == '':
            text = "📍 Tumaningizni tanlang:"
            buttons = []
            for region in response["districts"]:
                buttons.append(
                    types.InlineKeyboardButton(text=region["title"], callback_data=f"selected_district_{region['id']}")
                )
            await Form.district.set()

            markup = types.InlineKeyboardMarkup(inline_keyboard=chunk([*buttons], 2))


        elif response["student"]["birthday"] is None or response["student"]["birthday"] == '':
            text = "🗓 Tug'ilgan kuningizni <b>kun.oy.yil</b> formatida kiriting.\nMisol uchun: 20.02.1980"
            markup = back_button
            await Form.birthday.set()


        elif response["student"]["tgender"] is None or response["student"]["tgender"] == '':
            text = "Jinsingizni tanlang:"
            markup = types.InlineKeyboardMarkup(inline_keyboard=[
                [
                    types.InlineKeyboardButton(text="Эркак", callback_data="selected_gender_male")
                ],
                [
                    types.InlineKeyboardButton(text="Аёл", callback_data="selected_gender_female")
                ]
            ])
            await Form.gender.set()


        elif response["student"]["company"] is None or response["student"]["company"] == '':
            text = "🏢 Tashkilotingzni nomini kiriting:"
            markup = back_button
            await Form.company.set()


        elif response["student"]["job"] is None or response["student"]["job"] == '':
            text = "✍️ Tashkilotdagi lavozimingizni kiriting:"
            markup = types.InlineKeyboardMarkup(inline_keyboard=[
                [
                    types.InlineKeyboardButton(text="Хўжалик раҳбари", callback_data="selected_job_Хўжалик раҳбари")
                ],
                [
                    types.InlineKeyboardButton(text="Ишчи", callback_data="selected_job_Ишчи")
                ],
            ])
            await Form.job.set()

        elif response["student"]["activity"] is None or response["student"]["activity"] == '':
            text = "📄 Tashkilotingiz faoliyat turini tanlang:"
            markup = types.InlineKeyboardMarkup(inline_keyboard=[
                [
                    types.InlineKeyboardButton(text="Пахтачилик/Ғаллачилик", callback_data="selected_activty_Пахтачилик/Ғаллачилик")
                ],
                [
                    types.InlineKeyboardButton(text="Боғдорчилик/Узумчилик", callback_data="selected_activty_Боғдорчилик/Узумчилик")
                ],
                [
                    types.InlineKeyboardButton(text="Сабзавот/Полиз", callback_data="selected_activty_Сабзавот/Полиз")
                ],
                [
                    types.InlineKeyboardButton(text="Сабзавотлар/ғаллачилик", callback_data="selected_activty_Сабзавотлар/ғаллачилик")
                ],
                [
                    types.InlineKeyboardButton(text="Бошқа ёналиш", callback_data="selected_activty_Бошқа ёналиш")
                ]
            ])
            await Form.activity.set()



    elif response["status"] == "end":
        await state.finish()
        text = f"👤 <b>{response['student']['fio']}</b>\n"
        text += f"🆔 {response['student']['id']}\n"
        text += f"📞 {response['student']['phone']}\n"
        text += f"📍 {response['student']['region']['title']}, {response['student']['district']['title']}\n"
        text += f"🗓 {response['student']['birthday']}\n\n"
        markup = types.ReplyKeyboardRemove(selective=True)

    
    if type == 'inline':
        await bot.delete_message(chat_id, message_id)

    await bot.send_message(chat_id, text, reply_markup=markup)


@dp.message_handler(commands=["start"], state='*')
async def start(message: types.Message, state:FSMContext):
    chat_id = message.from_user.id


    if await is_user_subscribed(chat_id, CHANNEL_USERNAME):
        response = request_server("user/", data={"telegram_id": chat_id})
        await state.finish()

        await checker(response, state, chat_id)


    else:
        markup = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Kanalga o'tish", url="https://t.me/"+ CHANNEL_USERNAME)
            ], 
            [
                types.InlineKeyboardButton(text="Obunalikni tekshirish", callback_data="check_subscription")
            ], 
        ])
        await bot.send_message(chat_id, "Botdan foydalanish uchun avvaliga kanalimizga obuna bo'ling", reply_markup=markup)


@dp.message_handler(text="🔙 Ortga", state='*')
async def answer_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    if await is_user_subscribed(chat_id, CHANNEL_USERNAME):
        state_name = str(await Form.previous()).replace("Form:", "")
        response = request_server("answer/", {"telegram_id": chat_id, "field": f"{state_name}", "value": None})
        await checker(response, state, chat_id)
    
    else:
        text = "Botdan foydalanish uchun avvaliga kanalimizga obuna bo'ling"
        markup = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Kanalga o'tish", url="https://t.me/"+ CHANNEL_USERNAME)
            ], 
            [
                types.InlineKeyboardButton(text="Obunalikni tekshirish", callback_data="check_subscription")
            ], 
        ])

        await bot.send_message(chat_id, text, reply_markup=markup)


@dp.message_handler(content_types=["contact"], state=Form.phone)
async def check_subscription(message: types.Message, state:FSMContext):
    chat_id = message.from_user.id
    
    if await is_user_subscribed(chat_id, CHANNEL_USERNAME):
        phone_number = message.contact.phone_number.replace("+", '')
        if phone_number.startswith('998'):
            response = request_server("answer/", {"telegram_id": chat_id, "field": "phone", "value": phone_number})
        
            await state.finish()
            text = "⏳ Iltimos kuting..."
            markup = types.ReplyKeyboardRemove(selective=True)
            await bot.send_message(chat_id, text, reply_markup=markup)
            await checker(response, state, chat_id)

        else:
            text = f"❌ Notogri raqam formati! Iltimos qaytadan urinib ko'ring."
            await bot.send_message(chat_id, text)
            await checker(response, state, chat_id)




@dp.message_handler(content_types=["text"], state=Form.fio)
async def answer_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    
    if await is_user_subscribed(chat_id, CHANNEL_USERNAME):
        fullname = message.text
        try: 
            first_name = fullname.split(" ")[0]
            last_name = fullname.split(" ")[1]
            response = request_server("answer/", {"telegram_id": chat_id, "field": "fio", "value": fullname})
            await state.finish()
            await checker(response, state, chat_id)
            
        except IndexError:
            await bot.send_message(chat_id, "❌ Ism Familyangizni F.I.SH formatda kiriting.\n Misol Uchun Azimov Azizbek Aziz o'g'li")


    else:
        text = "Botdan foydalanish uchun avvaliga kanalimizga obuna bo'ling"
        markup = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Kanalga o'tish", url="https://t.me/"+ CHANNEL_USERNAME)
            ], 
            [
                types.InlineKeyboardButton(text="Obunalikni tekshirish", callback_data="check_subscription")
            ], 
        ])

        await bot.send_message(chat_id, text, reply_markup=markup)




@dp.callback_query_handler(lambda callback_query: callback_query.data == 'check_subscription')
async def check_subscription(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.from_user.id
    
    if await is_user_subscribed(chat_id, CHANNEL_USERNAME):
        response = request_server("user/", data={"telegram_id": chat_id})
        await checker(response, state, chat_id, 'inline', callback_query.message.message_id)


    else:    
        await bot.answer_callback_query(callback_query.id, "❗️ Siz hali kanalga obuna bo'lmadingiz", show_alert=True)
        


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'check_sertificat')
async def check_subscription(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.from_user.id
    
    if await is_user_subscribed(chat_id, CHANNEL_USERNAME):
        response = request_server("sertificate/", data={"telegram_id": chat_id})

        if response["file_path"]:
            try:
                file = types.InputFile(response["file_path"])
                await bot.send_document(chat_id,  document=file)
            except FileNotFoundError:
                await bot.answer_callback_query(callback_query.id, "⏳ O'quv kursi hali yakunlanmagan\n O'quv kurs yakunlangandan so'ng sertifikatingizni yuklab olishingiz mumkin", show_alert=True)

                
                
        else: 
            await bot.answer_callback_query(callback_query.id, "⏳ O'quv kursi hali yakunlanmagan\n O'quv kurs yakunlangandan so'ng sertifikatingizni yuklab olishingiz mumkin", show_alert=True)

    else:    
        await bot.answer_callback_query(callback_query.id, "❗️ Siz hali kanalga obuna bo'lmadingiz", show_alert=True)
        



@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('selected_region_'), state=Form.region)
async def check_subscription(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.from_user.id
    region_id = callback_query.data.replace("selected_region_", "")

    if await is_user_subscribed(chat_id, CHANNEL_USERNAME):
        response = request_server("answer/", {"telegram_id": chat_id, "field": "region_id", "value": region_id})

        await state.finish()
        await checker(response, state, chat_id, 'inline', callback_query.message.message_id)


    else:    
        await bot.answer_callback_query(callback_query.id, "❗️ Siz hali kanalga obuna bo'lmadingiz", show_alert=True)
        

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('selected_district_'), state=Form.district)
async def check_subscription(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.from_user.id
    district_id = callback_query.data.replace("selected_district_", "")

    if await is_user_subscribed(chat_id, CHANNEL_USERNAME):
        response = request_server("answer/", {"telegram_id": chat_id, "field": "district_id", "value": district_id})

        await state.finish()
        await checker(response, state, chat_id, 'inline', callback_query.message.message_id)


    else:    
        await bot.answer_callback_query(callback_query.id, "❗️ Siz hali kanalga obuna bo'lmadingiz", show_alert=True)


@dp.message_handler(content_types=["text"], state=Form.birthday)
async def answer_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    if await is_user_subscribed(chat_id, CHANNEL_USERNAME):
        try: 
            date_format = "%d.%m.%Y"
            date_object = datetime.datetime.strptime(message.text, date_format)
            response = request_server("answer/", {"telegram_id": chat_id, "field": "birthday", "value": message.text})
            await state.finish()
            await checker(response, state, chat_id)

        except ValueError:
            response = request_server("user/", data={"telegram_id": chat_id})
            await checker(response, state, chat_id)
            

        
    else:
        text = "Botdan foydalanish uchun avvaliga kanalimizga obuna bo'ling"
        markup = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Kanalga o'tish", url="https://t.me/"+ CHANNEL_USERNAME)
            ], 
            [
                types.InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subscription")
            ], 
        ])

        await bot.send_message(chat_id, text, reply_markup=markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('selected_gender_'), state=Form.gender)
async def check_subscription(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.from_user.id
    gender = callback_query.data.replace("selected_gender_", "")

    if await is_user_subscribed(chat_id, CHANNEL_USERNAME):
        response = request_server("answer/", {"telegram_id": chat_id, "field": "tgender", "value": gender})

        await state.finish()
        await checker(response, state, chat_id, 'inline', callback_query.message.message_id)


    else:    
        await bot.answer_callback_query(callback_query.id, "❗️ Siz hali kanalga obuna bo'lmadingiz", show_alert=True)
        


@dp.message_handler(content_types=["text"], state=Form.company)
async def answer_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    if await is_user_subscribed(chat_id, CHANNEL_USERNAME):
        response = request_server("answer/", {"telegram_id": chat_id, "field": "company", "value": message.text})
        await state.finish()
        await checker(response, state, chat_id)
        

    
    else:
        text = "Botdan foydalanish uchun avvaliga kanalimizga obuna bo'ling"
        markup = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Kanalga o'tish", url="https://t.me/"+ CHANNEL_USERNAME)
            ], 
            [
                types.InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subscription")
            ], 
        ])

        await bot.send_message(chat_id, text, reply_markup=markup)






@dp.callback_query_handler(lambda callback: callback.data.startswith("selected_job_"), state=Form.job)
async def answer_handler(callback: types.CallbackQuery, state: FSMContext):
    chat_id =callback.message.chat.id
    value = callback.data.replace("selected_job_", "")

    if await is_user_subscribed(chat_id, CHANNEL_USERNAME):
        response = request_server("answer/", {"telegram_id": chat_id, "field": "job", "value": value})
        await state.finish()
        await checker(response, state, chat_id, 'inline', callback.message.message_id)
        

    
    else:
        text = "Botdan foydalanish uchun avvaliga kanalimizga obuna bo'ling"
        markup = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Kanalga o'tish", url="https://t.me/"+ CHANNEL_USERNAME)
            ], 
            [
                types.InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subscription")
            ], 
        ])

        await bot.send_message(chat_id, text, reply_markup=markup)
        

@dp.callback_query_handler(lambda callback: callback.data.startswith("selected_activty_"), state=Form.activity)
async def answer_handler(callback: types.CallbackQuery, state: FSMContext):
    chat_id =callback.message.chat.id
    value = callback.data.replace("selected_activty_", "")

    if await is_user_subscribed(chat_id, CHANNEL_USERNAME):
        response = request_server("answer/", {"telegram_id": chat_id, "field": "activity", "value": value})
        await state.finish()
        await checker(response, state, chat_id, 'inline', callback.message.message_id)
        

    
    else:
        text = "Botdan foydalanish uchun avvaliga kanalimizga obuna bo'ling"
        markup = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Kanalga o'tish", url="https://t.me/"+ CHANNEL_USERNAME)
            ], 
            [
                types.InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subscription")
            ], 
        ])

        await bot.send_message(chat_id, text, reply_markup=markup)




executor.start_polling(dp, skip_updates=True)
