# ECS165A HW4
# Valerie Cho 998831802
# Selena Tuyen

import psycopg2
import csv
import os


conn = psycopg2.connect("dbname='fakeudb'")
cur = conn.cursor()

# 3a
for i in range(1,21):
	cur.execute("""SELECT cast(c.count as float)/cast(tot.count as float) AS percentage FROM 
		(SELECT COUNT(*) FROM  (SELECT TERM, SUM(student.UNITS) AS total, student.sid FROM course, student
		WHERE student.scid = course.cid GROUP BY student.sid, TERM) AS totalStud WHERE totalStud.total = %s) AS c,
		(SELECT COUNT(*) FROM student WHERE UNITS <> 0) AS tot;""" % (i))
	result = cur.fetchall()
	print i,result

# 3b


cur.close()
conn.close()