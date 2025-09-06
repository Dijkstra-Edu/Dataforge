from fastapi import Depends, FastAPI
from Settings.logging_config import setup_logging
from Controllers import main_controller
from Controllers.Opportunities import job_controller
from Controllers.User import certificate_controller
from Controllers.Opportunities import fellowships_controller, organization_controller, projects_opportunities_controller
from Controllers.User import user_controller
from db import init_db

app = FastAPI()

# Initialize logging
logger = setup_logging()

@app.on_event("startup")
def on_startup():
    logger.info("Starting up the application...")
    init_db()
    logger.info("Database initialized successfully.")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("Shutting down the application...")

app.include_router(main_controller.router)
app.include_router(certificate_controller.router)
app.include_router(job_controller.router)
app.include_router(fellowships_controller.router)
app.include_router(organization_controller.router)
app.include_router(projects_opportunities_controller.router)
app.include_router(user_controller.router)