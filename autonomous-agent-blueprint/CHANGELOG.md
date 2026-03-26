# Changelog

All notable changes to the repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) where applicable.

## [Unreleased]

### Added
- Companion note links to all six v4 essays (guide/action, guide/reasoning, guide/memory, guide/multi-agent, guide/safety, guide/optimization)
- REPOSITORY_ANALYSIS.md references to practical-chapter-blueprints/README.md
- Rewrite-ledger files moved to `notes/essay-evolution/` with clearer names
- Topic-level READMEs planning (not yet created)

### Fixed
- Corrected broken file references in root README.md: Operating Agents series now points to `guide/launch-note/00-launch-note-v4.md`
- Updated root README.md "Repository Map" and "Publication Layering" sections to reflect topic subfolder organization
- Fixed all v3→v4 references in guide/README.md (V4, V3, V2, and Draft Set tables now use correct subfolder paths)
- Updated all six companion notes to link to v4 essays in their correct subfolders
- Verified that essay subfolder structure is consistently documented

### Changed
- None yet

### Removed
- None (empty artifacts folders retained; old essay versions remain in subfolders)

## [2025-03-25] - Initial Public Release (v4 essays)

### Added
- Practical chapter blueprints (6 files in `practical-chapter-blueprints/`)
- Guide essays v4 (6 topics, organized into subfolders: action, reasoning, memory, multi-agent, safety, optimization, launch-note)
- Companion notes (6 files in `guide/companions/`)
- Paper notes (80+ files in `papers/`)
- Use cases (3 files)
- Case studies (3 dossiers)
- Evaluation assets (2 files)
- Templates (5 files)
- REPOSITORY_ANALYSIS.md (structural analysis)
- MAINTENANCE.md (source intake rules)
- BUILD_HISTORY.md (build notes)

### Fixed
- None (initial release)

### Changed
- None (initial release)

### Removed
- None (initial release)

## [Earlier] - Pre-v4 Drafts (v1–v3)

**Status**: Partially documented. The folder `guide/` retained all draft versions (v1, v2, v3, and original drafts) alongside v4 for archival reference. Conversion between versions is not fully tracked in this changelog; see rewrite-ledger files in `notes/essay-evolution/` for partial evolution notes.

### Added (during draft phases)
- Original near-public draft set (`*-v1.md` equivalents)
- v2 rewrite package (`*-v2.md`) - clearer series pacing, stronger narrative differentiation
- v3 rewrite package (`*-v3.md`) - publication candidate with fuller citations
- v4 rewrite package (`*-v4.md`) - voice guide realignment, denser argument, inline citations

### Fixed
- Unknown (see notes/essay-evolution/ for partial change rationale)

### Removed
- None (all historic drafts retained in topic subfolders)

---

**Note**: This changelog is incomplete for early drafts (v1–v3). If you need precise version-to-version change details for a specific essay, consult the rewrite-ledger files in `notes/essay-evolution/` or compare diffs across the draft files kept in each `guide/*/` subfolder.
