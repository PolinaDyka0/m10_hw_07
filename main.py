from sqlalchemy import func, desc, select, and_, text

from database.models import Teacher, Student, Discipline, Grade, Group
from database.db import session

bool_v = True

def select_1():
    """
    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    SELECT s.fullname, ROUND(AVG(g.grade), 2) as avg_grade
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY avg_grade DESC
    LIMIT 5;
    :return:
    """
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
             .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    # order_by(Grade.grade.desc())
    return result


def select_2():
    """
    SELECT d.name, s.fullname, ROUND(AVG(g.grade), 2) as avg_grade
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d ON d.id = g.discipline_id
    WHERE d.id = 5
    GROUP BY s.id
    ORDER BY avg_grade DESC
    LIMIT 1;
    :return:
    """
    result = session.query(
                        Discipline.name,
                        Student.fullname,
                        func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                    .select_from(Grade).join(Student).join(Discipline)\
                    .filter(Discipline.id == 5)\
                    .group_by(Student.id, Discipline.name).order_by(desc('avg_grade')).limit(1).first()
    return result

def select_3():
    """
    -- Знайти середній бал у групах з певного предмета.
    SELECT gr.name, d.name, ROUND(AVG(g.grade), 2) as avg_grade
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d ON d.id = g.discipline_id
    LEFT JOIN [groups] gr ON gr.id = s.group_id
    WHERE d.id = 1
    GROUP BY gr.id
    ORDER BY avg_grade DESC;
    """
    result = session.query(Group.name, Discipline.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Student, Student.group_id == Group.id) \
        .join(Grade, Grade.student_id == Student.id) \
        .join(Discipline, Discipline.id == Grade.discipline_id) \
        .filter(Discipline.id == 1) \
        .group_by(Group.id, Discipline.name) \
        .order_by(text('avg_grade DESC')) \
        .all()
    return result

def select_4():
    '''
    --Знайти середній бал на потоці (по всій таблиці оцінок).
    SELECT ROUND(AVG(grade),2) as avg_grade
    FROM grades;
    '''
    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')).first()
    return result.avg_grade

def select_5():
    '''
    --Знайти які курси читає певний викладач.
    SELECT disciplines.name AS discipline_name
    FROM disciplines
    INNER JOIN teachers ON disciplines.teacher_id = teachers.id
    WHERE teachers.fullname = 'Яків Баклан';
    '''
    teacher_name = input("Enter teacher's full name: ") or 'Edwin Hart'

    result = session.query(Discipline.name.label('discipline_name')) \
        .join(Teacher, Discipline.teacher_id == Teacher.id) \
        .filter(Teacher.fullname == teacher_name) \
        .all()
    return result

def select_6():
    """
    -- Знайти імена студентів у певній групі.
    SELECT students.fullname
    FROM students
    JOIN groups ON students.group_id = groups.id
    WHERE groups.name = 'ХП-31';
    """
    group_name = input("Enter group's name: ") or 'ВВ1'

    result = session.query(Student.fullname) \
        .join(Group, Student.group_id == Group.id) \
        .filter(Group.name == group_name) \
        .all()
    return result

def select_7():
    """
   --Знайти оцінки студентів у окремій групі з певного предмета.
    SELECT students.fullname, grades.grade
    FROM grades
    JOIN students ON students.id = grades.student_id
    JOIN groups ON students.group_id = groups.id
    JOIN disciplines ON grades.discipline_id = disciplines.id
    WHERE groups.name = 'ХП-31' AND disciplines.name = 'Актуарна математика';
    """
    group_name = input("Enter group's name: ") or 'ВВ1'
    discipline_name = input("Enter discipline's name: ") or "Хімія"

    result = session.query(Student.fullname, Grade.grade) \
        .join(Group, Student.group_id == Group.id) \
        .join(Grade, Grade.student_id == Student.id) \
        .join(Discipline, Grade.discipline_id == Discipline.id) \
        .filter(Group.name == group_name, Discipline.name == discipline_name) \
        .all()

    return result

def select_8():
    """
   --Знайти середній бал, який ставить певний викладач зі своїх предметів.
    SELECT teachers.fullname, ROUND(AVG(grades.grade), 2) as avg_grade
    FROM teachers
    INNER JOIN disciplines ON teachers.id = disciplines.teacher_id
    INNER JOIN grades ON disciplines.id = grades.discipline_id
    GROUP BY teachers.id
    HAVING teachers.fullname = 'Яків Баклан'
    """
    teacher_name = input("Enter teacher's full name: ") or 'Edwin Hart'

    result = session.query(Teacher.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Discipline, Teacher.id == Discipline.teacher_id) \
        .join(Grade, Grade.discipline_id == Discipline.id) \
        .group_by(Teacher.id) \
        .having(Teacher.fullname == teacher_name) \
        .all()
    return result

def select_9():
    """
    --Знайти список курсів, які відвідує студент.
    SELECT DISTINCT disciplines.name
    FROM grades
    JOIN students ON grades.student_id = students.id
    JOIN disciplines ON grades.discipline_id = disciplines.id
    WHERE students.fullname = 'Устим Височан';
    """
    student_name = input("Enter student's full name: ") or 'Gregory Thompson'

    result = session.query(Discipline.name) \
        .join(Grade, Grade.discipline_id == Discipline.id) \
        .join(Student, Grade.student_id == Student.id) \
        .filter(Student.fullname == student_name) \
        .distinct() \
        .all()
    return result

def select_10():
    """
    --Список курсів, які певному студенту читає певний викладач.
    SELECT disciplines.name
    FROM grades
    INNER JOIN students ON grades.student_id = students.id
    INNER JOIN disciplines ON grades.discipline_id = disciplines.id
    INNER JOIN teachers ON disciplines.teacher_id = teachers.id
    WHERE students.fullname = 'Устим Височан' AND teachers.fullname = 'Амалія Власюк'
    GROUP BY disciplines.name;
    """
    student_name = input("Enter student's full name: ") or 'Gregory Thompson'
    teacher_name = input("Enter teacher's full name: ") or 'Edwin Hart'

    result = session.query(Discipline.name) \
        .join(Grade, Grade.discipline_id == Discipline.id) \
        .join(Student, Student.id == Grade.student_id) \
        .join(Teacher, Teacher.id == Discipline.teacher_id) \
        .filter(Student.fullname == student_name) \
        .filter(Teacher.fullname == teacher_name) \
        .group_by(Discipline.name) \
        .all()
    return result

def select_11():
    """
    --Середній бал, який певний викладач ставить певному студентові.
    SELECT ROUND(AVG(grades.grade), 2) as avg_grade
    FROM grades
    JOIN students ON students.id = grades.student_id
    JOIN disciplines ON disciplines.id = grades.discipline_id
    JOIN teachers ON teachers.id = disciplines.teacher_id
    WHERE teachers.fullname = 'Азар Штепа' AND students.fullname = 'Устим Височан';
    """
    student_name = input("Enter student's full name: ") or 'Gregory Thompson'
    teacher_name = input("Enter teacher's full name: ") or 'Edwin Hart'

    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Student, Grade.student_id == Student.id) \
        .join(Discipline, Grade.discipline_id == Discipline.id) \
        .join(Teacher, Discipline.teacher_id == Teacher.id) \
        .filter(Teacher.fullname == teacher_name, Student.fullname == student_name) \
        .one()
    return result

def select_12():
    """
    -- Оцінки студентів у певній групі з певного предмета на останньому занятті.
    select s.id, s.fullname, g.grade, g.date_of
    from grades g
    join students s on s.id = g.student_id
    where g.discipline_id = 3 and s.group_id = 3 and g.date_of = (
        select max(date_of)
        from grades g2
        join students s2 on s2.id = g2.student_id
        where g2.discipline_id = 3 and s2.group_id = 3
    );
    :return:
    """
    subquery = (select(func.max(Grade.date_of)).join(Student).filter(and_(
                    Grade.discipline_id == 3, Student.group_id == 3
                )).scalar_subquery())

    result = session.query(Student.id, Student.fullname, Grade.grade, Grade.date_of)\
                    .select_from(Grade)\
                    .join(Student)\
                    .filter(and_(
                        Grade.discipline_id == 3, Student.group_id == 3, Grade.date_of == subquery
                    )).all()
    return result

def bye():
    global bool_v
    bool_v = False
    return 'See you later, alligator'

queries = {
        1: select_1,
        2: select_2,
        3: select_3,
        4: select_4,
        5: select_5,
        6: select_6,
        7: select_7,
        8: select_8,
        9: select_9,
        10: select_10,
        11: select_11,
        12: select_12,
        0: bye
    }

if __name__ == '__main__':

    while bool_v:
        query_number = int(input("Enter query number: "))
        result = queries[query_number]()
        print(result)

