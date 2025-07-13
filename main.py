from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.customers import router_customers
from routes.orders import router_orders
from routes.products import router_products

from schemas.models import HealthResponse

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router_customers, prefix="/customers")
app.include_router(router=router_products, prefix="/products")
app.include_router(router=router_orders, prefix="/orders")


@app.get("/", response_model=HealthResponse)
async def health():
    return HealthResponse(status="Ok")
