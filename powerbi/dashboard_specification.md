# Power BI Dashboard Specification

## Dashboard Overview

Two separate dashboards with identical structure but different data sources:
1. **US Weather Transit Dashboard** (Boston, Chicago, New York)
2. **Indian Weather Transit Dashboard** (Delhi, Mumbai, Bangalore)

Each dashboard has 5 pages with interactive filters and drill-down capabilities.

---

## Color Scheme

**US Dashboard:**
- Primary: #0078D4 (Blue)
- Secondary: #50E6FF (Light Blue)
- Accent: #FFB900 (Amber)
- Alert: #E81123 (Red)
- Success: #107C10 (Green)

**Indian Dashboard:**
- Primary: #FF6B35 (Orange)
- Secondary: #F7931E (Saffron)
- Accent: #004B87 (Blue)
- Alert: #D62828 (Red)
- Success: #2A9D8F (Teal)

---

## Page 1: Overview Dashboard

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│  WEATHER IMPACT ON PUBLIC TRANSPORTATION - [US/INDIA]      │
├──────────┬──────────┬──────────┬──────────┬────────────────┤
│  Total   │  Total   │  Avg     │  Total   │  Max Delay     │
│  Days    │  Routes  │  Delay   │  Trips   │  Recorded      │
│  [KPI]   │  [KPI]   │  [KPI]   │  [KPI]   │  [KPI]         │
├──────────┴──────────┴──────────┴──────────┴────────────────┤
│                                                              │
│  Weather Impact Comparison (Bar Chart)                      │
│  - X: Weather Condition                                     │
│  - Y: Average Delay (minutes)                               │
│  - Color by Weather Condition                               │
│                                                              │
├──────────────────────────────┬───────────────────────────────┤
│                              │                               │
│  City Performance            │  Delay Trend Over Time        │
│  (Clustered Column Chart)    │  (Line Chart)                 │
│  - X: City                   │  - X: Date                    │
│  - Y: Avg Delay              │  - Y: Avg Delay               │
│  - Legend: Weather Type      │  - Multiple lines by city     │
│                              │                               │
└──────────────────────────────┴───────────────────────────────┘
```

### Visualizations

**1. KPI Cards (Top Row)**
- **Total Days Tracked**: `vw_[us/india]_overview_kpis.total_days`
- **Total Routes**: `vw_[us/india]_overview_kpis.total_routes`
- **Average Delay**: `vw_[us/india]_overview_kpis.overall_avg_delay` (with trend indicator)
- **Total Trips**: `vw_[us/india]_overview_kpis.total_trips_analyzed`
- **Max Delay**: `vw_[us/india]_overview_kpis.max_delay`

**2. Weather Impact Bar Chart**
- **Visual**: Clustered Bar Chart
- **Data**: `vw_[us/india]_weather_impact`
- **Axis**: `weather_condition`
- **Values**: `avg_delay`
- **Data Labels**: Show values
- **Conditional Formatting**: Red for high delays, Green for low

**3. City Performance Chart**
- **Visual**: Clustered Column Chart
- **Data**: `vw_[us/india]_city_weather_matrix`
- **Axis**: `city`
- **Values**: `avg_delay`
- **Legend**: `weather_condition`
- **Tooltip**: Add `occurrences`, `total_trips`

**4. Delay Trend Line Chart**
- **Visual**: Line Chart
- **Data**: `vw_[us/india]_time_series_daily`
- **Axis**: `date`
- **Values**: `avg_delay`
- **Legend**: Split by city (if available)
- **Markers**: Show data points

### Filters (Apply to all pages)
- **Date Range Slicer**: `date` (Between style)
- **City Slicer**: Multi-select dropdown
- **Weather Condition Slicer**: Multi-select tiles

---

## Page 2: Weather Impact Analysis

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│  WEATHER IMPACT DEEP DIVE                                   │
├──────────────────────────────┬───────────────────────────────┤
│                              │                               │
│  Weather Impact Matrix       │  Delay Distribution           │
│  (Heatmap/Matrix)            │  (Box Plot)                   │
│  - Rows: City                │  - X: Weather Condition       │
│  - Columns: Weather          │  - Y: Delay Minutes           │
│  - Values: Avg Delay         │  - Show outliers              │
│                              │                               │
├──────────────────────────────┴───────────────────────────────┤
│                                                              │
│  Weather Condition Statistics (Table)                       │
│  - Weather | Records | Avg Delay | Min | Max | Std Dev     │
│                                                              │
├──────────────────────────────┬───────────────────────────────┤
│                              │                               │
│  Seasonal/Monsoon Analysis   │  Weather Frequency            │
│  (Stacked Column)            │  (Donut Chart)                │
│  - X: Season                 │  - Values: Record Count       │
│  - Y: Avg Delay              │  - Legend: Weather Type       │
│                              │                               │
└──────────────────────────────┴───────────────────────────────┘
```

### Visualizations

**1. Weather Impact Matrix**
- **Visual**: Matrix or Heatmap
- **Data**: `vw_[us/india]_city_weather_matrix`
- **Rows**: `city`
- **Columns**: `weather_condition`
- **Values**: `avg_delay`
- **Conditional Formatting**: Color scale (Green → Yellow → Red)

**2. Delay Distribution Box Plot**
- **Visual**: Box and Whisker Chart (or Violin Plot)
- **Data**: `vw_[us/india]_correlation_data`
- **Category**: `weather_condition`
- **Values**: `avg_delay_minutes`
- **Show**: Median, Quartiles, Outliers

**3. Weather Statistics Table**
- **Visual**: Table
- **Data**: `vw_[us/india]_weather_impact`
- **Columns**: 
  - `weather_condition`
  - `record_count`
  - `avg_delay`
  - `min_delay`
  - `max_delay`
  - `std_delay`
- **Conditional Formatting**: Highlight highest delays

**4. Seasonal/Monsoon Analysis**
- **Visual**: Stacked Column Chart
- **Data**: `vw_us_seasonal_analysis` or `vw_india_monsoon_analysis`
- **Axis**: `season`
- **Values**: `avg_delay`
- **Legend**: `weather_condition` (if available)

**5. Weather Frequency Donut**
- **Visual**: Donut Chart
- **Data**: `vw_[us/india]_weather_impact`
- **Values**: `record_count`
- **Legend**: `weather_condition`
- **Data Labels**: Percentage

---

## Page 3: City Comparison

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│  CITY-WISE PERFORMANCE ANALYSIS                             │
├──────────────────────────────┬───────────────────────────────┤
│                              │                               │
│  City Performance Metrics    │  City Ranking                 │
│  (Clustered Bar Chart)       │  (Table with Sparklines)      │
│  - Y: City                   │  - City | Avg Delay | Trend   │
│  - X: Avg Delay              │  - Routes | Total Trips       │
│  - Color by City             │                               │
│                              │                               │
├──────────────────────────────┴───────────────────────────────┤
│                                                              │
│  City Weather Impact Comparison (Grouped Column)            │
│  - X: City                                                   │
│  - Y: Avg Delay                                             │
│  - Legend: Weather Condition (Snow, Rain, Clear, etc.)      │
│                                                              │
├──────────────────────────────┬───────────────────────────────┤
│                              │                               │
│  City Delay Trends           │  City Statistics Cards        │
│  (Small Multiples Line)      │  - Selected City Details      │
│  - One chart per city        │  - Total Routes               │
│  - X: Date, Y: Delay         │  - Avg Delay                  │
│                              │  - Worst Weather Impact       │
│                              │                               │
└──────────────────────────────┴───────────────────────────────┘
```

### Visualizations

**1. City Performance Bar Chart**
- **Visual**: Clustered Bar Chart (Horizontal)
- **Data**: `vw_[us/india]_city_performance`
- **Axis**: `city`
- **Values**: `avg_delay`
- **Color**: By city (distinct colors)
- **Sort**: Descending by avg_delay

**2. City Ranking Table**
- **Visual**: Table
- **Data**: `vw_[us/india]_city_performance`
- **Columns**:
  - `city`
  - `avg_delay`
  - `routes`
  - `total_trips`
  - `avg_delay_snow/rain/clear`
- **Conditional Formatting**: Icons for ranking

**3. City Weather Impact Comparison**
- **Visual**: Clustered Column Chart
- **Data**: `vw_[us/india]_city_weather_matrix`
- **Axis**: `city`
- **Values**: `avg_delay`
- **Legend**: `weather_condition`
- **Data Labels**: Show values

**4. City Delay Trends (Small Multiples)**
- **Visual**: Line Chart with Small Multiples
- **Data**: `vw_[us/india]_time_series_daily`
- **Axis**: `date`
- **Values**: `avg_delay`
- **Small Multiple**: By `city`

**5. City Statistics Cards**
- **Visual**: Multi-row Card (Dynamic based on slicer selection)
- **Data**: `vw_[us/india]_city_performance`
- **Fields**: All metrics for selected city
- **Interaction**: Updates when city is selected

### Interactions
- Clicking a city filters all other visuals
- Cross-highlighting enabled

---

## Page 4: Time Series Analysis

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│  TEMPORAL TRENDS & PATTERNS                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Daily Delay Trend (Line Chart with Forecast)               │
│  - X: Date                                                   │
│  - Y: Average Delay                                         │
│  - Multiple lines: By City or Weather                       │
│  - Forecast: 30 days (optional)                             │
│                                                              │
├──────────────────────────────┬───────────────────────────────┤
│                              │                               │
│  Monthly Aggregation         │  Day of Week Pattern          │
│  (Column Chart)              │  (Column Chart)               │
│  - X: Month                  │  - X: Day of Week             │
│  - Y: Avg Delay              │  - Y: Avg Delay               │
│  - Tooltip: Weather stats    │  - Color by Weather           │
│                              │                               │
├──────────────────────────────┴───────────────────────────────┤
│                                                              │
│  Seasonal Comparison (Line + Column Combo)                  │
│  - X: Month                                                  │
│  - Y1: Avg Delay (Line)                                     │
│  - Y2: Precipitation/Snowfall (Column)                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Visualizations

**1. Daily Delay Trend**
- **Visual**: Line Chart with Analytics
- **Data**: `vw_[us/india]_time_series_daily`
- **Axis**: `date`
- **Values**: `avg_delay`
- **Legend**: `city` or `weather_conditions`
- **Analytics**: Add trend line, average line
- **Forecast**: Enable 30-day forecast (optional)

**2. Monthly Aggregation**
- **Visual**: Column Chart
- **Data**: `vw_[us/india]_time_series_monthly`
- **Axis**: `month`
- **Values**: `avg_delay`
- **Tooltip**: Add `total_precipitation`, `total_snowfall`, `total_trips`
- **Color**: Gradient based on delay

**3. Day of Week Pattern**
- **Visual**: Column Chart
- **Data**: Create DAX measure to extract day of week from `vw_[us/india]_time_series_daily`
- **Axis**: Day of Week (Mon-Sun)
- **Values**: Average of `avg_delay`
- **Legend**: `weather_condition`

**4. Seasonal Comparison (Combo Chart)**
- **Visual**: Line and Stacked Column Chart
- **Data**: `vw_[us/india]_time_series_monthly`
- **Axis**: `month`
- **Column Values**: `total_precipitation` (US) or `avg_humidity` (India)
- **Line Values**: `avg_delay`
- **Dual Axis**: Yes

### Date Hierarchy
- Year → Quarter → Month → Day
- Enable drill-down functionality

---

## Page 5: Route Performance

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│  ROUTE-LEVEL ANALYSIS                                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Top 10 Most Delayed Routes (Bar Chart)                     │
│  - Y: Route Name                                            │
│  - X: Average Delay                                         │
│  - Color by City                                            │
│                                                              │
├──────────────────────────────┬───────────────────────────────┤
│                              │                               │
│  Route Performance Table     │  Route Delay by Weather       │
│  (Detailed Table)            │  (Stacked Bar)                │
│  - Route | City | Avg Delay  │  - Y: Route                   │
│  - Max Delay | Total Trips   │  - X: Avg Delay               │
│  - Days Tracked              │  - Legend: Weather            │
│                              │                               │
├──────────────────────────────┴───────────────────────────────┤
│                                                              │
│  Route Delay Distribution (Scatter Plot)                    │
│  - X: Total Trips                                           │
│  - Y: Average Delay                                         │
│  - Size: Days Tracked                                       │
│  - Color: City                                              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Visualizations

**1. Top 10 Most Delayed Routes**
- **Visual**: Bar Chart (Horizontal)
- **Data**: `vw_[us/india]_route_performance`
- **Axis**: `route_name` (US) or `route_id` (India)
- **Values**: `avg_delay`
- **Color**: By `city`
- **Filter**: Top 10 by avg_delay
- **Sort**: Descending

**2. Route Performance Table**
- **Visual**: Table with Conditional Formatting
- **Data**: `vw_[us/india]_route_performance`
- **Columns**:
  - `route_id`
  - `route_name` (US only)
  - `city`
  - `avg_delay`
  - `max_delay`
  - `total_trips`
  - `days_tracked`
- **Conditional Formatting**: 
  - Data bars on `avg_delay`
  - Color scale on `max_delay`
- **Sorting**: Enable on all columns

**3. Route Delay by Weather**
- **Visual**: Stacked Bar Chart
- **Data**: `vw_[us/india]_top_delays_by_weather`
- **Axis**: `route_id` or `route_name`
- **Values**: `avg_delay`
- **Legend**: `weather_condition`
- **Filter**: Top 15 routes

**4. Route Delay Distribution Scatter**
- **Visual**: Scatter Chart
- **Data**: `vw_[us/india]_route_performance`
- **X-Axis**: `total_trips`
- **Y-Axis**: `avg_delay`
- **Size**: `days_tracked`
- **Color**: `city`
- **Tooltip**: Add `route_name`, `max_delay`

### Interactions
- Click route to filter other visuals
- Drill-through to route details

---

## Global Filters (All Pages)

### Filter Panel (Left Side)

**1. Date Range Slicer**
- **Type**: Between slicer
- **Field**: `date`
- **Default**: All dates
- **Style**: Slider

**2. City Filter**
- **Type**: Dropdown (Multi-select)
- **Field**: `city`
- **Default**: All selected
- **Style**: Dropdown list

**3. Weather Condition Filter**
- **Type**: Tile slicer
- **Field**: `weather_condition`
- **Default**: All selected
- **Style**: Tiles with icons

**4. Route Filter** (Page 5 only)
- **Type**: Search dropdown
- **Field**: `route_id` or `route_name`
- **Default**: All
- **Style**: Searchable dropdown

---

## DAX Measures (See dax_measures.txt)

Key measures to create:
- Delay Impact %
- Weather Severity Score
- Delay Trend (MoM, YoY)
- Route Reliability Score
- City Performance Index

---

## Interactivity Features

### Cross-Filtering
- Enable on all visuals
- Click any chart element to filter others

### Drill-Through
- From any visual → Route Details page
- From City → City-specific analysis

### Tooltips
- Custom tooltips showing:
  - Weather details
  - Trip counts
  - Date ranges

### Bookmarks
- "Clear All Filters"
- "High Delay Routes"
- "Weather Extremes"
- "City Comparison"

### Buttons
- Reset Filters
- Navigate between pages
- Export to PDF

---

## Mobile Layout

Create mobile-optimized layouts:
- Portrait orientation
- Simplified visuals
- Touch-friendly filters
- Key metrics on top

---

## Publishing & Sharing

### Power BI Service
1. Publish to workspace
2. Set up scheduled refresh
3. Create app for end users
4. Configure row-level security (if needed)

### Export Options
- PDF reports
- PowerPoint presentations
- Excel data export
- Analyze in Excel

---

## Performance Optimization

1. **Use Import Mode** (not DirectQuery) for this dataset size
2. **Reduce Visual Count** per page (max 10-12)
3. **Optimize DAX** measures (avoid complex calculations)
4. **Use Aggregations** from views (already done)
5. **Limit Data** with filters if dataset grows

---

## Accessibility

- High contrast colors
- Alt text for all visuals
- Keyboard navigation
- Screen reader support
- Clear labels and titles

---

## Next Steps

1. Run SQL scripts to create views
2. Connect Power BI to PostgreSQL
3. Load data from views
4. Create measures from dax_measures.txt
5. Build visualizations following this spec
6. Test interactivity
7. Publish to Power BI Service
