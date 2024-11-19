from flask import Flask, render_template, jsonify, request, flash
import pandas as pd
import numpy as np
from pathlib import Path
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'

def clean_app_size(size_str):
    try:
        if pd.isna(size_str):
            return "0 MB"
        size_str = str(size_str).upper()
        if 'MB' in size_str:
            return size_str.strip()
        if 'KB' in size_str:
            size_mb = float(size_str.replace('KB', '').strip()) / 1024
            return f"{size_mb:.1f} MB"
        return "0 MB"
    except:
        return "0 MB"

def clean_price(price_str):
    try:
        if pd.isna(price_str) or 'Free' in str(price_str):
            return 'Free'
        price_str = str(price_str)
        if '$' in price_str:
            return price_str
        return f"${price_str}"
    except:
        return 'Free'

# Load and process data
def load_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, 'data')
        
        print(f"\nLooking for CSV files in: {data_dir}")
        csv_files = list(Path(data_dir).glob('*.csv'))
        
        if not csv_files:
            print("No CSV files found!")
            return pd.DataFrame()
        
        print(f"Found {len(csv_files)} CSV files")
        
        dfs = []
        for file in csv_files:
            try:
                print(f"\nProcessing dataset: {file}")
                df = pd.read_csv(file)
                print(f"Columns found: {df.columns.tolist()}")
                
                required_columns = ['App Name', 'App Size', 'App Price', 'App Type', 'App Version', 'User Rating', 'Downloads']
                
                if not all(col in df.columns for col in required_columns):
                    missing_cols = [col for col in required_columns if col not in df.columns]
                    print(f"Warning: Missing columns in {file}: {missing_cols}")
                    continue
                
                # Clean the data
                df['App Size'] = df['App Size'].apply(clean_app_size)
                df['App Price'] = df['App Price'].apply(clean_price)
                df['User Rating'] = pd.to_numeric(df['User Rating'], errors='coerce')
                df['User Rating'] = df['User Rating'].fillna(0)
                
                print(f"Successfully processed {len(df)} rows")
                dfs.append(df)
                
            except Exception as e:
                print(f"Error processing {file}: {str(e)}")
                continue
        
        if not dfs:
            print("No valid datasets loaded!")
            return pd.DataFrame()
        
        print("\nCombining datasets...")
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"Total rows after combining: {len(combined_df)}")
        
        # Calculate metrics for each app
        print("\nCalculating app metrics...")
        app_metrics = combined_df.groupby('App Name').agg({
            'User Rating': ['mean', 'count', 'max'],
            'Downloads': 'max',
            'App Type': 'first',
            'App Size': 'first',
            'App Version': 'max',
            'App Price': 'first'
        }).reset_index()
        
        # Flatten column names
        app_metrics.columns = ['App Name', 'Average Rating', 'Version Count', 'Highest Rating', 
                             'Downloads', 'App Type', 'App Size', 'Latest Version', 'App Price']
        
        # Round ratings
        app_metrics['Average Rating'] = app_metrics['Average Rating'].round(2)
        app_metrics['Highest Rating'] = app_metrics['Highest Rating'].round(2)
        
        # Convert price to INR
        app_metrics['Price_INR'] = app_metrics['App Price'].apply(
            lambda x: 0 if 'Free' in str(x) else float(str(x).replace('$', '')) * 83
        )
        
        print(f"\nFinal dataset has {len(app_metrics)} unique apps")
        print("Sample of processed data:")
        print(app_metrics.head())
        
        return app_metrics
        
    except Exception as e:
        print(f"\nError in load_data: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return pd.DataFrame()

# Global variable to store processed data
df = load_data()

@app.route('/')
def home():
    try:
        if df.empty:
            print("\nNo data available")
            return render_template('index.html', top_apps=[], categories=[], 
                                message="No app data available. Please check the console for details.")
        
        # Get top rated apps (top 3 for each category)
        top_apps = df.sort_values('Average Rating', ascending=False).groupby('App Type').head(3)
        categories = sorted(df['App Type'].unique().tolist())
        
        print(f"\nRendering template with {len(categories)} categories and {len(top_apps)} top apps")
        return render_template('index.html', top_apps=top_apps.to_dict('records'), 
                             categories=categories)
    
    except Exception as e:
        print(f"\nError in home route: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return f"An error occurred: {str(e)}"

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    if df.empty:
        return jsonify([])
    
    # Find apps matching the query
    matching_apps = df[df['App Name'].str.lower().str.contains(query)]
    
    # Sort by average rating and get only the top result
    top_result = matching_apps.sort_values('Average Rating', ascending=False).head(1)
    
    return jsonify(top_result.to_dict('records'))

@app.route('/category/<category>')
def category(category):
    if df.empty:
        return jsonify([])
    category_apps = df[df['App Type'] == category].sort_values('Average Rating', ascending=False)
    return jsonify(category_apps.to_dict('records'))

if __name__ == '__main__':
    print("\nStarting Flask application...")
    print("1. Open your browser")
    print("2. Go to: http://localhost:3000")
    app.run(host='localhost', port=3000, debug=True)
