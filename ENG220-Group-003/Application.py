import streamlit as st
import pandas as pd

# Title of the app
st.title('McClure Water Reservoir Level with Moving Average')

# Load CSV file named "extracted_data.csv"
try:
    df = pd.read_csv("extracted_data.csv")
    st.write("Data from extracted_data.csv:")
    st.write(df)

    # Slider for image width adjustment
    #x = st.slider(';)', min_value=10, max_value=500)
    #st.image("OIP.jpg", width=x)
    #st.write('https://docs.streamlit.io/get-started/fundamentals/main-concepts')
    


    # Bar chart visualization
    st.bar_chart(df[['Time (Days)', 'Basin Water Level (Acre ft)']].set_index('Time (Days)'))
    moving_avg = st.checkbox('Moving Average')
    if moving_avg:
        moving_avg_column = 'Basin Water Level (Acre ft)'
        window_size = 1000
        df['Moving Average'] = df[moving_avg_column].rolling(window_size).sum()/window_size
        st.write(f"Moving Average for {moving_avg_column} (Window Size: {window_size}):")
        #st.line_chart(df[['Time (Days)', moving_avg_column,'Moving Average']].set_index('Time (Days)'), color=["#2491D9","#D51616"])
        st.line_chart(df[['Time (Days)', 'Moving Average']].set_index('Time (Days)'), color=["#D51616"])


except FileNotFoundError:
    st.error("The file 'extracted_data.csv' was not found. Please ensure the file is available in the directory.")
