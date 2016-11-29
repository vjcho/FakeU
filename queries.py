# ECS165A HW4
# Valerie Cho 998831802
# Selena Tuyen

import psycopg2
import csv
import os


conn = psycopg2.connect("dbname='fakeudb'")
cur = conn.cursor()

# 3a
# for i in range(1,21):
#     cur.execute("""SELECT cast(c.count as float)/cast(tot.count as float) AS percentage FROM 
#         (SELECT COUNT(*) FROM  (SELECT TERM, SUM(student.UNITS) AS total, student.sid FROM course, student
#         WHERE student.scid = course.cid GROUP BY student.sid, TERM) AS totalStud WHERE totalStud.total = %s) AS c,
#         (SELECT COUNT(*) FROM student WHERE UNITS <> 0) AS tot;""" % (i))
#     result = cur.fetchall()
#     print i,result

# 3b
for i in range(1,21):
    cur.execute("""
        SELECT AVG(x.gpa) 
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
            END AS gpa
            FROM student, 
                (SELECT id FROM (
                    SELECT TERM, SUM(student.UNITS) AS total, student.sid AS id 
                    FROM course, student 
                    WHERE student.scid = course.cid 
                    GROUP BY student.sid, TERM) AS comb 
                WHERE comb.total = %s) AS tot
            WHERE student.sid = tot.id
        ) AS x
        """ % (i))
    result = cur.fetchall()
    print i,result

cur.close()
conn.close()