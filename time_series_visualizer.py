import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv').set_index('date')

# Clean data
df = df[
        (df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot    
    # converter o índice 'date' para o tipo datetime
    df.index = pd.to_datetime(df.index)

    # criar o gráfico
    plt.figure(figsize=(24, 8))  
    plt.plot(df.index, df['value'], color='red', linestyle='-') 

    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    fig = plt.gcf()
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)
    df_bar['year'] = pd.DatetimeIndex(df_bar['date']).year
    df_bar['month'] = pd.DatetimeIndex(df_bar['date']).month
    df_bar.groupby(['year', 'month'],as_index=False)['value'].mean()
    # Draw bar plot
    plt.figure(figsize=(15, 8))
    ax = sns.barplot(data=df_bar, x='year', y='value', hue='month', palette='bright')
    plt.xlabel('Year')
    plt.ylabel('Average Page Views')
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(title='Month', labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], handles=handles)
    # labels do gráfico e título
    plt.title('Average Page Views/Years')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    fig = plt.gcf()
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Ordenar os meses para que apareçam corretamente no gráfico
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)

    # Criar a figura e os subplots (2 subplots)
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 7))

    # Primeiro Boxplot: Year-wise Box Plot (Trend)
    sns.boxplot(ax=axes[0], x='year', y='value', data=df_box, hue='year', legend=False, palette='bright')
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Segundo Boxplot: Month-wise Box Plot (Seasonality)
    sns.boxplot(ax=axes[1], x='month', y='value', data=df_box, hue='month', legend=False, palette='bright')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    fig = plt.gcf()
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
