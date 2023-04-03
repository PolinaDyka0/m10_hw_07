import argparse
from database.models import Teacher, Student, Group, Discipline, Grade
from database.db import session


def list_records(model, id_field_name, name_field_name, group_field_name=None, teacher_field_name=None):
    records = session.query(model).all()
    for record in records:
        if group_field_name:
            if group_field_name == 'group_id':
                group_name = getattr(record, group_field_name)
            else:
                group_name = getattr(getattr(record, group_field_name), 'name')
            print(f'ID={getattr(record, id_field_name)}, Full name="{getattr(record, name_field_name)}", Group="{group_name}"')
        elif teacher_field_name:
            teacher_id = getattr(record, teacher_field_name)
            discipline_id = getattr(record, id_field_name)
            print(f'ID={discipline_id}, Name="{getattr(record, name_field_name)}", Teacher ID={teacher_id}')
        else:
            print(f'ID={getattr(record, id_field_name)}, Full name="{getattr(record, name_field_name)}".')



def create_record(model, **kwargs):
    record = model(**kwargs)
    session.add(record)
    session.commit()
    print(f'{model.__name__} with ID={record.id} was successfully created.')

def remove_record(model, id):
    record = session.query(model).filter_by(id=id).first()
    if record is None:
        print(f'{model.__name__} with ID={id} was not found.')
    else:
        session.delete(record)
        session.commit()
        print(f'{model.__name__} with ID={id} was successfully removed.')

def update_record(model, id, new_name=None, newgroup_id=None, newteacher_id=None):
    record = session.query(model).filter_by(id=id).first()
    if record is None:
        print(f'{model.__name__} with ID={id} was not found.')
    else:
        if new_name is not None:
            record.name = new_name
        if newgroup_id is not None:
            record.group_id = newgroup_id
        if newteacher_id is not None:
            record.teacher_id = newteacher_id
        session.commit()
        print(f'{model.__name__} with ID={id} was successfully updated.')

def list_grades():
    grades = session.query(Grade).all()
    for grade in grades:
        print(f'ID={grade.id}, Grade={grade.grade}, Date={grade.date_of}, Student ID={grade.student_id}, Discipline ID={grade.discipline_id}')


def create_grade(grade, date_of, student_id, discipline_id):
    record = Grade(grade=grade, date_of=date_of, student_id=student_id, discipline_id=discipline_id)
    session.add(record)
    session.commit()
    print(f'Grade with ID={record.id} was successfully created.')


def update_grade(id, new_grade=None, new_date_of=None, new_student_id=None, new_discipline_id=None):
    record = session.query(Grade).filter_by(id=id).first()
    if record is None:
        print(f'Grade with ID={id} was not found.')
    else:
        if new_grade is not None:
            record.grade = new_grade
        if new_date_of is not None:
            record.date_of = new_date_of
        if new_student_id is not None:
            record.student_id = new_student_id
        if new_discipline_id is not None:
            record.discipline_id = new_discipline_id
        session.commit()
        print(f'Grade with ID={id} was successfully updated.')


def remove_grade(id):
    record = session.query(Grade).filter_by(id=id).first()
    if record is None:
        print(f'Grade with ID={id} was not found.')
    else:
        session.delete(record)
        session.commit()
        print(f'Grade with ID={id} was successfully removed.')






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI program for CRUD operations.')
    parser.add_argument('--action', '-a', required=True, choices=['create', 'list', 'update', 'remove'],
                        help='Action to perform with table.')
    parser.add_argument('--model', '-m', required=True, choices=['Teacher', 'Student', 'Group', 'Discipline', 'Grade'],
                        help='Model to perform operation with.')

    # add arguments for create
    parser.add_argument('--name', '-n', help='Full name (used for create operation).')
    parser.add_argument('--group_id', '-g', type=int, help='Group ID (used for create operation).')
    parser.add_argument('--teacher_id', '-t', type=int, help='Teacher ID (used for create operation).')


    # add arguments for update
    parser.add_argument('--id', '-i', type=int, help='ID  (used for update and remove operation).')
    parser.add_argument('--newname', '-nn', help='New name (used for update operation).')
    parser.add_argument('--newgroup_id', '-ng', type=int, help='Group ID (used for update operation).')
    parser.add_argument('--newteacher_id', '-nt', type=int, help='Teacher ID (used for update operation).')

    # arguments just for grades
    parser.add_argument('--grade', '-gr', type=int, help='Grade (used for create operation).')
    parser.add_argument('--date', '-d', help='Date (used for create operation).')
    parser.add_argument('--student_id', '-s', type=int, help='Student ID (used for create operation).')
    parser.add_argument('--discipline_id', '-di', type=int, help='Discipline ID (used for create operation).')

    parser.add_argument('--new_grade', '-ngr', type=float, help='New grade (used for update operation).')
    parser.add_argument('--new_date_of', '-nd', help='New date of grade (used for update operation).')
    parser.add_argument('--new_student_id', '-nsi', help='New student id of grade (used for update operation).')
    parser.add_argument('--new_discipline_id', '-ndi', help='New discipline id of grade (used for update operation).')

    args = parser.parse_args()

    if args.action == 'create':
        if args.model == 'Teacher':
            create_record(Teacher, fullname=args.name)
        elif args.model == 'Student':
            create_record(Student, fullname=args.name, group_id=args.group_id)
        elif args.model == 'Group':
            create_record(Group, name=args.name)
        elif args.model == 'Discipline':
            create_record(Discipline, name=args.name, teacher_id=args.teacher_id)
        elif args.model == 'Grade':
            create_grade(args.grade, args.date, args.student_id, args.discipline_id)

    elif args.action == 'list':
        if args.model == 'Teacher':
            list_records(Teacher, 'id', 'fullname')
        elif args.model == 'Student':
            list_records(Student, 'id', 'fullname', 'group_id')
        elif args.model == 'Group':
            list_records(Group, 'id', 'name')
        elif args.model == 'Discipline':
            list_records(Discipline, 'id', 'name', teacher_field_name='teacher_id')
        elif args.model == 'Grade':
            list_grades()


    elif args.action == 'update':
        if args.model == 'Teacher':
            update_record(Teacher, args.id, new_name=args.newname)
        elif args.model == 'Student':
            update_record(Student, args.id, new_name=args.newname, newgroup_id=args.newgroup_id)
        elif args.model == 'Group':
            update_record(Group, args.id, new_name=args.newname)
        elif args.model == 'Discipline':
            update_record(Discipline, args.id, new_name=args.newname, newteacher_id=args.newteacher_id)
        elif args.model == 'Grade':
            update_grade(args.id, new_grade=args.new_grade, new_date_of=args.new_date_of, new_student_id=args.new_student_id, new_discipline_id=args.new_discipline_id)

    elif args.action == 'remove':
        if args.model == 'Teacher':
            remove_record(Teacher, args.id)
        elif args.model == 'Student':
            remove_record(Student, args.id)
        elif args.model == 'Group':
            remove_record(Group, args.id)
        elif args.model == 'Discipline':
            remove_record(Discipline, args.id)
        elif args.model == 'Grade':
            remove_grade(args.id)


