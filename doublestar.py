# doublestar.py
# input date and Keplerian elements from WDS for a binary star (2000 epoch coo.)
# output position angle in degrees and separation in arc secs for date
# repeats calculations by incrementing date
# transforms polar to Cartesian coordinates
# displays orbit as graph
# displays positions
# -----------------------------------------------------------
from tkinter import *
from math import sin, cos, tan, atan, sqrt, radians, pi
import numpy as np
import matplotlib.pyplot as plt
import csv

global disc, wds


# -----------------------------------------------------------
# read local file (cat. with orbit Keplerian elements)
f = open('Input_Files/6thorbiths.txt', 'r')
#
epo2kco = []
wds_id = []
dis = []
per = []
p_u = []
alfa = []
alfa_u = []
incl = []
node = []
time = []
ecc = []
long = []
#


def load_wds():

    for contents in f:
        epo2kco.append(contents[0:18])
        wds_id.append(contents[19:29])
        dis.append(contents[30:42])
        # period in units
        if (contents[81:90]) > '    .    ':
            per.append(float(contents[81:90]))
        else:
            per.append(0)
        # period units
        p_u.append(contents[92:93])
        # Semimajor axis, alfa in units
        if contents[104:114] > '    .     ':
            alfa.append(float(contents[104:114]))
        else:
            alfa.append(0)
        # Semimajor axis units
        alfa_u.append(contents[114:115])
        # Inclination
        if contents[125:133] > '   .    ':
            incl.append(float(contents[125:133]))
        else:
            incl.append(0)
        # Node in degrees
        if contents[143:151] > '   .    ':
            node.append(float(contents[143:151]))
        else:
            node.append(0)
        # Time of periastron (no unit..)
        if contents[162:174] > '     .      ':
            time.append(float(contents[162:174]))
        else:
            time.append(0)
        # Eccentricity
        if contents[187:195] > ' .      ':
            ecc.append(float(contents[187:195]))
        else:
            ecc.append(0)
        # Longitude of periastron (long), in degrees
        if contents[205:213] > '   .    ':
            long.append(float(contents[205:213]))
        else:
            long.append(0)
    f.close()
    return
# -----------------------------------------------------------


def doublestar(p_per, p_time, p_alfa, p_ecc, p_incl, p_long, p_node, p_date):

    pi2 = pi * 2
    p_incl_rad = radians(p_incl)
    p_node_rad = radians(p_node)
    p_long_rad = radians(p_long)
    #
    n = pi2 / p_per
    ma = n * (p_date - p_time)
    m = ma - pi2 * int(ma / pi2)
    ea = m
    a = ea - (p_ecc * sin(ea)) - m
    while abs(a) >= 1E-15:
        a = a / (1 - (p_ecc * cos(ea)))
        ea = ea - a
        a = ea - (p_ecc * sin(ea)) - m
    #
    tu = sqrt((1 + p_ecc) / (1 - p_ecc)) * tan(ea / 2)
    nu = 2 * atan(tu)
    r = p_alfa - p_alfa * p_ecc * cos(ea)
    y = sin(nu + p_long_rad) * cos(p_incl_rad)
    x = cos(nu + p_long_rad)
    q = atan(y / x)
    #
    if x < 0:
        q = q + pi
    else:
        if q < 0:
            q = q + pi2
    #
    th = q + p_node_rad
    if th > pi2:
        th = th - pi2
    rh = r * x / cos(q)
    #
    pa = int(th / radians(1) * 10 + 0.5) / 10
    sep = int(rh * 100 + 0.5) / 100
    #
    # print('year = ', d)
    # print('pa   = ', pa, ' deg')
    # print('sep. = ', sep, ' arcsec')
    line = str(p_date) + ';' + str(sep) + ';' + str(pa) + ';'
    return line
# -----------------------------------------------------------


def btn_click_1():
    global disc, wds

    try:
        print(i_epo2kco.get())
        ix = epo2kco.index(i_epo2kco.get())
        disc = dis[ix]
        wds = wds_id[ix]
        Label(root, text=wds + ' ' + disc, fg='green', font=40).grid(row=9, column=1)
        Label(root, text='Period ' + str(per[ix])).grid(row=10, column=1)
        Label(root, text='Time   ' + str(time[ix])).grid(row=11, column=1)
        Label(root, text='Semi-major axis  ' + str(alfa[ix])).grid(row=12, column=1)
        Label(root, text='Eccentricity ' + str(ecc[ix])).grid(row=13, column=1)
        Label(root, text='Inclination ' + str(incl[ix])).grid(row=14, column=1)
        Label(root, text='Longitude ' + str(long[ix])).grid(row=15, column=1)
        Label(root, text='Node   ' + str(node[ix])).grid(row=16, column=1)
        ff = open('Output_Files/' + i_epo2kco.get() + ' position.txt', 'w')
        line = 'year;sep;pa'
        ff.write(line)
        ff.write('\n')
        line = doublestar(per[ix], time[ix], alfa[ix], ecc[ix], incl[ix], long[ix], node[ix], date.get())
        ff.write(line)
        ff.write('\n')
        if inc_p.get() > 0 and num_i.get() > 0:
            dd = date.get() + inc_p.get()
            while dd <= date.get() + (num_i.get() * inc_p.get()):
                line = doublestar(per[ix], time[ix], alfa[ix], ecc[ix], incl[ix], long[ix], node[ix], dd)
                ff.write(line)
                ff.write('\n')
                dd = dd + inc_p.get()
        Label(root, text='Calculation done!', fg='blue', font=20).grid(row=18, column=1)
    #
    except ValueError:
        Label(root, text='*** Not found ***', fg='red', font=20).grid(row=18, column=1)
    return
# -----------------------------------------------------------


def btn_click_2():
    global disc, wds

    x_coo = []
    y_coo = []
    fd = open('Output_Files/'+i_epo2kco.get() + ' position.txt', 'r')
    for rec in fd:
        rec = csv.reader(fd, delimiter=";")
        for row in rec:
            sep = float(row[1])
            pa = float(row[2])
            # Convert polar to x,y coordinates
            x = round(sep * sin(radians(pa)), 2)
            y = round(sep * -1 * cos(radians(pa)), 2)
            print(sep, pa, x, y, sep * x, sep * y)
            x_coo.append(x)
            y_coo.append(y)
    #
    area = np.pi * 2
    # secondary
    plt.scatter(x_coo, y_coo, s=area, alpha=0.5, color='b')
    # primary
    plt.scatter(0, 0, s=area, alpha=0.5, color='r')
    plt.title('WDS ' + i_epo2kco.get() + ' ' + wds + ' ' + disc)
    plt.xlabel('N')
    plt.ylabel('W')
    plt.axvline(0, 0, 1, color='r')
    plt.axhline(0, 0, 1, color='r')
    plt.show()
    return
# -----------------------------------------------------------


def btn_click_3():

    root.quit()
    return


def btn_click_4():

    root2 = Tk()
    Label(root2, text='Position(s) of ' + wds + ' ' + disc).grid(row=0, column=1)
    text = Text(root2, height=25)
    text.grid(row=0, column=1, )
    scroll = Scrollbar(root2, orient="vertical", command=text.yview)
    scroll.grid(row=0, column=1, sticky="ns")
    fd = open('Output_Files/' + i_epo2kco.get() + ' position.txt', 'r')
    n = 1
    for rec in fd:
        rec = csv.reader(fd, delimiter=";")
        for row in rec:
            pos_date = row[0]
            sep = row[1]
            pa = row[2]
            print(n, pa, sep, pos_date)
            Label(root2, text=pos_date + ' ' + pa + ' ' + sep).grid(row=n, column=1)
            n += 1
    root2.mainloop()
# -----------------------------------------------------------


load_wds()

# -----------------------------------------------------------
root = Tk()
Label(root, text='Calculate Position(s) of a binary star').grid(row=0, column=1)
Label(root, text='Enter identifier (WDS epoch 2000 coor.)').grid(row=1, column=1)
i_epo2kco = StringVar()
Entry(root, textvariable=i_epo2kco, width=20).grid(row=2, column=1)
Label(root, text='Enter increment,inc_p (years)').grid(row=3, column=1)
inc_p = DoubleVar()
Entry(root, textvariable=inc_p, width=20).grid(row=4, column=1)
Label(root, text='Enter no of increments, num_i').grid(row=5, column=1)
num_i = IntVar()
Entry(root, textvariable=num_i, width=20).grid(row=6, column=1)
Label(root, text='Enter epoch').grid(row=7, column=1)
date = DoubleVar()
Entry(root, textvariable=date, width=20).grid(row=8, column=1)
# -----------------------------------------------------------
Button(root, text='Calculate', command=btn_click_1).grid(row=17, column=1)
Button(root, text='Show position(s)', command=btn_click_4).grid(row=19, column=1)
Button(root, text='Show Orbit', command=btn_click_2).grid(row=20, column=1)
Button(root, text='End', command=btn_click_3).grid(row=21, column=1)
# -----------------------------------------------------------
root.mainloop()
# -----------------------------------------------------------
