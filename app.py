import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="CSV Filter - VK Data",
    layout="wide"
)

# Application title
st.title("CSV Filter Application")
st.markdown("Load and filter CSV data with fields like: first_name, last_name, id, last_seen, sex, followers_count, etc.")

# Function to load CSV
def load_csv(file):
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file, encoding=encoding, delimiter=',')
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            st.error("Error reading file. Check the encoding.")
            return None
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

# Function to convert dates
def parse_dates(df):
    date_columns = ['last_seen', 'bdate']
    
    for col in date_columns:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col], format='%d.%m.%Y', errors='coerce')
            except:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    pass
    return df

# Sidebar for upload
with st.sidebar:
    st.header("File Upload")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="File with columns: first_name, last_name, id, last_seen, sex, followers_count, etc."
    )
    
    st.markdown("---")
    st.header("How to use")
    st.markdown("""
    1. Upload CSV file
    2. Use filters below
    3. View data
    4. Export results
    """)

# Check if file was loaded
if uploaded_file is not None:
    # Load data
    df = load_csv(uploaded_file)
    
    if df is not None:
        # Convert dates
        df = parse_dates(df)
        
        # Show basic information
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            if 'id' in df.columns:
                st.metric("Unique IDs", df['id'].nunique())
        
        # Sidebar for filters
        st.sidebar.header("Filters")
        
        # Filter by first name
        if 'first_name' in df.columns:
            names = ['All'] + sorted(df['first_name'].dropna().unique().tolist())
            selected_name = st.sidebar.selectbox("First Name", names)
            if selected_name != 'All':
                df = df[df['first_name'] == selected_name]
        
        # Filter by gender
        if 'sex' in df.columns:
            sex_options = ['All', 'Male (1)', 'Female (2)']
            selected_sex = st.sidebar.selectbox("Gender", sex_options)
            
            if selected_sex == 'Male (1)':
                df = df[df['sex'] == 1]
            elif selected_sex == 'Female (2)':
                df = df[df['sex'] == 2]
        
        # Filter by country
        if 'country_title' in df.columns:
            countries = ['All'] + sorted(df['country_title'].dropna().unique().tolist())
            selected_country = st.sidebar.selectbox("Country", countries)
            if selected_country != 'All':
                df = df[df['country_title'] == selected_country]
        
        # Filter by city
        if 'city_title' in df.columns and len(df) > 0:
            cities = ['All'] + sorted(df['city_title'].dropna().unique().tolist())
            selected_city = st.sidebar.selectbox("City", cities)
            if selected_city != 'All':
                df = df[df['city_title'] == selected_city]
        
        # Filter by birth year
        if 'byear' in df.columns:
            min_year = int(df['byear'].min()) if not df['byear'].isna().all() else 1900
            max_year = int(df['byear'].max()) if not df['byear'].isna().all() else datetime.now().year
            
            year_range = st.sidebar.slider(
                "Birth Year",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year)
            )
            df = df[(df['byear'] >= year_range[0]) & (df['byear'] <= year_range[1])]
        
        # Filter by followers
        if 'followers_count' in df.columns:
            min_followers = int(df['followers_count'].min()) if not df['followers_count'].isna().all() else 0
            max_followers = int(df['followers_count'].max()) if not df['followers_count'].isna().all() else 10000
            
            followers_range = st.sidebar.slider(
                "Followers Count",
                min_value=min_followers,
                max_value=max_followers,
                value=(min_followers, max_followers)
            )
            df = df[(df['followers_count'] >= followers_range[0]) & 
                   (df['followers_count'] <= followers_range[1])]
        
        # Filter by private messages
        if 'can_write_private_message' in df.columns:
            message_options = ['All', 'Can send', 'Cannot send']
            selected_message = st.sidebar.selectbox("Private Message", message_options)
            
            if selected_message == 'Can send':
                df = df[df['can_write_private_message'] == 1]
            elif selected_message == 'Cannot send':
                df = df[df['can_write_private_message'] == 0]
        
        # Show filtered data
        st.subheader(f"Filtered Data ({len(df)} records)")
        
        # Column selection for display
        if len(df.columns) > 10:
            all_columns = df.columns.tolist()
            default_cols = ['first_name', 'last_name', 'id', 'last_seen', 'country_title']
            selected_columns = st.multiselect(
                "Select columns to display:",
                all_columns,
                default=default_cols
            )
            
            if selected_columns:
                df_display = df[selected_columns]
            else:
                df_display = df
        else:
            df_display = df
        
        # Show dataframe
        st.dataframe(df_display, use_container_width=True)
        
        # Statistics
        with st.expander("Statistics"):
            col1, col2 = st.columns(2)
            
            with col1:
                if 'sex' in df.columns:
                    st.write("**Gender Distribution:**")
                    sex_counts = df['sex'].value_counts()
                    for sex, count in sex_counts.items():
                        sex_label = "Male" if sex == 1 else "Female" if sex == 2 else "Other"
                        st.write(f"{sex_label}: {count}")
                
                if 'country_title' in df.columns:
                    st.write("**Top 5 Countries:**")
                    country_counts = df['country_title'].value_counts().head()
                    st.write(country_counts)
            
            with col2:
                if 'followers_count' in df.columns:
                    st.write("**Followers Statistics:**")
                    st.write(f"Average: {df['followers_count'].mean():.0f}")
                    st.write(f"Maximum: {df['followers_count'].max():.0f}")
                    st.write(f"Minimum: {df['followers_count'].min():.0f}")
        
        # Export options
        st.subheader("Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export to CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="filtered_data.csv",
                mime="text/csv",
            )
        
        with col2:
            # Exportar para JSON como alternativa
            json_data = df.to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Baixar JSON",
                data=json_data,
                file_name="dados_filtrados.json",
                mime="application/json",
            )
        
        # Button to clear filters
        if st.button("Clear All Filters"):
            st.rerun()

else:
    # Initial screen without file
    st.info("Please upload a CSV file using the sidebar")
    
    # Example of expected structure
    st.subheader("Expected CSV Structure:")
    
    example_data = {
        'first_name': ['Pappa', 'Maria', 'John'],
        'last_name': ['Hapa', 'Silva', 'Doe'],
        'id': [470000405, 470000406, 470000407],
        'last_seen': ['01.08.2023', '15.07.2023', '20.06.2023'],
        'sex': [1, 2, 1],
        'followers_count': [862, 1500, 320],
        'country_title': ['Brazil', 'Portugal', 'USA'],
        'city_title': ['São Paulo', 'Lisbon', 'New York'],
        'byear': [1993, 1990, 1985],
        'can_write_private_message': [1, 1, 0]
    }
    
    example_df = pd.DataFrame(example_data)
    st.dataframe(example_df)

# Footer
st.markdown("---")
st.markdown("Application developed for CSV data filtering")