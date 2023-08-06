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


# This is an example module. We have called this 'example'...
# MIRBot only looks for modules with a class.
class example:
	# You need to initiate your module. Core object will be passed
	# to the class. You can therefore access the core functions.
	def __init__(self, core):
		# Make core accessible to the rest of the module.
		self.core = core

		# Put your basic commands in the following dictionary. This is for
		# Functions accessible to regular users.
		self.basic_help = {
			'example': 'An example function.',
			'dummy': 'This is a dummy function, it will do nothing!'
		}

		# For functions requiring user promotion put them in the following
		# Dictionary. It is only visible to users in the promoted list.
		self.promoted_help = {
			'promotedexample': 'An example of promoted user function'
		}

		# For functions requiring user login put them in the following
		# Dictionary. It is only visible to logged in users.
		self.oper_help = {
			'operexample': 'An example of oper function'
		}

		# For functions you want to run on changes to buffer, add them to this
		# list. The methods must be prefixed with o_, below ignore the o_
		# prefix, it will be added by core. Again, make unique and ref in the
		# OnLoad()
		self.on_commands = {
			'TOPIC': ['example']
		}

	# This is the hook for importing user help functions into core.
	def au_help(self):
		return self.basic_help

	# This is the hook for importing promoted user help functions into core.
	def ap_help(self):
		return self.promoted_help

	# This is the hook for importing oper help functions into core.
	def ao_help(self):
		return self.oper_help

	# This is the hook for loading "On commands", functions triggered by
	# buffer changes.
	def onLoad(self):
		return self.on_commands

	# This is an example function. Stupidly basic.
	# All module methods will be given the buffer text as an argument.
	# eg. strBufferText = "!example blah blah"
	def u_example(self, strBufferText):
		self.core.notice("This is an example function! %s" % strBufferText)
		return True

	# This is an oper function. Again, basic.
	# All module methods will be given the buffer text as an argument.
	# eg. strBufferText = "!operexample blah blah"
	def u_operexample(self, strBufferText):
		# Check we have a login before doing anything.
		if self.core.hasAccess(self.core.buffer['user_host']):
			self.core.notice("This is an example oper function! %s"
				% strBufferText)
		else:
			self.core.notice("Access Denied!")

		return True

	# Onload function example. This will be executed when the buffer changes.
	# Remember: these functions will receive a dictionary of the current
	# buffer. Use this as it is most likely to be correct.
	def o_example(self, aBuffer):
		# I listen for topic.
		self.core.pm("The topic has changed: %s."
			% aBuffer['text'].replace("*TOPIC: :", ''),	aBuffer['channel'])

		return True
