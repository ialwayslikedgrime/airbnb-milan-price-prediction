import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_percentage_distribution(df, column, bins=None, title=None, 
                               figsize=(10, 6), show_summary=True):
    """
    Plot percentage distribution with binned categories.
    
    Parameters:
    df: DataFrame containing the data
    column: column name to plot (should contain percentage strings like '80%')
    bins: list of bin edges or 'auto' for automatic binning
    title: chart title (optional)
    figsize: tuple for figure size
    show_summary: bool to print summary table
    """
    
    # Convert percentage strings to numeric values
    def clean_percentage(val):
        if pd.isna(val):
            return np.nan
        if isinstance(val, str) and val.endswith('%'):
            return float(val.rstrip('%'))
        return float(val)
    
    # Clean the data
    numeric_data = df[column].apply(clean_percentage)
    
    # Define default bins if not provided
    if bins is None:
        bins = [0, 20, 60, 90, 98, 100]
        bin_labels = ['0-20%', '20-60%', '60-90%', '90-98%', '98%+']
    elif bins == 'auto':
        # Create 5 equal bins
        min_val = numeric_data.min()
        max_val = numeric_data.max()
        bins = np.linspace(min_val, max_val, 6)
        bin_labels = [f'{int(bins[i])}-{int(bins[i+1])}%' for i in range(len(bins)-1)]
    else:
        # Custom bins provided
        bin_labels = [f'{int(bins[i])}-{int(bins[i+1])}%' for i in range(len(bins)-1)]
    
    # Create categories
    binned_data = pd.cut(numeric_data, bins=bins, labels=bin_labels, include_lowest=True)
    
    # Add missing category
    binned_data = binned_data.cat.add_categories(['Missing'])
    binned_data = binned_data.fillna('Missing')
    
    # Get counts and percentages
    counts = binned_data.value_counts()
    # Reorder to put Missing last
    if 'Missing' in counts.index:
        counts = counts.reindex([label for label in bin_labels if label in counts.index] + ['Missing'])
    
    percentages = (counts / counts.sum() * 100).round(1)
    
    # Create vertical bar chart
    fig, ax = plt.subplots(figsize=figsize)
    
    # Colors - gradient from red to green
    colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#27ae60', '#95a5a6']
    plot_colors = colors[:len(counts)]
    
    bars = ax.bar(range(len(counts)), counts, 
                  color=plot_colors,
                  edgecolor='white', 
                  linewidth=1.5,
                  alpha=0.9)
    
    # Add count and percentage labels on top of each bar
    for i, (count, pct) in enumerate(zip(counts, percentages)):
        ax.text(i, count + counts.max() * 0.01, 
                f'{count:,}\n({pct}%)', 
                ha='center', 
                va='bottom',
                fontweight='bold',
                fontsize=11,
                color='black')
    
    # Styling
    chart_title = title if title else f'{column.replace("_", " ").title()} Distribution'
    ax.set_title(chart_title, 
                 fontsize=18, 
                 fontweight='bold', 
                 pad=25,
                 color='#2c3e50')
    
    ax.set_xlabel('Rate Range', 
                  fontsize=14, 
                  fontweight='bold',
                  color='#34495e')
    
    ax.set_ylabel('Number of Hosts', 
                  fontsize=14, 
                  fontweight='bold',
                  color='#34495e')
    
    # Set x-axis labels
    ax.set_xticks(range(len(counts)))
    ax.set_xticklabels(counts.index, rotation=45, ha='right', fontsize=12)
    
    # Add grid
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.7)
    ax.set_axisbelow(True)
    
    # Format y-axis with comma separators
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.8)
    ax.spines['bottom'].set_linewidth(0.8)
    
    # Set y-axis limits
    ax.set_ylim(0, counts.max() * 1.15)
    
    # Add summary box
    total_count = counts.sum()
    summary_text = f'Total: {total_count:,}'
    ax.text(0.02, 0.98, summary_text, 
            transform=ax.transAxes, 
            ha='left', va='top',
            bbox=dict(boxstyle='round,pad=0.8', 
                      facecolor='#ecf0f1', 
                      edgecolor='#bdc3c7',
                      alpha=0.9),
            fontsize=11,
            fontweight='bold')
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    
    plt.show()
    
    # Summary table
    if show_summary:
        print(f"\n" + "="*50)
        print(f"{chart_title.upper()}")
        print("="*50)
        for category, count, pct in zip(counts.index, counts, percentages):
            print(f"{str(category):<15}: {count:>8,} ({pct:>6.1f}%)")
        print("-"*50)
        print(f"{'TOTAL':<15}: {total_count:>8,} (100.0%)")
        print("="*50)

# Example usage:
# plot_percentage_distribution(df, 'host_acceptance_rate')
# plot_percentage_distribution(df, 'host_response_rate', title='Host Response Rate Analysis')
# plot_percentage_distribution(df, 'host_acceptance_rate', bins=[0, 50, 80, 95, 100])