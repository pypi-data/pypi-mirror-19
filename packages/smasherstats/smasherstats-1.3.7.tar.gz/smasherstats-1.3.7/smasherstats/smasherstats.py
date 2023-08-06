import datetime
import sys
import re

import requests
from bs4 import BeautifulSoup as bsoup
import pysmash

CURRENT_YEAR = datetime.datetime.now().year
smash = pysmash.SmashGG()

def getResults(tag, year, game, event):
    res = []
    smasher = '_'.join(i for i in tag.split())
    request = 'http://www.ssbwiki.com/Smasher:'
    page = requests.get(request + smasher)
    if page.status_code != 200:
        page = requests.get(request[:-8] + smasher)  # hehe
    soup = bsoup(page.content, "html.parser")
    while page.status_code != 200:
        print(f'Invalid tag \'{smasher}\'. Try again.')
        tag = input('Smasher: ')
        tag = ' '.join(i[0].upper() + i[1:] for i in tag.split())
        smasher = '_'.join(i for i in tag.split())
        page = requests.get(request + smasher)
        if page.status_code != 200:
            page = requests.get(request[:-8] + smasher)  # hehe
        soup = bsoup(page.content, "html.parser")

    tables = soup.find_all('div', {'id': 'mw-content-text'})[0].contents[2].contents[1].contents[1]
    for header in tables.find_all('h3'):
        if game in header.contents[0].text:
            tables = tables.contents[tables.index(header) + 2]
            break
    if str(year[0]).upper() == 'ALL':
        year = [int(tables.contents[3].contents[3].text.split(', ')[1]), CURRENT_YEAR]

    for i in range(3, len(tables.contents), 2):
        try:
            t = tables.contents[i]
            t_name = t.contents[1].text
            t_year = int((t.contents[3].text).strip(' ')[-4:])
            if event == 'Singles':
                t_place = str(t.contents[5].text).strip(' ')
            elif event == 'Doubles':
                t_place = str(t.contents[7].text).strip(' ')
            res += [[t_place, t_name, t_year]]
        except:
            continue
    res = [i for i in res if int(year[0]) <= i[2] <= int(year[-1])]
    return [res, year, tag]


def getRecord(tags, results, game):
    if len(tags) == 2:
        print(f'{tags[0]} vs. {tags[1]}')
    tournaments = [r[1] for res in results for r in res[1] if res[0] in tags]
    filter_t = []
    for t in tournaments:
        if tournaments.count(t) == len(tags) and t not in filter_t:
            filter_t.append(t)
    tournaments = filter_t

    setcounts = [0, 0]
    gamecounts = [0, 0]

    fail_tournaments = []
    records = []
    #print(tournaments)
    for tournament in tournaments:
        sys.stdout.write(f'Retrieving tournament {tournaments.index(tournament)+1}/{len(tournaments)}...')
        sys.stdout.write('\r')
        sys.stdout.flush()
        havePlayed = 0

        "TODO: Fix bug where latest bracket in tourney where both players where present is returned, \
               meaning that two players could have played in a previous bracket but still be present \
               in a later bracket (e.g. one in winners and one in losers). To fix, loop through all  \
               brackets and if both players are present, check that they actually played. If they    \
               played in losers, stop looking, but if they played in winners, keep looking until one \
               player gets knocked out of the tournament."


        tournament_name = '-'.join(re.sub(r'[^\w\s]','',tournament.replace('\'', ' ')).split())
        try:
            t = smash.tournament_show_event_brackets(tournament_name, f'{game}-singles')
        except:
            fail_tournaments.append(tournament)
            continue

        # API_STRING=f'https://api.smash.gg/tournament/{tournament_name}/event/{game}-singles?expand[]=groups'
        # tour = requests.get(API_STRING).json()['entities']['groups']
        # print(tour)
        # break

        havePlayed = 0
        temp_tags = set(map(str.lower, tags))
        for bracket in list(reversed(t['bracket_ids'])):
            if not havePlayed:
                players = smash.bracket_show_players(bracket)
                if temp_tags.issubset([p['tag'].lower() for p in players]):
                    sets = smash.bracket_show_sets(bracket)
                    player_ids = ['' for _ in range(len(tags))]
                    for p in players:
                        if p['tag'] in tags:
                            player_ids[tags.index(p['tag'])] = p['entrant_id']
                    for s in sets:
                        if all(str(n) != 'None' for n in s.values()):
                            ids = [int(s['entrant_1_id']), int(s['entrant_2_id'])]
                            scores = [s['entrant_1_score'], s['entrant_2_score']]
                            if all(i in ids for i in player_ids):
                                havePlayed = 1
                                p_tag = ''
                                if len(tags) == 1:
                                    p_id = ids[not ids.index(player_ids[0])]
                                    for p in players:
                                        if p['entrant_id'] == p_id:
                                            p_tag = p['tag']
                                if ids[0] != player_ids[0]:
                                    ids.reverse()
                                    scores.reverse()
                                if scores[0] > scores[1]:
                                    outcome = 'WIN'
                                else:
                                    outcome = 'LOSS'
                                for i in range(len(gamecounts)):
                                    gamecounts[i] += scores[i]
                                setcounts[scores.index(max(scores))] += 1
                                if len(tags) == 1:
                                    res = [tournament,
                                           s['full_round_text'],
                                           p_tag,
                                           f'{scores[0]} - {scores[1]}',
                                           outcome]
                                elif len(tags) == 2:
                                    res = [tournament,
                                           s['full_round_text'],
                                           f'{scores[0]} - {scores[1]}',
                                           tags[player_ids.index(int(s['winner_id']))]]
                                records.append(res)
            else:
                break
    return records, setcounts, gamecounts, fail_tournaments

def getSetTable(tags, results, game):
    st = [['-' for _ in range(len(tags))] for _ in range(len(tags))]
    fail_tournaments = []
    for i in range(len(tags)):
        for j in range(i+1, len(tags)):
            record = getRecord([tags[i], tags[j]], results, game)
            print(record[3])
            for f in record[3]:
                if f not in fail_tournaments:
                    fail_tournaments.append(f)
            record = record[1]
            print('\n')
            st[i][j] = f'{record[0]} - {record[1]}'
            st[j][i] = f'{record[1]} - {record[0]}'
    return st, fail_tournaments