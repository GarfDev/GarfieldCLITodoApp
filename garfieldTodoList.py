from colorama import init, Fore, Back, Style

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import threading, time, re
from tabulate import tabulate
from datetime import datetime
import os

###Functional_components

engine = create_engine('sqlite:///garfieldTodoList.sqlite3', echo=True)
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
screenLock = threading.Lock()
init(convert=True)


### Database_classes

class todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    userid = Column(String)
    projectid = Column(String)
    assignTo = Column(Integer)
    body = Column(String)
    timestamp = Column(String)
    status = Column(String)


class project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
    ownerid = Column(String)


class tempProjectToUser(Base):
    __tablename__ = 'tempProjectToUser'

    id = Column(Integer, primary_key=True)
    projectid = Column(Integer)
    memberid = Column(Integer)


class tempProjectToTodo(Base):
    __tablename__ = 'assignProjectTodoToUser'

    id = Column(Integer, primary_key=True)
    todoId = Column(Integer)
    memberId = Column(Integer)
    projectId = Column(Integer)


class user(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    createdAt = Column(String)


###Functions

class messages:  # Messages_handle
    def __init__(self, message):
        self.message = message

    def alert(message):
        screenLock.acquire()
        print(Fore.LIGHTMAGENTA_EX + Style.DIM + "[>] " + Style.RESET_ALL + message + Style.RESET_ALL)
        screenLock.release()

    def error(message):
        screenLock.acquire()
        print(Fore.RED + Style.DIM + "[!] " + Style.RESET_ALL + message + Style.RESET_ALL)
        screenLock.release()

    def passed(message):
        screenLock.acquire()
        print(Fore.LIGHTGREEN_EX + Style.DIM + "[//] " + Style.RESET_ALL + message + Style.RESET_ALL)
        screenLock.release()


def cleanScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def showSomeHelp():
    commands = [["-h, --help", "show this message"],
                ['-list, --list "custom status" "custom_id"', "show Todo list."],
                ['-add, --add "TODO CONTENT" "PROJECT ID"', 'add Todo to Todo list.'],
                ['-del, --del "Todo ID"', 'remove todo from todo list'],
                ['-mod, --mod "Todo ID" "status"', "modify todo status"],
                ['-create, --create "Project Name"', "create a new project"],
                ['-assignTo, --assignTo "Todo ID" "USER ID"', "assign a Todo to a user"],
                ['-userList, --userList', 'See current user list'],
                ["-projectList, --projectList", "See current Project list"],
                ['-assignToProject, --assignToProject "USER ID" "PROJECT ID"', "Add a user to project"],
                ["-who_to_fire, --who_to_fire", "Show a list of lazy users!"]]
    print(tabulate(commands, tablefmt="rst"))


def getUsernameFromID(id):
    result = session.query(user).filter(user.id == id).first()
    if result:
        return result.username
    else:
        return None


def getProjectFromID(id):
    result = session.query(project).filter(project.id == id).first()
    if result:
        return result.name
    else:
        return None


def login(username):
    global currentUserId, currentUsername
    result = session.query(user). \
        filter(user.username == username)
    if result.count() == 0:
        messages.alert("Seem you're new here, let's create your account!")
        inputEmail = input("Please tell me your email: ")
        newUser = user(username=username, email=inputEmail, createdAt=int(time.time()))
        session.add(newUser)
        session.commit()
        messages.passed("Your account have created, have fun with my program.")
        updated_result = session.query(user). \
            filter(user.username == username).first()
        currentUserId, currentUsername = updated_result.id, updated_result.username
        return False
    elif result.count() >= 0:
        messages.alert(f"Welcome back, {result.first().username}!")
        currentUserId, currentUsername = result.first().id, result.first().username
        return True


def displayTodoList(status=None, id=None):
    tableContent = []
    if status and id:
        result = session.query(todo). \
            join(user, user.id == currentUserId). \
            filter(todo.status == status, todo.id == id). \
            filter(todo.assignTo == currentUserId). \
            filter(todo.userid == currentUserId)
    elif status and not id:
        result = session.query(todo). \
            join(user, user.id == currentUserId). \
            filter(todo.status == status). \
            filter(todo.assignTo == currentUserId). \
            filter(todo.userid == currentUserId)
    elif id and not status:
        result = session.query(todo). \
            join(user, user.id == currentUserId). \
            filter(todo.id == id, todo)
    else:
        result = session.query(todo). \
            filter(or_(todo.userid == currentUserId, todo.assignTo == currentUserId))
    headers = ["ID", "PROJECT", "CONTENT", "OWNER", "ASSIGN TO", "TIMESTAMP", "STATUS"]
    if result.count() > 0:
        for row in result.all():
            tableContent.append(
                [row.id, getProjectFromID(row.projectid), row.body, getUsernameFromID(row.userid),
                 getUsernameFromID(row.assignTo), row.timestamp,
                 row.status])
        print(tabulate(tableContent, headers=headers))
    else:
        messages.error("There notthing to show, if you belived this is an error, please contact Garfield#7189.")


def addTodoList(body, project=None):
    try:
        new_todo = todo(userid=currentUserId, projectid=project, body=body, timestamp=int(time.time()), status="DOING")
        session.add(new_todo)
        session.commit()
    except:
        messages.error("Error while add your todo!")
        return False
    else:
        displayTodoList()
        return True


def delTodoList(id):
    todo_to_del = session.query(todo).filter(todo.id == id).first()
    session.delete(todo_to_del)
    session.commit()
    displayTodoList()


def changeTodoStatus(id, status="DOING"):
    try:
        result = session.query(todo).filter(todo.id == id).first()
        result.status = status
        session.commit()
    except:
        messages.error("Error while modifying your todo!")
        return False
    else:
        displayTodoList()
        return True


def createProject(name):
    try:
        new_project = project(name=name, ownerid=currentUserId, status="WORKING ON")
        session.add(new_project)
        session.commit()
    except:
        return False
    else:
        messages.passed("Successful on create your Project")
        return True


def assignProjectToUser(todoID, userID):
    result = session.query(todo).filter(todo.id == todoID).first()
    if result.userid == currentUserId:
        result.assignTo = userID
        session.commit()
    else:
        messages.error("You're not own this Todo to assign it to anyone")


def createNewUser(name, email):
    if currentUsername == "Garfield":
        user(username=name, email=email, createdAt=int(time.time()))
        session.add(user)
        session.commit()
    else:
        messages.error("You dont have permmision to create new user")


def seeUserList():
    userList = []
    result = session.query(user).all()
    headers = ["ID", "USERNAME", "EMAIL", "CREATED AT"]
    for row in result:
        userList.append([row.id, row.username, row.email, row.createdAt])
    print(tabulate(userList, headers=headers))


def seeProjectList():
    projectList = []
    result = session.query(project).all()
    headers = ["ID", "PROJECT", "STATUS", "OWNER"]
    for row in result:
        projectList.append([row.id, row.name, row.status, getUsernameFromID(row.ownerid)])
    print(tabulate(projectList, headers=headers))


def addMemberToProject(userid, projectid):
    new_link = tempProjectToUser(projectid=projectid, memberid=userid)
    session.add(new_link)


def ProjectSummary():
    project_result = session.query(project).filter(project.ownerid == currentUserId)
    if project_result.count() < 1:
        messages.alert("You're currently not own any project")
    else:
        memberList = []
        member_result = session.query(tempProjectToUser).filter(
            tempProjectToUser.projectid == project_result.first().id)
        for row in member_result:
            memberList.append([getUsernameFromID(row.memberid)])
            print(f"Project name: {project_result.first().name}")
        print(tabulate(memberList, headers=["MEMBER"]))


def who_to_fire():
    fire_list = []
    my_query = """SELECT username FROM user
                INNER JOIN todo ON todo.userid == user.id
                WHERE todo.userid != user.id
                GROUP BY username"""
    results = connection.execute(my_query).fetchall()
    if len(results) > 0:
        for row in results:
            fire_list.append(row[0])
        print(tabulate(fire_list), headers=["LAZY USER"])
    else:
        messages.error("Sorry but there no one to fire this time..")


### Default_system_variable

currentUserId, currentUsername = None, None
programEnded = False

### MainSystem
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print(Fore.LIGHTYELLOW_EX + """
         ██████╗  █████╗ ██████╗ ███████╗██╗███████╗██╗     ██████╗ 
        ██╔════╝ ██╔══██╗██╔══██╗██╔════╝██║██╔════╝██║     ██╔══██╗
        ██║  ███╗███████║██████╔╝█████╗  ██║█████╗  ██║     ██║  ██║
        ██║   ██║██╔══██║██╔══██╗██╔══╝  ██║██╔══╝  ██║     ██║  ██║
        ╚██████╔╝██║  ██║██║  ██║██║     ██║███████╗███████╗██████╔╝
         ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝╚═════╝ 
                  \\\  WORLD GREATEST CONSOLE TODO APP  // 
                """ + Style.RESET_ALL)

while not currentUserId:  # While_user_not_logged_in
    messages.alert("Please input your username:")
    inputUsername = input(" > ")
    login(inputUsername)

displayTodoList()

while not programEnded:  # While_program_is_running
    try:
        command = input(" > ")
        if "-list" in command:
            content = re.findall('"(.*?)"', command)
            if len(content) == 2:
                displayTodoList(status=content[0], id=content[1])
            elif len(content) == 1:
                if content[0].isdigit():
                    print("I was in digit")
                    displayTodoList(id=content[0])
                else:
                    print("I was in Not digit")
                    displayTodoList(status=content[0])
            else:
                displayTodoList()
        elif "-help" in command:
            showSomeHelp()
        elif "-add" in command:
            content = re.findall('"(.*?)"', command)
            if len(content) == 2:
                addTodoList(content[0], content[1])
            else:
                addTodoList(content[0])
        elif "-del" in command:
            content = re.findall('"(.*?)"', command)
            if len(content) == 1:
                delTodoList(content[0])
        elif "-mod" in command:
            content = re.findall('"(.*?)"', command)
            if len(content) == 2:
                changeTodoStatus(content[0], content[1])
        elif "-create" in command:
            content = re.findall('"(.*?)"', command)
            if len(content) == 1:
                createProject(content[0])
        elif "-assignTo" in command:
            content = re.findall('"(.*?)"', command)
            if len(content) == 2:
                createProject(content[0], content[1])
        elif "-userList" in command:
            seeUserList()
        elif "-projectList" in command:
            seeProjectList()
        elif "-assignToProject" in command:
            content = re.findall('"(.*?)"', command)
            if len(content) == 2:
                addMemberToProject(content[0], content[1])
        elif "-projectSummary" in command:
            ProjectSummary()
        elif "-who_to_fire" in command:
            who_to_fire()
        else:
            messages.alert("Please correct input command, press '-help' to see full list of command")
    except Exception as Error:
        messages.error("Something wrong while progressing your command")
        print(Error)
        continue
