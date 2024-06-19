import os
import argparse
import scanpy as sc
import numpy as np
import pandas as pd
from utils import get_basename_without_extension

parser = argparse.ArgumentParser(
    description="wrapper for concatenating the samples.")
parser.add_argument('-i', '--input', required=True, help='Path to directory containing files to be concatenated.')
parser.add_argument("-o", "--output", required = True, help = "The output h5ad file path.")

args = parser.parse_args()

adata_list = []

for h5_file_path in os.listdir(args.input):
    adata_path = os.path.join(args.input, h5_file_path)
    adata = sc.read(adata_path)
    sample_name = h5_file_path
    adata.obs['sample_name'] = get_basename_without_extension(h5_file_path).rsplit('_', 1)[0]
    adata.obs.index = adata.obs['sample_name'] + "_" + adata.obs.index
    adata.var_names_make_unique()
    adata_list.append(adata)
    
combined_adata = sc.concat(adata_list, axis = 0, join = 'outer')

# QC
combined_adata.var["mt"] = combined_adata.var_names.str.lower().str.startswith('mt-')
combined_adata.var["ribo"] = combined_adata.var_names.str.lower().str.startswith(("rps", "rpl"))
combined_adata.var["hb"] = combined_adata.var_names.str.lower().str.contains("^hb[^(p)]")
sc.pp.calculate_qc_metrics(
    combined_adata, qc_vars=["mt", "ribo"], inplace=True, log1p=True, percent_top = (50, 100)
)
combined_adata.write_h5ad(args.output)