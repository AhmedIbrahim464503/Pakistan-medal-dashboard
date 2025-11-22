import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Pakistan Sports Medal Dashboard", layout="wide")

# Title
st.title("🏅 Pakistan Sports Medal Analysis Dashboard")

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_excel('database_filled1 anonymised.xlsx')
    df['Group1'] = pd.to_numeric(df['Group1'], errors='coerce').fillna(0)
    
    # Create prestige category if missing
    bins = [0, 0.05, 0.15, 0.3]
    labels = ['Low', 'Medium', 'High']
    df['Prestige Category'] = pd.cut(df['Game Prestige Score'], bins=bins, labels=labels, right=False)
    
    return df

# Load data
try:
    df = load_data()
    st.success(f"Data loaded successfully! Total games: {len(df)}")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
country_columns = ['PK', 'IND', 'IR', 'CN', 'UK', 'GER', 'AUS', 'CAN', 'USA']

# Create tabs for different visualizations
tab1, tab2, tab3 = st.tabs([
    "📊 Medal Proportions by Prestige", 
    "🎯 Total Medal Comparison", 
    "🇵🇰 Pakistan's Medal Distribution"
])

# TAB 1: Stacked Proportion of Medals per Country Across Prestige Categories
with tab1:
    st.header("Stacked Proportion of Medals per Country Across Prestige Categories")
    st.write("This chart shows how each country's medals are distributed across different prestige levels.")
    
    # Total medals per country
    total_medals_per_country = df[country_columns].sum()
    
    # Medals per prestige category
    country_prestige = df.groupby('Prestige Category', observed=False)[country_columns].sum().reset_index()
    
    # Proportion per country per category
    country_prestige_prop = country_prestige.copy()
    for col in country_columns:
        if total_medals_per_country[col] > 0:
            country_prestige_prop[col] = country_prestige_prop[col] / total_medals_per_country[col]
        else:
            country_prestige_prop[col] = 0
    
    # Melt for plotting
    country_prestige_proportion_melted = country_prestige_prop.melt(
        id_vars='Prestige Category',
        var_name='Country',
        value_name='Proportion of Medals'
    )
    
    # Pivot for stacked bar chart
    df_plot = country_prestige_proportion_melted.pivot(
        index='Country',
        columns='Prestige Category',
        values='Proportion of Medals'
    )
    
    df_plot = df_plot[['Low', 'Medium', 'High']]
    
    # Use the SAME COLOR PALETTE
    colors = sns.color_palette("viridis", 3)
    
    # Stacked bar chart
    fig1, ax1 = plt.subplots(figsize=(15, 8))
    bottom = None
    
    for i, cat in enumerate(df_plot.columns):
        ax1.bar(
            df_plot.index,
            df_plot[cat],
            bottom=bottom,
            label=cat,
            color=colors[i]
        )
        bottom = df_plot[cat] if bottom is None else bottom + df_plot[cat]
    
    ax1.set_title("Stacked Proportion of Medals per Country Across Prestige Categories", fontsize=16)
    ax1.set_xlabel("Country", fontsize=12)
    ax1.set_ylabel("Proportion (Total = 1)", fontsize=12)
    ax1.set_xticklabels(df_plot.index, rotation=45, ha="right")
    ax1.set_ylim(0, 1)
    ax1.legend(title="Prestige Category")
    plt.tight_layout()
    
    st.pyplot(fig1)
    
    # Display data table
    with st.expander("View Data Table"):
        st.dataframe(df_plot.style.format("{:.2%}"))

# TAB 2: Total Medal Count Comparison
with tab2:
    st.header("Total Medal Count Comparison: Pakistan vs. Group1 and Other Countries")
    st.write("Compare total medal counts across all entities.")
    
    # Calculate total medal counts
    total_medals_pk = df['PK'].sum()
    total_medals_group1 = df['Group1'].sum()
    other_countries = ['IND', 'IR', 'CN', 'UK', 'GER', 'AUS', 'CAN', 'USA']
    total_medals_other_countries = df[other_countries].sum()
    
    # Create a pandas Series for total medal counts
    all_totals = pd.concat([
        pd.Series({'PK': total_medals_pk}),
        pd.Series({'Group1': total_medals_group1}),
        total_medals_other_countries
    ])
    
    # Convert to DataFrame for plotting
    total_medals_df = all_totals.reset_index()
    total_medals_df.columns = ['Entity', 'Total Medals']
    
    # Generate bar chart
    fig2, ax2 = plt.subplots(figsize=(14, 7))
    sns.barplot(x='Entity', y='Total Medals', hue='Entity', data=total_medals_df, palette='viridis', legend=False, ax=ax2)
    ax2.set_title('Total Medal Count Comparison: Pakistan vs. Group1 and Other Countries', fontsize=16)
    ax2.set_xlabel('Entity', fontsize=12)
    ax2.set_ylabel('Total Medals', fontsize=12)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    
    st.pyplot(fig2)
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pakistan (PK)", f"{int(total_medals_pk)} medals")
    with col2:
        st.metric("Group1", f"{int(total_medals_group1)} medals")
    with col3:
        st.metric("Highest Country", f"{total_medals_df.loc[total_medals_df['Total Medals'].idxmax(), 'Entity']}: {int(total_medals_df['Total Medals'].max())} medals")
    
    # Display data table
    with st.expander("View Data Table"):
        st.dataframe(total_medals_df.sort_values('Total Medals', ascending=False))

# TAB 3: Pakistan's Medal Distribution
with tab3:
    st.header("Pakistan's Medal Distribution Analysis")
    st.write("Detailed analysis of Pakistan's performance across different prestige categories.")
    
    # Filter for Pakistan medals
    df_pk_medals = df[df['PK'] > 0].copy()
    
    st.info(f"Number of games where Pakistan won medals: {len(df_pk_medals)}")
    
    # Create two columns for the visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pakistan's Medals vs. Game Prestige Score")
        
        # Scatter plot
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x='Game Prestige Score', y='PK', data=df_pk_medals, 
                       hue='Prestige Category', palette='coolwarm', s=100, ax=ax3)
        ax3.set_title('Pakistan\'s Medals vs. Game Prestige Score\n(Games with PK Medals)', fontsize=12)
        ax3.set_xlabel('Game Prestige Score')
        ax3.set_ylabel('Pakistan Medals (PK)')
        ax3.legend(title='Prestige Category')
        plt.tight_layout()
        
        st.pyplot(fig3)
    
    with col2:
        st.subheader("Distribution of Prestige Categories")
        
        # Count plot
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.countplot(x='Prestige Category', data=df_pk_medals, 
                     order=df['Prestige Category'].cat.categories, 
                     palette='viridis', hue='Prestige Category', legend=False, ax=ax4)
        ax4.set_title('Distribution of Prestige Categories\nfor Pakistan\'s Medals', fontsize=12)
        ax4.set_xlabel('Prestige Category')
        ax4.set_ylabel('Number of Games')
        plt.tight_layout()
        
        st.pyplot(fig4)
    
    # Summary statistics
    st.subheader("Pakistan's Performance Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Low Prestige Games", len(df_pk_medals[df_pk_medals['Prestige Category'] == 'Low']))
    with col2:
        st.metric("Medium Prestige Games", len(df_pk_medals[df_pk_medals['Prestige Category'] == 'Medium']))
    with col3:
        st.metric("High Prestige Games", len(df_pk_medals[df_pk_medals['Prestige Category'] == 'High']))
    
    # Display sample data
    with st.expander("View Pakistan's Medal-Winning Games"):
        st.dataframe(df_pk_medals[['Games', 'Game Prestige Score', 'PK', 'Prestige Category']].sort_values('Game Prestige Score', ascending=False))

# Footer
st.markdown("---")
st.markdown("### About this Dashboard")
st.write("This dashboard provides comprehensive analysis of medal distributions across different countries and prestige categories, with special focus on Pakistan's performance.")
