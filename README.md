# 🏅 Pakistan Sports Medal Dashboard

An interactive Streamlit dashboard for analyzing medal distributions across countries and Pakistan's performance in different prestige categories.

## Features

- **Medal Proportions by Prestige**: Stacked bar chart showing how each country's medals are distributed across prestige levels
- **Total Medal Comparison**: Compare Pakistan, Group1, and other countries' total medal counts
- **Pakistan's Medal Distribution**: Detailed analysis with scatter plots and distribution charts

## Setup & Installation

### Prerequisites
- Python 3.8 or higher
- Excel file: `database_filled1 anonymised.xlsx` (place in root directory)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-name>

# Install dependencies
pip install -r requirements.txt
```

## Running the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## Deployment

### Option 1: Streamlit Community Cloud (Recommended)

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app" and select your repository
5. Set main file path to `dashboard.py`
6. Click "Deploy"

**Note**: Upload your Excel file separately or use a public URL link in the code.

### Option 2: Render.com

1. Create account at [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run dashboard.py --server.port $PORT --server.headless true`

## Technologies Used

- **Streamlit**: Interactive web dashboard
- **Pandas**: Data manipulation and analysis
- **Matplotlib & Seaborn**: Data visualization
- **OpenPyXL**: Excel file handling

## Dashboard Sections

### 1. Medal Proportions by Prestige
Shows stacked proportions of medals for each country across Low, Medium, and High prestige categories.

### 2. Total Medal Comparison
Displays total medal counts comparing Pakistan (PK), Group1, and other countries (IND, IR, CN, UK, GER, AUS, CAN, USA).

### 3. Pakistan's Medal Distribution
- Scatter plot showing Pakistan's medals vs. game prestige score
- Distribution chart of prestige categories for Pakistan's medal-winning games
- Summary statistics and detailed data tables

## Data Requirements

The dashboard expects an Excel file named `database_filled1 anonymised.xlsx` with the following columns:
- Country columns: PK, IND, IR, CN, UK, GER, AUS, CAN, USA
- Group1
- Game Prestige Score
- Games (game names)

## License

This project is for educational purposes.
