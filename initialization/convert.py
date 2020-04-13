import xlrd
import csv
import docx2txt as docx


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
        wr.writerow(sh.row_values(row_id))

    csv_file.close()
