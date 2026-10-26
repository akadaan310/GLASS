# Glass Listening Publisher Implementation Plan

> Agentic workers: execute this plan inline, preserving owner-authorized main publication after each completed unit.

**Goal:** Deliver a native concurrent commission recorder, a replayable behavior projection, and an acquired-source atlas.

**Architecture:** Versioned declarations and pre-appended intents govern observations. One durable journal reconstructs concurrent region configurations and a structural behavior weight. Original archives and pinned upstream content feed a coverage-aware atlas.

**Tech Stack:** C++20, POSIX file locking and fsync, file-backed TSV journal, JSON/Markdown exports; host acquisition tools for immutable source inventory.

**Spec:** docs/GLASS_COMMISSION.md

## Global constraints

- Integration branch: main.
- Original source custody retains bytes and source identities.
- Runtime core: native C++20.
- Each observed effect references an earlier intent and matching declared transition.
- Publication and acquisition receipts describe actual observed outcomes.

## Review focus

- Interrupted appends: retain evidence and surface journal-tail recovery requirements.
- Concurrent writers: lock entire read/validate/append operation and compare event cursor.
- Multiple matching rules: require one destination per region for a given state/event.
- Repeated submissions: retain intent IDs and accept one outcome per intent.
- Source equivalence: retain source occurrence identity alongside content identity.

## Unit 1: Native commission kernel

Files: runtime/glass.hpp, runtime/main.cpp, tests/kernel.cpp, Makefile.
Interfaces: Machine::apply(vector<string>), Machine::state(), Machine::weight(); Journal::submit(command, expected_cursor).

- [ ] Write assertions for undeclared event, pre-intent requirement, simultaneous reactions in two regions, duplicate outcome, replay, torn tail, and stale cursor.
- [ ] Observe compiler failure while the kernel interface is pending.
- [ ] Implement declarations, intent/outcome grammar, one atomic observation record, prefix-tree behavior projection, and locked journal replay.
- [ ] Run native kernel assertions and CLI replay fixture.
- [ ] Publish exact source and evidence to GLASS/main.

## Unit 2: Source custody and atlas

Files: sources/inventory/*.json, atlas/*.json, docs/ATLAS.md.

- [ ] Inventory supplied originals and recursively inspect ZIP members under fixed member/depth/byte limits.
- [ ] Acquire pinned University source content and extract exact topics, divisions, definitions, glossary entries, books, and source references.
- [ ] Inventory SURFACE tree and existing compiler/PHANTOM paths.
- [ ] Record per-source coverage with a resumable frontier.
- [ ] Produce human and machine projections and publish the reviewed atlas records.

## Unit 3: Persistence and continuation

Files: docs/CONTINUE.md, docs/TRANSPORT.md, evidence/publication.json, portable package.

- [ ] Specify URL/MCP command mapping, version preconditions, identity, source visibility, and service deployment receipts.
- [ ] Preserve supplied originals in the private portable package; publish public implementation and reviewed source metadata to main.
- [ ] Save portable deliverable, source custody manifest, and exact next commands.
- [ ] Record active implementation scope and remaining acquisition frontier.
