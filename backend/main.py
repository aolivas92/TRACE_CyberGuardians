from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from strawberry.fastapi import GraphQLRouter
import strawberry
import logging
import uvicorn
import time

# TODO: import the ml and the crawler services
# from src.modules.scanning.CrawlerManager import CrawlerManager
from src.modules.ai.credential_generator import Credential_Generator
from src.modules.ai.web_scraper import WebScraper

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock database for storing crawled pages
mock_crawled_pages = [
    {"url": "https://example.com", "title": "Example", "links": ["https://example.com/about"]}
]

# Pydantic model for crawler configuration
class CrawlerConfig(BaseModel):
    target_url: str
    depth: Optional[int] = 2
    max_pages: Optional[int] = 50
    user_agent: Optional[str] = None
    delay: Optional[int] = 1000
    proxy: Optional[int] = None

    # Handles formatting data from fronted.
    class Config:
        alias_generator = lambda field_name: field_name.replace('_', '-')
        populate_by_name = True
        
    # This method logs the received data
    @classmethod
    def debug_request(cls, data: dict):
        logger.info(f"Raw request data: {data}")
        for key, value in data.items():
            logger.info(f"Field: {key}, Value: {value}, Type: {type(value)}")
        return data
    
# Pydantic model for ml algorithm configuration
class MLAlgorithmConfig(BaseModel):
    # TODO: add the different variables that will be passed.
    target_url: str

    # Handles formatting data from fronted.
    class Config:
        alias_generator = lambda field_name: field_name.replace('_', '-')
        populate_by_name = True
        
    # TODO: Add the section to handle formatting the data that is given from the frontend.
    # This method logs the received data
    @classmethod
    def debug_request(cls, data: dict):
        logger.info(f"Raw request data: {data}")
        for key, value in data.items():
            logger.info(f"Field: {key}, Value: {value}, Type: {type(value)}")
        return data

#Response model for crawler job status
class CrawlerJobResponse(BaseModel):
    job_id: str
    message: str
    status: str
    # TODO: Could add the percentage and other information to be passed.

#Response model for ml algorithm job status.
class MLAlgorithmJobResponse(BaseModel):
    job_id: str
    message: str
    status: str
    # TODO: Could add the percentage and other information to be passed.

# GraphQL Schema Definitions
@strawberry.type
class CrawlerResult:
    url: str
    title: str
    links: list[str]

@strawberry.type
class Query:
    @strawberry.field
    def get_crawled_pages(self) -> list[CrawlerResult]:
        return [CrawlerResult(**page) for page in mock_crawled_pages]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_page(self, url: str, title: str, links: list[str]) -> bool:
        mock_crawled_pages.append({"url": url, "title": title, "links": links})
        return True

# Setup GraphQL Schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

# Create FastAPI App
app = FastAPI(title="Web Crawler API")

# Configure CORS to allow requests from SvelteKit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")

# Crawler endpoints.
@app.post("/api/crawler")
async def receive_crawler_data(config: CrawlerConfig):
    logger.info(f"Received crawler configuration: {config}")
    
    # Pass the configuration to the crawler service
    # TODO: once implemented start a job with the crawler.
    
    return {
        "message": "Crawler started successfully!",
        "config": config.dict(),
        "job_id": "12345"  # Mock job ID
    }

# Crawler endpoints.
@app.post("/api/ml_algorithm")
async def receive_ml_algorithm_data(config: MLAlgorithmConfig):
    logger.info(f"Received ML Algorithm configuration: {config}")
    
    # Scrape the target URL
    # TODO: Update to be the correct target url
    scraper = WebScraper(urls=[config.target_url])
    scraped_data = scraper.scrape_pages()

    # Save the Scraped data to database
    # TODO: Update to save it to the correct database, for now a csv file
    csv_path = "./src/database/scraped_data.csv"

    # Initialize and run credential generator
    # TODO: Update utilize the count that the user has passed.
    generator = Credential_Generator(csv_path=csv_path)
    credentials = generator.generate_credentials(count=10)
    
    return {
        "job_id": "ml_" + str(int(time.time())),
        "status": "success",
        "message": f"Generated {len(credentials)} credentials from {config.target_url}",
        "credentials": [
            {"username": u, "password": p} for u, p in credentials
        ]
    }

@app.get("/")
async def root():
    return {"message": "Web Crawler API is running. Access /docs for documentation."}

# For debugging - print raw request body
@app.post("/api/debug")
async def debug_endpoint(request: Request):
    body = await request.body()
    logger.info(f"Raw request body: {body}")
    try:
        json_body = await request.json()
        logger.info(f"JSON body: {json_body}")
        return {"received": json_body}
    except Exception as e:
        logger.error(f"Error parsing JSON: {e}")
        return {"error": str(e), "raw_body": body.decode()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)