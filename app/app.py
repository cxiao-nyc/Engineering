#importing libraries
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from sqlalchemy import create_engine


#loading data into SQLite database and extracting data
def load_data():
    death = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    
    confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

    recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

    country = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')
    
    delta = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_time.csv', parse_dates=['Last_Update'])

    return death, confirmed, recovered, country, delta

death, confirmed, recovered, country, delta= load_data()


engine = create_engine('sqlite:///covid.db')

# create table for each df in DB
death.to_sql('death_data', con=engine, if_exists='replace', index=False)
confirmed.to_sql('confirmed_data', con=engine, if_exists='replace', index=False)
recovered.to_sql('recovered_data', con=engine, if_exists='replace', index=False)
country.to_sql('country_data', con=engine, if_exists='replace', index=False)
delta.to_sql('delta_data', con=engine, if_exists='replace', index=False)

death_df = pd.read_sql('SELECT * from death_data', engine)
confirmed_df = pd.read_sql('SELECT * from confirmed_data', engine)
recovered_df = pd.read_sql('SELECT * from recovered_data', engine)
country_df = pd.read_sql('SELECT * from country_data', engine)
delta_df = pd.read_sql('SELECT * from delta_data', engine)


#reducing columns for analyzing purposes
delta_df = delta_df[['Country_Region', 'Delta_Confirmed', 'Last_Update']]

# renaming the df column names to lowercase
country_df.columns = map(str.lower, country_df.columns)
confirmed_df.columns = map(str.lower, confirmed_df.columns)
death_df.columns = map(str.lower, death_df.columns)
recovered_df.columns = map(str.lower, recovered_df.columns)
delta_df.columns = map(str.lower, delta_df.columns)

# renaming some columns for clarity 
confirmed_df = confirmed_df.rename(columns={'province/state': 'state', 'country/region': 'country', 'lat': 'lat', 'long': 'lon'})
recovered_df = recovered_df.rename(columns={'province/state': 'state', 'country/region': 'country'})
death_df = death_df.rename(columns={'province/state': 'state', 'country/region': 'country'})
country_df = country_df.rename(columns={'country_region': 'country'})
delta_df = delta_df.rename(columns={'last_update': 'date', 'country_region': 'country_name'})

#list of all countries
list_all_countries = list(confirmed_df['country'].unique())

#total cases, deaths and recovery 
confirmed_total = int(country_df['confirmed'].sum())
deaths_total = int(country_df['deaths'].sum())
recovered_total = recovered_df.iloc[:,4:].max(axis=1).sum()

#number of cases, death, recovered today
confirmed_today = int(confirmed_df[confirmed_df.columns[-1]].sum() - confirmed_df[confirmed_df.columns[-2]].sum())
confirmed_sign = '+' if confirmed_today>=0 else '-'
death_today = int(death_df[death_df.columns[-1]].sum() - death_df[death_df.columns[-2]].sum())
death_sign = '+' if death_today>=0 else '-'
recovered_today = int(recovered_df[recovered_df.columns[-1]].sum() - recovered_df[recovered_df.columns[-2]].sum())
recovered_sign = '+' if recovered_today>=0 else '-'


#for a better app performance
st.cache(persist=True) 

image = Image.open('masks.jpeg')
st.image(image)

st.markdown(
    """<head>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
  <title>COVID-19 Dashboard | Connie Xiao</title>
  <style>
  body{
      background-color: #fff;
      font-size: 40px;
  }
  </style>
</head>""", unsafe_allow_html=True
)

st.markdown('''<div class="jumbotron text-center" style='background-color: #fff'>
  <h1 style="margin: auto; width: 100%; color: #000 ">COVID-19 Dashboard</h1>
  <h4 style='margin: auto; font-weight: 400; text-align: center; width: 100%; color: #000'>Connie Xiao</h4>
   <h4></h4><p style='margin: auto; font-weight: 200; text-align: center; width: 100%; color: #000'>Data Source: CSSE, John Hopkins University</p>
    <p style='margin: auto; font-weight: 400; text-align: center; width: 100%; color: #000'>Last Updated: ''' + str(country_df['last_update'][0]) + '''</p>
</div>

<div class="jumbotron text-center" style='padding: 0px'>
  <div class="row" style="background-color: #fff;width: 100%; margin: auto;">
  <p style="margin: auto; font-weight: 500; color: #000; text-align: center; width: 100%; font-size: 50px">Global Stats</p>
    <div class="col-sm-4">
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: #000'>Total Confirmed</p>
      <p style='text-align: center; font-size: 15px; color: #000'>[''' + str(confirmed_sign) + str(confirmed_today) + ''']</p>
      <p style='text-align: center; font-size: 35px; font-weight: bold; color: #000'>''' + str(confirmed_total) + '''</p>
    </div>
    <div class="col-sm-4" style='background-color: #fff; border-radius: 5px'>
      <p style='text-align: center; font-weight: 400 ; color: #000'>Total Deaths</p>
      <p style='text-align: center; font-size: 15px; color: #e73631'>[''' + str(death_sign) + str(death_today) + ''']</p>
      <p style='text-align: center; font-size: 35px; font-weight: bold; color: #e73631'>''' + str(deaths_total) + '''</p>
    </div>
    <div class="col-sm-4">
      <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: #000'>Total Recovered</p>
      <p style='text-align: center; font-size: 15px; color: #70a82c'>[''' + str(recovered_sign) + str(recovered_today) + ''']</p>
      <p style='text-align: center; font-size: 35px; font-weight: bold; color: #70a82c'>''' + str(recovered_total) + '''</p>
    </div>
  </div>
</div>
''', unsafe_allow_html=True);

st.markdown(
    '''<iframe src='https://flo.uri.sh/visualisation/7272359/embed' title='Interactive or visual content' class='flourish-embed-iframe' frameborder='0' scrolling='no' style='width:100%;height:600px;' sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation'></iframe><div style='width:100%!;margin-top:4px!important;text-align:right!important;'><a class='flourish-credit' href='https://public.flourish.studio/visualisation/7272359/?utm_source=embed&utm_campaign=visualisation/7272359' target='_top' style='text-decoration:none!important'><img alt='Made with Flourish' src='https://public.flourish.studio/resources/made_with_flourish.svg' style='width:105px!important;height:16px!important;border:none!important;margin:0!important;'> </a></div>''',
    unsafe_allow_html=True
)

st.markdown(
    '''<iframe src='https://flo.uri.sh/visualisation/7263516/embed' title='Interactive or visual content' class='flourish-embed-iframe' frameborder='0' scrolling='no' style='width:100%;height:600px;' sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation'></iframe><div style='width:100%!;margin-top:4px!important;text-align:right!important;'><a class='flourish-credit' href='https://public.flourish.studio/visualisation/7263516/?utm_source=embed&utm_campaign=visualisation/7263516' target='_top' style='text-decoration:none!important'><img alt='Made with Flourish' src='https://public.flourish.studio/resources/made_with_flourish.svg' style='width:105px!important;height:16px!important;border:none!important;margin:0!important;'> </a></div>''',
    unsafe_allow_html=True
)

st.title('Current Top 20 Countries')
country_stats_df = country_df[['country', 'last_update','confirmed', 'deaths']]

fig = go.FigureWidget(layout=go.Layout())
def highlight_col(x):
    red = 'color: #e73631'
    green = 'color: #70a82c'
    df1 = pd.DataFrame('', index=x.index, columns=x.columns)
    df1.iloc[:, 2] = green
    df1.iloc[:, 3] = red
    return df1

def show_latest_cases(n):
    n = int(n)
    if n>0:
        return country_stats_df.sort_values('confirmed', ascending= False).reset_index(drop=True).head(n).style.apply(highlight_col, axis=None).set_properties(**{'text-align': 'left', 'font-size': '15px'})

to_show = show_latest_cases(21)
st.table(to_show)

def plot_cases_of_a_country(country):
    labels = ['Confirmed', 'Deaths', 'Recovered']
    colors = ['black', 'red', 'green']
    mode_size = [8, 8, 8]
    line_size = [5, 5, 5]
    
    df_list = [confirmed_df, death_df, recovered_df]
    
    fig = go.Figure();
    
    for i, df in enumerate(df_list):
        if country == 'World' or country == 'world':
            x_data = np.array(list(df.iloc[:, 4:].columns))
            y_data = np.sum(np.asarray(df.iloc[:,4:]),axis = 0)
            
        else:    
            x_data = np.array(list(df.iloc[:, 4:].columns))
            y_data = np.sum(np.asarray(df[df['country'] == country].iloc[:,4:]),axis = 0)
            
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i]),
        connectgaps=True,
        text = "Total " + str(labels[i]) +": "+ str(y_data[-1])
        ));
    
    fig.update_layout(
        title="COVID 19 Cases: " + country,
        xaxis_title='Date',
        yaxis_title='# of Cases',
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='#fff',
        plot_bgcolor='rgba(0,0,0,0)'
    );
    
    fig.update_yaxes(type="linear")
    return fig

delta_pivoted_df = delta_df.pivot_table(index='date', columns='country_name', values='delta_confirmed', aggfunc=np.sum)
delta_pivoted_df.reset_index(level=0, inplace=True)
delta_world_df = pd.DataFrame()
delta_world_df['World'] = delta_pivoted_df[delta_pivoted_df.columns].sum(axis=1)
delta_world_df['date'] = delta_pivoted_df['date']

def plot_new_cases_of_country(Country):
    country = Country
    if(country == 'World' or country == 'world'):
        y_data = np.array(list(delta_world_df[country]))
    elif(country == 'US'):
        y_list = list(delta_pivoted_df[country])
        y_list = [x / 2 for x in y_list]
        y_data = np.array(y_list)
    else:
        y_data = np.array(list(delta_pivoted_df[country]))
    x_data = np.array(list(delta_df['date']))
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x_data,
        y=y_data,
        name='Daily Increase',
        marker_color='crimson',
        hovertemplate='Date: %{x}; \n  New Cases: %{y}',
    ))
    fig.update_layout(
            title="Daily Cases: " + country,
            xaxis_title='Date',
            yaxis_title='# of New Cases',
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='#fff',
            plot_bgcolor='rgba(0,0,0,0)',
    );
    fig.update_yaxes(type="linear")
    return fig


def show_country_stats(country):

    country_confirmed_df = confirmed_df[confirmed_df['country'] == country]
    country_death_df = death_df[death_df['country'] == country]
    country_recovered_df = recovered_df[recovered_df['country'] == country]

    country_confirmed = country_confirmed_df[country_confirmed_df.columns[-1]].sum()
    country_death = country_death_df[country_death_df.columns[-1]].sum()
    country_recovered = country_recovered_df.iloc[:,4:].max(axis=1).sum()

    country_confirmed_today = int(country_confirmed_df[country_confirmed_df.columns[-1]].sum()) - int(country_confirmed_df[country_confirmed_df.columns[-2]].sum())

    country_death_today = int(country_death_df[country_death_df.columns[-1]].sum()) - int(country_death_df[country_death_df.columns[-2]].sum())
    
    country_recovered_today = int(country_recovered_df[country_recovered_df.columns[-1]].sum()) - int(country_recovered_df[country_recovered_df.columns[-2]].sum())

    country_confirmed_today_sign = '+' if country_confirmed_today>=0 else ''
    country_death_today_sign = '+' if country_death_today>=0 else ''
    country_recovered_today_sign = '+' if country_recovered_today else ''
    

    
    st.markdown(
        '''
        <h1></h1>
    <div class="jumbotron text-center" style='padding: 0px; background-color: #fff'>
    <div class="row" style="background-color: #fff;width: 100%; margin: auto;">
        <div class="col-sm-4">
        <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: #000'>Total Confirmed</p>
        <p style='text-align: center; font-size: 15px; color: #000'>[''' + str(country_confirmed_today_sign) + str(country_confirmed_today) + ''']</p>
        <p style='text-align: center; font-size: 35px; font-weight: bold; color: #000'>''' + str(country_confirmed) + '''</p>
        </div>
        <div class="col-sm-4" style='background-color: #fff; border-radius: 5px'>
        <p style='text-align: center; font-weight: 400 ; color: #000'>Total Deaths</p>
        <p style='text-align: center; font-size: 15px; color: #e73631'>[''' + str(country_death_today_sign) + str(country_death_today) + ''']</p>
        <p style='text-align: center; font-size: 35px; font-weight: bold; color: #e73631'>''' + str(country_death) + '''</p>
        </div>
        <div class="col-sm-4">
        <p style='text-align: center; background-color: #fff; font-weight: 400 ;color: #000'>Total Recovered</p>
        <p style='text-align: center; font-size: 15px; color: #70a82c'>[''' + str(country_recovered_today_sign) + str(country_recovered_today) + ''']</p>
        <p style='text-align: center; font-size: 35px; font-weight: bold; color: #70a82c'>''' + str(country_recovered) + '''</p>
        </div>
    </div>
    <br><p style="margin: auto; font-weight: 400; font-size-25px; background-color #fff; text-align: center; width: 100%; color: #0000;">(Graphs are interactive. Drag over graph to zoom in and double tap to zoom out.)</p>
    </div>
        ''',
        unsafe_allow_html=True
    )

st.title('Select a Country')

default_index = list_all_countries.index('US')
country_name = st.selectbox('Country', list_all_countries, default_index)
to_show_overall = plot_cases_of_a_country(country_name)
to_show_daily = plot_new_cases_of_country(country_name)
show_country_stats(country_name)

st.write(to_show_overall)
st.write(to_show_daily)



    