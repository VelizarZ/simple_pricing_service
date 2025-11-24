### In this assignemnt - the pricing of a detereministic stock option and an European option was proposed.

The current value of the stock forward contract is substracting the spot price with the discounting of the forward price to the present via the following formula.

$$C = S_0 - K \times e^{-rT}$$

The vega for a forward contract is assumed to be 0 and the delta is assumed to be 1.

For proividng the current value of an European stock option the closed-form Black-Scholes models was used. The model is essentialy the solution the of the BSM PDE with the assumption that the underlying stock pricing has a trajectory defined by geometric Brownian motion. Issues with these assumption can be that the underlying dynamics don't invovle jumps, volatility is not constant and non-stationarity in parametrization.

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
The software is implemented as a simple FastAPI application exposing two POST endpoints for submitting parameters to the two pricing models. A Streamlit interface was used due to its high-level abstractions and ease of use in Python. A Redis instance—running in a Docker container—is included to demonstrate how cached results can improve response times.

The system consists of three Docker containers and is orchestrated using Docker Compose. For demonstration purposes, the application was deployed on a small AWS EC2 instance on my personal account (please don’t stress-test it—there is no security hardening in place).

In a production environment, an ingress layer—typically a reverse proxy or API gateway—should be placed in front of all application instances. The services can be deployed within a Kubernetes cluster to provide high availability and fault tolerance. Raw equity market data would likely be ingested from a colocated facility or low-latency data center and then replicated to make it highly available for downstream tasks. Using a high-performance time-series database such as kdb+ for storing and querying the data enables efficient real-time pricing of the two options.

Useful resources:
https://www.columbia.edu/~mh2078/FoundationsFE/BlackScholes.pdf

## Running the Application

To run the application, use Docker Compose: `docker-compose up --build`. The API will be available at `http://localhost:8000` and the Streamlit UI at `http://localhost:8501`.
