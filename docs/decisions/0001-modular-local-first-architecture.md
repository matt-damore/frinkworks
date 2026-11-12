# ADR-0001: Modular, Local-First Architecture

**Status:** Accepted
**Date:** 2026-11-11

## Context

FrinkWorks is a single-developer media technology portfolio project.

It will demonstrate media asset management, technical metadata extraction, automated QC, analytics, and cloud processing.

The system must support meaningful local development without requiring AWS infrastructure during the initial milestones.

It should also be possible to introduce cloud-based processing without rewriting the core QC logic.

## Decision

FrinkWorks will use a modular, local-first Python architecture.

The initial implementation will:

- Run locally on the developer's workstation
- Separate domain models from storage and presentation
- Keep QC rules independent of execution environments
- Use Python application services to coordinate operations
- Introduce background processing as needed
- Defer AWS infrastructure until the local system is functional

## Alternatives Considered

### Cloud-First Architecture

Developing directly against AWS services would provide early experience with cloud infrastructure.

However, it would increase development complexity, require cloud resources during early implementation, and introduce potential costs before core functionality exists.

### Monolithic Panel Application

Implementing all functionality directly inside Panel would simplify initial development.

However, tightly coupling the interface with processing logic would make automated testing, background execution, and future cloud integration more difficult.

## Consequences

### Benefits

- Faster local development and debugging.
- Lower initial infrastructure costs.
- Reusable QC and metadata processing components.
- Easier unit testing.
- Clearer separation of responsibilities.

### Trade-offs

- Additional module boundaries and interfaces.
- Some architectural abstractions may initially appear unnecessary.
- Cloud-specific behavior will require integration testing later.