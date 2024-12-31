#!/usr/bin/env python

from pathlib import Path
import pandas as pd

pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 10)
pd.set_option("display.width", 1000)

root_dir = Path(__file__).parent

v3_result_fp = root_dir / 'v3_outputs/final_assignments.csv.bz2'
v3_result_df = pd.read_csv(v3_result_fp, header=0, index_col=0, compression='bz2')

# Drop references
v3_result_df = v3_result_df[~v3_result_df['Reference']]

# Drop unused (by ICTV challenge) columns
unused_cols = ['RefSeqID', 'Proteins', 'Size (Kb)', 'network']
ref_cols = [col for col in v3_result_df.columns if 'Reference' in col]
unused_cols.extend(ref_cols)

v3_result_df = v3_result_df[[col for col in v3_result_df.columns.tolist() if col not in unused_cols]]

# Rename columns prior to unification
renamer = {
    'GenomeName': 'SequenceID',
    'realm (prediction)': 'Realm (-viria)',
    'phylum (prediction)': 'Phylum (-viricota)',
    'class (prediction)': 'Class (-viricetes)',
    'order (prediction)': 'Order (-virales)',
    'family (prediction)': 'Family (-viridae)',
    'subfamily (prediction)': 'Subfamily (-virinae)',
    'genus (prediction)': 'Genus (-virus)'
}

v3_result_df = v3_result_df.rename(columns=renamer)

template_fp = root_dir / 'results/classification_template.csv'
template_df = pd.read_csv(template_fp, header=0, index_col=None)

# Remove first row
template_df = template_df.iloc[1:]

# Merge
results_df = pd.concat([template_df, v3_result_df], ignore_index=True)

# Reorder cuz it's annoying
results_df = results_df[template_df.columns]

# Save
results_df.to_csv(root_dir / 'results/classification_results.csv', index=False)
