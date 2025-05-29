import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Health Data")

# Load data directly from file
data = pd.read_csv('./HealthData.csv') 

if data is not None:
    st.write("### Data Preview")
    st.dataframe(data)

    # Dropdown for selecting columns
    columns = data.columns.tolist()
    x_column = st.selectbox("Select X-axis column", columns)
    y_column = st.selectbox("Select Y-axis column", columns)

    # Dropdown for graph type
    graph_type = st.selectbox(
        "Select Graph Type",
        ["Line", "Scatter", "Bar", "Pie"]
    )

    # Plot button
    if st.button("Plot Graph"):
        fig, ax = plt.subplots()

        if graph_type != "Pie":
            # Dynamically scale Y-axis for numeric data
            if pd.api.types.is_numeric_dtype(data[y_column]):
                y_min, y_max = data[y_column].min(), data[y_column].max()
                padding = (y_max - y_min) * 0.1  # Add 10% padding
                y_min -= padding
                y_max += padding
            else:
                st.error("Y-axis column must be numeric for this plot type.")
                st.stop()

        if graph_type == "Line":
            ax.plot(data[x_column], data[y_column], marker='o')
            ax.set_title(f"{y_column} vs {x_column} (Line Plot)")
            plt.xticks(rotation=90)
            ax.set_ylim(y_min, y_max)

        elif graph_type == "Scatter":
            ax.scatter(data[x_column], data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Scatter Plot)")
            plt.xticks(rotation=90)
            ax.set_ylim(y_min, y_max)

        elif graph_type == "Bar":
            ax.bar(data[x_column], data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Bar Chart)")
            plt.xticks(rotation=90)
            ax.set_ylim(y_min, y_max)

        elif graph_type == "Pie":
            # Aggregate data for meaningful pie chart
            if len(data[x_column].unique()) <= 35:  # Limit unique categories
                pie_data = data.groupby(x_column)[y_column].sum()
                plt.pie(
                    pie_data,
                    labels=pie_data.index,
                    autopct='%1.1f%%',
                    startangle=90,
                )
                plt.title(f"{y_column} Distribution (Pie Chart)")
            else:
                st.error("Pie chart requires fewer unique categories in the X-axis.")

        if graph_type != "Pie":
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            st.pyplot(fig)
        else:
            st.pyplot(plt)

    st.write("Tip: Ensure the selected columns are numeric for meaningful plots.")
else:
    st.info("Please upload a CSV file to get started.")
