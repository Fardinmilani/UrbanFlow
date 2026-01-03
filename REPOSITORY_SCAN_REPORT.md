# Repository Scan Report - UrbanFlow

## PHASE 0: Current State Analysis

### Repository Structure
```
UrbanFlow/
├── README.md                    ✅ Updated, but has inconsistencies
├── requirements.txt              ⚠️  No version pinning
├── Transport_project.ipynb       ⚠️  Old notebook, not referenced in README
├── UrbanFlow_demo.ipynb          ✅ New demo notebook
├── edges_example.csv             ✅ Example data
├── urbanflow/                    ✅ Package structure exists
│   ├── __init__.py
│   ├── core.py
│   └── cli.py
├── images/                       ✅ Assets
├── LICENSE                       ✅ MIT License
└── viz_polish/                   ⚠️  Output directory (should be gitignored)
```

---

## IDENTIFIED ISSUES

### 🔴 Critical (User-facing, breaks reproducibility)

1. **README filename mismatch**
   - README mentions "Transport project v2.ipynb" (doesn't exist)
   - Actual file: `Transport_project.ipynb`
   - Impact: Users following README will fail to find the notebook

2. **Missing .gitignore**
   - Output directories (`viz_polish/`, `urbanflow_output/`, etc.) are tracked
   - `__pycache__/` directories are tracked
   - Impact: Repository pollution, accidental commits of generated files

3. **No version pinning in requirements.txt**
   - Current: `pandas`, `networkx`, `matplotlib`, `numpy` (no versions)
   - Impact: Non-reproducible builds, potential breaking changes

4. **Unclear input format documentation**
   - README shows `'3': ['4', '4']` implying multi-edges via duplicate values
   - Code uses MultiDiGraph but dict format is ambiguous
   - Impact: Users confused about how to represent parallel edges

### 🟡 Medium (Maintainability, correctness)

5. **No path enumeration safety mechanisms**
   - `find_all_paths_between_all_pairs()` can explode on dense graphs
   - No `max_path_length`, `max_paths`, or cycle detection limits
   - Impact: Hangs/crashes on real-world networks

6. **Old notebook (`Transport_project.ipynb`) not integrated**
   - Contains original logic but not using new package
   - Duplicates functionality, creates confusion
   - Impact: Two ways to do the same thing, maintenance burden

7. **No input validation**
   - No checks for empty graphs, invalid node types, missing nodes
   - Impact: Cryptic errors for users

8. **Output directory not standardized**
   - CLI uses `--output-dir`, notebook uses hardcoded paths
   - No `.gitignore` for outputs
   - Impact: Inconsistent behavior, repo pollution

### 🟢 Low (Polish, professional standards)

9. **No tests**
   - Zero test coverage
   - Impact: No confidence in refactoring, regression risk

10. **No CI/CD**
    - No automated testing or linting
    - Impact: Broken code can be merged

11. **Missing type hints in some places**
    - Some functions lack complete type annotations
    - Impact: Less IDE support, harder maintenance

12. **No examples directory**
    - Example CSV is in root, no structured examples/
    - Impact: Less discoverable for new users

---

## PROPOSED PLAN

### Phase 1: Fix Obvious User-Facing Problems (MUST-DO)
**Risk: LOW** - Safe, straightforward fixes

#### A) README Consistency
- [ ] **Decision needed**: Rename notebook OR update README?
  - Option 1: Rename `Transport_project.ipynb` → `Transport_project_v2.ipynb` (match README)
  - Option 2: Update README to reference `Transport_project.ipynb` (simpler)
  - **Recommendation**: Option 2 (update README) - less disruptive
  
- [ ] Update all README references to match actual filenames
- [ ] Verify all commands in README are runnable

#### B) Dependencies / Reproducibility
- [ ] Pin versions in `requirements.txt` (use `>=` for minor flexibility)
- [ ] Add Python version requirement (3.11+)
- [ ] Update README setup section with venv instructions
- [ ] Test clean install from scratch

#### C) Input Format Clarification
- [ ] **Decision needed**: How should multi-edges be represented?
  - Option 1: Keep dict with duplicates `{'3': ['4', '4']}` → MultiDiGraph
  - Option 2: Use edge list format (CSV) as primary, dict as legacy
  - Option 3: Explicit MultiDiGraph construction API
  - **Recommendation**: Option 1 (current approach) + document clearly
  
- [ ] Add clear documentation with examples
- [ ] Add input validation with helpful errors

### Phase 2: Safety & Performance Guardrails
**Risk: MEDIUM** - Changes behavior, needs testing

- [ ] Add `max_path_length` parameter (default: 10-15)
- [ ] Add `max_paths_per_od` parameter (default: 1000)
- [ ] Add cycle detection / visited node tracking (already exists but no limits)
- [ ] Add warnings when limits are hit
- [ ] Document limits in README and docstrings

### Phase 3: Repository Hygiene
**Risk: LOW** - Safe cleanup

- [ ] Create `.gitignore`:
  - `__pycache__/`, `*.pyc`, `*.pyo`
  - `*.csv`, `*.xlsx`, `*.txt` (outputs)
  - `outputs/`, `*_output/`, `viz_*/`
  - `.venv/`, `venv/`
  - `.pytest_cache/`, `.mypy_cache/`
- [ ] Move `edges_example.csv` to `examples/` directory
- [ ] Clean up tracked output files (move to `.gitignore`)

### Phase 4: Testing & CI
**Risk: LOW** - Additive only

- [ ] Create `tests/` directory
- [ ] Add `pytest` to requirements
- [ ] Write tests:
  - Graph loading from CSV
  - Path enumeration with known graph
  - Edge usage counting correctness
  - OD incidence matrix shape/values
  - Safety limits (max_path_length)
- [ ] Add `.github/workflows/ci.yml`:
  - Python 3.11, 3.12
  - `pip install -r requirements.txt`
  - `pytest`
- [ ] Add basic linting (ruff) - optional but recommended

### Phase 5: Notebook Integration
**Risk: LOW** - Keep old notebook working

- [ ] Update `Transport_project.ipynb` to optionally use `urbanflow` package
- [ ] Add comment at top: "Legacy notebook - see UrbanFlow_demo.ipynb for package usage"
- [ ] OR: Move to `examples/legacy/` if keeping for reference

### Phase 6: Documentation Polish
**Risk: LOW** - Documentation only

- [ ] Add CHANGELOG section to README
- [ ] Add "Limitations" section (path explosion, etc.)
- [ ] Add "Contributing" guidelines (if not exists)
- [ ] Add example outputs snippet/screenshot

---

## ESTIMATED RISK PER PHASE

- **Phase 1**: LOW - Documentation and dependency fixes
- **Phase 2**: MEDIUM - Behavior changes, needs careful testing
- **Phase 3**: LOW - Cleanup, no functional changes
- **Phase 4**: LOW - Additive, improves confidence
- **Phase 5**: LOW - Optional, can skip if preferred
- **Phase 6**: LOW - Documentation only

---

## QUESTIONS FOR USER

1. **Notebook naming**: Rename `Transport_project.ipynb` to match README, or update README?
2. **Multi-edge format**: Keep current dict-with-duplicates approach, or prefer explicit API?
3. **Old notebook**: Keep `Transport_project.ipynb` as-is, update it, or archive it?

---

## NEXT STEPS

After user confirms decisions, proceed with Phase 1 fixes in logical commits.

