## COVID-19 Dashboard

Connie Xiao

---

**Real-Time Global COVID-19 Dashboard** 

### Abstract
---

There are countless dashboards displaying the data and statistics of COVID-19, such as the John Hopkins dashboard that provides extremely detailed analysis and visualizations. It can get overwhelming with the amount of data presented to a person who just wants the jist of whats going on. As a person who is interested in the field of healthcare analytics, I wanted to explore COVID-19 data and create a dashboard of my own. There are three priorities to this project:

1. User-friendly dashboard that gets the point across
2. Interactive/animated dashboard to get users engaged
3. Providing up-to-date data

### Data
---

Data was collected from CSSE at John Hopkin's [github](https://github.com/CSSEGISandData/COVID-19). They provided up-to-date data that users like us can retrieve and analyze. I collected 5 files from their github:

- Confirmed cases: 279 rows, 606 columns
- Recovered cases: 264 rows, 606 columns
- Death cases: 279 rows, 606 columns
- Cases by country: 195 rows, 16 columns
- Delta variant cases: 152306 rows, 17 columns

### Results
--- 

A pipeline was created by retrieving data via github and stored into SQLAlchemy database, dataframes were created by querying to SQLite. Everytime the app is launched, it will automatically get the latest updated dataset from John Hopkin's github. Columns are cleaned and only important features were used. Essentially majority of the displays in the dashboard are glorified exploratory data analysis. Then I got a list of all the countries listed in the country's file. I wanted the app to display statistics for overall confirmed cases, death cases, and recovered cases, as well as daily cases. A website called 'Flourish' is awesome at making interactive and animated data visualizations. Using Flourish, a world map was created to show the mortality rate for each country and I also created a bar graph race for time series to see how fast and how much the infection has spread across each country. Next I wanted to display the top 20 countries with the most infections, via death and confirmed cases. Finally I wanted to display visuals for each country individually, and that was accomplished using pivot tables. Total confirmed cases, death, and recovered cases are displayed and a graph showing daily new cases (including the delta variant) are used. Here is the link to my dashboard: [COVID-19 DASHBOARD](https://covid-19-dashboard-coxiao.herokuapp.com/)

### Tools
---
- Pandas
- Plotly Express
- SQLAlchemy
- Streamlit
- Heroku
