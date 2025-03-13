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
#plt.show()

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
sales_by_product_segment = data.groupby(['Product', 'Segment'])['Sales'].sum().reset_index()

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



#############
# Week 9 Code