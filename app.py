from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import json

app = Flask(__name__)

# Load or initialize configuration
try:
    with open('config.json', 'r') as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    CONFIG = {
        'categories': {
            'Income': ['salary', 'dividend', 'interest'],
            'Groceries': ['grocery', 'supermarket'],
            'Dining': ['restaurant', 'cafe', 'food delivery'],
            'Utilities': ['electricity', 'water', 'gas', 'internet'],
            'Entertainment': ['netflix', 'spotify', 'movie'],
            'Shopping': ['amazon', 'retail'],
            'Transportation': ['uber', 'fuel', 'parking'],
            'Housing': ['rent', 'mortgage'],
            'Other': []
        },
        'budgets': {
            'Groceries': 500,
            'Dining': 300,
            'Entertainment': 100,
            'Shopping': 200
        }
    }
    with open('config.json', 'w') as f:
        json.dump(CONFIG, f)

def categorize_transaction(description):
    description = str(description).lower()
    for category, keywords in CONFIG['categories'].items():
        if any(keyword in description for keyword in keywords):
            return category
    return 'Other'

def generate_monthly_summary(transactions):
    # Ensure we have transactions
    if transactions.empty:
        return {
            'total_income': 0.0,
            'total_expenses': 0.0,
            'savings': 0.0,
            'category_spending': {}
        }
    
    # Get current month's transactions
    current_month = pd.Timestamp.now().strftime('%Y-%m')
    
    # Ensure Date column is datetime
    transactions['Date'] = pd.to_datetime(transactions['Date'])
    
    # Filter for current month
    monthly_transactions = transactions[
        transactions['Date'].dt.strftime('%Y-%m') == current_month
    ]
    
    # Handle empty monthly transactions
    if monthly_transactions.empty:
        monthly_transactions = transactions  # Use all transactions if no current month data
    
    # Calculate key metrics
    income_mask = monthly_transactions['Amount'] > 0
    expense_mask = monthly_transactions['Amount'] < 0
    
    total_income = monthly_transactions[income_mask]['Amount'].sum()
    total_expenses = abs(monthly_transactions[expense_mask]['Amount'].sum())
    savings = total_income - total_expenses
    
    # Calculate category spending
    category_spending = (monthly_transactions[expense_mask]
                        .groupby('Category')['Amount']
                        .sum()
                        .abs()
                        .sort_values(ascending=False)
                        .head(4))  # Top 4 spending categories
    
    return {
        'total_income': float(total_income),
        'total_expenses': float(total_expenses),
        'savings': float(savings),
        'category_spending': category_spending.to_dict()
    }
def generate_spending_chart(transactions):
    # Create monthly spending chart
    monthly_spending = (transactions[transactions['Amount'] < 0]
                       .set_index('Date')
                       .resample('M')['Amount']
                       .sum()
                       .abs()
                       .tail(6))  # Last 6 months
    
    # Set style for modern look
    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor('#1f2937')  # Dark background
    ax.set_facecolor('#1f2937')
    
    # Create gradient effect
    gradient = np.linspace(0, 1, 100)
    gradient = np.vstack((gradient, gradient))
    
    # Plot data with modern styling
    x = range(len(monthly_spending))
    y = monthly_spending.values
    
    # Create gradient fill
    ax.fill_between(x, y, alpha=0.2, color='#3b82f6')
    line = ax.plot(x, y, color='#3b82f6', linewidth=3, zorder=2)
    
    # Add stylized markers
    scatter = ax.scatter(x, y, color='#3b82f6', s=100, 
                        linewidth=2, edgecolor='white', zorder=3)
    
    # Add value labels
    for i, value in enumerate(y):
        ax.text(i, value + (max(y) * 0.02), f'${value:,.0f}',
                ha='center', va='bottom', color='white',
                fontsize=10, fontweight='bold',
                bbox=dict(facecolor='#3b82f6', edgecolor='none', 
                         alpha=0.7, pad=3, boxstyle='round,pad=0.5'))
    
    # Customize appearance
    ax.set_title('Monthly Spending Trend', 
                pad=20, fontsize=14, fontweight='bold', color='white')
    ax.set_xlabel('Month', labelpad=10, fontsize=12, color='#9ca3af')
    ax.set_ylabel('Amount ($)', labelpad=10, fontsize=12, color='#9ca3af')
    
    # Set x-axis labels
    plt.xticks(x, monthly_spending.index.strftime('%B'), 
               rotation=45, ha='right', color='#9ca3af')
    plt.yticks(color='#9ca3af')
    
    # Customize grid
    ax.grid(True, linestyle='--', alpha=0.2, color='#9ca3af')
    ax.set_axisbelow(True)
    
    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Format y-axis labels as currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Adjust layout
    plt.tight_layout()
    
    # Convert plot to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300, bbox_inches='tight',
                facecolor='#1f2937', edgecolor='none')
    img.seek(0)
    plt.close()
    
    return base64.b64encode(img.getvalue()).decode()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' in request.files:
            file = request.files['file']
            if file:
                # Read and process transactions
                transactions = pd.read_csv(file)
                transactions['Date'] = pd.to_datetime(transactions['Date'])
                transactions['Category'] = transactions['Description'].apply(categorize_transaction)
                
                # Generate monthly summary and chart
                monthly_summary = generate_monthly_summary(transactions)
                spending_chart = generate_spending_chart(transactions)
                
                # Get recent transactions
                recent_transactions = (transactions
                    .sort_values('Date', ascending=False)
                    .head(5)
                    .to_dict('records'))
                
                return render_template(
                    "index.html",
                    monthly_summary=monthly_summary,
                    spending_chart=spending_chart,
                    recent_transactions=recent_transactions,
                    categories=CONFIG['categories'],
                    budgets=CONFIG['budgets']
                )
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)