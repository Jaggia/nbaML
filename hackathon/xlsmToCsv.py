import csv
import xlrd

workbook = xlrd.open_workbook('../nba-enhanced-stats/BBRef_Composite_1978_2016.xlsm')
for sheet in workbook.sheets():
    with open('../nba-enhanced-stats/composite/{}.csv'.format(sheet.name), 'wb') as f:
        writer = csv.writer(f)
        for row in range(sheet.nrows):
            out = []
            for cell in sheet.row_values(row):
                try:
                    out.append(cell.encode('utf8'))
                except:
                    out.append(cell)
            try:
                writer.writerow(out)
            except:
                print('failed ', out)