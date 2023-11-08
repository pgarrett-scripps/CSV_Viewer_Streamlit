from io import StringIO
import pandas as pd
import streamlit as st

# Streamlit page configuration
st.set_page_config(
    page_title="Enhanced CSV Reader",
    page_icon=":page_with_curl:",
    layout="wide"
)


# Function to load and parse the CSV data
def load_csv(input_text, delimiter, header):
    text_io = StringIO(input_text)
    return pd.read_csv(text_io, sep=delimiter, header=0 if header else None)


# Function to handle file uploads or text input
def handle_input():
    with st.sidebar:
        st.header("CSV Input Options")
        # Option to choose input method
        input_method = st.radio(
            "Choose input method:",
            options=['Upload CSV file', 'Enter CSV text']
        )

        # Conditional logic based on input method
        if input_method == 'Enter CSV text':
            text = st.text_area("Enter CSV data", height=250)
        else:
            uploaded_file = st.file_uploader("Upload a CSV file", type=['csv'])
            text = StringIO(uploaded_file.getvalue().decode("utf-8")).getvalue() if uploaded_file is not None else ""

        return text


# Function to display the DataFrame in Streamlit
def display_dataframe(df):
    st.subheader("CSV Data")
    st.dataframe(df, use_container_width=True)


# Sidebar configuration for additional options
with st.sidebar:
    st.header("CSV Reader Settings")

    # Delimiter selection
    delimiter = st.selectbox(
        "Select a delimiter:",
        options=[
            (",", "Comma (,)"),
            (";", "Semicolon (;)"),
            (":", "Colon (:)"),
            ("\t", "Tab"),
            ("|", "Pipe (|)"),
            ("custom", "Custom")
        ],
        format_func=lambda x: x[1],  # Display the description to the user
        index=0
    )
    delimiter = delimiter[0]

    if delimiter == "custom":
        delimiter = st.text_input("Custom Delimiter", value=",")

    has_header = st.checkbox("CSV has header row", value=True)

# Process and display the CSV data
text = handle_input()

if text:
    try:
        st.write(delimiter)
        df = load_csv(text, delimiter, has_header)
        display_dataframe(df)
        # Provide a download button for the processed DataFrame
    except pd.errors.EmptyDataError:
        st.error("The provided CSV data is empty. Please enter some data.")
    except pd.errors.ParserError as e:
        st.error(f"Error parsing CSV data: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Use the sidebar to upload a CSV file or enter CSV data directly into the text area.")
