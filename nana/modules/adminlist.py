import os, requests, html

from bs4 import BeautifulSoup

from nana import app, Owner, Command
from nana.helpers.parser import mention_html, mention_markdown
from pyrogram import Filters

NamaModul = "Admin List"
HelpCMD = ['`admin <*grup tag/id>` - Melihat semua admin pada grup target']


@app.on_message(Filters.user("self") & Filters.command(["admins", "adminlist"], Command))
def adminlist(client, message):
	replyid = None
	toolong = False
	if len(message.text.split()) >= 2:
		chat = message.text.split(None, 1)[1]
		grup = client.get_chat(chat)
	else:
		chat = message.chat.id
		grup = client.get_chat(chat)
	if message.reply_to_message:
		replyid = message.reply_to_message.message_id
	alladmins = client.iter_chat_members(chat, filter="administrators")
	creator = []
	admin = []
	badmin = []
	for a in alladmins:
		try:
			nama = a.user.first_name + " " + a.user.last_name
		except:
			nama = a.user.first_name
		if nama == None:
			nama = "☠️ Deleted account"
		if a.status == "administrator":
			if a.user.is_bot == True:
				badmin.append(mention_markdown(a.user.id, nama))
			else:
				admin.append(mention_markdown(a.user.id, nama))
		elif a.status == "creator":
			creator.append(mention_markdown(a.user.id, nama))
	admin.sort()
	badmin.sort()
	totaladmins = len(creator)+len(admin)+len(badmin)
	teks = "**Admins in {}**\n".format(grup.title)
	teks += "╒═══「 Creator 」\n"
	for x in creator:
		teks += "│ • {}\n".format(x)
		if len(teks) >= 4096:
			message.reply(message.chat.id, teks, reply_to_message_id=replyid)
			teks = ""
			toolong = True
	teks += "╞══「 {} Human Administrator 」\n".format(len(admin))
	for x in admin:
		teks += "│ • {}\n".format(x)
		if len(teks) >= 4096:
			message.reply(message.chat.id, teks, reply_to_message_id=replyid)
			teks = ""
			toolong = True
	teks += "╞══「 {} Bot Administrator 」\n".format(len(badmin))
	for x in badmin:
		teks += "│ • {}\n".format(x)
		if len(teks) >= 4096:
			message.reply(message.chat.id, teks, reply_to_message_id=replyid)
			teks = ""
			toolong = True
	teks += "╘══「 Total {} Admins 」".format(totaladmins)
	if toolong:
		message.reply(message.chat.id, teks, reply_to_message_id=replyid)
	else:
		message.edit(teks)

@app.on_message(Filters.user("self") & Filters.command(["reportadmin", "reportadmins"], Command))
def report_admin(client, message):
	message.delete()
	if len(message.text.split()) >= 2:
		text = message.text.split(None, 1)[1]
	else:
		text = None
	grup = client.get_chat(message.chat.id)
	alladmins = client.iter_chat_members(message.chat.id, filter="administrators")
	admin = []
	for a in alladmins:
		if a.status == "administrator" or a.status == "creator":
			if a.user.is_bot == False:
				admin.append(mention_html(a.user.id, "\u200b"))
	if message.reply_to_message:
		if text:
			teks = '{}'.format(text)
		else:
			teks = '{} reported to admins.'.format(mention_html(message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name))
	else:
		if text:
			teks = '{}'.format(html.escape(text))
		else:
			teks = "Calling admins in {}.".format(grup.title)
	teks += "".join(admin)
	if message.reply_to_message:
		client.send_message(message.chat.id, teks, reply_to_message_id=message.reply_to_message.message_id, parse_mode="html")
	else:
		client.send_message(message.chat.id, teks, parse_mode="html")

@app.on_message(Filters.user("self") & Filters.command(["everyone"], Command))
def tag_all_users(client, message):
	message.delete()
	if len(message.text.split()) >= 2:
		text = message.text.split(None, 1)[1]
	else:
		text = "Hi all 🙃"
	kek = client.iter_chat_members(message.chat.id)
	for a in kek:
		if a.user.is_bot == False:
			text += mention_html(a.user.id, "\u200b")
	if message.reply_to_message:
		client.send_message(message.chat.id, text, reply_to_message_id=message.reply_to_message.message_id, parse_mode="html")
	else:
		client.send_message(message.chat.id, text, parse_mode="html")


@app.on_message(Filters.user("self") & Filters.command(["botlist"], Command))
def get_list_bots(client, message):
	replyid = None
	if len(message.text.split()) >= 2:
		chat = message.text.split(None, 1)[1]
		grup = client.get_chat(chat)
	else:
		chat = message.chat.id
		grup = client.get_chat(chat)
	if message.reply_to_message:
		replyid = message.reply_to_message.message_id
	getbots = client.iter_chat_members(chat)
	bots = []
	for a in getbots:
		try:
			nama = a.user.first_name + " " + a.user.last_name
		except:
			nama = a.user.first_name
		if nama == None:
			nama = "☠️ Deleted account"
		if a.user.is_bot == True:
			bots.append(mention_markdown(a.user.id, nama))
	teks = "**All bots in group {}**\n".format(grup.title)
	teks += "╒═══「 Bots 」\n"
	for x in bots:
		teks += "│ • {}\n".format(x)
	teks += "╘══「 Total {} Bots 」".format(len(bots))
	if replyid:
		client.send_message(message.chat.id, teks, reply_to_message_id=replyid)
	else:
		message.edit(teks)
