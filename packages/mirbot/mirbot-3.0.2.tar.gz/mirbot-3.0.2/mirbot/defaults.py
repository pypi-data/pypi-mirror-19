#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# MIRbot
# (Modular Information Retrieval bot)
# ----------------------------------------------------------------------------
# Written by Xan Manning
# ----------------------------------------------------------------------------
#
# Copyright (c) 2015 Xan Manning (http://xan-manning.co.uk)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ----------------------------------------------------------------------------

config = {
	# Bot nickname
	'nick':				'MIRbot',

	# Bot name
	'name':				'MIRbot',

	# Server to connect to
	'server': 			'127.0.0.1',

	# Server port number (usually 6667)
	'port':				6667,

	# Server uses SSL?
	'ssl':				False,

	# Server requires password? False or "password".
	'password':			False,

	# Array of channels to join on connect
	'channels': 		['#lobby'],

	# Lenght of botmaster session
	'user_session':		3600,

	# Prefix for commands, try something like ! or .
	'prefix':			'!',

	# Data directory
	'data_dir':			'data',

	# SQLite3 Database name
	'sqlite_db':		'MIRbot.db',

	# Enable logging
	'logging':			True,

	# Enable auto-trim logging
	# False or number of days to keep logs.
	'logging_trim':		False,

	# Date format for logging
	'date_format':		'%Y-%m-%d %H:%M',

	# Welcome new users
	'welcome_new':		True,

	# Welcome message for new users
	# {NICK} is replaced with nickname
	# {CHANNEL} is replaced with channel
	'welcome_message':	'Hello {NICK}, welcome to {CHANNEL}!',

	# Announce when joining a channel
	'say_online':		True,

	# What to say when joining a channel
	'online_message':	'Hello {CHANNEL}!',

	# Attempt to self-oper on joining channel
	# Only works if you log in as IRC Oper
	'self_oper':		False,

	# Attempt to avoid flooding the server and getting blocked.
	'avoid_flooding':	True,

	# Flood count (max number of sends/second)
	'flood_count':		5,

	# Flood timeout (seconds before counter is reset)
	'flood_timeout':	5,

	# Flood wait (seconds to wait when flood exceeded)
	'flood_wait':		2,

	# Owner (this is required to register as root botmaster)
	'owner':			'admin',

	# Hashing algorithm, (refer to hashlib)
	'algorithm':		'sha512',

	# Allow email to be sent from modules. (False or Email Address)
	# Email is done by connecting to local sendmail interface.
	'allow_sendmail':	'MIRbot@example.com',

	# Start up commands
	# This is an array of RAW IRC COMMANDS to issue on server connect.
	# Example:
	# 'commands':		['OPER root pass', 'PRIVMSG NICKSERV :identify pass']
	'commands':			[]
}
