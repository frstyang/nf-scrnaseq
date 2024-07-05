#!/usr/bin/env python
import argparse
import scanpy as sc
import celltypist
from celltypist import models

parser = argparse.ArgumentParser(
    description="Run celltypist for cell type annotation. "
)
parser.add_argument("input_h5ad", help="Path to h5ad file.")
parser.add_argument("output_h5ad", help="The output path to h5ad file.")
parser.add_argument(
    "--model",
    default="Human_Lung_Atlas.pkl",
    type=str,
    help="Number of iterations to use; default is 50",
)
parser.add_argument(
    "--majority_voting",
    type=bool,
    default=True,
    action=argparse.BooleanOptionalAction,
    help="Whether to use majority voting classifier.",
)

args = parser.parse_args()

# Read data (assuming normalized)
adata = sc.read_h5ad(args.input_h5ad)
print(f"Read {args.input_h5ad}")

# Download and download the model
models.download_models(model=args.model)
print(f"Downloaded {args.model} at {models.models_path}")

# Load the model
model = models.Model.load(model=args.model)
print(f"Loaded {args.model}")

# prediction
predictions = celltypist.annotate(
    adata, model=model, majority_voting=args.majority_voting
)
print(f"Loaded {args.model}")

adata = predictions.to_adata(insert_labels=True, insert_conf=True, insert_prob=True)

# Write data
adata.write_h5ad(args.output_h5ad)
print(f"Wrote {args.output_h5ad}")
