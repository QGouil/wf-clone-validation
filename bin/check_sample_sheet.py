#!/usr/bin/env python
"""Script to check that sample sheet is well-formatted."""
import argparse
import sys

import pandas as pd


def main():
    """Run entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument('sample_sheet')
    parser.add_argument('output')
    args = parser.parse_args()

    try:
        samples = pd.read_csv(args.sample_sheet, sep=None)
        if 'alias' in samples.columns:
            if 'sample_name' in samples.columns:
                sys.stderr.write(
                    "Warning: sample sheet contains both 'alias' and "
                    'sample_name, using the former.')
            samples['sample_name'] = samples['alias']
        if 'barcode' not in samples.columns \
                or 'sample_name' not in samples.columns:
            raise IOError()
    except Exception:
        raise IOError(
            "Could not parse sample sheet, it must contain two columns "
            "named 'barcode' and 'sample_name' or 'alias'.")
    # check duplicates
    dup_bc = samples['barcode'].duplicated()
    dup_sample = samples['sample_name'].duplicated()
    if any(dup_bc) or any(dup_sample):
        raise IOError(
            "Sample sheet contains duplicate values.")
    samples.to_csv(args.output, sep=",", index=False)


if __name__ == '__main__':
    main()
