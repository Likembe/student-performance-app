import sqlite3

def create_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

def execute_sql(conn, sql, data=None):
    try:
        c = conn.cursor()
        if data:
            # If data is a list of tuples, we need to execute many.
            if isinstance(data[0], tuple):
                c.executemany(sql, data)
            else:
                c.execute(sql, data)
        else:
            c.execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def query_db(conn, query, params=None):
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def print_query_results(results, headers):
    for row in results:
        print(", ".join(f"{header}: {col}" for header, col in zip(headers, row)))

def main():
    database = 'student_performance.db'
    
    sql_create_tables = [
        '''CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            student_name TEXT NOT NULL,
            student_email TEXT UNIQUE NOT NULL
        );''',
        '''CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY,
            course_name TEXT NOT NULL,
            course_teacher TEXT NOT NULL
        );''',
        '''CREATE TABLE IF NOT EXISTS grades (
            student_id INTEGER,
            course_id INTEGER,
            grade INTEGER NOT NULL,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students (student_id),
            FOREIGN KEY (course_id) REFERENCES courses (course_id)
        );'''
    ]
    
    conn = create_connection(database)
    if conn is not None:
        for sql in sql_create_tables:
            execute_sql(conn, sql)

        
        data_entries = [
            ('students', [
                (1,'Ralph Bunche', 'ralph.bunche@moringa.com'),
                (2, 'Alpha Likembe', 'alpha.likembe@moringa.com'),
                (3, 'Jet Lee', 'jet.lee@moringa.com')
            ]),  
            ('courses', [
                 (1, 'Mathematics', 'Mr. White'),
                 (2, 'English', 'Mr. Moh'),
                 (3, 'Sciences', 'Ms. Trina')
            ]), 
            ('grades', [
                (1, 1, 70),
                (1, 2, 60),
                (1, 3, 80),
                (2, 1, 65),
                (2, 2, 80),
                (2, 3, 79),
                (3, 1, 90),
                (3, 2, 50),
                (3, 3, 80)
            ])  
        ]


        for table, data in data_entries:
            # Use len(data[0]) to create the right number of placeholders
            placeholders = ", ".join("?" * len(data[0]))
            insert_sql = f'INSERT OR REPLACE INTO {table} VALUES ({placeholders})'
            execute_sql(conn, insert_sql, data)

        conn.close()
    else:
        print("Error! cannot create the database connection.")

def calculate_letter_grade(average):
    if average >= 70:
        return 'A'
    elif average >= 60:
        return 'B'
    elif average >= 50:
        return 'C'
    elif average >= 40:
        return 'D'
    else:
        return 'E'



def get_student_performance(db_file, student_name=None):
    conn = create_connection(db_file)
    if conn is not None:
        # Fetch individual course grades and average grade for each student
        student_grades_sql = '''
            SELECT students.student_name, courses.course_name, grades.grade
            FROM grades
            INNER JOIN students ON students.student_id = grades.student_id
            INNER JOIN courses ON courses.course_id = grades.course_id
            {where_clause}
            ORDER BY students.student_name, courses.course_name;
        '''
        average_grades_sql = '''
            SELECT students.student_name, AVG(grades.grade) as average_grade
            FROM grades
            INNER JOIN students ON students.student_id = grades.student_id
            {where_clause}
            GROUP BY students.student_id
            ORDER BY students.student_name;
        '''
        
        # Apply WHERE clause if a specific student name is provided
        where_clause = "WHERE students.student_name = ?" if student_name else ""
        student_grades_sql = student_grades_sql.format(where_clause=where_clause)
        average_grades_sql = average_grades_sql.format(where_clause=where_clause)
        
        params = (student_name,) if student_name else None
        individual_grades = query_db(conn, student_grades_sql, params)
        average_grades = query_db(conn, average_grades_sql, params)
        
        # Print individual grades
        if individual_grades:
            print("Individual Course Grades:")
            for student, course, grade in individual_grades:
                grade_int = int(grade) if isinstance(grade, str) else grade
                print(f"Student: {student}, Course: {course}, Grade: {grade} ({calculate_letter_grade(grade_int)})")

        # Print average performance
        if average_grades:
            print("\nStudent Average Performance:")
            for student, avg_grade in average_grades:
                avg_grade_float = float(avg_grade)
                print(f"Student: {student}, Average Grade: {avg_grade:.2f} ({calculate_letter_grade(avg_grade_float)})")


        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
    #print performance for all the students
    get_student_performance('student_performance.db')

    #print performance for a specific student
    get_student_performance('student_performance.db', 'Alpha Likembe')


