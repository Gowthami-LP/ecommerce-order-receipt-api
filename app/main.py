from fastapi import FastAPI

from app.routes.invoices import router as invoices_router
from app.routes.orders import router as orders_router
from app.routes.profiles import router as profiles_router
from app.routes.products import router as products_router
from app.routes.receipts import router as receipts_router

app = FastAPI(
    title="E-Commerce Order Receipt API",
    description="A beginner-friendly FastAPI application that combines data from MongoDB collections into a single receipt response.",
    version="1.0.0",
)

app.include_router(profiles_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(invoices_router)
app.include_router(receipts_router)


@app.get("/", tags=["Health"])
def root():
    """Simple health check for the application root."""
    return {"message": "E-Commerce Order Receipt API is running"}


@app.get("/health", tags=["Health"])
def health_check():
    """Health endpoint used for simple startup checks."""
    return {"status": "healthy"}
