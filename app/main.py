import uvicorn
import httpx
from fastapi import FastAPI, Request, HTTPException
from Settings.logging_config import setup_logging
from Entities.SearchParams import SearchParams
from Controllers import MainController 
import requests,os
from collections import Counter

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
async def getCertData(userName: str):
    logger.info("GET Request GitHub Data for user: " + userName)
    return await MainController.getCertData(userName) # Combine this with the other API




