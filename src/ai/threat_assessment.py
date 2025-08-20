def threat_score(target: dict) -> float:
    # Basit kural: daha büyük bbox + daha yüksek güven = daha yüksek tehdit
    x1,y1,x2,y2 = target["bbox"]
    area = (x2-x1)*(y2-y1)
    return 0.7*target.get("confidence",0.0) + 0.3*(area/10000.0)
