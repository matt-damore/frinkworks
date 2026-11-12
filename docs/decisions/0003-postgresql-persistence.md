# ADR-0003: PostgreSQL for Application Persistence

**Status:** Accepted  
**Date:** 2026-11-11

## Context

FrinkWorks will maintain structured information about media assets, asset versions, QC profiles, processing jobs, technical metadata, and QC findings.

The project requires reliable relationships between these entities and support for analytical queries.

## Decision

PostgreSQL will serve as the primary relational database.

SQLAlchemy is the planned Python database toolkit, with Alembic planned for schema migrations.

Media files will remain in filesystem or object storage. PostgreSQL will store their references and associated metadata.

## Alternatives Considered

### SQLite

SQLite would simplify local development and eliminate the need for a database server.

However, PostgreSQL provides experience with a database platform commonly used in production applications and supports the project's future service-oriented architecture.

### Document Database

A document database could store flexible technical metadata without requiring a rigid schema.

However, FrinkWorks has naturally relational entities such as assets, versions, jobs, and findings.

PostgreSQL also supports JSONB for flexible metadata storage.

## Consequences

### Benefits

- Relational integrity
- Structured queries and analytics
- Flexible JSONB storage
- Compatibility with SQLAlchemy and Alembic
- Potential future deployment using Amazon RDS

### Trade-offs

- Requires running and maintaining a database service
- Introduces schema migration responsibilities
- More initial setup than SQLite