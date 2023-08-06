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

# Basic extra functions.
# ======================
# Provides things like time, show bot owner and noob help.
#
# Delete this file or remove functions if you do not want users to
# Access the following funcitons.

import datetime
import string

class basic:
	# Initialize the module
	def __init__(self, core):
		self.core = core

		# Set our help text
		self.basic_help = {
			'time': 'Tells you the time.',
			'noob': 'Information for n00bs.',
			'owner': 'Reveal the bot owner.'
		}


	# This is the hook for importing user help functions into core.
	def au_help(self):
		return self.basic_help

	# Show the time
	def u_time(self, bufferText):
		# Format the time...
		timev = datetime.datetime.utcnow()
		timef = timev.strftime(self.core.config['date_format'])

		# Tell the user.
		self.core.notice("[Time]: %s (UTC)" % timef)


	# Owner of the bot
	def u_owner(self, bufferText):
		self.core.notice("My root botmaster is %s."
			% self.core.config['owner'])


	# Info for n00bs
	def u_noob(self, bufferText):
		helpGuide = "http://www.irchelp.org/irchelp/irctutorial.html"
		self.core.notice("[Beginner Help]: Welcome %s, IRC Help here: %s"
			% (self.core.buffer['username'], helpGuide))
