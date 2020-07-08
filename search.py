import pymysql
import telebot
import hashlib
import sys
import time

try:
	#авторизация бота
	bot = telebot.TeleBot('1072639905:AAEcbgRJf7-z6h5pL12NCps2fqF6UF9OZDI')
	print("бот авторизирован")

	def decryptMD5(h):
		password = h
		dictionary = "личный словарь.txt"
		dictionary = open(dictionary,'r')
		for p in dictionary:
			h_obj = hashlib.md5(p.strip().encode('utf-8')).hexdigest()
			if h_obj == password:
				return "Пароль расшифрован: %s " % p
				break
			else:
				return "Не удалось расшифровать :("
	def dehash(message):
		msg = message.split(" ")
		if len(msg) == 2:
			return decryptMD5(msg[1])
		else:
			return "Используй /dehash хэш"

	def search(message):
		try:
			print("запуск поиска")
			datab = pymysql.connect("pma.sprinthost.ru", 'f0452641_search', '123123', 'players')
			msg = message.split(" ")
			with datab:
				cur = datab.cursor()
				cur.execute("SELECT * FROM players")
				rows = cur.fetchall()

				for row in rows:
					if row["nick"] == msg[1]:
						return row["password"]
		except pymysql.err.OperationalError as c:
			print(c)
			return "Извините, сейчас небольшие неполадки с базой данных :( Попробуйте другие функции /help :D"
	#обработка сообщений
	@bot.message_handler(content_types=['text'])
	def getMessages(message):
		print("обработка сообщений")
		if message.text == "Привет":
			bot.send_message(message.from_user.id,"Привет, чтобы узнать комманды напиши /help")

		elif message.text == "/help":
			bot.send_message(message.from_user.id, "----------------\n/search - посиск по нику\n----------------\n/dehash - расшифровка хэша MD5\n")

		elif message.text.count("/search") != 0:
			bot.send_message(message.from_user.id, search(message.text))

		elif message.text.count("/dehash") != 0:

			bot.send_message(message.from_user.id, "Подождите немного перед дехэшированием :D")

			dehaha = dehash(message.text)
			num = 0
			while num != 110:
				bot.send_message(message.from_user.id, "Идет декодирование хэша - " + str(num) + "%")
				num += 10
			bot.send_message(message.from_user.id, dehaha)

		elif message.text == "/dehash":
			bot.send_message(message.from_user.id, "Используй /dehash хэш")

		else:
			bot.send_message(message.from_user.id,"Я тебя не понимаю :( Напиши /help, чтобы узнать комманды :D")

	bot.polling(none_stop=True, interval=0)
except:
	pass
