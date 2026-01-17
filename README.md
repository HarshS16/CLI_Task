# Project Stats CLI

A powerful command-line tool to scan project folders and generate comprehensive code statistics. Get insights into your codebase including language breakdown, largest files, file anomalies, and time-based insights.

## Features

- **Total file and line counts** - Quick overview of project size
- **Language breakdown** - Lines and files per programming language (30+ languages supported)
- **Top N largest files** - Identify complexity hotspots
- **File anomalies detection** - Find empty and very small files
- **Time insights** - Track newest and oldest files in the project
- **Export reports** - Save statistics to a text file
- **Smart directory skipping** - Automatically ignores `node_modules`, `.git`, `__pycache__`, etc.

## Installation

### Prerequisites

- Python 3.6 or higher

### Setup

1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   cd CLI_Task
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install fire
   ```

## Usage

### Basic Scan

Scan the current directory:
```bash
python project_stats.py scan
```

Scan a specific folder:
```bash
python project_stats.py scan ./my-project
python project_stats.py scan "C:\Users\YourName\Projects\my-app"
python project_stats.py scan /home/user/projects/my-app
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `path` | Path to the project folder | `.` (current directory) |
| `--top` | Number of largest files to display | `5` |
| `--export` | File path to export the report | None |

### Examples

**Show top 10 largest files:**
```bash
python project_stats.py scan ./my-project --top=10
```

**Export report to a file:**
```bash
python project_stats.py scan ./my-project --export=report.txt
```

**Combine options:**
```bash
python project_stats.py scan ./my-project --top=15 --export=stats.txt
```

## Sample Output

```
Scanning: C:\Users\YourName\Projects\my-app

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
  3. src\pages\Profile.tsx – 2,159 lines
  4. server\package-lock.json – 2,048 lines
  5. src\pages\Dashboard.tsx – 1,686 lines

File Anomalies:
  Empty files: 0
  Very small files (<5 lines): 4

Time Insights:
  Newest file: src\pages\Messages.tsx (2 days ago)
  Oldest file: components.json (5 months ago)
```

## Supported Languages

| Language | Extensions |
|----------|------------|
| Python | `.py` |
| JavaScript | `.js`, `.jsx` |
| TypeScript | `.ts`, `.tsx` |
| HTML | `.html`, `.htm` |
| CSS | `.css`, `.scss`, `.sass`, `.less` |
| Java | `.java` |
| C/C++ | `.c`, `.cpp`, `.h`, `.hpp` |
| C# | `.cs` |
| Go | `.go` |
| Rust | `.rs` |
| Ruby | `.rb` |
| PHP | `.php` |
| Swift | `.swift` |
| Kotlin | `.kt` |
| Scala | `.scala` |
| R | `.r`, `.R` |
| SQL | `.sql` |
| Shell | `.sh`, `.bash` |
| PowerShell | `.ps1` |
| JSON | `.json` |
| XML | `.xml` |
| YAML | `.yaml`, `.yml` |
| Markdown | `.md` |
| Vue | `.vue` |
| Svelte | `.svelte` |

## Directories Automatically Skipped

The tool automatically skips these directories to avoid scanning dependencies and build artifacts:

- `node_modules`
- `.git`
- `__pycache__`
- `.venv`, `venv`, `env`, `.env`
- `dist`, `build`
- `.idea`, `.vscode`
- `target`, `bin`, `obj`
- `.next`, `.nuxt`

## License

MIT License

## Contributing

Feel free to submit issues and pull requests for new features or bug fixes!
