# ml/recommendation.py

def calculate_recommendation_score(hospital_service, max_budget=None, max_distance=None):
    """
    Score formula based on:
    - Price weight (40%)
    - Rating weight (35%)
    - Distance weight (25%)
    """
    price = hospital_service.get('price_inr', 0)
    rating = hospital_service.get('rating', 3.0)
    distance = hospital_service.get('distance', 5.0) or 5.0

    # Budget filter check
    if max_budget and price > float(max_budget):
        return -1  # Budget se bahar

    # Distance score (Jitna paas, utna zyada score - max 10km scale)
    distance_score = max(0, (10 - min(distance, 10)) / 10) * 25

    # Rating score (5 star scale -> 35 points)
    rating_score = (rating / 5.0) * 35

    # Price score (Cheaper is better)
    price_score = max(0, 1000 - price) / 1000 * 40

    total_score = round(distance_score + rating_score + price_score, 2)
    return total_score

def get_best_recommendation(hospital_list, max_budget=None):
    scored_list = []
    for h in hospital_list:
        score = calculate_recommendation_score(h, max_budget)
        if score >= 0:
            item = dict(h)
            item['score'] = score
            scored_list.append(item)
    
    # Highest score first
    scored_list.sort(key=lambda x: x['score'], reverse=True)
    return scored_list