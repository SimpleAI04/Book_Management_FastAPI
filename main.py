from fastapi import FastAPI
from app.api.endpoints import book, author, category

app = FastAPI(
    title="Book Management API",
    description="Simple API for managing books, author, category",
    version="1.0.0",
)

# include router
app.include_router(book.router, prefix="/books", tags=["Books"])
app.include_router(author.router, prefix="/authors", tags=["Authors"])
app.include_router(category.router, prefix="/categories", tags=["Categories"])


@app.get("/")
def root():
    return {"Welcome to FAST API"}
