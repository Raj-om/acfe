import numpy as np

class UncertaintyQuantifier:
    """
    UncertaintyQuantifier (MC Dropout, ensemble)
    """
    def __init__(self, num_samples: int = 100):
        self.num_samples = num_samples
        
    def mc_dropout_uncertainty(self, model, x, adj, num_samples=None):
        """
        Estimate epistemic uncertainty using Monte Carlo Dropout.
        model must be a PyTorch model with dropout enabled.
        """
        import torch
        num_samples = num_samples or self.num_samples
        model.train() # Enable dropout
        
        predictions = []
        with torch.no_grad():
            for _ in range(num_samples):
                out = model(x, adj)
                predictions.append(out.cpu().numpy())
                
        predictions = np.array(predictions)
        
        # Mean prediction
        mean_pred = np.mean(predictions, axis=0)
        
        # Variance (Uncertainty)
        variance = np.var(predictions, axis=0)
        
        return mean_pred, variance
        
    def ensemble_uncertainty(self, predictions_list: list):
        """
        Estimate uncertainty from an ensemble of models.
        predictions_list: list of np.array predictions from different models.
        """
        preds = np.array(predictions_list)
        mean_pred = np.mean(preds, axis=0)
        variance = np.var(preds, axis=0)
        return mean_pred, variance
