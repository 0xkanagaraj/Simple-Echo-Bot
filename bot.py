# Importing required modules
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Loading local module
from config import config
from helper import *

# Logging info
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Initializing the bot
BOT_ID = int(config.TOKEN.partition(":")[0])
bot = Bot(config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Router to handle updates
command_router = Router()
@command_router.message(Command('start'))
async def cmd_welcome(message: types.Message):
    await message.answer(
        f"Hi, *{message.from_user.full_name}*! 👋\n"
        "Welcome to Echo Bot!",
        parse_mode=ParseMode.MARKDOWN
    )
    return

message_router = Router()
@message_router.message()
async def cmd_echo(message: types.Message):
    try:
        # Handle text with formatting
        formatted_text=None
        if message.text or message.caption:
            content = message.text or message.caption
            entities = message.entities or message.caption_entities
            formatted_text = preserve_entities(content, entities)
                
        # Handle media with formatted caption
        if message.photo:
            await message.answer_photo(
                message.photo[-1].file_id,
                caption=formatted_text if formatted_text else None,
                parse_mode=ParseMode.HTML
            )
        elif message.video:
            await message.answer_video(
                message.video.file_id,
                caption=formatted_text if formatted_text else None,
                parse_mode=ParseMode.HTML
            )
        elif message.audio:
            await message.answer_audio(
                audio=message.audio.file_id,
                caption=formatted_text if formatted_text else None,
            )                    
        elif message.document:
            await message.answer_document(
                document=message.document.file_id,
                caption=formatted_text if formatted_text else None,
            ) 
        elif message.poll:
            await bot.send_poll(
                chat_id=message.chat.id,
                question=message.poll.question,
                options=[option.text for option in message.poll.options],
                is_anonymous=message.poll.is_anonymous,
                type=message.poll.type,  # 'regular' or 'quiz'
                allows_multiple_answers=message.poll.allows_multiple_answers,
                correct_option_id=message.poll.correct_option_id if message.poll.type == 'quiz' else None,
                explanation=message.poll.explanation if message.poll.type == 'quiz' else None,
                open_period=message.poll.open_period,
                close_date=message.poll.close_date
            )
        elif message.location:
            if message.location.live_period:  # Live location
                await message.answer_location(
                    latitude=message.location.latitude,
                    longitude=message.location.longitude,
                    live_period=message.location.live_period,
                    horizontal_accuracy=message.location.horizontal_accuracy,
                    heading=message.location.heading,
                    proximity_alert_radius=message.location.proximity_alert_radius
                )
            else:  # Static location
                await message.answer_location(
                    latitude=message.location.latitude,
                    longitude=message.location.longitude,
                    horizontal_accuracy=message.location.horizontal_accuracy
                )
        
        # Handle venue messages (locations with titles/addresses)
        elif message.venue:
            await message.answer_venue(
                latitude=message.venue.location.latitude,
                longitude=message.venue.location.longitude,
                title=message.venue.title,
                address=message.venue.address,
                foursquare_id=message.venue.foursquare_id,
                foursquare_type=message.venue.foursquare_type,
                google_place_id=message.venue.google_place_id,
                google_place_type=message.venue.google_place_type
            )
        # Handle non-text content
        elif message.sticker:
            await message.answer_sticker(
                message.sticker.file_id
            )
        elif message.voice:
            await message.answer_voice(
                message.voice.file_id
            )
        elif message.video_note:
            await message.answer_video_note(
                message.video_note.file_id
            )
        # Handle text only content 
        else:
            await message.answer(
                formatted_text,
                parse_mode=ParseMode.HTML
            )        
    except Exception as e:
        logger.error(f"Echo error: {e}")
        await message.answer("⚠️ Couldn't process this message")

# Polling
async def main():
    # Including router in dispatcher
    dp.include_router(command_router)
    dp.include_router(message_router)

    # Skip pending updates
    await bot.delete_webhook(drop_pending_updates=True)

    # Start polling
    await dp.start_polling(bot)

# Calls the main function when running the file
if __name__ == "__main__":
    asyncio.run(main())