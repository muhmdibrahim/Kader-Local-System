from flask import Flask, render_template, request, redirect, url_for, flash
from database import (
    # Students
    get_students, get_student_by_id, add_student, update_student, delete_student, 
    get_total_students_count, search_student,

    # Courses
    get_courses, get_total_courses_count, get_course_by_id, add_course, 
    update_course, delete_course, search_course,

    # Groups
    get_groups, get_group_by_id, add_group, get_total_groups_count , update_group, delete_group, 
    search_group,
    # Attendence(students)
    get_student_attendance, add_attendance_record, update_student_attended_sessions, get_attendance_record,
    update_attendance_record, delete_attendance_record
)
from flask_mail import Mail, Message
# Debug database status
from database import create_tables, create_connection
from datetime import datetime

# Check and show database status
def check_database():
    print("\n=== DATABASE DEBUG INFO ===")
    
    conn = create_connection()
    if not conn:
        print("[ERROR] Database connection failed")
        return
    
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    print(f"Found tables: {[t[0] for t in tables]}")
    conn.close()

# Initialize database
if create_tables():
    print("[OK] Database initialized successfully")
else:
    print("[ERROR] Database initialization failed")

check_database()  # Debug log

from datetime import datetime 
app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kadertechacademy@gmail.com'  # Your Gmail
app.config['MAIL_PASSWORD'] = 'jsurvzvmswwsmhse'     # App password (not Gmail password!)

mail = Mail(app)
@app.route('/')
def index():
    return render_template('index.html',
                        total_students_count=get_total_students_count(),
                        course_count=get_total_courses_count(),
                        group_count=get_total_groups_count())

@app.route('/students')
def students():
    search_term = request.args.get('search', '')
    if search_term:
        students = search_student(search_term)
    else:
        students = get_students()
    return render_template('students.html', students=students, search_term=search_term)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student_route():
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']
        level = request.form['level']
        email = request.form['email']
        phone = request.form['phone']
        num_courses = int(request.form.get('num_courses', 0))
        num_sessions = num_courses * 12
        schedule_day_1 = request.form.get('schedule_day_1')
        schedule_day_2 = request.form.get('schedule_day_2')
        time_slot_1 = request.form.get('time_slot_1')
        time_slot_2 = request.form.get('time_slot_2')
        num_attended = int(request.form.get('num_attended_session', 0))
        num_excused = int(request.form.get('num_excused_session', 0))  # New field
        left_sessions = num_sessions - num_attended
        payment_paid = int(request.form.get('payment_paid', 0.0))
        account_type = request.form.get('account_type', 'online')
        num_of_students = int(request.form.get('num_of_students', 1))

        # Calculate payment_left based on the new logic
        if account_type == "offline":
            if num_courses == 1:
                payment_left = 1800 - payment_paid
            elif num_courses == 2:
                payment_left = 3400 - payment_paid
            elif num_courses == 4:
                payment_left = 6600 - payment_paid
            else:
                payment_left = 0.0
        else:  # online
            if num_of_students == 1:
                if num_courses == 1:
                    payment_left = 2100 - payment_paid
                elif num_courses == 2:
                    payment_left = 4000 - payment_paid
                elif num_courses == 4:
                    payment_left = 7800 - payment_paid
                else:
                    payment_left = 0.0
            else:  # 2 or more students
                if num_courses == 1:
                    payment_left = 1500 - payment_paid
                elif num_courses == 2:
                    payment_left = 2900 - payment_paid
                elif num_courses == 4:
                    payment_left = 5700 - payment_paid
                else:
                    payment_left = 0.0

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result = add_student(
            name, student_id, level, email, phone,
            num_courses, num_sessions,
            schedule_day_1, schedule_day_2,
            time_slot_1, time_slot_2,
            num_attended, num_excused,
            left_sessions,
            payment_paid, payment_left,
            account_type, num_of_students,
            created_at
        )

        if result:
            msg = Message(
                subject='Welcome To Kader👋',
                sender='kadertechacademy@gmail.com',
                recipients=[email],
                body=f"""
                السلام عليكم ورحمة الله وبركاته {name} 👋

                🎊 مبروك! تم تسجيلك بنجاح في أكاديمية كادر 🎊

                📝 تفاصيل تسجيلك:
                --------------------------
                🆔 رقم الطالب: {student_id}
                📚 المستوى: {level}
                📧 البريد الإلكتروني: {email}
                📱 الهاتف: {phone or 'غير متوفر'}
                
                🏫 التفاصيل الأكاديمية:
                --------------------------
                📖 عدد الكورسات: {num_courses}
                🕒 عدد الحصص: {num_sessions}
                ✅ الحضور: {num_attended}
                🟡 الأعذار: {num_excused}  <!-- Added excused sessions count -->
                ⏳ الحصص المتبقية: {left_sessions}
                
                💰 التفاصيل المالية:
                --------------------------
                💵 المبلغ المدفوع: {payment_paid} جنيه
                💳 المتبقي: {payment_left} جنيه
                
                🗓️ جدولك الدراسي:
                --------------------------
                📅 اليوم الأول: {schedule_day_1 or 'غير محدد'}
                ⏰ الوقت: {time_slot_1 or 'غير محدد'}
                📅 اليوم الثاني: {schedule_day_2 or 'غير محدد'}
                ⏰ الوقت: {time_slot_2 or 'غير محدد'}
                
                📅 تاريخ التسجيل: {created_at}
                
                🌟 نتمنى لك رحلة تعليمية ممتعة ومفيدة معنا!
                🏆 سنكون معك خطوة بخطوة نحو التميز
                
                مع تحيات،
                فريق أكاديمية كادر
                📞 للاستفسار: 201148102054
                """
            )
            mail.send(msg)
            return redirect(url_for('students'))

    return render_template('add.html', item_type='student', item=None)


@app.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student_route(student_id):
    student = get_student_by_id(student_id)

    if request.method == 'POST':
        name = request.form['name']
        st_id = request.form['student_id']
        level = request.form['level']
        email = request.form['email']
        phone = request.form['phone']
        num_courses = int(request.form.get('num_courses', 0))
        num_sessions = num_courses * 12
        schedule_day_1 = request.form.get('schedule_day_1')
        schedule_day_2 = request.form.get('schedule_day_2')
        time_slot_1 = request.form.get('time_slot_1')
        time_slot_2 = request.form.get('time_slot_2')
        num_attended = int(request.form.get('num_attended_session', 0))
        num_excused = int(request.form.get('num_excused_session', 0))
        left_sessions = num_sessions - num_attended
        payment_paid = int(request.form.get('payment_paid', 0))
        account_type = request.form.get('account_type', 'online')
        num_of_students = int(request.form.get('num_of_students', 1))

        # Payment logic
        if account_type == "offline":
            if num_courses == 1:
                payment_left = 1800 - payment_paid
            elif num_courses == 2:
                payment_left = 3400 - payment_paid
            elif num_courses == 4:
                payment_left = 6600 - payment_paid
            else:
                payment_left = 0.0
        else:  # online
            if num_of_students == 1:
                if num_courses == 1:
                    payment_left = 2100 - payment_paid
                elif num_courses == 2:
                    payment_left = 4000 - payment_paid
                elif num_courses == 4:
                    payment_left = 7800 - payment_paid
                else:
                    payment_left = 0.0
            else:  # 2 or more students
                if num_courses == 1:
                    payment_left = 1500 - payment_paid
                elif num_courses == 2:
                    payment_left = 2900 - payment_paid
                elif num_courses == 4:
                    payment_left = 5700 - payment_paid
                else:
                    payment_left = 0.0

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        update_student(
            student_id, name, st_id, level, email, phone,
            num_courses, num_sessions,
            schedule_day_1, schedule_day_2,
            time_slot_1, time_slot_2,
            num_attended, num_excused,
            left_sessions,
            payment_paid, payment_left,
            created_at, account_type, num_of_students
        )

        return redirect(url_for('students'))

    return render_template('edit.html', item_type='student', item=student)


@app.route('/students/<int:student_id>/delete', methods=['POST'])
def delete_student_route(student_id):
    if delete_student(student_id):
        print('Student deleted successfully!', 'success')
    else:
        print('Error deleting student!', 'error')
    return redirect(url_for('students'))

# ----- Groups routes -----
@app.route('/groups')
def groups():
    search_term = request.args.get('search', '')
    if search_term:
        groups = search_group(search_term)
    else:
        groups = get_groups()
    return render_template('groups.html', groups=groups, search_term=search_term)

@app.route('/add_group', methods=['GET', 'POST'])
def add_group_route():
    if request.method == 'POST':
        group_name = request.form['group_name']
        group_id = request.form['group_id']
        num_students = request.form['num_students']
        student_id_1 = request.form.get('student_id_1', '')
        student_id_2 = request.form.get('student_id_2', '')
        student_id_3 = request.form.get('student_id_3', '')
        student_id_4 = request.form.get('student_id_4', '')
        student_id_5 = request.form.get('student_id_5', '')
        course_name = request.form['course_name']
        num_attended_session = int(request.form['num_attended_session'])
        left_sessions = 12 - num_attended_session
        schedule_day_1 = request.form['schedule_day_1']
        schedule_day_2 = request.form['schedule_day_2']
        time_slot_1 = request.form['time_slot_1']
        time_slot_2 = request.form['time_slot_2']

        result = add_group(group_name, group_id, num_students, student_id_1, student_id_2, student_id_3, student_id_4, student_id_5,
                           course_name, num_attended_session, left_sessions, schedule_day_1, schedule_day_2, time_slot_1, time_slot_2)
        if result:
            return redirect(url_for('groups'))
    
    return render_template('add.html', item_type='group', item=None)

@app.route('/groups/<int:group_id>/edit', methods=['GET', 'POST'])
def edit_group_route(group_id):
    group = get_group_by_id(group_id)
    
    if request.method == 'POST':
        group_name = request.form['group_name']
        group_id_form = request.form['group_id']
        num_students = request.form['num_students']
        student_id_1 = request.form.get('student_id_1', '')
        student_id_2 = request.form.get('student_id_2', '')
        student_id_3 = request.form.get('student_id_3', '')
        student_id_4 = request.form.get('student_id_4', '')
        student_id_5 = request.form.get('student_id_5', '')
        course_name = request.form['course_name']
        num_attended_session = int(request.form['num_attended_session'])
        left_sessions = 12 - num_attended_session
        schedule_day_1 = request.form['schedule_day_1']
        schedule_day_2 = request.form['schedule_day_2']
        time_slot_1 = request.form['time_slot_1']
        time_slot_2 = request.form['time_slot_2']

        update_group(group_id, group_name, group_id_form, num_students, student_id_1, student_id_2, 
                     student_id_3, student_id_4, student_id_5, course_name, num_attended_session, 
                     left_sessions, schedule_day_1, schedule_day_2, time_slot_1, time_slot_2)
        return redirect(url_for('groups'))
    
    return render_template('edit.html', item_type='group', item=group)

@app.route('/groups/<int:group_id>/delete', methods=['POST'])
def delete_group_route(group_id):
    if delete_group(group_id):
        print('Group deleted successfully!', 'success')
    else:
        print('Error deleting group!', 'error')
    return redirect(url_for('groups'))

@app.route('/courses')
def courses():
    search_term = request.args.get('search', '')
    if search_term:
        courses = search_course(search_term)
    else:
        courses = get_courses()
    return render_template('courses.html', courses=courses, search_term=search_term)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course_route():
    if request.method == 'POST':
        code = request.form['code']
        title = request.form['title']
        credit_hours = request.form['credit_hours']
        
        # Get all 12 lesson values (they can be empty if not filled)
        lessons = [request.form.get(f'lesson_{i}', '') for i in range(1, 13)]

        # Unpack the lessons list and pass to add_course
        add_course(code, title, credit_hours, *lessons)

        return redirect(url_for('courses'))
    
    return render_template('add.html', item_type='course', item=None)
@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    course = get_course_by_id(course_id)
    
    if request.method == 'POST':
        code = request.form['code']
        title = request.form['title']
        credit_hours = request.form['credit_hours']
        # Get all 12 lesson values (they can be empty if not filled)
        lessons = [request.form.get(f'lesson_{i}', '') for i in range(1, 13)]
        
        update_course(course_id, code, title, credit_hours, *lessons)
        return redirect(url_for('courses'))
    
    return render_template('edit.html', item_type='course', item=course)

@app.route('/delete_course/<int:course_id>')
def delete_course_route(course_id):
    delete_course(course_id)
    return redirect(url_for('courses'))

# Attendence
@app.route('/students/<int:student_id>/attendance')
def student_attendance(student_id):
    student = get_student_by_id(student_id)
    attendance_records = get_student_attendance(student_id)
    return render_template('attendance.html', 
                         student=student, 
                         attendance_records=attendance_records)

@app.route('/students/<int:student_id>/add_attendance', methods=['GET', 'POST'])
def add_attendance(student_id):
    if request.method == 'POST':
        status = request.form['status']
        feedback = request.form.get('feedback', '')
        rating = request.form.get('rating')
        
        # Add the attendance record
        add_attendance_record(student_id, status, feedback, rating)
        
        # Update the student's attended session count
        update_student_attended_sessions(student_id)
        
        # Get updated student data
        student = get_student_by_id(student_id)
        attended = student[12]  # num_attended_session
        left = student[13]      # left_sessions
        
        # Send email notification
        if student and student[4]:  # Check if email exists
            send_attendance_email(
                student_email=student[4],
                student_name=student[1],
                status=status,
                feedback=feedback,
                rating=rating,
                attended_sessions=attended,
                left_sessions=left
            )
        return redirect(url_for('student_attendance', student_id=student_id))
    student = get_student_by_id(student_id)
    return render_template('add_attendance.html', student=student)
@app.route('/attendance/<int:record_id>/edit', methods=['GET', 'POST'])
def edit_attendance(record_id):
    record = get_attendance_record(record_id)
    if not record:
        return "Attendance record not found", 404
    
    student = get_student_by_id(record[1])  # record[1] is student_id
    
    if request.method == 'POST':
        status = request.form['status']
        feedback = request.form.get('feedback', '')
        rating = request.form.get('rating')
        
        if update_attendance_record(record_id, status, feedback, rating):
            # Update the student's attended session count
            update_student_attended_sessions(student[0])
            return redirect(url_for('student_attendance', student_id=student[0]))
    
    return render_template('edit_attendance.html', 
                            student=student, 
                            record=record)
@app.route('/attendance/<int:record_id>/delete', methods=['POST'])
def delete_attendance(record_id):
    delete_attendance_record(record_id)
    return redirect(url_for('students'))

def send_attendance_email(student_email, student_name, status, feedback, rating, attended_sessions, left_sessions):
    try:
        # Arabic email content with emojis
        subject = "📝 تحديث الحضور في أكاديمية كادر"
        
        body = f"""
        السلام عليكم {student_name} 👋

        تم تسجيل حضورك اليوم في أكاديمية كادر:

        📅 التاريخ: {datetime.now().strftime('%Y-%m-%d')}
        🟢 الحالة: {status.upper()}
        
        📊 إحصائيات الحضور:
        ✅ عدد الحصص الحاضرة: {attended_sessions}
        ⏳ الحصص المتبقية: {left_sessions}
        
        {f"📝 ملاحظات المدرب: {feedback}" if feedback else "📝 لا توجد ملاحظات اليوم"}
        {f"⭐ تقييم الجلسة: {'★' * int(rating) if rating else 'غير متوفر'}" if rating else ""}

        🌟 استمر في التميز! نحن نقدر جهودك
        
        مع تحيات،
        فريق أكاديمية كادر
        """
        
        msg = Message(
            subject=subject,
            sender=app.config['MAIL_USERNAME'],
            recipients=[student_email],
            body=body
        )
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
if __name__ == '__main__':
    app.run(debug=True)