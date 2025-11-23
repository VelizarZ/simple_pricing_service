from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
import uvicorn

from pricers.forward import price_forward
from pricers.european_option import price_european_option


# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------
logger = logging.getLogger("pricing-service")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ------------------------------------------------------------------------------
# FastAPI app
# ------------------------------------------------------------------------------
app = FastAPI(
    title="Pricing Service",
    description="Forward + European Option Pricing API",
    version="1.0.0",
)


# ------------------------------------------------------------------------------
# Request Schemas
# ------------------------------------------------------------------------------
class ForwardInput(BaseModel):
    S0: float
    K: float
    r: float
    T: float


class OptionInput(BaseModel):
    S0: float
    K: float
    r: float
    sigma: float
    T: float
    type: str = "call"


# ------------------------------------------------------------------------------
# Error Handling
# ------------------------------------------------------------------------------
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error."},
    )





# ------------------------------------------------------------------------------
# API Endpoints
# ------------------------------------------------------------------------------
@app.post("/price/forward")
async def price_forward_endpoint(data: ForwardInput):
    try:
        return price_forward(data.S0, data.K, data.r, data.T)
    except Exception as e:
        logger.error(f"Forward pricing error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/price/european-option")
async def price_option_endpoint(data: OptionInput):
    try:
        return price_european_option(
            data.S0, data.K, data.r, data.sigma, data.T, data.type
        )
    except Exception as e:
        logger.error(f"Option pricing error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ------------------------------------------------------------------------------
# Run with: python api/server.py
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
