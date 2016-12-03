# ECS165A HW4
# Valerie Cho 998831802
# Selena Tuyen

import psycopg2
import csv
import os

conn = psycopg2.connect("dbname='fakeudb'")
cur = conn.cursor()

# Write a program that will find an open room for course expansion. The program must prompt for term, CID, and number students to add. The room(s) returned should be ordered from best to worst fit with up to 5 results. Assume that each room capacity is the maximum number of students listed for any particular meeting in the data files (don’t forget that
# lectures may be split across multiple CIDs).

term = input('Enter term: ')
CID = input('Enter CID: ')
numStu = input('Enter number of students: ')
print term, CID, numStu

cur.close()
conn.close()
