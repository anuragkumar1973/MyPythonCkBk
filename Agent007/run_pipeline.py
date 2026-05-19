#!/usr/bin/env python
"""
Run Microsoft Foundry Pipeline
Wrapper script to handle PYTHONPATH and execution
"""

import sys
import os

# Add project root to PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now run the pipeline
from src.pipelines.sample_pipeline import main

if __name__ == "__main__":
    main()
