course(CID,TERM,SUBJ,CRSE,SEC,UNITS)
meeting(INSTRUCTOR,TYPE,DAYS,TIME,BUILD,ROOM)
student(SEAT,SID,SURNAME,PREFNAME,LEVEL,UNITS,CLASS,MAJOR,GRADE,STATUS,EMAIL)

TODO:
- how to deal with multiple instructors for one class

32671 students taking units

3a.
SELECT cast(c.count as float)/cast(tot.count as float) AS percentage FROM 
		(SELECT COUNT(*) FROM  (SELECT TERM, SUM(student.UNITS) AS total, student.sid FROM course, student
		WHERE student.scid = course.cid GROUP BY student.sid, TERM) AS totalStud WHERE totalStud.total = %s) AS c,
		(SELECT COUNT(*) FROM student WHERE UNITS <> 0) AS tot;

3b.

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

3c.
link = meeting x student where mcid = scid
https://www.techonthenet.com/sql/max.php

SELECT avgs.instructor, avgs.avgGpa AS "Average GPA"
FROM (SELECT instructor, AVG(gpa) AS avgGpa
  FROM (
    SELECT
      CASE
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
      END AS gpa, roster.RINSTRUCTOR AS instructor
    FROM student, roster
    WHERE student.scid = roster.rcid
  ) AS grades
  GROUP BY instructor) AS avgs,
  
  (SELECT MIN(avg) AS lowest, MAX(avg) AS highest
  FROM (
    SELECT instructor, AVG(gpa) 
    FROM (
      SELECT
        CASE
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
        END AS gpa, roster.RINSTRUCTOR AS instructor
      FROM student, roster
      WHERE student.scid = roster.rcid
    ) AS grades
    GROUP BY instructor
  ) AS averages) AS max
WHERE avgs.avgGpa = max.highest;

3d.

SELECT AVG(gpa) AS avgGpa
FROM (
    SELECT CASE
        WHEN GRADE = 'A+' OR GRADE = 'A' THEN 4
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
    END AS gpa, course.subj, course.crse
    FROM student, course
    WHERE course.subj = 'ABC' AND course.crse = 100
) AS grades

SELECT avgs.instructor, avgs.avgGpa AS "Average GPA"
FROM (SELECT instructor, AVG(gpa) AS avgGpa
  FROM (
    SELECT
      CASE
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
      END AS gpa, roster.RINSTRUCTOR AS instructor
    FROM student, roster
    WHERE student.scid = roster.rcid
  ) AS grades
  GROUP BY instructor) AS avgs,
  
  (SELECT MIN(avg) AS lowest, MAX(avg) AS highest
  FROM (
    SELECT instructor, AVG(gpa) 
    FROM (
      SELECT
        CASE
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
        END AS gpa, roster.RINSTRUCTOR AS instructor
      FROM student, roster
      WHERE student.scid = roster.rcid
    ) AS grades
    GROUP BY instructor
  ) AS averages) AS max
WHERE avgs.avgGpa = max.highest;