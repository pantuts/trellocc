#!/usr/bin/python2.7
# By: pantuts
# http://pantuts.com
# MIT License
# Dependencies: requests, trello
# sudo pip install requests trello

import json
import sys
from ConfigParser import ConfigParser
from trello import TrelloApi


class TrelloCards:
    def __init__(self, KEY, TOKEN, BOARD_ID, REQUIRED_LIST):
        self.KEY = KEY
        self.TOKEN = TOKEN
        self.BOARD_ID = BOARD_ID
        self.REQUIRED_LIST = REQUIRED_LIST
        self.board_lists = {}
        self.data = {}
        self.trello = TrelloApi(self.KEY, self.TOKEN)


    def get_board_lists(self):
        try:
            print "Checking board's lists..."
            self.board_lists = self.trello.boards.get_list(self.BOARD_ID)
            self.data.update({
                'idBoard': self.board_lists[0]['idBoard'],
                '_boardName': None,
                '_boardShortLink': None
            })
            # returns array of dictionaries
            # print json.dumps(board_lists, indent=4, sort_keys=True)
        except Exception, e:
            print str(e)
            sys.exit(1)


    def get_required_list(self):
        bl = self.board_lists
        print "Getting required list..."
        req_list = next((item for item in bl if item['name'].lower() == self.REQUIRED_LIST.lower()), None)
        self.data.update({
            '_listID': req_list['id'],
            '_listName': req_list['name']
        })
        # print json.dumps(req_list, indent=4, sort_keys=True)
        # returns dictionary


    def get_all_cards(self):
        print "Getting all cards for " + self.REQUIRED_LIST
        # those additional fields are for future references only
        cards = self.trello.lists.get_card(self.data['_listID'], 
                fields=['badges', 'dateLastActivity', 'desc', 'due', 'email',
                        'id', 'idAttachmentCover', 'idBoard', 'idList',
                        'idMembers', 'labels', 'name', 'pos', 'shortLink',
                        'shortUrl', 'url'])
        self.data.update({ 'cards': {} })
        for card in cards:
            labels = []
            for label in card['labels']:
                labels.append(label['name'])

            self.data['cards'].update({
                card['name']: {
                    'id': card['id'],
                    'shortLink': card['shortLink'],
                    'shortUrl': card['shortUrl'],
                    'url': card['url'],
                    'labels': labels,
                    'desc': card['desc'],
                    '_commentsCount': card['badges']['comments'],
                    'dateLastActivity': card['dateLastActivity'],
                    'idMembers': card['idMembers'],
                    'comments': {}
                }
            })
        # print json.dumps(cards, indent=4, sort_keys=True)
        # returns array of dictionaries


    def get_actions(self):
        print "Getting description, comments, etc..."
        for card, values in self.data['cards'].iteritems():
            if int(values['_commentsCount']) > 0:
                tmp_acts = self.trello.cards.get_action(values['shortLink'], filter="commentCard")
                # print json.dumps(tmp_acts, indent=4, sort_keys=True)
                # returns array of dictionaries

                if not self.data['_boardName']:
                    self.data['_boardName'] = tmp_acts[0]['data']['board']['name']
                if not self.data['_boardShortLink']:
                    self.data['_boardShortLink'] = tmp_acts[0]['data']['board']['shortLink']

                for i in range(len(tmp_acts)):
                    self.data['cards'][card]['comments'].update({
                        i + 1: {
                            'id': tmp_acts[i]['id'],
                            'text': tmp_acts[i]['data']['text'],
                            'date': tmp_acts[i]['date'],
                            'fullName': tmp_acts[i]['memberCreator']['fullName'],
                            '_memberID': tmp_acts[i]['memberCreator']['id']
                        }
                    })


    def get_data(self):
        '''
        # This is for future references
        data = [
                boardName
                boardID
                boardShortLink
                listName
                listID
                cards: {
                    cardName: {
                        cardShortLink
                        description
                        dateActivity
                        commentsCount
                        members
                        shortlink
                        shorturl
                        url
                        comments: {
                            commentID
                            commentText
                            commenterFN
                            commentDate
                    }
                }
            }
        ]
        '''
        self.get_board_lists()
        self.get_required_list()
        self.get_all_cards()
        self.get_actions()
        # print json.dumps(self.data, indent=4, sort_keys=True)


def read_config(f):
    config = f
    conf = ConfigParser()
    try:
        conf.read(config)
        k = conf.get('Config', 'KEY')
        t = conf.get('Config', 'TOKEN')
        b = conf.get('Config', 'BOARD_ID')
        r = conf.get('Config', 'REQUIRED_LIST')
        d = conf.get('Config', 'OUTPUT_DEST')
        return k, t, b ,r, d
    except Exception, e:
        print str(e)
        sys.exit(1)

if __name__=='__main__':
    if len(sys.argv) < 2:
        print 'Supply your config file'
        sys.exit(1)
    config = sys.argv[1]
    KEY, TOKEN, BOARD_ID, REQUIRED_LIST, OUTPUT_DEST = read_config(config)

    trello = TrelloCards(KEY, TOKEN, BOARD_ID, REQUIRED_LIST)
    trello.get_data()
    data = trello.data

    import output
    output.create_output(OUTPUT_DEST, data)
