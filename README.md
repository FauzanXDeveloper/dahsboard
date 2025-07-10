# AI Data Analyst Dashboard

A comprehensive standalone AI-powered data analysis dashboard that supports multiple data sources and provides an intelligent chat interface for data exploration.

## Features

- 📊 **Multi-format Data Support**: SQL databases, Excel files, CSV files
- 🤖 **AI Chat Interface**: Natural language queries powered by OpenAI GPT
- 🔍 **Query Tools**: SQL query builder and executor
- 📈 **Data Visualization**: Interactive charts and graphs with Plotly
- 💾 **Database Management**: Connect to PostgreSQL, MySQL, SQLite
- 🎨 **Modern UI**: Clean, professional dashboard interface

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. **Upload Data**: Upload CSV files, Excel files, or connect to SQL databases
2. **Explore Data**: Use the AI chat to ask questions about your data
3. **Query Data**: Write custom SQL queries or use natural language
4. **Visualize**: Generate charts and graphs automatically
5. **Export**: Download results and visualizations

## Supported Data Sources

- CSV files
- Excel files (.xlsx, .xls)
- SQLite databases
- PostgreSQL databases
- MySQL databases

## AI Capabilities

- Natural language data queries
- Automatic chart generation
- Data insights and analysis
- SQL query generation from natural language
- Data cleaning suggestions
