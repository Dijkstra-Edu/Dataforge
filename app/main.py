from fastapi import Depends, FastAPI
from Settings.logging_config import setup_logging
from Controllers import main_controller
from Controllers.Opportunities import job_controller
from Controllers.User import (
    certifications_controller,
    dijkstra_certificate_controller,
    education_controller,
    leetcode_controller,
    links_controller,
    profile_controller,
    projects_controller,
    publication_controller,
    user_controller,
    volunteering_controller,
    workexperience_controller,
)

from Controllers.Opportunities import fellowships_controller, organization_controller, projects_opportunities_controller
from Controllers.User import location_controller
from Controllers.error_handlers import register_exception_handlers
from db import init_db
app = FastAPI()

# Initialize logging
logger = setup_logging()

@app.on_event("startup")
def on_startup():
    logger.info("Starting up the application...")
    # init_db()
    logger.info("Database initialized successfully.")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("Shutting down the application...")

register_exception_handlers(app)
app.include_router(main_controller.router)

app.include_router(user_controller.router)
app.include_router(workexperience_controller.router)
app.include_router(location_controller.router)
app.include_router(profile_controller.router)
app.include_router(leetcode_controller.router)
app.include_router(dijkstra_certificate_controller.router)
app.include_router(certifications_controller.router)
app.include_router(job_controller.router)
app.include_router(fellowships_controller.router)
app.include_router(organization_controller.router)
app.include_router(projects_opportunities_controller.router)
app.include_router(links_controller.router)
app.include_router(volunteering_controller.router)
app.include_router(projects_controller.router)
app.include_router(education_controller.router)
app.include_router(publication_controller.router)
