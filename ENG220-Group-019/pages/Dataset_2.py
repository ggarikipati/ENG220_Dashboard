import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("EPI.csv")

data = pd.read_csv("./EPI.csv")

st.write("### Data Preview")
st.dataframe(data)

columns = data.columns.tolist()
x_column = st.selectbox("Select X-axis column", columns)
y_column = st.selectbox("Select Y-axis column", columns)

graph_type = st.selectbox("Select Graph Type", ["Line", "Scatter", "Bar", "Pie"])

if st.button("Plot Graph"):
    fig, ax = plt.subplots()

    if graph_type == "Line":
        ax.plot(data[x_column], data[y_column], marker='o')
        ax.set_title(f"{y_column} vs {x_column} (Line Plot)")

    elif graph_type == "Scatter":
        ax.scatter(data[x_column], data[y_column])
        ax.set_title(f"{y_column} vs {x_column} (Scatter Plot)")

    elif graph_type == "Bar":
        ax.bar(data[x_column], data[y_column])
        ax.set_title(f"{y_column} vs {x_column} (Bar Chart)")

    elif graph_type == "Pie":
        if len(data[x_column].unique()) <= 10:
            plt.pie(data[y_column], labels=data[x_column], autopct='%1.1f%%', startangle=90)
            plt.title(f"{y_column} (Pie Chart)")
        else:
            st.error("Pie chart requires fewer unique categories in the X-axis.")

    if graph_type != "Pie":
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        st.pyplot(fig)
    else:
        st.pyplot(plt)

st.write("Tip: Ensure the selected columns are numeric for meaningful plots.")
