from fastapi import FastAPI
from model import Base

from database import engine
from routers import auth, todos,admin,users

app = FastAPI()

Base.metadata.create_all(bind=engine)

#Health Check Endpoint
#It simply tells----> “Is my API running or not?”
@app.get("/healthy")
async def health_check():
    return {'status': 'Healthy'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

