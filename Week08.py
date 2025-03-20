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