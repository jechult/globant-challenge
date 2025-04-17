from fastapi import FastAPI
from routers import auth, load_file, reporting

# defining app variable as main app

app = FastAPI()

# including different routers to be used in main app

app.include_router(auth.router)
app.include_router(load_file.router)
app.include_router(reporting.router)