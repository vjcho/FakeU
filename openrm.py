# ECS165A HW4
# Valerie Cho 998831802
# Selena Tuyen

import psycopg2
import csv
import os

conn = psycopg2.connect("dbname='fakeudb'")
cur = conn.cursor()
print 'Ultimate Room Finder Program'
term = input('Enter term: ')
CID = input('Enter CID: ')
numStu = input('Enter number of students: ')
#print term, CID, numStu

cur.execute("""
	SELECT COUNT(DISTINCT stu.SID) AS sCount, stu.INSTRUCTOR, stu.ROOM, stu.BUILD, stu.TERM
	FROM 
		(
			SELECT DISTINCT SID, TERM, ROOM, BUILD, INSTRUCTOR
			FROM student, meeting 
			WHERE student.SCID = meeting.MCID AND 
			student.STERM = meeting.TERM AND
			meeting.ROOM <> -1 AND
			meeting.INSTRUCTOR <> ''
		) AS stu
	GROUP BY stu.INSTRUCTOR, stu.ROOM, stu.BUILD, stu.TERM ORDER BY sCount
	""")
data = cur.fetchall()
theRoom = -1
sidCount = [x[0] for x in data]
for i in range (0, len(data)):
	#print sidCount[i]
	if numStu <= sidCount[i]:
		theRoom = i
		break

if theRoom == -1:
	print 'Cannot find any rooms'
else:
	print 'Top 5 Rooms and Buildings:'
	print '1. Room:', data[theRoom][2], 'Building:', data[theRoom][3] 
	print '2. Room:', data[theRoom+1][2], 'Building:', data[theRoom+1][3]  
	print '3. Room:', data[theRoom+2][2], 'Building:', data[theRoom+2][3]  
	print '4. Room:', data[theRoom+3][2], 'Building:', data[theRoom+3][3]  
	print '5. Room:', data[theRoom+4][2], 'Building:', data[theRoom+4][3]   
# print [x[2] for x in data[theRoom]], [x[3] for x in data[theRoom]]
# print [x[2] for x in data[theRoom+1]], [x[3] for x in data[theRoom+1]]
# print [x[2] for x in data[theRoom+2]], [x[3] for x in data[theRoom+2]]
# print [x[2] for x in data[theRoom+3]], [x[3] for x in data[theRoom+3]]
# print [x[2] for x in data[theRoom+4]], [x[3] for x in data[theRoom+4]]
cur.close()
conn.close()