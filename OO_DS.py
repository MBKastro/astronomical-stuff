from math import sin, cos, tan, atan, sqrt, radians, pi
global no_of_with_orbits, max_loops

orb_wds_disc = [] # key: coor_2k & discoverer designation & components
orb_per = []
orb_alfa = []
orb_incl = []
orb_node = []
orb_time = []
orb_ecc = []
orb_long = []
orb_grade = []
orb_may_be_calc = []
orb_per_e = []
orb_alfa_e = [] 
orb_incl_e = [] 
orb_node_e = []
orb_time_e = []
orb_ecc_e = []
orb_long_e = []
orb_has_errors = []

class Position:

    def __init__(self, coor_2k, disc, comp, date_last, pa_last, sep_last, note):

        self.coor_2k = coor_2k
        self.disc = disc
        self.comp = comp
        self.epoch = float(date_last)
        self.obsv_pos_pa  = float(pa_last)          # last precise
        self.obsv_pos_sep = float(sep_last)         # last precise
        self.note = note
        self.calc_pos_pa  = 0                       #
        self.calc_pos_sep = 0                       #
        self.diff_pos_pa  = 0                       #
        self.diff_pos_sep = 0                       #
        self.calc_pos_pa_err_min  = 0               #  - error
        self.calc_pos_sep_err_min = 0               #  - error
        self.calc_pos_pa_err_max  = 0               #  + error
        self.calc_pos_sep_err_max = 0               #  + error

        return

    @classmethod
    def get(cls, text_str):

        coor_2k = text_str[0:10]
        disc = text_str[10:17]
        comp = text_str[17:22]
        date_last = text_str[28:32]
        pa_last = text_str[38:44]
        sep_last = text_str[46:53]
        note = text_str[106:110]

        return cls(coor_2k, disc, comp, date_last, pa_last, sep_last, note)

    def has_orbit(self):

        if self.note[0] == 'O' or self.note[1] == 'O' or self.note[2] == 'O' or \
                self.note[0] == 'C' or self.note[1] == 'C' or self.note[2] == 'C':

            return True
        else:
            return False

    @staticmethod
    def make_header1():

        return '||Observed|Observed|Calculated|Calculated|Difference|Difference|Error Min|Error Min|Error Max|Error Max|'

    @staticmethod
    def make_header2():

        return 'Identification|Epoch|Position Angle|Separation|Position Angle|Separation|Position Angle|Separation|' \
               'Position Angle|Separation|Position Angle|Separation|Orbit Grade|'

    def make_line(self,grade):

        return self.coor_2k + self.disc + self.comp + '|' + str(self.epoch) + '|' + \
            str(self.obsv_pos_pa) + '|' + str(self.obsv_pos_sep) + '|' + str(self.calc_pos_pa) + '|' + \
            str(self.calc_pos_sep) + '|' + str(self.diff_pos_pa) + '|' + str(self.diff_pos_sep) + '|' + \
            str(self.calc_pos_pa_err_min) + '|' + str(self.calc_pos_sep_err_min) + '|' + \
            str(self.calc_pos_pa_err_max) + '|' + str(self.calc_pos_sep_err_max) + '|' + str(grade)+'|'

    @staticmethod
    def make_footer1():

        return 'Obs. in wds|With orbits|Not found|Written with orbits|||||'

    @staticmethod
    def make_footer2(n1, n2, n3, n4, n5):

        return str(n1) + '|' + str(n2) + '|' + str(n3) + '|' + str(n4) + '|' + str(n5) + '||||'

    @staticmethod
    def diff(pa_1, pa_2, sep_1, sep_2):  # _1: calc _2: obsv

        add_1 = 0
        add_2 = 0

        if pa_2 > 180 > pa_1:
            add_2 = 360
        elif pa_2 < 180 < pa_1:
            add_1 = 360

        diff_pa = abs(round((pa_1 + add_1) - (pa_2 + add_2), 2))

        if diff_pa > 360:
            diff_pa -= 360
            diff_pa = round(diff_pa, 2)

        diff_sep = abs(round(sep_1 - sep_2, 2))

        return diff_pa, diff_sep

    @staticmethod
    def calc(per, alfa, incl, long, time, ecc, node, epoch, max_loops):

        pa = 0
        sep = 0

        if per <= 0:
            print('! Period <= ZERO  -  Position cannot be calculated')
        else:
            c = pi * 2
            incl_rad = radians(incl)
            node_rad = radians(node)
            long_rad = radians(long)
            n = c / per
            ma = n * (epoch - time)
            m = ma - c * int(ma / c)
            ea = m
            a = ea - (ecc * sin(ea)) - m
            loops = 0
            while (abs(a) >= 1E-15) and (loops < max_loops):
                loops += 1
                a = a / (1 - (ecc * cos(ea)))
                ea = ea - a
                a = ea - (ecc * sin(ea)) - m
            if loops == max_loops:
                print('! Calculation of anomaly requires > max_loops  -  stopped - cannot calculate')
            else:
                tu = sqrt((1 + ecc) / (1 - ecc)) * tan(ea / 2)
                nu = 2 * atan(tu)
                r = alfa - alfa * ecc * cos(ea)
                y = sin(nu + long_rad) * cos(incl_rad)
                x = cos(nu + long_rad)
                q = atan(y / x)
                if x < 0:
                    q = q + pi
                else:
                    if q < 0:
                        q = q + c
                th = q + node_rad
                if th > c:
                    th = th - c
                rh = r * x / cos(q)
                pa = int(th / radians(1) * 10 + 0.5) / 10
                sep = int(rh * 100 + 0.5) / 100

        return pa, sep


class Orbit:

    def __init__(self, wds, disc, peri, peri_unit, peri_error, alfa, alfa_error, alfa_unit, incl, incl_error, node,
                 node_error, time_peri, time_unit, time_error, ecc, ecc_error, long, long_error, grade):

        self.wds = wds
        self.disc = disc        # discoverer designation & components
        self.per = float(peri)
        self.per_u = peri_unit
        self.per_e = float(peri_error)
        self.alfa = float(alfa)
        self.alfa_u = alfa_unit
        self.alfa_e = float(alfa_error)
        self.incl = float(incl)
        self.incl_e = float(incl_error)
        self.node = float(node)
        self.node_e = float(node_error)
        self.time = float(time_peri)
        self.time_u = time_unit
        self.time_e = float(time_error)
        self.ecc = float(ecc)
        self.ecc_e = float(ecc_error)
        self.long = float(long)
        self.long_e = float(long_error)
        self.grade = int(grade)
        self.calc = True

    def show_error(self):

        return self.wds + str(self.per_e) + '|' + str(self.alfa_e) + '|' + str(self.incl_e) + '|' + \
            str(self.node_e) + '|' + str(self.time_e) + '|' + str(self.ecc_e) + '|' + str(self.long_e) + '|'

    @classmethod
    def get(cls, text_str):

        ra, dec, wds, disc, ads, hd, hip, mag1, mag_flag1, vis_mag2, mag_flag2, peri, peri_unit, peri_error, alfa, \
            alfa_unit, alfa_error, incl, incl_error, node, node_asc, node_error, time_peri, time_unit, \
            time_error, ecc, ecc_error, long, long_error, eqnx, last_obs, grade, notes, ref, name \
            = text_str.split('|')

        def c0(c):
            if c == '' or c == '--.':
                return '0'
            else:
                return c

        return cls(wds, disc, c0(peri), peri_unit, c0(peri_error), c0(alfa), c0(alfa_error), alfa_unit, c0(incl),
                   c0(incl_error),c0(node), c0(node_error), c0(time_peri), time_unit, c0(time_error), c0(ecc),
                   c0(ecc_error), c0(long), c0(long_error), c0(grade))

    def is_calcuable(self):

        if self.grade in range(1, 6) and self.per_u == 'y' and self.alfa_u == 'a':
            return True
        else:
            self.calc = False       # overwrite to skip
            return False

    def make_line(self):

        return self.wds + self.disc + '|' + str(self.per) + '|' + self.per_u + '|' + str(self.alfa) + '|' + \
            str(self.incl) + '|' + str(self.node) + '|' + str(self.time) + '|' + str(self.ecc) + '|' + \
            str(self.long) + '|' + str(self.grade) + '|'

    def append_orbit_elt(self):

        orb_wds_disc.append(self.wds+self.disc)
        
        orb_per.append(self.per)
        orb_alfa.append(self.alfa)
        orb_incl.append(self.incl)
        orb_node.append(self.node)
        orb_time.append(self.time)
        orb_ecc.append(self.ecc)
        orb_long.append(self.long)
        orb_grade.append(self.grade)

        orb_may_be_calc.append(self.calc)

        orb_per_e.append(self.per_e)
        orb_alfa_e.append(self.alfa_e)  
        orb_incl_e.append(self.incl_e)  
        orb_node_e.append(self.node_e)  
        orb_time_e.append(self.time_e)  
        orb_ecc_e.append(self.ecc_e)  
        orb_long_e.append(self.long_e)

        if self.per_e == 0 and self.alfa_e == 0 and self.incl_e == 0 and self.node_e == 0 and self.time_e == 0 and \
                self.ecc_e == 0 and self.long_e == 0:
            errors = False
        else:
            errors = True
        orb_has_errors.append(errors)

        return

def get_wds_make_files(max_loops, acc_pa, acc_sep, calc_with_errors):

    f = open('Input_Files/wds_precise.txt', 'r')                 # all last precise positions in wds
    pn = open('Output_Files/not found key in 6thorbit.txt', 'w') # orbit not found (key reference missing or inexact)
    p0 = open('Output_Files/wds_positions_all.txt', 'w')         # last precise positions of physical pairs (...have orbits)
    p1 = open('Output_Files/wds_positions_acc.txt', 'w')         # difference in PA <= acc_pa and difference in Sep. <= acc_sep
    p2 = open('Output_Files/wds_positions_pa_off.txt', 'w')      #               PA  > acc_pa and               Sep. <= acc_sep
    p3 = open('Output_Files/wds_positions_sep_off.txt', 'w')     #               PA <= acc_pa and               Sep.  > acc_sep
    p4 = open('Output_Files/wds_positions_pa_sep_off.txt', 'w')  #               PA  > acc_pa and               Sep.  > acc_sep

    global no_of_with_orbits
    no_of_wds_obsv = 0
    no_of_with_orbits = 0
    no_of_not_found = 0
    no_of_skipped = 0
    no_of_with_orbits_write = 0

    pn.write(Position.make_header1())
    pn.write('\n')
    pn.write(Position.make_header2())
    pn.write('\n')
    p0.write(Position.make_header1())
    p0.write('\n')
    p0.write(Position.make_header2())
    p0.write('\n')
    p1.write(Position.make_header1())
    p1.write('\n')
    p1.write(Position.make_header2())
    p1.write('\n')
    p2.write(Position.make_header1())
    p2.write('\n')
    p2.write(Position.make_header2())
    p2.write('\n')
    p3.write(Position.make_header1())
    p3.write('\n')
    p3.write(Position.make_header2())
    p3.write('\n')
    p4.write(Position.make_header1())
    p4.write('\n')
    p4.write(Position.make_header2())
    p4.write('\n')

    for pos in f:
        no_of_wds_obsv += 1
        ix = 0
        w = Position.get(pos)
        if Position.has_orbit(w):
            no_of_with_orbits += 1
            comp_with_spc = w.comp
            comp_with_no_spc = comp_with_spc.rstrip()
            try:
                ix = orb_wds_disc.index(w.coor_2k+w.disc+comp_with_no_spc)
                if orb_may_be_calc[ix]:
                    print('Calculating Position of '+w.coor_2k+w.disc+comp_with_no_spc)
                    w.calc_pos_pa, w.calc_pos_sep = Position.calc(orb_per[ix], orb_alfa[ix],
                                                                  orb_incl[ix], orb_long[ix],
                                                                  orb_time[ix], orb_ecc[ix],
                                                                  orb_node[ix], w.epoch, max_loops)

                    w.diff_pos_pa, w.diff_pos_sep = Position.diff(w.calc_pos_pa, w.obsv_pos_pa, w.calc_pos_sep, w.obsv_pos_sep)

                    if calc_with_errors:
                        if orb_has_errors[ix]:
                            print('Calculating with Errors - Differences of ' + w.coor_2k + w.disc + comp_with_no_spc)
                            w.calc_pos_pa_err_min, calc_pos_sep_err_min = Position.calc(orb_per[ix] - orb_per_e[ix],
                                                                                        orb_alfa[ix] - orb_alfa_e[ix],
                                                                                        orb_incl[ix] - orb_incl_e[ix],
                                                                                        orb_long[ix] - orb_long_e[ix],
                                                                                        orb_time[ix] - orb_time_e[ix],
                                                                                        orb_ecc[ix] - orb_ecc_e[ix],
                                                                                        orb_node[ix] - orb_node_e[ix],
                                                                                        w.epoch, max_loops)

                            w.calc_pos_pa_err_max, calc_pos_sep_err_max = Position.calc(orb_per[ix] + orb_per_e[ix],
                                                                                        orb_alfa[ix] + orb_alfa_e[ix],
                                                                                        orb_incl[ix] + orb_incl_e[ix],
                                                                                        orb_long[ix] + orb_long_e[ix],
                                                                                        orb_time[ix] + orb_time_e[ix],
                                                                                        orb_ecc[ix] + orb_ecc_e[ix],
                                                                                        orb_node[ix] + orb_node_e[ix],
                                                                                        w.epoch, max_loops)

                    p0.write(Position.make_line(w, orb_grade[ix]))                  # all
                    p0.write('\n')
                    no_of_with_orbits_write += 1
                    
                    # split into files depending on difference in OBSV-CALC pa & sep
                    if abs(w.diff_pos_pa) <= acc_pa and abs(w.diff_pos_sep) <= acc_sep:
                        p1.write(Position.make_line(w, orb_grade[ix]))              # pa & sep within range
                        p1.write('\n')
                    elif abs(w.diff_pos_pa) > acc_pa and abs(w.diff_pos_sep) <= acc_sep:
                        p2.write(Position.make_line(w, orb_grade[ix]))              # pa outside range
                        p2.write('\n')
                    elif abs(w.diff_pos_pa) <= acc_pa and abs(w.diff_pos_sep) > acc_sep:
                        p3.write(Position.make_line(w, orb_grade[ix]))              # sep outside range
                        p3.write('\n')
                    else:
                        p4.write(Position.make_line(w, orb_grade[ix]))              # pa & sep outside range
                        p4.write('\n')
                else:
                    no_of_skipped += 1  # may not be calculated

            except ValueError:              # is supposed to have orbit in 6th but none exists!? id. problem!
                pn.write(Position.make_line(w, 0))
                pn.write('\n')
                no_of_not_found += 1

        del w               # delete instance from memory

    p0.write(Position.make_footer1())
    p0.write('\n')
    p0.write(Position.make_footer2(no_of_wds_obsv, no_of_with_orbits, no_of_not_found, no_of_with_orbits_write, no_of_skipped))
    p0.write('\n')

    pn.close()
    p0.close()
    p1.close()
    p2.close()
    p3.close()
    p4.close()
    f.close()

    print('No of wds obsv. read      : ', no_of_wds_obsv)
    print('    with orbits           : ', no_of_with_orbits)
    print('    with orbits written   : ', no_of_with_orbits_write)
    print('    rejected (incalcuable): ', no_of_skipped)
    print('    not found (wrong id.) : ', no_of_not_found)


def get_orbits():

    f = open('Input_Files/orb6orbits with pipe.txt', 'r')    # all orbits in 6th cat.
    c = open('Output_Files/calcuable orbits.txt', 'w')        # all orbits with high grade orbits and periods in years
    s = open('Output_Files/skipped orbits.txt', 'w')          # orbits rejected

    no_of_calcuable = 0
    no_of_rejected = 0
    no_of_orbits = 0

    f.readline()  # read header 1
    f.readline()  # read header 2
    for orbit in f:  # read orbital data
        no_of_orbits += 1
        o = Orbit.get(orbit)
        if Orbit.is_calcuable(o):    # may set to skip = 1
            no_of_calcuable += 1
            c.write(Orbit.make_line(o))
            c.write('\n')
        else:
            no_of_rejected += 1
            s.write(f'{o.wds} skipped due to grade {o.grade},  period unit {o.per_u}, alfa unit {o.alfa_u}')
            s.write('\n')

        Orbit.append_orbit_elt(o) # store in array regardless of skipped or not

        del o                  # delete instance from memory

    f.close()
    c.close()
    s.close()

    print('No of read 6th cat. orbits                :', no_of_orbits)
    print(' rejected  (grade, period-  or alfa-unit) :', no_of_rejected)
    print(' calcuable                                :', no_of_calcuable)

    return

# --------------- "Mission Control" --------------
get_orbits()
get_wds_make_files(30000, 0,0,True)        # max_loops for anomaly, diff in pa, diff. in sep, boolean calc_with_errors
# ------------------------------------------------
