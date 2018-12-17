# # YouTube Video: https://www.youtube.com/watch?v=Z3vFdtZ7d-g
from selenium import webdriver
import os
#
# MAX_PAGE_NUM = 5
# MAX_PAGE_DIG = 3

# with open('results.csv', 'w') as f:
#     f.write("Buyer, Price \n")
#
# for i in range(1, MAX_PAGE_NUM + 1):
#     page_num = (MAX_PAGE_DIG - len(str(i))) * "0" + str(i)
#     url = "http://econpy.pythonanywhere.com/ex/" + page_num + ".html"
#
#     driver.get(url)
#
#     buyers = driver.find_elements_by_xpath('//div[@title="buyer-name"]')
#     prices = driver.find_elements_by_xpath('//span[@class="item-price"]')
#
#     num_page_items = len(buyers)
#     with open('results.csv', 'a') as f:
#         for i in range(num_page_items):
#             f.write(buyers[i].text + "," + prices[i].text + "\n")
#
# driver.close()


# https://www.basketball-reference.com/teams/{TEAM}/{YEAR}.html
teams =["ATL", "BKN", "BOS", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW",
        "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK",
        "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS",
        "NJN", "VAN", "NOH", "SEA"] ## old names
driver = None
#for year in range(2000, 2017):
for year in range(2000, 2001):
    for team in teams[:1]:
        fname = 'data/{}/{}_advanced.txt'.format(year, team)
        if not os.path.isdir('data/' + str(year)):
            os.mkdir('data/' + str(year))

        if not os.path.isfile(fname):
            driver = webdriver.Firefox() if driver is None else driver
            url = "https://www.basketball-reference.com/teams/" + str(team) \
                  + "/" + str(year) + ".html"
            driver.get(url=url)
            gotAdvanced = False
            try:
                advanced = driver.find_element_by_id(id_='advanced')
                gotAdvanced = True
                per_game = driver.find_element_by_id(id_='per_game')
                per_100 = driver.find_element_by_id(id_='per_poss')
                total = driver.find_element_by_id(id_='totals')
            except:
                if gotAdvanced:
                    print("Got advanced but still threw exception")
                continue
            lines = advanced.text
            # print(advanced_table.text)
            advStats = []
            for n, line in enumerate(lines.split('\n')):
                # print(line + '\n\n')
                if n == 0:
                    advKeys = line.split(' ')
                    advKeys[1] = "First"
                    advKeys[2] = "Last"
                else:
                    advStats += [line.split(' ')]

            while '' in advKeys:
                advKeys.remove('')

            prefixes = ['TOT_', 'PER_100_', 'PER_GAME_']
            stats = []
            for m, lines in enumerate([total.text, per_100.text, per_game.text]):
                prefix = prefixes[m]
                for n, line in enumerate(lines.split('\n')):
                    # print(line + '\n\n')
                    startIndex = None
                    if n == 0:
                        keys = line.split(' ')
                        keys[1] = "First"
                        keys[2] = "Last"
                        startIndex = keys.index('GS') + 1
                        keys = keys[startIndex:]
                        keys = [prefix + key for key in keys]
                    else:
                        stats += [line.split(' ')[startIndex:]]
                print(f'{prefix} Keys length: {len(keys)}, Stats length: {len(stats)}')
                advKeys.append(keys)
                [advStats[player].append(stats[player]) for player in range(len(stats))]
                print(f'Total length of keys: {len(advKeys)}, Total length of stats: {len(advStats[0])}')

            with open(fname, 'w') as of:
                [of.write(key + ' ') for key in keys[:-1]]
                of.write(keys[-1] + '\n')
                for statsline in stats:
                    [of.write(stat + ' ') for stat in statsline[:-1]]
                    of.write(statsline[-1] + '\n')

        else:
            f = open(fname, 'r')
            lines = f.read()
            stats = []
            for n, line in enumerate(lines.split('\n')):
                # print(line + '\n\n')
                if n == 0:
                    keys = line.split(' ')
                else:
                    stats += [line.split(' ')]

        # print(len(keys))
        # print(keys)
        # print(len(stats[0]))
        # print(stats)








