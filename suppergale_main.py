# suppergalebot #

import json
import requests
import time
import random
import telegram
from bs4 import BeautifulSoup
import feedparser as fp

# counters for thankshelene
PREV = time.time()
NOW = 0
DIFF = 0

TOKEN = '<token>' #insert token here
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Poll
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# UTILITY #

def start(update,context):
  update.message.reply_text("I'm alive! Use /help to find out what I can do.")

def ping(update, context):
    update.message.reply_text("pong! 🏓")

def list(update,context):
  update.message.reply_text("Currently available commands\n"

                          "\nMemes:\n"
                          "• /rand\n"
                          "• /thankshelene\n"
                          "• /announcement\n"
                          "• /samsays\n"
                          
                          "\nMore Memes:\n"
                          "• /cat\n"
                          "• /kermit\n"
                          "• /pikachu\n"
                          "• /parrot\n"
                          "• /hamster\n"
                          "• /patrick\n"
                          "• /radio\n"
                          
                          "\nOtouto clones:\n"
                          "• /8ball\n"
                          "• /xkcd <comic number>\n"
                          "• /set <seconds> <message>\n"
                          
                          "\nUtility:\n"
                          "• /start\n"
                          "• /ping\n"
                          "• /help")

def redblack(update, context):
    question = "Red / Black"
    options= ["Red","Black"]
    keyboard = [[InlineKeyboardButton("Close round", callback_data='Close')]]
    context.bot.send_poll(chat_id=update.effective_chat.id,
                          question=question,
                          options=options,
                          is_anonymous=True,
                          allows_multiple_answers=False,
                          reply_markup=InlineKeyboardMarkup(keyboard),
                          is_closed=False,
                          disable_notification=True,
                          )

# helper function - redblack callback queries
def Button(update,context):
    query = update.callback_query

    if (query.data == "Close"):
        keyboard = [[InlineKeyboardButton("RESET", callback_data='Reset')]]
        context.bot.stop_poll(chat_id=update.effective_chat.id,
                              message_id=update.effective_message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard)
                              )
        query.answer()

    elif (query.data == "Reset"):
        update.effective_message.delete()
        question = "Red / Black"
        options= ["Red","Black"]
        keyboard = [[InlineKeyboardButton("Close round", callback_data='Close')]]
        update.effective_chat.send_poll(question=question,
                                        options=options,
                                        is_anonymous=True,
                                        allows_multiple_answers=False,
                                        reply_markup=InlineKeyboardMarkup(keyboard),
                                        is_closed=False,
                                        disable_notification=True,
                                        )
        query.answer()


# MEMES #

def rand(update,context):
    update.message.reply_sticker(random.choice(stickerIDlist))

stickerIDlist = ['CAACAgUAAxkBAAEBYsVfccjron2sngX2P_ESrzdMphqBsAACXgADIpOQBdu6gyOzY5faGwQ',
                'CAACAgUAAxkBAAEBYtRfcc58s4e4XkH7cUX87AFSgYLItQACXwADIpOQBZvGve4yh9uKGwQ',
                'CAACAgUAAxkBAAEBYtZfcc5_qKtfbazStr3mpWovfeCjNgACYAADIpOQBXhETHv-cczFGwQ',
                'CAACAgUAAxkBAAEBYthfcc6BdNfl_v8Pdw6fdpuf6A-ajAACYQADIpOQBT9bCq9JxwmsGwQ',
                'CAACAgUAAxkBAAEBYtpfcc7mMEy0EsUGjKyTfcXTJc_FqgACYgADIpOQBd-Ld4RQMiasGwQ',
                'CAACAgUAAxkBAAEBYtxfcc8GuIHF03SfKCb14IUI_S1qiwACYwADIpOQBVyzzNu3OdOvGwQ',
                'CAACAgUAAxkBAAEBYt5fcc8RpHh9kmuxXMJKOkQSYBHL-wACZAADIpOQBV3cXZwXEJeWGwQ',
                'CAACAgUAAxkBAAEBYuBfcc8TDQ_M2P6hG2iWCNSJ353BqwACZQADIpOQBVhMK5vv0Mv2GwQ',
                'CAACAgUAAxkBAAEBYuJfcc8saEGh0I3asnrjQqmI0-d0rAACZgADIpOQBVA-n-qeTLqsGwQ',
                'CAACAgUAAxkBAAEBYuRfcc8tp9Mn0rFYas4ilgABnqb6wNAAAmcAAyKTkAX1IFpS6DWjXxsE',
                'CAACAgUAAxkBAAEBYuVfcc8uVvZ2hOH1g2FNC4JokNnvzQACaAADIpOQBRO2dMwgHtjrGwQ',
                'CAACAgUAAxkBAAEBYudfcc8wFlRKnXBWaJ54TDOk0C8TcQACaQADIpOQBePWXS2eVVdlGwQ',
                'CAACAgUAAxkBAAEBYupfcc9TMTRRa4M6wU_mMxHgVuvyvgACagADIpOQBQ6oDiceO1y7GwQ',
                'CAACAgUAAxkBAAEBYutfcc9UCT9GqOVbGrdjPIq2k1NW4QACawADIpOQBSb1QFrF36fSGwQ',
                'CAACAgUAAxkBAAEBYu5fcc9Wrf5MUWmo2PeEJa_0CJ0ooAACbAADIpOQBVxBkTksrLtKGwQ',
                'CAACAgUAAxkBAAEBYu9fcc9XyVwrXoZCEe7WywQ7aJsp_wACbQADIpOQBbXg8nB9BEi7GwQ',
                'CAACAgUAAxkBAAEBYvJfcc9aETTaj184u8qEJgaOwqgk0gACbgADIpOQBUKWnVklaITwGwQ',
                'CAACAgUAAxkBAAEBYvNfcc9bp_y8PcPyCssK6iJPK2pdDgACbwADIpOQBYO8AZOcNHf7GwQ',
                'CAACAgUAAxkBAAEBYvRfcc9b-oR3A2Hg5Im5f8gEx64g6QACcAADIpOQBbSeEI2LV4OkGwQ',
                'CAACAgUAAxkBAAEBYvVfcc9bXLmpO4hzmqSvkFTq94hP9AACcQADIpOQBd5i00GdU8XtGwQ',
                'CAACAgUAAxkBAAEBYvpfcc9gFzNuMwUiha5PiX4m--7iUgACcgADIpOQBRzDuCD-tZlTGwQ',
                'CAACAgUAAxkBAAEBYvtfcc9gOE_U36UbrducqkeQbJ0_3AACcwADIpOQBUpq93J6F0nKGwQ',
                'CAACAgUAAxkBAAEBYx9fceX5_sEWpP2GsanW74fI9i7LowACdAADIpOQBXCXEW0IVoeWGwQ',
                'CAACAgUAAxkBAAEBYyBfceX5wmeir5tlM4kPVHEJCKNgBgACdQADIpOQBT1Vl8zfuKyJGwQ',
                'CAACAgUAAxkBAAEBYyFfceX50EPvnJlw-nSuNQzmjWUPUQACdgADIpOQBaFwgf330ElkGwQ',
                'CAACAgUAAxkBAAEBYyJfceX5Ci4aBcYPKy1qzYAG8CNBewACdwADIpOQBSi6GWxtFhbPGwQ',
                'CAACAgUAAxkBAAEBYyNfceX53IQZc449BvfkubhPixddsgACeAADIpOQBTiugkY3UR-fGwQ',
                'CAACAgUAAxkBAAEBYyRfceX5PugkEeRykS_oPAisLbJ5fwACeQADIpOQBWJ68-R1EAjbGwQ',
                'CAACAgUAAxkBAAEBYyVfceX5e6vG9jVeB7DmGChwS6uk_QACegADIpOQBRb70o2tKH3sGwQ',
                'CAACAgUAAxkBAAEBYyZfceX5XAUrUKHaOEhg5Bn_kSfzggACewADIpOQBdeX4U3S_aQWGwQ',
                'CAACAgUAAxkBAAEBYydfceX5P064Y4VQGEMcA_yKHyoY2wACfAADIpOQBZBotoZnDzCzGwQ',
                'CAACAgUAAxkBAAEBYyhfceX5bfKoNewiAAG9Plf9VRwlDhMAAn0AAyKTkAXT6jQOc6cfsBs',
                'CAACAgUAAxkBAAEBYzNfcegIBo9kuGE2Dlbit6E1W0QgDAACfgADIpOQBdcFZOmz-0wkGwQ',
                ]

def thankshelene(update,context):
  global PREV, NOW, DIFF
  NOW = time.time()
  DIFF = NOW - PREV
  PREV = NOW
  update.message.reply_text("Thanks Helene!\nIt has been " + str(int(DIFF)) + " seconds since Helene was last thanked.")

def announcement(update,context):
  update.message.reply_text(update.message.from_user.first_name + " is hungry!")

def samsays(update,context):
  update.message.reply_text(random.choice(samquotes))

samquotes = ["Why are you like this?", 
             "I'm an idiot sandwich!", 
             "I can't believe you've done this!", 
             "It do be like that sometimes.", 
             "It's time to stop.", 
             "Where are your parents??", 
             "Who invented Python?", 
             "Who invented math?", 
             "Who invented integration?", 
             "Fuck you", 
             "Why are you here?",
             "Go home!"]


# MORE MEMES #

def cat(update,context):
  update.message.reply_photo("https://i.kym-cdn.com/photos/images/original/001/505/718/136.jpg")

def kermit(update,context):
  update.message.reply_video("https://media.giphy.com/media/3o85xGocUH8RYoDKKs/giphy.gif")

def pikachu(update,context):
    update.message.reply_photo("https://66.media.tumblr.com/60aeee62dc1aee0c3c0fbad1702eb860/tumblr_inline_pfp352ORsk1r4hkfd_250.png")

def parrot(update,context):
    update.message.reply_sticker("CAACAgIAAxkBAAEBYxJfceDO5hmMkCBJWi19-1TsazADawACsQADwPsIAAED7avN0x5kmRsE")

def hamster(update,context):
    update.message.reply_sticker("CAACAgUAAxkBAAEBYwtfcducd1AxpTduS97Xy-GtppJNMQACAgADirMWFiYe4zQdqswTGwQ")

def patrick(update,context):
    update.message.reply_sticker("CAACAgUAAxkBAAEBYxBfcd_H0ZNMOsZvBVZLrl-swvV9ygACgQADsB58DyM8Hefp7Z62GwQ")

def radio(update,context):
  update.message.reply_text(random.choice(radioList))

radioList = ["https://youtu.be/NoWudgNNIwM", # mongolian throat singing
             "https://youtu.be/Mh5LY4Mz15o", # history of japan
             "https://youtu.be/xuCn8ux2gbs", # history of the world
             "https://youtu.be/tVj0ZTS4WF4", # russian singer
             "https://youtu.be/7CawoPNkY00", # asian music video
             "https://youtu.be/-Yvh6hWDBzA", # ali's cheena agogo
             "https://youtu.be/W8x4m-qpmJ8", # xue hua piao piao
             "https://youtu.be/fLr0-gDOaMY", # pink guy stfu
            ]


# OTOUTO CLONES #

def eightball(update,context):
    update.message.reply_text(random.choice(ballList))

ballList = ["No.", 
            "It is certain.", 
            "My reply is no.", 
            "My sources say no.", 
            "Very doubtful.", 
            "Don't count on it.", 
            "Yes.", 
            "It is decidedly so.", 
            "Of course, my horse.", 
            "Without a doubt.", 
            "You may rely on it.", 
            "As I see it, yes.", 
            "Signs point to yes.", 
            "Most likely.", 
            "Ask again later.", 
            "Cannot predict now.",
            "Concentrate and ask again.",
            "There is a time and place for everything, but not now."]

def xkcd(update,context):
    try:
        num = int(context.args[0])
        if num < 0:
            update.message.reply_text("That is not a valid comic number!")
            return
            
        #argv = " ".join(context.args)
        
        pagetxt = requests.get('https://xkcd.com/{}' .format(num))
        soup = BeautifulSoup(pagetxt.text, 'html.parser')
        #ctitle = (soup.find("div", {"id": "ctitle"})).get_text()
        
        tmp = soup.find("div", {"id": "comic"}).findAll('img')
        for title in tmp:
            ctitle = title['alt']
        for subtext in tmp:
            csubtext = subtext['title']
        for image in tmp:
            cimage = image['src']
        
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text="<a href='https:{}'><b>{} ({})</b></a> \n<i>{}</i>".format(cimage, ctitle, num, csubtext), parse_mode=telegram.ParseMode.HTML)
        #update.message.reply_text("{} ({}) \n{} \nhttps:{}".format(ctitle, argv, csubtext, cimage))

    except (IndexError, ValueError):
        update.message.reply_text("Usage: /xkcd <comic number>")

def set_timer(update, context):
    # Add a job to the queue.
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text("Usage: /set <seconds> <message>")
            return
            
        if context.args[1] == "":
            update.message.reply_text("Usage: /set <seconds> <message>")
            return

        # Add job to queue and stop current one if there is a timer already
        #if 'job' in context.chat_data: #remove current job, if it exists
        #    old_job = context.chat_data['job']
        #    old_job.schedule_removal()
        
        argv = " ".join(context.args).split(" ")
        usr_msg = ""
        for i in range (1, len(argv)):
            usr_msg = usr_msg + " " + argv[i]
        
        new_job = context.job_queue.run_once(alarm, due, context = {"chat_id": update.message.chat_id, "str": usr_msg})
        context.chat_data['job'] = new_job

        update.message.reply_text("I will remind you in {} seconds! ({} minutes)".format(due, round(due/60,2)))
        
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /set <seconds> <message>")
        
def alarm(context):
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context["chat_id"], job.context["str"])

def main():

  # Create Updater object and attach dispatcher to it
  #updater = Updater(TOKEN)
  updater = Updater(TOKEN, use_context=True)
  dp = updater.dispatcher
  print("Bot is alive!")

  # Add '<command>' command handler to dispatcher

  # Utility
  dp.add_handler(CommandHandler('start',start))
  dp.add_handler(CommandHandler('help',list))
  dp.add_handler(CommandHandler('ping',ping))

  dp.add_handler(CommandHandler('redblack',redblack))
  dp.add_handler(CallbackQueryHandler(Button))

  # Memes
  dp.add_handler(CommandHandler('rand',rand))
  dp.add_handler(CommandHandler('thankshelene',thankshelene))
  dp.add_handler(CommandHandler('announcement',announcement))
  dp.add_handler(CommandHandler('samsays',samsays))
  
  # More Memes
  dp.add_handler(CommandHandler('cat', cat))
  dp.add_handler(CommandHandler('kermit',kermit))
  dp.add_handler(CommandHandler('pikachu',pikachu))
  dp.add_handler(CommandHandler('parrot',parrot))
  dp.add_handler(CommandHandler('hamster',hamster))
  dp.add_handler(CommandHandler('patrick',patrick))
  dp.add_handler(CommandHandler('radio',radio))
  
  # Otouto clones
  dp.add_handler(CommandHandler('8ball',eightball))
  dp.add_handler(CommandHandler('xkcd',xkcd))
  dp.add_handler(CommandHandler('set', set_timer, pass_args=True, pass_job_queue=True, pass_chat_data=True))

  
  
  # Start the bot
  updater.start_polling()

  # Run the bot until you press Ctrl-C
  updater.idle()

if __name__ == '__main__':
  main()