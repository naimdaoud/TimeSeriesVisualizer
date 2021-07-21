import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')

# Clean data
df = df.drop(df[(df['value']<df['value'].quantile(0.025)) | (df['value']>df['value'].quantile(0.975))].index)

def draw_line_plot():
    # Draw line plot
    df.plot(x='date',y='value',color='red') 
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    fig =plt.gcf()
    fig.set_size_inches(23, 8)
    # Save image and return fig (don't change this part)
    plt.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Year'] = pd.DatetimeIndex(df_bar['date']).year
    df_bar['Month'] = pd.DatetimeIndex(df_bar['date']).month
    df_bar = df_bar.groupby(['Year', 'Month'])['value'].mean()  
    df_bar = df_bar.unstack()
    month_names=['January', 'February', 'March', 'April', 'May', 'June', 'July', 
             'August', 'September', 'October', 'November', 'December']

    # Draw bar plot
    fig = df_bar.plot(kind= 'bar', figsize = (15,10)).figure
    plt.title('')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    lg = plt.legend(title= 'Months', fontsize = 15, labels = month_names)
    title = lg.get_title()
    title.set_fontsize(15)
    fig =plt.gcf()
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def fixed_boxplot(*args, label=None, **kwargs):
    sns.boxplot(*args, **kwargs, labels=[label])

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = pd.DatetimeIndex(df_box['date']).year
    df_box['date'] = pd.to_datetime(df_box['date'])
    df_box['month'] = df_box['date'].dt.strftime('%b')
    

    # adjust data
    # - first month of 2016 is may > boxplot starts with may
    # - resort by year desc > first month of 2019 is january 
    df_box.sort_values(by=['year','date'], ascending=[False, True], inplace=True)

    # Draw box plots (using Seaborn)
    df_box["Page Views"] = df_box["value"]
    df_box["Month"] = df_box["month"]
    df_box["Year"] = df_box["year"]
    g = sns.PairGrid(df_box, y_vars=["Page Views"], x_vars=["Year", "Month"], palette="hls")
    g.map(fixed_boxplot)
    fig = g.fig
    fig.set_figheight(6)
    fig.set_figwidth(16)
    fig.axes[0].set_ylabel('Page Views')
    fig.axes[1].set_ylabel('Page Views')
    fig.axes[0].set_title('Year-wise Box Plot (Trend)')
    fig.axes[1].set_title('Month-wise Box Plot (Seasonality)')
    plt.tight_layout()
    

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

draw_box_plot()