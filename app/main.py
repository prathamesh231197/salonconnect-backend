# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.session import engine, Base
from api.v1 import auth
from api.v1 import users
from api.v1 import salons
from api.v1 import bookings
from api.v1 import availability


# create tables (simple approach for dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SalonConnect API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])


@app.get("/api/health")
async def health():
    return {"status": "ok"}


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(salons.router, prefix="/api/salons", tags=["salons"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["bookings"])
app.include_router(availability.router,
                   prefix="/api/availability", tags=["availability"])
