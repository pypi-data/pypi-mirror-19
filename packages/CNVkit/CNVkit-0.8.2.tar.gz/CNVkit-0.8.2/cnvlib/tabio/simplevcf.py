"""Simple VCF I/O.

Read only coordinate info & store the remaining columns as unparsed strings.
Just enough functionality to extract a subset of samples and/or perform
bedtools-like operations on VCF records.
"""
from __future__ import absolute_import, division, print_function

# import logging

import pandas as pd

