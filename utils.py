import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import os

class DatabaseManager:
    """Utility class for managing database connections and operations"""
    
    def __init__(self):
        self.engine = None
        self.connection_type = None
    
    def create_sqlite_database(self, db_path, data_dict):
        """Create SQLite database from dictionary of DataFrames"""
        try:
            engine = create_engine(f'sqlite:///{db_path}')
            
            for table_name, df in data_dict.items():
                df.to_sql(table_name, engine, if_exists='replace', index=False)
            
            return True, f"SQLite database created at {db_path}"
        except Exception as e:
            return False, f"Error creating database: {str(e)}"
    
    def get_table_info(self, engine):
        """Get information about tables in the database"""
        try:
            with engine.connect() as conn:
                # For SQLite
                if 'sqlite' in str(engine.url):
                    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                    return [table[0] for table in tables]
                # For PostgreSQL
                elif 'postgresql' in str(engine.url):
                    tables = conn.execute("""
                        SELECT table_name FROM information_schema.tables 
                        WHERE table_schema = 'public'
                    """).fetchall()
                    return [table[0] for table in tables]
                # For MySQL
                elif 'mysql' in str(engine.url):
                    tables = conn.execute("SHOW TABLES").fetchall()
                    return [table[0] for table in tables]
        except Exception as e:
            print(f"Error getting table info: {e}")
            return []
    
    def validate_sql_query(self, query):
        """Basic SQL query validation"""
        # Remove comments and extra whitespace
        query = query.strip()
        
        # Check for potentially dangerous operations
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE']
        query_upper = query.upper()
        
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return False, f"Query contains potentially dangerous keyword: {keyword}"
        
        # Check if it starts with SELECT
        if not query_upper.startswith('SELECT'):
            return False, "Only SELECT queries are allowed"
        
        return True, "Query is valid"

class DataProcessor:
    """Utility class for data processing and analysis"""
    
    @staticmethod
    def clean_data(df):
        """Basic data cleaning operations"""
        cleaned_df = df.copy()
        
        # Remove duplicate rows
        initial_rows = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates()
        duplicates_removed = initial_rows - len(cleaned_df)
        
        # Convert string columns that look like numbers
        for col in cleaned_df.columns:
            if cleaned_df[col].dtype == 'object':
                # Try to convert to numeric
                numeric_series = pd.to_numeric(cleaned_df[col], errors='coerce')
                if not numeric_series.isna().all():
                    cleaned_df[col] = numeric_series
        
        return cleaned_df, duplicates_removed
    
    @staticmethod
    def get_data_quality_report(df):
        """Generate data quality report"""
        report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_values': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'duplicate_rows': df.duplicated().sum()
        }
        
        # Calculate missing percentage
        report['missing_percentage'] = {
            col: (missing / len(df)) * 100 
            for col, missing in report['missing_values'].items()
        }
        
        return report
    
    @staticmethod
    def suggest_visualizations(df):
        """Suggest appropriate visualizations based on data types"""
        suggestions = []
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        # Single variable suggestions
        if numeric_cols:
            suggestions.append({
                'type': 'histogram',
                'title': 'Distribution Analysis',
                'columns': numeric_cols[:3],
                'description': 'Show distribution of numeric variables'
            })
            
            if len(numeric_cols) > 1:
                suggestions.append({
                    'type': 'correlation_heatmap',
                    'title': 'Correlation Analysis',
                    'columns': numeric_cols,
                    'description': 'Show correlations between numeric variables'
                })
        
        if categorical_cols:
            suggestions.append({
                'type': 'bar_chart',
                'title': 'Category Counts',
                'columns': categorical_cols[:3],
                'description': 'Show frequency of categorical variables'
            })
        
        # Two variable suggestions
        if len(numeric_cols) >= 2:
            suggestions.append({
                'type': 'scatter_plot',
                'title': 'Relationship Analysis',
                'columns': numeric_cols[:2],
                'description': f'Explore relationship between {numeric_cols[0]} and {numeric_cols[1]}'
            })
        
        if numeric_cols and categorical_cols:
            suggestions.append({
                'type': 'box_plot',
                'title': 'Group Comparison',
                'columns': [categorical_cols[0], numeric_cols[0]],
                'description': f'Compare {numeric_cols[0]} across {categorical_cols[0]} categories'
            })
        
        if datetime_cols and numeric_cols:
            suggestions.append({
                'type': 'time_series',
                'title': 'Time Series Analysis',
                'columns': [datetime_cols[0], numeric_cols[0]],
                'description': f'Show {numeric_cols[0]} trends over time'
            })
        
        return suggestions

class AIPromptGenerator:
    """Generate prompts for AI analysis"""
    
    @staticmethod
    def generate_analysis_prompt(df, user_question):
        """Generate a comprehensive prompt for data analysis"""
        data_summary = DataProcessor.get_data_quality_report(df)
        
        prompt = f"""
        As an expert data analyst, please analyze this dataset and answer the user's question.
        
        Dataset Overview:
        - Total rows: {data_summary['total_rows']}
        - Total columns: {data_summary['total_columns']}
        - Columns: {list(df.columns)}
        - Data types: {data_summary['data_types']}
        - Missing values: {data_summary['missing_values']}
        
        Sample data (first 5 rows):
        {df.head().to_string()}
        
        User Question: {user_question}
        
        Please provide:
        1. A direct answer to the user's question
        2. Relevant insights from the data
        3. Suggested next steps or additional analysis
        4. If applicable, suggest SQL queries or visualizations
        
        Be specific and actionable in your response.
        """
        
        return prompt
    
    @staticmethod
    def generate_sql_from_natural_language(df, natural_query):
        """Generate SQL query from natural language"""
        columns = ', '.join(df.columns)
        
        prompt = f"""
        Convert this natural language query to SQL.
        
        Available columns: {columns}
        Table name: data_table
        
        Natural language query: {natural_query}
        
        Return only the SQL query, no explanation.
        Use only SELECT statements.
        """
        
        return prompt
