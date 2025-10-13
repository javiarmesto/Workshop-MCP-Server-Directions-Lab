# Workshop Data Files

This directory contains sample data files used by the MCP Workshop Server for demonstration and testing purposes.

## Files Description

### CSV Files

- **prices.csv**: Sample pricing data for Business Central items
  - Contains item numbers, descriptions, unit prices, and currency information
  - Used by pricing analysis tools

- **categories.csv**: Item category classifications
  - Maps items to their respective categories
  - Used for category-based analysis and filtering

- **substitutes.csv**: Product substitution mappings
  - Defines which items can substitute for others
  - Used by the substitute recommendation tool

### JSON Files

- **price-analysis.json**: Pre-computed price analysis results
  - Contains statistical analysis of pricing data
  - Includes averages, trends, and insights
  - Used for quick reference without recalculation

## Data Format

All CSV files use UTF-8 encoding and include headers. The data is fictional and intended for workshop exercises only.

## Usage

These files are automatically loaded by the MCP server when running in mock mode (without Business Central credentials). The server will use this local data to demonstrate tool functionality.

## Notes

- Data is for demonstration purposes only
- Currency amounts are in various currencies (EUR, USD, etc.)
- Item numbers and descriptions are fictional
- Not suitable for production use
