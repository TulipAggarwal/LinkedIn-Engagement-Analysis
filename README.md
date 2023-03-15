# LinkedIn Engagement Analysis

## Link to the deployed Website
[LinkedIn Engagement Analysis](https://linkedin-engagement.streamlit.app/)

## Description
This project has been designed to provide users with a comprehensive tool for tracking and analyzing the performance of their LinkedIn posts. By using this project, users can gain insights into the effectiveness of their content strategy and identify areas for improvement. One of the primary functions of this project is to monitor the performance of LinkedIn posts over a specified amount of time. Users can select a time range and the project will provide them with a detailed report of the engagement levels and impressions of their posts received during that period. The project also analyzes the engagement levels of each post, taking into account likes, comments, shares, and other interactions. This analysis can help users to identify which posts were most successful in engaging their audience and which ones may need improvement. In addition, the project calculates the percentage of engagement per impression, providing users with an understanding of the effectiveness of their content in reaching and engaging their intended audience.

## Getting Started
### Requirements
- altair==4.2.0
- pandas==1.2.3
- streamlit==1.12.2
- streamlit-aggrid==0.2.3.post2
- streamlit-lottie==0.0.3
- requests==2.28.1
- jsonschema==4.17.3
- openpyxl==3.0.10
### Execution
In your command prompt run the following commands in order to run the code on your machine -
- cd .../file
- pip install streamlit
- python -m streamlit run file.py

## Flow of Control
### def main_page() <br> 
This Python function in the code generates the main page of a LinkedIn Engagement Analysis web application using Streamlit, a Python library for creating interactive web applications. The page consists of a title, a sidebar, and two main content sections. The `st.write()` method is used to display the main title of the page, which is **LinkedIn Engagement Analysis**. The `st.sidebar.markdown()` method is used to create the sidebar of the page. It contains the title, author name, and some brief instructions for using the application. The `st.columns()` method is used to create two columns for the main content section. The left column contains a subheader and some text explaining how to monitor the performance of LinkedIn posts. The right column displays an animation using the Lottie animation library, which is loaded using the `load_lottieurl()` function. `The st_lottie()` method is used to display the animation. Overall, this code generates the main page of a LinkedIn engagement analysis web application, providing users with information about how to use the application and what they can expect to see when they analyze their LinkedIn posts.

### def page2() <br> 
This piece of code creates an interactive line chart using the `altair` library in Python, which displays the data of engagements and impressions over time for a LinkedIn page. The chart also displays tooltips on hovering over each data point that show the date, number of engagements, impressions, percentage engagement, and a link to the corresponding LinkedIn post. The first part of the code checks whether the user has uploaded the necessary files (Engagements & Impressions File and Shares File) and loads the data from them. The Engagements & Impressions file contains the data on engagements and impressions, and the Shares file contains the data on the posts made on LinkedIn. The code then sets up a sidebar that allows the user to adjust the plot width, plot height, and select the date range for which they want to view the data. The line chart is created using the Altair library and consists of two lines, one for engagements and the other for impressions, and a point for each data point. The chart uses the nearest-point selection to highlight the data point closest to the cursor on hover, and a click on a data point opens the corresponding LinkedIn post. The tooltips display the data for each data point and are linked to the corresponding point. Finally, the code generates the line chart with all the specified parameters and selections.

### def page3() <br>
The first part of the code sets up the page title and a sidebar with buttons for connecting with me on LinkedIn and GitHub, as well as a contact form. The second part of the code displays instructions for downloading two types of data from LinkedIn: impressions & engagements and shares. The page provides links to the instructions for downloading this data. Finally, if the user fills out the contact form and submits it, the function prints the form data to the console and displays a success message.

## Novelty
This project offers a unique feature that sets it apart from LinkedIn's analytics. While LinkedIn restricts users to view engagement and impressions data for a pre-determined timeframe, this project allows users to choose their own timeline. Moreover, the project presents this data in a clear and easy-to-understand way, with daily visualizations of engagements, impressions, and engagement-to-impression percentage. In addition to these visualizations, the project also provides a tabular form of data that shows changes, averages, and totals for impressions and engagements during the chosen period. This comprehensive data analysis allows users to track their LinkedIn activity and gain valuable insights into their audience engagement. Overall, this project provides an effective project for users to monitor and improve their LinkedIn presence.

## Screenshots
### Welcome Page
![image](https://user-images.githubusercontent.com/93984886/225281233-a7cfe60a-67c0-4fec-ad62-667141e78d01.png)

### LinkedIn Engagement Analysis Page
![image](https://user-images.githubusercontent.com/93984886/225281399-5e22b5d9-76c6-4d90-b619-67b43db85b24.png)
![image](https://user-images.githubusercontent.com/93984886/225281439-1cd0c0bb-ec90-4817-b094-9113e3a7a1f6.png)

### Data Directions and Instructions Page
![image](https://user-images.githubusercontent.com/93984886/225281541-cd73102a-e779-4015-ac3f-485647e25d63.png)
