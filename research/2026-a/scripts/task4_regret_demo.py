"""Synthetic structural example only; no real cities or student observations."""
import json
from math import sqrt
from pathlib import Path

BASELINE_WEIGHT = 0.75

CITIES = {
    "Synthetic-Specialist-A": (0.98, 0.45),
    "Synthetic-Balanced": (0.75, 0.75),
    "Synthetic-Specialist-B": (0.55, 0.94),
    "Synthetic-Dominated": (0.40, 0.40),
}


def score(z, w):
    plus = sqrt(w * (1-z[0])**2 + (1-w) * (1-z[1])**2)
    minus = sqrt(w * z[0]**2 + (1-w) * z[1]**2)
    return minus / (plus + minus)


def evaluate(grid):
    result = {}
    for city, z in CITIES.items():
        regrets = [max(score(h, w) for h in CITIES.values()) - score(z, w)
                   for w in grid]
        worst = max(range(len(grid)), key=regrets.__getitem__)
        result[city] = {
            "baseline_score": score(z, BASELINE_WEIGHT),
            "maximum_tested_regret": regrets[worst],
            "worst_tested_first_dimension_weight": grid[worst],
        }
    return result


def main():
    # Uniform finite grid is a declared exploration design, not a population model.
    grid = [0.2 + 0.6*k/600 for k in range(601)]
    rows = evaluate(grid)
    baseline = sorted(rows, key=lambda n: rows[n]["baseline_score"], reverse=True)
    revised = sorted(rows, key=lambda n: rows[n]["maximum_tested_regret"])
    # Offset grid checks the recommendation between design-grid points.
    offset = evaluate([0.2 + 0.6*(k+0.5)/600 for k in range(600)])
    offset_winner = min(offset, key=lambda n: offset[n]["maximum_tested_regret"])
    # Meaningful structural checks: dominance and regret normalization.
    assert all(score(CITIES["Synthetic-Balanced"], w) >
               score(CITIES["Synthetic-Dominated"], w) for w in grid)
    assert all(0 <= r["maximum_tested_regret"] <= 1 for r in rows.values())
    result = {
        "status": "SYNTHETIC ONLY; finite tested scenarios, no global certificate",
        "baseline_weights": [BASELINE_WEIGHT, 1-BASELINE_WEIGHT],
        "first_dimension_weight_range": [0.2, 0.8],
        "scenario_count": len(grid),
        "cities": rows,
        "baseline_ranking": baseline,
        "revised_ranking": revised,
        "offset_grid_winner": offset_winner,
        "offset_grid_agrees": offset_winner == revised[0],
    }
    output = Path(__file__).resolve().parents[1] / "design/task4_regret_demo_results.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
