import fire
import os
from collections import defaultdict
from datetime import datetime

class ProjectStats:
    """CLI tool to scan a project folder and return code statistics."""
    
    # Map file extensions to language names
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
    
    def _format_time_ago(self, timestamp: float) -> str:
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
    
    def scan(self, path: str = ".", top: int = 5, export: str = None):
        """
        Scan a project folder and display code statistics.
        
        Args:
            path: Path to the project folder (default: current directory)
            top: Number of largest files to display (default: 5)
            export: File path to export the report (optional)
        """
        path = os.path.abspath(path)
        
        if not os.path.exists(path):
            print(f"Error: Path '{path}' does not exist.")
            return
        
        if not os.path.isdir(path):
            print(f"Error: '{path}' is not a directory.")
            return
        
        # Collect output lines for both printing and exporting
        output_lines = []
        
        def output(text=""):
            """Print and collect output for export."""
            print(text)
            output_lines.append(text)
        
        output(f"\nScanning: {path}\n")
        
        total_files = 0
        total_lines = 0
        language_stats = defaultdict(lambda: {'files': 0, 'lines': 0})
        file_stats = []  # Track (filepath, line_count) for top N largest files
        empty_files = []  # Track empty files (0 lines)
        small_files = []  # Track very small files (<5 lines)
        newest_file = None  # (filepath, mtime)
        oldest_file = None  # (filepath, mtime)
        
        for root, dirs, files in os.walk(path):
            # Skip unwanted directories
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]
            
            for filename in files:
                filepath = os.path.join(root, filename)
                _, ext = os.path.splitext(filename)
                
                if ext in self.LANGUAGE_MAP:
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            line_count = sum(1 for _ in f)
                        
                        total_files += 1
                        total_lines += line_count
                        
                        lang_name = self.LANGUAGE_MAP[ext]
                        language_stats[ext]['files'] += 1
                        language_stats[ext]['lines'] += line_count
                        
                        # Track file for top N largest files
                        relative_path = os.path.relpath(filepath, path)
                        file_stats.append((relative_path, line_count))
                        
                        # Track file anomalies
                        if line_count == 0:
                            empty_files.append(relative_path)
                        elif line_count < 5:
                            small_files.append((relative_path, line_count))
                        
                        # Track file modification times
                        mtime = os.path.getmtime(filepath)
                        if newest_file is None or mtime > newest_file[1]:
                            newest_file = (relative_path, mtime)
                        if oldest_file is None or mtime < oldest_file[1]:
                            oldest_file = (relative_path, mtime)
                        
                    except (IOError, OSError) as e:
                        print(f"Warning: Could not read file {filepath}: {e}")
        
        # Display results
        output(f"Total files: {total_files:,}")
        output(f"Total lines of code: {total_lines:,}")
        output("\nLanguage breakdown:")
        
        # Sort by lines of code (descending)
        sorted_stats = sorted(
            language_stats.items(), 
            key=lambda x: x[1]['lines'], 
            reverse=True
        )
        
        for ext, stats in sorted_stats:
            lang_name = self.LANGUAGE_MAP[ext]
            output(f"  - {lang_name} ({ext}): {stats['lines']:,} lines ({stats['files']} files)")
        
        if not language_stats:
            output("  No code files found.")
        
        # Display top N largest files
        if file_stats:
            output(f"\nTop {min(top, len(file_stats))} largest files:")
            sorted_files = sorted(file_stats, key=lambda x: x[1], reverse=True)[:top]
            for i, (filepath, lines) in enumerate(sorted_files, 1):
                output(f"  {i}. {filepath} – {lines:,} lines")
        
        # Display file anomalies
        if empty_files or small_files:
            output("\nFile Anomalies:")
            output(f"  Empty files: {len(empty_files)}")
            output(f"  Very small files (<5 lines): {len(small_files)}")
        
        # Display time insights
        if newest_file or oldest_file:
            output("\nTime Insights:")
            if newest_file:
                output(f"  Newest file: {newest_file[0]} ({self._format_time_ago(newest_file[1])})")
            if oldest_file:
                output(f"  Oldest file: {oldest_file[0]} ({self._format_time_ago(oldest_file[1])})")
        
        output()
        
        # Export to file if requested
        if export:
            try:
                with open(export, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(output_lines))
                print(f"Report exported to: {export}")
            except (IOError, OSError) as e:
                print(f"Error: Could not export report to {export}: {e}")


if __name__ == "__main__":
    fire.Fire(ProjectStats)
