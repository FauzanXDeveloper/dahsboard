import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import openai
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import io
import json
from typing import Dict, List, Any, Optional
import re

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Data Analyst Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
        background-color: #f8f9fa;
    }
    
    .user-message {
        border-left-color: #28a745;
        background-color: #e8f5e9;
    }
    
    .ai-message {
        border-left-color: #1f77b4;
        background-color: #e3f2fd;
    }
    
    .data-info {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

class DataAnalyst:
    def __init__(self):
        self.data = None
        self.data_name = ""
        self.engine = None
        self.openai_client = None
        self.chat_history = []
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.openai_client = openai.OpenAI(api_key=api_key)
    
    def load_csv_data(self, file):
        """Load data from CSV file"""
        try:
            self.data = pd.read_csv(file)
            self.data_name = file.name
            return True, f"Successfully loaded {len(self.data)} rows from {file.name}"
        except Exception as e:
            return False, f"Error loading CSV: {str(e)}"
    
    def load_excel_data(self, file, sheet_name=0):
        """Load data from Excel file"""
        try:
            self.data = pd.read_excel(file, sheet_name=sheet_name)
            self.data_name = file.name
            return True, f"Successfully loaded {len(self.data)} rows from {file.name}"
        except Exception as e:
            return False, f"Error loading Excel: {str(e)}"
    
    def connect_database(self, db_type, connection_params):
        """Connect to database"""
        try:
            if db_type == "SQLite":
                self.engine = create_engine(f"sqlite:///{connection_params['database']}")
            elif db_type == "PostgreSQL":
                self.engine = create_engine(
                    f"postgresql://{connection_params['user']}:{connection_params['password']}@"
                    f"{connection_params['host']}:{connection_params['port']}/{connection_params['database']}"
                )
            elif db_type == "MySQL":
                self.engine = create_engine(
                    f"mysql+pymysql://{connection_params['user']}:{connection_params['password']}@"
                    f"{connection_params['host']}:{connection_params['port']}/{connection_params['database']}"
                )
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            return True, f"Successfully connected to {db_type} database"
        except Exception as e:
            return False, f"Database connection error: {str(e)}"
    
    def execute_query(self, query):
        """Execute SQL query"""
        try:
            if self.engine:
                self.data = pd.read_sql(query, self.engine)
                self.data_name = "SQL Query Result"
                return True, f"Query executed successfully. Retrieved {len(self.data)} rows."
            else:
                return False, "No database connection available"
        except Exception as e:
            return False, f"Query execution error: {str(e)}"
    
    def get_data_info(self):
        """Get basic information about the loaded data"""
        if self.data is None:
            return "No data loaded"
        
        info = {
            "shape": self.data.shape,
            "columns": self.data.columns.tolist(),
            "dtypes": self.data.dtypes.to_dict(),
            "null_counts": self.data.isnull().sum().to_dict(),
            "numeric_summary": self.data.describe().to_dict() if len(self.data.select_dtypes(include=[np.number]).columns) > 0 else {}
        }
        return info
    
    def generate_ai_response(self, user_message):
        """Generate AI response using OpenAI"""
        if not self.openai_client:
            return "OpenAI API key not configured. Please add your API key to use AI features."
        
        try:
            # Prepare context about the data
            data_context = ""
            if self.data is not None:
                data_info = self.get_data_info()
                data_context = f"""
                Current dataset: {self.data_name}
                Shape: {data_info['shape']}
                Columns: {data_info['columns']}
                Data types: {data_info['dtypes']}
                """
            
            # Create system message
            system_message = f"""
            You are an AI data analyst assistant. You help users analyze their data and answer questions about it.
            {data_context}
            
            When users ask about data analysis:
            1. Provide clear, actionable insights
            2. Suggest relevant SQL queries when appropriate
            3. Recommend visualizations
            4. Explain your reasoning
            5. Be concise but thorough
            
            If users want to create charts, suggest specific chart types and the columns to use.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"AI response error: {str(e)}"
    
    def create_visualization(self, chart_type, x_col, y_col, title=""):
        """Create visualizations using Plotly"""
        if self.data is None:
            return None
        
        try:
            if chart_type == "Bar Chart":
                fig = px.bar(self.data, x=x_col, y=y_col, title=title)
            elif chart_type == "Line Chart":
                fig = px.line(self.data, x=x_col, y=y_col, title=title)
            elif chart_type == "Scatter Plot":
                fig = px.scatter(self.data, x=x_col, y=y_col, title=title)
            elif chart_type == "Histogram":
                fig = px.histogram(self.data, x=x_col, title=title)
            elif chart_type == "Box Plot":
                fig = px.box(self.data, y=y_col, title=title)
            elif chart_type == "Pie Chart":
                value_counts = self.data[x_col].value_counts()
                fig = px.pie(values=value_counts.values, names=value_counts.index, title=title)
            else:
                return None
            
            fig.update_layout(
                template="plotly_white",
                font=dict(size=12),
                title_font_size=16
            )
            
            return fig
        except Exception as e:
            st.error(f"Visualization error: {str(e)}")
            return None

def main():
    # Initialize session state
    if 'analyst' not in st.session_state:
        st.session_state.analyst = DataAnalyst()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    analyst = st.session_state.analyst
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Data Analyst Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar for data management
    with st.sidebar:
        st.header("📁 Data Management")
        
        # Data source selection
        data_source = st.selectbox(
            "Choose Data Source",
            ["Upload File", "Database Connection", "Sample Data"]
        )
        
        if data_source == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload your data file",
                type=['csv', 'xlsx', 'xls'],
                help="Supported formats: CSV, Excel"
            )
            
            if uploaded_file is not None:
                file_extension = uploaded_file.name.split('.')[-1].lower()
                
                if file_extension == 'csv':
                    success, message = analyst.load_csv_data(uploaded_file)
                elif file_extension in ['xlsx', 'xls']:
                    success, message = analyst.load_excel_data(uploaded_file)
                
                if success:
                    st.success(message)
                else:
                    st.error(message)
        
        elif data_source == "Database Connection":
            st.subheader("Database Configuration")
            
            db_type = st.selectbox("Database Type", ["SQLite", "PostgreSQL", "MySQL"])
            
            if db_type == "SQLite":
                db_file = st.text_input("Database File Path", "database.db")
                if st.button("Connect to SQLite"):
                    success, message = analyst.connect_database(db_type, {"database": db_file})
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            
            else:
                host = st.text_input("Host", "localhost")
                port = st.number_input("Port", value=5432 if db_type == "PostgreSQL" else 3306)
                database = st.text_input("Database Name")
                user = st.text_input("Username")
                password = st.text_input("Password", type="password")
                
                if st.button(f"Connect to {db_type}"):
                    connection_params = {
                        "host": host,
                        "port": port,
                        "database": database,
                        "user": user,
                        "password": password
                    }
                    success, message = analyst.connect_database(db_type, connection_params)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
        
        elif data_source == "Sample Data":
            if st.button("Load Sample Sales Data"):
                # Create sample data
                np.random.seed(42)
                sample_data = pd.DataFrame({
                    'Date': pd.date_range('2024-01-01', periods=100, freq='D'),
                    'Product': np.random.choice(['Product A', 'Product B', 'Product C'], 100),
                    'Sales': np.random.randint(100, 1000, 100),
                    'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
                    'Customer_Satisfaction': np.random.uniform(3.0, 5.0, 100)
                })
                analyst.data = sample_data
                analyst.data_name = "Sample Sales Data"
                st.success("Sample data loaded successfully!")
        
        # Data overview
        if analyst.data is not None:
            st.header("📊 Data Overview")
            data_info = analyst.get_data_info()
            
            st.markdown(f"""
            <div class="data-info">
                <strong>Dataset:</strong> {analyst.data_name}<br>
                <strong>Rows:</strong> {data_info['shape'][0]}<br>
                <strong>Columns:</strong> {data_info['shape'][1]}
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("Column Details"):
                for col, dtype in data_info['dtypes'].items():
                    null_count = data_info['null_counts'][col]
                    st.write(f"**{col}**: {dtype} ({null_count} nulls)")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Tabs for different functionalities
        tab1, tab2, tab3, tab4 = st.tabs(["💬 AI Chat", "🔍 SQL Query", "📈 Visualizations", "📋 Data View"])
        
        with tab1:
            st.header("AI Chat Assistant")
            
            # Chat interface
            chat_container = st.container()
            
            # Display chat history
            with chat_container:
                for i, (user_msg, ai_msg) in enumerate(st.session_state.chat_history):
                    st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {user_msg}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="chat-message ai-message"><strong>AI:</strong> {ai_msg}</div>', unsafe_allow_html=True)
            
            # Chat input
            user_input = st.text_input("Ask me anything about your data:", key="chat_input")
            
            col_send, col_clear = st.columns([1, 1])
            
            with col_send:
                if st.button("Send", key="send_chat"):
                    if user_input and analyst.data is not None:
                        ai_response = analyst.generate_ai_response(user_input)
                        st.session_state.chat_history.append((user_input, ai_response))
                        st.rerun()
                    elif user_input and analyst.data is None:
                        st.warning("Please load data first to start chatting!")
            
            with col_clear:
                if st.button("Clear Chat", key="clear_chat"):
                    st.session_state.chat_history = []
                    st.rerun()
        
        with tab2:
            st.header("SQL Query Interface")
            
            if analyst.engine or analyst.data is not None:
                # SQL query input
                query = st.text_area(
                    "Enter your SQL query:",
                    height=150,
                    placeholder="SELECT * FROM your_table LIMIT 10"
                )
                
                col_execute, col_sample = st.columns([1, 1])
                
                with col_execute:
                    if st.button("Execute Query"):
                        if query.strip():
                            if analyst.engine:
                                success, message = analyst.execute_query(query)
                                if success:
                                    st.success(message)
                                else:
                                    st.error(message)
                            else:
                                st.warning("Database connection required for SQL queries")
                        else:
                            st.warning("Please enter a query")
                
                with col_sample:
                    if st.button("Sample Queries"):
                        st.code("""
-- Sample SQL Queries:
SELECT * FROM table_name LIMIT 10;
SELECT column1, COUNT(*) FROM table_name GROUP BY column1;
SELECT * FROM table_name WHERE column1 > 100;
SELECT AVG(column1), MAX(column2) FROM table_name;
                        """)
            else:
                st.info("Connect to a database or load data to use SQL queries")
        
        with tab3:
            st.header("Data Visualizations")
            
            if analyst.data is not None:
                col_chart, col_settings = st.columns([2, 1])
                
                with col_settings:
                    chart_type = st.selectbox(
                        "Chart Type",
                        ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Box Plot", "Pie Chart"]
                    )
                    
                    numeric_cols = analyst.data.select_dtypes(include=[np.number]).columns.tolist()
                    all_cols = analyst.data.columns.tolist()
                    
                    if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot"]:
                        x_col = st.selectbox("X-axis", all_cols)
                        y_col = st.selectbox("Y-axis", numeric_cols)
                    elif chart_type in ["Histogram", "Box Plot"]:
                        x_col = st.selectbox("Column", numeric_cols)
                        y_col = x_col
                    elif chart_type == "Pie Chart":
                        x_col = st.selectbox("Category Column", all_cols)
                        y_col = None
                    
                    chart_title = st.text_input("Chart Title", f"{chart_type} of {analyst.data_name}")
                    
                    if st.button("Generate Chart"):
                        fig = analyst.create_visualization(chart_type, x_col, y_col, chart_title)
                        if fig:
                            with col_chart:
                                st.plotly_chart(fig, use_container_width=True)
                
                # Quick insights
                st.subheader("Quick Insights")
                if numeric_cols:
                    insights_col1, insights_col2 = st.columns(2)
                    
                    with insights_col1:
                        # Correlation heatmap
                        if len(numeric_cols) > 1:
                            fig_corr = px.imshow(
                                analyst.data[numeric_cols].corr(),
                                title="Correlation Heatmap",
                                color_continuous_scale="RdBu_r"
                            )
                            st.plotly_chart(fig_corr, use_container_width=True)
                    
                    with insights_col2:
                        # Distribution of first numeric column
                        first_numeric = numeric_cols[0]
                        fig_dist = px.histogram(
                            analyst.data,
                            x=first_numeric,
                            title=f"Distribution of {first_numeric}"
                        )
                        st.plotly_chart(fig_dist, use_container_width=True)
            else:
                st.info("Load data to create visualizations")
        
        with tab4:
            st.header("Data View & Statistics")
            
            if analyst.data is not None:
                # Data preview
                st.subheader("Data Preview")
                st.dataframe(analyst.data.head(20), use_container_width=True)
                
                # Download data
                csv = analyst.data.to_csv(index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name=f"{analyst.data_name}_processed.csv",
                    mime="text/csv"
                )
                
                # Statistical summary
                if len(analyst.data.select_dtypes(include=[np.number]).columns) > 0:
                    st.subheader("Statistical Summary")
                    st.dataframe(analyst.data.describe(), use_container_width=True)
                
                # Missing values
                st.subheader("Missing Values")
                missing_data = analyst.data.isnull().sum()
                missing_data = missing_data[missing_data > 0]
                if len(missing_data) > 0:
                    st.dataframe(missing_data.to_frame("Missing Count"), use_container_width=True)
                else:
                    st.success("No missing values found!")
            else:
                st.info("Load data to view details")
    
    with col2:
        # Quick actions panel
        st.header("🚀 Quick Actions")
        
        if analyst.data is not None:
            st.metric("Total Rows", len(analyst.data))
            st.metric("Total Columns", len(analyst.data.columns))
            
            # Quick analysis buttons
            if st.button("📊 Generate Summary Report"):
                if analyst.openai_client:
                    summary_prompt = f"Analyze this dataset and provide key insights: {analyst.get_data_info()}"
                    summary = analyst.generate_ai_response(summary_prompt)
                    st.text_area("AI Summary", summary, height=200)
                else:
                    st.warning("OpenAI API key required for AI summary")
            
            if st.button("🔍 Find Outliers"):
                numeric_cols = analyst.data.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    outliers_info = {}
                    for col in numeric_cols:
                        Q1 = analyst.data[col].quantile(0.25)
                        Q3 = analyst.data[col].quantile(0.75)
                        IQR = Q3 - Q1
                        outliers = analyst.data[(analyst.data[col] < Q1 - 1.5*IQR) | (analyst.data[col] > Q3 + 1.5*IQR)]
                        outliers_info[col] = len(outliers)
                    
                    st.json(outliers_info)
                else:
                    st.info("No numeric columns for outlier detection")
            
            if st.button("📈 Auto-Visualize"):
                numeric_cols = analyst.data.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) >= 2:
                    # Create automatic correlation plot
                    fig = px.scatter_matrix(analyst.data[numeric_cols[:4]], title="Automatic Correlation Matrix")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Need at least 2 numeric columns for auto-visualization")
        
        # API Configuration
        st.header("⚙️ Configuration")
        
        with st.expander("OpenAI API Setup"):
            current_key = os.getenv("OPENAI_API_KEY", "")
            api_key_input = st.text_input(
                "OpenAI API Key",
                value="***" if current_key else "",
                type="password",
                help="Enter your OpenAI API key for AI features"
            )
            
            if st.button("Update API Key"):
                if api_key_input and api_key_input != "***":
                    os.environ["OPENAI_API_KEY"] = api_key_input
                    analyst.openai_client = openai.OpenAI(api_key=api_key_input)
                    st.success("API key updated!")
                    st.rerun()
        
        # Help section
        with st.expander("💡 Tips & Help"):
            st.markdown("""
            **Getting Started:**
            1. Upload a CSV/Excel file or connect to a database
            2. Use the AI chat to ask questions about your data
            3. Create visualizations in the Charts tab
            4. Run SQL queries for advanced analysis
            
            **AI Chat Examples:**
            - "What are the main trends in this data?"
            - "Show me the top 10 customers by sales"
            - "Create a chart showing sales by region"
            - "Find any anomalies in the data"
            
            **Need Help?**
            Check the README.md file for detailed instructions.
            """)

if __name__ == "__main__":
    main()
