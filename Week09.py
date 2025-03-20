########################
# Week 9 Code
#
#

''' 
#####
# Plot by country
#
# We can use the package Geopandas to plot by country.
# Need to find replacement for natural earth dataset

import geopandas as gpd
country_sales = df.groupby('Country')['Sales'].sum().reset_index()

# Load world map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the sales data with the world map
world_sales = world.merge(country_sales, how="left", left_on="name", right_on="Country")

# Plotting the map
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world_sales.boundary.plot(ax=ax, linewidth=1)
world_sales.plot(column='Sales', ax=ax, legend=True,
                 legend_kwds={'label': "Total Sales by Country",
                              'orientation': "horizontal"},
                 cmap='OrRd', missing_kwds={"color": "lightgrey", "label": "No Sales Data"})

plt.title('Sales Performance by Country')
plt.show()'


'''
####
# Visualise monthly sales trends by using a line plot
# Calculate monthly sales by resampling (resampling is used to regularise our data in prparation for the plot)
#
monthly_sales = df['Sales'].resample('M').sum().reset_index()
monthly_sales.columns = ['Month', 'Total Sales']

# Plot monthly sales
# import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales['Month'], monthly_sales['Total Sales'], marker='o', linestyle='-', color='g', label='Monthly Sales')
plt.title('Monthly Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.grid(True)
plt.legend()
plt.show()

#####
# Exponantial Smoothing
#
# We can also apply exponential smoothing to 
# you will need to install statsmodels 
#
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt

# Step 1: Calculate monthly sales
monthly_sales = df['Sales'].resample('M').sum().reset_index()
monthly_sales.columns = ['Month', 'Total Sales']

# Step 2: Apply the Exponential Smoothing Model
model = ExponentialSmoothing(
    monthly_sales['Total Sales'], 
    trend="additive", 
    seasonal=None
)
fit = model.fit()

# Step 3: Forecast for the next 12 months
forecast_periods = 12
forecast = fit.forecast(forecast_periods)

# Step 4: Prepare DataFrame for Forecasted Periods
last_date = monthly_sales['Month'].iloc[-1]
forecast_dates = pd.date_range(last_date + pd.offsets.MonthEnd(1), periods=forecast_periods, freq='M')
forecast_df = pd.DataFrame({'Month': forecast_dates, 'Total Sales': forecast})

# Step 5: Combine Actual and Forecasted Data
all_data = pd.concat([
    monthly_sales,
    forecast_df
]).reset_index(drop=True)

# Step 6: Plot Actual and Forecasted Sales
# Note that these are two plots plotted on the same figure
plt.figure(figsize=(14, 7))
plt.plot(monthly_sales['Month'], monthly_sales['Total Sales'], label='Actual Monthly Sales', marker='o', color='b')
plt.plot(forecast_df['Month'], forecast_df['Total Sales'], label='Forecasted Monthly Sales', marker='o', linestyle='--', color='r')
plt.axvline(x=last_date, color='gray', linestyle='--', label='Forecast Start')
plt.title('Actual and Forecasted Monthly Sales (Next 12 Months)')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.legend()
plt.grid(True)
plt.show()

#####
# Adding Seasonal variations and trends
#
# We already did thes imports
#import pandas as pd
#from statsmodels.tsa.holtwinters import ExponentialSmoothing
#import matplotlib.pyplot as plt

# Step 1: Prepare the monthly sales data
monthly_sales = df['Sales'].resample('M').sum().reset_index()
monthly_sales.columns = ['Month', 'Total Sales']

# Step 2: Apply Exponential Smoothing Model with Trend and Seasonality
model = ExponentialSmoothing(monthly_sales['Total Sales'], 
                              trend='add', 
                              seasonal='add', 
                              seasonal_periods=12)  # 12 periods for yearly seasonality
fit = model.fit()

# Step 3: Forecast the next 12 months
forecast_periods = 12
forecast = fit.forecast(forecast_periods)

# Step 4: Prepare the forecasted data
last_date = monthly_sales['Month'].iloc[-1]
forecast_dates = pd.date_range(last_date + pd.offsets.MonthEnd(1), periods=forecast_periods, freq='M')
forecast_df = pd.DataFrame({'Month': forecast_dates, 'Total Sales': forecast})

# Step 5: Combine the actual and forecasted data
all_data = pd.concat([monthly_sales[['Month', 'Total Sales']], forecast_df]).reset_index(drop=True)

# Step 6: Plot the actual and forecasted sales
plt.figure(figsize=(14, 7))
plt.plot(monthly_sales['Month'], monthly_sales['Total Sales'], label='Actual Monthly Sales', marker='o', color='b')
plt.plot(forecast_df['Month'], forecast_df['Total Sales'], label='Forecasted Monthly Sales (ETS)', marker='o', linestyle='--', color='r')
plt.axvline(x=monthly_sales['Month'].iloc[-1], color='gray', linestyle='--', label='Forecast Start')
plt.title('Actual and Forecasted Monthly Sales (Exponential Smoothing - Trend and Seasonality)')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.legend()
plt.grid(True)
plt.show() 
