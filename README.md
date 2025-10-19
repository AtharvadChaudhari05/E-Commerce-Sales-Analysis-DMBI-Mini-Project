# E-commerce Sales Dashboard

This project is a multi-functional Streamlit web application designed to provide insights into e-commerce sales through various analyses, including Market Basket Analysis and Sales Performance vs. Target analysis.

## Project Structure

```
ecommerce-sales-dashboard
├── src
│   ├── assets
│   │   └── styles.css
│   ├── components
│   │   ├── market_basket.py
│   │   ├── sales_performance.py
│   │   └── utils.py
│   ├── data
│   │   ├── products.csv
│   │   ├── sales.csv
│   │   └── targets.csv
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_market_basket.py
│   │   └── test_sales_performance.py
│   └── app.py
├── requirements.txt
├── .gitignore
├── config.yaml
└── README.md
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ecommerce-sales-dashboard
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command in your terminal:
```bash
streamlit run src/app.py
```

## Features

- **Market Basket Analysis**: Analyze customer purchasing patterns and generate association rules.
- **Sales Performance vs. Target**: Compare actual sales against predefined targets to evaluate performance.

## Data Sources

The application utilizes the following CSV files for analysis:
- `src/data/products.csv`: Contains product information.
- `src/data/sales.csv`: Contains sales transaction data.
- `src/data/targets.csv`: Contains sales targets for comparison.

## Testing

Unit tests are provided for the components of the application. To run the tests, navigate to the `src/tests` directory and execute:
```bash
pytest
```

## Configuration

Configuration settings can be modified in the `config.yaml` file to adjust file paths and parameters as needed.

## License

This project is licensed under the MIT License. See the LICENSE file for details.