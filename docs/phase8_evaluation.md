# Phase 8: Experimental Validation Framework for the Adaptive Confidence Fusion Engine (ACFE)

## 1. Evaluation Philosophy

### Why Evaluation Matters for Confidence Fusion
Confidence fusion in mission-critical applications requires extreme reliability. A simple accuracy metric is insufficient; the system must be rigorously evaluated on its ability to accurately estimate uncertainty, handle conflicting information, and degrade gracefully under adversarial or noisy conditions. Confidence fusion bridges the gap between predictive performance and trusted decision-making. 

### Threat to Validity Analysis
- **Internal Validity:** The risk of information leakage between train and test sets, especially in temporally correlated sensor data. Mitigated via strict chronological splitting and blocked cross-validation.
- **External Validity:** The generalizability of the ACFE framework across different modalities (e.g., healthcare vs. aerospace). Addressed by evaluating on diverse public datasets spanning multiple domains.
- **Construct Validity:** Whether the chosen metrics accurately reflect real-world utility. Addressed by incorporating Expected Calibration Error (ECE) and Brier Score alongside standard classification metrics.

### Statistical Significance Requirements
Given the stochastic nature of some baselines and the necessity for robust claims, all experiments will be conducted over 10 random seeds. Statistical significance will be established using the Wilcoxon signed-rank test for paired comparisons and the Friedman test for multiple comparisons across datasets, with a strict alpha level of 0.05.

---

## 2. Public Datasets

To ensure reproducibility and broad applicability, the ACFE will be evaluated on the following datasets:

### 1. MIMIC-III (Medical Information Mart for Intensive Care)
- **Source:** https://physionet.org/content/mimiciii/
- **Size:** Data from over 40,000 intensive care unit stays.
- **Format:** CSV files (relational database format) containing time-series vitals, lab results, and clinical notes.
- **Relevance:** Represents a multi-sensor analog with high clinical uncertainty, missing data, and conflicting indicators (e.g., heart rate vs. blood pressure anomalies).

### 2. UCR Time Series Classification Archive
- **Source:** https://www.cs.ucr.edu/~eamonn/time_series_data_2018/
- **Size:** 128 distinct time series datasets.
- **Format:** TXT/CSV files with pre-defined train/test splits.
- **Relevance:** Provides diverse temporal sensor signals to evaluate the ACFE-Temporal component's ability to fuse dynamic confidence over time.

### 3. NASA FIRMS (Fire Information for Resource Management System)
- **Source:** https://firms.modaps.eosdis.nasa.gov/
- **Size:** Global daily fire detection data (millions of records).
- **Format:** CSV/SHP containing spatial coordinates, brightness, and confidence scores from MODIS and VIIRS instruments.
- **Relevance:** Excellent for multi-source fusion where different satellite sensors provide varying confidence levels on geospatial anomalies.

### 4. USGS Earthquake Hazards Program
- **Source:** https://earthquake.usgs.gov/data/
- **Size:** Millions of seismic events.
- **Format:** GeoJSON, CSV.
- **Relevance:** Seismic multi-sensor arrays provide correlated, noisy temporal data perfect for evaluating the Kalman-augmented confidence tracking.

### 5. OpenStreetMap + Overture Maps
- **Source:** https://overturemaps.org/
- **Size:** Global scale geospatial data.
- **Format:** GeoParquet / JSON.
- **Relevance:** Geospatial fusion requires resolving conflicting ontological classifications and spatial boundaries.

### 6. IEEE DataPort: Infrastructure Monitoring
- **Source:** https://ieee-dataport.org/
- **Size:** Varies (e.g., bridge structural health monitoring).
- **Format:** HDF5/CSV.
- **Relevance:** High-frequency, noisy sensor data ideal for evaluating graph-based dependency modeling (ACFE-Graph).

### 7. Kaggle: Anomaly Detection Datasets (e.g., Credit Card Fraud)
- **Source:** https://www.kaggle.com/mlg-ulb/creditcardfraud
- **Size:** ~285,000 transactions.
- **Format:** CSV.
- **Relevance:** Highly imbalanced data testing the robustness of DS-theory conflict resolution.

### 8. NOAA Weather Sensor Datasets
- **Source:** https://www.ncdc.noaa.gov/
- **Size:** Terabytes of historical climatological data.
- **Format:** NetCDF/CSV.
- **Relevance:** Multi-modal sensor networks (temperature, pressure, humidity) with known physical dependencies, suitable for unified ACFE testing.

---

## 3. Baselines to Compare

### 1. Simple Average Fusion
- **Description:** Arithmetic mean of confidence scores from all sources.
- **Reference:** Kittler et al., "On combining classifiers", IEEE TPAMI 1998.
- **Expected Performance:** Good baseline for non-conflicting, independent sources, but fails under high conflict.

### 2. Weighted Average (Static Weights)
- **Description:** Weighted sum of scores, weights optimized on validation set.
- **Reference:** Standard ensemble method.
- **Expected Performance:** Better than simple average but lacks adaptive capability for dynamic sensor degradation.

### 3. Bayesian Fusion
- **Description:** Updates belief using Bayes' theorem, assuming conditional independence.
- **Reference:** Pearl, "Probabilistic Reasoning in Intelligent Systems".
- **Expected Performance:** Strong mathematically but overconfident when the conditional independence assumption is violated.

### 4. Dempster-Shafer Theory (Standard)
- **Description:** Evidential reasoning combining mass functions using Dempster's rule.
- **Reference:** Shafer, "A Mathematical Theory of Evidence".
- **Expected Performance:** Handles uncertainty well but degrades (Zadeh's paradox) under extreme conflict.

### 5. Kalman Filter (Confidence Tracking)
- **Description:** Standard linear Kalman filter applied to confidence scores over time.
- **Reference:** Kalman, 1960.
- **Expected Performance:** Smooths temporal noise but cannot resolve semantic conflicts between discrete sources.

### 6. Deep Ensemble
- **Description:** Multiple neural networks trained with different initializations.
- **Reference:** Lakshminarayanan et al., NeurIPS 2017.
- **Expected Performance:** Excellent uncertainty calibration, but computationally expensive and lacks explicit sensor dependency modeling.

### 7. ACFE-Core (Proposed)
- **Description:** The hybrid Bayesian-DS module without temporal or graph components.
- **Expected Performance:** Superior to pure Bayesian or pure DS in resolving high-conflict scenarios.

### 8. ACFE-Full (Proposed)
- **Description:** The complete architecture integrating Bayesian-DS, Kalman temporal smoothing, and GNN dependency modeling.
- **Expected Performance:** State-of-the-art across all metrics, particularly ECE and conflict resolution in noisy environments.

---

## 4. Evaluation Metrics

### 1. Classification Metrics
- **Accuracy, Precision, Recall, F1-score**
- **Threshold:** F1 > 0.85 on balanced datasets.

### 2. AUC-ROC, AUC-PR
- **Interpretation:** Ability to rank true positives higher than false positives across all confidence thresholds.
- **Threshold:** AUC-ROC > 0.90, AUC-PR > 0.85 (for imbalanced data).

### 3. Expected Calibration Error (ECE)
- **Formula:** $ECE = \sum_{m=1}^{M} \frac{|B_m|}{n} |acc(B_m) - conf(B_m)|$
- **Interpretation:** Measures the alignment between predicted confidence and actual empirical accuracy.
- **Threshold:** ECE < 0.05.

### 4. Brier Score
- **Formula:** $BS = \frac{1}{N} \sum_{i=1}^{N} (f_i - o_i)^2$
- **Interpretation:** Mean squared error of probability forecasts.
- **Threshold:** BS < 0.10.

### 5. Latency (p50, p95, p99)
- **Interpretation:** Time required to fuse an event.
- **Threshold:** p99 < 50ms for real-time applicability.

### 6. Throughput
- **Interpretation:** Fused events per second.
- **Threshold:** > 10,000 events/sec on a single CPU thread.

### 7. Memory Usage
- **Interpretation:** RAM required during inference.
- **Threshold:** < 500 MB footprint.

### 8. Uncertainty Sharpness
- **Interpretation:** Variance of the predicted confidence distributions.
- **Threshold:** Maximized sharpness subject to calibration constraints.

### 9. Negative Log-Likelihood (NLL)
- **Interpretation:** Standard proper scoring rule for probabilistic models.

---

## 5. Experimental Protocol

- **Split Strategy:** 70% Train, 15% Validation, 15% Test. Time-series data uses chronological splitting to prevent future-leakage.
- **Cross-Validation:** 5-fold blocked cross-validation for non-temporal data; TimeSeriesSplit for temporal data.
- **Hyperparameter Tuning:** Optuna framework using TPE (Tree-structured Parzen Estimator), targeting ECE optimization, bounded to 50 trials per dataset.
- **Statistical Tests:** Wilcoxon signed-rank test (alpha=0.05) to compare ACFE-Full against the best baseline.
- **Effect Size:** Cohen's d to measure the standardized difference in means.

---

## 6. Expected Results Template

| Method | MIMIC-III (F1/ECE) | FIRMS (F1/ECE) | USGS (F1/ECE) | Latency (p99) |
|---|---|---|---|---|
| Simple Avg | 0.72 / 0.15 | 0.81 / 0.12 | 0.75 / 0.18 | **2ms** |
| Bayesian | 0.75 / 0.18 | 0.83 / 0.14 | 0.78 / 0.20 | 5ms |
| DS Theory | 0.76 / 0.10 | 0.82 / 0.09 | 0.77 / 0.12 | 15ms |
| Deep Ens. | 0.82 / 0.06 | 0.88 / 0.05 | 0.84 / 0.08 | 150ms |
| ACFE-Core | 0.80 / 0.05 | 0.87 / 0.04 | 0.82 / 0.06 | 12ms |
| **ACFE-Full**| **0.85 / 0.02** | **0.91 / 0.02** | **0.88 / 0.03** | 25ms |

### Ablation Study Design
Evaluate performance drop when removing:
1. GNN dependency modeling (assume independent sources).
2. Kalman temporal smoothing (treat time steps independently).
3. DS conflict resolution (use pure Bayesian).

### Robustness Experiment
- **Noise Injection:** Inject Gaussian noise to sensor inputs at 10%, 20%, 50% SNR.
- **Sensor Dropout:** Randomly drop 10-40% of sensor streams during test time to evaluate graceful degradation.

---

## 7. Evaluation Code Skeleton

```python
# experiment_runner.py - complete skeleton
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, roc_auc_score, brier_score_loss
from sklearn.model_selection import TimeSeriesSplit
import optuna
import time
from typing import Dict, List, Any

def calculate_ece(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> float:
    \"\"\"Calculate Expected Calibration Error.\"\"\"
    bin_limits = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        bin_idx = (y_prob >= bin_limits[i]) & (y_prob < bin_limits[i+1])
        if np.any(bin_idx):
            acc = np.mean(y_true[bin_idx] == (y_prob[bin_idx] > 0.5))
            conf = np.mean(y_prob[bin_idx])
            ece += (np.sum(bin_idx) / len(y_true)) * np.abs(acc - conf)
    return ece

def run_experiment(dataset_name: str, method: Any, data: Dict) -> Dict:
    \"\"\"Runs a single experiment on a dataset using the specified method.\"\"\"
    X_train, y_train = data['train']
    X_val, y_val = data['val']
    X_test, y_test = data['test']
    
    # Timing
    start_time = time.time()
    method.fit(X_train, y_train, validation_data=(X_val, y_val))
    train_time = time.time() - start_time
    
    start_time = time.time()
    y_pred_prob = method.predict_proba(X_test)
    y_pred = (y_pred_prob > 0.5).astype(int)
    inference_time = time.time() - start_time
    
    # Metrics
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_prob)
    ece = calculate_ece(y_test, y_pred_prob)
    brier = brier_score_loss(y_test, y_pred_prob)
    
    latency_per_sample = (inference_time / len(X_test)) * 1000 # in ms
    
    return {
        'dataset': dataset_name,
        'method': method.__class__.__name__,
        'f1': f1,
        'roc_auc': roc_auc,
        'ece': ece,
        'brier': brier,
        'latency_ms': latency_per_sample,
        'train_time_s': train_time
    }

def main():
    datasets = ["MIMIC-III", "FIRMS", "USGS"]
    methods = []
    
    results = []
    
    for dataset in datasets:
        print(f"Loading {dataset}...")
        data = {'train': (np.random.rand(100,5), np.random.randint(0,2,100)),
                'val': (np.random.rand(20,5), np.random.randint(0,2,20)),
                'test': (np.random.rand(20,5), np.random.randint(0,2,20))}
        
        for method in methods:
            print(f"Running {method.__class__.__name__} on {dataset}...")
            # res = run_experiment(dataset, method, data)
            # results.append(res)
            
    print("Experiments completed.")

if __name__ == "__main__":
    main()
```
