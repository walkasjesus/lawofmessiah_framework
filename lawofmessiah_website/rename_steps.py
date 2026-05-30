#!/usr/bin/env python3
"""Rename jv_waj_stap_N_* files to jv_waj_lom_[ID].png convention."""
import os
import glob
import re

IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'media', 'images')

# Full step → LOM ID mapping
STEP_MAP = {
    1: 'GA1', 2: 'GA4', 3: 'BA40', 4: 'GA3', 5: 'FA2', 6: 'FA4', 7: 'D1',
    8: 'QA4', 9: 'BA54', 10: 'UA5', 11: 'AA24', 12: 'AA3', 13: 'DA53',
    14: 'A13', 15: 'NA12', 16: 'JA9', 17: 'AA29', 18: 'O1', 19: 'AA9',
    20: 'BA10', 21: 'DA2', 22: 'GB39', 23: 'CB23', 24: 'M2', 25: 'JA6',
    26: 'E7', 27: 'N1', 28: 'A14', 29: 'EA4', 30: 'G19', 31: 'BA55',
    32: 'D13', 33: 'CA3', 34: 'M1', 35: 'N13', 36: 'AA7', 37: 'G20',
    38: 'DA7', 39: 'TA1', 40: 'KA2', 41: 'BA20', 42: 'QA6', 43: 'N18',
    44: 'JA5', 45: 'G6', 46: 'AB9', 47: 'BA25', 48: 'Y6', 49: 'N3',
    50: 'BA26', 51: 'BA57', 52: 'AA56', 53: 'A2', 54: 'PA1', 55: 'TA4',
    56: 'BA41', 57: 'FA18', 58: 'R1', 59: 'AA8', 60: 'HA5', 61: 'O4',
    62: 'FA9', 63: 'CB15', 64: 'DA5', 65: 'G12', 66: 'G4', 67: 'DA24',
    68: 'HA3', 69: 'ZA1', 70: 'ZA8', 71: 'BA42', 72: 'DA16', 73: 'Y2',
    74: 'BA33', 75: 'NA20', 76: 'QA1', 77: 'BA44',
}

def main():
    # Find all stap files, group by step number
    pattern = os.path.join(IMAGES_DIR, 'jv_waj_stap_*.png')
    files = sorted(glob.glob(pattern))

    # Group by step number
    from collections import defaultdict
    step_files = defaultdict(list)
    for f in files:
        basename = os.path.basename(f)
        m = re.match(r'jv_waj_stap_(\d+)[_\-]', basename)
        if m:
            step_num = int(m.group(1))
            step_files[step_num].append(f)
        else:
            print(f'SKIP (no match): {basename}')

    # Sort files within each step for consistent ordering
    for step_num in step_files:
        step_files[step_num].sort()

    # Perform renames
    for step_num in sorted(step_files.keys()):
        lom_id = STEP_MAP.get(step_num)
        if not lom_id:
            print(f'WARNING: No LOM ID for step {step_num}')
            continue

        lom_id_lower = lom_id.lower()
        files_for_step = step_files[step_num]

        for i, src in enumerate(files_for_step):
            if i == 0:
                dst_name = f'jv_waj_lom_{lom_id_lower}.png'
            else:
                dst_name = f'jv_waj_lom_{lom_id_lower}_{i + 1}.png'

            dst = os.path.join(IMAGES_DIR, dst_name)
            src_basename = os.path.basename(src)

            if os.path.exists(dst):
                print(f'EXISTS (skip): {dst_name}')
            else:
                os.rename(src, dst)
                print(f'RENAMED: {src_basename} -> {dst_name}')

if __name__ == '__main__':
    main()
