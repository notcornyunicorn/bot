import flask
import telebot
import conf

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Добро пожаловать! Я - бот, который с помощью магии определяет твое настроение. Напиши мне одно предложение (не забывая про пунктуацию!), и я покажу тебе свое волшебство!")


@bot.message_handler(func=lambda m: True)
def send_mood(message):
	if '?' in message.text:
		reply = 'Ты, наверное, хочешь что-то узнать от жизни, не правда ли?'
	elif '!' in message.text:
		reply = 'Что-то тебя очень взбудоражило! Ты либо радостен, либо зол, либо воодушевлен!'
	elif '...' in message.text:
		reply = 'Ты, наверное, грустишь?...'
	elif '.' in message.text:
		reply = 'Да, в общем-то, обычное у тебя настроение. Нормальное, как говорят. Хорошего дня.'
	else:
		reply = 'даже мне не под силу тебя понять'

	bot.send_message(message.chat.id, reply)


@app.route('/', methods=['GET', 'HEAD'])
def index():
	return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
	if flask.request.headers.get('content-type') == 'application/json':
		json_string = flask.request.get_data().decode('utf-8')
		update = telebot.types.Update.de_json(json_string)
		bot.process_new_updates([update])
		return ''
	else:
		flask.abort(403)
