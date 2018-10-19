# coding: utf-8
import discord
import logging
import datetime
import locale
import os
import mysql.connector

d = datetime.datetime.now()
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord_syslog_'+'%s-%s-%s' % (d.year, d.month, d.day)+'.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client = discord.Client()

@client.event
async def on_ready():
	print('------')
	print('システム起動完了')
	print("起動時刻:",'%s年%s月%s日' % (d.year, d.month, d.day),'%s時%s分%s秒' % (d.hour, d.minute, d.second))
	print('LoggingBot Ver3.5.2')
	print(client.user.id)
	print('------')
	print('導入サーバ一覧:')
	[print(' - ' + s.name) for s in client.servers]

@client.event
async def on_message(message):
	import datetime
	d = datetime.datetime.now()
	print("============")
	print("サーバ名:",message.server)
	print("投稿者：",message.author.name)
	print("Type：MessageContribution")
	print("内容：",message.content.encode('cp932', "ignore").decode("cp932"))
	print("Channel:" + str(message.channel))
	print("データ取得日時:",'%s年%s月%s日' % (d.year, d.month, d.day),'%s時%s分%s秒' % (d.hour, d.minute, d.second))
	print("============")
	os.makedirs('logdata/' + str(message.server) + '/' + message.author.name + '/' + str(message.channel) + '/Contribution', exist_ok=True)
	f = open('logdata/' + str(message.server) + '/' + message.author.name + '/' + str(message.channel) + '/Contribution/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f.write("[Channel:" + str(message.channel) + " UserName:" + message.author.name + " Date:" + str(d) + " Type：MessageContribution]\n" + message.content + "\n\n")
	f.close()
	#全操作ログ(チャンネル毎に保存かつ、操作内容でカテ分け)
	os.makedirs('logdata/' + str(message.server) + '/alldata/Contribution/' + str(message.channel), exist_ok=True)
	f2 = open('logdata/' + str(message.server) + '/alldata/Contribution/' + str(message.channel) + '/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f2.write("[Channel:" + str(message.channel) + " UserName:" + message.author.name + " Date:" + str(d) + " Type：MessageContribution]\n" + message.content + "\n\n")
	f2.close()
	#全操作ログを保存
	os.makedirs('logdata/' + str(message.server) + '/alldata/all_log/' + str(message.channel), exist_ok=True)
	f3 = open('logdata/' + str(message.server) + '/alldata/all_log/' + str(message.channel) + '/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f3.write("[Channel:" + str(message.channel) + " UserName:" + message.author.name + " Date:" + str(d) + " Type：MessageContribution]\n" + message.content + "\n\n")
	f3.close()
	#DBの処理
	server = message.server
	channel = message.channel
	username = message.author.name
	msg_type = "Contribution"
	message = message.content
	date_time = str(d)
	DataBasePushContribution(server,channel,username,msg_type,message,date_time)

@client.event
async def on_message_edit(before, after):
	import datetime
	d = datetime.datetime.now()
	print("============")
	print("サーバ名:",before.server)
	print("投稿者：",before.author.name)
	print("Type：Edit")
	print("編集前：",before.content.encode('cp932', "ignore").decode("cp932"))
	print("編集後：",after.content.encode('cp932', "ignore").decode("cp932"))
	print("Channel:" + str(before.channel))
	print("データ取得日時:",'%s年%s月%s日' % (d.year, d.month, d.day),'%s時%s分%s秒' % (d.hour, d.minute, d.second))
	print("============")
	os.makedirs('logdata/' + str(before.server) + '/' + before.author.name + '/' + str(before.channel) + '/edit', exist_ok=True)
	f = open('logdata/' + str(before.server) + '/' + before.author.name + '/' + str(before.channel) + '/edit/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f.write("[Channel:" + str(before.channel) + " UserName:" + before.author.name + " Date:" + str(d) + " Type：Edit]\nBefore Edit:\n" + before.content + "\n---------------------\nAfter Edit:\n" + after.content + "\n\n")
	f.close()
	#全操作ログ(チャンネル毎に保存かつ、操作内容でカテ分け)
	os.makedirs('logdata/' + str(before.server) + '/alldata/Edit/' + str(before.channel), exist_ok=True)
	f2 = open('logdata/' + str(before.server) + '/alldata/Edit/' + str(before.channel) + '/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f2.write("[Channel:" + str(before.channel) + " UserName:" + before.author.name + " Date:" + str(d) + " Type：Edit]\nBefore Edit:\n" + before.content + "\n---------------------\nAfter Edit:\n" + after.content + "\n\n")
	f2.close()
	#全操作ログを保存
	os.makedirs('logdata/' + str(before.server) + '/alldata/all_log/' + str(before.channel), exist_ok=True)
	f3 = open('logdata/' + str(before.server) + '/alldata/all_log/' + str(before.channel) + '/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f3.write("[Channel:" + str(before.channel) + " UserName:" + before.author.name + " Date:" + str(d) + " Type：Edit]\nBefore Edit:\n" + before.content + "\n---------------------\nAfter Edit:\n" + after.content + "\n\n")
	f3.close()
	#DBの処理
	server = before.server
	channel = before.channel
	username = before.author.name
	msg_type = "Edit"
	before_message = before.content
	after_message = after.content
	date_time = str(d)
	DataBasePushEdit(server,channel,username,msg_type,before_message,after_message,date_time)

@client.event
async def on_message_delete(message):
	import datetime
	d = datetime.datetime.now()
	print("============")
	print("サーバ名:",message.server)
	print("投稿者：",message.author.name)
	print("Type：MessageDelete")
	print("内容：",message.content.encode('cp932', "ignore").decode("cp932"))
	print("Channel:" + str(message.channel))
	print("データ取得日時:",'%s年%s月%s日' % (d.year, d.month, d.day),'%s時%s分%s秒' % (d.hour, d.minute, d.second))
	print("============")
	os.makedirs('logdata/' + str(message.server) + '/' + message.author.name + '/' + str(message.channel) + '/delete', exist_ok=True)
	f = open('logdata/' + str(message.server) + '/' + message.author.name + '/' + str(message.channel) + '/delete/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f.write("[Channel:" + str(message.channel) + " UserName:" + message.author.name + " Date:" + str(d) + " Type：MessageDelete]\n" + message.content + "\n\n")
	f.close()
	#全操作ログ(チャンネル毎に保存かつ、操作内容でカテ分け)
	os.makedirs('logdata/' + str(message.server) + '/alldata/delete/' + str(message.channel), exist_ok=True)
	f2 = open('logdata/' + str(message.server) + '/alldata/delete/' + str(message.channel) + '/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f2.write("[Channel:" + str(message.channel) + " UserName:" + message.author.name + " Date:" + str(d) + " Type：MessageDelete]\n" + message.content + "\n\n")
	f2.close()
	#全操作ログを保存
	os.makedirs('logdata/' + str(message.server) + '/alldata/all_log/' + str(message.channel), exist_ok=True)
	f3 = open('logdata/' + str(message.server) + '/alldata/all_log/' + str(message.channel) + '/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f3.write("[Channel:" + str(message.channel) + " UserName:" + message.author.name + " Date:" + str(d) + " Type：MessageDelete]\n" + message.content + "\n\n")
	f3.close()
	#DBの処理
	server = message.server
	channel = message.channel
	username = message.author.name
	msg_type = "Delete"
	message = message.content
	date_time = str(d)
	DataBasePushDelete(server,channel,username,msg_type,message,date_time)

def DataBasePushContribution(server,channel,username,msg_type,message,date_time):
	db=mysql.connector.connect(host="HOST", user="USER", password="PASSWORD")
	cursor=db.cursor()

	# データベース「DB_NAME(データベース名)」を選択
	cursor.execute("USE DB_NAME")
	db.commit()

	# データを挿入
	insert_fruit = "INSERT INTO msg_contribution(server,channel,username,msg_type,message,date_time) VALUES ('"+str(server)+"','"+str(channel)+"','"+username+"', '"+msg_type+"', '"+message+"', '"+date_time+"');"

	cursor.execute(insert_fruit)

	db.commit()

def DataBasePushEdit(server,channel,username,msg_type,before_message,after_message,date_time):
	db=mysql.connector.connect(host="HOST", user="USER", password="PASSWORD")
	cursor=db.cursor()

	# データベース「DB_NAME(データベース名)」を選択
	cursor.execute("USE DB_NAME")
	db.commit()

	# データを挿入
	insert_fruit = "INSERT INTO msg_edit(server,channel,username,msg_type,before_message,after_message,date_time) VALUES ('"+str(server)+"','"+str(channel)+"','"+username+"', '"+msg_type+"', '"+before_message+"','"+after_message+"', '"+date_time+"');"

	cursor.execute(insert_fruit)

	db.commit()

def DataBasePushDelete(server,channel,username,msg_type,message,date_time):
	db=mysql.connector.connect(host="HOST", user="USER", password="PASSWORD")
	cursor=db.cursor()

	# データベース「DB_NAME(データベース名)」を選択
	cursor.execute("USE DB_NAME")
	db.commit()

	# データを挿入
	insert_fruit = "INSERT INTO msg_delete(server,channel,username,msg_type,message,date_time) VALUES ('"+str(server)+"','"+str(channel)+"','"+username+"', '"+msg_type+"', '"+message+"', '"+date_time+"');"

	cursor.execute(insert_fruit)

	db.commit()

#本番環境
client.run("DISCORD_CLIENT_KEY")
