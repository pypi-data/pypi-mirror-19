#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# MIRbot Class
# (Modular Information Retrieval bot)
# ----------------------------------------------------------------------------
# Written by Xan Manning
# ----------------------------------------------------------------------------
#
# Copyright (c) 2017 PyratLabs (http://pyrat.io)
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

# Import standard modules required for core module.
import importlib
import time
import datetime
import sys
import os
import shutil
import socket
import ssl
import string
import json
import random
import hashlib
import sqlite3
import smtplib

from mirbot.defaults import config

# Define our core class.
class MIRCore:
    # Initiate the core module.
    def __init__(self, arg_config = {}, args = {}):
        # Variables for storing globally accessible data.
        # These are never reset on reconnect.
        # Schema version.
        self.version = 3002

        # User's Homedir Configuration
        if 'home' not in args:
            self.home = os.path.expanduser("~/.mirbot")
        else:
            print("Setting config directory: %s" % args['home'])
            self.home = args['home']

        # Does homedir exist? If not create it.
        if not os.path.isdir(self.home):
            os.mkdir(self.home, 0o700)

            # Copy over the defaults file.
            for syspath in sys.path:
                if os.path.isfile(syspath + "/mirbot/defaults.py"):
                    shutil.copyfile(syspath + "/mirbot/defaults.py",
                                   self.home + "/config.py")
                    break

        # Register Homedir configuration in Python sys path
        if self.home not in sys.path:
            sys.path.append(self.home)

        # Has a configuration been specified on init?
        if len(arg_config) > 0:
            self.config = arg_config
        else:
            # Is there a config file in our homedir? If so, use it.
            if os.path.isfile(self.home + "/config.py"):
                self.importConfiguration()
            else:
                self.config = config

        self.dbFile = None
        self.dbConn = None
        self.loaded_modules = {}
        self.module_instance = {}

        # Load default help dictionaries
        self.defaultHelp()

        # Load variables that are reset on reconnect
        self.clean()

        # Functions to run at init.
        self.checkDbExists()
        self.updateSchema()
        self.loadConfiguration()
        self.loadModules()

        # Load help from the loaded modules as well as "on commands"
        self.moduleHelp()
        self.loadOnCommands()


    # Clean up arrays to be all fresh for a new session
    def clean(self, bConfReload = False):
        # Empty the socket
        self.socket = None
        self.reconnect = True

        # Clear the buffer
        self.buffer = {
            'text': '',
            'username': '',
            'channel': '',
            'command': ''
        }

        # Clear the joined channels
        self.joined_channels = []

        # Clear sessions
        self.users = {}
        self.on_commands = {
            'PING': [],
            'JOIN': [],
            'PART': [],
            'MODE': [],
            'QUIT': [],
            'NICK': [],
            'KICK': [],
            'TOPIC': [],
            'NOTICE': [],
            'PRIVMSG': [],
            'ERROR': [],
            'INVITE': [],
        }

        # Default the help dictionaries
        self.defaultHelp()

        # Remove all loaded modules, clear the instances.
        self.loaded_modules = {}
        self.module_instance = {}

        # Clear flood Information
        self.config['flood'] = {
            'start': 0,
            'count': 0
        }

        # Reload the modules if reconnecting, recreate the instances.
        if bConfReload:
            self.loadModules()
            self.loadConfiguration()
            self.moduleHelp()
            self.loadOnCommands()


    # Method for defining the default help dictionaries
    def defaultHelp(self):
        loginHelp = 'Lets you login to %s' \
            ' Syntax: /msg %s %slogin username password' \
            % (self.config['nick'], self.config['nick'], self.config['prefix'])

        # Help dictionaries
        self.module_help = [{
            'about': 'Information about bot.',
            'login': loginHelp,
            'seen': 'See a users last recorded action.'
        }]

        self.module_promoted_help = []

        self.module_oper_help = [{
            'nick': 'Change the bot nickname.',
            'restart': 'Restart Bot. (refreshes modules)',
            'join': 'Tell Bot to join a Channel.',
            'part': 'Tell Bot to leave a Channel.',
            'rejoin': 'Rejoin all Channels bot is assigned to.',
            'disconnect': 'Disconnect Bot.',
            'logging': 'Enable/Disable Logging.',
            'adduser': 'Add a User.',
            'deluser': 'Delete a User.',
            'ignore': 'Ignore a User.',
            'listento': 'Stop ignoring a User.',
            'promote': 'Promote a user.',
            'demote': 'Remove a user promoted status.',
            'welcoming': 'Enable/Disable Welcoming.',
            'welcomemsg': 'Alter the Welcome Message.',
            'prefix': 'Change the Bot function prefix.',
            'vaccum': 'Run VACUUM; command on SQLite3 DB',
            'clearlog': 'Truncate the log file.'
        }]



    # Method to check the SQLite3 exists/
    def checkDbExists(self):
        # Set the file name accessible to all.
        self.dbFile = self.home + "/" \
            + self.config['data_dir'] \
            + "/" + self.config['sqlite_db']

        # Check directory exists?
        if not os.path.isdir(self.home + "/" + self.config['data_dir']):
            os.mkdir(self.home + "/" + self.config['data_dir'], 0o700)

        # Does the file exist? If not create it, else continue.
        if os.path.isfile(self.dbFile):
            print("----------------------------------------------------------")
            print("Connecting to Database...")
            print("----------------------------------------------------------")
            self.dbConn = sqlite3.connect(self.dbFile)
        else:
            print("----------------------------------------------------------")
            print("Installing Database")
            print("----------------------------------------------------------")
            self.dbConn = sqlite3.connect(self.dbFile)
            c = self.dbConn.cursor()

            print("Creating log table...")
            c.execute("CREATE TABLE logs"
                + " (Datestamp INT NOT NULL, Command TEXT,"
                + " Channel TEXT, Username TEXT, Text TEXT);")

            print("Creating ignored user table...")
            c.execute("CREATE TABLE ignored (Username TEXT);")

            print("Creating promoted user table...")
            c.execute("CREATE TABLE promoted (Username TEXT);")

            print("Creating bot assignment table...")
            c.execute("CREATE TABLE botassign (Channel TEXT, Username TEXT);")

            print("Creating user recognised table...")
            c.execute("CREATE TABLE recognised"
                + " (Time INT, Username TEXT, Channel TEXT, Action TEXT);")

            print("Creating user table...")
            c.execute("CREATE TABLE users"
                + " (Username TEXT, Password TEXT, Salt TEXT);")

            print("Creating variables table...")
            c.execute("CREATE TABLE variables"
                + " (Name TEXT NOT NULL UNIQUE, Value TEXT);")

            print("Commit. Done.")
            # Commit queries.
            self.dbConn.commit()

            # Add a salt to the database.
            print("Generating salt...")
            self.set_variable("salt", self.generateSalt(32))

            print("Setting database version...")
            self.set_variable("db_version", self.version)

            print("Insert. Done.")

        return True


    # Update from latest 2.x.x release to 3.x.x
    def update_3000(self):
        return True


    # Method for processing schema updates.
    def updateSchema(self):
        # Get the schema version.
        schemaVersion = self.get_variable('db_version', self.version)

        # If schema version is less than code version
        if schemaVersion < self.version:
            print("Schema is out of date.")
            for i in range((self.version - schemaVersion) + 1):
                u = 2000 + i
                # Is an update available for this version?
                if self.methodExistsInClass("update_%s" % u):
                    # Apply it.
                    print("Applying update %s." % u)
                    self.callMethodInClass("update_%s" % u)

            # Set the schema version now we have applied updates.
            print("Updated database version.")
            self.set_variable('db_version', self.version)

        return True


    # Method to execute a single query
    def db_exec(self, strQuery, aArgs = ()):
        # Make a cursor
        c = self.dbConn.cursor()
        # Execute the query
        c.execute(strQuery, aArgs)

        # Commit
        return self.dbConn.commit()


    # Method to query a database and return the output as dictionary
    def db_query(self, strQuery, aArgs = (), bCount = False):
        # Make a row_factory
        self.dbConn.row_factory = sqlite3.Row
        # Make a cursor
        c = self.dbConn.cursor()

        # Execute the query
        c.execute(strQuery, aArgs)

        # Result list
        results = []

        # Return the results
        if bCount == True:
            return len(c.fetchall())
        else:
            for row in c.fetchall():
                results.append(dict(row))

            return results


    # Set varbaibles
    def set_variable(self, varName, varValue):
        # Make sure the variable is serialized nicely. We use JSON.
        varValue = json.dumps(varValue)

        # Does the variable already exist?
        varCheck = self.db_query("SELECT Name FROM variables" \
            " WHERE Name = ?;", (varName,), True)

        # If yes, update the variable.
        if varCheck > 0:
            query = self.db_exec("UPDATE variables SET Value = ?" \
                " WHERE Name = ?;", (varValue, varName))
        # Else, create the variable.
        else:
            query = self.db_exec("INSERT INTO variables (Name, Value)" \
                " VALUES (?, ?);", (varName, varValue))

        # Returnt he state of the query.
        return query



    # Get varbaibles
    def get_variable(self, varName, varDefault = None):
        # Query to get the variable.
        result = self.db_query("SELECT Value FROM variables" \
            " WHERE Name = ?;", (varName,))

        # If we don't have a result, return the Default.
        if result == None or len(result) < 1:
            return varDefault
        # Else return the value we want in Pyhton format.
        else:
            return json.loads(result[0]['Value'])

        return False


    # Generate a salt for use in password hashing.
    def generateSalt(self, saltLength):
        # Our choice of characters
        pool = string.ascii_letters + string.digits + string.punctuation
        # Empty variable to store our salt
        salt = ""

        # Generate out salt.
        for i in range(saltLength):
            salt = ("%s%s" % (salt, random.SystemRandom().choice(pool)))

        # Return the salt.
        return salt


    # Load initial configuration from database.
    def loadConfiguration(self):
        # Tell the world we are doing this.
        print("----------------------------------------------------------")
        print("Loading Updated Configuration...")
        print("----------------------------------------------------------")

        # Cycle configurations.
        for confName in self.config:
            self.config[confName] = self.get_variable(confName,
                self.config[confName])


    # Method to import configuration file.
    def importConfiguration(self):
        # Tell the world we are doing this.
        print("----------------------------------------------------------")
        print("Importing config from %s/config.py" % self.home)
        print("----------------------------------------------------------")

        config = importlib.import_module("config").config
        self.config = config

        print("Loaded: %s/config.py" % self.home)

        return True


    # Method to dynamically load modules.
    def loadModules(self):
        # Tell the world we are doing this.
        print("----------------------------------------------------------")
        print("Loading Modules...")
        print("----------------------------------------------------------")

        self.module_dir = self.home + "/modules"

        #  Create if ./modules/ dir exists
        if not os.path.isdir(self.module_dir):
            os.mkdir(self.module_dir, 0o700)

            # Copy any pre-loaded default modules.
            for syspath in sys.path:
                module_syspath = syspath + "/mirbot/modules"
                if os.path.isdir(module_syspath):
                    for defaultModule in os.listdir(module_syspath):
                        # Is this a python file?
                        if defaultModule[-3:] == ".py":
                            source = module_syspath + "/" + defaultModule
                            target = self.home + "/modules/" + defaultModule
                            shutil.copyfile(source, target)

        # Foreach file in ./modules/ dir
        for moduleName in os.listdir(self.module_dir):
            # Skip files with __ prefix or non .py files
            if moduleName[0:2] == "__" or moduleName == "__init__.py":
                print("Skipped: " + moduleName.replace(".py", ""))
                continue
            else:
                # As long as it is a .py file, import.
                if moduleName[-3:] == ".py":
                    # Index for module name
                    moduleIndex = moduleName[:-3]

                    # Import class module and assoc methods.
                    if moduleIndex not in self.loaded_modules:
                        self.loaded_modules[moduleIndex] = getattr(
                            importlib.import_module(
                                "modules.%s" % moduleName[:-3]),
                                "%s" % moduleName[:-3])

                        self.module_instance[moduleIndex] = \
                             self.loaded_modules[moduleIndex](self)

                        print("Loaded: " + moduleName.replace(".py", ""))

        return True


    # Call a loaded module.
    def callMethod(self, methodName, methodArgs):
        # Return class containing our method
        className = self.methodExists(methodName)
        if className != False:
            getattr(self.module_instance[className], methodName)(methodArgs)
        else:
            return False

        return True


    # Find out if our method exists.
    def methodExists(self, methodName):
        # For each module class name in loaded modules.
        for className in self.loaded_modules:
            # For each method name in the loaded modules list
            if methodName in dir(self.module_instance[className]):
                return className

        return False


    # Check we have a method in this class
    def methodExistsInClass(self, methodName):
        # check if the method exists in self
        if methodName in dir(self):
            return True
        else:
            return False


    # Call a method in this class.
    def callMethodInClass(self, methodName):
        # Does it exist?
        if self.methodExistsInClass(methodName):
            getattr(self, methodName)()
        else:
            return False


    # Method for starting our connection.
    def connect(self):
        # Tell the world we are doing this.
        print("----------------------------------------------------------")
        print("Connecting to IRC Server...")
        print("----------------------------------------------------------")

        # Set our socket connection up. Put it into globally accessible
        # Variable so we can use it to listen to.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Wrap SSL if required.
        if self.config['ssl']:
            self.socket = ssl.wrap_socket(self.socket)

        # Try establish a connection, throw a wobbly if cannot connect.
        try:
            self.socket.connect((self.config['server'], self.config['port']))
        except Exception as e:
            print("Cannot connect to %s on port %d: %s"
                % (self.config['server'], self.config['port'], e))
            exit(1)

        # Send password to the server if one is required
        if self.config['password']:
            self.send("PASS %s" % self.config['password'])

        # Send our identification details to the server.
        self.send("NICK %s" % self.config['nick'])
        self.send("USER %s %s %s :%s"
            % (self.config['nick'],
            self.config['owner'],
            self.config['owner'],
            self.config['name'])
        )

        # Above may take a while.
        print("Please wait...")

        # Set our buffer object to blank.
        self.buffer['all'] = ""
        self.buffer['old'] = ""

        return True

    # Method for closing our connection
    def disconnect(self):
        # Tell the world we are doing this.
        print("----------------------------------------------------------")
        print("Closing connection...")
        print("----------------------------------------------------------")

        if self.socket:
            self.send("QUIT :Goodbye!")
            self.socket.close()


        self.reconnect = False

        print("Connection closed!")

        exit(0)
        return True



    # Method for reconnecting
    def restart(self):
        # Tell the world we are doing this.
        print("----------------------------------------------------------")
        print("Restarting...")
        print("----------------------------------------------------------")

        if self.socket:
            self.send("QUIT :I'll be back!")
            self.reconnect = True
            self.socket = False

        print("Connection closed!")

        return True



    # Method for parsing buffer
    def parseBuffer(self, lineBuffer):
        # Create empty dicitonary for output buffer.
        outbuffer = {}

        # Split the buffer into it's componant parts
        buffer = lineBuffer.split(' ', 3)

        # Are we dealing with user buffer?
        if buffer[0].find("!") < 0:
            return True

        # Temporary cut for the username
        cut = buffer[0].split("!", 2)

        # Temporary cut for inted
        if len(cut[1]) > 0:
            chop = cut[1].split("@")
        else:
            chop = ()
            chop[0] = ""

        hostname_start = buffer[0].find("@") + 1

        # Output buffer dictionary.
        outbuffer['username'] = cut[0].replace(":", "")
        outbuffer['inted'] = chop[0]
        outbuffer['hostname'] = buffer[0][hostname_start:]
        outbuffer['user_host'] = buffer[0][1:]
        outbuffer['_channel'] = buffer[2].replace(":", "")
        outbuffer['command'] = buffer[1].upper()
        outbuffer['all'] = lineBuffer

        if outbuffer['command'] == "JOIN":
            # Someone is joining the channel we are in...
            outbuffer['text'] = "*JOINS: %s (%s)" \
                % (outbuffer['username'], outbuffer['user_host'])
            outbuffer['command'] = "JOIN"
            outbuffer['channel'] = outbuffer['_channel'].replace("\r", '')
            outbuffer['action'] = "Idle"

            if self.config['welcome_new'] == True \
                and outbuffer['username'] != self.config['nick']:
                self.notice(self.config['welcome_message'].replace('{NICK}',
                    outbuffer['username']).replace('{CHANNEL}',
                        outbuffer['channel']),
                    outbuffer['username'])

            self.onCommand(outbuffer)
            self.seenLog(
                outbuffer['username'],
                outbuffer['channel'],
                outbuffer['action'])

        elif outbuffer['command'] == "QUIT":
            # Someone is quitting from the server
            outbuffer['text'] = "*QUITS: %s (%s)" \
                % (outbuffer['username'], outbuffer['user_host'])
            outbuffer['command'] = "QUIT"
            outbuffer['channel'] = outbuffer['_channel']
            outbuffer['action'] = "Leaving"

            self.onCommand(outbuffer)
            self.seenLog(
                outbuffer['username'],
                outbuffer['channel'],
                outbuffer['action'])

        elif outbuffer['command'] == "NOTICE":
            # Someone is sending a notice...
            outbuffer['text'] = "*NOTICE: %s" % outbuffer['username']
            outbuffer['command'] = "NOTICE"
            outbuffer['channel'] = outbuffer['_channel']
            outbuffer['action'] = "Sending a Notice"

            self.onCommand(outbuffer)
            self.seenLog(
                outbuffer['username'],
                outbuffer['channel'],
                outbuffer['action'])

        elif outbuffer['command'] == "PART":
            # Someone is parting the channel
            outbuffer['text'] = "*PARTS: %s (%s)" \
                % (outbuffer['username'], outbuffer['user_host'])
            outbuffer['command'] = "PART"
            outbuffer['channel'] = outbuffer['_channel']
            outbuffer['action'] = "Parting"

            self.onCommand(outbuffer)
            self.seenLog(
                outbuffer['username'],
                outbuffer['channel'],
                outbuffer['action'])

        elif outbuffer['command'] == "MODE":
            # Someone is setting a mode
            outbuffer['text'] = "%s sets mode: %s" \
                % (outbuffer['username'], buffer[3].replace("\r", ""))
            outbuffer['command'] = "MODE"
            outbuffer['channel'] = outbuffer['_channel']
            outbuffer['action'] = "Changing mode"

            self.onCommand(outbuffer)
            self.seenLog(
                outbuffer['username'],
                outbuffer['channel'],
                outbuffer['action'])

        elif outbuffer['command'] == "NICK":
            # Someone is changing nickname
            outbuffer['text'] = "*NICK: %s => %s (%s)" \
                % (outbuffer['username'],
                buffer[2][1:],
                outbuffer['user_host'])
            outbuffer['command'] = "NICK"
            outbuffer['channel'] = outbuffer['_channel']
            outbuffer['action'] = "Changing nickname"

            self.onCommand(outbuffer)
            self.seenLog(
                outbuffer['username'],
                outbuffer['channel'],
                outbuffer['action'])

        elif outbuffer['command'] == "TOPIC":
            # Someone is changing channel topic
            outbuffer['text'] = "*TOPIC: %s" % buffer[3].replace("\r", "")
            outbuffer['command'] = "TOPIC"
            outbuffer['channel'] = outbuffer['_channel']
            outbuffer['action'] = "Changing Topic"

            self.onCommand(outbuffer)
            self.seenLog(
                outbuffer['username'],
                outbuffer['channel'],
                outbuffer['action'])

        elif outbuffer['command'] == "KICK":
            # Someone is kicking another user
            otherUser = buffer[3].split("\n").replace("\r", "")
            outbuffer['text'] = "%s KICKS: %s" \
                % (outbuffer['username'], otherUser[0])
            outbuffer['command'] = "KICK"
            outbuffer['channel'] = outbuffer['_channel']
            outbuffer['action'] = "Kicking"

            self.onCommand(outbuffer)
            self.seenLog(
                outbuffer['username'],
                outbuffer['channel'],
                outbuffer['action'])

        else:
            # Someone is talking...
            outbuffer['text'] = buffer[3][1:].replace("\r", "")
            outbuffer['command'] = buffer[1]

            if buffer[2][:1] == "#":
                outbuffer['channel'] = buffer[2]
            else:
                outbuffer['channel'] = outbuffer['username']

            outbuffer['action'] = "Talking"

            self.onCommand(outbuffer)
            self.seenLog(
                outbuffer['username'],
                outbuffer['channel'],
                outbuffer['action'])


        self.buffer = outbuffer
        self.log(outbuffer)

        return outbuffer


    # Method for returning time since...
    # http://flask.pocoo.org/snippets/33/
    # http://stackoverflow.com/a/1551394/4063448
    def timeSince(self, datestamp):
        # Use datetime.
        datestamp = self.unix2datetime(datestamp)
        # Our current datetime.
        now = self.unix2datetime(self.unixtime())

        # Difference between times
        diff = now - datestamp

        # Sort our the format of our string.
        if diff.days == 0:
            if diff.seconds < 10:
                return "a few seconds"
            elif diff.seconds < 60:
                return "%d seconds" % diff.seconds
            elif diff.seconds < 120:
                return "about a minute"
            elif diff.seconds < 3600:
                return "%.1f minutes" % (diff.seconds / 60)
            elif diff.seconds < 7200:
                return "1 hour and %.1f minutes" % ((diff.seconds - 3600) / 60)
            elif diff.seconds < 86400:
                return "%.1f hours" % (diff.seconds / 3600)
        else:
            if diff.days == 1:
                return "1 day and %.1f hours" % ((diff.seconds) / 3600)
            elif diff.days < 7:
                return "%d days" % (diff.days)
            elif diff.days < 30:
                return "%d weeks" % (diff.days / 7)
            elif diff.days < 365:
                return "%d months" % (diff.days / 30)
            else:
                return "%.1f years ago" % (diff.days / 365)

        return "just now"


    # Method to check if user is ignored...
    def checkIgnored(self, username):
        # Username to search by
        username = username.lower()

        userCheck = self.db_query(
            "SELECT * FROM ignored WHERE Username = ?;",
            (username,),
            True)

        if userCheck > 0:
            return True
        else:
            return False


    # Method to check if user is promoted...
    def checkPromoted(self, username):
        # Username to search by
        username = username.lower()

        userCheck = self.db_query(
            "SELECT * FROM promoted WHERE Username = ?;",
            (username,),
            True)

        if userCheck > 0:
            return True
        else:
            return False


    # Load onCommands from modules.
    def loadOnCommands(self):
        # Tell the world we are doing this.
        print("----------------------------------------------------------")
        print("Hooking event triggers...")
        print("----------------------------------------------------------")

        # Foreach class in loaded_modules
        for className in self.loaded_modules:
            # For each method name in the loaded modules list
            print("Checking %s..." % className)
            if 'onLoad' in dir(self.module_instance[className]):
                print("Found onCommands for %s" % className)
                module_on_commands = self.module_instance[className].onLoad()
                for listener in module_on_commands:
                    for command in module_on_commands[listener]:
                        self.on_commands[listener].append(command)

        return True



    # Method for triggering events on buffer input
    def onCommand(self, buffer):
        # Do we have an array?
        if len(self.on_commands[buffer['command']]) < 1:
            return True

        # Commands in this event
        event_commands = self.on_commands[buffer['command']]

        # Are we ignoring this user?
        if self.checkIgnored(buffer['username']) == True:
            return True

        # OnCommands
        for className in self.loaded_modules:
            for command in event_commands:
                method_name = "o_%s" % command

                # Check method exists
                if method_name in dir(self.module_instance[className]):
                    getattr(self.module_instance[className],
                        method_name)(buffer)

        return True


    # Keeping a record of users we have seen...
    def seenLog(self, username, channel, action):
        # Username to lower.
        username = username.lower()

        # Check Query
        checkQuery = "SELECT * FROM recognised WHERE Username = ?;"

        # Is the user in the DB?
        userCheck = self.db_query(checkQuery, (username,), True)

        if userCheck > 0:
            updateQuery = "UPDATE recognised" \
                " SET Time = ?, Channel = ?, Action = ?" \
                " WHERE Username = ?;"

            self.db_exec(updateQuery,
                (self.unixtime(), channel, action, username))
        else:
            insertQuery = "INSERT INTO recognised" \
                " (Time, Channel, Action, Username)" \
                " VALUES (?, ?, ?, ?)"

            self.db_exec(insertQuery,
                (self.unixtime(), channel, action, username))

        return True


    # Function for sending data to the IRC server
    def send(self, strCommand):
        # Time format
        timef = self.date_formatted()

        # Flood protection.
        if self.config['avoid_flooding']:
            if self.config['flood']['start'] == 0 \
                or (self.config['flood']['start'] \
                    + self.config['flood_timeout']) < self.unixtime():
                self.config['flood']['start'] = self.unixtime()
                self.config['flood']['count'] = 1
            else:
                if self.config['flood']['count'] \
                        % self.config['flood_count'] == 0 \
                    and self.config['flood']['count'] > 0:
                    time.sleep(self.config['flood_wait'])
                    self.config['flood']['start'] = 0
                    self.config['flood']['count'] = 0
                else:
                    self.config['flood']['start'] = self.unixtime()
                    self.config['flood']['count'] += 1

        self.b_print("[ %s ] <- %s" % (timef, strCommand))
        # Send command to the server.
        if len(strCommand) > 0:
            return self.socket.send(bytes(strCommand + "\n", "UTF-8"))

        return True


    # Print buffer to the screen
    def b_print(self, strBuffer):
        # We only want the text bit. I know, lazy, but I want to maintain
        # Screen buffer format.
        tmp = strBuffer.split(" <- ", 1)
        if len(tmp) < 2:
            tmp = strBuffer.split(" -> ", 1)

        # Don't start with a :
        if tmp[1][:1] == ":":
            tmp[1] = tmp[1][1:]

        print(strBuffer)


    # Define a method for sending email
    def send_mail(self, email_to, email_subject, email_message):
        # Make sure we can send email.
        if self.config['allow_sendmail'] == False:
            return False

        header = 'To: <%s>\nFrom: %s <%s>\nSubject: %s\n\n' % (email_to,
            self.config['nick'],
            self.config['allow_sendmail'],
            email_subject)

        message = """%s

        %s

        ---
        This message was sent via an IRC bot on %s. If you did not wish to
        receive this email, please contact %s on that IRC network.
        """ % (header,
            email_message,
            self.config['server'],
            self.config['owner'])

        try:
            mail_server = smtplib.SMTP('localhost', 25)
            mail_server.sendmail(self.config['allow_sendmail'],
                email_to,
                message)
            return True
        except ConnectionRefusedError:
            return False
        except smtplib.SMTPDataError:
            return False
        except smtplib.SMTPConnectError:
            return False
        except smtplib.SMTPException:
            return False


    # Lets return unix timestamp.
    def unixtime(self):
        datetimestamp = datetime.datetime.utcnow().strftime("%s")
        return int(datetimestamp)


    # unixtime to datetime
    def unix2datetime(self, iUnixTime):
        return datetime.datetime.fromtimestamp(iUnixTime)


    # formatted date correctly.
    def date_formatted(self):
        return datetime.datetime.now().strftime(self.config['date_format'])


    # Trim the logs a number of days
    def trimLogs(self):
        # Are we allowed to trim logs?
        if self.config['logging_trim']:
            self.config['log_check'] = self.get_variable('log_check')
            last_check = self.config['log_check']
            now = self.unixtime()

            # If the last check of logs was a day ago...
            if (now - last_check) >= 86400:
                trim_after = now - (self.config['logging_trim'] * 86400)

                # Time format
                timef = self.date_formatted()
                self.b_print("[ %s ] <- %s" % (timef, "Auto-Trimmed Logs"))

                self.db_exec("DELETE FROM logs" \
                    " WHERE Datestamp <= ?;", (trim_after,))
                self.set_variable('log_check', now)

        return True


    # Ping Event Handler - Specific handler
    def pingHandler(self):
        # Trim logs if necessary for PING.
        self.trimLogs()

        return True


    # Create the listener.
    def listen(self):
        # While socket is open, add to the buffer dictionary
        while self.socket:
            # Time format
            timed = datetime.datetime.now()
            timef = timed.strftime(self.config['date_format'])

            # Get buffer from socket
            self.buffer['recv'] = self.socket.recv(4096)
            self.buffer['all'] = self.buffer['recv'].decode("UTF-8", 'ignore')

            # for each line in the buffer
            for line in str.split(self.buffer['all'], "\n"):
                # Empty line? Let's finish
                if len(line) <= 0:
                    break

                # Re-set buffer to this line.
                self.buffer['all'] = line

                # Is this a private message? Make sure we don't show this
                # message, it may contain passwords.
                if line.find("PRIVMSG " + self.config['nick'] + " :") > 0:
                    self.b_print("[ %s ] -> [ PRIVATE MESSAGE ]" % timef)
                else:
                    self.b_print("[ %s ] -> %s" % (timef, line))

                # Ping? Send a pong. Else parse buffer and process commands.
                if line[0:6] == "PING :":
                    self.send("PONG :%s" % line[6:])
                    self.pingHandler()
                elif line[0:7] == "ERROR :":
                    self.parseBuffer(line)
                    self.processCommands()
                    self.disconnect()
                else:
                    self.parseBuffer(line)
                    self.processCommands()

                # Did we get a pong. Great, I don't care.
                if line.find("PONG") > 0:
                    break

                # Send some pings to make sure the server knows we are
                # alive and well.
                if line.find("376") > 0 or line.find("255") > 0:
                    self.send('PING :%s' % self.config['server'])

                # Hold this buffer for retrieving past info.
                self.buffer['old'] = line



    # Adding to the logging database
    def log(self, aBuffer):
        if aBuffer['username'] == aBuffer['channel'] \
            and aBuffer['command'] == "PRIVMSG":
            bufferText = "[ PRIVATE MESSAGE ]"
        else:
            bufferText = aBuffer['text']

        # If logging enabled... Write log
        if self.config['logging'] == True:
            return self.db_exec("INSERT INTO logs (Datestamp, Command," \
                " Channel, Username, Text) VALUES (?, ?, ?, ?, ?);",
                (self.unixtime(), aBuffer['command'], aBuffer['channel'],
                aBuffer['username'], bufferText))
        else:
            return True


    # Process Commands
    def processCommands(self):
        # Get the first word of the buffer text.
        tmp = self.buffer['text'].split(" ")
        firstWord = tmp[0]

        # Are we ignoring this user?
        if self.checkIgnored(self.buffer['username']):
            return True

        # Length of the command prefix
        prefixLen = len(self.config['prefix'])
        function = None

        # Is the prefix at the beggining of the first word?
        if firstWord[:prefixLen] == self.config['prefix']:
            # Create the function from the command
            command = firstWord[prefixLen:]
            function = "u_%s" % command

            # If the method is in this class, execute
            if self.methodExistsInClass(function):
                self.callMethodInClass(function)
            # Else execute the method from a module
            elif self.methodExists(function):
                self.callMethod(function, self.buffer['text'])
            else:
                return True

        return True


    # Method for joining a channel
    def join(self, channel):
        # Send the join command
        self.send("JOIN %s" % channel)

        # Are we telling the world we are online? If so send the channel a
        # Message, as per the config.
        if self.config['say_online'] == True:
            self.pm(
                self.config['online_message'].replace("{CHANNEL}", channel),
                channel)

        # Are we setting ourselves as a channel operator?
        if self.config['self_oper'] == True:
            self.send("MODE %s +ao %s %s" %
                (channel, self.config['nick'], self.config['nick']))

        # Add to the array of jouned channels.
        if channel not in dir(self.joined_channels):
            self.joined_channels.append(channel)



    # Method for rejoining channels on reconnect
    def rejoin(self):
        # Join all channels in the config
        if len(self.config['channels']) > 0:
            for channel in self.config['channels']:
                self.join(channel)

        # List of channels we have been assigned to.
        botAssign = self.db_query("SELECT * FROM botassign;")

        # If the list is nice and big.
        if len(botAssign) > 0:
            # Join each channel.
            for toJoin in botAssign:
                self.join(toJoin['Channel'])



    # Method for sending private message.
    def pm(self, strMessage, strTarget = None):
        # Default to the last username in buffer
        if strTarget == None:
            strTarget = self.buffer['username']

        # Set the log buffer for this PM
        aBuffer = {
            'command': 'PRIVMSG',
            'channel': strTarget,
            'username': self.config['nick'],
            'text': strMessage
        }

        # Log what is being PM'd
        self.log(aBuffer)

        # Send PM
        self.send("PRIVMSG %s :%s" % (strTarget, strMessage))



    # Method for sending a notice.
    def notice(self, strMessage, strTarget = None):
        # Default to the last username in buffer.
        if strTarget == None:
            strTarget = self.buffer['username']


        # Set the log buffer for this Notice
        aBuffer = {
            'command': 'NOTICE',
            'channel': strTarget,
            'username': self.config['nick'],
            'text': strMessage
        }

        # Log what is being Noticed
        self.log(aBuffer)

        # Send notice.
        self.send("NOTICE %s :%s" % (strTarget, strMessage))


    # Mehtod to enable logging
    def loggingEnable(self, bool):
        if bool == True:
            self.config['logging'] = True
            self.set_variable('logging', True)
        elif bool == False:
            self.config['logging'] = False
            self.set_variable('logging', False)
        else:
            self.notice("Sorry, I don't know what %s is." % str(bool))

        return True


    # Mehtod to enable welcome message
    def welcomeEnable(self, bool):
        if bool == True:
            self.config['welcome_new'] = True
            self.set_variable('welcome_new', True)
        elif bool == False:
            self.config['welcome_new'] = False
            self.set_variable('welcome_new', False)
        else:
            self.notice("Sorry, I don't know what %s is." % str(bool))

        return True


    # Method to set welcome message
    def welcomeMessage(self, stringMessage = None):
        if stringMessage == None or len(stringMessage) < 1:
            self.notice("Welcome message too short!")
        else:
            self.config['welcome_message'] = stringMessage
            self.set_variable('welcome_message', stringMessage)

        return True


    # Method for finding out if user has access to botmaster stuff.
    def hasAccess(self, userHost, level = 10):
        if len(self.users) < 1:
            return False

        if userHost in self.users:
            timeCheck = self.users[userHost]['time'] \
                + self.config['user_session']
        else:
            return False

        if timeCheck >= self.unixtime():
            if self.users[userHost]['level'] >= level:
                return True

        return False


    # Get help info from loaded modules
    def moduleHelp(self):
        for className in self.loaded_modules:
            # For each method name in the loaded modules list
            if 'au_help' in dir(self.module_instance[className]):
                self.module_help.append(
                    getattr(self.module_instance[className],
                    'au_help')()
                )

            # Add to the promoted list
            if 'ap_help' in dir(self.module_instance[className]):
                self.module_promoted_help.append(
                    getattr(self.module_instance[className],
                    'ap_help')()
                )

            # Add to the oper list
            if 'ao_help' in dir(self.module_instance[className]):
                self.module_oper_help.append(
                    getattr(self.module_instance[className],
                    'ao_help')()
                )

        return True


    # Help method
    def u_help(self):
        # Describe the format of the help
        self.notice("[function]: description")
        self.notice("-")

        # For each module dictioary in help...
        for module_dict in self.module_help:
            for helpFunction in module_dict:
                helpDescription = module_dict[helpFunction]
                # format as [function] description
                self.notice("[%s%s]: %s"
                    % (self.config['prefix'], helpFunction, helpDescription))

        # Show promoted user functions
        if self.checkPromoted(self.buffer['username']) \
            and len(self.module_promoted_help) > 0:
            self.notice("-")
            self.notice("=== Promoted user functions ===")
            self.notice("-")
            for module_dict in self.module_promoted_help:
                for helpFunction in module_dict:
                    helpDescription = module_dict[helpFunction]
                    self.notice("[%s%s]: %s"
                        % (self.config['prefix'],
                           helpFunction,
                           helpDescription))

        # Show botmaster functions
        if self.hasAccess(self.buffer['user_host']):
            self.notice("-")
            self.notice("=== Botmaster functions ===")
            self.notice("-")
            for module_dict in self.module_oper_help:
                for helpFunction in module_dict:
                    helpDescription = module_dict[helpFunction]
                    self.notice("[%s%s]: %s"
                        % (self.config['prefix'],
                           helpFunction,
                           helpDescription))

        return True


    # Information about this bot...
    def u_about(self):
        self.notice("Hi, I'm %s. I am a Modular Information Retrieval (MIR)" \
            " Internet Relay Chat (IRC) bot written by Xan Manning."
            % self.config['nick'])
        self.notice("I am written in Python 3 and I am fully customisable" \
            " with modules.")
        self.notice("You can grab a copy of me from:")
        self.notice("https://github.com/PyratLabs/MIRbot.git")


    # Find out where a user has gone
    def u_seen(self):
        # Get the options
        options = self.buffer['text'].split(" ", 2)

        # If we don't have the right syntax throw a wobbly.
        if len(options) < 2:
            self.notice("Syntax: %sseen [Username]" % self.config['prefix'])
            return None

        # Get data about this user
        userData = self.db_query("SELECT * FROM recognised" \
            " WHERE Username = ?;", (options[1].lower(),))

        # Do we have any data on the user? Share it with the requester.
        if len(userData) > 0:
            userData = userData[0]
            self.notice("[%s] Seen %s ago. %s -> %s"
                % (options[1],
                    self.timeSince(userData['Time']),
                    userData['Action'],
                    userData['Channel']))
        else:
            self.notice("Sorry, not seen %s" % options[1])


    # Authenticate a user.
    def u_login(self):
        # If this is in a public place, do not login!
        if self.buffer['channel'].lower() != self.buffer['username'].lower():
            self.pm("Incorrect login!", self.buffer['channel'])
            self.pm("You may have just compromised your password! Please " \
                "make sure you are logging in via" \
                " /msg %s %slogin [username] [password]"
                % (self.config['nick'], self.config['prefix']),
                self.buffer['username'])
            return False

        # Get username/pass from buffer
        options = self.buffer['text'].split(" ", 3)

        # Check syntax
        if len(options) < 3:
            self.notice("Syntax: /msg %s %slogin [username] [password]"
                % (self.config['nick'], self.config['prefix']))
            return False

        # Grab the latest salt from the database.
        self.config['salt'] = self.get_variable('salt')

        # Set the un variable
        username = options[1].lower()

        # Do we have users in the user table?
        userCount = self.db_query("SELECT * FROM users;", (), True)

        # If there are no users, proceed to create new user.
        if userCount < 1:
            # Is the attempted login from the owner?
            if self.buffer['username'].lower() == self.config['owner'].lower():
                # Generate a salt for this user.
                salt = self.generateSalt(32)

                # Hash the password
                h = hashlib.new(self.config['algorithm'])
                hashStr = "%s:%s:%s" % (self.config['salt'], options[2], salt)

                h.update(bytes(hashStr, 'UTF-8'))

                # Set the password variable
                password = h.hexdigest()

                # Let's create a login
                self.db_exec("INSERT INTO users" \
                    " (Username, Password, Salt) VALUES (?, ?, ?);",
                    (username, password, salt))

                # Authenticate this user.
                self.users[self.buffer['user_host']] = {
                    'time': self.unixtime(),
                    'level': 10
                }

                # Tell them they are logged in
                self.notice("Logged in. (%s. logged in as %s." \
                    " Auto-logout in %d seconds)."
                    % (username,
                        self.buffer['user_host'],
                        self.config['user_session']))

                return True
            else:
                # Don't create a user for anyone else!
                self.notice("You are not the owner," \
                    + " you cannot create a login!")
                return False

        # Grab user Salt
        saltQuery = self.db_query("SELECT Salt FROM users" \
            " WHERE Username = ?", (username,))

        # Grab this user's salt.
        if len(saltQuery) > 0:
            salt = saltQuery[0]['Salt']
        else:
            self.notice("User not found!")
            return False

        # Hash the password
        h = hashlib.new(self.config['algorithm'])
        hashStr = "%s:%s:%s" % (self.config['salt'], options[2], salt)

        h.update(bytes(hashStr, 'UTF-8'))

        # Set the password variable
        password = h.hexdigest()

        # Does the username/password match?
        checkLogin = self.db_query("SELECT * FROM users" \
            " WHERE Username = ? AND Password = ?;", \
            (username, password), True)

        # It does?!
        if checkLogin > 0:
            # Create the session...
            self.users[self.buffer['user_host']] = {
                'time': self.unixtime(),
                'level': 10
            }

            # Tell them they are logged in
            self.notice("Logged in. (%s. logged in as %s." \
                " Auto-logout in %d seconds)."
                % (username,
                    self.buffer['user_host'],
                    self.config['user_session']))

            return True
        else:
            # Wrong password, I'm afraid.
            self.notice("Incorrect login!")



    # Logout when we are finished with our session.
    def u_logout(self):
        # If logged in...
        if self.hasAccess(self.buffer['user_host']):
            # Destroy user session.
            del self.users[self.buffer['user_host']]
            self.notice("Logged out. (%s)" % self.buffer['user_host'])
        else:
            self.notice("Not logged in!")


    # Disconnect command.
    def u_disconnect(self):
        # Has authentication?
        if self.hasAccess(self.buffer['user_host']):
            # Tell us we are disconnecting then do it.
            self.notice("Disconnecting...")
            self.disconnect()
        else:
            self.notice("Access Denied!")


    # Reconnect (restart) command.
    def u_restart(self):
        # Has authentication?
        if self.hasAccess(self.buffer['user_host']):
            # Tell us we are disconnecting then do it.
            self.notice("Restarting...")
            self.restart()
        else:
            self.notice("Access Denied!")



    # User method to join channel
    def u_join(self):
        # Do we have access to join the channel?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        # Get command arguments
        options = self.buffer['text'].split(" ", 2)

        # Is the syntax correct?
        if len(options) < 2 or options[1][:1] != "#":
            self.notice("Syntax: %sjoin [#channel]" % self.config['prefix'])
            return False

        # Are we already in the channel?
        checkJoined = self.db_query("SELECT * FROM botassign" \
            " WHERE Channel = ?;", (options[1],), True)

        # If yes, then rejoin just in case, else add to bot assignment db
        if checkJoined > 0:
            self.notice("I'm already in %s!" % options[1])
            self.join(options[1])
        else:
            self.db_exec("INSERT INTO botassign (Channel, Username)" \
                " VALUES (?, ?);", (options[1], self.buffer['username']))
            self.notice("Joining %s." % options[1])
            self.join(options[1])

        return True


    # User method to rejoin all channels
    def u_rejoin(self):
        # Do we have access to join the channel?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        self.notice("Rejoining all channels...")
        self.rejoin()
        return True



    # User method to join channel
    def u_part(self):
        # Do we have access to part the channel?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        # Get command arguments
        options = self.buffer['text'].split(" ", 2)

        # Is the syntax correct?
        if len(options) < 2 or options[1][:1] != "#":
            self.notice("Syntax: %spart [#channel]" % self.config['prefix'])
            return False

        # Are we already in the channel?
        checkJoined = self.db_query("SELECT * FROM botassign" \
            " WHERE Channel = ?;", (options[1],), True)

        # If yes, then part and remove from db, else part anyways.
        if checkJoined > 0:
            self.notice("Parting %s..." % options[1])
            self.db_exec("DELETE FROM botassign" \
                " WHERE Channel = ?;", (options[1],))
            self.send("PART %s" % options[1])
        else:
            self.notice("I'm not in %s." % options[1])
            self.send("PART %s" % options[1])

        return True



    # User method to change command prefix
    def u_prefix(self):
        # Do we have access to this method?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        # Get command arguments
        options = self.buffer['text'].split(" ", 1)

        # Is the syntax correct?
        if len(options) < 2:
            self.notice("Syntax: %sprefix [prefix]"
                % self.config['prefix'])
            return False

        self.config['prefix'] = options[1].lower()
        self.set_variable('prefix', options[1].lower())
        self.notice("Changed prefix to: %s" % options[1].lower())



    # User method to change command nickname
    def u_nick(self):
        # Do we have access to this method?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        # Get command arguments
        options = self.buffer['text'].split(" ", 2)

        # Is the syntax correct?
        if len(options) < 2:
            self.notice("Syntax: %snick [nickname]"
                % self.config['prefix'])
            return False

        self.config['nick'] = options[1]
        self.set_variable('nick', options[1])
        self.send("NICK %s" % self.config['nick'])
        self.notice("Changed nickname to: %s" % options[1])


    # User method to enable logging
    def u_logging(self):
        # Do we have access to this method?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        # Get command arguments
        options = self.buffer['text'].split(" ", 2)

        # Is the syntax correct?
        if len(options) < 2:
            self.notice("Syntax: %slogging [True/False]"
                % self.config['prefix'])
            return False

        # What are we doing?
        if options[1].lower() == "true":
            bLog = True
            strLog = "Enabled"
        else:
            bLog = False
            strLog = "Disabled"

        self.loggingEnable(bLog)
        self.notice("Logging is %s" % strLog)



    # User method to enable welcoming
    def u_welcoming(self):
        # Do we have access to this method?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        # Get command arguments
        options = self.buffer['text'].split(" ", 2)

        # Is the syntax correct?
        if len(options) < 2:
            self.notice("Syntax: %swelcoming [True/False]"
                % self.config['prefix'])
            return False

        # What are we doing?
        if options[1].lower() == "true":
            bLog = True
            strLog = "Enabled"
        else:
            bLog = False
            strLog = "Disabled"

        self.welcomeEnable(bLog)
        self.notice("Welcoming new users is %s" % strLog)



    # User method to change welcome message
    def u_welcomemsg(self):
        # Do we have access to this method?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        # Get command arguments
        options = self.buffer['text'].split(" ", 1)

        # Is the syntax correct?
        if len(options) < 2:
            self.notice("Syntax: %swelcomemsg [message]"
                % self.config['prefix'])
            return False

        self.welcomeMessage(options[1])
        self.notice("Welcome message changed to: %s" % options[1])



    # User method to add a user
    def u_adduser(self):
        # Do we have access to this method?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        # Get command arguments
        options = self.buffer['text'].split(" ", 3)

        # Grab the latest salt from the database.
        self.config['salt'] = self.get_variable('salt')

        # Generate a salt for this user.
        salt = self.generateSalt(32)

        # Is the syntax correct?
        if len(options) < 3:
            self.notice("Syntax: %sadduser [username] [password]"
                % self.config['prefix'])
            return False

        # Hash the password
        h = hashlib.new(self.config['algorithm'])
        hashStr = "%s:%s:%s" % (self.config['salt'], options[2], salt)

        h.update(bytes(hashStr, 'UTF-8'))

        # Set the un/pw variables
        username = options[1].lower()
        password = h.hexdigest()

        # Do we have users in the user table?
        userCount = self.db_query("SELECT * FROM users" \
            " WHERE Username = ?;", (username,), True)


        if userCount > 0:
            self.notice("User already exists!")
            return False

        self.db_exec("INSERT INTO users (Username, Password, Salt)" \
            " VALUES (?, ?, ?);", (username, password, salt))

        self.notice("New user added: %s" % options[1])



    # User method to delete a user
    def u_deluser(self):
        # Do we have access to this method?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        # Get command arguments
        options = self.buffer['text'].split(" ", 2)

        # Is the syntax correct?
        if len(options) < 2:
            self.notice("Syntax: %sdeluser [username]"
                % self.config['prefix'])
            return False

        # Set the un variables
        username = options[1].lower()

        # Do we have users in the user table?
        userCount = self.db_query("SELECT * FROM users" \
            " WHERE Username = ?;", (username,), True)


        if userCount < 1:
            self.notice("User doesn't exists!")
            return False

        self.db_exec("DELETE FROM users WHERE Username = ?;",
            (username,))

        self.notice("Deleted user: %s" % options[1])



    # User method to ignore a user
    def u_ignore(self):
        # Do we have access to this method?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        # Get command arguments
        options = self.buffer['text'].split(" ", 2)

        # Is the syntax correct?
        if len(options) < 2:
            self.notice("Syntax: %signore [username]"
                % self.config['prefix'])
            return False

        # Do we have users in the ignored table?
        userCount = self.db_query("SELECT * FROM ignored" \
            " WHERE Username = ?;", (options[1].lower(),), True)

        if userCount > 0:
            self.notice("User already ignored!")
            return False

        self.db_exec("INSERT INTO ignored (Username)" \
            " VALUES (?);", (options[1].lower(),))

        self.db_exec("DELETE FROM promoted " \
            " WHERE Username = ?;", (options[1].lower(),))

        self.notice("Ignoring user: %s" % options[1])


    # User method to promote a user
    def u_promote(self):
        # Do we have access to this method?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        # Get command arguments
        options = self.buffer['text'].split(" ", 2)

        # Is the syntax correct?
        if len(options) < 2:
            self.notice("Syntax: %spromote [username]"
                % self.config['prefix'])
            return False

        # Do we have users in the ignored table?
        userCount = self.db_query("SELECT * FROM promoted" \
            " WHERE Username = ?;", (options[1].lower(),), True)

        if userCount > 0:
            self.notice("User already promoted!")
            return False

        self.db_exec("INSERT INTO promoted (Username)" \
            " VALUES (?);", (options[1].lower(),))

        self.db_exec("DELETE FROM ignored " \
            " WHERE Username = ?;", (options[1].lower(),))

        self.notice("Promoted user: %s" % options[1])


    # User method to stop ignoring a user
    def u_listento(self):
        # Do we have access to this method?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        # Get command arguments
        options = self.buffer['text'].split(" ", 2)

        # Is the syntax correct?
        if len(options) < 2:
            self.notice("Syntax: %slistento [username]"
                % self.config['prefix'])
            return False

        # Do we have users in the ignored table?
        userCount = self.db_query("SELECT * FROM ignored" \
            " WHERE Username = ?;", (options[1].lower(),), True)

        if userCount < 1:
            self.notice("User not being ignored!")
            return False

        self.db_exec("DELETE FROM ignored WHERE Username = ?;",
            (options[1].lower(),))

        self.notice("Listening to user: %s" % options[1])


    #User method to stop demote a user
    def u_demote(self):
        # Do we have access to this method?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        # Get command arguments
        options = self.buffer['text'].split(" ", 2)

        # Is the syntax correct?
        if len(options) < 2:
            self.notice("Syntax: %sdemote [username]"
                % self.config['prefix'])
            return False

        # Do we have users in the ignored table?
        userCount = self.db_query("SELECT * FROM promoted" \
            " WHERE Username = ?;", (options[1].lower(),), True)

        if userCount < 1:
            self.notice("User not promoted!")
            return False

        self.db_exec("DELETE FROM promoted WHERE Username = ?;",
            (options[1].lower(),))

        self.notice("Demoted to user: %s" % options[1])


    # User method to vacuum the database
    def u_vacuum(self):
        # Do we have access to this method?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        aBuffer = {
            'command': "VACUUM",
            'channel': self.config['nick'],
            'text': "Vacuumed database.",
            'username': self.buffer['username']
        }

        if sys.version_info > (3,5):
            self.notice("This action is unavailable in Python 3.6+")
        else:
            self.db_exec("VACUUM;")

        self.log(aBuffer)
        self.notice("Database vacuumed.")


    # User method to vacuum the database
    def u_clearlog(self):
        # Do we have access to this method?
        if self.hasAccess(self.buffer['user_host']) == False:
            self.notice("Access Denied!")
            return False

        aBuffer = {
            'command': "CLEAR LOG",
            'channel': self.config['nick'],
            'text': "Cleared IRC Log table.",
            'username': self.buffer['username']
        }

        self.db_exec("DELETE FROM logs WHERE Datestamp > 0;")
        self.log(aBuffer)
        self.notice("Log table has been cleared!.")


    # A test method - Should always return True
    def u_pytest(self):
        return True
