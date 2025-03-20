##############
# Week 7 Code

# import the libraries
import pandas as pd
import matplotlib.pyplot as plt

# Read the data into a new dataframe
df = pd.read_csv("Coffee_company.csv")
print(df.head())
print(df.columns)

# Clean up the column headings
df.columns = df.columns.str.strip()
print(df.head())
print(df.columns)

# Round up 'Units Sold' data by converting it to int
df['Units Sold'] = df['Units Sold'].astype(int)
print(df.head())

# Change 'Month Name' to 'Month" 
# If we didn't strip the column names this would not work

print(df.columns) # to check the exact name of each column
df.rename(columns={'Month Name':'Month'}, inplace = True)
print(df.head())
print(df.columns)

# 
# 
# Week 7 Extension Code
# Calculate total Sales

df['Sales'] = pd.to_numeric(df['Sales'].str.replace(',', '').str.replace('$', ''), errors='coerce')
#df['Sales'] = pd.to_numeric(df['Sales'].str.replace(',', '', regex=False).str.replace('$', '', regex=False), errors='coerce')
df['Sales'] = df['Sales'].astype(float)
total_sales = df['Sales'].sum()
print("Total Sales: $", total_sales)


# Convert 'Date' to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Set 'Date' as the index
df.set_index('Date', inplace=True)

# Calculate quarterly sales
quarterly_sales = df['Sales'].resample('Q').sum().reset_index()
quarterly_sales.columns = ['Quarter', 'Total Sales']

print(quarterly_sales)

################
# Week 8 Code
#
# Plotting the quarterly sales as a bar chart
# Set the figure size to (10, 6)
plt.figure(figsize=(10, 6))


#
plt.bar(quarterly_sales['Quarter'].dt.to_period('Q').astype(str), quarterly_sales['Total Sales'], color='skyblue')

# Set the properties of the plot
plt.title('Quarterly Sales')
plt.xlabel('Quarter')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()

# show the plot (you need this for VS Code)
plt.show()

# Adding data labels on top of the bars
bars  = plt.bar(quarterly_sales['Quarter'].dt.to_period('Q').astype(str), quarterly_sales['Total Sales'], color='skyblue')
# loop through each bar to add the label in the specified location
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

# show the plot (see changes form original)
#plt.show()

#
# Calculate the sales of each product
#
#
product_sales = df.groupby('Product')['Sales'].sum().reset_index()
print(product_sales)

# Plotting the sales of products as a bar chart
plt.figure(figsize=(12, 6))
bars = plt.bar(product_sales['Product'], product_sales['Sales'], color='lightcoral')

# Adding data labels on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

plt.title('Total Sales by Product')
plt.xlabel('Product')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#
# Analyse sales by segment
#
#
segment_sales = df.groupby('Segment')['Sales'].sum().reset_index()
print(segment_sales)

# Plotting the sales of products as a bar chart
plt.figure(figsize=(12, 6))
bars = plt.bar(segment_sales['Segment'], segment_sales['Sales'], color='lightcoral')

# Adding data labels on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

plt.title('Total Sales by Segment')
plt.xlabel('Segment')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Week 8 Extension code
# Group by Product and Segment, then sum the sales
sales_by_product_segment = df.groupby(['Product', 'Segment'])['Sales'].sum().reset_index()

# Pivot the DataFrame for plotting
pivot_table = sales_by_product_segment.pivot(index='Product', columns='Segment', values='Sales').fillna(0)

# Plotting the grouped bar chart
ax = pivot_table.plot(kind='bar', figsize=(12, 6), color=['lightblue', 'salmon', 'lightgreen'])
plt.title('Sales by Product and Segment')
plt.xlabel('Product')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.legend(title='Segment')

# Adding data labels
#for container in ax.containers:
#    for bar in container:
#        height = bar.get_height()
#        ax.annotate(f'{height:.2f}',  # Format the height to 2 decimal places
#                    xy=(bar.get_x() + bar.get_width() / 2, height),  # Positioning the label
#                    ha='center', va='bottom')  # Center the label above the bar

plt.tight_layout()
plt.show()



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

