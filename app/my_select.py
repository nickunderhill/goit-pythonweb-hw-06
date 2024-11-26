import logging
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from models import Student, Grade, Course, Teacher, Group

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1(session: Session):
    return (
        session.query(Student.name, func.avg(Grade.value).label("avg_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .limit(5)
        .all()
    )


# 2. Знайти студента із найвищим середнім балом з певного предмета.
def select_2(session: Session, course_id: int):
    return (
        session.query(Student.name, func.avg(Grade.value).label("avg_grade"))
        .join(Grade)
        .filter(Grade.course_id == course_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .first()
    )


# 3. Знайти середній бал у групах з певного предмета.
def select_3(session: Session, course_id: int):
    return (
        session.query(Group.name, func.avg(Grade.value).label("avg_grade"))
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.course_id == course_id)
        .group_by(Group.id)
        .all()
    )


# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4(session: Session):
    return session.query(func.avg(Grade.value).label("avg_grade")).scalar()


# 5. Знайти які курси читає певний викладач.
def select_5(session: Session, teacher_id: int):
    return session.query(Course.name).filter(Course.teacher_id == teacher_id).all()


# 6. Знайти список студентів у певній групі.
def select_6(session: Session, group_id: int):
    return session.query(Student.name).filter(Student.group_id == group_id).all()


# 7. Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(session: Session, group_id: int, course_id: int):
    return (
        session.query(Student.name, Grade.value)
        .join(Grade, Grade.student_id == Student.id)
        .filter(Student.group_id == group_id, Grade.course_id == course_id)
        .all()
    )


# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(session: Session, teacher_id: int):
    return (
        session.query(func.avg(Grade.value).label("avg_grade"))
        .join(Course, Course.id == Grade.course_id)
        .filter(Course.teacher_id == teacher_id)
        .scalar()
    )


# 9. Знайти список курсів, які відвідує певний студент.
def select_9(session: Session, student_id: int):
    return (
        session.query(Course.name)
        .join(Grade, Grade.course_id == Course.id)
        .filter(Grade.student_id == student_id)
        .all()
    )


# 10. Список курсів, які певному студенту читає певний викладач.
def select_10(session: Session, student_id: int, teacher_id: int):
    return (
        session.query(Course.name)
        .join(Grade)
        .join(Student)
        .join(Teacher)
        .filter(Grade.student_id == student_id, Course.teacher_id == teacher_id)
        .group_by(Course.id)
        .all()
    )


def run_queries():
    from connect import Session

    with Session() as session:
        logger.info(
            "1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів."
        )
        logger.info(select_1(session))

        logger.info("2. Знайти студента із найвищим середнім балом з певного предмета.")
        logger.info(select_2(session, 1))

        logger.info("3. Знайти середній бал у групах з певного предмета.")
        logger.info(select_3(session, 1))

        logger.info("4. Знайти середній бал на потоці (по всій таблиці оцінок).")
        logger.info(select_4(session))

        logger.info("5. Знайти які курси читає певний викладач.")
        logger.info(select_5(session, 1))

        logger.info("6. Знайти список студентів у певній групі.")
        logger.info(select_6(session, 1))

        logger.info("7. Знайти оцінки студентів у окремій групі з певного предмета.")
        logger.info(select_7(session, 1, 1))

        logger.info(
            "8. Знайти середній бал, який ставить певний викладач зі своїх предметів."
        )
        logger.info(select_8(session, 1))

        logger.info("9. Знайти список курсів, які відвідує певний студент.")
        logger.info(select_9(session, 1))

        logger.info("10. Список курсів, які певному студенту читає певний викладач.")
        logger.info(select_10(session, 1, 1))


if __name__ == "__main__":
    run_queries()
