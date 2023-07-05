
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns


# Load the dataset
df = pd.read_csv('newcitydataset.csv')
# Add custom CSS for background color and sidebar/text color
st.markdown(
    """
    <style>
    .stApp {
        background-color:  #38598b;
    }
    .stSidebar {
        background-color: #a1dd70;
    }
    .stSidebar .sidebar-content {
        color: #a1dd70;
    }
    .stMarkdown {#a1dd70
        color: #333333;
    }
    .stBlockquote {
        color: #a1dd70;
    }
    .navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px;
        background-color: #333333;
        color: #ffffff;
        font-weight: bold;
    }
    .navbar-item {
        margin-right: 10px;
        cursor: pointer;
    }
    .navbar-item:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True
)
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://t4.ftcdn.net/jpg/01/24/20/57/240_F_124205761_iJAxo9nyhKJr0X6nDclZI37Kz99z6Lle.jpg");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
background-attachment: local;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
# Add content to the sidebar
st.sidebar.title("RMRDC PRICE MOVEMENT")
st.sidebar.text("Dashboard")

# Set up the Streamlit app
st.title("📊Commodity Price Dashboard")

# Navigation bar
st.markdown(
    """
    <div class="navbar">
        <div class="navbar-item" onclick="navigateToDashboard()">Dashboard</div>
        <div class="navbar-item" onclick="navigateToComparison()">Comparison</div>
    </div>
    <script>
    function navigateToDashboard() {
        window.location.href = "#dashboard";
    }
    function navigateToComparison() {
        window.location.href = "#comparison";
    }
    </script>
    """,
    unsafe_allow_html=True
)
# Add KPIs section
st.subheader("Key Performance Indicators")
#import streamlit as st
# CSS for navigation bar
navbar_style = """
    <style>
    .navbar {
        display: flex;
        justify-content: space-between;
        background-color: #1dd147;  /* Set the background color to red */
        padding: 10px;
        color: #ffffff;
        font-weight: bold;
    }
    .navbar-item {
        margin-right: 20px;
    }
    .navbar-item:last-child {
        margin-right: 0;
    }
    </style>
"""


# Calculate KPIs
total_commodities = len(df["COMMODITY"].unique())
total_cities = len(df["City"].unique())
total_records = len(df)

# Display navigation bar
st.markdown(navbar_style, unsafe_allow_html=True)
#st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# Add logo to sidebar
logo_url = "https://global.ariseplay.com/amg/www.thisdaylive.com/uploads/RMRDC-LOGO.png"  # Replace with your logo URL
st.sidebar.image(logo_url, use_column_width=True)
# Navigation bar content
st.markdown('<div class="navbar">\
                <div class="navbar-item">Total Commodities: {}</div>\
                <div class="navbar-item">Total Cities: {}</div>\
                <div class="navbar-item">Total Records: {}</div>\
            </div>'.format(total_commodities, total_cities, total_records), unsafe_allow_html=True)


# Display KPIs
#col1, col2, col3 = st.columns(3)
#with col1:
    #st.metric("Total Commodities", total_commodities)
#with col2:
    #st.metric("Total Cities", total_cities)
#with col3:
    #st.metric("Total Records", total_records)
# Add sidebar
st.sidebar.title("⚙️Filter Options")
# Check the data type of the 'AVERAGE' column
if df['AVERAGE'].dtype == object:
    # Clean the 'AVERAGE' column if it is of string type
    df['AVERAGE'] = df['AVERAGE'].str.replace('₦', '').astype(float)

# Create filters for month and year
months = sorted(df["Month"].unique())
selected_month = st.selectbox("Select Month to Filter", months)

years = sorted(df["Year"].unique())
selected_year = st.selectbox("Select Year to Filter", years)
filtered_data = df[(df["Month"] == selected_month) & (df["Year"] == selected_year)]

# Display filtered data
st.subheader("Filtered Price Data")
st.dataframe(filtered_data)

# Unique and sorted values for months, Year, Cities, Commodities, and commodities_type
months = sorted(df["Month"].unique())
years = sorted(df["Year"].unique())
cities = sorted(df["City"].unique())
commodities = sorted(df["COMMODITY"].unique())
commodity_types = sorted(df["Type"].unique())

# Sidebar components
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    selected_month = st.selectbox("Select Month", months, key='month_select')
with col2:
    selected_year = st.selectbox("Select Year", years, key='year_select')

with col3:
    selected_cities = st.multiselect('Select Cities', cities, key='cities_multiselect')

with col4:
    selected_commodities = st.multiselect('Select Commodities', commodities, key='commodities_multiselect')

with col5:
    selected_commodity_types = st.multiselect('Select Types', commodity_types, key='commodity_types_multiselect')
filtered_data = df[(df["Month"] == selected_month) & (df["Year"] == selected_year)]
# Check if commodities are selected
if selected_commodities:
    # Deselect commodity types
    selected_commodity_types = []

    # Filter the data based on user selections
    filtered_df = df[
        (df['City'].isin(selected_cities)) &
        (df['COMMODITY'].isin(selected_commodities)) &
        (df["Month"] == selected_month) & (df["Year"] == selected_year)
    ]
else:
    # Filter the data based on user selections
    filtered_df = df[
        (df['City'].isin(selected_cities)) &
        (df['Type'].isin(selected_commodity_types)) &
        (df["Month"] == selected_month) & (df["Year"] == selected_year)
    ]

# Calculate the minimum and maximum prices for selected commodities
min_price = filtered_df[filtered_df['COMMODITY'].isin(selected_commodities)][["MARKET (1)", "MARKET (2)", "MARKET (3)"]].min().min()
max_price = filtered_df[filtered_df['COMMODITY'].isin(selected_commodities)][["MARKET (1)", "MARKET (2)", "MARKET (3)"]].max().max()

# Plot market prices
st.subheader("📊 Market Prices")
st.markdown("This graph shows the market prices of selected commodities in the chosen cities.")
fig_market_prices = go.Figure()

if selected_commodities:
    filtered_commodities = filtered_df[filtered_df['COMMODITY'].isin(selected_commodities)]["COMMODITY"]
else:
    filtered_commodities = filtered_df[filtered_df['Type'].isin(selected_commodity_types)]["COMMODITY"]

for market_col in ["MARKET (1)", "MARKET (2)", "MARKET (3)"]:
    fig_market_prices.add_trace(go.Bar(
        x=filtered_commodities,
        y=filtered_df[filtered_df['COMMODITY'].isin(filtered_commodities)][market_col],
        name=market_col
    ))

fig_market_prices.update_layout(
    xaxis_title='Commodity',
    yaxis_title='Market Price'
)
st.plotly_chart(fig_market_prices)

st.markdown("The bar chart above visualizes the market prices of the selected commodities across different cities.")

# Display minimum and maximum prices
st.subheader("Minimum and Maximum Prices")
st.write(f"Minimum Price: {min_price}")
st.write(f"Maximum Price: {max_price}")

# Plot total price
st.subheader("📊 Total Price")
st.markdown("This graph shows the total prices of selected commodities in the chosen cities.")
fig_total_price = go.Figure(go.Bar(
    x=filtered_df[filtered_df['COMMODITY'].isin(selected_commodities)]["COMMODITY"],
    y=filtered_df[filtered_df['COMMODITY'].isin(selected_commodities)]["TOTAL"]
))
fig_total_price.update_layout(
    xaxis_title='Commodity',
    yaxis_title='Total Price'
)
st.plotly_chart(fig_total_price)
st.markdown("The bar chart above visualizes the total prices of the selected commodities across different cities.")


# Sidebar components
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    selected_month2 = st.selectbox("Select Month", months, key='month_select_new')

with col2:
    selected_year2 = st.selectbox("Select Year", years, key='year_select_new')

with col3:
    selected_cities2 = st.multiselect('Select Cities', cities, key='cities_multiselect_new')

with col4:
    selected_commodities2 = st.multiselect('Select Commodities', commodities, key='commodities_multiselect_new')
    
with col5:
    selected_commodity_type2 = st.multiselect('Select Type', commodity_types, key='commodities_Type_multiselect_new')

filtered_data = df[
    (df['Month'] == selected_month2) &
    (df['Year'] == selected_year2) &
    (df['City'].isin(selected_cities2)) &
    (
        (df['Type'].isin(selected_commodity_type2)) |
        (df['COMMODITY'].isin(selected_commodities2))
    )
]

# Display filtered data if month and year are selected
if selected_month2 and selected_year2:
    # Display filtered price data
    st.subheader("Filtered Price Data Comparison")
    st.dataframe(filtered_data)

    # Group the data by city and commodity and calculate the average market value
    grouped_df = filtered_data.groupby(['City', 'COMMODITY'])['AVERAGE'].mean().reset_index()

    # Calculate minimum and maximum prices
    min_price = grouped_df['AVERAGE'].min()
    max_price = grouped_df['AVERAGE'].max()

    # Display minimum and maximum prices
    st.subheader("Minimum and Maximum Prices")
    st.write(f"Minimum Price: {min_price}")
    st.write(f"Maximum Price: {max_price}")

    # Plot the graph
    if not selected_commodities2:  # Check if selected_commodities2 is empty
        fig = px.bar(grouped_df, x='COMMODITY', y='AVERAGE', color='City', barmode='group')
        fig.update_layout(
            title='Distribution of Commodity Types in Selected Cities',
            xaxis_title='Commodity Type',
            yaxis_title='Average Market Value',
            xaxis_tickangle=45
        )
        st.plotly_chart(fig)
    else:
        fig = px.bar(grouped_df, x='COMMODITY', y='AVERAGE', color='City', barmode='group')
        fig.update_layout(
            title='Distribution of Commodities in Selected Cities',
            xaxis_title='Commodity',
            yaxis_title='Average Market Value',
            xaxis_tickangle=45
        )
        st.plotly_chart(fig)


st.markdown("The bar chart above visualizes the total prices of the selected commodities across different cities.")
# Add new code to load a dataset with columns minerals, price, and mineral_type by the right sidebar and plot its Plotly bar charts separately
mineral_data = pd.read_csv("MineralsAllcsv2.csv")

# Add a sidebar to select the type of mineral to display
mineral_type = st.sidebar.selectbox("Select Mineral Type", mineral_data["Mineral Type"].unique())

# Distribution of Minerals
st.subheader("Distribution of Minerals")
## Filter the mineral data by the selected mineral type
filtered_mineral_data = mineral_data[mineral_data["Mineral Type"] == mineral_type]

## Plot a bar chart of the market prices for the selected mineral type
fig_market_prices_mineral = go.Figure(go.Bar(
    x=filtered_mineral_data[" Mineral"],
    y=filtered_mineral_data["Price"],
    name=mineral_type
))
st.plotly_chart(fig_market_prices_mineral)

## Plot a bar chart of the total price for the selected mineral type
fig_total_price_mineral = go.Figure(go.Bar(
    x=filtered_mineral_data[" Mineral"],
    y=filtered_mineral_data["Price"],
    name=mineral_type
))

st.plotly_chart(fig_total_price_mineral)
#selected_commodity_types = st.sidebar.multiselect("Select Commodity Types", ["Type A", "Type B", "Type C"])

# Existing code...

uploaded = st.sidebar.file_uploader("Upload New Dataset", type="csv")
new_dataset_uploaded = False

if uploaded is not None:
    new_data = pd.read_csv(uploaded)
    if len(selected_commodity_types) > 0:
        new_data["Type"] = selected_commodity_types[:len(new_data)]  # Assign selected commodity types
    data = pd.concat([df, new_data], ignore_index=True)
    data.to_csv("newcitydataset.csv", index=False)
    st.sidebar.success("New dataset uploaded successfully!")
    new_dataset_uploaded = True

# Refresh the filtered data only if a new dataset has been uploaded
if new_dataset_uploaded:
    filtered_data = data[(data["Month"] == selected_month) & (data["Year"] == selected_year)]
    filtered_data = filtered_data[filtered_data["Type"].isin(selected_commodity_types)]

# Update the market prices figure using the filtered data
fig_market_prices = go.Figure()
for market_col in ["MARKET (1)", "MARKET (2)", "MARKET (3)"]:
    fig_market_prices.add_trace(go.Bar(
        x=filtered_data["COMMODITY"],
        y=filtered_data[market_col],
        name=market_col
    ))

# Hide Streamlit footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
footer:after{visibility: visible;
      content:'Copyright @RMRDC 2023';
      display:block;
      position:relative;
      color: #1dd147;
      padding:5px
      top:3px;
}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)







