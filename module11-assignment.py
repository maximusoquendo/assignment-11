# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Create a seed for reproducibility
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='QE')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022', 
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Generate quarterly sales data for each location and category
quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales with seasonal pattern (Q4 higher, Q1 lower)
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8
            
            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]
            
            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]
            
            # Growth trend over time (5% per year, quarterly compounded)
            growth_factor = (1 + 0.05/4) ** quarter_idx
            
            # Calculate sales with some randomness
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)  # Add noise
            
            # Advertising spend (correlated with sales but with diminishing returns)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            
            # Record
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Create customer data
customer_data = []
total_customers = 2000

# Age distribution parameters for each location
age_params = {
    'Tampa': (45, 15),      # Older demographic
    'Miami': (35, 12),      # Younger demographic
    'Orlando': (38, 14),    # Mixed demographic
    'Jacksonville': (42, 13)  # Middle-aged demographic
}

for location in locations:
    # Generate ages based on location demographics
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])
    
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)  # Ensure ages are between 18-80
    
    # Generate purchase amounts
    for age in ages:
        # Younger and older customers spend differently across categories
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        
        # Purchase amount based on age and category
        base_amount = np.random.gamma(shape=5, scale=20)
        
        # Product tier (budget, mid-range, premium)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], 
                                     p=[0.3, 0.5, 0.2])
        
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        
        purchase_amount = base_amount * tier_factor
        
        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add some calculated columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print data info
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


# TODO 1: Time Series Visualization - Sales Trends

def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    # Group sales by quarter label so each point represents total quarterly sales.
    quarterly_sales = sales_df.groupby("QuarterLabel")["Sales"].sum().reindex(quarter_labels)

    # Create the figure and axis.
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot total sales over time.
    ax.plot(quarterly_sales.index, quarterly_sales.values, marker="o", linewidth=2)

    # Add labels and formatting.
    ax.set_title("Overall Quarterly Sales Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Sales ($)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig


def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    # Group sales by quarter and location.
    location_sales = sales_df.groupby(["QuarterLabel", "Location"])["Sales"].sum().unstack()

    # Keep quarters in the original chronological order.
    location_sales = location_sales.reindex(quarter_labels)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot one line for each location.
    for location in location_sales.columns:
        ax.plot(location_sales.index, location_sales[location], marker="o", linewidth=2, label=location)

    ax.set_title("Quarterly Sales Trends by Location")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Sales ($)")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig


# TODO 2: Categorical Comparison - Product Performance by Location

def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    # Create a table of total sales for each location and category.
    category_location_sales = sales_df.pivot_table(
        values="Sales",
        index="Category",
        columns="Location",
        aggfunc="sum"
    )

    fig, ax = plt.subplots(figsize=(11, 6))

    # Pandas creates a grouped bar chart directly from the pivot table.
    category_location_sales.plot(kind="bar", ax=ax)

    ax.set_title("Category Performance by Location")
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Total Sales ($)")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="Location")
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    return fig


def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    # Create a table showing category sales within each location.
    composition = sales_df.pivot_table(
        values="Sales",
        index="Location",
        columns="Category",
        aggfunc="sum"
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    # Stacked bars show how each category contributes to each location's total.
    composition.plot(kind="bar", stacked=True, ax=ax)

    ax.set_title("Sales Composition by Location")
    ax.set_xlabel("Location")
    ax.set_ylabel("Total Sales ($)")
    ax.tick_params(axis="x", rotation=0)
    ax.legend(title="Category", bbox_to_anchor=(1.05, 1), loc="upper left")

    fig.tight_layout()
    return fig


# TODO 3: Relationship Analysis - Advertising and Sales

def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(9, 6))

    # Scatter plot compares ad spend with sales for each record.
    ax.scatter(sales_df["AdSpend"], sales_df["Sales"], alpha=0.7)

    ax.set_title("Advertising Spend vs. Sales")
    ax.set_xlabel("Advertising Spend ($)")
    ax.set_ylabel("Sales ($)")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig


def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    # Average sales per advertising dollar by quarter.
    efficiency = sales_df.groupby("QuarterLabel")["SalesPerDollarSpent"].mean().reindex(quarter_labels)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(efficiency.index, efficiency.values, marker="o", color="green", linewidth=2)

    ax.set_title("Advertising Efficiency Over Time")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales per Advertising Dollar")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig


# TODO 4: Distribution Analysis - Customer Demographics

def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    # Create a 2x3 grid so we can show overall distribution plus each location.
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()

    # Overall customer age distribution.
    axes[0].hist(customer_df["Age"], bins=20, edgecolor="black", alpha=0.7)
    axes[0].set_title("Overall Age Distribution")
    axes[0].set_xlabel("Age")
    axes[0].set_ylabel("Number of Customers")

    # One histogram for each location.
    for i, location in enumerate(locations, start=1):
        location_ages = customer_df[customer_df["Location"] == location]["Age"]
        axes[i].hist(location_ages, bins=15, edgecolor="black", alpha=0.7)
        axes[i].set_title(f"{location} Age Distribution")
        axes[i].set_xlabel("Age")
        axes[i].set_ylabel("Number of Customers")

    # Hide the unused final subplot.
    axes[-1].axis("off")

    fig.tight_layout()
    return fig


def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    # Create age groups for easier comparison.
    age_bins = [17, 29, 49, 80]
    age_labels = ["18-29", "30-49", "50+"]

    customer_df_copy = customer_df.copy()
    customer_df_copy["AgeGroup"] = pd.cut(
        customer_df_copy["Age"],
        bins=age_bins,
        labels=age_labels
    )

    # Collect purchase amounts for each age group.
    purchase_data = [
        customer_df_copy[customer_df_copy["AgeGroup"] == group]["PurchaseAmount"]
        for group in age_labels
    ]

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.boxplot(purchase_data, tick_labels=age_labels)

    ax.set_title("Purchase Amounts by Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Purchase Amount ($)")
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    return fig


# TODO 5: Sales Distribution - Pricing Tiers

def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(9, 6))

    # Histogram shows how customer purchase amounts are distributed.
    ax.hist(customer_df["PurchaseAmount"], bins=30, edgecolor="black", alpha=0.7)

    ax.set_title("Purchase Amount Distribution")
    ax.set_xlabel("Purchase Amount ($)")
    ax.set_ylabel("Number of Purchases")
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    return fig


def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    # Sum purchase amounts for each price tier.
    tier_sales = customer_df.groupby("PriceTier")["PurchaseAmount"].sum()

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.pie(
        tier_sales.values,
        labels=tier_sales.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Sales Breakdown by Price Tier")

    fig.tight_layout()
    return fig


# TODO 6: Market Share Analysis

def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    # Sum total sales by product category.
    category_sales = sales_df.groupby("Category")["Sales"].sum()

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.pie(
        category_sales.values,
        labels=category_sales.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Market Share by Product Category")

    fig.tight_layout()
    return fig


def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    # Sum total sales by location.
    location_sales = sales_df.groupby("Location")["Sales"].sum()

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.pie(
        location_sales.values,
        labels=location_sales.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Sales Distribution by Location")

    fig.tight_layout()
    return fig


# TODO 7: Comprehensive Dashboard

def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Subplot 1: Overall sales trend.
    quarterly_sales = sales_df.groupby("QuarterLabel")["Sales"].sum().reindex(quarter_labels)
    axes[0, 0].plot(quarterly_sales.index, quarterly_sales.values, marker="o")
    axes[0, 0].set_title("Quarterly Sales Trend")
    axes[0, 0].tick_params(axis="x", rotation=45)
    axes[0, 0].set_ylabel("Sales ($)")
    axes[0, 0].grid(True, alpha=0.3)

    # Subplot 2: Sales by location.
    location_sales = sales_df.groupby("Location")["Sales"].sum()
    axes[0, 1].bar(location_sales.index, location_sales.values)
    axes[0, 1].set_title("Total Sales by Location")
    axes[0, 1].set_ylabel("Sales ($)")
    axes[0, 1].tick_params(axis="x", rotation=30)

    # Subplot 3: Sales by category.
    category_sales = sales_df.groupby("Category")["Sales"].sum()
    axes[1, 0].bar(category_sales.index, category_sales.values)
    axes[1, 0].set_title("Total Sales by Category")
    axes[1, 0].set_ylabel("Sales ($)")
    axes[1, 0].tick_params(axis="x", rotation=45)

    # Subplot 4: Ad spend versus sales.
    axes[1, 1].scatter(sales_df["AdSpend"], sales_df["Sales"], alpha=0.7)
    axes[1, 1].set_title("Ad Spend vs. Sales")
    axes[1, 1].set_xlabel("Ad Spend ($)")
    axes[1, 1].set_ylabel("Sales ($)")
    axes[1, 1].grid(True, alpha=0.3)

    fig.suptitle("SunCoast Retail Business Dashboard", fontsize=16)
    fig.tight_layout()

    return fig


# Main function to execute all visualizations
# REQUIRED: Do not modify this function name
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)
    
    # REQUIRED: Call all visualization functions and store figures
    # Store each figure in a variable for potential saving/display
    
    # Time Series Analysis
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()
    
    # Categorical Comparison
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()
    
    # Relationship Analysis
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()
    
    # Distribution Analysis
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()
    
    # Sales Distribution
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    
    # Market Share Analysis
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    
    # Comprehensive Dashboard
    fig13 = create_business_dashboard()
    
    # REQUIRED: Add business insights summary
    print("\nKEY BUSINESS INSIGHTS:")
    
    top_location = sales_df.groupby("Location")["Sales"].sum().idxmax()
    top_category = sales_df.groupby("Category")["Sales"].sum().idxmax()
    best_quarter = sales_df.groupby("QuarterLabel")["Sales"].sum().idxmax()
    avg_ad_efficiency = sales_df["SalesPerDollarSpent"].mean()

    print(f"- Top Location: {top_location} generated the highest total sales.")
    print(f"- Top Category: {top_category} was the strongest product category.")
    print(f"- Best Quarter: {best_quarter} had the highest sales performance.")
    print(f"- Advertising Efficiency: The average sales per advertising dollar was {avg_ad_efficiency:.2f}.")
    # Your insights here based on the visualizations
    
    # Display all figures
    plt.show()

# Run the main function
if __name__ == "__main__":
    main()