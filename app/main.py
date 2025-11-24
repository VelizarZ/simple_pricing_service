from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from redis.asyncio import Redis
import json
import os
import logging

from pydantic import BaseModel
from app.pricers.forward_option import price_forward
from app.pricers.european_option import price_european_option

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ----------------------------
# Lifespan (startup + shutdown)
# ----------------------------
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Connect to Redis (no await needed on creation)
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    app.state.redis = Redis.from_url(
        redis_url,
        decode_responses=True
    )
    logger.info(f"🚀 Redis connected at {redis_url}")
    yield
    # Clean shutdown
    await app.state.redis.aclose()
    logger.info("🛑 Redis disconnected")


app = FastAPI(lifespan=app_lifespan)


# ----------------------------
# Models
# ----------------------------
class ForwardRequest(BaseModel):
    S0: float
    K: float
    r: float
    T: float


class EuropeanOptionRequest(BaseModel):
    S0: float
    K: float
    r: float
    sigma: float
    T: float
    type: str  # call/put


# ----------------------------
# Helper: cache key
# ----------------------------
def make_cache_key(prefix: str, data: dict):
    return prefix + ":" + json.dumps(data, sort_keys=True)


# ----------------------------
# Endpoints
# ----------------------------
@app.post("/price/forward")
async def price_forward_endpoint(req: ForwardRequest):
    """Price a stock forward contract. Returns price, delta, and vega."""
    try:
        redis = app.state.redis
        req_dict = req.dict()
        key = make_cache_key("forward", req_dict)

        # Check cache
        cached = await redis.get(key)
        if cached:
            cached_result = json.loads(cached)
            logger.info(f"Cache hit for forward pricing: {req_dict}")
            return {"cached": True, **cached_result}

        # Calculate pricing
        logger.info(f"Calculating forward price for: {req_dict}")
        result = price_forward(**req_dict)
        
        # Cache the full result (price, delta, vega)
        await redis.set(key, json.dumps(result), ex=60)  # TTL: 60 seconds
        
        logger.info(f"Forward pricing result: {result}")
        return {"cached": False, **result}
    
    except ValueError as e:
        logger.error(f"Validation error in forward pricing: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in forward pricing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/price/european-option")
async def price_option_endpoint(req: EuropeanOptionRequest):
    """Price a European stock option. Returns price, delta, and vega."""
    try:
        redis = app.state.redis
        req_dict = req.dict()
        key = make_cache_key("european", req_dict)

        # Check cache
        cached = await redis.get(key)
        if cached:
            cached_result = json.loads(cached)
            logger.info(f"Cache hit for European option pricing: {req_dict}")
            return {"cached": True, **cached_result}

        # Convert "type" to "option_type" for the pricing function
        req_dict["option_type"] = req_dict.pop("type")
        
        # Calculate pricing
        logger.info(f"Calculating European option price for: {req_dict}")
        result = price_european_option(**req_dict)
        
        # Cache the full result (price, delta, vega)
        await redis.set(key, json.dumps(result), ex=60)
        
        logger.info(f"European option pricing result: {result}")
        return {"cached": False, **result}
    
    except ValueError as e:
        logger.error(f"Validation error in European option pricing: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in European option pricing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
