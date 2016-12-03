# ECS 165A HW 4
# Valerie Cho 998831802
# Selena Tuyen 999085398

import psycopg2
import csv
import os
from datetime import datetime



conn = psycopg2.connect("dbname='fakeudb'")
cur = conn.cursor()

#clear tables
cur.execute("DROP TABLE IF EXISTS course")
cur.execute("DROP TABLE IF EXISTS meeting")
cur.execute("DROP TABLE IF EXISTS student")
cur.execute("DROP TABLE IF EXISTS roster")

#create tables
cur.execute("CREATE TABLE course (CID INTEGER, TERM CHAR(10), SUBJ CHAR(3), CRSE INTEGER, SEC INTEGER, UNITS CHAR(20), CLASS CHAR(10))")
cur.execute("CREATE TABLE meeting (INSTRUCTOR CHAR(32), TYPE CHAR(25), DAYS CHAR(10), starttime TIME, endtime TIME, BUILD CHAR(10), ROOM CHAR(10), MCID INTEGER, TERM CHAR(10))") #, MCID INTEGER REFERENCES course(CID)")
cur.execute("CREATE TABLE student (SEAT INTEGER, SID INTEGER, SURNAME CHAR(32), PREFNAME CHAR(32), LEVEL CHAR(6), UNITS FLOAT, CLASS CHAR(5), MAJOR CHAR(8), GRADE CHAR(20), STATUS CHAR(40), EMAIL CHAR(60), SCID INTEGER, STERM CHAR(10))")
cur.execute("CREATE TABLE roster (RCID INTEGER, RINSTRUCTOR CHAR(32), RSID INTEGER, RTERM CHAR(20))")
#TODO: set primary keys and table relationships

course_str = ''
meeting_str = ''
stud_str = ''
roster_str = ''
stud_id = []

meetings = []
courses = []

coursear = []
meetingar = []
studar = []
rosterar = []

cid = 0
instructor = ''
sid = 0
term = ''

rosterobj = []

prevheader = True 

for filename in os.listdir('./Grades'):
    print filename
    schema = 'none'
    with open(os.path.join('./Grades', filename), "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if schema == 'none':
                if row[0] == 'CID':
                    schema = 'course'
                elif row[0] == 'INSTRUCTOR(S)':
                    schema = 'meeting'
                elif row[0] == 'SEAT':
                    schema = 'student'
                prevheader = True
                continue 
            elif len(row) == 1: # empty row
                if schema == 'student' and prevheader == True:
                    # no students so delete meeting and course
                    if len(coursear) > 0:
                        coursear.pop()
                    if len(meetingar) > 0:
                        meetingar.pop()
                schema = 'none'
            elif schema == 'course':
                # print row[2] + row[3]
                row.append(row[2] + row[3])
                coursear.append(row)
                cobj = {}
                cobj['course'] = row[3]
                cobj['subject'] = row[2]
                courses.append(cobj)
                cid = row[0]
                # print cid
                term = row[1]
                prevheader = False
            elif schema == 'meeting':
                obj = {}
                obj['days'] = row[2]
                obj['time'] = row[3]
                obj['build'] = row[4]
                obj['room'] = row[5]

                # print obj

                # if obj in meetings:
                #     # print len(courses)
                #     # print len(meetings)
                #     if len(courses) > 0 and courses[-1] != courses[meetings.index(obj)]:
                #     # print 'true'
                #         if courses[-1]['course'] == '103' and courses[-1]['subject'] == 'ABC':
                #             print obj
                #             print courses[-1]
                #             print courses[meetings.index(obj)]
                #         coursear[-1][1] = coursear[-1][1] + '-b'
                timestr = row[3]
                # timestr = "10:00 AM - 10:50 AM"
                starttime = None
                endtime = None
                if timestr != '':
                    times = timestr.split('-')
                    # print times
                    starttime = datetime.strptime(times[0],'%I:%M %p ').strftime('%H:%M')
                    endtime = datetime.strptime(times[1], ' %I:%M %p').strftime('%H:%M')
                    # print starttime
                    # print endtime
                row[3] = starttime
                row.insert(4, endtime)

                meetings.append(obj)
                if prevheader == True:
                    instructor = row[0]
                # print cid
                row.append(cid)
                row.append(term)
                meetingar.append(row)

                #meeting_str += '('
                #meeting_str += cur.mogrify("%s,%s,%s,%s,%s,%s", (row[0],row[1],row[2],row[3],row[4],row[5]))
                #meeting_str += '),'

                
                if prevheader == False:
                    courses.append(courses[-1])
                prevheader = False
            elif schema == 'student':
                #if len(row) == 11:
                if row[5] == '':
                    row[5] = 0
                # if row[1] not in stud_id:
                    #print row[2] + ',' + row[3]
                    #stud_str += '('
                    #stud_str += cur.mogrify("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10]))
                    #stud_str += '),'
                row.append(cid)
                studar.append(row)
                row.append(term)
                stud_id.append(row[1])
                
                # rosterobj.append(row[1])
                
                prevheader = False
                sid = row[1]
                rosterar.append([cid,instructor,sid,term])
    meetings = []
    courses = []


for r in coursear:
    course_str += '('
    course_str += cur.mogrify("%s,%s,%s,%s,%s,%s,%s", (r[0],r[1],r[2],r[3],r[4],r[5],r[6]))
    course_str += '),'

for r in meetingar:
    meeting_str += '('
    meeting_str += cur.mogrify("%s,%s,%s,%s,%s,%s,%s,%s,%s", (r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8]))
    meeting_str += '),'

for r in studar:
    stud_str += '('
    stud_str += cur.mogrify("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s", (r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12]))
    stud_str += '),'

for r in rosterar:
    roster_str += '('
    roster_str += cur.mogrify("%s,%s,%s,%s", (r[0],r[1],r[2],r[3]))
    roster_str += '),'

course_str = course_str[:-1]
meeting_str = meeting_str[:-1]
stud_str = stud_str[:-1]
roster_str = roster_str[:-1]

# print rosterar

# print len(stud_id)
print 'Inserting into database'
cur.execute("INSERT INTO course VALUES " + course_str)
print 'Done inserting courses'
cur.execute("INSERT INTO meeting VALUES " + meeting_str)
print 'Done inserting meetings'
cur.execute("INSERT INTO student VALUES " + stud_str)
print 'Done inserting students'
cur.execute("INSERT INTO roster VALUES " + roster_str)
print 'Done inserting rosters'

conn.commit()

cur.close()
conn.close()


