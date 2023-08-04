import telebot
from instaloader import Instaloader, Profile
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("bot_token")

bot = telebot.TeleBot(token)
L = Instaloader()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! I am an Instagram downloader bot. Send me an Instagram profile username. without '@', and I will send you their latest posts.")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    profile_name = message.text.strip()
    if not profile_name:
        bot.reply_to(message, 'Please enter a valid Instagram profile username.')
    else:
        try:
            profile = Profile.from_username(L.context, profile_name)
            send_num_posts_button(message.chat.id, profile_name)
        except Exception as e:
            bot.reply_to(message, f'Error: {str(e)}')

def send_num_posts_button(chat_id, profile_name):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('Set Number of Posts'))
    msg = bot.send_message(chat_id, f"Send me the number of posts you want to download from {profile_name}:",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, process_num_posts, profile_name)

def process_num_posts(message, profile_name):
    try:
        num_posts = int(message.text)
        if num_posts <= 0:
            bot.send_message(message.chat.id, 'Please enter a valid positive number for the post count.')
        else:
            bot.send_message(message.chat.id, "Please wait.......")
            download_posts(message.chat.id, profile_name, num_posts)
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid input. Please enter a valid number.')
    except Exception as e:
        bot.send_message(message.chat.id, f'Error: {str(e)}')

def download_posts(chat_id, profile_name, num_posts):
    try:
        profile = Profile.from_username(L.context, profile_name)
        posts_sorted_by_date = sorted(profile.get_posts(), key=lambda post: post.date_utc, reverse=True)
        selected_posts = posts_sorted_by_date[:num_posts]

        for post in selected_posts:
            media_url = None
            if post.typename == 'GraphImage':
                media_url = post.url
                bot.send_photo(chat_id, media_url, caption=post.caption)
            elif post.typename == 'GraphVideo':
                media_url = post.video_url
                bot.send_video(chat_id, media_url, caption=post.caption)
            elif post.typename == 'GraphSidecar':
                sidecar_children = post.get_sidecar_children()
                for child_post in sidecar_children:
                    media_url = None
                    if child_post.typename == 'GraphImage':
                        media_url = child_post.url
                        bot.send_photo(chat_id, media_url, caption=child_post.caption)
                    elif child_post.typename == 'GraphVideo':
                        media_url = child_post.video_url
                        bot.send_video(chat_id, media_url, caption=child_post.caption)

        bot.send_message(chat_id, f'Sent the latest {num_posts} posts from {profile_name}.')
        bot.send_message(chat_id, "𝙏𝙝𝙖𝙣𝙠𝙨 𝙛𝙤𝙧 𝙪𝙨𝙞𝙣𝙜 𝙤𝙪𝙧 𝙗𝙤𝙩\n Love you 💝 ")
    except Exception as e:
        bot.send_message(chat_id, f'Error: {str(e)}')

print('Bot Started!')
bot.infinity_polling()
