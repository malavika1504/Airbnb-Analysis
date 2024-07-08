import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
pd.set_option('display.max_columns', None)
import plotly.express as px
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

#setting page configuration
st.set_page_config(page_title="AirBnb-Analysis", page_icon=":herb:", layout="wide")


def datafr():
    df= pd.read_csv("C:/Users/DELL/Desktop/p4/Airbnb.csv")
    return df

df= datafr()


# Creating option menu in the side bar
with st.sidebar:
    SELECT = option_menu("Menu", ["Home","Explore Data"],
                           icons=["house","graph-up-arrow","bar-chart-line"],
                           menu_icon="menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "18px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#6495ED"}})
    


# HOME PAGE
if SELECT == "Home":
    st.markdown("<h1 style='text-align: center;color:red;'>Airbnb Analysis</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <style>
        hr.rainbow {
            border: 0;
            height: 4px;
            background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
            margin-top: 10px;}
    </style>
    <hr class="rainbow">""", unsafe_allow_html=True)
    
    col1,col2=st.columns(2)
    with col1:
        st.markdown("""
        <ul style='text-align: left;'>
            <li style='color: #B5D5C5; font-size: 20px;'>Welcome to the Airbnb Analysis Dashboard! This interactive platform provides insights into Airbnb data, helping you explore various trends and patterns in the travel and property management industry.</li>
            <li style='color: #FFBABA; font-size: 20px;'>Airbnb is a website where you can rent a place to stay, like someone's house or apartment, for a short period. It's popular because it offers a wide variety of places to stay in different locations around the world, often at different prices than hotels.</li>
            <li style='color: #E7D4B5; font-size: 20px;'>Reviews can give you insights into the property and the host’s hospitality. Look for detailed reviews that mention cleanliness, amenities, and the accuracy of the listing description.</li>
            <li style='color: #E1AFD1; font-size: 20px;'>Understand the cancellation policy of the property before booking. Some listings offer flexible cancellation, while others may have stricter policies.</li>
        </ul>""",unsafe_allow_html=True)

    
    with col2:
        image_path = "C:/Users/DELL/Desktop/p4/1.jpeg"
        # Open the image using PIL (Python Imaging Library)
        img = Image.open(image_path)
        # Display the image with adjusted height and width
        st.image(img, width=600, use_column_width=False)

    st.markdown("""<h1 style='font-size: 25px; color: #C5EBAA;'>Objectives:</h1>""",unsafe_allow_html=True)

    st.markdown("""<ul style='text-align: left;'>
        <li style='color: #B5C0D0; font-size: 18px;'>Connect to MongoDB Atlas and retrieve the Airbnb dataset efficiently.</li>
        <li style='color: #B5C0D0; font-size: 18px;'>Clean the dataset by addressing missing values, duplicates, and converting data types.</li>
        <li style='color: #B5C0D0; font-size: 18px;'>Create a Streamlit app with maps showing Airbnb listing distributions, prices, ratings, etc.</li>
        <li style='color: #B5C0D0; font-size: 18px;'>Analyze price variations across locations and property types.</li>
        <li style='color: #FFEEA9; font-size: 18px;'>Visualize seasonal booking patterns using line charts and heatmaps.</li>
        <li style='color: #FFEEA9; font-size: 18px;'>Create interactive visualizations for user exploration.</li>
        <li style='color: #FFEEA9; font-size: 18px;'>Enable data filtering and drill-down features in visualizations.</li>
        <li style='color: #FFEEA9; font-size: 18px;'>Build comprehensive dashboard with Tableau or Power BI for key insights.</li>
    </ul>""",unsafe_allow_html=True)

    st.markdown("""<h1 style='font-size: 25px; color: #FFBE98;'>Technologies:</h1>""",unsafe_allow_html=True)
    st.markdown("""<ul style='text-align: left;'>
        <li style='color: #E2BFB3; font-size: 18px;'> Python, Pandas, Plotly, Streamlit, MongoDB </li></ul>""",unsafe_allow_html=True)
    
    st.markdown("""<h1 style='font-size: 25px; color: #C5EBAA;'>Domain:</h1>""",unsafe_allow_html=True)
    st.markdown("""<ul style='text-align: left;'>
        <li style='color: #EEC759; font-size: 18px;'> The project is focused on the travel industry, property management, and tourism, aiming to provide actionable insights for stakeholders involved in Airbnb listings and rentals. </li></ul>""",unsafe_allow_html=True)
    
    st.markdown("""<h1 style='font-size: 25px; color: #596FB7;'>Overview:</h1>""",unsafe_allow_html=True)
    st.markdown("""<ul style='text-align: left;'>
        <li style='color: #DDF2FD; font-size: 18px;'> This project focuses on analyzing Airbnb data using a variety of technologies and tools to derive insights into pricing, availability patterns, and location-based trends within the travel, property management, and tourism industries. </li></ul>""",unsafe_allow_html=True)



#Explore Data Page
if SELECT == "Explore Data":
    fil = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
    if fil is not None:
        filename = fil.name
        st.write(filename)
        df = pd.read_csv(filename, encoding="ISO-8859-1")
        


    st.sidebar.header('Filter Options')
    selected_countries = st.sidebar.multiselect("Select the Country", df["country"].unique(), default=df["country"].unique())
    selected_room_types = st.sidebar.multiselect("Select the Room Type", df["room_type"].unique(), default=df["room_type"].unique())
    min_price, max_price = st.sidebar.slider('Select Price Range', min_value=int(df['price'].min()), max_value=int(df['price'].max()), value=(int(df['price'].min()), int(df['price'].max())))
    selected_property_types = st.sidebar.multiselect("Select the Property Type", df["property_type"].unique(), default=df["property_type"].unique())



    # Filter the DataFrame based on selected countries, room types, property types, and price range
    df_filtered = df[
        (df["country"].isin(selected_countries)) &
        (df["room_type"].isin(selected_room_types)) &
        (df["price"].between(min_price, max_price)) &
        (df["property_type"].isin(selected_property_types))]

    df_filtered.reset_index(drop=True, inplace=True)

    # Creating KPIs
    avg_price = (df["price"]).mean()
    total_data = int(df["_id"].count())
    avg_reviews_per_property = (df["number_of_reviews"]).mean()

    with st.container():
        # Create three columns for KPIs
            kpi1, kpi2, kpi3 = st.columns(3)

            # Fill in those three columns with respective metrics or KPIs
            kpi1.metric(
                label="Average Price ",
                value=f"${round(avg_price, 5)}",
                delta=round(avg_price) - 100,)
            
            kpi2.metric(
                label="Total Data ",
                value=int(total_data),
                delta=total_data - 100,)
            
            kpi3.metric(
                label="Average Reviews per Property ",
                value=f"{round(avg_reviews_per_property, 2)}",
                delta=round(avg_reviews_per_property-10, 2),)



    ch_col1,ch_col2=st.columns(2)

    with ch_col1:
        # Group by property type and calculate sums
        df1 = df_filtered.groupby("property_type")[["price","review_scores", "number_of_reviews"]].sum()
        df1.reset_index(inplace=True)  # Reset the index after grouping

        # Plot the bar chart
        fig_bar = px.bar(
            df1, x='property_type', y="price", title="Price Distribution by Property Type",text=['{:,}'.format(x) for x in df1["price"]],
            hover_data=["number_of_reviews","review_scores"], color_discrete_sequence=px.colors.sequential.Redor_r,
            width=600, height=500
        )
        st.plotly_chart(fig_bar)


    # Place the radio button in the first column
    with ch_col2:
        a = st.radio("Select the visualization", ['Pie', 'Bar'])

    # Depending on the selection, display either a pie chart or a treemap
    if a == "Pie":
        # Pie chart for price distribution by country
        fig = px.pie(df_filtered, values='price', names='country', title='Price Distribution by Country')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        with ch_col2:
            st.plotly_chart(fig, use_container_width=True)
    elif a == "Bar":
        # Bar for price distribution by country
        fig = px.bar(df_filtered, x='country', y='price', title='Price Distribution by Country',
                        hover_data=['country_code'],color_discrete_sequence=px.colors.qualitative.T10,color='country')
        with ch_col2:
            st.plotly_chart(fig, use_container_width=True)

        
    ch_col1,ch_col2=st.columns(2)
    with ch_col1:
        # Group by property type and calculate sums
        df1 = df_filtered.groupby(["property_type"]).size().reset_index(name="listings").sort_values(
                        by='listings', ascending=False)
        df1.reset_index(inplace=True)

        # Plot the bar chart
        fig = px.bar(df1,
                    title='Total Listings in Each Property Types',x='property_type',y='listings',color='property_type',
                    color_discrete_sequence=px.colors.sequential.Magenta,width=100,height=500)
        st.plotly_chart(fig, use_container_width=True)

    with ch_col2:
        # Group by room type and calculate sums
        df1= df_filtered.groupby(["country", "room_type"]).size().reset_index(name="counts")
        # Plot the pie chart
        fig = px.sunburst(df1, path=['country', 'room_type'], values='counts', title='Total Listings in each Room Type by Country',
                        color_continuous_scale=px.colors.sequential.Magma,color='counts')
        fig.update_layout(font=dict(color="white", size=15),width=800, height=600,)
        fig.update_traces(textinfo='label+percent entry')
        st.plotly_chart(fig, use_container_width=True)



    ch_col1,ch_col2=st.columns(2)
    with ch_col1:
        # Group data by country and count the number of listings
        country_df = df_filtered.groupby(['country'],as_index=False)[['name']].count().rename(columns={'name': 'total_Listings'})

        # Plot the choropleth map showing total listings in each country
        fig = px.choropleth(country_df,
                            title='Total Listings in each Country',
                            locations='country',
                            locationmode='country names',
                            color='total_Listings',
                            color_continuous_scale=px.colors.sequential.Agsunset_r
                            )
        st.plotly_chart(fig, use_container_width=True)

    with ch_col2:
        # Create a scatter mapbox to show property prices and types across suburbs
        fig = px.scatter_mapbox(df_filtered, 
                            lat='latitude', 
                            lon='longitude', 
                            color='price',
                            size="price",
                            color_continuous_scale=px.colors.sequential.Agsunset,
                            hover_data=['country', 'property_type', 'price'],
                            center=dict(lat=0, lon=180),
                            zoom=0,
                            mapbox_style="open-street-map")

        # Add a title to the map
        fig.update_layout(title="Property Prices and Types Across Suburbs")
        st.plotly_chart(fig,use_container_width=True)


    ch_col1,ch_col2=st.columns(2)
    with ch_col1:
    # Calculate average price for each combination of room type and property type
        df1 = df_filtered.groupby(['room_type', 'property_type'], as_index=False)['price'].mean().sort_values(by='price')

    # Create the bar chart
        fig = px.bar(data_frame=df1,
                x='room_type',
                y='price',
                color='price',
                hover_data='property_type',
                title='Average Price in Each Room Type and Property Type')
        st.plotly_chart(fig, use_container_width=True)


    with ch_col2:  
    # Scattergeo Plot of Average Price by Country
    # Calculate average price for each country
        country_df = df_filtered.groupby('country', as_index=False)['price'].mean()

        # Create the scattergeo plot showing average price in each country
        fig = px.scatter_geo(data_frame=country_df,
                            locations='country',
                            color='price',
                            hover_data=['price'],
                            locationmode='country names',
                            size='price',
                            title='Avg Price in each Country',
                            color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig, use_container_width=True)


    ch_col1,ch_col2=st.columns(2)
    with ch_col1:
        # Group data by host response time and sum availability and price columns
        df1=df_filtered.groupby("host_response_time")[["availability_30","availability_60","availability_90","availability_365",'price']].sum()
        df1.reset_index(inplace= True)

        # Bar chart for availability based on host response time
        fig= px.bar(df1, x='host_response_time', y=['availability_30', 'availability_60', 'availability_90', "availability_365"], 
            title='AVAILABILITY BASED ON HOST RESPONSE TIME',hover_data="price",color_discrete_sequence=px.colors.sequential.Sunset_r)

        st.plotly_chart(fig,use_container_width=True)

        # Expander for detailed view of availability
        with st.expander("AVAILABILITY BASED ON HOST RESPONSE TIME"):
            st.write(df1.style.background_gradient(cmap="RdYlBu"))

    with ch_col2:
        # Select box for host response time
        host_time= st.selectbox("Select the type of host response",df["host_response_time"].unique())
        df5= df[df["host_response_time"]==host_time]
        df_bar=pd.DataFrame(df5.groupby("bed_type")[["minimum_nights","maximum_nights","price"]].sum())
        df_bar.reset_index(inplace= True)

        # Bar chart for minimum and maximum nights
        fig= px.bar(df_bar,x='bed_type', y=['minimum_nights', 'maximum_nights'],barmode='group',title='MINIMUM NIGHTS AND MAXIMUM NIGHTS',hover_data="price",
            color_discrete_sequence=px.colors.sequential.Viridis_r)
        fig.update_layout(title_font=dict(size=17, family="Muli, sans-serif"),
                            font=dict(color='#8a8d93'),
                            legend=dict(orientation="v"))
        st.plotly_chart(fig,use_container_width=True)
        
        # Expander for detailed data view
        with st.expander("MINIMUM NIGHTS AND MAXIMUM NIGHTS"):
            st.write(df_bar.style.background_gradient(cmap="Purples_r"))

with st.expander("Data"):
    pd.set_option("styler.render.max_elements", 283305)
    st.write(df.style.background_gradient(cmap='PuOr'))