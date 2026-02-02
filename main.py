import logging
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, ContentType, ReplyKeyboardRemove

# -----------------------------------------------------
# SOZLAMALAR
# -----------------------------------------------------
# Siz yuborgan token
API_TOKEN = '8464907116:AAHwWKIwoB8jOGSbMxSRm_bFI7fle44UZic'

# DIQQAT: Bu yerga o'zingizning HTML faylingiz joylashgan manzilni qo'ying!
# Masalan: "https://sizning-loginingiz.github.io/test-bot/index.html"
WEB_APP_URL = "https://kxanifa.github.io/best-test" 

# Loggingni yoqish
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# -----------------------------------------------------
# MANTIQ: 50 ballik shkala (Faqat Grammatika)
# -----------------------------------------------------
def get_result_data(score):
    """
    50 ta savolga asoslangan baholash.
    """
    if 0 <= score <= 15:
        return "Beginner (A1)", "Start Grammarway 1"
    
    elif 16 <= score <= 30:
        return "Elementary (A2)", "Start Grammarway 2"
    
    elif 31 <= score <= 40:
        return "Pre-Intermediate (B1)", "Start Grammarway 3"
    
    elif 41 <= score <= 50:
        return "Intermediate (B2)", "Start Grammarway 4 / IELTS Foundation"
    
    else:
        return "Xatolik", "Noma'lum"

# -----------------------------------------------------
# HANDLERS
# -----------------------------------------------------

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Web App tugmasi
    web_app_info = WebAppInfo(url=WEB_APP_URL)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Tugma matni
    keyboard.add(KeyboardButton(text="🚀 Testni Boshlash", web_app=web_app_info))

    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}!\n\n"
        "Ingliz tili (Grammatika) darajangizni aniqlash uchun pastdagi tugmani bosing.\n"
        "Jami savollar soni: 50 ta.",
        reply_markup=keyboard
    )

@dp.message_handler(content_types=ContentType.WEB_APP_DATA)
async def answer_web_app(message: types.Message):
    try:
        # Web Appdan kelgan ma'lumotni o'qish
        raw_data = message.web_app_data.data
        data = json.loads(raw_data)
        
        # Ballni olish (HTML fayldan keladi)
        score = int(data.get('score', 0))
        # Jami savollar sonini 50 deb belgilaymiz
        total = int(data.get('total', 50))
        
        # Daraja va Tavsiyani aniqlash funksiyasini chaqirish
        level, action = get_result_data(score)
        
        # Foiz hisoblash
        percentage = (score / total) * 100

        # Natija matnini shakllantirish
        result_text = (
            f"✅ <b>TEST YAKUNLANDI</b>\n"
            f"➖➖➖➖➖➖➖➖➖➖\n"
            f"👤 <b>Foydalanuvchi:</b> {message.from_user.full_name}\n"
            f"📊 <b>Ball:</b> {score} / {total} ({percentage:.0f}%)\n"
            f"➖➖➖➖➖➖➖➖➖➖\n"
            f"🏆 <b>Daraja:</b> {level}\n"
            f"📚 <b>Tavsiya:</b> {action}\n"
        )

        # Javobni yuborish
        await message.answer(
            result_text, 
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )
        
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.answer("Natijani hisoblashda xatolik yuz berdi.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
