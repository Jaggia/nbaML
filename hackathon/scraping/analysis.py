import os
import sys

import sklearn
import pandas as pd

def fix_naming():
    for folder in next(os.walk('data'))[1]:  # directories in data/
        for fname in os.listdir('data/' + folder + '/'):
            print(folder, fname)
            try:
                teamSeasonData = pd.read_csv(filepath_or_buffer='data/' + folder + '/' + fname,
                                            delim_whitespace=True,
                                            header=0)
                # print(teamSeasonData)
            except Exception, e:
                error_str = str(e)
                print(error_str)
                comma_idx = error_str.index(",")
                line_num = int((error_str[comma_idx - 2 : comma_idx]).strip())
                df_to_fix = pd.read_csv(filepath_or_buffer='data/' + folder + '/' + fname, header=0)
                line_to_fix = df_to_fix.values[line_num - 2][0].split()
                first_name_idx = 1
                last_name_idx = -1
                for index, word in enumerate(line_to_fix[1:]):
                    if word.isdigit():
                        last_name_idx = index
                        break
                name = line_to_fix[first_name_idx : last_name_idx + 1]
                first_nm = name[0]
                last_name_arr = name[1:]
                last_nm = ""
                for nm in last_name_arr:
                    last_nm += nm + "-"
                last_nm = last_nm[:-1]
                fixed_line = df_to_fix.values[line_num - 2][0]
                first_num = -1
                for idx, char in enumerate(fixed_line):
                    if char.isalpha():
                        fixed_line = fixed_line.replace(char, "")
                        first_num = idx if first_num == -1 else first_num
                fixed_line = fixed_line.replace(" ", " " + first_nm + " " + last_nm, 1)
                fixed_line = fixed_line.replace("   ", " ")
                fixed_line = fixed_line.replace("  ", " ")
                df_to_fix.values[line_num - 2][0] = fixed_line
                df_to_fix.to_csv('data/' + folder + '/' + fname, index=False)

def extract_dfs():
    for folder in next(os.walk('data'))[1]:  # directories in data/
        for fname in os.listdir('data/' + folder + '/'):
            print(folder, fname)
            teamSeasonData = pd.read_csv(filepath_or_buffer='data/' + folder + '/' + fname,
                                        delim_whitespace=True,
                                        header=0)
            print(teamSeasonData)

if __name__ == "__main__":
    # fix_naming()