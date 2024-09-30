from io import StringIO, BytesIO
import pandas as pd
import streamlit as st

# Streamlit page configuration
st.set_page_config(
    page_title="Deliminated File Reader",
    page_icon=":page_with_curl:",
    layout="wide"
)

DEFAULT_TITLE = 'File Content'


def parse_csv():
    st.subheader("CSV Input Options")

    has_header = st.checkbox("CSV has header row", value=True)
    delimiter = ','

    input_type = st.radio(
        "Select input type:",
        ("Upload file", "Enter text"),
        horizontal=True
    )

    if input_type == "Upload file":
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
        if uploaded_file is not None:
            text = StringIO(uploaded_file.getvalue().decode("utf-8")).getvalue()
        else:
            text = None
    else:
        text = st.text_area("Enter CSV text", height=250)
        if text == "":
            text = None

    if text is None:
        st.warning("Please upload a CSV file or enter CSV text.")
        st.stop()

    file_name = uploaded_file.name if uploaded_file else DEFAULT_TITLE

    df = pd.read_csv(StringIO(text), sep=delimiter, header=0 if has_header else None)
    return df, file_name


def parse_parquet():
    st.subheader("Parquet Input Options")

    uploaded_file = st.file_uploader("Choose a Parquet file", type=["parquet"])
    if uploaded_file is not None:
        text = uploaded_file.getvalue()
    else:
        text = None

    if text is None:
        st.warning("Please upload a Parquet file or enter Parquet text.")
        st.stop()

    df = pd.read_parquet(BytesIO(text))

    file_name = uploaded_file.name if uploaded_file else "text"

    return df, file_name


def parse_tsv():
    st.subheader("TSV Input Options")

    has_header = st.checkbox("TSV has header row", value=True)
    delimiter = '\t'

    input_type = st.radio(
        "Select input type:",
        ("Upload file", "Enter text"),
        horizontal=True
    )

    if input_type == "Upload file":
        uploaded_file = st.file_uploader("Choose a TSV file", type=["tsv"])
        if uploaded_file is not None:
            text = StringIO(uploaded_file.getvalue().decode("utf-8")).getvalue()
        else:
            text = None
    else:
        text = st.text_area("Enter TSV text", height=250)
        if text == "":
            text = None

    if text is None:
        st.warning("Please upload a TSV file or enter TSV text.")
        st.stop()

    df = pd.read_csv(StringIO(text), sep=delimiter, header=0 if has_header else None)

    file_name = uploaded_file.name if uploaded_file else DEFAULT_TITLE

    return df, file_name


def parse_excel():
    st.subheader("Excel Input Options")

    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])
    if uploaded_file is not None:
        text = uploaded_file.getvalue()
    else:
        text = None

    if text is None:
        st.warning("Please upload an Excel file or enter Excel text.")
        st.stop()

    df = pd.read_excel(BytesIO(text))

    file_name = uploaded_file.name if uploaded_file else DEFAULT_TITLE

    return df, file_name


def parse_tabular_data():
    st.header("Tabular Data Reader")

    deliminator = st.text_input("Enter the deliminator", value=",")

    has_header = st.checkbox("Data has header row", value=True)

    input_type = st.radio(
        "Select input type:",
        ("Upload file", "Enter text"),
        horizontal=True
    )

    if input_type == "Upload file":
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            text = StringIO(uploaded_file.getvalue().decode("utf-8")).getvalue()
        else:
            text = None

    else:
        text = st.text_area("Enter text", height=250)

        if text == "":
            text = None

    if text is None:
        st.warning("Please upload a file or enter text.")
        st.stop()

    df = pd.read_csv(StringIO(text), sep=deliminator, header=0 if has_header else None)

    file_name = uploaded_file.name if uploaded_file else DEFAULT_TITLE

    return df, file_name


with st.sidebar:
    st.title("Data Reader")

    file_type = st.selectbox(
        "Select file type:",
        ("CSV", "TSV", "Parquet", "Excel", "Custom Delimited Text"),
    )
    hide_index = st.checkbox("Hide index", value=True)

    limit_rows = st.checkbox("Limit rows displayed", value=False)

    max_rows = None
    if limit_rows:
        max_rows = st.number_input("Max rows to display", min_value=1, value=10)

    if file_type == "CSV":
        df, title = parse_csv()
    elif file_type == "Parquet":
        df, title = parse_parquet()
    elif file_type == "TSV":
        df, title = parse_tsv()
    elif file_type == "Excel":
        df, title = parse_excel()
    elif file_type == "Custom Delimited Text":
        df, title = parse_tabular_data()
    else:
        raise ValueError("Invalid file type selected")


if df is not None:

    st.subheader(title)
    if max_rows:
        st.dataframe(df.head(max_rows), use_container_width=True, hide_index=hide_index, height=750)
    else:
        st.dataframe(df, use_container_width=True, hide_index=hide_index, height=750)
