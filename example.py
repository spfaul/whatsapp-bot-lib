import wa
import selenium

import pathlib # optional
import os # optional


# initialise bot 
bot = wa.WhatsApp(
        wait=10, # amount of time to wait for whatsapp page to load
        pathToDriver='driver/chromedriver.exe', # path to your chromedriver executable
        session=f'{pathlib.Path().absolute()}\\mySession' # absolute path of session folder, so no need to rescan
                                                          # the QR Code on every run. 
    )
command_helper = wa.CommandHandler(commPrefix='/') # initialize built in command handler 
print('BOT HAS BEEN INITIALIZED')

# constants
CONTACT = 'COOL GROUP CHAT' # the contact name of the whatsapp group/contact to send to

####### COMMANDS ########

class Commands:
    def __init__(self, bot):
        self.msg_sender = None
        self.bot = bot

    def updateInfo(self, msg_sender):
        self.msg_sender = msg_sender

    def whoami(self, args, kwargs):
        """
        outputs the user who invoked the command
        Example Usage: /[COMMANDNAME] 

        # ARGS
                None
        # KWARGS
                None
        """
        if not self.msg_sender: # exit if cannot detect message sender
            return
        self.bot.send_message(CONTACT, self.msg_sender)

    def add2Nums(self, args, kwargs):
        """
        outputs the sum of 2 integers
        Example Usage: /[COMMANDNAME] 3 4 pretty=true

        # ARGS
                numA (int): mandatory argument : first number to add 
                numB (int): mandatory argument : second number to add 
        # KWARGS
                pretty (bool): optional argument: outputs in a "prettier" format
        """
        if len(args) != 2: # we only need 2 args
            return

        # args and kwargs are passed as strings, so we
        # have to convert them to our desired type
        numA = wa.strToInt(args[0]) # returns None if argument not convertable to int
        numB = wa.strToInt(args[1])
        doPretty = wa.getKwarg(kwargs, 'pretty', 'false') # false is default value

        if None in [numA, numB]: # if mandatory arguments are invalid, exit
            return

        # calculate total and send
        total = numA + numB
        if doPretty == 'true':
            self.bot.send_message(CONTACT, f'The total is {total}')
        else:
            self.bot.send_message(CONTACT, str(total))


# add our commands to the command helper
# NOTE: you don't have to use classes, i only
#       use it to update message info for /whoami.
comms = Commands(bot)
command_helper.add('whoami', comms.whoami)
command_helper.add('add', comms.add2Nums)

#########################

# go to the target contact chat
bot.goto_contact(CONTACT) 

while True:
    # if the window has been closed, exit
    if not bot.isWindowOpen():
        os.system('taskkill /F /IM chromedriver.exe') # this kills all running chromedriver proccesses
                                                      # but shuts down the bot faster (FOR WINDOWS)
        bot.quit_browser()
        break

    # fetch all messages
    msgs, msgs_info = bot.get_all_message_blind()
    if msgs == None or msgs_info == None:
        continue
    # get latest message
    latest_msg = msgs[-1]
    latest_msg_sender = msgs_info[-1]

    # update global info for commands (in this case the sender of the latest message)
    comms.updateInfo(latest_msg_sender)

    # pass latest message to command helper
    command_helper.process(latest_msg)


print('BOT HAS SHUT DOWN')

