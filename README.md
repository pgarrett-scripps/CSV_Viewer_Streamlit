# Delimited File Reader

A simple Streamlit app to read and display data from various file formats including CSV, TSV, Parquet, Excel, and SQLite databases.

## Features
- Upload and view delimited text files (CSV, TSV, custom delimiters).
- Upload and view Excel, Parquet, and SQLite database files.
- Option to enter data manually via text input.
- Toggle display options like hiding the index and limiting the number of displayed rows.

## How to Use
1. Select the file type from the sidebar.
2. Upload your file or enter text.
3. View the content in the main display area.

## How to Run Locally
```bash
git clone https://github.com/pgarrett-scripps/CSV_Viewer_Streamlit.git
cd CSV_Viewer_Streamlit
pip install -r requirements.txt
streamlit run app.py
```

## Online Demo
https://csv-text-viewer.streamlit.app/