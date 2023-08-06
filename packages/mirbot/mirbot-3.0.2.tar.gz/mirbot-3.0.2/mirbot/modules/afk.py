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

# Away from Keyboard (AFK) module.
# ======================
# Marks users as AFK, alerts people to someone being away.
# Also informs you of someone asking for you and when.

import datetime
import string
import json

class afk:
	# Initialize the module
	def __init__(self, core):
		self.core = core

		# Set our help text
		self.basic_help = {
			'afk': 'Set yourself as Away From Keyboard.'
		}

		# Set our botmaster help text
		self.oper_help = {
			'removeafk': 'Remove a user AFK message.'
		}

		self.on_commands = {
			'PRIVMSG': ['checkStatus']
		}

		self.checkAFKInstalled()


	# This is the hook for importing user help functions into core.
	def au_help(self):
		return self.basic_help

	# This is the hook for importing oper help functions into core.
	def ao_help(self):
		return self.oper_help

	# This is the hook for loading "On commands", functions triggered by
	# buffer changes.
	def onLoad(self):
		return self.on_commands

	# Function for checking a DB exists for AFK
	def checkAFKInstalled(self):
		# Is the table in sqlite_master?
		tables = self.core.db_query("SELECT name FROM sqlite_master" \
			" WHERE type = 'table' AND name = 'afk';", (), True)

		# If not, make it.
		if tables < 1:
			print("Creating afk table...")
			self.core.db_exec("CREATE TABLE afk" \
				" (Time INT NOT NULL, Username TEXT," \
				" Reason TEXT, Asked TEXT);")


	# Control afk users
	def u_afk(self, bufferText, user = False):
		options = bufferText.split(" ", 1)

		if len(options) < 2:
			self.core.notice("Syntax: %safk [Reason.../Back]"
				% self.core.config['prefix'])
			return False

		reason = options[1]

		if user:
			user_search = user
		else:
			user_search = self.core.buffer['username']

		afkCheck = self.core.db_query("SELECT * FROM afk WHERE Username = ?;",
			(user_search.lower(),))

		if reason.lower() == "back":
			if len(afkCheck) < 1:
				self.core.notice("Back from where?")
				return False

			afkCheck = afkCheck[0]

			self.core.db_exec("DELETE FROM afk WHERE Username = ?;",
				(afkCheck['Username'],))

			whoAsked = json.loads(afkCheck['Asked'])
			iAsked = len(whoAsked) - 1

			self.core.notice("You are back after %s! %d users were alerted."
				% (self.core.timeSince(afkCheck['Time']), iAsked))

			if iAsked > 0:
				stringAsked = "People who asked for you:"

				for asked in whoAsked:
					if asked['Username'] != user_search.lower():
						stringAsked = stringAsked + " [%s -> %s ago]" \
							% (asked['Username'].capitalize(),
								self.core.timeSince(asked['Time']))

				self.core.notice(stringAsked)
		else:
			if len(afkCheck) > 0:
				self.core.db_exec("UPDATE afk SET Reason = ?" \
					" WHERE Username = ?;",
					(reason, user_search))
				self.core.notice("Away status updated!")
			else:
				asked = [{
					'Username': user_search.lower(),
					'Time': self.core.unixtime()
				}]

				self.core.db_exec("INSERT INTO afk" \
					" (Username, Reason, Time, Asked)" \
					" VALUES (?, ?, ?, ?);",
					(user_search.lower(),
						reason,
						self.core.unixtime(),
						json.dumps(asked)))

				self.core.notice("You have been marked as away!")

		return True



	# Alias for .afk back
	def u_back(self, bufferText):
		self.core.buffer['text'] = "%safk back" % self.core.config['prefix']
		self.u_afk(self.core.buffer['text'])

		return True


	# User method to remove a user AFK
	def u_removeafk(self, bufferText):
		# Do we have access to this method?
		if self.core.hasAccess(self.core.buffer['user_host']) == False:
			self.core.notice("Access Denied!")
			return False

		# Get command arguments
		options = bufferText.split(" ", 1)

		# Is the syntax correct?
		if len(options) < 2:
			self.core.notice("Syntax: %sremoveafk [username]"
				% self.core.config['prefix'])
			return False

		self.core.buffer['text'] = "%safk back" % self.core.config['prefix']
		self.u_afk(self.core.buffer['text'], options[1].lower())

		self.core.notice("Removed AFK status from: %s" % options[1])



	# Method to check the status of username
	def o_checkStatus(self, aBuffer):
		# Check we have the correct conditions for checking user status.
		if aBuffer['command'] == "PRIVMSG" \
			and aBuffer['channel'] != None \
			and aBuffer['text'] != None:
			# Set our variables.
			text = aBuffer['text']
			channel = aBuffer['channel']
			username = aBuffer['username']
		else:
			return True

		# Only use lowercase usernames
		username = username.lower()

		# Is this user away?
		userCheck = self.core.db_query("SELECT * FROM afk;")

		# Default action is to do nothing
		alert = False

		# Do we have users in afk to check? If not, return.
		if len(userCheck) < 1:
			return True

		# For each afk person...
		for afk in userCheck:
			# Is this person in the latest buffer text?
			if afk['Username'] in text.lower() and afk['Username'] != username:
				# Do we have a list of people who asked about us?
				# If so deserialize, else make an empty list.
				if afk['Asked']:
					whoAsked = json.loads(afk['Asked'])
				else:
					whoAsked = []

				# Is the asked list empty? If not...
				if len(whoAsked) > 0:
					# Check everyone who asked...
					for asked in whoAsked:
						# Is the person asking in this list? Have they asked
						# in the last 5 minutes?
						if asked['Username'] == username \
							and self.core.unixtime() - asked['Time'] > 600:
							# If so remove them from the list to be re-added.
							whoAsked.remove(asked)
							# Flag that we will alert the user.
							alert = True
						elif asked['Username'] == username \
							and self.core.unixtime() - asked['Time'] < 600:
							# Carry on doing nothing.
							alert = False
						else:
							# Now alert.
							alert = True

					# Are we alerting?
					if alert == True:
						# Add a new entry to the Asked column
						newAsked = {
							'Username': username,
							'Time': self.core.unixtime()
						}

						# Send a notice to the user asking.
						self.core.notice("%s has been away for %s." \
							" REASON: %s." \
							% (afk['Username'].capitalize(),
								self.core.timeSince(afk['Time']),
								afk['Reason']),
							username)

						# Append to the whoAsked list.
						whoAsked.append(newAsked)

						# Are we ignoring the away user?
						if self.core.checkIgnored(afk['Username']) == False:
							# Format the message for the user who is away.
							alertMsg = '%s, %s has just asked for you' \
								' in %s. You have been away for %s.' \
								% (afk['Username'].capitalize(),
									username.capitalize(),
									channel,
									self.core.timeSince(afk['Time']))

							# Send them a private message.
							self.core.pm(alertMsg, afk['Username'])

						# Update our database so that we have the most
						# Up-to-date list. Remember to serialize the list
						# As a JSON string.
						self.core.db_exec("UPDATE afk SET Asked = ?" \
							" WHERE Username = ?;",
							(json.dumps(whoAsked), afk['Username']))

				else:
					# Right, whole new list with a new user and timestamp
					newAsked = [{
						'Username': username,
						'Time': self.core.unixtime()
					}]

					# Tell the user that we've been afk for a while.
					self.core.notice("%s has been away for %s. REASON: %s." \
						% (afk['Username'].capitalize(),
							self.core.timeSince(afk['Time']),
							afk['Reason']),
						username)

					# Is the afk user ignored?
					if self.core.checkIgnored(afk['Username']) == False:
						# Format the message to them...
						alertMsg = '%s, %s has just asked for you' \
							' in %s. You have been away for %s.' \
							% (afk['Username'].capitalize(),
								username.capitalize(),
								channel,
								self.core.timeSince(afk['Time']))

						# Send the away user a private message
						self.core.pm(alertMsg, afk['Username'])

					# Update our DB with our JSON serialized array of users
					# Who have asked for us.
					self.core.db_exec("UPDATE afk SET Asked = ?" \
						" WHERE Username = ?;",
						(json.dumps(newAsked), afk['Username']))

		# Clear buffer
		self.core.buffer['text'] = None

		# All done
		return True
