"""Recheck rankings after actual school-matched teacher and exam evidence."""
from task4_intake_v40 import run
if __name__=='__main__':
    run(folders=('task4_v41_toronto','task4_v41_phoenix_education'),
        output='results/task4_v41_matched_evidence',
        distinction='New same-school Phoenix teacher counts and Toronto test denominators are observed; incomplete city coverage and incompatible educational estimands prevent main-model replacement. Missing intervals remain unchanged.')
