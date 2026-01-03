# Changelog

All notable changes to UrbanFlow will be documented in this file.

## [Unreleased] - 2025-01-03

### Added
- **Safety mechanisms**: Added `max_path_length` (default: 15) and `max_paths_per_od` (default: 1000) parameters to prevent path enumeration explosion on large networks
- **Input validation**: Added validation for empty graphs and invalid input types with helpful error messages
- **Testing**: Added comprehensive pytest test suite with 20+ tests covering core functionality
- **CI/CD**: Added GitHub Actions workflow for automated testing on Python 3.11 and 3.12 (Ubuntu and Windows)
- **Examples directory**: Created `examples/` directory with sample CSV file and documentation
- **Documentation**: Enhanced README with virtual environment setup instructions, limitations section, and clearer input format examples

### Changed
- **Dependencies**: Pinned minimum versions in `requirements.txt` for reproducibility
- **Documentation**: Clarified multi-edge input format (duplicate entries in neighbor lists)
- **Code quality**: Added type hints and docstrings to core functions

### Fixed
- **Repository hygiene**: Created `.gitignore` to prevent committing output files, cache directories, and virtual environments
- **Documentation**: Fixed README to reference actual notebook filenames and updated CLI examples

### Security
- No security-related changes in this release

---

## Previous Versions

See git history for earlier changes.

