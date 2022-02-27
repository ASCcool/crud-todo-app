from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import Base, engine, Users, engine1
from sqlalchemy.orm import Session, sessionmaker
import models
import schemas
import uvicorn
import datetime

# Create the database
Base.metadata.create_all(engine)
Users.metadata.create_all(engine1)

# Initialize app
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):

    session = Session(bind=engine1, expire_on_commit=False)

    print("Token",token)
    user = session.query(models.User).filter_by(username=token).first()
    session.close()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    session = Session(bind=engine1, expire_on_commit=False)
    user = session.query(models.User).filter_by(username=form_data.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    if not form_data.password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/")
def root():
    return "TO-DO APP!!"

@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User):

    # create a new database session
    session = Session(bind=engine1, expire_on_commit=False)

    # create an instance of the User database model
    userdb = models.User(username=user.username, password=user.password, email=user.email, full_name=user.full_name)

    # add it to the session and commit it
    session.add(userdb)
    session.commit()

    # grab the id given to the object from the database
    id = userdb.id

    # close the session
    session.close()

    # return the id
    return f"created user with id {id}"

@app.get("/users")
def read_users_list():
    # create a new database session
    session = Session(bind=engine1, expire_on_commit=False)

    # get all todo items
    users_list = session.query(models.User).all()

    # close the session
    session.close()

    return users_list

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDo):

    session = Session(bind=engine, expire_on_commit=False)

    tododb = models.ToDo(task = todo.task, due_date = todo.due_date, is_completed = todo.is_completed, assigned_to = todo.assigned_to, group_name = todo.group_name)

    session.add(tododb)
    session.commit()

    id = tododb.id

    session.close()

    return f"created todo item with id {id}"

@app.get("/todo/{id}")
def read_todo(id: int):

    session = Session(bind=engine, expire_on_commit=False)

    todo = session.query(models.ToDo).get(id)

    session.close()

    # Check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo

@app.put("/todo/{id}")
def update_todo(id: int, task: str, due_date: datetime.date, is_completed: str, assigned_to: str):

    session = Session(bind=engine, expire_on_commit=False)

    todo = session.query(models.ToDo).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if todo:
        todo.task = task
        todo.due_date = due_date
        todo.is_completed = is_completed
        todo.assigned_to = assigned_to
        session.commit()

    session.close()

    # Check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo

@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):

    session = Session(bind=engine, expire_on_commit=False)

    todo = session.query(models.ToDo).get(id)

    # If todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return None

@app.get("/todos")
def read_todo_list():

    session = Session(bind=engine, expire_on_commit=False)

    todo_list = session.query(models.ToDo).all()

    session.close()

    return todo_list

@app.put("/marktodogroup/{group_name}", status_code=status.HTTP_201_CREATED)
def create_group(group_name: str, user = Depends(get_current_user)):

    session = Session(bind=engine, expire_on_commit=False)
    todo_group_list = session.query(models.ToDo).filter_by(group_name=group_name).all()

    if todo_group_list:
        session.query(models.ToDo).filter_by(group_name=group_name).update({"is_completed": "Yes"})
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"No such group with name {group_name} exists")

    return f"Marked all todo tasks in group {group_name} as completed"

@app.delete("/deletetodogroup/{group_name}", status_code=status.HTTP_204_NO_CONTENT)
def create_group(group_name: str, user = Depends(get_current_user)):

    session = Session(bind=engine, expire_on_commit=False)

    todo_group_list = session.query(models.ToDo).filter_by(group_name=group_name).all()

    if todo_group_list:
        for todo in todo_group_list:
            session.delete(todo)
            session.commit()
        session.close()

    else:
        raise HTTPException(status_code=404, detail=f"No such group with name {group_name} exists")

    return None

@app.post("/createtodogroup", status_code=status.HTTP_201_CREATED)
def create_group(todo: schemas.ToDo, user = Depends(get_current_user)):

    if not todo.group_name:
        raise HTTPException(status_code=404, detail=f"No group specified for todo task")

    session = Session(bind=engine, expire_on_commit=False)

    tododb = models.ToDo(task = todo.task, due_date = todo.due_date, is_completed = todo.is_completed, assigned_to = todo.assigned_to, created_by = user.username, group_name = todo.group_name)

    session.add(tododb)
    session.commit()

    id = tododb.id

    session.close()

    return f"created todo item with id {id} and group name {todo.group_name}"


if __name__ == "__main__":
    uvicorn.run(app, host  = "0.0.0.0", port = 8000)