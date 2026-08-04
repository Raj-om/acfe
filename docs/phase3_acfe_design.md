# Phase 3 Adaptive Confidence Fusion Engine (ACFE) Research Design

**Author**: Principal Research Scientist
**Date**: August 3, 2026
**Status**: Phase 3 Algorithm Design Document

## Abstract

This document presents the rigorous algorithmic design for Phase 3 of the Adaptive Confidence Fusion Engine (ACFE). The ACFE addresses the fundamental challenge of combining conflicting, dynamically varying uncertainty estimates from heterogeneous sensor streams in high-stakes environments. The architecture is decomposed into four primary sub-components: ACFE-Core (a Bayesian-Dempster-Shafer hybrid), ACFE-Temporal (Kalman-augmented confidence tracking), ACFE-Graph (GNN-based dependency modeling), and ACFE-XAI (Integrated attribution). This document formalizes the mathematical underpinnings, computational complexity, robustness properties, and theoretical convergence for each component, while carefully delineating established techniques from proposed extensions.

---

## 1. Introduction and Scope

The objective of Phase 3 ACFE is to move beyond static, single-point fusion mechanisms to an adaptive, temporally coherent, and explainable fusion framework. 

**Constraints on Claims**:
*   *Established Techniques*: Bayesian Inference, Dempster-Shafer (DS) evidence theory, Extended Kalman Filters (EKF), and basic Graph Neural Networks (GNNs).
*   *Proposed Extensions*: Dynamic reliability weighting mapping Bayesian priors to DS basic probability assignments, time-varying process noise in confidence state-spaces, and attribution-aware message passing. These are extensions formulated for this project and undergo empirical validation in Phase 4.
*   *Speculative Ideas*: Real-time continuous SHAP approximation inside the GNN message-passing layer is considered highly speculative and marked as such throughout the text.

---

## 2. ACFE-Core: Adaptive Bayesian-DS Hybrid with Dynamic Reliability Weighting

### 2.1. Intuition and Motivation

Traditional Bayesian fusion struggles with epistemic uncertainty (unknown unknowns) and highly conflicting evidence. Dempster-Shafer (DS) theory handles ignorance and conflict well via the power set of hypotheses but lacks the continuous learning capabilities of Bayesian priors. ACFE-Core proposes a hybrid: using a Bayesian framework to dynamically estimate sensor reliability, which then scales the Basic Probability Assignments (BPAs) in a generalized DS fusion rule.

### 2.2. Mathematical Derivation and Variable Definitions

Let $\Omega = \{\omega_1, \dots, \omega_N\}$ be the frame of discernment (the set of mutually exclusive hypotheses).
Let $S = \{s_1, \dots, s_K\}$ be the set of sensors.

**Variables**:
*   $m_i(A, t)$: The Basic Probability Assignment (BPA) from sensor $s_i$ for proposition $A \subseteq \Omega$ at time $t$. $\sum_{A \subseteq \Omega} m_i(A, t) = 1$.
*   $r_i(t) \in [0, 1]$: The dynamic reliability weight of sensor $s_i$ at time $t$.
*   $\theta_i$: The hidden parameter representing the true long-term reliability of sensor $i$.
*   $D(t)$: The observed data/evidence up to time $t$.

**Known Technique**: Standard DS discounting rule. A discounted BPA $\tilde{m}_i$ based on a static reliability $r_i$ is defined as:
$$ \tilde{m}_i(A, t) = r_i \cdot m_i(A, t) \quad \forall A \subset \Omega $$
$$ \tilde{m}_i(\Omega, t) = 1 - r_i + r_i \cdot m_i(\Omega, t) $$

**Proposed Extension**: Dynamic Reliability Weighting.
We model $r_i(t)$ as a random variable drawn from a Beta distribution whose parameters are updated via Bayesian inference based on the historical conflict between sensor $i$'s predictions and the consensus.

Let the consensus at time $t-1$ be $C(t-1)$. We define a conformity score $c_i(t) \in [0, 1]$ comparing $m_i(t)$ and $C(t-1)$.
The Bayesian update for the parameters $\alpha_i, \beta_i$ of the Beta distribution is proposed as:
$$ \alpha_i(t) = \lambda \alpha_i(t-1) + c_i(t) $$
$$ \beta_i(t) = \lambda \beta_i(t-1) + (1 - c_i(t)) $$
where $\lambda \in (0, 1]$ is a forgetting factor. The expected reliability is then $r_i(t) = \frac{\alpha_i(t)}{\alpha_i(t) + \beta_i(t)}$.

### 2.3. Recursive Update Rule

The final fusion utilizes the modified Dempster's rule of combination over the dynamically discounted BPAs:
$$ m_{fused}(A, t) = \left( \tilde{m}_1 \oplus \tilde{m}_2 \oplus \dots \oplus \tilde{m}_K \right)(A, t) $$
$$ = \frac{1}{1 - K_{conflict}} \sum_{\cap A_j = A} \prod_{i=1}^K \tilde{m}_i(A_j, t) $$
where $K_{conflict} = \sum_{\cap A_j = \emptyset} \prod_{i=1}^K \tilde{m}_i(A_j, t)$.

### 2.4. Initialization Procedure

1. Initialize $\alpha_i(0) = \alpha_0, \beta_i(0) = \beta_0$ (e.g., uninformed prior $\alpha_0=1, \beta_0=1$).
2. For the first $T_{warmup}$ steps, use simple average fusion to generate the consensus $C(t)$ to stabilize the conformity scores $c_i(t)$.

### 2.5. Computational Complexity Analysis

*   **Space**: $O(K \cdot 2^{|\Omega|})$ to store BPAs for each sensor.
*   **Time**: Dempster's rule is famously $\#P$-complete, running in $O(K \cdot 2^{|\Omega|})$.
*   *Justification*: We assume $|\Omega|$ is small (e.g., $|\Omega| \le 10$). If $|\Omega|$ is large, approximations (like focusing only on focal elements with mass $> \epsilon$) must be employed.

### 2.6. Robustness Properties and Failure Cases

*   **Robustness**: The dynamic discounting $r_i(t)$ inherently bounds the influence of a suddenly compromised sensor. The forgetting factor $\lambda$ allows recovery if the sensor is repaired.
*   **Failure Case 1 (Zeno's paradox of conflict)**: If all sensors conflict simultaneously, $K_{conflict} \to 1$, and the denominator causes numerical instability.
    *   *Mitigation*: Use Yager's modified rule, which assigns conflict mass to the universal set $\Omega$ instead of normalizing.
*   **Failure Case 2 (Echo Chamber)**: If a correlated group of erroneous sensors dominates the early consensus, they will discount the correct sensors.
    *   *Mitigation*: Add ground-truth injection points when available to force hard resets of $\alpha, \beta$.

### 2.7. Pseudocode

```python
def ACFE_Core_Update(BPAs_t, alphas_prev, betas_prev, consensus_prev, lambda_f):
    """
    BPAs_t: List of dicts, [{A: mass, ...}] for each sensor
    """
    K = len(BPAs_t)
    r_t = zeros(K)
    discounted_BPAs = []
    
    for i in range(K):
        # 1. Compute conformity (e.g., Jousselme distance inverse)
        c_i = compute_conformity(BPAs_t[i], consensus_prev)
        
        # 2. Bayesian Update
        alphas_prev[i] = lambda_f * alphas_prev[i] + c_i
        betas_prev[i] = lambda_f * betas_prev[i] + (1 - c_i)
        r_t[i] = alphas_prev[i] / (alphas_prev[i] + betas_prev[i])
        
        # 3. Discounting
        m_tilde = discount_BPA(BPAs_t[i], r_t[i])
        discounted_BPAs.append(m_tilde)
        
    # 4. DS Fusion
    fused_BPA = Dempster_Rule(discounted_BPAs)
    
    return fused_BPA, alphas_prev, betas_prev
```

---

## 3. ACFE-Temporal: Kalman-Augmented Confidence Tracking

### 3.1. Overview and State Space Extension

While ACFE-Core handles instantaneous conflict, confidence metrics often exhibit temporal inertia. ACFE-Temporal uses a Kalman Filter to track the *latent confidence state* of each sensor, filtering out high-frequency noise in confidence reports.

**Known Technique**: Kalman Filtering for state estimation.
**Proposed Extension**: Applying KF not to the physical state of the environment, but to the multi-dimensional confidence vector reported by the sensor itself.

### 3.2. State Vector Definition

Let $x_i^{(c)}(t) \in \mathbb{R}^M$ be the true, latent confidence state vector of sensor $i$ (where $M$ might represent confidences across different feature dimensions).
Let $z_i^{(c)}(t) \in \mathbb{R}^M$ be the raw, noisy confidence reported by sensor $i$.

### 3.3. Models

**Process Model (Reliability Drift)**:
$$ x_i^{(c)}(t) = F x_i^{(c)}(t-1) + w(t) $$
where $w(t) \sim \mathcal{N}(0, Q(t))$. 
*Proposed Extension*: The process noise covariance $Q(t)$ is modeled as a function of environmental volatility (e.g., higher volatility = faster drift in true confidence).

**Measurement Model (Confidence Signals)**:
$$ z_i^{(c)}(t) = H x_i^{(c)}(t) + v(t) $$
where $v(t) \sim \mathcal{N}(0, R(t))$.

### 3.4. Unscented Variant Justification

If the mapping from physical environment changes to confidence drift is highly non-linear, an Unscented Kalman Filter (UKF) is justified over the Extended Kalman Filter (EKF) because it avoids calculating Jacobians, which are often undefined for black-box neural network confidence outputs.

### 3.5. Computational Complexity and Failure Cases

*   **Complexity**: $O(M^3)$ per sensor per timestep due to matrix inversion in the Kalman gain calculation. Since $M$ (dimension of confidence vector) is small, this is highly efficient.
*   **Failure Case**: Mis-specified $Q$ and $R$ matrices leading to filter divergence. If $R$ is set too low, the filter chases noise.
    *   *Mitigation*: Adaptive covariance estimation (e.g., using moving windows of measurement residuals).

---

## 4. ACFE-Graph: GNN-based Inter-Sensor Dependency Modeling

### 4.1. Graph Construction

Sensors are rarely independent. ACFE-Graph models spatial and modal correlations.
Let $G = (V, E)$ be the sensor graph. Node $v_i \in V$ corresponds to sensor $i$. Edge $e_{ij} \in E$ exists if sensors $i$ and $j$ are correlated (e.g., overlapping field of view, or same physical modality).

### 4.2. Features and Message Passing Formulation

**Node Features**: $h_i^{(0)} = [x_i^{(pred)}, z_i^{(c)}, r_i]$ (the prediction, raw confidence, and Bayesian reliability).
**Edge Features**: $e_{ij}$ (distance, modality similarity).

**Proposed Extension**: Confidence-Attentive Message Passing.
We utilize an attention mechanism where the attention weight $\alpha_{ij}$ is modulated explicitly by the source node's reliability $r_j$.

$$ h_i^{(l+1)} = \sigma \left( \sum_{j \in \mathcal{N}(i) \cup \{i\}} \alpha_{ij}^{(l)} W^{(l)} h_j^{(l)} \right) $$

where the attention coefficient is calculated as:
$$ e_{ij} = \text{LeakyReLU} \left( a^T [W h_i || W h_j] \cdot \Phi(r_j) \right) $$
$$ \alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k \in \mathcal{N}(i)} \exp(e_{ik})} $$
where $\Phi$ is a gating function emphasizing highly reliable neighbors.

### 4.3. Training and Inference Time

*   **Training**: Offline via supervised contrastive learning or end-to-end if ground truth labels are available.
*   **Inference Time**: $O(|E| \cdot d^2)$ where $d$ is feature dimensionality. Highly scalable for sparse graphs.
*   **Failure Case**: Out-of-distribution (OOD) topological changes (e.g., a sensor moves).
    *   *Mitigation*: Dynamic graph construction using k-NN in feature space instead of fixed physical topology.

---

## 5. ACFE-XAI: Integrated Attribution for Fusion Decisions

### 5.1. SHAP Value Integration

To trust the fusion engine, operators must know *why* a specific confidence level was output. We utilize Shapley Additive Explanations (SHAP).

Let $f(X)$ be the unified ACFE fusion function. $X = \{x_1, \dots, x_K\}$ are the sensor inputs.
The attribution for sensor $i$ is:
$$ \phi_i = \sum_{S \subseteq X \setminus \{i\}} \frac{|S|! (K - |S| - 1)!}{K!} [f(S \cup \{i\}) - f(S)] $$

### 5.2. Counterfactual Generation and Limitations

*   **Counterfactuals**: "If Sensor 2 had a confidence of 0.9 instead of 0.2, the fused confidence would rise by 0.4."
*   **Speculative Idea**: To avoid the $O(2^K)$ complexity of exact SHAP at runtime, we propose embedding a small attribution-distillation network parallel to the GNN that predicts SHAP values directly from graph embeddings. This is speculative and requires validation to ensure the surrogate doesn't hallucinate attributions.
*   **Limitations**: Additive feature attribution assumes independence of features to some degree; high correlations in ACFE-Graph may cause SHAP to distribute credit counter-intuitively.

---

## 6. Unified ACFE Framework Architecture

The full pipeline operates sequentially at each timestep $t$:

1.  **Sensor Input**: $K$ sensors provide predictions and raw confidences $z_1^{(c)}, \dots, z_K^{(c)}$.
2.  **Temporal Filtering (ACFE-Temporal)**: Raw confidences are passed through the Kalman filter to obtain smoothed latent confidences $x_1^{(c)}, \dots, x_K^{(c)}$.
3.  **Reliability Estimation (ACFE-Core)**: Conformity is assessed against the previous consensus. Beta distributions are updated to output dynamic reliabilities $r_1, \dots, r_K$.
4.  **Graph Fusion (ACFE-Graph)**: Predictions, smoothed confidences, and reliabilities are passed into the GNN to perform spatial correlation-aware aggregation.
5.  **Evidence Combination (ACFE-Core DS)**: The GNN embeddings are mapped to BPAs, discounted by $r_i$, and fused via Dempster's rule for the final decision.
6.  **Attribution (ACFE-XAI)**: SHAP surrogates generate the explanation vector $\Phi$.

### 6.1. Comparison to Baselines

| Feature | Naive Bayesian | Pure DS Theory | Kalman Fusion | Ensemble Averaging | **Unified ACFE** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Handles Ignorance** | No (forces prob) | Yes | No | No | **Yes** (via DS) |
| **Continuous Learning** | Yes | No (static mass) | Yes (state) | No | **Yes** (Beta priors) |
| **Temporal Smoothing** | No | No | Yes | No | **Yes** (ACFE-Temp) |
| **Spatial Correlation**| Difficult | No | No | No | **Yes** (ACFE-Graph)|
| **Explainability** | Probabilistic | Mass traces | Innovation | Weights | **Yes** (SHAP XAI) |

---

## 7. Convergence Analysis

For ACFE-Core, assuming the environment is locally stationary (true reliabilities $\theta_i$ are constant over a window) and $\lambda < 1$:

The expected value of the updated reliability is:
$$ \mathbb{E}[r_i(t)] = \mathbb{E}\left[ \frac{\lambda \alpha_{i, t-1} + c_i(t)}{\lambda \alpha_{i, t-1} + \lambda \beta_{i, t-1} + 1} \right] $$

As $t \to \infty$, the geometric series formed by the forgetting factor $\lambda$ converges. The sufficient statistics $\alpha_i, \beta_i$ converge in expectation to $\frac{\bar{c}_i}{1-\lambda}$ and $\frac{1-\bar{c}_i}{1-\lambda}$ respectively, where $\bar{c}_i$ is the true expected conformity. Thus, $r_i(t) \to \bar{c}_i$, demonstrating that the dynamic reliability weight converges exactly to the long-term empirical conformity of the sensor, neutralizing transient anomalies.

---
*End of Design Document*
