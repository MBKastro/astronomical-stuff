import pyodbc
conn = pyodbc.connect("Driver=SQL Server;Server=MBK;Database=DoubleStarsDB;Trusted_Connection=yes")
from decimal import Decimal

class Position:

    def __init__(self, coor_2k, disc, comp, date_last, pa_last, sep_last, note):

        self.WDS_id = coor_2k+disc+comp
        self.coor_2k = coor_2k
        self.disc = disc
        self.comp = comp
        self.epoch = float(date_last)
        self.pa_last = float(pa_last)          # last precise
        self.sep_last = float(sep_last)         # last precise
        self.note = note
        return

    @classmethod
    def get(cls, text_str):

        coor_2k = text_str[0:10]
        disc = text_str[10:17]
        comp = text_str[17:23]
        date_last = text_str[28:32]
        pa_last = text_str[38:44]
        sep_last = text_str[46:53]
        note = text_str[106:110]
        return cls(coor_2k, disc, comp, date_last, pa_last, sep_last, note)

# ----------------------------- show Table --------------------------------


# def convert_mysql_decimal_to_float(decimal_object):
#     if (decimal_object == None):
#         return None
#     else:
#         return float(decimal_object)
#
# cell_value = convert_mysql_decimal_to_float(row[4])

def read_WDS(conn):

    cursor = conn.cursor()
    cursor.execute("SELECT WDS_ID, COORD, DISC, COMP, LSTDATE, LSTPA, LSTSEP, NOTES FROM dbo.WDS;")
    for data_row in cursor:
        print(f'WDS: {data_row[0]} {data_row[1]} {data_row[2]} {data_row[3]} {data_row[4]} {data_row[5]} {data_row[6]} {data_row[7]}')


# ----------------------------- drop & create Table --------------------------------


def drop_WDS_table(conn):

    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS WDS;")
    t = "CREATE TABLE WDS (WDS_ID CHAR(22) PRIMARY KEY, COORD CHAR(10),  DISC CHAR(7), COMP CHAR(5), "
    t += "LSTDATE NUMERIC(4), LSTPA NUMERIC(3), LSTSEP NUMERIC(5,1), NOTES CHAR(4));"
    cursor.execute(t)
    conn.commit()

# ----------------------------- the Main man --------------------------------
def main_control(load):

    if load is True:
        f = open('wds_precise.txt', 'r')  # all last precise positions in wds
        drop_WDS_table(conn)
        cursor = conn.cursor()
        no_of_wds = 0
        for pos in f:
            no_of_wds += 1
            w = Position.get(pos)
            val = (w.WDS_id, w.coor_2k, w.disc, w.comp, w.epoch, w.pa_last, w.sep_last, w.note)
            sql = "INSERT INTO WDS (WDS_ID, COORD, DISC, COMP, LSTDATE, LSTPA, LSTSEP, NOTES) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, val)
            conn.commit()
            del w  # delete instance from memory

        f.close()
        print('No of wds read      : ', no_of_wds)
# ----------------------------- Mission Control --------------------------------
main_control(True)
read_WDS(conn)