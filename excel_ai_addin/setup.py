from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="excel-ai-addin",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI-powered Excel add-in for disease surveillance analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/excel-ai-addin",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openpyxl>=3.1.2",
        "pandas>=2.1.0",
        "python-docx>=0.8.11",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "nltk>=3.8.1",
        "spacy>=3.7.2",
        "transformers>=4.35.0",
        "torch>=2.1.0",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.7.1",
        "seaborn>=0.12.2",
        "numpy>=1.24.3",
        "plotly>=5.18.0"
    ],
    entry_points={
        "console_scripts": [
            "excel-ai-addin=excel_ai_addin.excel_ai_addin:main",
        ],
    },
    include_package_data=True,
    package_data={
        "excel_ai_addin": ["example_data/*.xlsx"],
    },
) 