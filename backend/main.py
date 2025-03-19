from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry

# Mock database for storing crawled pages
mock_crawled_pages = [
    {"url": "https://example.com", "title": "Example", "links": ["https://example.com/about"]}
]

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
app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

@app.post("/api/crawler")
async def receive_crawler_data(data: dict):
    print("Received data:", data)
    return {"message": "Crawler started!", "received": data}
