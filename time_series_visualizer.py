import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Load data
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

# Clean data by filtering out the top and bottom 2.5% of page views
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='tab:red', linewidth=1)
    
    # Title and labels
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    
    # Save and return the figure
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy data and prepare for bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Pivot data for grouped bar chart
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Plotting
    fig = df_bar.plot(kind='bar', figsize=(10, 8), legend=True).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    
    # Set the legend with full month names
    plt.legend(title="Months", labels=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Sort months for the box plot
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Year-wise Box Plot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    
    # Month-wise Box Plot
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    
    fig.savefig('box_plot.png')
    return fig
