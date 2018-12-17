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
for year in range(2000, 2017):
    for team in teams:
        fname = 'data/{}/{}_advanced.txt'.format(year, team)
        if not os.path.isdir('data/' + str(year)):
            os.mkdir('data/' + str(year))

        if not os.path.isfile(fname):
            driver = webdriver.Firefox() if driver is None else driver
            url = "https://www.basketball-reference.com/teams/" + str(team) \
                  + "/" + str(year) + ".html"
            driver.get(url=url)
            try:
                advanced_table = driver.find_element_by_id(id_='advanced')
            except:
                continue
            lines = advanced_table.text
            # print(advanced_table.text)
            stats = []
            for n, line in enumerate(lines.split('\n')):
                # print(line + '\n\n')
                if n == 0:
                    keys = line.split(' ')
                    keys[1] = "First"
                    keys[2] = "Last"
                else:
                    stats += [line.split(' ')]

            while '' in keys:
                keys.remove('')

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








