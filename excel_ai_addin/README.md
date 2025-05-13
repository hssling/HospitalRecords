# Excel AI Add-in

An intelligent Excel add-in that provides AI-powered data analysis and automated report generation. This tool uses natural language processing and machine learning to analyze Excel data and create comprehensive reports.

## Features

- AI-powered data summarization using BART model
- Statistical analysis of numerical data
- Trend identification and analysis
- Automated report generation in Word format
- Support for multiple Excel sheets
- Comprehensive error handling and logging

## Requirements

- Python 3.8 or higher
- Microsoft Excel
- Microsoft Word (for report generation)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd excel_ai_addin
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Download required NLTK data:
```python
import nltk
nltk.download('punkt')
```

5. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

1. Prepare your Excel file with the data you want to analyze.

2. Run the script:
```python
from excel_ai_addin import ExcelAIAnalyzer

# Initialize the analyzer
analyzer = ExcelAIAnalyzer()

# Read and analyze your Excel file
df = analyzer.read_excel_data("your_file.xlsx")
insights = analyzer.analyze_data(df)

# Generate a report
analyzer.generate_report(insights, "analysis_report.docx")
```

## Report Structure

The generated report includes:
- Executive summary of the data
- Statistical analysis of numerical columns
- Trend analysis and insights
- Timestamp of report generation

## Error Handling

The add-in includes comprehensive error handling and logging. All operations are logged to help with debugging and monitoring.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Uses the BART model from Facebook AI Research
- Built with openpyxl, pandas, and python-docx
- NLP capabilities powered by spaCy and NLTK 