"""
Usage:
    script.py results [-s <tag>]... [-y <year>] [-y <year>] [options]
    script.py records [-s <tag>] [-s <tag>] [-y <year>] [-y <year>] [options]
    script.py settable [-s <tag>]... [-y <year>] [-y <year>] [options]
    script.py -h | --help

Get tournament results of specified smasher

Options:
  -h, --help                Show this help message and exit
  -s, --smasher <tag>       The tag of the smasher you want results for
  -i, --input_file <path>   Path to input file where tags are stored
  -o, --output_file <path>  Path to output file where results are put
  -t, --threshold <place>   Tournaments where the smasher placed worse will have
                            their names displayed
  -y, --year <year>         Specified year used to filter tournament dates
                            List 1 specific year or 2 to define a range
  -g, --game <game>         Specified game to get tournament results for
                            [default: Melee]
  -e, --event <event>       What event to pull results for
                            [default: Singles]
  --debug                   Run in debug mode
"""

from smasherstats import *
from docopt import docopt
from prettytable import PrettyTable, ALL
import os.path

def nums_from_string(string):
    nums = ''
    for char in string:
        if char.isnumeric():
            nums += char
    return int(nums)

def output_write(output, path):
    if os.path.isfile(path):
        with open(path, 'a+', encoding='utf8') as f:
            ofile = path
            for c in ['\\', '/']:
                ofile = ofile.replace(c, ' ')
            ofile = ofile.split()[-1]
            if output not in open(path).read():
                f.write(output + '\n\n')
                print(f'Output written to {ofile}')
            else:
                print(f'Output already in {ofile}')
    else:
        print(output)


# globals
smasher = ''
tags = []
threshold = 1
year = [CURRENT_YEAR]
game = 'Melee'
results_game = 'Melee'
record_game = 'melee'
event = ''
input_file = ''
output_file = ''
valid = 0

args = docopt(__doc__)
if args['--debug']:
    print(args)
for arg in args:
    if args[arg] is not None:
        globals()[arg.strip('-')] = args[arg]

for y in year:
    if not str(y).isnumeric() and y.upper() != 'ALL':
        print('Invalid year \'{y}\'. Defaulting to current year.')
        y = CURRENT_YEAR
    y = str(y).lstrip('0')
    try:
        y = int(y)
    except:
        pass
if year == []:
    year = [CURRENT_YEAR]

games = [
    ['MELEE',
     'SMASH MELEE',
     'SMASH BROS MELEE',
     'Super Smash Bros. Melee',
     'melee'],

    ['64',
     'SMASH 64',
     'SUPER SMASH BROS 64',
     'Super Smash Bros.',
     'smash-64'],

    ['BRAWL',
     'SMASH BROS BRAWL',
     'SMASH BRAWL',
     'Super Smash Bros. Brawl',
     'brawl'],

    ['SMASH 4',
     'SM4SH',
     'SMASH WII U',
     'SMASH BROS 4',
     'SMASH BROS WII U',
     'SMASH BROS 4',
     'SUPER SMASH BROS 4',
     'Super Smash Bros. for Wii U',
     'wii-u'],

    ['PM',
     'PROJECT MELEE',
     'SUPER SMASH BROS PROJECT M',
     'SUPER SMASH BROS PM',
     'Project M',
     'pm']
]
for g in games:
    if game.strip('.').upper() in g:
        game = g[-2]
        record_game = g[-1]
        results_game = g[0]
        valid = 1
if not valid:
    print('Invalid game \'{game}\'. Defaulting to Melee.')
    game = 'Super Smash Bros. Melee'
    record_game = 'melee'

events = [
    ['SINGLES',
     'Singles'],

    ['DOUBLES',
     'Doubles']
]

for e in events:
    if event.upper() in e:
        event = e[-1]
        valid = 1
if not valid:
    print('Invalid event \'{event}\'. Defaulting to Singles.')
    event = 'Singles'

if input_file != '':
    tags = [line.strip('\n') for line in open(input_file, 'r')]
if tags == [] and smasher == []:
    smasher = [input('Smasher: ')]
for tag in smasher:
    if tag != '' and tag.lower() not in map(str.lower, tags):
        tags += [tag]

results = []
tags = [' '.join(i[0].upper() + i[1:] for i in tag.split()) for tag in tags]
for tag in tags:
    r = getResults(tag, year, game, event)
    results.append([r[2], r[0]])
    year = r[1]

if args['results']:
    for i in range(len(tags)):
        tag = results[i][0]
        res = results[i][1]
        output = '-'*20 + '\n'
        output += f'{tag}\'s {results_game.capitalize()} {event} results for '
        if len(year) == 1:
            output += str(year[0])
        elif len(year) == 2:
            output += f'<{year[0]}, {year[1]}>'
        output += ':'
        if int(threshold) not in [0, 1]:
            output += f'\nTournament names listed for placings of {threshold} or below.\n'

        res = [r for r in res if any(c.isdigit() for c in r[0])]
        res = sorted(res, key=lambda x: nums_from_string(x[0]))

        # sorted by place
        # formatted like so: [[place, name, year], ...]
        for j in range(len(res)):
            r = [j[0] for j in res]
            place = res[j][0]
            if res[j - 1][0] != place:
                output += '\n'
                count = r.count(place)
                t_str = f'{place} - {count}'
                if nums_from_string(place) >= int(threshold) > 0:
                    for k in range(len(res)):
                        if res[k][0] == place:
                            t_name = res[k][1]
                            t_year = str(res[k][2])
                            if t_str[0] != '\n':
                                t_str = '\n' + t_str
                            t_str += '\n - ' + t_name + ' '
                            if len(year) != 1 and t_year not in t_name:
                                t_str += t_year
                output += t_str
        if i == len(tags) - 1:
            output += '\n' + '-'*20
        output_write(output, output_file)

if args['records']:
    record = getRecord(tags, results, record_game)
    output = ''
    output += '\n'
    if len(tags) == 2 and output_file != '':
        output += f'{tags[0]} vs. {tags[1]}'
    output += '\n'
    if len(record[3]) > 0:
        output += 'Tournaments where specified players were present but results failed to be retrieved:'
        for f in record[3]:
          output += f'\n - {f}'
        output += '\n'

    pt = PrettyTable()
    if len(tags) == 1:
        pt.field_names = ['Tournament', 'Round', f'{tags[0]} vs. ↓', 'Score', 'Outcome']
    elif len(tags) == 2:
        pt.field_names = ['Tournament', 'Round', f'{tags[0]} - {tags[1]}', 'Winner']

    pt_rows = record[0]
    for i in range(len(pt_rows)):
        row = pt_rows[i]
        r_name = row[0]
        if i > 0:
            if r_name == pt_rows[i-1][0]:
                r_name = ''
            else:
                pt.add_row(['' for _ in range(len(pt.field_names))])
        pt.add_row([r_name] + row[1:])
    output += pt.get_string()

    if len(tags) == 2:
        output += f'\n\nTotal Set Count: {tags[0]} {record[1][0]} - {record[1][1]} {tags[1]}'
        output += f'\nTotal Game Count: {tags[0]} {record[2][0]} - {record[2][1]} {tags[1]}'
    output_write(output, output_file)

if args['settable']:
    settable = PrettyTable(hrules=ALL)
    settable.field_names = ['↓ vs. →'] + tags
    output = ''
    st = getSetTable(tags, results, record_game)
    for i in range(len(st[0])):
        settable.add_row([tags[i]] + st[0][i])
    output += '\n\n'
    if len(st[1]) > 0:
        output += 'Tournaments where specified players were present but results failed to be retrieved:'
        for f in st[1]:
          output += f'\n - {f}'
        output += '\n'
    output += settable.get_string()
    output_write(output, output_file)