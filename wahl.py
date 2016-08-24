from sopel import module
import datetime

@module.commands('wahl')
@module.rate(10)
@module.require_privmsg()
def wahl(bot, trigger):
    now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    bot.say('Wahlbeteiligung Stand: '+now)
    with open('/tmp/wahlbet.irc.txt', 'r') as wahlfile:
        for line in wahlfile:
            bot.say(line)
		
