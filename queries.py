# ECS165A HW4
# Valerie Cho 998831802
# Selena Tuyen 999085398

import psycopg2
import csv
import os


conn = psycopg2.connect("dbname='fakeudb'")
cur = conn.cursor()

# 3a
print '3a:'
for i in range(1,21):
    cur.execute("""
        SELECT cast(c.count as float)/cast(tot.count as float)*100 AS percentage 
        FROM (
            SELECT COUNT(*) 
            FROM (
               SELECT TERM, SUM(student.UNITS) AS total, student.sid 
               FROM course, student
               WHERE student.scid = course.cid GROUP BY student.sid, TERM) AS totalStud 
            WHERE totalStud.total = %s) AS c,
        (SELECT COUNT(*) FROM student WHERE UNITS <> 0) AS tot;
        """ % (i))
    result = cur.fetchall()
    print i,result

# 3b
print '3b:'
# weighted gpa
for i in range(1,21):
    cur.execute("""   
        SELECT AVG(weighted)
        FROM(
            SELECT SUM(gpa)/SUM(units) AS weighted, term, sid
            FROM (
                SELECT sid, term, cid, student.units, CASE
                        WHEN GRADE = 'A+' OR GRADE = 'A' THEN 4.0 * student.UNITS
                        WHEN GRADE = 'A-' THEN 3.7 * student.UNITS
                        WHEN GRADE = 'B+' THEN 3.33 * student.UNITS
                        WHEN GRADE = 'B' THEN 3 * student.UNITS
                        WHEN GRADE = 'B-' THEN 2.7 * student.UNITS
                        WHEN GRADE = 'C+' THEN 2.3 * student.UNITS
                        WHEN GRADE = 'C' THEN 2 * student.UNITS
                        WHEN GRADE = 'C-' THEN 1.7 * student.UNITS
                        WHEN GRADE = 'D+' THEN 1.3 * student.UNITS
                        WHEN GRADE = 'D' THEN 1 * student.UNITS
                        WHEN GRADE = 'D-' THEN .7 * student.UNITS
                        WHEN GRADE = 'F' THEN 0
                    END AS gpa 
                FROM student, course
                WHERE student.scid = course.cid AND student.sterm = course.term
            ) AS x
            WHERE gpa is not null
            GROUP BY term, sid
            HAVING SUM(units) = %s
        ) AS weight;
        """ % (i))
    result = cur.fetchall()
    print i, result

# 3c
print '3c:'
cur.execute("""
    SELECT SUM(gpa)/SUM(units) AS weighted, instructor
    FROM (
        SELECT CASE
            WHEN GRADE = 'A+' OR GRADE = 'A' THEN 4.0 * student.UNITS
            WHEN GRADE = 'A-' THEN 3.7 * student.UNITS
            WHEN GRADE = 'B+' THEN 3.33 * student.UNITS
            WHEN GRADE = 'B' THEN 3 * student.UNITS
            WHEN GRADE = 'B-' THEN 2.7 * student.UNITS
            WHEN GRADE = 'C+' THEN 2.3 * student.UNITS
            WHEN GRADE = 'C' THEN 2 * student.UNITS
            WHEN GRADE = 'C-' THEN 1.7 * student.UNITS
            WHEN GRADE = 'D+' THEN 1.3 * student.UNITS
            WHEN GRADE = 'D' THEN 1 * student.UNITS
            WHEN GRADE = 'D-' THEN .7 * student.UNITS
            WHEN GRADE = 'F' THEN 0
        END AS gpa, course.subj, course.crse, roster.rinstructor AS instructor, course.term, course.cid, student.units
        FROM student, course, roster
        WHERE student.scid = course.cid AND roster.rcid = course.cid AND roster.rcid = student.scid
    ) AS grades
    WHERE instructor <> '' AND gpa is not null
    GROUP BY instructor
    """)
results = cur.fetchall()
gpas = [x[0] for x in results]
instructors = [x[1] for x in results]

maxindex = gpas.index(max(gpas))
minindex = gpas.index(min(gpas))
print "Easiest Instructor | Hardest Instructor"
print instructors[maxindex],max(gpas),'|',instructors[minindex],min(g for g in gpas if g is not None)

# 3d
print '3d:'
print "Easiest Instructor | Hardest Instructor"
for i in range(101,115): # only takes into account classes that have instructors
    cur.execute("""
        SELECT SUM(gpa)/SUM(units) AS weighted, instructor, subj, crse
        FROM (
            SELECT CASE
                WHEN GRADE = 'A+' OR GRADE = 'A' THEN 4.0 * student.UNITS
                WHEN GRADE = 'A-' THEN 3.7 * student.UNITS
                WHEN GRADE = 'B+' THEN 3.33 * student.UNITS
                WHEN GRADE = 'B' THEN 3 * student.UNITS
                WHEN GRADE = 'B-' THEN 2.7 * student.UNITS
                WHEN GRADE = 'C+' THEN 2.3 * student.UNITS
                WHEN GRADE = 'C' THEN 2 * student.UNITS
                WHEN GRADE = 'C-' THEN 1.7 * student.UNITS
                WHEN GRADE = 'D+' THEN 1.3 * student.UNITS
                WHEN GRADE = 'D' THEN 1 * student.UNITS
                WHEN GRADE = 'D-' THEN .7 * student.UNITS
                WHEN GRADE = 'F' THEN 0
            END AS gpa, course.subj, course.crse, roster.rinstructor AS instructor, course.term, course.cid, student.units
            FROM student, course, roster
            WHERE student.scid = course.cid AND roster.rcid = course.cid AND roster.rcid = student.scid AND course.subj = 'ABC' AND course.crse BETWEEN 100 AND 199
        ) AS grades
        WHERE crse = %s AND instructor <> '' AND gpa is not null
        GROUP BY instructor, subj, crse
        """ % (i))
    result = cur.fetchall()
    gpas = [x[0] for x in result]
    instructors = [x[1] for x in result]
    subjs = [x[2] for x in result]
    crses = [x[3] for x in result]

    
    if len(gpas) == 0 or max(gpas) == None:
        passrate = []
        cur.execute("""
            SELECT COUNT(*), instructor, subj, crse
            FROM (
                SELECT grade, course.subj, course.crse, roster.rinstructor AS instructor, course.term, course.cid
                FROM student, course, roster
                WHERE student.scid = course.cid AND roster.rcid = course.cid AND roster.rcid = student.scid AND course.subj = 'ABC' AND course.crse BETWEEN 100 AND 199
            ) AS grades
            WHERE crse = %s AND grade = 'P' AND instructor <> ''
            GROUP BY instructor, subj, crse
            """ % (i))
        passesResult = cur.fetchall()
        passes = [x[0] for x in passesResult]
        pinstructors = [x[1] for x in passesResult]
        subjs = [x[2] for x in passesResult]
        crses = [x[3] for x in passesResult]

        cur.execute("""
            SELECT COUNT(*), instructor, subj, crse
            FROM (
                SELECT grade, course.subj, course.crse, roster.rinstructor AS instructor, course.term, course.cid
                FROM student, course, roster
                WHERE student.scid = course.cid AND roster.rcid = course.cid AND roster.rcid = student.scid AND course.subj = 'ABC' AND course.crse BETWEEN 100 AND 199
            ) AS grades
            WHERE crse = %s AND instructor <> ''
            GROUP BY instructor, subj, crse
            """ % (i))
        total = cur.fetchall()
        total = [x[0] for x in total]
        for k in range(0,len(passes)):
            passrate.append(float(passes[k])/float(total[k]) * 100)
        maxindexes = []
        minindexes = []
        maxpassrate = max(passrate)
        minpassrate = min(passrate)
        # print len(passrate), len(pinstructors)
        for k in range(0, len(passrate)):
            if passrate[k] == maxpassrate:
                maxindexes.append(k)
            if passrate[k] == minpassrate:
                minindexes.append(k)
        maxindex = passrate.index(max(passrate))
        minindex = passrate.index(min(passrate))
        print subjs[0], crses[0], 'Easiest Instructors:'
        for index in maxindexes:
            print max(passrate), pinstructors[index]

        print subjs[0],crses[0], 'Hardest Instructors:'
        for index in minindexes:
            print min(passrate), pinstructors[index]
    else:
        maxindex = gpas.index(max(gpas))
        minindex = gpas.index(min(gpas))
        print subjs[0], crses[0], max(gpas), instructors[maxindex], '|', min(g for g in gpas if g is not None), instructors[minindex]

# 3e
print '3e'
cur.execute("""
    SELECT c1.class,c2.class
    FROM
    (SELECT *, meeting.term AS term1
    FROM meeting, course
    WHERE meeting.mcid = course.cid AND meeting.term = course.term) AS c1, 
    (SELECT *, meeting.term AS term2
    FROM meeting, course
    WHERE meeting.mcid = course.cid AND meeting.term = course.term) AS c2
    WHERE c1.term1 = c2.term2 AND RIGHT(c1.term1,2) = '06' AND c1.days ~ c2.days AND 
    ((c1.starttime >= c2.starttime AND c1.starttime <= c2.endtime) 
        OR (c2.starttime >= c1.starttime AND c2.starttime <= c1.endtime)
        OR (c1.endtime <= c2.endtime AND c1.endtime >= c2.starttime)
        OR (c2.endtime <= c1.endtime AND c2.endtime >= c1.starttime)
        OR (c1.starttime = c2.starttime AND c1.endtime = c2.endtime)) 
    AND c1.build = c2.build AND c1.room = c2.room AND c1.class <> c2.class
    GROUP BY c1.class, c2.class;
    """)
result = cur.fetchall()

cur.execute("""
    SELECT x.class1, x.class2
    FROM(
    (SELECT c1.class1, c2.class2, c1.sid, c2.sid, c1.major, c2.major, c1.sterm, c2.sterm
    FROM
    (SELECT *, course.class AS class1, student.class AS sclass1 
    FROM student, course
    WHERE student.scid = course.cid AND student.sterm = course.term
    ) AS c1, 
    (SELECT *, course.class AS class2, student.class AS sclass2
    FROM student, course
    WHERE student.scid = course.cid AND student.sterm = course.term
    ) AS c2
    WHERE c1.term = c2.term AND RIGHT(c1.term,2) = '06' AND c1.sid = c2.sid AND c1.major <> c2.major)
    UNION
    (SELECT c1.class1, c2.class2, c1.sid, c2.sid, c1.major, c2.major, c1.sterm, c2.sterm
    FROM
    (SELECT *, course.class AS class1, student.class AS sclass1 
    FROM student, course
    WHERE student.scid = course.cid AND student.sterm = course.term
    ) AS c1, 
    (SELECT *, course.class AS class2, student.class AS sclass2
    FROM student, course
    WHERE student.scid = course.cid AND student.sterm = course.term
    ) AS c2
    WHERE c1.term = c2.term AND RIGHT(c1.term,2) = '06' AND c1.sid = c2.sid AND c1.sclass1 <> c2.sclass2)
    UNION
    (SELECT c1.class1, c2.class2, c1.sid, c2.sid, c1.major, c2.major, c1.sterm, c2.sterm
    FROM
    (SELECT *, course.class AS class1, student.class AS sclass1 
    FROM student, course
    WHERE student.scid = course.cid AND student.sterm = course.term
    ) AS c1, 
    (SELECT *, course.class AS class2, student.class AS sclass2
    FROM student, course
    WHERE student.scid = course.cid AND student.sterm = course.term
    ) AS c2
    WHERE c1.term = c2.term AND RIGHT(c1.term,2) = '06' AND c1.sid = c2.sid AND c1.status <> c2.status)
    UNION
    (SELECT c1.class1, c2.class2, c1.sid, c2.sid, c1.major, c2.major, c1.sterm, c2.sterm
    FROM
    (SELECT *, course.class AS class1, student.class AS sclass1 
    FROM student, course
    WHERE student.scid = course.cid AND student.sterm = course.term
    ) AS c1, 
    (SELECT *, course.class AS class2, student.class AS sclass2
    FROM student, course
    WHERE student.scid = course.cid AND student.sterm = course.term
    ) AS c2
    WHERE c1.term = c2.term AND RIGHT(c1.term,2) = '06' AND c1.sid = c2.sid AND c1.level <> c2.level)
    ) AS x
    GROUP BY x.class1, x.class2;
    """)
result2 = cur.fetchall()

# print unique combinations
classes = []
ans = []
first = [x[0] for x in result]
sec = [x[1] for x in result]
for i in range(0,len(first)):
    if first[i] in classes and sec[i] in classes:
        continue
    else:
        classes.append(first[i])
        classes.append(sec[i])
        ans.append((first[i],sec[i]))

first = [x[0] for x in result2]
sec = [x[1] for x in result2]
for i in range(0,len(first)):
    if first[i] in classes and sec[i] in classes:
        continue
    else:
        classes.append(first[i])
        classes.append(sec[i])
        ans.append((first[i],sec[i]))

print sorted(ans)

#3f
print '3f:'
cur.execute("""
    SELECT avgs.majors, avgs.avgpa 
    FROM (SELECT majors, AVG(gpa) AS avgpa
        FROM (
            SELECT CASE
                WHEN GRADE = 'A+' OR GRADE = 'A' THEN 4.0
                WHEN GRADE = 'A-' THEN 3.7
                WHEN GRADE = 'B+' THEN 3.33
                WHEN GRADE = 'B' THEN 3
                WHEN GRADE = 'B-' THEN 2.7
                WHEN GRADE = 'C+' THEN 2.3
                WHEN GRADE = 'C' THEN 2
                WHEN GRADE = 'C-' THEN 1.7
                WHEN GRADE = 'D+' THEN 1.3
                WHEN GRADE = 'D' THEN 1
                WHEN GRADE = 'D-' THEN .7
                WHEN GRADE = 'F' THEN 0
            END AS gpa, student.major AS majors, course.cid AS crs, course.subj AS sub
            FROM student, course
            WHERE student.scid = course.cid AND course.subj = 'ABC'
        ) AS grades
    GROUP BY majors) AS avgs,

    (SELECT MIN(avg) AS lowest, MAX(avg) AS highest
    FROM (
        SELECT majors, AVG(gpa) 
        FROM (
            SELECT CASE
                WHEN GRADE = 'A+' OR GRADE = 'A' THEN 4.0
                WHEN GRADE = 'A-' THEN 3.7
                WHEN GRADE = 'B+' THEN 3.33
                WHEN GRADE = 'B' THEN 3
                WHEN GRADE = 'B-' THEN 2.7
                WHEN GRADE = 'C+' THEN 2.3
                WHEN GRADE = 'C' THEN 2
                WHEN GRADE = 'C-' THEN 1.7
                WHEN GRADE = 'D+' THEN 1.3
                WHEN GRADE = 'D' THEN 1
                WHEN GRADE = 'D-' THEN .7
                WHEN GRADE = 'F' THEN 0
            END AS gpa, student.major AS majors, course.cid AS crs, course.subj AS sub
            FROM student, course
            WHERE student.scid = course.cid AND course.subj = 'ABC'
        ) AS grades
    GROUP BY majors) AS averages) AS MAX
    WHERE avgs.avgpa = max.highest;  
    """)
max = cur.fetchall()
print max

cur.execute("""
    SELECT avgs.majors, avgs.avgpa 
    FROM (SELECT majors, AVG(gpa) AS avgpa
        FROM (
            SELECT CASE
                WHEN GRADE = 'A+' OR GRADE = 'A' THEN 4.0
                WHEN GRADE = 'A-' THEN 3.7
                WHEN GRADE = 'B+' THEN 3.33
                WHEN GRADE = 'B' THEN 3
                WHEN GRADE = 'B-' THEN 2.7
                WHEN GRADE = 'C+' THEN 2.3
                WHEN GRADE = 'C' THEN 2
                WHEN GRADE = 'C-' THEN 1.7
                WHEN GRADE = 'D+' THEN 1.3
                WHEN GRADE = 'D' THEN 1
                WHEN GRADE = 'D-' THEN .7
                WHEN GRADE = 'F' THEN 0
            END AS gpa, student.major AS majors, course.cid AS crs, course.subj AS sub
            FROM student, course
            WHERE student.scid = course.cid AND course.subj = 'ABC'
        ) AS grades
    GROUP BY majors) AS avgs,

    (SELECT MIN(avg) AS lowest, MAX(avg) AS highest
    FROM (
        SELECT majors, AVG(gpa) 
        FROM (
            SELECT CASE
                WHEN GRADE = 'A+' OR GRADE = 'A' THEN 4.0
                WHEN GRADE = 'A-' THEN 3.7
                WHEN GRADE = 'B+' THEN 3.33
                WHEN GRADE = 'B' THEN 3
                WHEN GRADE = 'B-' THEN 2.7
                WHEN GRADE = 'C+' THEN 2.3
                WHEN GRADE = 'C' THEN 2
                WHEN GRADE = 'C-' THEN 1.7
                WHEN GRADE = 'D+' THEN 1.3
                WHEN GRADE = 'D' THEN 1
                WHEN GRADE = 'D-' THEN .7
                WHEN GRADE = 'F' THEN 0
            END AS gpa, student.major AS majors, course.cid AS crs, course.subj AS sub
            FROM student, course
            WHERE student.scid = course.cid AND course.subj = 'ABC'
        ) AS grades
    GROUP BY majors) AS averages) AS MAX
    WHERE avgs.avgpa = max.lowest;  
    """)
min = cur.fetchall()
print min

#3g
print '3g:'
cur.execute("""
    SELECT COUNT(DISTINCT theStudent.student1)
    FROM
        (SELECT DISTINCT sameSIDs.student1, sameSIDs.studentMaj
        FROM
            (SELECT s1.SID AS student1, s1.major AS studentMaj
             FROM student s1, student s2
             WHERE s1.SID = s2.SID AND s1.major NOT LIKE 'ABC%'
            )AS sameSIDs) AS theStudent, roster r1, roster r2, student laterStudent
    WHERE
        theStudent.student1 = r1.RSID AND 
        theStudent.student1 = r2.RSID AND 
        theStudent.student1 = laterStudent.SID AND 
        laterStudent.major LIKE 'ABC%' AND
        r1.RTERM < r2.RTERM; 
    """)
trans = cur.fetchall()

cur.execute("""
    SELECT COUNT(DISTINCT SID)
    FROM STUDENT;
    """)
total = cur.fetchall()
ans = [x[0] for x in trans]
ans2 = [x[0] for x in total]
print float(ans[0])/float(ans2[0]) * 100


cur.execute("""
    SELECT COUNT(DISTINCT theStudent.student1), theStudent.studentMaj
    FROM
        (SELECT DISTINCT sameSIDs.student1, sameSIDs.studentMaj
        FROM
            (SELECT s1.SID AS student1, s1.major AS studentMaj
             FROM student s1, student s2
             WHERE s1.SID = s2.SID AND s1.major NOT LIKE 'ABC%'
            )AS sameSIDs) AS theStudent, roster r1, roster r2, student laterStudent
    WHERE
        theStudent.student1 = r1.RSID AND
        theStudent.student1 = r2.RSID AND
        theStudent.student1 = laterStudent.SID AND
        laterStudent.major LIKE 'ABC%' AND
        r1.RTERM < r2.RTERM
    GROUP BY theStudent.studentMaj ORDER BY COUNT(DISTINCT theStudent.student1) DESC
    LIMIT 5;
    """)
majorCount= cur.fetchall()

cur.execute("""
    SELECT SUM(st.totTrans)
    FROM(
        SELECT COUNT(DISTINCT theStudent.student1) AS totTrans
        FROM
            (SELECT DISTINCT sameSIDs.student1, sameSIDs.studentMaj
            FROM
                (SELECT s1.SID AS student1, s1.major AS studentMaj
                 FROM student s1, student s2
                 WHERE s1.SID = s2.SID AND s1.major NOT LIKE 'ABC%'
                )AS sameSIDs) AS theStudent, roster r1, roster r2, student laterStudent
        WHERE
            theStudent.student1 = r1.RSID AND
            theStudent.student1 = r2.RSID AND
            theStudent.student1 = laterStudent.SID AND
            laterStudent.major LIKE 'ABC%' AND
            r1.RTERM < r2.RTERM
        GROUP BY theStudent.studentMaj) AS st;
    """)

total = cur.fetchall()
count = [x[0] for x in majorCount]

major = [x[1] for x in majorCount]
ans2 = [x[0] for x in total]
for i in range (0,5):
    print float(count[i])/float(ans2[0]) * 100, '%',  major[i]

cur.close()
conn.close()
