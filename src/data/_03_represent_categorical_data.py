import matplotlib.pyplot as plt
import pandas as pd

def plot_categorical_distribution(df, column, category_order=None, title=None, 
                                figsize=(8, 6), show_summary=True, 
                                missing_label='Missing'):
    """
    Plot categorical distribution with counts and percentages.
    
    Parameters:
    df: DataFrame containing the data
    column: column name to plot
    category_order: list of categories in desired order (optional)
    title: chart title (optional, defaults to column name)
    figsize: tuple for figure size
    show_summary: bool to print summary table
    missing_label: label for missing values
    """
    
    # Handle missing values and create series
    s = df[column].fillna(missing_label)
    
    # Get value counts
    if category_order:
        # Use provided order
        s = s.astype(pd.CategoricalDtype(categories=category_order, ordered=True))
        counts = s.value_counts().reindex(category_order)
    else:
        # Use natural order
        counts = s.value_counts()
        category_order = counts.index.tolist()
    
    percentages = (counts / counts.sum() * 100).round(1)
    
    # Create vertical bar chart
    fig, ax = plt.subplots(figsize=figsize)
    
    # Generate colors based on number of categories
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#8B8B8D', 
              '#16537e', '#85204a', '#c26f00', '#9a2f15', '#6b6b6d']
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
    
    ax.set_xlabel(column.replace('_', ' ').title(), 
                  fontsize=14, 
                  fontweight='bold',
                  color='#34495e')
    
    ax.set_ylabel('Count', 
                  fontsize=14, 
                  fontweight='bold',
                  color='#34495e')
    
    # Set x-axis labels
    ax.set_xticks(range(len(category_order)))
    ax.set_xticklabels(category_order, rotation=45, ha='right', fontsize=12)
    
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
        for category, count, pct in zip(category_order, counts, percentages):
            print(f"{str(category):<22}: {count:>8,} ({pct:>6.1f}%)")
        print("-"*50)
        print(f"{'TOTAL':<22}: {total_count:>8,} (100.0%)")
        print("="*50)
    
    # Optionally return values if needed
    # return fig, ax, counts, percentages

# Example usage:
# plot_categorical_distribution(df, 'host_response_time')
# plot_categorical_distribution(df, 'room_type', title='Room Type Distribution')
# plot_categorical_distribution(df, 'neighbourhood', category_order=['Downtown', 'Suburbs', 'Other'])