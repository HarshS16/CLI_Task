// Language colors for the chart
const languageColors = {
    'Python': '#3572A5',
    'JavaScript': '#f1e05a',
    'TypeScript': '#2b7489',
    'TypeScript (TSX)': '#2b7489',
    'JavaScript (JSX)': '#f1e05a',
    'HTML': '#e34c26',
    'CSS': '#563d7c',
    'SCSS': '#c6538c',
    'Sass': '#a53b70',
    'Less': '#1d365d',
    'Java': '#b07219',
    'C': '#555555',
    'C++': '#f34b7d',
    'C/C++ Header': '#555555',
    'C++ Header': '#f34b7d',
    'C#': '#178600',
    'Go': '#00ADD8',
    'Rust': '#dea584',
    'Ruby': '#701516',
    'PHP': '#4F5D95',
    'Swift': '#ffac45',
    'Kotlin': '#F18E33',
    'Scala': '#c22d40',
    'R': '#198CE7',
    'SQL': '#e38c00',
    'Shell': '#89e051',
    'Bash': '#89e051',
    'PowerShell': '#012456',
    'JSON': '#292929',
    'XML': '#0060ac',
    'YAML': '#cb171e',
    'Markdown': '#083fa1',
    'Text': '#999999',
    'Vue': '#41b883',
    'Svelte': '#ff3e00'
};

// DOM Elements
const scanBtn = document.getElementById('scanBtn');
const exportBtn = document.getElementById('exportBtn');
const folderPathInput = document.getElementById('folderPath');
const topFilesInput = document.getElementById('topFiles');
const loadingEl = document.getElementById('loading');
const resultsEl = document.getElementById('results');
const errorEl = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');

// Store current results for export
let currentResults = null;

// Event Listeners
scanBtn.addEventListener('click', scanProject);
exportBtn.addEventListener('click', exportReport);
folderPathInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') scanProject();
});

async function scanProject() {
    const folderPath = folderPathInput.value.trim();
    const topN = parseInt(topFilesInput.value) || 5;

    if (!folderPath) {
        showError('Please enter a folder path');
        return;
    }

    showLoading(true);
    hideError();
    hideResults();

    try {
        const response = await fetch('/api/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                path: folderPath,
                top: topN
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to scan project');
        }

        currentResults = data;
        displayResults(data);
    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

function displayResults(data) {
    // Summary Cards
    document.getElementById('totalFiles').textContent = formatNumber(data.totalFiles);
    document.getElementById('totalLines').textContent = formatNumber(data.totalLines);
    
    if (data.newestFile) {
        document.getElementById('newestFile').textContent = data.newestFile.timeAgo;
        document.getElementById('newestFile').title = data.newestFile.path;
    }
    
    if (data.oldestFile) {
        document.getElementById('oldestFile').textContent = data.oldestFile.timeAgo;
        document.getElementById('oldestFile').title = data.oldestFile.path;
    }

    // Language Chart
    const chartContainer = document.getElementById('languageChart');
    const languageList = document.getElementById('languageList');
    chartContainer.innerHTML = '';
    languageList.innerHTML = '';

    if (data.languages && data.languages.length > 0) {
        data.languages.forEach(lang => {
            const percentage = (lang.lines / data.totalLines) * 100;
            const color = languageColors[lang.name] || getRandomColor();

            // Chart bar
            const bar = document.createElement('div');
            bar.className = 'chart-bar';
            bar.style.width = `${percentage}%`;
            bar.style.backgroundColor = color;
            bar.title = `${lang.name}: ${formatNumber(lang.lines)} lines (${percentage.toFixed(1)}%)`;
            chartContainer.appendChild(bar);

            // Language list item
            const item = document.createElement('div');
            item.className = 'language-item';
            item.innerHTML = `
                <div class="language-color" style="background-color: ${color}"></div>
                <div class="language-info">
                    <div class="language-name">${lang.name} (${lang.ext})</div>
                    <div class="language-stats">${formatNumber(lang.lines)} lines • ${lang.files} files</div>
                </div>
            `;
            languageList.appendChild(item);
        });
    }

    // Top Largest Files
    const filesList = document.getElementById('largestFiles');
    filesList.innerHTML = '';

    if (data.largestFiles && data.largestFiles.length > 0) {
        data.largestFiles.forEach((file, index) => {
            const item = document.createElement('div');
            item.className = 'file-item';
            item.innerHTML = `
                <span class="file-rank">${index + 1}</span>
                <span class="file-path">${file.path}</span>
                <span class="file-lines">${formatNumber(file.lines)} lines</span>
            `;
            filesList.appendChild(item);
        });
    }

    // File Anomalies
    document.getElementById('emptyFiles').textContent = data.emptyFiles || 0;
    document.getElementById('smallFiles').textContent = data.smallFiles || 0;

    showResults();
}

function exportReport() {
    if (!currentResults) return;

    let report = `Project Stats Report\n`;
    report += `${'='.repeat(50)}\n\n`;
    report += `Scanning: ${folderPathInput.value}\n\n`;
    report += `Total files: ${formatNumber(currentResults.totalFiles)}\n`;
    report += `Total lines of code: ${formatNumber(currentResults.totalLines)}\n\n`;

    report += `Language Breakdown:\n`;
    report += `${'-'.repeat(30)}\n`;
    currentResults.languages.forEach(lang => {
        report += `  - ${lang.name} (${lang.ext}): ${formatNumber(lang.lines)} lines (${lang.files} files)\n`;
    });

    report += `\nTop ${currentResults.largestFiles.length} Largest Files:\n`;
    report += `${'-'.repeat(30)}\n`;
    currentResults.largestFiles.forEach((file, i) => {
        report += `  ${i + 1}. ${file.path} – ${formatNumber(file.lines)} lines\n`;
    });

    report += `\nFile Anomalies:\n`;
    report += `${'-'.repeat(30)}\n`;
    report += `  Empty files: ${currentResults.emptyFiles}\n`;
    report += `  Very small files (<5 lines): ${currentResults.smallFiles}\n`;

    if (currentResults.newestFile) {
        report += `\nTime Insights:\n`;
        report += `${'-'.repeat(30)}\n`;
        report += `  Newest file: ${currentResults.newestFile.path} (${currentResults.newestFile.timeAgo})\n`;
        report += `  Oldest file: ${currentResults.oldestFile.path} (${currentResults.oldestFile.timeAgo})\n`;
    }

    // Download file
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'project-stats-report.txt';
    a.click();
    URL.revokeObjectURL(url);
}

// Utility Functions
function formatNumber(num) {
    return num.toLocaleString();
}

function getRandomColor() {
    const colors = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];
    return colors[Math.floor(Math.random() * colors.length)];
}

function showLoading(show) {
    loadingEl.classList.toggle('hidden', !show);
}

function showResults() {
    resultsEl.classList.remove('hidden');
}

function hideResults() {
    resultsEl.classList.add('hidden');
}

function showError(message) {
    errorMessage.textContent = message;
    errorEl.classList.remove('hidden');
}

function hideError() {
    errorEl.classList.add('hidden');
}
