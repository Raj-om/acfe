# Phase 5: Mathematical Model for the Adaptive Confidence Fusion Engine (ACFE)

This document details the rigorous mathematical framework underpinning the Adaptive Confidence Fusion Engine (ACFE). The ACFE is designed to synthesize multi-source probabilistic inputs into a calibrated, robust, and dynamically adaptive confidence estimate.

---

## 1. Problem Formulation

### 1.1 Formal Definition of the Multi-Source Confidence Fusion Problem
Let the environment be observed by a set of $N$ heterogeneous sources (e.g., sensors, models, or heuristic algorithms), denoted by $S = \{S_1, S_2, \dots, S_N\}$. At any discrete time step $t \in \mathbb{N}$, each source $S_i$ provides an observation regarding an unknown true state $x^* \in \mathcal{X}$. The goal of the multi-source confidence fusion problem is to construct an aggregation function $\mathcal{F}$ that synthesizes individual source estimates and their respective confidence scores into a unified, calibrated, and highly reliable joint confidence estimate for the true state $x^*$.

### 1.2 State Space, Observation Space, Action Space
- **State Space ($\mathcal{X}$):** The space of all possible true states of the system. For a classification task, $\mathcal{X} = \{1, 2, \dots, K\}$ where $K$ is the number of classes. For a continuous tracking task, $\mathcal{X} \subseteq \mathbb{R}^d$.
- **Observation Space ($\mathcal{Z}$):** The domain of measurements produced by the sources. An observation from source $i$ at time $t$ is denoted $z_i(t) \in \mathcal{Z}_i$, where $\mathcal{Z}_i$ is the specific observation space for source $i$. We denote the joint observation vector as $\mathbf{z}(t) = [z_1(t), z_2(t), \dots, z_N(t)]^T$.
- **Action Space ($\mathcal{A}$):** The space of decisions made based on the fused confidence. While ACFE primarily focuses on state estimation and confidence calibration, in a decision-theoretic framework, a policy $\pi(a | \mathbf{z}(t))$ selects an action $a \in \mathcal{A}$ to minimize an expected risk.

### 1.3 Notation Table
| Symbol | Definition |
| :--- | :--- |
| $N$ | Number of independent sources/sensors. |
| $S_i$ | The $i$-th source, where $i \in \{1, 2, \dots, N\}$. |
| $t$ | Discrete time step. |
| $x^*$ | The unobservable true state. |
| $z_i(t)$ | Observation from source $S_i$ at time $t$. |
| $c_i(t)$ | Raw confidence score reported by source $i$ at time $t$. |
| $w_i(t)$ | Adaptive weight assigned to source $i$ at time $t$. |
| $\lambda_i$ | Temporal decay constant for source $i$. |
| $\mathcal{F}$ | The fusion mapping function. |
| $p_i(x | z_i(t))$ | Probability distribution over $\mathcal{X}$ from source $i$. |

---

## 2. Confidence Equations

### 2.1 Per-Source Confidence Score: $c_i(t)$ Derivation
The raw confidence score $c_i(t) \in [0, 1]$ represents the source's internal estimate of the probability that its observation $z_i(t)$ accurately reflects the true state $x^*$. It is typically derived from the entropy of the predictive distribution or margin classifiers.
$$ c_i(t) = 1 - \frac{\mathcal{H}(p_i(x|z_i(t)))}{\log|\mathcal{X}|} $$
where $\mathcal{H}(\cdot)$ is the Shannon entropy. 

### 2.2 Multi-Dimensional Confidence Vector Representation
At time $t$, the system aggregates confidence scores into a multi-dimensional confidence vector:
$$ \mathbf{c}(t) = \begin{bmatrix} c_1(t) \\ c_2(t) \\ \vdots \\ c_N(t) \end{bmatrix} \in [0, 1]^N $$

### 2.3 Confidence Normalization Across Sources
Before fusion, confidences may require normalization to account for inherently overconfident or underconfident sources. Let $\mu_{c_i}$ and $\sigma_{c_i}$ be the historical mean and standard deviation of source $i$'s confidence. We define the normalized confidence $\tilde{c}_i(t)$ via robust scaling:
$$ \tilde{c}_i(t) = \Phi \left( \frac{c_i(t) - \mu_{c_i}}{\sigma_{c_i}} \right) $$
where $\Phi(\cdot)$ is the standard normal Cumulative Distribution Function (CDF), ensuring $\tilde{c}_i(t) \in (0, 1)$.

### 2.4 Temporal Decay Model for Confidence
In asynchronous or latent environments, observations become stale. We model the degradation of confidence over time using an exponential decay function. If the last observation from source $i$ was received at $t_0$, the projected confidence at time $t > t_0$ is:
$$ c_i(t) = c_i(t_0) \cdot e^{-\lambda_i (t - t_0)} $$
where $\lambda_i > 0$ is the source-specific decay rate, determined empirically based on the source's measurement volatility. 

---

## 3. Adaptive Weighting Mechanism

### 3.1 Dynamic Weight Computation
The core of the fusion engine relies on dynamic weights $w_i(t)$, which dictate the influence of each source. These weights are a function of historical reliability $R_i(t)$ and the temporally decayed confidence $c_i(t)$. We define a raw affinity score $a_i(t)$:
$$ a_i(t) = \theta_1 R_i(t) + \theta_2 c_i(t) + \theta_3 (1 - u_i(t)) $$
where $u_i(t)$ is the estimated epistemic uncertainty of the source, and $\theta_1, \theta_2, \theta_3$ are learned parameters.

### 3.2 Softmax Normalization of Weights
To ensure weights form a valid convex combination (i.e., $\sum_{i=1}^N w_i(t) = 1$ and $w_i(t) \ge 0$), we apply the softmax function with a temperature parameter $\tau$:
$$ w_i(t) = \frac{\exp(a_i(t) / \tau)}{\sum_{j=1}^N \exp(a_j(t) / \tau)} $$

### 3.3 Reliability-Adjusted Weighting
Reliability $R_i(t)$ is updated recursively based on the source's past performance against the final fused consensus or ground truth (if available). Using an exponential moving average (EMA) with decay factor $\alpha \in (0, 1)$:
$$ R_i(t) = \alpha R_i(t-1) + (1 - \alpha) \mathcal{S}(z_i(t), x^*) $$
where $\mathcal{S}$ is a scoring rule (e.g., negative Brier score).

### 3.4 Adversarial Robustness Constraint
To prevent malicious or faulty sources from hijacking the fusion engine, we impose a divergence constraint. Let $D_{KL}(p_i \| p_{fused})$ be the Kullback-Leibler divergence between source $i$'s prediction and the fused prediction. If $D_{KL} > \delta_{thresh}$, the raw weight $a_i(t)$ is heavily penalized:
$$ a'_i(t) = a_i(t) - \eta \cdot \max(0, D_{KL}(p_i \| p_{fused}) - \delta_{thresh}) $$

### 3.5 Mathematical Properties
- **Convergence:** Due to the EMA update of reliability and the continuous nature of the softmax mapping, $w_i(t)$ asymptotically converges to stationary values if the underlying source distributions and true state remain stationary.
- **Boundedness:** By definition of the softmax function, $w_i(t) \in [0, 1] \forall i, t$.

---

## 4. Uncertainty Propagation

### 4.1 Total Uncertainty Decomposition
Uncertainty in predictions arises from two primary sources:
- **Aleatoric Uncertainty ($u_{a}$):** Inherent data noise (e.g., sensor noise).
- **Epistemic Uncertainty ($u_{e}$):** Model ignorance (e.g., lack of training data).
Total uncertainty $U(t)$ is the sum: $U(t) = u_a(t) + u_e(t)$. For a probabilistic model, if $p(y|x, \theta)$ is the predictive distribution parameterized by $\theta \sim q(\theta)$, total variance is:
$$ \text{Var}(y) = \mathbb{E}_{q(\theta)}[\text{Var}(y|x, \theta)] + \text{Var}_{q(\theta)}(\mathbb{E}[y|x, \theta]) $$
The first term is aleatoric; the second is epistemic.

### 4.2 Propagation through Linear Fusion Layers
For a linear fusion combination $\hat{y} = \sum_{i=1}^N w_i y_i$, assuming sources have uncorrelated errors with variances $\sigma_i^2$, the combined variance (uncertainty) is:
$$ \sigma_{fused}^2 = \sum_{i=1}^N w_i^2 \sigma_i^2 $$
To minimize $\sigma_{fused}^2$ under $\sum w_i = 1$, the optimal inverse-variance weights are $w_i \propto \frac{1}{\sigma_i^2}$.

### 4.3 Propagation through Nonlinear (GNN) Fusion
When using a Graph Neural Network (GNN) for fusion, where nodes represent sources and edges represent correlations, uncertainty propagation is tracked via the Delta method or Monte Carlo Dropout. Let the fusion operation be $f_{\phi}(\mathbf{z})$. The propagated epistemic uncertainty is approximated by:
$$ u_{e, fused} \approx \frac{1}{M} \sum_{m=1}^M f_{\phi^{(m)}}(\mathbf{z}) - \left( \frac{1}{M} \sum_{m=1}^M f_{\phi^{(m)}}(\mathbf{z}) \right)^2 $$
where $\phi^{(m)}$ are sampled from the dropout distribution.

### 4.4 Uncertainty Accumulation Bounds
By the Cauchy-Schwarz inequality, the maximum possible uncertainty (in the case of fully correlated sources) is bounded by:
$$ \sigma_{fused} \le \sum_{i=1}^N w_i \sigma_i \le \max_i (\sigma_i) $$

### 4.5 Calibration Error: Expected Calibration Error (ECE)
To measure how well the propagated uncertainty aligns with empirical error, we define ECE. Let predictions be grouped into $M$ bins $B_1, \dots, B_M$.
$$ \text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} \left| \text{acc}(B_m) - \text{conf}(B_m) \right| $$
where $\text{acc}$ is the average accuracy in the bin, and $\text{conf}$ is the average predicted confidence.

---

## 5. Dynamic Normalization

### 5.1 Min-Max, Z-score, and Robust Scaling
- **Min-Max:** $x_{norm} = \frac{x - x_{min}}{x_{max} - x_{min}}$
- **Z-score:** $x_{norm} = \frac{x - \mu}{\sigma}$
- **Robust Scaling:** $x_{norm} = \frac{x - \text{median}}{\text{IQR}}$

### 5.2 Online Normalization with Running Statistics
For real-time streaming data, mean and variance are updated recursively (Welford's algorithm):
$$ \mu_t = \mu_{t-1} + \frac{x_t - \mu_{t-1}}{t} $$
$$ S_t = S_{t-1} + (x_t - \mu_{t-1})(x_t - \mu_t) $$
$$ \sigma_t^2 = \frac{S_t}{t} $$

### 5.3 Distribution Shift Detection
A statistical test (e.g., Page's CUSUM or online Kolmogorov-Smirnov) tracks the drift. If the divergence $D_{drift}(P_t \| P_{historical}) > \epsilon$, a renormalization trigger resets the running statistics to prevent contamination by obsolete distributions.

---

## 6. Probability Calibration

### 6.1 Platt Scaling, Isotonic Regression, Temperature Scaling
- **Platt Scaling:** Fits a logistic regression over the uncalibrated logits $z$: $p(y=1|z) = \frac{1}{1 + \exp(A z + B)}$.
- **Isotonic Regression:** Fits a non-decreasing piecewise constant function $f(z)$ minimizing $\sum (y_i - f(z_i))^2$.
- **Temperature Scaling:** A multi-class extension of Platt scaling, $q_i = \max_k \frac{\exp(z_k / T)}{\sum_j \exp(z_j / T)}$, optimizing $T > 0$ via Negative Log-Likelihood.

### 6.2 Beta Calibration
Designed for probabilities bounded in $[0,1]$, Beta calibration maps uncalibrated $p \in [0,1]$ to calibrated $q$:
$$ q = \frac{1}{1 + \exp(-c) \frac{(1-p)^b}{p^a}} $$

### 6.3 Reliability Diagram Mathematics
A reliability diagram plots $\text{conf}(B_m)$ on the x-axis versus $\text{acc}(B_m)$ on the y-axis. Perfect calibration implies the curve $y=x$.

### 6.4 ECE and MCE Definitions
- **Expected Calibration Error (ECE):** Defined in 4.5.
- **Maximum Calibration Error (MCE):** Focuses on the worst-case disparity:
$$ \text{MCE} = \max_{m \in \{1, \dots, M\}} \left| \text{acc}(B_m) - \text{conf}(B_m) \right| $$

---

## 7. Bayesian Updates

### 7.1 Prior Construction
Let $P(x)$ be the prior belief. It is constructed from sensor metadata, historical rates, or uniform uninformed priors.
$$ P(x) = \text{Dirichlet}(\alpha_1, \dots, \alpha_K) $$ (for categorical states).

### 7.2 Likelihood Model
Each sensor $i$ possesses a likelihood model $P(z_i | x)$. If observations are Gaussian with known variance $\sigma_i^2$, $P(z_i | x) = \mathcal{N}(z_i; x, \sigma_i^2)$.

### 7.3 Posterior Fusion across N Sensors
Assuming conditional independence of sensors given the true state $x$:
$$ P(x | z_1, \dots, z_N) \propto P(x) \prod_{i=1}^N P(z_i | x) $$

### 7.4 Sequential (Online) Bayesian Update
At time $t$, the posterior from $t-1$ becomes the new prior:
$$ P(x_t | z_{1:t}) = \frac{P(z_t | x_t) P(x_t | z_{1:t-1})}{\int P(z_t | x) P(x | z_{1:t-1}) dx} $$

### 7.5 Conjugate Prior Selection
Using conjugate priors ensures closed-form updates. For Gaussian likelihoods with known variance, a Gaussian prior yields a Gaussian posterior, rendering the update highly computationally efficient (equivalent to a 1D Kalman filter).

---

## 8. Dempster-Shafer Component

### 8.1 Basic Probability Assignment (BPA)
Let $\Omega$ be the frame of discernment. A BPA is a mass function $m: 2^\Omega \to [0, 1]$ satisfying $m(\emptyset) = 0$ and $\sum_{A \subseteq \Omega} m(A) = 1$.

### 8.2 Dempster's Rule of Combination
For two independent sources with masses $m_1$ and $m_2$, their combination is:
$$ (m_1 \oplus m_2)(A) = \frac{1}{1 - K} \sum_{B \cap C = A} m_1(B) m_2(C) $$
where $K = \sum_{B \cap C = \emptyset} m_1(B) m_2(C)$ measures the conflict.

### 8.3 Conflict Handling
When $K \to 1$, Dempster's rule becomes unstable (Zadeh's paradox).
- **Yager's Rule:** Assigns the conflict mass $K$ to the universal set $\Omega$.
- **PCR5 (Proportional Conflict Redistribution):** Redistributes conflict mass proportionally to the sets involved in the empty intersection.
- **Murphy's Average:** Averages the masses before combining, $m_{avg} = \frac{1}{N} \sum m_i$, then combines $m_{avg}$ with itself $N-1$ times.

### 8.4 When to use DS vs. Bayesian
Use Bayesian fusion when priors are well-defined and sensor error distributions are known. Use Dempster-Shafer when dealing with severe epistemic uncertainty, ignorance (ability to assign mass to $2^\Omega$), or when conflict identification is paramount.

---

## 9. Kalman Filter Component

### 9.1 State Vector for Confidence Tracking
We track the true state and its rate of change. $\mathbf{x}_t = [x_t, \dot{x}_t]^T$.

### 9.2 Transition Matrix F, Observation Matrix H
$$ \mathbf{x}_{t} = F \mathbf{x}_{t-1} + \mathbf{w}_t, \quad \mathbf{w}_t \sim \mathcal{N}(0, Q) $$
$$ \mathbf{z}_t = H \mathbf{x}_t + \mathbf{v}_t, \quad \mathbf{v}_t \sim \mathcal{N}(0, R) $$

### 9.3 Innovation and Kalman Gain
- **Prediction:** $\hat{\mathbf{x}}_{t|t-1} = F \hat{\mathbf{x}}_{t-1|t-1}$
  $P_{t|t-1} = F P_{t-1|t-1} F^T + Q$
- **Innovation:** $\mathbf{y}_t = \mathbf{z}_t - H \hat{\mathbf{x}}_{t|t-1}$
  $S_t = H P_{t|t-1} H^T + R$
- **Kalman Gain:** $K_t = P_{t|t-1} H^T S_t^{-1}$
- **Update:** $\hat{\mathbf{x}}_{t|t} = \hat{\mathbf{x}}_{t|t-1} + K_t \mathbf{y}_t$
  $P_{t|t} = (I - K_t H) P_{t|t-1}$

### 9.4 Adaptive Q/R Estimation (AKFS)
In dynamic environments, $Q$ and $R$ are not static. We estimate $R$ based on the innovation covariance:
$$ \hat{R}_t = \beta \hat{R}_{t-1} + (1 - \beta)(\mathbf{y}_t \mathbf{y}_t^T - H P_{t|t-1} H^T) $$

---

## 10. Loss Functions

### 10.1 Negative Log-Likelihood (NLL)
For a predicted distribution $p(y|x)$ and true label $y^*$:
$$ \mathcal{L}_{NLL} = -\log p(y^* | x) $$

### 10.2 Brier Score
A strictly proper scoring rule measuring the mean squared difference between predicted probabilities $\hat{p}_k$ and one-hot true labels $y_k^*$:
$$ \mathcal{L}_{Brier} = \frac{1}{K} \sum_{k=1}^K (\hat{p}_k - y_k^*)^2 $$

### 10.3 Continuous Ranked Probability Score (CRPS)
For continuous distributions with CDF $F$ and actual observation $y$:
$$ \text{CRPS}(F, y) = \int_{-\infty}^{\infty} (F(x) - \mathbb{I}(x \ge y))^2 dx $$

### 10.4 Composite ACFE Loss
The ACFE optimization minimizes a multi-objective loss function balancing accuracy, proper scoring, and calibration:
$$ \mathcal{L}_{ACFE} = \alpha \mathcal{L}_{NLL} + \beta \mathcal{L}_{Brier} + \gamma \mathcal{L}_{calib} $$
where $\mathcal{L}_{calib}$ is a differentiable approximation of ECE (e.g., Maximum Mean Discrepancy).

### 10.5 Hyperparameter Selection
$\alpha, \beta, \gamma$ are selected via grid search or Bayesian optimization to optimize the Pareto front between accuracy and calibration on a hold-out validation set.

---

## 11. Optimization Strategy

### 11.1 Online Gradient Descent for Adaptive Weights
Let $\theta$ represent the trainable parameters (e.g., in the affinity function $a_i(t)$). The online update is:
$$ \theta_{t+1} = \theta_t - \eta_t \nabla_\theta \mathcal{L}_{ACFE}(\theta_t; \mathbf{z}_t, x^*_t) $$

### 11.2 Adam Optimizer Configuration
For deep fusion architectures (GNNs), Adam is employed with parameters $\beta_1 = 0.9, \beta_2 = 0.999$, $\epsilon = 10^{-8}$. Momentums are maintained to stabilize fusion weights across noisy mini-batches.

### 11.3 Learning Rate Scheduling
A cosine annealing schedule with warm restarts is used to prevent the network from getting stuck in local minima during non-stationary concept drifts.
$$ \eta_t = \eta_{min} + \frac{1}{2}(\eta_{max} - \eta_{min}) \left(1 + \cos\left(\frac{T_{cur}}{T_i}\pi\right)\right) $$

### 11.4 Convergence and Regularization
- **Convergence:** Assured under standard stochastic approximation conditions (Robbins-Monro) assuming convexity in local neighborhoods.
- **Regularization:** $L_2$ penalty is applied to weights to prevent over-reliance on a single source: $\lambda_{reg} \|\theta\|_2^2$. Moreover, entropy regularization $-\lambda_H \mathcal{H}(\mathbf{w})$ is used to encourage exploration among sources.

---

## 12. Evaluation Metrics

### 12.1 Standard Classification Metrics
- **Accuracy:** The proportion of true results.
- **Precision, Recall, F1:** Standard measures for imbalanced datasets, computed via standard confusion matrix arithmetic.
- **AUC-ROC & AUC-PR:** Area under the Receiver Operating Characteristic and Precision-Recall curves.

### 12.2 Calibration & Uncertainty Metrics
- **ECE / MCE:** Detailed in section 6.4.
- **Brier Score:** Detailed in section 10.2.
- **Uncertainty Sharpness:** The concentration of the predictive distribution, defined as the inverse of the predictive entropy or predictive variance.
- **Proper Scoring Rules:** Any rule $S(P, Q)$ where the expected score is minimized iff $P = Q$. ACFE relies on NLL, Brier, and CRPS.

### 12.3 System Performance Metrics
- **Latency (p50, p95, p99):** The time from receiving observations $\mathbf{z}_t$ to outputting the fused confidence, measured at the 50th, 95th, and 99th percentiles.
- **Throughput:** Processed fusion events per second.
- **Memory footprint:** The RAM required to store historical states (e.g., running statistics for normalization, EMA variables).

---
*End of Document. This mathematical foundation guarantees that ACFE remains theoretically rigorous, numerically stable, and resilient against pathological source behaviors in dynamic, non-stationary environments.*
