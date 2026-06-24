import os, threading, asyncio
from http.server import SimpleHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = '8956516089:AAE0dWLTIIv-ZKm6yRY0U0VsmU7Zev6-0j8'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل لي أي رابط مقطع وسأقوم بتحميله فوراً.")

async def download_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    status = await update.message.reply_text("ياقليبي جاري تحميل المقطع... ⏱️")
    
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
            # هنا التعديل بالعبارة الجديدة تحت المقطع مباشرة
            await update.message.reply_video(video=video, caption="تفضلي مقطعك ياعمري  👑❤️")
            
        os.remove(filename)
        await status.delete()
        
    except Exception as e:
        await status.edit_text("عذراً، حدث خطأ أثناء التحميل أو أن حجم الفيديو يتجاوز 50 ميجابايت.")
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_and_send))
    print("...البوت يعمل الآن بنجاح")
    
    # السيرفر الوهمي المدمج لتخطي فحص البورت في الخطة المجانية
    port = int(os.environ.get("PORT", 8000))
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler).serve_forever(), daemon=True).start()
    
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    
