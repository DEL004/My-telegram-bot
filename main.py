import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = '8956516089:AAFnnPdxU__6zQWVYUyGxlqht7ve-PrIvfs'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("يامرحباااااا انا بوت من حبيبك عشان تكون حياتك اسهل \nارسلي رابط اي مقطع وبرسله لك بثواني")

async def download_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    # العبارة الجديدة التي تظهر فور إرسال الرابط
    status = await update.message.reply_text("ثواني ويجيك المقطع ياقلبي... ⏳")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'max_filesize': 50 * 1024 * 1024,
    }
    
    try:
        loop = asyncio.get_event_loop()
        def download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
                
        filename = await loop.run_in_executor(None, download)
            
        await status.edit_text("جاري إرسال المقطع لك... 📤")
        with open(filename, 'rb') as video:
            await update.message.reply_video(video=video, caption="تفضل المقطع الخاص بك! 🎉")
            
        os.remove(filename)
        await status.delete()
    except Exception as e:
        await status.edit_text("عذراً، تعذر تحميل المقطع. تأكد من أن الرابط صحيح أو أن حجم الفيديو لا يتجاوز 50 ميجابايت.")
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_and_send))
    print("البوت يعمل الآن بنجاح...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
  
