import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse
from app.delivery_fee.router import delivery_fee_router
from http import HTTPStatus


app = FastAPI()
# Namespace all the routes under /api
api_root = APIRouter(prefix="/api")


# Include the delivery_fee_router under /api/delivery
api_root.include_router(delivery_fee_router, prefix="/delivery")


# include the root router
app.include_router(api_root)


# Redirect requests on root page to /docs page since there is
# nothing to see on the root page
@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs", status_code=HTTPStatus.PERMANENT_REDIRECT)


def run():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    run()
