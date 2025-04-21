def detect_bias(explanation: dict, threshold: float = 0.5):
    sorted_items = sorted(explanation.items(), key=lambda x: abs(x[1]), reverse=True)
    top_feature, top_value = sorted_items[0]
    is_biased = abs(top_value) > threshold
    return {"biased": is_biased, "top_feature": top_feature, "impact": top_value}