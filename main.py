import os, telebot, random, requests, sqlite3, time
# from PIL import Image, ImageOps
from telebot import types
from pytube import YouTube, extract
from pydub import AudioSegment
import funcs

API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)




@bot.message_handler(commands=['start', 'Start', 'START', 'help', 'Help'])
def greet(message):

    bot.reply_to(
        message, '''
Hello there!
Welcome to my bot.
Here is the list of commands you can use:
/image : Returns a random wallpaper
/cat : Get a random cat pic
/duck : get a random duck pic
/yt: download youtube videos as audio 
eg: /yt http://youtube-link
Send any image to convert it into desired ratios with black borders

    ''')


@bot.message_handler(commands=['image'])
def image_send(message):

    bot.send_photo(
        message.chat.id, 'https://source.unsplash.com/random/' +
        str(random.randrange(10, 10000, 1)))


@bot.message_handler(commands=['cat'])
def cat_pic(message):

    catpic = requests.get('https://api.thecatapi.com/v1/images/search').json()
    bot.send_photo(message.chat.id, catpic[0]['url'])


@bot.message_handler(commands=['duck'])
def duck_pic(message):

    duckpic = requests.get('https://random-d.uk/api/v2/random').json()

    bot.send_photo(message.chat.id, duckpic['url'])


@bot.message_handler(content_types=['photo'])
def photo_square(message):

    fsize = 0
    #get the biggest file
    for p in message.photo:
        if p.file_size > fsize:
            fsize = p.file_size
            pic = p.file_id

    file_info = bot.get_file(pic)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(
        API_KEY, file_info.file_path))
    with open('temp/temp.png', 'wb') as f:
        f.write(file.content)

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('1:1', callback_data='1,1')
    btn2 = types.InlineKeyboardButton('4:5', callback_data='4,5')
    btn3 = types.InlineKeyboardButton('4:3', callback_data='4,3')
    btn4 = types.InlineKeyboardButton('9:16', callback_data='9,16')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     'What Ratio do you want?',
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def call(call):

    new_image = funcs.imagesaq(call.data.split(','))
    bot.send_chat_action(call.from_user.id, 'upload_photo')
    bot.answer_callback_query(call.id, 'done')
    bot.send_photo(call.from_user.id, photo=new_image)
@bot.message_handler(commands=['dice'])
def dice_game(msg):
  bot.send_dice(msg.chat.id)
  


@bot.message_handler(commands=['yt', 'Yt', 'YT', 'yT'])
def ytdownload(message):
    #Extract the youtube link from the message and ignore everything else

    prefix = '/yt'
    link = message.text[len(prefix):].strip().split()[0]
    vid_id = extract.video_id(link)

    #check if the bot has already sent the file before, if yes then send the file id of the file
    conn = sqlite3.connect("youtube.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM youtube WHERE links = ?", (vid_id, ))
    results = cur.fetchall()

    if results:
        #if result found then send the file_id to as a message and end
        file_id = results[0][2]

        msg = bot.send_message(message.chat.id, 'File found...')
        bot.send_audio(message.chat.id, audio=file_id)
        bot.delete_message(msg.chat.id, msg.id)
    else:

        #Else Download the file and send
        msg = bot.send_message(message.chat.id, 'Getting Info..')

        yt = YouTube(link)
        #select the highest quality audio file
        stream = yt.streams.get_audio_only(subtype='webm')

        bot.edit_message_text('Downloading Audio...',
                              message_id=msg.id,
                              chat_id=msg.chat.id)

        #download file
        stream.download(output_path='temp/music')
        name = 'temp/music/' + stream.default_filename
        #Convert the file to mp3
        mp3_name = os.path.splitext(name)[0] + '.mp3'
        bot.edit_message_text('Converting Audio...',
                              message_id=msg.id,
                              chat_id=msg.chat.id)

        AudioSegment.from_file(name).export(mp3_name, format='mp3')
        #open the downloaded file as a binary
        f = open(mp3_name, 'rb')
        bot.edit_message_text('Uploading Audio...',
                              message_id=msg.id,
                              chat_id=msg.chat.id)
        bot.send_chat_action(message.chat.id, 'upload_audio')

        #Send the audio file and store the returned msg in audmsg
        audmsg = bot.send_audio(message.chat.id,
                                audio=f,
                                title=yt.title,
                                duration=yt.length,
                                reply_to_message_id=message.id,
                                thumb=yt.thumbnail_url,
                                performer=yt.author)

        bot.delete_message(msg.chat.id, msg.id)  #delete the alert message
        f.close()  #close the file
        t = int(time.time())  #DateTime in EPOCH

        #store the audio link, file_id, file_size, stream abr, file type, datetime(epoch), chat ID , Username of user in the Database for future use.

        cur.execute("INSERT INTO youtube VALUES (NULL,?,?,?,?,?,?,?,?)",
                    (vid_id, audmsg.audio.file_id, audmsg.audio.file_size,
                     stream.abr, stream.mime_type, t, audmsg.chat.id,
                     message.chat.first_name + ' ' + message.chat.last_name))

        conn.commit()
        #delete the audio temp file to save storage space
        os.remove(mp3_name)
        os.remove(name)
    #close the database connection
    conn.close()


@bot.message_handler(commands=['dbcheck'])
def dbcheck(message):
    string = ''
    conn = sqlite3.connect('youtube.db')
    cur = conn.cursor()
    cur.execute('select * from youtube ORDER BY rid DESC LIMIT 10')
    results = cur.fetchall()
    for i in results:
        string += str(i[0]) + ' ' + time.ctime(int(i[6])) + ' ' + str(
            i[8]) + '''
'''

    bot.send_message(message.chat.id, string, parse_mode='HTML')


@bot.message_handler(func=lambda m: True)
def echo_all(message):

    bot.send_message(message.chat.id,
                     message.chat.first_name + ' said:  ' + message.text)


bot.infinity_polling()
