# FrinkWorks

**A Python-based Media Asset Management, Automated Quality Control, and Cloud Processing Platform**

FrinkWorks is an independent software engineering project focused on developing modular, extensible tools for professional media workflows.

The platform combines media asset management (MAM), technical metadata extraction, automated quality control (QC), analytics, and cloud-based processing.

## Project Goals

- Build a Python-based media asset management system
- Extract and normalize technical metadata from video and audio assets
- Develop configurable automated QC profiles and validation rules
- Analyze video, audio, and metadata for technical defects
- Support Dolby Vision and IMF metadata validation
- Provide interactive dashboards using Panel and HoloViews
- Implement local and AWS-based media processing workflows
- Analyze QC performance, defect patterns, and processing metrics

## Technology Stack

| Category | Technology |
|---|---|
| Language | Python 3.13|
| Web Interface | Panel, HoloViews, hvPlot |
| API | FastAPI |
| Database | PostgreSQL, SQLAlchemy |
| Media Tools | FFmpeg, FFprobe, MediaInfo, QCTools, OpenCV |
| Analytics | Pandas, NumPy, Plotly |
| Cloud | AWS S3, Lambda, SQS, ECS/Fargate, CloudWatch |
| Infrastructure as Code | AWS CDK (Python) |
| Testing | pytest |
| Code Quality | Ruff |

> **Note:** Technologies will be introduced incrementally as development progresses.

## Development Roadmap

| Milestone | Description |
|---|---|
| M0 | Project Foundation |
| M1 | Media Metadata |
| M2 | QC Engine |
| M3 | MAM & Panel UI |
| M4 | AWS Integration |
| M5 | Cloud Processing |
| M6 | Signal QC |
| M7 | Dolby Vision & IMF |
| M8 | Analytics |

Development progress is tracked through [Github_Issues](https://github.com/matt-damore/frinkworks/issues) and the FrinkWorks Development Project board.

## Getting Started

### Requirements

- Python 3.13
- Git
- VS Code or another Python-compatible editor

### Clone the Repository

```powershell
git clone https://github.com/matt-damore/frinkworks.git
cd frinkworks
```

### Create a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install Development Dependcies

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### Verify Installation

```powershell
python -c "import frinkworks; print(frinkworks.__file__)"
python -m pytest --version
ruff --version
```

### Run Quality Code Checks

```powershell
ruff check src
python -m compileall -q src/frinkworks
```

## Project Architecture

FrinkWorks uses a modular Python architecture with separate components for:

- **Domain:** Core business entities and application models
- **Ingest:** Media asset registration and ingest workflows
- **Metadata:** Technical metadata extraction and normalization
- **QC:** Automated quality control profiles, rules, and findings
- **Storage:** Database persistence and asset storage
- **Workers:** Background processing and job execution
- **API:** Application service endpoints
- **UI:** Panel-based web interface

The processing engine is designed to run locally or through cloud-based workers without depending on the user interface.

### Initial Repository Structure

```text
frinkworks/
├── docs/
│   ├── architecture/
│   └── decisions/
├── src/
│   └── frinkworks/
│       ├── domain/
│       ├── ingest/
│       ├── metadata/
│       ├── qc/
│       ├── storage/
│       ├── workers/
│       ├── api/
│       └── ui/
├── infrastructure/
│   ├── local/
│   └── aws/
├── profiles/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── notebooks/
├── scripts/
├── pyproject.toml
├── .gitignore
└── README.md
```

## Current Status

**M0 - Project Foundation (In Progress)**

The initial repository structure and Python development environment are being established.

Media processing, database integration, and the web application are planned but not yet implemented.

## Licensing

No open-source license has been selected at this stage. All rights are reserved unless otherwise specified.

## Disclaimer

FrinkWorks is an independent project and is not affiliated with or endorced by the creators or rights holders of *The Simpsons*, Dolby Laboratories, Amazon Web Services, or any other referenced product or franchise.
