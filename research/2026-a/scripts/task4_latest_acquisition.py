"""Refresh acquisition certificates after actual Warsaw/Shanghai/Delhi evidence."""
from task4_delhi_school_revision import delhi_bounds
from task4_post_cape_acquisition import run
if __name__=='__main__':
    run(bounds_fn=delhi_bounds,reference='results/task4_v34_delhi_school/ranks.csv',
        scenario='participating_headcount',output='results/task4_v36_acquisition',
        prior_path='results/task4_v31_acquisition/minimum_measurements.csv',
        baseline='V34 delhi_bounds; V35 rejected estimates remain unknown',
        reference_version='v34',prior_version='v31')
