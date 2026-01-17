"""
Flask server to serve the Project Stats GUI.
Run this file and open http://localhost:5000 in your browser.
"""

from flask import Flask, request, jsonify, send_from_directory
import os
from collections import defaultdict
from datetime import datetime

app = Flask(__name__, static_folder='web')

# Language mapping
LANGUAGE_MAP = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript (TSX)',
    '.jsx': 'JavaScript (JSX)',
    '.html': 'HTML',
    '.htm': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.sass': 'Sass',
    '.less': 'Less',
    '.java': 'Java',
    '.c': 'C',
    '.cpp': 'C++',
    '.h': 'C/C++ Header',
    '.hpp': 'C++ Header',
    '.cs': 'C#',
    '.go': 'Go',
    '.rs': 'Rust',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.scala': 'Scala',
    '.r': 'R',
    '.R': 'R',
    '.sql': 'SQL',
    '.sh': 'Shell',
    '.bash': 'Bash',
    '.ps1': 'PowerShell',
    '.json': 'JSON',
    '.xml': 'XML',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.md': 'Markdown',
    '.txt': 'Text',
    '.vue': 'Vue',
    '.svelte': 'Svelte',
}

# Directories to skip
SKIP_DIRS = {
    'node_modules', '.git', '__pycache__', '.venv', 'venv',
    'env', '.env', 'dist', 'build', '.idea', '.vscode',
    'target', 'bin', 'obj', '.next', '.nuxt'
}


def format_time_ago(timestamp: float) -> str:
    """Format a timestamp as a human-readable 'time ago' string."""
    now = datetime.now()
    dt = datetime.fromtimestamp(timestamp)
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 2592000:  # 30 days
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 31536000:  # 365 days
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = int(seconds / 31536000)
        return f"{years} year{'s' if years != 1 else ''} ago"


def scan_project(path: str, top: int = 5):
    """Scan a project folder and return statistics."""
    path = os.path.abspath(path)
    
    if not os.path.exists(path):
        raise ValueError(f"Path '{path}' does not exist.")
    
    if not os.path.isdir(path):
        raise ValueError(f"'{path}' is not a directory.")
    
    total_files = 0
    total_lines = 0
    language_stats = defaultdict(lambda: {'files': 0, 'lines': 0})
    file_stats = []
    empty_files_count = 0
    small_files_count = 0
    newest_file = None
    oldest_file = None
    
    for root, dirs, files in os.walk(path):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for filename in files:
            filepath = os.path.join(root, filename)
            _, ext = os.path.splitext(filename)
            
            if ext in LANGUAGE_MAP:
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        line_count = sum(1 for _ in f)
                    
                    total_files += 1
                    total_lines += line_count
                    
                    language_stats[ext]['files'] += 1
                    language_stats[ext]['lines'] += line_count
                    
                    relative_path = os.path.relpath(filepath, path)
                    file_stats.append((relative_path, line_count))
                    
                    # Track anomalies
                    if line_count == 0:
                        empty_files_count += 1
                    elif line_count < 5:
                        small_files_count += 1
                    
                    # Track modification times
                    mtime = os.path.getmtime(filepath)
                    if newest_file is None or mtime > newest_file[1]:
                        newest_file = (relative_path, mtime)
                    if oldest_file is None or mtime < oldest_file[1]:
                        oldest_file = (relative_path, mtime)
                    
                except (IOError, OSError):
                    pass
    
    # Sort languages by lines
    sorted_langs = sorted(
        language_stats.items(),
        key=lambda x: x[1]['lines'],
        reverse=True
    )
    
    languages = [
        {
            'ext': ext,
            'name': LANGUAGE_MAP[ext],
            'lines': stats['lines'],
            'files': stats['files']
        }
        for ext, stats in sorted_langs
    ]
    
    # Sort and get top N largest files
    sorted_files = sorted(file_stats, key=lambda x: x[1], reverse=True)[:top]
    largest_files = [
        {'path': path, 'lines': lines}
        for path, lines in sorted_files
    ]
    
    result = {
        'totalFiles': total_files,
        'totalLines': total_lines,
        'languages': languages,
        'largestFiles': largest_files,
        'emptyFiles': empty_files_count,
        'smallFiles': small_files_count,
    }
    
    if newest_file:
        result['newestFile'] = {
            'path': newest_file[0],
            'timeAgo': format_time_ago(newest_file[1])
        }
    
    if oldest_file:
        result['oldestFile'] = {
            'path': oldest_file[0],
            'timeAgo': format_time_ago(oldest_file[1])
        }
    
    return result


# Routes
@app.route('/')
def index():
    return send_from_directory('web', 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('web', filename)


@app.route('/api/scan', methods=['POST'])
def api_scan():
    try:
        data = request.get_json()
        path = data.get('path', '.')
        top = data.get('top', 5)
        
        result = scan_project(path, top)
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Project Stats GUI Server")
    print("="*50)
    print("\n  Open http://localhost:5000 in your browser\n")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
