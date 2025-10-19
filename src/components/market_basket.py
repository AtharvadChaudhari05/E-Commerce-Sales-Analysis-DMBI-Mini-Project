import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from mlxtend.frequent_patterns import apriori, association_rules
from .utils import convert_to_inr, format_inr

class MarketBasketAnalysis:
    def __init__(self, sales_data, products_data):
        self.sales_data = sales_data
        self.products_data = products_data

    def merge_data(self):
        # Merge sales and products data on Order ID
        merged_data = pd.merge(self.sales_data, self.products_data, on='Order ID')
        return merged_data

    def filter_data(self, merged_data, min_support=0.01):
        # Create basket format for market basket analysis
        basket = (merged_data
                  .groupby(['Order ID', 'Sub-Category'])['Quantity']
                  .sum().unstack().reset_index().fillna(0)
                  .set_index('Order ID'))
        basket = basket.applymap(lambda x: 1 if x > 0 else 0)
        return basket

    def generate_association_rules(self, basket, min_support=0.01, min_confidence=0.5):
        frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
        return rules

    def display_category_analysis(self, merged_data):
        """Display category-wise analysis with pie charts and bar charts"""
        st.subheader("📊 Category Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Category distribution pie chart
            category_counts = merged_data['Category'].value_counts()
            fig_pie = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title="Sales Distribution by Category"
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Sub-category bar chart
            subcategory_counts = merged_data['Sub-Category'].value_counts().head(10)
            fig_bar = px.bar(
                x=subcategory_counts.values,
                y=subcategory_counts.index,
                orientation='h',
                title="Top 10 Sub-Categories by Sales Volume",
                labels={'x': 'Number of Orders', 'y': 'Sub-Category'}
            )
            fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)

    def display_amount_analysis(self, merged_data):
        """Display amount analysis with scatter plots and histograms"""
        st.subheader("💰 Sales Amount Analysis")
        
        # Convert amounts to INR
        merged_data_inr = merged_data.copy()
        merged_data_inr['Amount_INR'] = merged_data_inr['Amount'].apply(convert_to_inr)
        merged_data_inr['Profit_INR'] = merged_data_inr['Profit'].apply(convert_to_inr)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Average amount by category bar chart
            category_avg_amount = merged_data_inr.groupby('Category')['Amount_INR'].mean().reset_index()
            fig_bar = px.bar(
                category_avg_amount,
                x='Category',
                y='Amount_INR',
                title="Average Order Amount by Category",
                labels={'Amount_INR': 'Average Amount (₹)', 'Category': 'Category'}
            )
            fig_bar.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Amount distribution histogram
            fig_hist = px.histogram(
                merged_data_inr,
                x='Amount_INR',
                nbins=30,
                title="Distribution of Sales Amounts",
                labels={'Amount_INR': 'Amount (₹)', 'count': 'Frequency'}
            )
            st.plotly_chart(fig_hist, use_container_width=True)

    def display_geographic_analysis(self, merged_data):
        """Display geographic analysis"""
        st.subheader("🌍 Geographic Analysis")
        
        # Convert amounts to INR
        merged_data_inr = merged_data.copy()
        merged_data_inr['Amount_INR'] = merged_data_inr['Amount'].apply(convert_to_inr)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # State-wise sales
            state_sales = merged_data_inr.groupby('State')['Amount_INR'].sum().sort_values(ascending=False).head(10)
            fig_state = px.bar(
                x=state_sales.values,
                y=state_sales.index,
                orientation='h',
                title="Top 10 States by Sales Amount",
                labels={'x': 'Total Sales (₹)', 'y': 'State'}
            )
            fig_state.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_state, use_container_width=True)
        
        with col2:
            # City-wise sales
            city_sales = merged_data_inr.groupby('City')['Amount_INR'].sum().sort_values(ascending=False).head(10)
            fig_city = px.bar(
                x=city_sales.values,
                y=city_sales.index,
                orientation='h',
                title="Top 10 Cities by Sales Amount",
                labels={'x': 'Total Sales (₹)', 'y': 'City'}
            )
            fig_city.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_city, use_container_width=True)

    def display_profit_analysis(self, merged_data):
        """Display profit analysis with scatter plots"""
        st.subheader("📈 Profit Analysis")
        
        # Convert amounts to INR
        merged_data_inr = merged_data.copy()
        merged_data_inr['Amount_INR'] = merged_data_inr['Amount'].apply(convert_to_inr)
        merged_data_inr['Profit_INR'] = merged_data_inr['Profit'].apply(convert_to_inr)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Total profit by category bar chart
            category_profit = merged_data_inr.groupby('Category')['Profit_INR'].sum().reset_index()
            fig_profit = px.bar(
                category_profit,
                x='Category',
                y='Profit_INR',
                title="Total Profit by Category",
                labels={'Profit_INR': 'Total Profit (₹)', 'Category': 'Category'},
                color='Profit_INR',
                color_continuous_scale='Greens'
            )
            fig_profit.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_profit, use_container_width=True)
        
        with col2:
            # Profit margin by category
            category_profit = merged_data_inr.groupby('Category').agg({
                'Amount_INR': 'sum',
                'Profit_INR': 'sum'
            }).reset_index()
            category_profit['Profit_Margin'] = (category_profit['Profit_INR'] / category_profit['Amount_INR'] * 100).round(2)
            
            fig_margin = px.bar(
                category_profit,
                x='Category',
                y='Profit_Margin',
                title="Profit Margin by Category (%)",
                labels={'Profit_Margin': 'Profit Margin (%)', 'Category': 'Category'}
            )
            fig_margin.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_margin, use_container_width=True)

    def display_association_rules_visualization(self, rules):
        """Display association rules with enhanced visualizations"""
        if not rules.empty:
            st.subheader("🔗 Association Rules Analysis")
            
            # Convert frozensets to strings for visualization
            rules_display = rules.copy()
            rules_display['antecedents_str'] = rules_display['antecedents'].apply(lambda x: ', '.join(list(x)))
            rules_display['consequents_str'] = rules_display['consequents'].apply(lambda x: ', '.join(list(x)))
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top rules by support bar chart
                top_rules_support = rules_display.nlargest(10, 'support')
                rule_labels_support = [f"{ant} → {cons}" for ant, cons in zip(top_rules_support['antecedents_str'], top_rules_support['consequents_str'])]
                fig_rules_bar = px.bar(
                    top_rules_support,
                    x='support',
                    y=rule_labels_support,
                    orientation='h',
                    title="Top 10 Rules by Support",
                    labels={'support': 'Support', 'y': 'Rule'},
                    hover_data=['confidence', 'lift']
                )
                fig_rules_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_rules_bar, use_container_width=True)
            
            with col2:
                # Top rules by lift
                top_rules = rules_display.nlargest(10, 'lift')
                rule_labels = [f"{ant} → {cons}" for ant, cons in zip(top_rules['antecedents_str'], top_rules['consequents_str'])]
                fig_rules_bar = px.bar(
                    top_rules,
                    x='lift',
                    y=rule_labels,
                    orientation='h',
                    title="Top 10 Rules by Lift",
                    labels={'lift': 'Lift', 'y': 'Rule'},
                    hover_data=['support', 'confidence']
                )
                fig_rules_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_rules_bar, use_container_width=True)

    def run_analysis(self):
        try:
            st.subheader("🛒 Market Basket Analysis Dashboard")
            
            # Merge data first
            merged_data = self.merge_data()
            
            # Display overview metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Orders", len(merged_data['Order ID'].unique()))
            with col2:
                total_revenue_inr = convert_to_inr(merged_data['Amount'].sum())
                st.metric("Total Revenue", format_inr(total_revenue_inr))
            with col3:
                total_profit_inr = convert_to_inr(merged_data['Profit'].sum())
                st.metric("Total Profit", format_inr(total_profit_inr))
            with col4:
                avg_order_value_inr = convert_to_inr(merged_data['Amount'].mean())
                st.metric("Avg Order Value", format_inr(avg_order_value_inr))
            
            # Category Analysis
            self.display_category_analysis(merged_data)
            
            # Amount Analysis
            self.display_amount_analysis(merged_data)
            
            # Geographic Analysis
            self.display_geographic_analysis(merged_data)
            
            # Profit Analysis
            self.display_profit_analysis(merged_data)
            
            # Association Rules Section
            st.subheader("🔍 Association Rules Mining")
            
            # Get parameters from user
            col1, col2 = st.columns(2)
            with col1:
                min_support = st.slider("Minimum Support", 0.01, 0.1, 0.01, 0.01)
            with col2:
                min_confidence = st.slider("Minimum Confidence", 0.1, 1.0, 0.5, 0.1)
            
            # Create basket and generate rules
            basket = self.filter_data(merged_data, min_support)
            rules = self.generate_association_rules(basket, min_support, min_confidence)
            
            if not rules.empty:
                # Display rules table with proper formatting
                st.subheader("📋 Association Rules Table")
                
                # Convert frozensets to readable strings
                rules_display = rules.copy()
                rules_display['Antecedents'] = rules_display['antecedents'].apply(lambda x: ', '.join(list(x)))
                rules_display['Consequents'] = rules_display['consequents'].apply(lambda x: ', '.join(list(x)))
                
                # Select and format columns
                display_rules = rules_display[['Antecedents', 'Consequents', 'support', 'confidence', 'lift']].copy()
                display_rules.columns = ['Antecedents', 'Consequents', 'Support', 'Confidence', 'Lift']
                
                # Set pandas display options to show full numbers
                pd.set_option('display.max_columns', None)
                pd.set_option('display.width', None)
                pd.set_option('display.max_colwidth', None)
                
                # Display with full precision and better formatting
                styled_df = display_rules.style.format({
                    'Support': '{:.6f}',
                    'Confidence': '{:.6f}',
                    'Lift': '{:.6f}'
                }).set_properties(**{
                    'text-align': 'left',
                    'white-space': 'nowrap'
                })
                
                st.dataframe(styled_df, use_container_width=True)
                
                # Also show a summary of the rules
                st.subheader("📊 Rules Summary")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Rules", len(display_rules))
                with col2:
                    st.metric("Avg Support", f"{display_rules['Support'].mean():.6f}")
                with col3:
                    st.metric("Avg Confidence", f"{display_rules['Confidence'].mean():.6f}")
                
                # Display rules visualizations
                self.display_association_rules_visualization(rules)
                
            else:
                st.warning("No association rules found with the given parameters. Try lowering the minimum support or confidence.")
                
        except Exception as e:
            st.error(f"Error in market basket analysis: {str(e)}")

def load_data(products_path, sales_path):
    products_data = pd.read_csv(products_path)
    sales_data = pd.read_csv(sales_path)
    return products_data, sales_data