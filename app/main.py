import os
import sys

# Add the 'app' folder to sys.path so absolute imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import uvicorn
import httpx
from fastapi import FastAPI, Request, HTTPException
from settings.logging_config import setup_logging
from Entities.SearchParams import SearchParams
from Controllers import MainController



app = FastAPI()

# Initialize logging
logger = setup_logging()

@app.get('/Dijkstra/v1/certificate/health', status_code=200)
async def root():
    logger.info("Health Endpoint Triggered")
    return {"status": 200, 'message': 'Dijkstra Certificate Generator Health Endpoint Triggered!!!'}

@app.post('/Dijkstra/v1/certificate/download/{userName}')
async def postDownloadCertificate(userName: str):
    logger.info("POST Request Certificate Download for user: " + userName)
    return await MainController.postDownloadCertificate(userName)

@app.get('/Dijkstra/v1/certificate/data/{userName}')
async def getGitHubData(userName: str, params: SearchParams):
    logger.info("GET Request GitHub Data for user: " + userName)
    return await MainController.getGitHubData(userName, params) # Combine this with the other API