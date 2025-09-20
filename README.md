# Data-Visualization
Online Retail Data Visualization – Tata Forage Job Simulation

# Project Overview

This project was completed as part of the Tata Data Visualization: Empowering Business with Effective Insights job simulation on Forage. The goal was to clean retail transaction data and create Tableau visualizations to answer business questions from the CEO and CMO.

# Dataset

Source: Online Retail Dataset (UCI ML Repository)

Fields: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

Timeframe: 2010–2011

# Data Cleaning

Removed records with Quantity < 1 (returns).

Removed records with Unit Price < 0 (errors).

Created a Revenue column = Quantity × Unit Price.

Filtered incomplete or invalid entries.

# Business Questions & Visuals

CEO – Monthly Revenue Trends (2011):
Line chart showing revenue by month to identify seasonal patterns.

CMO – Top 10 Countries by Revenue (Excluding UK):
Bar chart with revenue and quantity sold for top countries.

CMO – Top 10 Customers by Revenue:
Bar chart ranking customers by highest revenue.

CEO – Global Product Demand (Excluding UK):
Map visualization of product demand (quantity sold) by country.

# Tools Used

Tableau Desktop

Excel/CSV (Online Retail Dataset)

# Key Insights

Seasonal peaks in November–December (holiday sales).

Top markets outside the UK include Netherlands, Germany, and France.

A small set of customers generate most of the revenue.

Growth opportunities in European and North American regions.

# Author

Maddu Manaswi Priya
September 2025
