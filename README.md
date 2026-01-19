# Project Stats

A command-line tool and web interface for analyzing codebases. Generates detailed statistics including language distribution, file complexity metrics, and structural anomalies.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Command Line Usage](#command-line-usage)
- [Web Interface](#web-interface)
- [Supported Languages](#supported-languages)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [License](#license)

## Features

| Feature | Description |
|---------|-------------|
| **File Metrics** | Total file count and aggregate lines of code |
| **Language Analysis** | Breakdown by programming language with file counts |
| **Complexity Detection** | Identifies the N largest files in the codebase |
| **Anomaly Detection** | Flags empty files and files under 5 lines |
| **Temporal Analysis** | Reports newest and oldest modified files |
| **Export** | Save reports to text files |
| **Smart Exclusions** | Automatically skips `node_modules`, `.git`, build directories |
| **Web Dashboard** | Browser-based interface with visual charts |

## Installation

### Requirements

- Python 3.6+

### Setup

```bash
# Clone repository
git clone <repository-url>
cd CLI_Task

# Create virtual environment
python -m venv .venv

# Activate environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install fire flask
```

## Command Line Usage

### Basic Commands

```bash
# Scan current directory
python project_stats.py scan

# Scan specific directory
python project_stats.py scan /path/to/project

# Scan with custom options
python project_stats.py scan /path/to/project --top=10 --export=report.txt
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `path` | string | `.` | Directory path to scan |
| `--top` | integer | `5` | Number of largest files to display |
| `--export` | string | None | Output file path for report |

### Example Output

```
Scanning: /home/user/my-project

Total files: 160
Total lines of code: 45,010

Language breakdown:
  - TypeScript (TSX) (.tsx): 19,959 lines (91 files)
  - JSON (.json): 16,825 lines (13 files)
  - TypeScript (.ts): 6,638 lines (31 files)
  - SQL (.sql): 897 lines (17 files)
  - CSS (.css): 422 lines (2 files)

Top 5 largest files:
  1. package-lock.json – 7,531 lines
  2. cities.json – 6,107 lines
  3. src/pages/Profile.tsx – 2,159 lines
  4. server/package-lock.json – 2,048 lines
  5. src/pages/Dashboard.tsx – 1,686 lines

File Anomalies:
  Empty files: 0
  Very small files (<5 lines): 4

Time Insights:
  Newest file: src/pages/Messages.tsx (2 days ago)
  Oldest file: components.json (5 months ago)
```

## Web Interface

### Starting the Server

```bash
python server.py
```

Navigate to `http://localhost:5000` in your browser.

### Interface Features

- Real-time project scanning
- Color-coded language distribution chart
- Summary cards for key metrics
- Ranked list of largest files
- Anomaly reporting section
- One-click report export

### Workflow

1. Enter the full path to target directory
2. Configure display options (optional)
3. Click **Scan Project**
4. Review results in the dashboard
5. Click **Export Report** to download

## Supported Languages

The tool recognizes the following file extensions:

| Category | Languages |
|----------|-----------|
| **Web** | JavaScript (`.js`, `.jsx`), TypeScript (`.ts`, `.tsx`), HTML (`.html`), CSS (`.css`, `.scss`, `.sass`, `.less`), Vue (`.vue`), Svelte (`.svelte`) |
| **Systems** | C (`.c`, `.h`), C++ (`.cpp`, `.hpp`), Rust (`.rs`), Go (`.go`) |
| **Enterprise** | Java (`.java`), C# (`.cs`), Kotlin (`.kt`), Scala (`.scala`) |
| **Scripting** | Python (`.py`), Ruby (`.rb`), PHP (`.php`), Shell (`.sh`, `.bash`), PowerShell (`.ps1`) |
| **Data** | SQL (`.sql`), JSON (`.json`), XML (`.xml`), YAML (`.yaml`, `.yml`) |
| **Mobile** | Swift (`.swift`), Kotlin (`.kt`) |
| **Other** | R (`.r`, `.R`), Markdown (`.md`), Text (`.txt`) |

## Configuration

### Excluded Directories

The following directories are automatically skipped:

```
node_modules/    .git/           __pycache__/
.venv/           venv/           env/
dist/            build/          .idea/
.vscode/         target/         bin/
obj/             .next/          .nuxt/
```

## Project Structure

```
CLI_Task/
├── project_stats.py     # CLI application
├── server.py            # Flask web server
├── README.md            # Documentation
├── .gitignore           # Git exclusions
└── web/
    ├── index.html       # Web interface
    ├── styles.css       # Stylesheet
    └── script.js        # Frontend logic
```

## Design Decisions

### Why Python Fire for CLI?

[Python Fire](https://github.com/google/python-fire) was chosen over alternatives like `argparse` or `click` for several reasons:

| Consideration | Decision |
|---------------|----------|
| **Zero boilerplate** | Fire automatically generates CLI from class methods without decorators or argument definitions |
| **Self-documenting** | Method signatures become CLI arguments; docstrings become help text |
| **Rapid development** | Adding new commands requires only adding new methods |
| **Maintained by Google** | Active development and production-tested |

Alternative considered: `argparse` would require 30+ lines of argument configuration for the same functionality.

### Why Flask for Web Server?

Flask was selected as the web framework for the GUI backend:

| Consideration | Decision |
|---------------|----------|
| **Lightweight** | Minimal overhead for a single-endpoint API |
| **No ORM needed** | Project doesn't require database connectivity |
| **Simple routing** | Only two routes: static files and `/api/scan` |
| **Rapid prototyping** | Full server implemented in ~100 lines |

Alternative considered: FastAPI offers async support, but synchronous file I/O is acceptable for local scanning.

### Why Vanilla JavaScript?

The frontend uses plain HTML/CSS/JS without frameworks:

| Consideration | Decision |
|---------------|----------|
| **No build step** | Files served directly without compilation |
| **Zero dependencies** | No npm, webpack, or node_modules |
| **Portability** | Works in any browser without polyfills |
| **Simplicity** | Single-page application with minimal state |

Alternative considered: React would add complexity for a single-view dashboard.

### Architecture Overview

```
┌─────────────────┐     HTTP POST      ┌─────────────────┐
│   Browser GUI   │ ─────────────────► │   Flask Server  │
│  (JavaScript)   │ ◄───────────────── │   (Python)      │
└─────────────────┘     JSON Response  └────────┬────────┘
                                                │
                                                │ os.walk()
                                                ▼
                                       ┌─────────────────┐
                                       │   File System   │
                                       └─────────────────┘

┌─────────────────┐                    ┌─────────────────┐
│   CLI (Fire)    │ ──── Direct ────►  │   File System   │
└─────────────────┘      Access        └─────────────────┘
```

Both interfaces share the same scanning logic:
- **CLI**: Direct function calls via Fire
- **Web**: HTTP API wrapper around the same logic

### Performance Considerations

| Decision | Rationale |
|----------|-----------|
| **Generator for line counting** | `sum(1 for _ in f)` avoids loading entire file into memory |
| **Directory exclusion during walk** | Modifying `dirs[:]` in-place prevents descending into `node_modules` |
| **Single-pass scanning** | All metrics collected in one traversal |
| **Relative path computation** | Calculated once per file, not on display |

## License

MIT License. See [LICENSE](LICENSE) for details.
