import datetime
import docx2txt as docx
import xlrd
import csv


def docx2txt(src, dest):
    content = docx.process(src)
    txt = open(dest, "w", newline='')
    txt.write(content)


def xls2csv(src, dest):

    wb = xlrd.open_workbook(src)
    sh = wb.sheet_by_index(0)

    csv_file = open(dest, 'w', newline='')
    wr = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE)

    for row_id in range(sh.nrows):
        values = sh.row_values(row_id)

        for col_id in range(sh.ncols):
            if str(sh.cell(row_id, col_id)).split(':')[0] == 'xldate':
                cell = sh.cell_value(row_id, col_id)
                values[col_id] = datetime.datetime(*xlrd.xldate_as_tuple(cell, wb.datemode))

        wr.writerow(values)

    csv_file.close()