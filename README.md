The current value of the stock forward contract is calculated by subtracting the discounted forward price from the spot price using the following formula.

$$C = S_0 - K \times e^{-rT}$$

The vega for a forward contract is assumed to be 0 and the delta is assumed to be 1.

To compute the current value of a European stock option, the closed-form Black–Scholes model was used. This model is essentially the analytical solution to the Black–Scholes PDE, under the assumption that the underlying stock price follows a geometric Brownian motion. Limitations of these assumptions include the fact that real stock prices may exhibit jumps, volatility is not constant, and model parameters may be non-stationary over time.

#### The Black-Scholes Equation 
$$C = S_t \Phi(d_1) - Ke^{-rt} \Phi(d_2)$$

$$\Phi(x) = \int_{-\infty}^x \frac{1}{\sqrt{2\pi}}e^{\frac{-s^2}{2}}ds$$

$$d_1 = \frac{ln(\frac{S_t}{K})+(r+\frac{\sigma^2}{2})t}{\sigma \sqrt{t}}$$

$$d_2 = d_1 - \sigma \sqrt{t}$$

$$\frac{dS_t}{S_t} = \mu dt + \sigma dW_t$$

### Black–Scholes Delta and Vega

#### Delta
- **Call delta**:
$$\Delta_{\text{call}} = N(d_1)$$
- **Put delta**:
$$\Delta_{\text{put}} = N(d_1) - 1$$

#### Vega
$$\text{Vega} = S_0 \sqrt{T}\, \phi(d_1)$$

Where the standard normal PDF is:
$$\phi(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2 / 2}$$


####
The software is implemented as a simple FastAPI application exposing two POST endpoints for submitting parameters to the two pricing models. A Streamlit interface was used due to its high-level abstractions and ease of use in Python. A Redis instance—running in a Docker container—is included to demonstrate how cached results can be used.

The system consists of three Docker containers and is orchestrated using Docker Compose. For demonstration purposes, the application is deployed on a small AWS EC2 instance on my personal account (please don’t stress-test it—there is no security hardening in place). The link is the following - http://13.217.226.80:8501/

In a production environment, an ingress layer, typically a reverse proxy or API gateway, should be placed in front of all application instances. The services can be deployed within a Kubernetes cluster to provide high availability and fault tolerance. Raw equity market data would likely be ingested from a colocated facility or low-latency data center and then replicated to make it highly available for downstream tasks. Using a high-performance time-series database such as kdb+ for storing and querying the data enables efficient real-time pricing of the two options.

Useful resources:
https://www.columbia.edu/~mh2078/FoundationsFE/BlackScholes.pdf

## Running the Application

To run the application, use Docker Compose: `docker-compose up --build`. The API will be available at `http://localhost:8000`, with the automatically generated docs page at `http://localhost:8000/docs`, and the Streamlit UI at `http://localhost:8501`.
