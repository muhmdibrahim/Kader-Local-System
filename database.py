import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('kader_customers.db')
        return conn
    except Error as e:
        print(e)
    return conn 

def create_tables():
    """Force-create tables with error handling"""
    conn = create_connection()
    if conn is None:
        print("Failed to connect to database")
        return False

    try:
        c = conn.cursor()

        # Create tables only if they don't exist
        c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id TEXT UNIQUE NOT NULL,
            level TEXT,
            email TEXT,
            phone TEXT,
            num_courses INTEGER,
            num_sessions INTEGER,
            schedule_day_1 TEXT,
            schedule_day_2 TEXT,
            time_slot_1 TEXT,
            time_slot_2 TEXT,
            num_attended_session INTEGER,
            num_excused_session INTEGER,
            left_sessions INTEGER,
            payment_paid INTEGER,
            payment_left INTEGER,
            account_type TEXT,
            num_of_students INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            group_id TEXT NOT NULL,
            num_students INTEGER,

            student_id_1 TEXT,
            student_id_2 TEXT,
            student_id_3 TEXT,
            student_id_4 TEXT,
            student_id_5 TEXT,

            course_name TEXT,
            num_attended_session INTEGER,
            left_sessions INTEGER,
            schedule_day_1 TEXT,
            schedule_day_2 TEXT,
            time_slot_1 TEXT,
            time_slot_2 TEXT,

            FOREIGN KEY (student_id_1) REFERENCES students(student_id),
            FOREIGN KEY (student_id_2) REFERENCES students(student_id),
            FOREIGN KEY (student_id_3) REFERENCES students(student_id),
            FOREIGN KEY (student_id_4) REFERENCES students(student_id),
            FOREIGN KEY (student_id_5) REFERENCES students(student_id),
            FOREIGN KEY (course_name) REFERENCES courses(title)
        )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            credit_hours INTEGER,
            lesson_1 TEXT,
            lesson_2 TEXT,
            lesson_3 TEXT,
            lesson_4 TEXT,
            lesson_5 TEXT,
            lesson_6 TEXT,
            lesson_7 TEXT,
            lesson_8 TEXT,
            lesson_9 TEXT,
            lesson_10 TEXT,
            lesson_11 TEXT,
            lesson_12 TEXT
        )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            student_id INTEGER,
            course_id INTEGER,
            enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (course_id) REFERENCES courses (id)
        )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL,
            feedback TEXT,
            rating INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
        ''')

        conn.commit()
        print("Tables created successfully")
        return True

    except Error as e:
        print(f"Table creation failed: {e}")
        return False

    finally:
        conn.close()

def get_students():
    """Get all students from database"""
    conn = create_connection()
    students = []
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM students")
            students = c.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.close()
    
    return students

def get_total_students_count():
    """Get total number of students"""
    conn = create_connection()
    total = 0
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT COUNT(student_id) FROM students")
            result = c.fetchone()
            total = result[0] if result[0] is not None else 0
        except Error as e:
            print(e)
        finally:
            conn.close()
    
    return total

def get_student_by_id(student_id):
    """Get a single student by ID"""
    conn = create_connection()
    student = None
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM students WHERE id=?", (student_id,))
            student = c.fetchone()
        except Error as e:
            print(e)
        finally:
            conn.close()
    
    return student

def add_student(name, student_id, level, email, phone, num_courses, num_sessions,
                schedule_day_1, schedule_day_2, time_slot_1, time_slot_2,
                num_attended_session, num_excused_session, left_sessions, payment_paid, payment_left,
                created_at, account_type, num_of_students):
    """Add a new student to the database"""
    conn = create_connection()

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute('''
                INSERT INTO students (
                    name, student_id, level, email, phone,
                    num_courses, num_sessions, schedule_day_1, schedule_day_2,
                    time_slot_1, time_slot_2, num_attended_session, num_excused_session,
                    left_sessions, payment_paid, payment_left, created_at,
                    account_type, num_of_students
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, student_id, level, email, phone, num_courses, num_sessions,
                  schedule_day_1, schedule_day_2, time_slot_1, time_slot_2,
                  num_attended_session, num_excused_session, left_sessions, payment_paid,
                  payment_left, created_at, account_type, num_of_students))
            conn.commit()
            return c.lastrowid
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()
    return None

def update_student(s_id, name, student_id, level, email, phone, num_courses, num_sessions,
                   schedule_day_1, schedule_day_2, time_slot_1, time_slot_2,
                   num_attended_session, num_excused_session, left_sessions, payment_paid, payment_left,
                   created_at, account_type, num_of_students):
    """Update an existing student"""
    conn = create_connection()

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute('''
                UPDATE students 
                SET name=?, student_id=?, level=?, email=?, phone=?,
                    num_courses=?, num_sessions=?, schedule_day_1=?, schedule_day_2=?,
                    time_slot_1=?, time_slot_2=?, num_attended_session=?, num_excused_session=?,
                    left_sessions=?, payment_paid=?, payment_left=?, created_at=?,
                    account_type=?, num_of_students=?
                WHERE id=?
            ''', (name, student_id, level, email, phone, num_courses, num_sessions,
                  schedule_day_1, schedule_day_2, time_slot_1, time_slot_2,
                  num_attended_session, num_excused_session, left_sessions, payment_paid,
                  payment_left, created_at, account_type, num_of_students, s_id))
            conn.commit()
            return True
        except Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
    return False

def delete_student(student_id):
    """Delete a student from the database"""
    conn = create_connection()
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("DELETE FROM students WHERE id=?", (student_id,))
            conn.commit()
            return True
        except Error as e:
            print(e)
        finally:
            conn.close()
    
    return False

def search_student(search_term):
    """Search students by name or student ID"""
    conn = create_connection()
    students = []
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute('''
                SELECT * FROM students 
                WHERE name LIKE ? OR student_id LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%'))
            students = c.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.close()
    
    return students

# ========== Group Functions ==========

def add_group(group_name, group_id, num_students,
              student_id_1, student_id_2, student_id_3, student_id_4, student_id_5,
              course_name, num_attended_session, left_sessions,
              schedule_day_1, schedule_day_2, time_slot_1, time_slot_2):
    conn = create_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute('''
                INSERT INTO groups (
                    group_name, group_id, num_students,
                    student_id_1, student_id_2, student_id_3, student_id_4, student_id_5,
                    course_name, num_attended_session, left_sessions,
                    schedule_day_1, schedule_day_2, time_slot_1, time_slot_2
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                group_name, group_id, num_students,
                student_id_1, student_id_2, student_id_3, student_id_4, student_id_5,
                course_name, num_attended_session, left_sessions,
                schedule_day_1, schedule_day_2, time_slot_1, time_slot_2
            ))
            conn.commit()
            return c.lastrowid
        except Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
    return None


def get_groups():
    conn = create_connection()
    groups = []
    if conn:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM groups")
            groups = c.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.close()
    return groups


def get_group_by_id(group_id):
    conn = create_connection()
    group = None
    if conn:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM groups WHERE id=?", (group_id,))
            group = c.fetchone()
        except Error as e:
            print(e)
        finally:
            conn.close()
    return group

def get_total_groups_count():
    """Get total number of groups"""
    conn = create_connection()
    total = 0
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT COUNT(id) FROM groups")
            result = c.fetchone()
            total = result[0] if result[0] is not None else 0
        except Error as e:
            print(e)
        finally:
            conn.close()
    return total

def update_group(gro_id, group_name, group_id, num_students,
                 student_id_1, student_id_2, student_id_3, student_id_4, student_id_5,
                 course_name, num_attended_session, left_sessions,
                 schedule_day_1, schedule_day_2, time_slot_1, time_slot_2):
    conn = create_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute('''
                UPDATE groups SET 
                    group_name=?, group_id=?, num_students=?,
                    student_id_1=?, student_id_2=?, student_id_3=?, student_id_4=?, student_id_5=?,
                    course_name=?, num_attended_session=?, left_sessions=?,
                    schedule_day_1=?, schedule_day_2=?,
                    time_slot_1=?, time_slot_2=?
                WHERE id=?
            ''', (
                group_name, group_id, num_students,
                student_id_1, student_id_2, student_id_3, student_id_4, student_id_5,
                course_name, num_attended_session, left_sessions,
                schedule_day_1, schedule_day_2, time_slot_1, time_slot_2,
                gro_id
            ))
            conn.commit()
            return True
        except Error as e:
            print(e)
        finally:
            conn.close()
    return False

def delete_group(group_id):
    conn = create_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute("DELETE FROM groups WHERE id=?", (group_id,))
            conn.commit()
            return True
        except Error as e:
            print(e)
        finally:
            conn.close()
    return False

def search_group(search_term):
    """Search groups by name or ID"""
    conn = create_connection()
    groups = []
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute('''
                SELECT * FROM groups 
                WHERE group_name LIKE ? OR id LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%'))
            groups = c.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.close()
    return groups

# courses functions
def get_courses():
    """Get all courses from database"""
    conn = create_connection()
    courses = []
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM courses")
            courses = c.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.close()
    
    return courses

def get_total_courses_count():
    """Get the sum of all courses"""
    conn = create_connection()
    total = 0
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT COUNT(code) FROM courses")
            result = c.fetchone()
            total = result[0] if result[0] is not None else 0
        except Error as e:
            print(e)
        finally:
            conn.close()
    
    return total
def get_course_by_id(course_id):
    """Get a single course by ID"""
    conn = create_connection()
    course = None
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM courses WHERE id=?", (course_id,))
            course = c.fetchone()
        except Error as e:
            print(e)
        finally:
            conn.close()
    
    return course 
def add_course(code, title, credit_hours,lesson_1=None, lesson_2=None, lesson_3=None, lesson_4=None, lesson_5=None,
               lesson_6=None, lesson_7=None, lesson_8=None, lesson_9=None, lesson_10=None,
               lesson_11=None, lesson_12=None):
    """Add a new student to the database"""
    conn = create_connection()
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute('''
                INSERT INTO courses (code, title, credit_hours, lesson_1, lesson_2, lesson_3, lesson_4, lesson_5,
                    lesson_6, lesson_7, lesson_8, lesson_9, lesson_10, lesson_11, lesson_12)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (code, title, credit_hours, lesson_1, lesson_2, lesson_3, lesson_4, lesson_5,
                  lesson_6, lesson_7, lesson_8, lesson_9, lesson_10, lesson_11, lesson_12))
            conn.commit()
            return c.lastrowid
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()
    return None

def update_course(course_id, code, title, credit_hours,
                  lesson_1=None, lesson_2=None, lesson_3=None, lesson_4=None, lesson_5=None,
                  lesson_6=None, lesson_7=None, lesson_8=None, lesson_9=None, lesson_10=None,
                  lesson_11=None, lesson_12=None):
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute('''
                UPDATE courses 
                SET code=?, title=?, credit_hours=?,lesson_1=?, lesson_2=?, lesson_3=?, lesson_4=?, 
                    lesson_5=?, lesson_6=?, lesson_7=?, lesson_8=?, lesson_9=?, lesson_10=?, lesson_11=?, 
                    lesson_12=?
                WHERE id=?
            ''', (code, title, credit_hours,
                  lesson_1, lesson_2, lesson_3, lesson_4, lesson_5,
                  lesson_6, lesson_7, lesson_8, lesson_9, lesson_10,
                  lesson_11, lesson_12, course_id))
            conn.commit()
            return True
        except Error as e:
            print(e)
        finally:
            conn.close()
    return False

    
    return False
def delete_course(id):
    """Delete a course from the database"""
    conn = create_connection()
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("DELETE FROM courses WHERE id=?", (id,))
            conn.commit()
            return True
        except Error as e:
            print(e)
        finally:
            conn.close()
    
    return False

def search_course(search_term):
    """Search courses by title or code"""
    conn = create_connection()
    courses = []
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute('''
                SELECT * FROM courses 
                WHERE title LIKE ? OR code LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%'))
            courses = c.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.close()
    
    return courses

# Add these functions to database.py
def get_student_attendance(student_id):
    """Get all attendance records for a student"""
    conn = create_connection()
    attendance = []
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("""
                SELECT * FROM attendance 
                WHERE student_id=?
                ORDER BY session_date DESC
            """, (student_id,))
            attendance = c.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.close()
    return attendance

def add_attendance_record(student_id, status, feedback=None, rating=None):
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute('''
                INSERT INTO attendance (student_id, status, feedback, rating)
                VALUES (?, ?, ?, ?)
            ''', (student_id, status, feedback, rating))
            
            # Update different counters based on status
            if status != 'excused':
                c.execute('''
                    UPDATE students 
                    SET num_attended_session = num_attended_session + 1,
                        left_sessions = left_sessions - 1
                    WHERE id = ?
                ''', (student_id,))
            elif status == 'excused':
                c.execute('''
                    UPDATE students 
                    SET num_excused_session = num_excused_session + 1
                    WHERE id = ?
                ''', (student_id,))
            
            conn.commit()
            return c.lastrowid
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()
    return None

def update_student_attended_sessions(student_id):
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            # Get counts for different statuses
            c.execute("""
                SELECT 
                    SUM(CASE WHEN status != 'excused' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN status = 'excused' THEN 1 ELSE 0 END)
                FROM attendance 
                WHERE student_id=?
            """, (student_id,))
            present_count, excused_count = c.fetchone()
            
            # Update student record
            c.execute("""
                UPDATE students 
                SET num_attended_session = ?,
                    num_excused_session = ?,
                    left_sessions = num_sessions - ?
                WHERE id=?
            """, (present_count or 0, excused_count or 0, present_count or 0, student_id))
            
            conn.commit()
            return True
        except Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
    return False
def get_attendance_record(record_id):
    """Get a single attendance record by ID"""
    conn = create_connection()
    record = None
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM attendance WHERE id=?", (record_id,))
            record = c.fetchone()
        except Error as e:
            print(e)
        finally:
            conn.close()
    
    return record
def update_attendance_record(record_id, status, feedback=None, rating=None):
    """Update an existing attendance record"""
    conn = create_connection()
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute('''
                UPDATE attendance 
                SET status=?, feedback=?, rating=?
                WHERE id=?
            ''', (status, feedback, rating, record_id))
            conn.commit()
            return True
        except Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
    return False
def delete_attendance_record(record_id):
    """Delete an attendance record"""
    conn = create_connection()
    
    if conn is not None:
        try:
            c = conn.cursor()
            # First get the student_id for this record
            c.execute("SELECT student_id FROM attendance WHERE id=?", (record_id,))
            student_id = c.fetchone()[0]
            
            # Delete the record
            c.execute("DELETE FROM attendance WHERE id=?", (record_id,))
            conn.commit()
            
            # Update the student's attendance count
            update_student_attended_sessions(student_id)
            
            return True
        except Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
    return False