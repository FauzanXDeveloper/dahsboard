# AI Data Analyst Dashboard Configuration

# Application Settings
APP_TITLE = "AI Data Analyst Dashboard"
APP_ICON = "📊"
APP_LAYOUT = "wide"

# File Upload Settings
ALLOWED_FILE_TYPES = ['csv', 'xlsx', 'xls']
MAX_FILE_SIZE_MB = 200

# Database Settings
SUPPORTED_DATABASES = {
    'SQLite': {
        'driver': 'sqlite',
        'default_port': None,
        'connection_string': 'sqlite:///{database}'
    },
    'PostgreSQL': {
        'driver': 'postgresql',
        'default_port': 5432,
        'connection_string': 'postgresql://{user}:{password}@{host}:{port}/{database}'
    },
    'MySQL': {
        'driver': 'mysql+pymysql',
        'default_port': 3306,
        'connection_string': 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    }
}

# AI Settings
OPENAI_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 1000
TEMPERATURE = 0.7

# Chart Settings
DEFAULT_CHART_TEMPLATE = "plotly_white"
CHART_HEIGHT = 400
CHART_WIDTH = 600

# Data Processing Settings
MAX_ROWS_DISPLAY = 1000
MAX_COLUMNS_DISPLAY = 50
SAMPLE_SIZE_FOR_AI = 5  # Number of rows to show AI for context

# Query Settings
QUERY_TIMEOUT_SECONDS = 30
MAX_QUERY_RESULTS = 10000

# Visualization Recommendations
CHART_RECOMMENDATIONS = {
    'numeric_single': ['histogram', 'box_plot'],
    'numeric_multiple': ['scatter_plot', 'correlation_heatmap', 'line_chart'],
    'categorical_single': ['bar_chart', 'pie_chart'],
    'categorical_multiple': ['stacked_bar', 'grouped_bar'],
    'time_series': ['line_chart', 'area_chart'],
    'mixed': ['grouped_bar', 'scatter_plot']
}

# Default color schemes
COLOR_SCHEMES = {
    'default': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
    'professional': ['#2E4057', '#048A81', '#54C6EB', '#F4A261', '#E76F51'],
    'modern': ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51'],
    'corporate': ['#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087']
}

# Sample queries for different scenarios
SAMPLE_QUERIES = {
    'basic': [
        "SELECT * FROM table_name LIMIT 10",
        "SELECT COUNT(*) FROM table_name",
        "SELECT column1, column2 FROM table_name WHERE column1 > 100"
    ],
    'aggregation': [
        "SELECT column1, COUNT(*), AVG(column2) FROM table_name GROUP BY column1",
        "SELECT MAX(column1), MIN(column1), AVG(column1) FROM table_name",
        "SELECT column1, SUM(column2) FROM table_name GROUP BY column1 ORDER BY SUM(column2) DESC"
    ],
    'analysis': [
        "SELECT column1, column2, ROW_NUMBER() OVER (ORDER BY column2 DESC) as rank FROM table_name",
        "SELECT column1, column2, LAG(column2) OVER (ORDER BY column1) as previous_value FROM table_name"
    ]
}

# AI Prompt Templates
AI_PROMPTS = {
    'data_analysis': """
    Analyze this dataset and provide insights:
    
    Dataset: {dataset_name}
    Columns: {columns}
    Sample data: {sample_data}
    
    Please provide:
    1. Key observations about the data
    2. Interesting patterns or trends
    3. Potential data quality issues
    4. Suggested analyses or visualizations
    """,
    
    'sql_generation': """
    Generate a SQL query for this request:
    
    Available columns: {columns}
    Table name: data_table
    User request: {user_request}
    
    Return only the SQL query, properly formatted.
    Use only SELECT statements.
    """,
    
    'visualization_suggestion': """
    Suggest the best visualization for this data analysis request:
    
    Dataset columns: {columns}
    Data types: {data_types}
    User request: {user_request}
    
    Recommend:
    1. Chart type
    2. X and Y axes
    3. Any additional parameters
    4. Brief explanation of why this chart is appropriate
    """
}

# Error Messages
ERROR_MESSAGES = {
    'no_data': "No data loaded. Please upload a file or connect to a database first.",
    'invalid_file': "Invalid file format. Please upload CSV or Excel files only.",
    'connection_failed': "Database connection failed. Please check your credentials.",
    'query_error': "Query execution failed. Please check your SQL syntax.",
    'ai_error': "AI service unavailable. Please check your API key configuration.",
    'visualization_error': "Unable to create visualization. Please check your data and parameters."
}

# Success Messages
SUCCESS_MESSAGES = {
    'data_loaded': "Data loaded successfully! {rows} rows and {columns} columns.",
    'database_connected': "Database connection established successfully.",
    'query_executed': "Query executed successfully. {rows} rows returned.",
    'chart_created': "Chart created successfully.",
    'export_completed': "Data exported successfully."
}

# Help Text
HELP_TEXT = {
    'file_upload': """
    **Supported file formats:**
    - CSV files (.csv)
    - Excel files (.xlsx, .xls)
    
    **File size limit:** 200MB
    """,
    
    'database_connection': """
    **Supported databases:**
    - SQLite (local file)
    - PostgreSQL
    - MySQL
    
    **Connection requirements:**
    - Valid credentials
    - Network access to database
    - Appropriate permissions
    """,
    
    'ai_chat': """
    **Example questions to ask:**
    - "What are the main trends in this data?"
    - "Show me the top 10 customers by sales"
    - "Create a chart showing sales by region"
    - "Find any anomalies in the data"
    - "Summarize the key insights"
    """,
    
    'sql_queries': """
    **SQL Guidelines:**
    - Only SELECT statements allowed
    - Use 'data_table' as table name
    - Reference actual column names
    - Include LIMIT for large results
    
    **Example queries:**
    ```sql
    SELECT * FROM data_table LIMIT 10;
    SELECT column1, COUNT(*) FROM data_table GROUP BY column1;
    ```
    """,
    
    'visualizations': """
    **Chart types available:**
    - Bar Chart: Categorical comparisons
    - Line Chart: Trends over time
    - Scatter Plot: Relationships between variables
    - Histogram: Distribution of values
    - Box Plot: Statistical summaries
    - Pie Chart: Part-to-whole relationships
    """
}
