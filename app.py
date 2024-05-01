import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('startup_cleaned.csv')
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['year'] = df['Date'].dt.year
df['month'] =  df['Date'].dt.month

st.set_page_config(layout='wide', page_title='Startup Analysis')

#data cleaning
#df['Investor'] = df['Investor'].fillna('')


def load_overall_analysis():
    st.title('Overall Analysis')

    #total Invested amount
    total = round(df['amount'].sum())
    
    #max amount infused in a startup
    max_funding = round(df.groupby('startup')['amount'].max().sort_values(ascending = False).head(1).values[0])

    #Average ticket size
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())

    #total funded startups
    num_startup = df['startup'].nunique()
    

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + 'Cr')
    with col2:
        st.metric('Max Funding', str(max_funding) + 'Cr')
    with col3:
        st.metric('Average Funding', str(avg_funding) + 'Cr')
    with col4:
        st.metric('Funded Startup', str(num_startup))

    st.header('MoM Graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    elif selected_option == 'Count':
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    
    temp_df['x_axis'] = temp_df['month'].astype(str) + "-" + temp_df['year'].astype(str)
    
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig3)


def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investment of the investor
    last_5_df = df[df['Investor'].str.contains(investor)].head()[['Date','startup','subvertical' ,'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last_5_df)

    col1, col2 = st.columns(2)
    with col1:
        # Biggest investment
        big_series = df[df['Investor'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending = False).head(5)
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)

        st.pyplot(fig)

    with col2:
        vertical_series = df[df['Investor'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(ascending = False).head(5)
        st.subheader('Top 5 Sector Invested In')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels = vertical_series.index, autopct = "%0.01f%%")

        st.pyplot(fig1)

    
    year_series = df[df['Investor'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('Year on Year Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)

    st.pyplot(fig2)


# Data Cleaning
#df['Investors Name'] = df['Investors Name'].fillna('undisclosed')

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'Startup':
    st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup')
    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select startup', sorted(set(df['Investor'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Detail')
    if btn2:
        load_investor_details(selected_investor)



