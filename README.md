# Simple Pricing Service

A Python-based service that prices financial instruments (stock forward contracts and European stock options) and exposes them via a REST API.

## Overview

This service implements:
- **Stock Forward Contract** pricing with delta and vega
- **European Stock Option** pricing (call/put) using Black-Scholes model with delta and vega
- RESTful API endpoints with JSON input/output
- Redis-based caching for improved performance
- Web UI for interactive pricing
- Comprehensive error handling and logging

## Features

✅ Pricing functions return **price, delta, and vega** for both instruments  
✅ RESTful API with JSON request/response format  
✅ Async request handling using FastAPI  
✅ Redis caching with 60-second TTL  
✅ Comprehensive error handling and validation  
✅ Structured logging  
✅ Docker-based deployment  
✅ Web UI for easy interaction  
✅ Client script for API demonstration  

---

## Design Decisions

### Architecture

1. **FastAPI Framework**: Chosen for its modern async/await support, automatic OpenAPI documentation, and high performance
2. **Separation of Concerns**: 
   - Pricing logic isolated in `app/pricers/` modules
   - API layer handles HTTP requests/responses and caching
   - Clear separation between business logic and infrastructure
3. **Caching Strategy**: Redis-based caching with JSON-serialized results to cache full response (price, delta, vega)
4. **Containerization**: Each service (API, UI) has its own Dockerfile for independent scaling and deployment

### Pricing Implementation

1. **Forward Contract**: 
   - Formula: `V₀ = S₀ - K * exp(-r * T)`
   - Delta: 1.0 (forward on non-dividend-paying stock)
   - Vega: 0.0 (no volatility sensitivity)

2. **European Option**:
   - Black-Scholes model implementation
   - Handles edge cases (T=0, sigma=0)
   - Uses error function for normal CDF approximation
   - Delta and Vega calculated analytically

### API Design

1. **RESTful Endpoints**: 
   - `POST /price/forward` - Price forward contracts
   - `POST /price/european-option` - Price European options
2. **Response Format**: Returns `price`, `delta`, `vega`, and `cached` flag
3. **Error Handling**: HTTP 400 for validation errors, 500 for server errors

### Caching

- Cache key: `{instrument_type}:{JSON-serialized request parameters}`
- TTL: 60 seconds (configurable)
- Stores full result (price, delta, vega) as JSON

---

## Assumptions

1. **Non-dividend-paying stocks**: All pricing assumes no dividends during the contract life
2. **Continuous compounding**: Risk-free rate `r` uses continuous compounding
3. **Constant volatility**: European option pricing assumes constant volatility (Black-Scholes assumption)
4. **Time units**: Time to maturity `T` is in years
5. **Volatility**: Annualized volatility (e.g., 0.2 = 20%)
6. **Input validation**: All inputs must be non-negative (except rate, which can be negative for unusual scenarios)
7. **Redis availability**: Service assumes Redis is available; falls back gracefully if not configured

---

## Running the Application

### Using Docker Compose (Recommended)

The application consists of three services:
- **API**: FastAPI backend on port 8000
- **UI**: Streamlit frontend on port 8501
- **Redis**: Caching service on port 6379

To run all services:

```bash
docker-compose up --build
```

This will:
1. Build the Docker images for `app` and `ui` services
2. Start all three services (api, ui, redis)
3. Make the services available at:
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - UI: http://localhost:8501
   - Redis: localhost:6379

To run in detached mode (background):
```bash
docker-compose up -d --build
```

To stop all services:
```bash
docker-compose down
```

To view logs:
```bash
docker-compose logs -f
```

### Running Locally (Without Docker)

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start Redis** (if not already running):
```bash
redis-server
```

3. **Start the API:**
```bash
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

4. **In another terminal, start the UI:**
```bash
cd ui
streamlit run app.py
```

---

## Deploying to AWS (Simplest Method)

For detailed instructions, see [AWS Deployment Guide](docs/AWS_DEPLOYMENT.md).

**Quick Steps:**
1. Launch EC2 instance (Amazon Linux or Ubuntu)
2. Install Docker: `sudo yum install docker -y` (or `sudo apt install docker.io -y` for Ubuntu)
3. Install Docker Compose (see deployment guide)
4. Upload code: `git clone <your-repo>` or use `scp`
5. Run: `docker-compose up -d --build`
6. Access: `http://<EC2_IP>:8000` (API) and `http://<EC2_IP>:8501` (UI)

**Quick deploy script:** After setup, just run `./deploy.sh` on EC2 to update.

---

## Running the Client Script

The client script demonstrates how to call both API endpoints with sample data.

### Prerequisites

- Python 3.11+
- `requests` library (included in requirements.txt)
- API service running (see "Running the Application" above)

### Usage

```bash
python client/client.py
```

Or make it executable:
```bash
chmod +x client/client.py
./client/client.py
```

The client script demonstrates:
1. Pricing a forward contract
2. Pricing a European call option
3. Pricing a European put option
4. Cache functionality (calling the same endpoint twice)
5. Error handling (invalid inputs)

### Example Output

```
============================================================
Pricing Service API Client Demo
============================================================
✅ API is reachable at http://localhost:8000

============================================================
SAMPLE 1: Stock Forward Contract
============================================================
Pricing Forward Contract:
  Spot Price (S0): 100.0
  Strike Price (K): 95.0
  Risk-free Rate (r): 0.02
  Time to Maturity (T): 0.5 years

============================================================
Endpoint: /price/forward
Status Code: 200
============================================================
{
  "cached": false,
  "price": 4.95,
  "delta": 1.0,
  "vega": 0.0
}
```

---

## API Endpoints

### POST /price/forward

Price a stock forward contract.

**Request Body:**
```json
{
  "S0": 100.0,    // Spot price
  "K": 95.0,      // Strike/forward price
  "r": 0.02,      // Risk-free rate (continuous compounding)
  "T": 0.5        // Time to maturity (years)
}
```

**Response:**
```json
{
  "cached": false,
  "price": 4.95,
  "delta": 1.0,
  "vega": 0.0
}
```

### POST /price/european-option

Price a European stock option.

**Request Body:**
```json
{
  "S0": 100.0,      // Spot price
  "K": 95.0,        // Strike price
  "r": 0.01,        // Risk-free rate (continuous compounding)
  "sigma": 0.2,     // Volatility (annualized)
  "T": 0.5,         // Time to maturity (years)
  "type": "call"    // "call" or "put"
}
```

**Response:**
```json
{
  "cached": false,
  "price": 7.39,
  "delta": 0.67,
  "vega": 26.83
}
```

---

## Production Improvements

The following enhancements are recommended for production deployment:

### Performance & Scalability

1. **Load Balancing**: 
   - Use nginx or AWS ALB in front of multiple API instances
   - Implement health checks and graceful degradation

2. **Horizontal Scaling**:
   - Run multiple API instances behind a load balancer
   - Use Redis Cluster for distributed caching

3. **Database Integration**:
   - Store historical pricing requests for analytics
   - Implement request/response logging database

### Caching Enhancements

1. **Cache Warming**: Pre-populate cache with common pricing scenarios
2. **Cache Invalidation**: More sophisticated TTL strategies based on market conditions
3. **Multi-level Caching**: Add in-memory cache (e.g., LRU) before Redis

### Monitoring & Observability

1. **Metrics**: 
   - Add Prometheus metrics (request rate, latency, cache hit rate)
   - Track pricing calculation times
   - Monitor Redis performance

2. **Distributed Tracing**: 
   - Implement OpenTelemetry for request tracing
   - Track requests across services

3. **Alerting**: 
   - Set up alerts for high error rates
   - Monitor cache hit rates and Redis availability

### Security

1. **Authentication/Authorization**: 
   - Add API keys or OAuth2
   - Rate limiting per user/IP

2. **Input Validation**: 
   - Add more sophisticated validation
   - Sanitize inputs to prevent injection attacks

3. **HTTPS**: Use TLS/SSL for all communications

### Reliability

1. **Circuit Breakers**: Implement circuit breakers for Redis connections
2. **Retry Logic**: Add exponential backoff for transient failures
3. **Graceful Shutdown**: Ensure in-flight requests complete before shutdown
4. **Health Checks**: Implement `/health` endpoint for orchestration systems

### Code Quality

1. **Testing**: 
   - Unit tests for pricing functions
   - Integration tests for API endpoints
   - Load testing for performance validation

2. **Documentation**: 
   - More detailed API documentation
   - OpenAPI/Swagger specification

3. **CI/CD**: 
   - Automated testing pipeline
   - Automated deployment workflows

---

## Project Structure

```
simple_pricing_service/
├── app/                    # FastAPI application
│   ├── Dockerfile
│   ├── main.py            # API endpoints and application setup
│   └── pricers/           # Pricing logic
│       ├── forward_option.py
│       └── european_option.py
├── ui/                    # Streamlit UI
│   ├── Dockerfile
│   └── app.py
├── client/                # Client script
│   └── client.py
├── docker-compose.yml     # Multi-service orchestration
├── requirements.txt       # Python dependencies
└── README.md
```

---

## License

Copyright © 2025 FactSet Research Systems Inc. All rights reserved.
