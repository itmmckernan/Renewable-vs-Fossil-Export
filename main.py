import plotly.express as px
import pandas as pd
import numpy as np

# https://ourworldindata.org/grapher/share-electricity-renewables
renewable = pd.read_csv('renewable energy.csv')
# https://data.worldbank.org/indicator/TX.VAL.FUEL.ZS.UN
fuel = pd.read_csv('fuel_exports.csv')

renewable = renewable[renewable['Code'] != '']

primaryFrame = pd.DataFrame()

for country in dict.fromkeys(renewable['Code']):
    if pd.isnull(country) or country == 'LAO':
        continue
    renewableAverageCountry = np.average(renewable[renewable['Code'] == country]['Renewables'])
    fossilAverageCountry = np.nanmean(fuel[fuel['Country Code'] == country][[str(x) for x in range(1960, 2016)]])
    primaryFrame = primaryFrame.append({'Code': country,
                                        'Country': renewable[renewable['Code'] == country]['Entity'].iloc[0],
                                        'Percentage of Renewable Energy': renewableAverageCountry,
                                        'Percentage of Economy That is Fossil Fuel Exports': fossilAverageCountry},
                                       ignore_index=True)

renewableAverage = primaryFrame[primaryFrame['Code'] != np.nan]

graph = px.scatter(primaryFrame, y='Percentage of Renewable Energy', x='Percentage of Economy That is Fossil Fuel '
                                                                       'Exports',
                   hover_name='Country', trendline='ols',
                   title="Fossil Fuel Exports Versus a Country's renewable export, for all countries in the world "
                         "except Laos")
graph.show()
graph.write_html('index.html')
