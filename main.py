import os
import telebot
import yt_dlp

# Создаем экземпляр бота и указываем ваш токен
proxy = "socks5://<proxy_host>:<proxy_port>"
bot = telebot.TeleBot("5752593949:AAE6ONLn15evOgMHkeg-ftX6GaS88hbx07s", proxy=proxy)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне ссылку на видео в VK для скачивания.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def download_video(message):
    # Получаем ссылку на видео из сообщения
    video_url = message.text

    # Проверяем, что ссылка ведет на VK
    # if "vk.com" not in video_url:
    #     bot.reply_to(message, "Неверная ссылка. Пожалуйста, отправьте ссылку на видео в VK.")
    #     return

    if "youtube.com" not in video_url:
        bot.reply_to(message, "Неверная ссылка. Пожалуйста, отправьте ссылку на видео в youtube.")
        return

    # Создаем объект yt-dlp
    ydl = yt_dlp.YoutubeDL()

    try:
        # Скачиваем видео
        info = ydl.extract_info(video_url, download=True)

        # Получаем путь к скачанному видео
        video_path = ydl.prepare_filename(info)

        # Отправляем видео пользователю
        with open(video_path, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file)

        # Удаляем скачанный файл
        os.remove(video_path)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при скачивании видео: {str(e)}")

# Запускаем бота
bot.polling()
