import os
import subprocess
import shutil
from datetime import datetime

def clean_build():
    """Clean build directories."""
    dirs_to_clean = ['build', 'dist', '*.egg-info']
    for dir_pattern in dirs_to_clean:
        for item in os.listdir('.'):
            if item.startswith(dir_pattern.replace('*', '')):
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)

def run_tests():
    """Run the test suite."""
    print("Running tests...")
    result = subprocess.run(['python', '-m', 'unittest', 'discover', 'tests'],
                          capture_output=True, text=True)
    if result.returncode != 0:
        print("Tests failed!")
        print(result.stdout)
        print(result.stderr)
        return False
    print("All tests passed!")
    return True

def build_package():
    """Build the package."""
    print("Building package...")
    result = subprocess.run(['python', 'setup.py', 'sdist', 'bdist_wheel'],
                          capture_output=True, text=True)
    if result.returncode != 0:
        print("Build failed!")
        print(result.stdout)
        print(result.stderr)
        return False
    print("Package built successfully!")
    return True

def check_distribution():
    """Check the distribution."""
    print("Checking distribution...")
    result = subprocess.run(['twine', 'check', 'dist/*'],
                          capture_output=True, text=True)
    if result.returncode != 0:
        print("Distribution check failed!")
        print(result.stdout)
        print(result.stderr)
        return False
    print("Distribution check passed!")
    return True

def create_release_notes():
    """Create release notes."""
    version = "1.0.0"  # Update this with your version
    date = datetime.now().strftime("%Y-%m-%d")
    
    release_notes = f"""# Release Notes - Version {version} ({date})

## Features
- AI-powered data analysis for disease surveillance
- Advanced visualization capabilities
- Automated report generation
- Risk factor analysis
- Anomaly detection
- Cluster analysis
- Temporal pattern analysis

## Improvements
- Enhanced data processing capabilities
- Improved visualization dashboard
- Better error handling
- Comprehensive test coverage

## Bug Fixes
- Fixed data type conversion issues
- Resolved visualization rendering problems
- Corrected report generation formatting

## Installation
```bash
pip install excel-ai-addin
```

## Usage
```python
from excel_ai_addin import ExcelAIAnalyzer

analyzer = ExcelAIAnalyzer()
df = analyzer.read_excel_data("your_file.xlsx")
insights = analyzer.analyze_data(df)
analyzer.generate_report(insights, "analysis_report.docx")
```
"""
    
    with open("RELEASE_NOTES.md", "w") as f:
        f.write(release_notes)
    print("Release notes created!")

def main():
    """Main distribution process."""
    print("Starting distribution process...")
    
    # Clean previous builds
    clean_build()
    
    # Run tests
    if not run_tests():
        return
    
    # Build package
    if not build_package():
        return
    
    # Check distribution
    if not check_distribution():
        return
    
    # Create release notes
    create_release_notes()
    
    print("""
Distribution package is ready!
To upload to PyPI, run:
    twine upload dist/*
    
To install locally, run:
    pip install dist/excel_ai_addin-1.0.0.tar.gz
    """)

if __name__ == "__main__":
    main() 