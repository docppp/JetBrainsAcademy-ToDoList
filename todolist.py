from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return f'{self.task}. {self.deadline.day} {self.deadline.strftime("%b")}'


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

day_names = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

prompt = """1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
"""

user_choice = input(prompt)


while user_choice != "0":
    if user_choice == "1":  # Today's tasks
        today = datetime.today()
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        print(f'\nToday {today.day} {today.strftime("%b")}:')
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for row in rows:
                print(f'{row.id}. {row.task}')

    if user_choice == "2":  # Week's tasks
        for i in range(7):
            day = datetime.today() + timedelta(days=i)
            rows = session.query(Table).filter(Table.deadline == day.date()).all()
            print(f'\n{day_names[day.weekday()]} {day.day} {day.strftime("%b")}:')
            if len(rows) == 0:
                print("Nothing to do!")
            else:
                for row in rows:
                    print(f'{row.id}. {row.task}')

    if user_choice == "3":  # All tasks
        rows = session.query(Table).order_by(Table.deadline).all()
        print('\nAll tasks:')
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for i, row in enumerate(rows):
                print(f'{i}. {row}')

    if user_choice == "4":  # Missed tasks
        day = datetime.today()
        rows = session.query(Table).order_by(Table.deadline).filter(Table.deadline < day.date()).all()
        print('\nMissed tasks:')
        if len(rows) == 0:
            print("Nothing is missed!")
        else:
            for i, row in enumerate(rows):
                print(f'{i+1}. {row}')
            print("\n")

    if user_choice == "5":  # Add task
        new_task = input("Enter task\n")
        deadline = input("Enter deadline\n")
        new_row = Table(task=new_task, deadline=datetime.strptime(deadline, '%Y-%m-%d'))
        session.add(new_row)
        session.commit()
        print("The task has been added!\n")

    if user_choice == "6":  # Delete task
        rows = session.query(Table).order_by(Table.deadline).all()
        print('\nChoose the number of the task you want to delete:')
        if len(rows) == 0:
            print("Nothing to delete")
        else:
            for i, row in enumerate(rows):
                print(f'{i+1}. {row}')
            task_to_delete = int(input())
            session.delete(rows[task_to_delete - 1])
            session.commit()

    user_choice = input(prompt)
