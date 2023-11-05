from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True)
    student_name = Column(String, nullable=False)
    student_email = Column(String, nullable=False, unique=True)
    grades = relationship('Grade', back_populates='student')

    def __repr__(self):
        return f"<Student(name={self.student_name}, email={self.student_email})>"

class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True)
    course_name = Column(String, nullable=False)
    course_teacher = Column(String, nullable=False)
    grades = relationship('Grade', back_populates='course')

    def __repr__(self):
        return f"<Course(name={self.course_name}, teacher={self.course_teacher})>"

class Grade(Base):
    __tablename__ = 'grades'

    student_id = Column(Integer, ForeignKey('students.student_id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'), primary_key=True)
    grade = Column(Integer, nullable=False)
    student = relationship('Student', back_populates='grades')
    course = relationship('Course', back_populates='grades')

    def get_letter_grade(self):
        if self.grade is None:
            print("Grade is None")  
            return 'E'
        
        if self.grade >= 70:
            return 'A'
        elif 60 <= self.grade < 70:
            return 'B'
        elif 50 <= self.grade < 60:
            return 'C'
        elif 40 <= self.grade < 50:
            return 'D'
        else:
            return 'E'

    def __repr__(self):
        return f"<Grade(student_id={self.student_id}, course_id={self.course_id}, grade={self.grade}, letter_grade={self.get_letter_grade()})>"

# create an engine that stores data in the local directory's school_performance.db file.
engine = create_engine('sqlite:///student_performance.db')

# create all tables in the engine
Base.metadata.create_all(engine)

# create a session
Session = sessionmaker(bind=engine)
session = Session()

def add_or_update(model, session, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        # This is an update since the instance already exists
        if defaults:
            for key, value in defaults.items():
                setattr(instance, key, value)
    else:
        # This is an insert since the instance does not exist
        params = dict(kwargs)
        if defaults:
            params.update(defaults)
        instance = model(**params)
        session.add(instance)
    # Commit outside the if/else block to apply either the update or the insert.
    session.commit()
    return instance

# Function to add a grade to a student in a specific course
def add_grade(student_email, course_name, grade_score):
    # Query the student and course by name/email
    try:
        grade_score = int(grade_score)
    except ValueError:
        print("Grade score must be an integer.")
        return
    
    #Query by email
    student = session.query(Student).filter_by(student_email=student_email).first()
    #Query by name
    course = session.query(Course).filter_by(course_name=course_name).first()

    if student and course:
        grade_info = {
            'student_id': student.student_id, 
            'course_id': course.course_id
        }
        # Use a dictionary for the defaults parameter
        defaults = {'grade': grade_score}
        add_or_update(Grade, session, defaults=defaults, **grade_info)

def assign_random_grades(session):
    students = session.query(Student).all()
    courses = session.query(Course).all()
    for student in students:
        for course in courses:
            # Generate a random grade between 0 and 100
            random_grade = random.randint(0, 100)
            # Here, make sure that add_grade is defined at this point
            add_grade(student.student_email, course.course_name, random_grade)

assign_random_grades(session)


def print_student_performance(session):
    students = session.query(Student).all()
    for student in students:
        print(f"Performance for {student.student_name} ({student.student_email}):")
        for grade in student.grades:
            course = session.query(Course).filter_by(course_id=grade.course_id).first()
            print(f"  {course.course_name}: {grade.grade} ({grade.get_letter_grade()})")
        print("")  # Blank line for readability between students

    
# Adding multiple new students using a list of dictionaries
new_students = [    
    {'student_name': 'Ralph Bunche', 'student_email': 'ralph.bunche@moringa.com'},
    {'student_name': 'Alpha Likembe', 'student_email': 'alpha.likembe@moringa.com'},
    {'student_name': 'Jet Lee', 'student_email': 'jet.lee@moringa.com'},
    {'student_name': 'John Doe', 'student_email': 'john.doe@moringa.com'},
    {'student_name': 'Emily Rose', 'student_email': 'emily.rose@moringa.com'},
]

# Adding multiple new courses using a list of tuples
# Each tuple contains (course_name, course_teacher)
new_courses = [
    ('Mathematics', 'Mr. White'),
    ('English', 'Mr. Moh'),
    ('Sciences', 'Ms. Trina'),
    ('Biology', 'Dr. Watson'),
    ('History', 'Mr. Clark'),
    # Add more courses as needed
]

# Adding new teachers and courses to the database
for course_name, course_teacher in new_courses:
    course_info = {'course_name': course_name, 'course_teacher': course_teacher}
    add_or_update(Course, session, **course_info)

    
# Add the new students to the database
for student in new_students:
    add_or_update(Student, session, **student)

# Example of adding a grade for a student to a course
# Assuming the student and course already added and the session is created
add_grade('john.doe@moringa.com', 'Biology', 90)

# Function to print all students
def print_all_students(session):
    students = session.query(Student).all()  # Query all students from the database
    for student in students:
        print(student)  # Utilizing the __repr__ method of the Student class for printing

# Function to print all courses
def print_all_courses(session):
    courses = session.query(Course).all()  # Query all courses from the database
    for course in courses:
        print(course)  # Utilizing the __repr__ method of the Course class for printing

# Now call the functions to print the students and courses
print("All Students:")
print_all_students(session)

print("\nAll Courses:")
print_all_courses(session)

#Function to print students & their grades
def print_students_grades(session):
    grades = session.query(Grade).all()  # Query all grades from the database
    for grade in grades:
        try:
            student = grade.student
            course = grade.course
            print(f"{student.student_name} received a grade of {grade.get_letter_grade()} in {course.course_name}")
        except Exception as e:  # Catching the exception and printing it out
            print(f"An error occurred: {e}")

print_student_performance(session)
