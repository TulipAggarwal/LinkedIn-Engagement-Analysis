import os
import openpyxl
import json
import requests
import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage
from streamlit_lottie import st_lottie
from st_aggrid import AgGrid
from datetime import datetime
import streamlit.components.v1 as components
import altair as alt

def main_page():
    
    st.write("# LinkedIn Engagement Analysis")

    # sidebar
    st.sidebar.markdown("# LinkedIn Engagement Analysis")
    st.sidebar.markdown("**Created by Tulip Aggarwal**")
    st.sidebar.markdown("You can **start** by uploading your data on the **LinkedIn Engagement Analysis** page.")
    st.sidebar.markdown("The process for obtaining your data can be found on the **Data Directions and Instructions** page.")

    # main content
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("How engaging are your posts?")
        st.markdown("You can monitor the performance of your posts over time by analyzing their engagements, impressions, and the percentage of engagement per impression.")
        st.markdown("By clicking on any data point, you will be redirected to the link of the corresponding post.")
    with col2:
        def load_lottieurl(url:str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        lottie_animation = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_cdu97cbh.json")
        st_lottie(lottie_animation, key="animation")

def page2():
    st.write("# LinkedIn Engagement Analysis")
    # sidebar
    file1 = st.sidebar.file_uploader("Upload Engagements & Impressions File",
        type=["xlsx"],
    )
    if file1 is not None:
	# To See details
        file1_details = {"filename":file1.name, "filetype":file1.type,
                        "filesize":file1.size}
    try:
        df = pd.read_excel(file1)
        df["Date"] = pd.to_datetime(df["Date"],infer_datetime_format = True).dt.date
    except:
        df = pd.DataFrame()
    
    # code for hardcoded file upload:
    # load data
    file2 = st.sidebar.file_uploader("Upload Shares File",
        type=["csv"],
    )
    if file2 is not None:

    # To See details
        file2_details = {"filename":file2.name, "filetype":file2.type,
                        "filesize":file2.size}
	
    #st.write(file1_details)
    try:
        df2 = pd.read_csv(file2)
    except:
        df2 = pd.DataFrame()
    try:
        df2["DateTime"] = df2["Date"]
        df2["Date"] = pd.to_datetime(df2["Date"],infer_datetime_format = True).dt.date
        df2["Time"] = pd.to_datetime(df2["DateTime"], format="%Y-%m-%d %H:%M:%S").dt.time
        df2 = df2.rename({'ShareCommentary': 'Post'}, axis=1)
        df = df.merge(df2,on="Date",how="left")
        # fill in null post descriptions and urls
        fill_df = pd.DataFrame()
        fill_df["Post"] = ["No post this day." for x in range(0,df.shape[0])]
        fill_df["ShareLink"] = ["https://www.linkedin.com/feed/" for x in range(0,df.shape[0])]
        df = df.fillna(value=fill_df)
    except:
        st.markdown("")
        df["Post"] = ["Unavailable. Data required." for x in range(0,df.shape[0])]
        df["ShareLink"] = ["https://www.linkedin.com/feed/" for x in range(0,df.shape[0])]
    
    # Setting the Plot 
    st.sidebar.subheader("Setting the Plot")
    # plot variables
    plot_width = st.sidebar.slider("Plot Width", 1, 25, 7)
    plot_height = st.sidebar.slider("Plot Height", 1, 10, 2)
    try:
        #Date Slider
        min_date = min(df["Date"])
        max_date = max(df["Date"])
        date_range = (min(df["Date"]),max(df["Date"]))
        st.markdown("Hover over any point to see details. Click a data point and it will open that LinkedIn post of yours!")
        date_range  = st.slider('Select Date Range', min_value=min_date, max_value=max_date, value = (min_date,max_date)) # Getting the input.
        df = df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])] # Filtering the dataframe.
        df["Percent"] = round(100 * df["Engagements"].div(df["Impressions"]).replace(np.nan, 0),2)
        source = df

        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                fields=['Date'], empty='none')
        # The basic line
        base = alt.Chart(source,title="Engagements & Impressions").encode(
            alt.X('Date:T', axis=alt.Axis(title=None,format="%m/%d/%Y"))
        )
        line1 = base.mark_line(stroke='#86888A', interpolate='monotone').encode(
            alt.Y('Engagements',
                  axis=alt.Axis(title='Engagements', titleColor='#86888A'))
        )
        line2 = base.mark_line(stroke='#0077b5', interpolate='monotone').encode(
            alt.Y('Impressions',
                  axis=alt.Axis(title='Impressions', titleColor='#0077b5'))
        )
        lines = alt.layer(
            line1,
            line2
        ).resolve_scale(
            y = 'independent'
        )
        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart(source).mark_point().encode(
            x='Date:T',
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )
        # Draw points on the line, and highlight based on selection
        points1 = line1.mark_point(color='#86888A').encode(
            [alt.Tooltip(c) for c in ['Date:T','Engagements:Q','Impressions:Q','Percent:Q','Post:N']],
            opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
            href='ShareLink:N'
        )
        points2 = line2.mark_point(color='#0077b5').encode(
            [alt.Tooltip(c) for c in ['Date:T','Engagements:Q','Impressions:Q','Percent:Q','Post:N']],
            opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
            href='ShareLink:N'
        )
        # Draw a rule at the location of the selection
        rule = alt.Chart(source).mark_rule(color='gray').encode(
            x='Date:T',
        ).transform_filter(
            nearest
        )
        # stuff for lower
        base2 = alt.Chart(source).encode(
            alt.X('Date:T', axis=alt.Axis(title=None,format="%m/%d/%Y"))
        )
        line3 = base2.mark_line(stroke='#86888A', interpolate='monotone').encode(
            alt.Y('Percent',
                  axis=alt.Axis(title='Percent',titleColor='#86888A'))
        )
        points3 = line3.mark_point(color='#313335').encode(
            [alt.Tooltip(c) for c in ['Date:T','Engagements:Q','Impressions:Q','Percent:Q','Post:N']],
            opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
            href='ShareLink:N'
        )
        # Put the layers into a chart and bind the data
        upper = alt.layer(
            lines, selectors, points1, points2, rule
        ).properties(
            width=100*plot_width, height=100*plot_height
        ).resolve_scale(
            y = 'independent'
        )
        lower = alt.layer(
            line3, points3, rule
        ).properties(
            width=100*plot_width, height=round(0.66*100*plot_height)
        )
        # plots   
        st.altair_chart(
            alt.vconcat(
            upper,
            lower
            ).configure_point(
            size=200
            ).configure_axis(
                labelFontSize=15,
                titleFontSize=20
        ).configure_title(
            fontSize=24
        ))
        # summary stats
        engage_stats = [
            "{0:,.0f}".format(round(sum(df["Engagements"]) / (df["Date"].iloc[-1] - df["Date"].iloc[0]).days)),
            "{0:,.0f}".format(round(sum(df["Engagements"]))),
            str("{0:,.0f}".format(round(100 * (df["Engagements"].iloc[-1] - df["Engagements"].iloc[0]) / max(1,df["Engagements"].iloc[0]),2))) + "%"
        ]
        impress_stats = [
            "{0:,.0f}".format(round(sum(df["Impressions"]) / (df["Date"].iloc[-1] - df["Date"].iloc[0]).days)),
            "{0:,.0f}".format(round(sum(df["Impressions"]))),
            str("{0:,.0f}".format(round(100 * (df["Impressions"].iloc[-1] - df["Impressions"].iloc[0]) / max(1,df["Impressions"].iloc[0]),2))) + "%"
        ]
        stat_names = ["Average","Total","Change"]
        stats_df = pd.DataFrame([stat_names,engage_stats,impress_stats]).transpose()
        stats_df.columns = ["Stats Over This Period","Engagements","Impressions"]
        st.subheader("Summary Statistics")
        AgGrid(
            stats_df,
            width = 100*plot_width,
            height = round(0.66*100*plot_height),
            theme = 'fresh',
            fit_columns_on_grid_load = True
        )
        # text
        st.markdown("##")
        st.subheader("Filtered Data Table")
        # data table
        colnames = ["Date","Engagements","Impressions","Percent"]
        output_df = df
        output_df = output_df.reindex(columns=colnames)
        output_df["Engagements"] = pd.Series(["{0:,.0f}".format(val) for val in output_df["Engagements"]], index = output_df.index)
        output_df["Impressions"] = pd.Series(["{0:,.0f}".format(val) for val in output_df["Impressions"]], index = output_df.index)
        output_df["Percent"] = pd.Series(["{0:,.2f}%".format(val) for val in output_df["Percent"]], index = output_df.index)
        output_df = output_df.sort_values(by="Date",axis=0,ascending=False)
        AgGrid(
            output_df,
            width = 100*plot_width,
            theme = 'fresh',
            fit_columns_on_grid_load = True
        )
    except:
        st.markdown("**Please upload your data**")

def page3():
    st.write("# LinkedIn Engagement Analysis")

    #Socials Connection
    st.sidebar.title('Connect with me -')
    # Define the HTML code for the buttons
    linkedin_button = '<a href="https://www.linkedin.com/in/tulipaggarwal/" target="_blank" style="text-align: center; margin: 0px 10px; padding: 5px 10px; border-radius: 5px; color: white; background-color: #0077B5; text-decoration: none">LinkedIn</a>'
    github_button = '<a href="https://github.com/TulipAggarwal" target="_blank" style="text-align: center; margin: 0px 10px; padding: 5px 10px; border-radius: 5px; color: white; background-color: #24292E; text-decoration: none">GitHub</a>'
    # Display the buttons in the app
    st.sidebar.markdown(f'{linkedin_button} {github_button} ', unsafe_allow_html=True)

    #Contact form
    st.sidebar.markdown('Please fill out the form below to contact me.')

    # Define the form fields
    with st.sidebar.form('Contact Form'):
        name = st.text_input('Name')
        email = st.text_input('Email')
        message = st.text_area('Message')
        submit_button = st.form_submit_button(label='Submit')

    # Process the form submission
    if submit_button:
        # Send the form data to a backend service, or save it to a database
        # Here, we're simply printing the form data to the console
        print(f'Name: {name}')
        print(f'Email: {email}')
        print(f'Message: {message}')
        st.success('Thank you for reaching out to me. I will get back to you as soon as possible.')
    
    #Main page
    st.subheader("Download Impressions & Engagements Data")
    st.markdown("This file provides the data necessary for plotting.")
    st.markdown("In order to download the Impressions & Engagements Data follow the following path - Your LinkedIn Profile -> Analytics & tools -> Post Impressions -> Export.")
    st.markdown("**Note:**")
    st.markdown("- After clicking Post Impressions you can edit the timeline for which you want to export the data for and this dashboard can be used with only this file if you choose.")
    st.markdown("- It is optional to upload your Shares file, but you won't be able to click through to posts from the chart.")
    st.subheader("Download Shares Data (Optional)")
    st.markdown("This data is necessary to provide the following:")
    st.markdown("- The previews of your posts' text on the charts when data points are hovered over")
    st.markdown("- The feature to click on any data point and be directed to the post you shared on a particular day")
    st.markdown("You'll have to request an archive of your data from LinkedIn following the instructions at this [link](https://www.linkedin.com/help/linkedin/answer/50191/downloading-your-account-data?lang=en). This generally takes ~24 hours, so go and request that!")
    st.markdown("In the meanwhile, it is possible to experiment with the readily accessible data on Engagements and Lmpressions from and for your LinkedIn Profile. Please refer to the instructions provided above.")

# create site
page_names_to_funcs = {
    "Welcome": main_page,
    "LinkedIn Engagement Analysis": page2,
    "Data Directions and Instructions": page3
}
selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
