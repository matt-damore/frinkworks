# ADR-0002: Panel-Based User Interface

**Status:** Accepted
**Date:** 2026-11-11

## Context

FrinkWorks requires an interactive interface for media asset browsing, technical metadata inspection, QC job monitoring, and analytics.

The project is developed primarily in Python and should avoid requiring a separate JavaScript or TypeScript frontend.

## Decision

FrinkWorks will use HoloViz Panel as its primary user interface framework, supported by HoloViews, hvPlot, and Bokeh.

The interface will interact with Python application services rather than directly implement QC business logic.

## Alternatives Considered

### Dash

Dash supports Python-based interactive applications and Plotly visualizations.

However, Panel offers a natural fit with the HoloViz ecosystem and the project's preferred Python development workflow.

### Streamlit

Streamlit enables rapid development of data applications.

However, Panel was selected for its flexible application composition, reactive programming capabilities, and integration with HoloViews and hvPlot.

### JavaScript Frontend

A dedicated JavaScript frontend could provide greater control
over user experience and application structure.

However, it would introduce an additional language and build
toolchain without a demonstrated need.

## Consequences

### Benefits

- Python-focused development.
- Integration with scientific computing and analytics tools.
- Flexible dashboards and interactive visualizations.
- No separate frontend language required.

### Trade-offs

- Panel-specific deployment considerations.
- Careful management of long-running processing operations.
- Potential UI customization limitations compared with a dedicated JavaScript frontend.