from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry

# mok database
mock_crawled_pages = [
    {"url": "https://example.com", "title": "Example", "links": ["https://example.com/about"]}
]

@strawberry.type
class CrawlerResult:
    url: str
    title: str
    links: list[str]

# Query Resolver to Fetch Crawled Data
@strawberry.type
class Query:
    @strawberry.field
    def get_crawled_pages(self) -> list[CrawlerResult]:
        return [CrawlerResult(**page) for page in mock_crawled_pages]  # Returns mock data

# Mutation Resolver to Add Crawled Data
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_page(self, url: str, title: str, links: list[str]) -> bool:
        mock_crawled_pages.append({"url": url, "title": title, "links": links})  # Stores in mock DB
        return True

# Create GraphQL Schema & Router
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

# Setup FastAPI
app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

# Start FastAPI Server (Run `uvicorn main:app --reload`)
