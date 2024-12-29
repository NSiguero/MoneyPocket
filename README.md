# MoneyPocket - Personal Finance Dashboard

MoneyPocket is a web-based financial dashboard that helps you track your spending, monitor savings, and make informed financial decisions. It provides visual analytics and categorization of your transactions.

- Made by NSiguero

## Features

-  Interactive financial dashboard
-  Automatic transaction categorization
-  Monthly spending trends visualization
-  Smart category detection
-  Dark/Light mode support
-  Responsive design
-  CSV file import support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MoneyPocket.git
cd MoneyPocket
```
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Prepare your transaction data in CSV format with the following columns:
   - Date: Transaction date (MM/DD/YYYY)
   - Description: Transaction description
   - Amount: Transaction amount (positive for income, negative for expenses)

4. Upload your CSV file through the web interface and click "Analyze Transactions"

## CSV File Format

Your CSV file should follow this format:
```csv
Date,Description,Amount
01/01/2024,Salary Deposit,+3500.00
01/05/2024,Grocery Shopping,-150.00
```

## Features in Detail

### Transaction Categorization
The app automatically categorizes transactions based on keywords:
- Income: salary, dividend, interest
- Groceries: grocery, supermarket
- Dining: restaurant, cafe, food delivery
- And more...

### Financial Metrics
- Monthly Income
- Monthly Expenses
- Monthly Savings
- Top Spending Categories

### Visualizations
- Monthly spending trends
- Category-wise expense breakdown
- Recent transactions list

## Configuration

The app uses a `config.json` file to store:
- Category definitions
- Budget limits
- Keywords for transaction categorization

You can modify these settings by editing the `config.json` file.

## Requirements

- Python 3.7+
- Flask
- Pandas
- Matplotlib
- NumPy

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact me.

## Acknowledgments

- Built with Flask and TailwindCSS
- Uses Feather Icons for UI elements
- Matplotlib for data visualization
=======
