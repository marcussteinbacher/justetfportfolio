# ETF Portfolio Analysis
A comprehensive Streamlit-based app for analyzing a portfolio of ETFs for the aggregated country, sector, and holdings exposure.

https://github.com/user-attachments/assets/62fe9982-2c81-402c-a7b2-a9fc759effe4

## Overview
- Add/remove ETFs listed on justETF with the number of shares or position value.
- Automatically calculates the weights based on the position value for the calculation of portfolio exposure and TER.

> Adding a position with the number of shares held fetches the latest quote to retrieve the position's value.

## Installation & Dependencies
0. Clone repo.
```bash
cd ./..
git clone https://github.com/marcussteinbacher/justetfportfolio.git
```
1. Install justetf-scraping. See https://github.com/druzsan/justetf-scraping for further information.
```bash
pip install git+https://github.com/druzsan/justetf-scraping.git
```
2. Install streamlit.
```bash
pip install streamlit
```

## Running the Application
```bash
cd justetfportfolio
streamlit run app.py
```

## How to Use

1. **Enter ETF Symbol**: Type the ETF ticker symbol in the search box.
2. **Set Shares or Value**: Enter the number of shares you own or the position value. If shares are entered, automatically fetches the latest quote to calculate the portfolio weights.
3. **Add to Portfolio**: Click "Add" to add the ETF to your portfolio.
4. **Remove from Portfolio**: Removing an ETF from the portfolio automatically re-adjusts the weights.
5. **Updating a position**: Adding an ETF already existent in your portfolio updates the position.

## Limitations
All data is crawled from justETF which might be subject of change! 

## Future Enhancements
Possible improvements:
- [ ] Import/Export portfolio to CSV
- [ ] Charting
- [ ] Backtesting portfolio performance against a benchmark
- [ ] Integration with additional data sources

## Acknowledgements
This application is build upon the great work in https://github.com/druzsan/justetf-scraping.
