#!/usr/bin/python2.7

from datetime import datetime
import os
import sys
import time
# import json

sys.dont_write_bytecode = True

def create_output(dst, data):
    dst = dst
    data = data
    taym = time.time()
    fname = datetime.fromtimestamp(taym).strftime('%Y-%m-%d %H:%M:%S') + '.html'

    if not os.path.isdir(dst):
        print 'Please correct your Destination folder in your configuration.'
        sys.exit(1)

    list_name = data['_listName']
    # default sort by hash (dictionary type)
    # cards_title = [key for key,values in data['cards'].iteritems()]
    # cards_values = [values for keys, values in data['cards'].iteritems()]

    # sort by last activity descending
    cards_title = sorted([(data['cards'][k]['dateLastActivity'], k) for k, v in data['cards'].iteritems()], reverse=True)
    # ('2015-04-12T05:06:25.650Z', 'test3')

    cards_values = [data['cards'][k[1]] for k in cards_title]
    # print json.dumps(cards_values, indent=4, sort_keys=True)
    
    template = '''
        <!doctype html>
        <html class="no-js" lang="">
            <head>
                <meta charset="utf-8">
                <meta http-equiv="x-ua-compatible" content="ie=edge">
                <title>''' + fname + '''</title>
                <meta name="description" content="">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/3.0.3/normalize.css">
                <style>
                    body { line-height: 1.4; color: rgb(81, 81, 81); }
                    h2 {
                        width: auto;
                        margin: 10px auto 0 auto;
                        display: table;
                    }
                    ul, li { list-style: none; }
                    .output {
                        max-width: 80%;
                        margin: 20px auto;
                        padding: 0;
                    }
                    .list-name {
                        padding: 10px;
                        background: rgb(215, 239, 194);
                        border: 1px solid rgb(214, 226, 210);
                        color: rgb(100, 107, 100);
                    }
                    .card-title {
                        padding: 5px;
                        background: rgb(247, 247, 247);
                        border: 1px solid rgb(228, 228, 228);
                        margin-bottom: 5px;
                        margin-top: 5px;
                    }
                    .comments { margin-left: 2em; }
                    .comauthor { color: rgb(132, 126, 95); }
                </style>
            </head>
            <body>

                <h2>Time Generated: ''' + fname.replace('.html', '') + '''</h2>
                <ul class="output">
                    <li class="list-name">
                        ''' + list_name + '''
                    </li>
                    <li>
                        <ul>
                                '''
    for i in range(len(cards_title)):
        labels = ', '.join(cards_values[i]['labels']) or ''
        template += '''<li class="card-title">''' + cards_title[i][1] \
                            + '''
                            </li>
                            <li>
                                <ul>
                                    <li class="desc"><span>Description:</span> 
                                    ''' + cards_values[i]['desc'] + '''
                                    </li>
                                    <li class="desc"><span>Last Activity:</span> 
                                    ''' + cards_values[i]['dateLastActivity'].replace('T', ' ').replace('Z','') + '''
                                    </li>
                                    <li class="labels"><span>Labels:</span> 
                                    ''' + labels + '''
                                        </li>
                                        <li>Comments:</li>'''
        for j in range(len(cards_values[i]['comments'])):
            template += '''<li class="comments"><span class="comauthor">''' \
                        + cards_values[i]['comments'][j + 1]['fullName'] + '''</span> - ''' \
                        + cards_values[i]['comments'][j + 1]['text'] + \
                                            '''</li>'''
        template += '''         </ul>
                            </li>
                                    '''

    template += '''     </ul>
                    </li>
                </ul>
            </body>
        </html>
        '''

    with open(dst + fname, 'a+') as f:
        f.write(template)
    print dst + fname + ' created.'

    