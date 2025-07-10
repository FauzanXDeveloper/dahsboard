# AI Data Analyst Dashboard - Setup Guide

## Quick Start

### Option 1: Automated Installation (Windows)

1. **Double-click** `install.bat` to automatically set up everything
2. **Edit** the `.env` file and add your OpenAI API key
3. **Double-click** `run.bat` to start the application

### Option 2: Manual Installation

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

#### Step-by-Step Installation

1. **Clone or download** this project to your local machine

2. **Open PowerShell or Command Prompt** in the project directory

3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

5. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Set up environment variables:**
   ```bash
   copy .env.example .env
   ```
   
   Edit the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

7. **Run the application:**
   ```bash
   streamlit run app.py
   ```

8. **Open your browser** to `http://localhost:8501`

## Getting Your OpenAI API Key

1. Go to [OpenAI's website](https://platform.openai.com/api-keys)
2. Sign up or log in to your account
3. Navigate to "API Keys" in your dashboard
4. Click "Create new secret key"
5. Copy the key and add it to your `.env` file

**Note:** You'll need to add billing information to use the OpenAI API.

## Features Overview

### 🗃️ Data Sources Supported
- **CSV files** - Upload any CSV file
- **Excel files** - Upload .xlsx or .xls files with multiple sheets
- **SQL Databases** - Connect to PostgreSQL, MySQL, or SQLite
- **Sample Data** - Built-in sample datasets for testing

### 🤖 AI Chat Capabilities
- Natural language data queries
- Automatic insights generation
- SQL query generation from plain English
- Data visualization suggestions
- Anomaly detection
- Trend analysis

### 📊 Visualization Tools
- Interactive charts with Plotly
- Automatic chart recommendations
- Customizable chart types:
  - Bar Charts
  - Line Charts
  - Scatter Plots
  - Histograms
  - Box Plots
  - Pie Charts
  - Correlation Heatmaps

### 🔍 Query Interface
- Visual SQL query builder
- Syntax validation
- Query history
- Export results

## Usage Examples

### 1. Upload and Analyze CSV Data
1. Click "Upload File" in the sidebar
2. Select your CSV file
3. Ask the AI: "What are the main trends in this data?"
4. View the generated insights and suggested visualizations

### 2. Connect to Database
1. Select "Database Connection" in the sidebar
2. Choose your database type (PostgreSQL, MySQL, SQLite)
3. Enter connection details
4. Use SQL queries or AI chat to analyze your data

### 3. Generate Visualizations
1. Load your data
2. Go to the "Visualizations" tab
3. Select chart type and columns
4. Customize and export your charts

### 4. AI-Powered Analysis
1. Load your data
2. In the AI Chat tab, ask questions like:
   - "Show me the top 10 customers by revenue"
   - "What patterns do you see in the sales data?"
   - "Create a chart showing monthly trends"
   - "Find any outliers in the data"

## Sample Data

The application includes sample datasets you can use for testing:

- **Sales Data**: 1000 records of sales transactions
- **Customer Data**: 500 customer profiles
- **Inventory Data**: 200 product inventory records

Access these through "Sample Data" in the sidebar.

## Database Connection Examples

### SQLite
```
Database File: ./data/sample.db
```

### PostgreSQL
```
Host: localhost
Port: 5432
Database: your_database
Username: your_username
Password: your_password
```

### MySQL
```
Host: localhost
Port: 3306
Database: your_database
Username: your_username
Password: your_password
```

## Troubleshooting

### Common Issues

**1. Import errors when starting**
- Make sure you activated the virtual environment
- Run: `pip install -r requirements.txt`

**2. OpenAI API errors**
- Check your API key in the `.env` file
- Ensure you have billing set up with OpenAI
- Verify your API quota hasn't been exceeded

**3. Database connection fails**
- Verify connection details
- Check network connectivity
- Ensure database server is running
- Verify user permissions

**4. Large file upload issues**
- Files over 200MB may cause memory issues
- Try sampling your data first
- Use database connection for very large datasets

**5. Streamlit won't start**
- Check if port 8501 is already in use
- Try: `streamlit run app.py --server.port 8502`

### Performance Tips

1. **For large datasets**: Use SQL queries to filter data before analysis
2. **For better AI responses**: Be specific in your questions
3. **For faster loading**: Use smaller sample sizes for initial exploration
4. **For memory efficiency**: Close browser tabs when not in use

## Advanced Features

### Custom SQL Queries
Write your own SQL queries in the SQL Query tab:
```sql
SELECT 
    region,
    SUM(sales_amount) as total_sales,
    AVG(customer_rating) as avg_rating
FROM data_table 
GROUP BY region
ORDER BY total_sales DESC;
```

### Export Options
- Download processed data as CSV
- Export visualizations as PNG/HTML
- Save query results

### Data Quality Checks
- Automatic missing value detection
- Duplicate row identification
- Data type validation
- Outlier detection

## Security Notes

- Never share your OpenAI API key
- Use read-only database connections when possible
- Be cautious with sensitive data
- The application runs locally for privacy

## Support

For issues and questions:
1. Check this README first
2. Review error messages carefully
3. Check the logs in the terminal
4. Ensure all requirements are properly installed

## Updates

To update the application:
1. Pull the latest changes
2. Update requirements: `pip install -r requirements.txt --upgrade`
3. Restart the application

---

**Happy analyzing! 📊🤖**
