import os
import sqlite3
import tempfile
from io import StringIO, BytesIO
import pandas as pd
import streamlit as st

# Streamlit page configuration
st.set_page_config(
    page_title="Delimited File Reader",
    page_icon=":page_with_curl:",
    layout="wide"
)

DEFAULT_TITLE = 'File Content'


def get_text_input(file_types, has_text_input=True, text_input_label="Enter text", file_input_label="Choose a file",
                   is_binary=False):
    """
    Generic function to get text input from user via file upload or text area.
    """
    input_type = st.radio(
        "Select input type:",
        ("Upload file", "Enter text") if has_text_input else ("Upload file",),
        horizontal=True
    )

    text = None
    file_name = DEFAULT_TITLE
    uploaded_file = None

    if input_type == "Upload file":
        uploaded_file = st.file_uploader(file_input_label)
        if uploaded_file is not None:
            if is_binary:
                text = uploaded_file.getvalue()
            else:
                text = uploaded_file.getvalue().decode("utf-8")
            file_name = uploaded_file.name
        else:
            st.warning("Please upload a file.")
            st.stop()
    else:
        text = st.text_area(text_input_label, height=250)
        if not text.strip():
            st.warning("Please enter text.")
            st.stop()

    return text, file_name


def parse_sqlite_database():
    """
    Parses an uploaded SQLite database file and returns a DataFrame.
    """
    uploaded_file = st.file_uploader("Upload SQLite Database File")
    if uploaded_file is not None:
        try:
            # Save the uploaded file to a temporary file
            db_bytes = uploaded_file.getvalue()
            with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp_file:
                tmp_file.write(db_bytes)
                tmp_file_path = tmp_file.name

            # Connect to the temporary SQLite database file
            with sqlite3.connect(tmp_file_path) as conn:
                # Get list of tables
                query = "SELECT name FROM sqlite_master WHERE type='table';"
                tables = pd.read_sql_query(query, conn)
                if tables.empty:
                    st.error("No tables found in the database.")
                    st.stop()
                table_names = tables['name'].tolist()
                selected_table = st.selectbox("Select a table to view", table_names)
                df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
                file_name = f"SQLite Database - {selected_table}"
            # Do not delete the temp file to avoid WinError 32
            # os.unlink(tmp_file_path)
            return df, file_name
        except Exception as e:
            st.error(f"Error reading SQLite database: {e}")
            st.stop()
    else:
        st.warning("Please upload a SQLite database file.")
        st.stop()

def parse_delimited_file(delimiter, has_header=True):
    """
    Parses a delimited text file and returns a DataFrame.
    """
    has_header = st.checkbox("Data has header row", value=has_header)
    text, file_name = get_text_input(file_types=["csv", "tsv", "txt"], has_text_input=True)
    try:
        df = pd.read_csv(StringIO(text), sep=delimiter, header=0 if has_header else None)
    except Exception as e:
        st.error(f"Error parsing file: {e}")
        st.stop()
    return df, file_name


def parse_parquet():
    """
    Parses a Parquet file and returns a DataFrame.
    """
    text, file_name = get_text_input(file_types=["parquet"], has_text_input=False, is_binary=True)
    try:
        df = pd.read_parquet(BytesIO(text))
    except Exception as e:
        st.error(f"Error parsing file: {e}")
        st.stop()
    return df, file_name


def parse_excel():
    """
    Parses an Excel file and returns a DataFrame.
    """
    text, file_name = get_text_input(file_types=["xlsx", "xls"], has_text_input=False, is_binary=True)
    try:
        df = pd.read_excel(BytesIO(text))
    except Exception as e:
        st.error(f"Error parsing file: {e}")
        st.stop()
    return df, file_name


def main():
    st.title("Data Reader")

    with st.sidebar:
        st.header("File Options")
        file_type = st.selectbox(
            "Select file type:",
            ("CSV", "TSV", "Parquet", "Excel", "Database", "Custom Delimited Text"),
        )

        hide_index = st.checkbox("Hide index", value=True)

        limit_rows = st.checkbox("Limit rows displayed", value=False)

        max_rows = None
        if limit_rows:
            max_rows = st.number_input("Max rows to display", min_value=1, value=10)

        if file_type == "CSV":
            st.subheader("CSV Input Options")
            df, title = parse_delimited_file(delimiter=',')
        elif file_type == "TSV":
            st.subheader("TSV Input Options")
            df, title = parse_delimited_file(delimiter='\t')
        elif file_type == "Custom Delimited Text":
            st.subheader("Custom Delimited Text Input Options")
            delimiter = st.text_input("Enter the delimiter", value=",")
            df, title = parse_delimited_file(delimiter=delimiter)
        elif file_type == "Parquet":
            st.subheader("Parquet Input Options")
            df, title = parse_parquet()
        elif file_type == "Excel":
            st.subheader("Excel Input Options")
            df, title = parse_excel()
        elif file_type == "Database":
            st.subheader("Database Input Options")
            df, title = parse_sqlite_database()
        else:
            st.error("Invalid file type selected")
            st.stop()

    if df is not None:
        st.subheader(title)
        if max_rows:
            st.dataframe(df.head(max_rows), use_container_width=True, hide_index=hide_index)
        else:
            st.dataframe(df, use_container_width=True, hide_index=hide_index)


if __name__ == "__main__":
    main()
