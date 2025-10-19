import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from .utils import convert_to_inr, format_inr

class SalesPerformance:
    def __init__(self, sales_data, targets_data):
        # Validate input data
        if not isinstance(sales_data, pd.DataFrame) or not isinstance(targets_data, pd.DataFrame):
            raise TypeError("Both sales_data and targets_data must be pandas DataFrames")
        
        # Validate required columns
        required_sales_columns = ['Order Date', 'Category', 'Amount']
        required_target_columns = ['Month of Order Date', 'Category', 'Target']
        
        if not all(col in sales_data.columns for col in required_sales_columns):
            raise ValueError(f"Sales data missing required columns: {required_sales_columns}")
        if not all(col in targets_data.columns for col in required_target_columns):
            raise ValueError(f"Targets data missing required columns: {required_target_columns}")
            
        self.sales_data = sales_data
        self.targets_data = targets_data
        
    def preprocess_data(self):
        try:
            # Convert Order Date to datetime with mixed format support
            # Handle both "1/4/2018" and "13-04-2018" formats
            self.sales_data['Order Date'] = pd.to_datetime(
                self.sales_data['Order Date'], 
                format='mixed',
                dayfirst=False  # Use month/day/year for M/D/YYYY format
            )
            # Create Month-Year column
            self.sales_data['Month-Year'] = self.sales_data['Order Date'].dt.strftime('%y-%b')
        except Exception as e:
            st.error(f"Error preprocessing data: {str(e)}")
            return False
        return True
        
    def calculate_monthly_sales(self):
        try:
            # Group by Month-Year and Category to get actual sales
            monthly_sales = self.sales_data.groupby(['Month-Year', 'Category'])['Amount'].sum().reset_index()
            
            # Merge with targets (rename column for consistency)
            targets_renamed = self.targets_data.copy()
            targets_renamed['Month-Year'] = targets_renamed['Month of Order Date']
            
            self.performance_data = pd.merge(
                monthly_sales,
                targets_renamed,
                on=['Month-Year', 'Category'],
                how='left'
            )
            
            # Handle missing values
            self.performance_data = self.performance_data.fillna(0)
            
            # Sort by Month-Year
            self.performance_data['Month-Year'] = pd.to_datetime(self.performance_data['Month-Year'], format='%y-%b')
            self.performance_data = self.performance_data.sort_values('Month-Year')
            self.performance_data['Month-Year'] = self.performance_data['Month-Year'].dt.strftime('%y-%b')
            
        except Exception as e:
            st.error(f"Error calculating monthly sales: {str(e)}")
            return False
        return True
        
    def display_overview_metrics(self):
        """Display overview metrics with KPIs"""
        st.subheader("📊 Performance Overview")
        
        # Calculate overall metrics
        total_sales = self.performance_data['Amount'].sum()
        total_targets = self.performance_data['Target'].sum()
        overall_achievement = (total_sales / total_targets * 100) if total_targets > 0 else 0
        
        # Convert to INR
        total_sales_inr = convert_to_inr(total_sales)
        total_targets_inr = convert_to_inr(total_targets)
        variance_inr = convert_to_inr(total_sales - total_targets)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sales", format_inr(total_sales_inr))
        with col2:
            st.metric("Total Targets", format_inr(total_targets_inr))
        with col3:
            st.metric("Overall Achievement", f"{overall_achievement:.1f}%")
        with col4:
            st.metric("Variance", format_inr(variance_inr), delta=format_inr(variance_inr))

    def display_category_overview(self):
        """Display category-wise overview with pie charts"""
        st.subheader("📈 Category Performance Overview")
        
        # Category performance summary
        category_performance = self.performance_data.groupby('Category').agg({
            'Amount': 'sum',
            'Target': 'sum'
        }).reset_index()
        category_performance['Achievement'] = (category_performance['Amount'] / category_performance['Target'] * 100).round(2)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales distribution pie chart
            fig_pie_sales = px.pie(
                category_performance,
                values='Amount',
                names='Category',
                title="Sales Distribution by Category"
            )
            fig_pie_sales.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie_sales, use_container_width=True)
        
        with col2:
            # Target distribution pie chart
            fig_pie_targets = px.pie(
                category_performance,
                values='Target',
                names='Category',
                title="Target Distribution by Category"
            )
            fig_pie_targets.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie_targets, use_container_width=True)


    def display_trend_analysis(self):
        """Display trend analysis with line charts"""
        st.subheader("📈 Trend Analysis")
        
        # Prepare data for trend analysis
        trend_data = self.performance_data.groupby(['Month-Year', 'Category']).agg({
            'Amount': 'sum',
            'Target': 'sum'
        }).reset_index()
        
        # Convert to INR
        trend_data['Amount_INR'] = trend_data['Amount'].apply(convert_to_inr)
        trend_data['Target_INR'] = trend_data['Target'].apply(convert_to_inr)
        
        # Sales trend line chart
        fig_trend_sales = px.line(
            trend_data,
            x='Month-Year',
            y='Amount_INR',
            color='Category',
            title="Sales Trend by Category",
            labels={'Amount_INR': 'Sales Amount (₹)', 'Month-Year': 'Month'}
        )
        fig_trend_sales.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_trend_sales, use_container_width=True)

    def display_category_comparison(self):
        """Display category comparison charts"""
        st.subheader("📊 Category Comparison")
        
        # Category summary
        category_summary = self.performance_data.groupby('Category').agg({
            'Amount': 'sum',
            'Target': 'sum'
        }).reset_index()
        category_summary['Achievement'] = (category_summary['Amount'] / category_summary['Target'] * 100).round(2)
        category_summary['Variance'] = category_summary['Amount'] - category_summary['Target']
        
        # Convert to INR
        category_summary['Variance_INR'] = category_summary['Variance'].apply(convert_to_inr)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Achievement by category bar chart
            fig_achievement = px.bar(
                category_summary,
                x='Category',
                y='Achievement',
                title="Achievement Rate by Category",
                labels={'Achievement': 'Achievement Rate (%)', 'Category': 'Category'},
                color='Achievement',
                color_continuous_scale='RdYlGn'
            )
            fig_achievement.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="100% Target")
            fig_achievement.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_achievement, use_container_width=True)
        
        with col2:
            # Variance by category bar chart
            fig_variance = px.bar(
                category_summary,
                x='Category',
                y='Variance_INR',
                title="Sales Variance by Category (Actual - Target)",
                labels={'Variance_INR': 'Variance (₹)', 'Category': 'Category'},
                color='Variance_INR',
                color_continuous_scale='RdYlGn'
            )
            fig_variance.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Target Met")
            fig_variance.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_variance, use_container_width=True)

    def display_detailed_performance(self):
        """Display detailed performance for selected category"""
        st.subheader("🔍 Detailed Performance Analysis")
        
        # Select category
        categories = sorted(self.performance_data['Category'].unique())
        selected_category = st.selectbox('Select Category for Detailed Analysis:', categories)
        
        # Filter data for selected category
        category_data = self.performance_data[
            self.performance_data['Category'] == selected_category
        ].copy()
        
        if category_data.empty:
            st.warning(f"No data available for category: {selected_category}")
            return
        
        # Calculate performance metrics
        category_data['Achievement'] = (category_data['Amount'] / category_data['Target'] * 100).round(2)
        category_data['Variance'] = category_data['Amount'] - category_data['Target']
        
        # Convert to INR for display
        total_sales_inr = convert_to_inr(category_data['Amount'].sum())
        total_targets_inr = convert_to_inr(category_data['Target'].sum())
        total_variance_inr = convert_to_inr(category_data['Variance'].sum())
        
        # Display metrics for selected category
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sales", format_inr(total_sales_inr))
        with col2:
            st.metric("Total Targets", format_inr(total_targets_inr))
        with col3:
            avg_achievement = category_data['Achievement'].mean()
            st.metric("Avg Achievement", f"{avg_achievement:.1f}%")
        with col4:
            st.metric("Total Variance", format_inr(total_variance_inr))
        
        # Convert table data to INR
        category_data_display = category_data.copy()
        category_data_display['Amount_INR'] = category_data_display['Amount'].apply(convert_to_inr)
        category_data_display['Target_INR'] = category_data_display['Target'].apply(convert_to_inr)
        category_data_display['Variance_INR'] = category_data_display['Variance'].apply(convert_to_inr)
        
        # Display comparison table with full precision
        st.subheader(f'Monthly Performance - {selected_category}')
        display_cols = ['Month-Year', 'Amount_INR', 'Target_INR', 'Achievement', 'Variance_INR']
        
        # Set pandas display options to show full numbers
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        
        st.dataframe(
            category_data_display[display_cols].style.format({
                'Amount_INR': '₹{:,.2f}',
                'Target_INR': '₹{:,.2f}',
                'Achievement': '{:.6f}%',
                'Variance_INR': '₹{:,.2f}'
            }),
            use_container_width=True
        )
        
        # Create detailed chart
        # Performance vs Target bar chart
        fig = px.bar(
            category_data_display,
            x='Month-Year',
            y=['Amount_INR', 'Target_INR'],
            title=f'Sales Performance vs Target - {selected_category}',
            barmode='group',
            labels={'value': 'Amount (₹)', 'variable': 'Metric'}
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    def display_performance_metrics(self):
        try:
            # Display all the enhanced visualizations
            self.display_overview_metrics()
            self.display_category_overview()
            self.display_trend_analysis()
            self.display_category_comparison()
            self.display_detailed_performance()
            
        except Exception as e:
            st.error(f"Error displaying metrics: {str(e)}")
        
    def run_analysis(self):
        if self.preprocess_data():
            if self.calculate_monthly_sales():
                self.display_performance_metrics()