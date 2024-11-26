from faker import Faker
from sqlalchemy.orm import Session
from models import Student, Group, Teacher, Course, Grade
from connect import engine

fake = Faker()


def seed_data():
    with Session(engine) as session:
        # Groups
        groups = [Group(name=fake.word()) for _ in range(3)]
        session.add_all(groups)

        # Teachers
        teachers = [Teacher(name=fake.name()) for _ in range(5)]
        session.add_all(teachers)

        # Courses
        courses = [
            Course(name=fake.word(), teacher=teachers[i % len(teachers)])
            for i in range(8)
        ]
        session.add_all(courses)

        # Students
        students = [
            Student(name=fake.name(), group=groups[i % len(groups)]) for i in range(50)
        ]
        session.add_all(students)

        # Grades
        for student in students:
            for course in courses:
                session.add(
                    Grade(
                        value=fake.random.randint(60, 100),
                        student=student,
                        course=course,
                        date_received=fake.date_time_this_year(),
                    )
                )

        session.commit()


if __name__ == "__main__":
    seed_data()
