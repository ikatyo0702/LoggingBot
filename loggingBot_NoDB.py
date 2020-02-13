# coding: utf-8
import discord
import logging
import datetime
import locale
import os
#import mysql.connector

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
	[print(' - ' + s.name) for s in client.guilds]

@client.event
async def on_message(message):
	import datetime
	d = datetime.datetime.now()
	print("============")
	print("サーバ名:",message.guild)
	print("投稿者：",message.author.name)
	print("Type：MessageContribution")
	print("内容：",message.content.encode('cp932', "ignore").decode("cp932"))
	print("Channel:" + str(message.channel))
	print("データ取得日時:",'%s年%s月%s日' % (d.year, d.month, d.day),'%s時%s分%s秒' % (d.hour, d.minute, d.second))
	print("============")
	os.makedirs('logdata/' + str(message.guild) + '/' + message.author.name + '/' + str(message.channel) + '/Contribution', exist_ok=True)
	f = open('logdata/' + str(message.guild) + '/' + message.author.name + '/' + str(message.channel) + '/Contribution/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f.write("[Channel:" + str(message.channel) + " UserName:" + message.author.name + " Date:" + str(d) + " Type：MessageContribution]\n" + message.content + "\n\n")
	f.close()
	#全操作ログ(チャンネル毎に保存かつ、操作内容でカテ分け)
	os.makedirs('logdata/' + str(message.guild) + '/alldata/Contribution/' + str(message.channel), exist_ok=True)
	f2 = open('logdata/' + str(message.guild) + '/alldata/Contribution/' + str(message.channel) + '/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f2.write("[Channel:" + str(message.channel) + " UserName:" + message.author.name + " Date:" + str(d) + " Type：MessageContribution]\n" + message.content + "\n\n")
	f2.close()
	#全操作ログを保存
	os.makedirs('logdata/' + str(message.guild) + '/alldata/all_log/' + str(message.channel), exist_ok=True)
	f3 = open('logdata/' + str(message.guild) + '/alldata/all_log/' + str(message.channel) + '/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f3.write("[Channel:" + str(message.channel) + " UserName:" + message.author.name + " Date:" + str(d) + " Type：MessageContribution]\n" + message.content + "\n\n")
	f3.close()

@client.event
async def on_message_edit(before, after):
	import datetime
	d = datetime.datetime.now()
	print("============")
	print("サーバ名:",before.guild)
	print("投稿者：",before.author.name)
	print("Type：Edit")
	print("編集前：",before.content.encode('cp932', "ignore").decode("cp932"))
	print("編集後：",after.content.encode('cp932', "ignore").decode("cp932"))
	print("Channel:" + str(before.channel))
	print("データ取得日時:",'%s年%s月%s日' % (d.year, d.month, d.day),'%s時%s分%s秒' % (d.hour, d.minute, d.second))
	print("============")
	os.makedirs('logdata/' + str(before.guild) + '/' + before.author.name + '/' + str(before.channel) + '/edit', exist_ok=True)
	f = open('logdata/' + str(before.guild) + '/' + before.author.name + '/' + str(before.channel) + '/edit/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f.write("[Channel:" + str(before.channel) + " UserName:" + before.author.name + " Date:" + str(d) + " Type：Edit]\nBefore Edit:\n" + before.content + "\n---------------------\nAfter Edit:\n" + after.content + "\n\n")
	f.close()
	#全操作ログ(チャンネル毎に保存かつ、操作内容でカテ分け)
	os.makedirs('logdata/' + str(before.guild) + '/alldata/Edit/' + str(before.channel), exist_ok=True)
	f2 = open('logdata/' + str(before.guild) + '/alldata/Edit/' + str(before.channel) + '/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f2.write("[Channel:" + str(before.channel) + " UserName:" + before.author.name + " Date:" + str(d) + " Type：Edit]\nBefore Edit:\n" + before.content + "\n---------------------\nAfter Edit:\n" + after.content + "\n\n")
	f2.close()
	#全操作ログを保存
	os.makedirs('logdata/' + str(before.guild) + '/alldata/all_log/' + str(before.channel), exist_ok=True)
	f3 = open('logdata/' + str(before.guild) + '/alldata/all_log/' + str(before.channel) + '/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f3.write("[Channel:" + str(before.channel) + " UserName:" + before.author.name + " Date:" + str(d) + " Type：Edit]\nBefore Edit:\n" + before.content + "\n---------------------\nAfter Edit:\n" + after.content + "\n\n")
	f3.close()

@client.event
async def on_message_delete(message):
	import datetime
	d = datetime.datetime.now()
	print("============")
	print("サーバ名:",message.guild)
	print("投稿者：",message.author.name)
	print("Type：MessageDelete")
	print("内容：",message.content.encode('cp932', "ignore").decode("cp932"))
	print("Channel:" + str(message.channel))
	print("データ取得日時:",'%s年%s月%s日' % (d.year, d.month, d.day),'%s時%s分%s秒' % (d.hour, d.minute, d.second))
	print("============")
	os.makedirs('logdata/' + str(message.guild) + '/' + message.author.name + '/' + str(message.channel) + '/delete', exist_ok=True)
	f = open('logdata/' + str(message.guild) + '/' + message.author.name + '/' + str(message.channel) + '/delete/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f.write("[Channel:" + str(message.channel) + " UserName:" + message.author.name + " Date:" + str(d) + " Type：MessageDelete]\n" + message.content + "\n\n")
	f.close()
	#全操作ログ(チャンネル毎に保存かつ、操作内容でカテ分け)
	os.makedirs('logdata/' + str(message.guild) + '/alldata/delete/' + str(message.channel), exist_ok=True)
	f2 = open('logdata/' + str(message.guild) + '/alldata/delete/' + str(message.channel) + '/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f2.write("[Channel:" + str(message.channel) + " UserName:" + message.author.name + " Date:" + str(d) + " Type：MessageDelete]\n" + message.content + "\n\n")
	f2.close()
	#全操作ログを保存
	os.makedirs('logdata/' + str(message.guild) + '/alldata/all_log/' + str(message.channel), exist_ok=True)
	f3 = open('logdata/' + str(message.guild) + '/alldata/all_log/' + str(message.channel) + '/' + '%s-%s-%s' % (d.year, d.month, d.day) + ".txt", 'a+')
	f3.write("[Channel:" + str(message.channel) + " UserName:" + message.author.name + " Date:" + str(d) + " Type：MessageDelete]\n" + message.content + "\n\n")
	f3.close()

#本番環境
client.run("DISCORD_CLIENT_KEY")
