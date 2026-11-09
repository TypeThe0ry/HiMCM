"""Sharp joint mean-minus-lower-tail gap in the retained historical aggregate set."""
from pathlib import Path
import hashlib
import json
import math
import subprocess
import numpy as np
from scipy.optimize import linprog

R = Path(__file__).resolve().parents[1]
P = Path('/data/projects/HiMCM-Overleaf')
O = R / 'results/task4_v158_joint_gap'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def tail(cells, alpha):
    target = alpha * sum(w for q, w in cells)
    left, value = target, 0.
    for q, w in sorted(cells):
        used = min(left, w)
        value += used * q
        left -= used
        if left <= 1e-8:
            return value / target, q
    raise AssertionError('Unfilled tail')


def joint_lp(q, w, free, alpha):
    # Independent convex epigraph: z, free utilities, one hinge per atom.
    n, k = len(q), len(free)
    mass = np.r_[w, free]
    N = mass.sum()
    c = np.r_[-1., free / N, mass / (alpha * N)]
    A, b = [], []
    for i in range(n + k):
        row = np.zeros(1 + k + n + k)
        row[0] = 1
        row[1 + k + i] = -1
        if i < n:
            rhs = q[i]
        else:
            row[1 + i - n] = -1
            rhs = 0
        A.append(row)
        b.append(rhs)
    solved = linprog(c, A_ub=A, b_ub=b,
                     bounds=[(0, 1)] * (1 + k) + [(0, None)] * (n + k), method='highs')
    assert solved.success, solved.message
    return solved.fun + np.dot(q, w) / N, solved.x


def main():
    O.mkdir(exist_ok=True)
    src = R / 'data/task4_v116_ibb/aggregate_results.json'
    source = json.loads(src.read_text())
    cells = [(math.exp(-float(t) / 30), row['weight'])
             for t, row in source['duration_histogram'].items()]
    q = np.array([x for x, w in cells])
    w = np.array([w for x, w in cells], dtype=float)
    W = w.sum()
    U = source['summary']['weight_unknown']
    B = source['optional_membership']['weight_total']
    Nmax = W + U + B
    old = json.loads((R / 'results/task4_v152_tail_access/summary.json').read_text())
    assert W == 499950 and Nmax == 681503
    rows, checks = [], 0
    rng = np.random.default_rng(158)
    for previous in old['lower_tail_rows']:
        a = previous['tail_fraction']
        observed_tail, threshold = tail(cells, a)
        gap = (sum(qi * wi for qi, wi in cells) - W * observed_tail) / Nmax
        witness = cells + [(threshold, U + B)]
        witness_tail, _ = tail(witness, a)
        witness_mean = sum(x * m for x, m in witness) / Nmax
        assert abs(witness_mean - witness_tail - gap) < 1e-12
        for included in np.linspace(0, B, 21):
            # Seven independently variable utility groups; valid relaxation.
            free = np.r_[np.full(7, U / 7), included]
            actual, solution = joint_lp(q, w, free, a)
            expected = gap * Nmax / (W + U + included)
            assert abs(actual - expected) < 1e-10
            assert actual >= gap - 1e-10
            checks += 1
        for _ in range(25):
            free = rng.dirichlet(np.ones(7)) * U
            completion = cells + list(zip(rng.uniform(0, 1, 7), free))
            completion += [(rng.uniform(), rng.uniform(0, B))]
            low, _ = tail(completion, a)
            mean = sum(x * m for x, m in completion) / sum(m for x, m in completion)
            assert mean - low >= gap - 1e-10
        rows.append(dict(alpha=a, prior_conservative_lower=previous['certified_mean_minus_tail_lower'],
                         sharp_joint_lower=gap, increase_over_old_certificate=gap-previous['certified_mean_minus_tail_lower'],
                         attaining_unknown_utility=threshold, attaining_minutes=-30*math.log(threshold),
                         witness_mean=witness_mean, witness_lower_tail=witness_tail,
                         optional_mass_included=B, denominator=Nmax))
    snapshot = json.loads((R / 'design/task4_user_v154_snapshot.json').read_text())
    for name, digest in snapshot['source_sha256'].items():
        assert sha(R/name) == digest, name
    # All manuscript files tracked before this iteration, rather than a selected subset.
    names = subprocess.check_output(['git', '-C', str(P), 'ls-files', '-z']).decode().split('\0')
    paper_hashes = {name:sha(P/name) for name in names if name}
    summary = dict(iteration='V158', primary='V154 unchanged', city='Istanbul', year=2012,
                   population=old['population'], provider_representation=source['provider'],
                   observed_weight=W, known_unknown_weight=U, optional_weight=B,
                   rows=rows, successful_joint_LPs=checks, random_completion_checks=75, seed=158,
                   scope='Sharp minimum over the retained aggregate uncertainty set; not current-city evidence or population CI',
                   source_sha256={str(src.relative_to(R)):sha(src)},
                   protected_scientific_files=len(snapshot['source_sha256']),
                   scientific_file_sha256=snapshot['source_sha256'],
                   generator_sha256=sha(Path(__file__)),
                   manuscript_files_unchanged_sha256=paper_hashes,
                   primary_pdf_sha256=sha(P/'drafts/task4_v154_paper.pdf'),
                   primary_data_admissions=0, primary_score_interval_width_reduction=0)
    (O/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(rows,indent=2))


if __name__ == '__main__':
    main()
