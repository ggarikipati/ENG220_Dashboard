import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Title of the app
st.title("Group-009")

st.markdown("""
### Firearm Arrests Analysis Dashboard

In this project, the objective is to analyze data related to firearm arrests and compare them both annually and monthly, focusing on the state of New Mexico.  
The data used for this project was obtained directly from the **Federal Bureau of Investigation**.  

From analyzing the data, we can observe that from **2018 to 2023**, arrests related to gun violence have increased dramatically.  
This trend could be attributed to **policy failures** or to more **effective data collection and analysis methods** over the years.
""")

try:
    # Load data using consistent path pattern
    current_dir = os.path.dirname(__file__)

    monthly_csv = os.path.join(current_dir, 'weapon_arrests_monthly.csv')
    summary_csv = os.path.join(current_dir, 'weapon_arrests_summary.csv')
    averages_csv = os.path.join(current_dir, 'weapon_arrests_monthly_averages.csv')

    monthly_data = pd.read_csv(monthly_csv)
    summary_data = pd.read_csv(summary_csv)
    monthly_averages = pd.read_csv(averages_csv)

    # Year range selection
    st.markdown("### 📆 Select Year Range")
    years = sorted(monthly_data['Year'].unique())
    year_range = st.select_slider("Select Year Range", options=years, value=(min(years), max(years)))

    filtered_data = monthly_data[
        (monthly_data['Year'] >= year_range[0]) &
        (monthly_data['Year'] <= year_range[1])
    ]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Arrests", f"{filtered_data['Arrests'].sum():,.0f}")
    with col2:
        st.metric("Average Monthly Arrests", f"{filtered_data['Arrests'].mean():.1f}")
    with col3:
        yoy_change = filtered_data['YoY_Change'].mean()
        st.metric("Average YoY Change", f"{yoy_change:.1f}%")
    with col4:
        st.metric("Trend", "📈" if yoy_change > 0 else "📉")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Monthly Trends", 
        "Year-over-Year Comparison",
        "Seasonal Patterns",
        "Detailed Statistics"
    ])

    with tab1:
        st.subheader("Monthly Arrest Trends")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_data['Year_Month'], y=filtered_data['Arrests'],
                                 name='Monthly Arrests', mode='lines+markers', line=dict(color='#1f77b4')))
        fig.add_trace(go.Scatter(x=filtered_data['Year_Month'], y=filtered_data['3_Month_Avg'],
                                 name='3-Month Avg', line=dict(color='#ff7f0e', dash='dash')))
        fig.add_trace(go.Scatter(x=filtered_data['Year_Month'], y=filtered_data['12_Month_Avg'],
                                 name='12-Month Avg', line=dict(color='#2ca02c', dash='dash')))
        fig.update_layout(title='Monthly Arrests with Moving Averages', xaxis_title='Date',
                          yaxis_title='Number of Arrests', hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Year-over-Year Comparison")
        yearly_comparison = filtered_data.pivot(index='Month', columns='Year', values='Arrests')
        fig = px.line(yearly_comparison, title='Year-over-Year Comparison by Month',
                      labels={'value': 'Number of Arrests', 'Month': 'Month'})
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

        yoy_pivot = filtered_data.pivot(index='Year', columns='Month', values='YoY_Change')
        fig_heatmap = px.imshow(yoy_pivot, title='Year-over-Year Change Heatmap (%)',
                                color_continuous_scale='RdYlBu', aspect='auto')
        st.plotly_chart(fig_heatmap, use_container_width=True)

    with tab3:
        st.subheader("Seasonal Patterns")
        fig = px.bar(monthly_averages, x='Month', y='Average_Arrests', error_y='Std_Dev',
                     title='Average Monthly Arrests (All Years)',
                     labels={'Average_Arrests': 'Average Number of Arrests'})
        fig.update_layout(xaxis_title='Month', yaxis_title='Average Arrests')
        st.plotly_chart(fig, use_container_width=True)

        fig = px.box(filtered_data, x='Month', y='Arrests',
                     title='Monthly Distribution of Arrests',
                     labels={'Arrests': 'Number of Arrests'})
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("Detailed Statistics")

        st.markdown("#### 📋 Summary by Year")
        st.dataframe(summary_data.style.format({
            'Total_Arrests': '{:,.0f}',
            'Average_Monthly_Arrests': '{:.1f}',
            'Max_Monthly_Arrests': '{:.0f}',
            'Min_Monthly_Arrests': '{:.0f}',
            'Standard_Deviation': '{:.1f}'
        }))

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📊 Monthly Averages")
            st.dataframe(monthly_averages.style.format({
                'Average_Arrests': '{:.1f}',
                'Std_Dev': '{:.1f}',
                'Min_Arrests': '{:.0f}',
                'Max_Arrests': '{:.0f}'
            }))
        with col2:
            st.markdown("#### 🔄 Yearly YoY Changes")
            yearly_changes = filtered_data.groupby('Year')['Arrests'].agg([
                ('Total_Arrests', 'sum'),
                ('YoY_Change', lambda x: ((x.sum() / x.shift(12).sum()) - 1) * 100)
            ]).reset_index()
            st.dataframe(yearly_changes.style.format({
                'Total_Arrests': '{:,.0f}',
                'YoY_Change': '{:.1f}%'
            }))

    st.markdown("---")
    st.markdown(f"""
        📊 Data source: NIBRS (National Incident-Based Reporting System)  
        📅 Last updated: {pd.Timestamp.now().strftime("%Y-%m-%d")}  
        GitHub Repository: [Weapon Arrests Analysis](https://github.com/yourusername/your-repo-name)
    """)

except Exception as e:
    st.error(f"""
        ❌ Error loading data: {str(e)}

        Please ensure the following files exist in the root directory:
        - weapon_arrests_monthly.csv
        - weapon_arrests_summary.csv
        - weapon_arrests_monthly_averages.csv
    """)
