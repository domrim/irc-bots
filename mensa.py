from sopel import module
import requests
from html.parser import HTMLParser
import re

@module.commands('mensa')
@module.require_privmsg()
@module.rate(10)

def mensa(bot, trigger):
    page = requests.get('http://mensa.akk.org')
    ws_text = page.text
    parser = MensaParser()
    parser.feed(ws_text)
    for key in sorted(parser.mensa_dict.keys()):
        bot.say(key+':')
        for food in parser.mensa_dict[key]:
            bot.say('     - '+food)

class MensaParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.mensa_dict = dict()
        self.food_court = str()
        self.food_string = str()
        self.food_list = list()
    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        court = re.match(('^(Linie|L6|Schnitzelbar|Curry Queen:$|Cafeteria|Abend).*:'),data)
        if court:
            food_court_new = court.group(0)
            food_court_new = food_court_new[:-1]
        else:
            food_court_new = None
        if not self.food_court:
            self.food_court = food_court_new
        if self.food_court:
            if data not in [' ','\n','-']:
                if not (food_court_new == self.food_court) and food_court_new :
                    self.mensa_dict[self.food_court] = self.food_list
                    self.food_list = list()
                    self.food_string = str()
                    self.food_court = food_court_new
                elif '€' in data:
                    #self.mensa_dict[self.linie] = self.food_string +' '+data
                    self.food_list += [self.food_string+' '+data]
                    self.food_string = ''
                elif not 'Linie' in data:
                    self.food_string += data

