# ============================================================
#   MODUŁ 24627 — produkcyjny rdzeń decyzyjny SIMTRIX/DARTBIX
# ============================================================

import numpy as np

# ------------------------------------------------------------
# 1. Wagi 24627 (jeden cykl)
# ------------------------------------------------------------
WEIGHTS = np.array([2, 4, 6, 2, 7])

# ------------------------------------------------------------
# 2. Realne metryki systemowe
#    input_vector musi mieć 5 wartości:
#    [cpu_load, ram_load, agent_count, error_rate, throughput]
# ------------------------------------------------------------

def normalize_metrics(metrics):
    """
    Normalizuje metryki do zakresu 0–1.
    metrics: dict z kluczami:
        cpu_load (0–100)
        ram_load (0–100)
        agent_count (0–1000)
        error_rate (0–1)
        throughput (0–10000)
    """
    return np.array([
        metrics["cpu_load"] / 100,
        metrics["ram_load"] / 100,
        metrics["agent_count"] / 1000,
        metrics["error_rate"],            # już 0–1
        metrics["throughput"] / 10000
    ])

# ------------------------------------------------------------
# 3. LC-01 — realny silnik decyzyjny
# ------------------------------------------------------------

def LC01_decision(metrics):
    """
    metrics: dict z realnymi wartościami systemowymi
    """
    vec = normalize_metrics(metrics)
    score = np.dot(vec, WEIGHTS)

    # Progi liczone dynamicznie
    # 0–3: lekki ruch
    # 3–6: średnie obciążenie
    # 6–9: wysokie obciążenie
    # >9: przeciążenie
    if score < 3:
        return "Tryb: HARMONIA — system stabilny"
    elif score < 6:
        return "Tryb: STRUKTURA — optymalizacja procesów"
    elif score < 9:
        return "Tryb: INTEGRACJA — skalowanie i routing"
    else:
        return "Tryb: ŚWIADOMOŚĆ — analiza krytyczna, decyzje operatorskie"

# ------------------------------------------------------------
# 4. Test modułu
# ------------------------------------------------------------

if __name__ == "__main__":
    test_metrics = {
        "cpu_load": 45,
        "ram_load": 62,
        "agent_count": 120,
        "error_rate": 0.03,
        "throughput": 4200
    }

    print("LC-01:", LC01_decision(test_metrics))
