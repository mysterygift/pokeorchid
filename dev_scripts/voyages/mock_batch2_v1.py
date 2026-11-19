"""
Batch 2 v1 (hand-composed Sevii 1-3 mockups, superseded by the FRLG translations of mock_batch2.py).
Kept for comparison: <venv python> dev_scripts/voyages/mock_batch2_v1.py -> out/batch2_v1/
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc       # noqa: E402
import specs_batch2_v1 as sp      # noqa: E402

if __name__ == "__main__":
    out = os.path.join(HERE, "out", "batch2_v1")
    for name, spec in sp.ALL.items():
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        vc.check_size(*spec["size"])
        vc.render(spec, os.path.join(out, name))
        print(name, spec["size"])
