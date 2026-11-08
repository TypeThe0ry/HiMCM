"""Recompute known-cohort aggregates from an in-memory official CKAN projection.

Input: JSON list on stdin, sorted person rows with current-status/school type,
age, person weight, weekday, form status and 11 whole-journey endpoint fields.
Never write the input; stdout contains aggregated counts and weighted bounds.
This is a historical empirical calculation, not a design confidence interval.
"""
import json
import math
import re
import sys
from collections import defaultdict

WEEKDAYS = {'PAZARTESİ', 'SALI', 'ÇARŞAMBA', 'PERŞEMBE', 'CUMA'}
VALID_FORMS = {'DOLDURULMUŞ ANKET', 'EKSİK AMA GEÇERLİ ANKET'}


def minutes(value):
    match = re.fullmatch(r'(\d{1,2}):(\d{2}):(\d{2}) (ÖÖ|ÖS)', value or '')
    if not match:
        return None
    hour, minute, second = map(int, match.group(1, 2, 3))
    if not (1 <= hour <= 12 and minute < 60 and second < 60):
        return None
    return (hour % 12 + 12 * (match[4] == 'ÖS')) * 60 + minute + second / 60


def summarize(rows):
    reasons = defaultdict(lambda: {'n': 0, 'weight': 0.0})
    hist = defaultdict(lambda: {'n': 0, 'weight': 0.0})
    total = numerator = observed_weight = duration_sum = 0.0
    n = 0
    for row in rows:
        if row.get('ogrencimi') != 'EVET' or row.get('okuduguOkulunTuru') != 'LİSE':
            continue
        if not (str(row.get('yasi', '')).isdigit() and 14 <= int(row['yasi']) <= 18):
            continue
        w = float(str(row['kisi_agirlik']).replace(',', '.'))
        if not math.isfinite(w) or w <= 0:
            raise ValueError('Cannot form weighted bounds with missing/nonpositive person weight')
        n += 1
        total += w
        state, duration = 'no_home_school_trip', None
        first_school = next((k for k in range(1, 12) if row.get(f'varisYeri.{k}') == 'OKUL'), None)
        first_home_school = next((k for k in range(1, 12) if row.get(f'basyer.{k}') == 'EV' and row.get(f'varisYeri.{k}') == 'OKUL'), None)
        if first_home_school is not None:
            a = minutes(row.get(f'baslangicSaati.{first_home_school}'))
            b = minutes(row.get(f'varisSaati.{first_home_school}'))
            if a is None or b is None:
                state = 'invalid_clock'
            elif b <= a:
                state = 'nonpositive_or_rollover'
            else:
                state, duration = 'observed', b - a
        if row.get('seyahatGunu') not in WEEKDAYS:
            state, duration = 'missing_or_nonweekday', None
        if state == 'observed' and row.get('anketDurumBilgisi') not in VALID_FORMS:
            state, duration = 'incomplete_unvalidated_form', None
        if state == 'observed' and first_school != first_home_school:
            state, duration = 'earlier_school_trip_not_home', None
        reasons[state]['n'] += 1
        reasons[state]['weight'] += w
        if state == 'observed':
            hist[duration]['n'] += 1
            hist[duration]['weight'] += w
            observed_weight += w
            numerator += w * math.exp(-duration / 30)
            duration_sum += w * duration
    return {
        'n': n, 'weight_total': total, 'weight_observed': observed_weight,
        'weight_unknown': total - observed_weight,
        'utility_known_numerator': numerator,
        'utility_lower': numerator / total,
        'utility_upper': (numerator + total - observed_weight) / total,
        'conditional_observed_mean_minutes': duration_sum / observed_weight,
        'unknown_reasons': dict(reasons), 'duration_histogram': dict(hist),
    }


if __name__ == '__main__':
    print(json.dumps(summarize(json.load(sys.stdin)), ensure_ascii=False, indent=2))
