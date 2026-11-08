"""Summarize published Table 4 school means; no individual coordinates used."""
import csv
from pathlib import Path

rows = list(csv.DictReader((Path(__file__).parent / 'published_school_durations.csv').open()))
assert len(rows) == 10
assert sum(int(r['retained_pedestrian_trajectories']) for r in rows) == 83
barcelona = [r for r in rows if r['school_municipality'] == 'Barcelona']
n = sum(int(r['retained_pedestrian_trajectories']) for r in barcelona)
assert len(barcelona) == 8 and n == 48
means = {}
for column in ('mean_before_privacy_seconds', 'mean_after_privacy_seconds'):
    means[column] = sum(int(r['retained_pedestrian_trajectories']) * float(r[column]) for r in barcelona) / n
    print(f'{column}: {means[column]:.4f} seconds; {means[column]/60:.4f} minutes')
print(f'Privacy truncation difference: {means["mean_before_privacy_seconds"] - means["mean_after_privacy_seconds"]:.4f} seconds')
print('Scope: 48 retained pedestrian trajectories at 8 Barcelona schools; no city-population inference.')
