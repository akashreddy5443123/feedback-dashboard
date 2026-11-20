# Power BI Report Page Specifications (5-Page Implementation)

This document contains visual-by-visual blueprints to build the 5-page Power BI Customer Feedback Report.

---

## Design System & Theme Standards

- **Primary Brand / Navy:** `#2C3E50` (Titles, Headers, Total Metrics)
- **Positive / Success:** `#2ECC71` (4–5 Stars, Positive Sentiment, Promoters)
- **Neutral / Warning:** `#F1C40F` (3 Stars, Neutral Sentiment, Passives)
- **Negative / Danger:** `#E74C3C` (1–2 Stars, Negative Sentiment, Detractors)
- **Background / Canvas:** `#F8F9FA` (Clean, modern light canvas)
- **Font Family:** `Segoe UI` (Standard Power BI corporate typography)

---

## 📄 Page 1: Executive Overview

**Goal:** Provide C-suite and VP stakeholders with a high-level pulse on customer satisfaction, volume trends, and channel distribution.

```
┌────────────────────────────────────────────────────────────────────────┐
│  PAGE 1: EXECUTIVE OVERVIEW                                            │
├─────────────────┬─────────────────┬──────────────────┬─────────────────┤
│ [Card] Total    │ [Card] Avg      │ [Card] Positive  │ [Card] Negative │
│   Feedback      │   Rating        │   Feedback %     │   Feedback %    │
│   600           │   3.49 / 5      │   54.8%          │   22.3%         │
├─────────────────┴─────────────────┼──────────────────┴─────────────────┤
│ [Visual 1] Overall Sentiment      │ [Visual 2] Feedback Trend Over Time│
│ Donut Chart (Pos/Neu/Neg)         │ Line Chart (Weekly/Monthly Volume) │
├───────────────────────────────────┼────────────────────────────────────┤
│ [Visual 3] Rating Distribution    │ [Visual 4] Feedback by Channel     │
│ Clustered Column Chart (1-5★)     │ Horizontal Bar Chart (Email/Tickets│
└───────────────────────────────────┴────────────────────────────────────┘
```

### Visual Specifications:
1. **KPI Card Row (Top Banner):**
   - **Card 1:** Field = `[Total Feedback]`, Label = "Total Feedback", Font = 28pt Bold.
   - **Card 2:** Field = `[Average Rating]`, Label = "Average Rating (out of 5)".
   - **Card 3:** Field = `[Positive Feedback Percentage]`, Label = "Positive %", Value Color = `#2ECC71`.
   - **Card 4:** Field = `[Negative Feedback Percentage]`, Label = "Negative %", Value Color = `#E74C3C`.
2. **Visual 1 (Donut Chart - Sentiment Breakdown):**
   - **Legend:** `Dim_Sentiment[Sentiment]`
   - **Values:** `[Total Feedback]`
   - **Colors:** Positive (`#2ECC71`), Neutral (`#F1C40F`), Negative (`#E74C3C`).
   - **Details:** Data labels = "Category, Percent of total". Hole size = 50%.
3. **Visual 2 (Line Chart - Feedback Trend Over Time):**
   - **X-Axis:** `Dim_Date[Date]` (Hierarchy: Year $\rightarrow$ Month $\rightarrow$ Date)
   - **Y-Axis:** `[Total Feedback]`
   - **Legend:** `Dim_Sentiment[Sentiment]`
   - **Format:** Stepped lines off, markers enabled, stroke width = 2pt.
4. **Visual 3 (Column Chart - Rating Distribution):**
   - **X-Axis:** `Fact_CustomerFeedback[Rating]` (Sorted ascending 1 to 5)
   - **Y-Axis:** `[Total Feedback]`
   - **Data Labels:** On, showing exact count of reviews per star.
5. **Visual 4 (Bar Chart - Feedback by Channel):**
   - **Y-Axis:** `Dim_Channel[ChannelName]`
   - **X-Axis:** `[Total Feedback]`
   - **Color:** Gradient Navy (`#2C3E50`).
6. **Page Slicers:**
   - Date Range slider (`Dim_Date[Date]`)
   - Region dropdown (`Dim_Region[RegionName]`)

---

## 📄 Page 2: Product Analysis

**Goal:** Enable Product Managers to compare satisfaction across tiers, identify struggling products, and prioritize engineering bug fixes.

### Visual Specifications:
1. **Visual 1 (Horizontal Bar Chart - Average Rating by Product):**
   - **Y-Axis:** `Dim_Product[ProductName]` (Sorted descending by `[Average Rating]`)
   - **X-Axis:** `[Average Rating]` (X-axis range clamped: Min = 1.0, Max = 5.0)
   - **Data Labels:** On (`0.00` format).
   - **Conditional Formatting:** Green for $\ge 3.5$, Red for $< 3.0$.
2. **Visual 2 (Clustered Bar Chart - Total Feedback by Product):**
   - **Y-Axis:** `Dim_Product[ProductName]`
   - **X-Axis:** `[Total Feedback]`
   - **Tooltip:** `[Average Rating]`, `[Positive Feedback Count]`, `[Negative Feedback Count]`.
3. **Visual 3 (100% Stacked Bar Chart - Sentiment Distribution by Product):**
   - **Y-Axis:** `Dim_Product[ProductName]`
   - **X-Axis:** `[Total Feedback]`
   - **Legend:** `Dim_Sentiment[Sentiment]` (Colors: Green, Amber, Red)
   - **Purpose:** Compares the ratio of praise vs. complaints per product regardless of volume differences.
4. **Visual 4 (Table / Matrix - Product Performance Summary):**
   - **Rows:** `Dim_Product[ProductName]`
   - **Columns / Values:**
     - `[Total Feedback]`
     - `[Average Rating]`
     - `[Positive Feedback Percentage]`
     - `[Negative Feedback Percentage]`
     - `[NPS Score]`
   - **Formatting:** Background color heatmaps on `[Average Rating]` and `[NPS Score]`.
5. **Visual 5 (Card / Alert - Lowest-Rated Product Callout):**
   - Dedicated KPI highlight surfacing the lowest-scoring product tier and its top complaint topic.

---

## 📄 Page 3: Sentiment Analysis

**Goal:** Provide Customer Experience (CX) and Marketing leads with deep-dive sentiment patterns across time, geography, and touchpoints.

### Visual Specifications:
1. **Visual 1 (Treemap or Donut - 3-Way Sentiment Distribution):**
   - **Group:** `Dim_Sentiment[Sentiment]`
   - **Values:** `[Total Feedback]`
2. **Visual 2 (Multi-Line Chart - Sentiment Trends Over Time):**
   - **X-Axis:** `Dim_Date[YearMonth]`
   - **Y-Axis:** Count of feedback
   - **Legend:** `Dim_Sentiment[Sentiment]`
   - **Business Action:** Detects sudden spikes in Negative sentiment following software patch releases.
3. **Visual 3 (Clustered Column Chart - Sentiment by Product):**
   - **X-Axis:** `Dim_Product[ProductName]`
   - **Y-Axis:** `[Total Feedback]`
   - **Legend:** `Dim_Sentiment[Sentiment]`
4. **Visual 4 (Stacked Bar Chart - Sentiment by Region):**
   - **Y-Axis:** `Dim_Region[RegionName]`
   - **X-Axis:** `[Total Feedback]`
   - **Legend:** `Dim_Sentiment[Sentiment]`
   - **Purpose:** Identifies regional dissatisfaction (e.g. currency billing bugs in MEA vs. server lag in APAC).
5. **Visual 5 (Matrix Visual - Sentiment by Feedback Channel):**
   - **Rows:** `Dim_Channel[ChannelName]`
   - **Columns:** `Dim_Sentiment[Sentiment]`
   - **Values:** `[Total Feedback]`

---

## 📄 Page 4: Customer and Channel Analysis

**Goal:** Optimize customer support operations, evaluate channel selection bias, and examine geographic patterns.

### Visual Specifications:
1. **Visual 1 (Filled Map or Bar Chart - Feedback by Region):**
   - **Location:** `Dim_Region[RegionName]`
   - **Bubble Size / Bar Length:** `[Total Feedback]`
   - **Color Saturation:** `[Average Rating]` (Red-Yellow-Green divergent palette).
2. **Visual 2 (Donut Chart - Share of Feedback by Channel):**
   - **Legend:** `Dim_Channel[ChannelName]`
   - **Values:** `[Total Feedback]`
3. **Visual 3 (Clustered Bar Chart - Average Rating by Channel):**
   - **Y-Axis:** `Dim_Channel[ChannelName]`
   - **X-Axis:** `[Average Rating]`
   - **Business Context:** Support Ticket channels typically skew lower due to negative selection bias (users only open tickets when blocked).
4. **Visual 4 (Scatter Plot - Volume vs Satisfaction Quadrant):**
   - **X-Axis:** `[Total Feedback]` (Channel Volume)
   - **Y-Axis:** `[Average Rating]` (Channel Satisfaction)
   - **Details:** `Dim_Channel[ChannelName]`
   - **Reference Lines:** X-Median line, Y-Average rating line (identifies high-volume, low-satisfaction problem channels).
5. **Interactive Filter Panel:**
   - Multi-select slicers for Product Tier, Geographic Territory, and Rating Stars.

---

## 📄 Page 5: Detailed Feedback Explorer

**Goal:** Allow support managers and decision scientists to inspect raw feedback text, search specific keywords, and investigate individual customer issues.

### Visual Specifications:
1. **Interactive Data Grid (Table Visual):**
   - **Columns (in order):**
     1. `Fact_CustomerFeedback[FeedbackID]` (Width: 90px, Center aligned)
     2. `Fact_CustomerFeedback[CustomerName]` (Width: 120px)
     3. `Dim_Product[ProductName]` (Width: 130px)
     4. `Dim_Date[DateFormatted]` (Width: 100px, Right aligned)
     5. `Fact_CustomerFeedback[Rating]` (Width: 70px, Star rating icon)
     6. `Dim_Sentiment[Sentiment]` (Conditional text color: Green/Amber/Red)
     7. `Dim_Channel[ChannelName]` (Width: 120px)
     8. `Dim_Region[RegionName]` (Width: 110px)
     9. `Fact_CustomerFeedback[FeedbackText]` (Multi-line text enabled, remaining width)
2. **Search & Filter Controls:**
   - Text Search Slicer (Keyword search across `FeedbackText`)
   - Rating Slicer (Buttons for 1★, 2★, 3★, 4★, 5★)
   - Sentiment Dropdown (`Positive`, `Neutral`, `Negative`)
   - Product Multi-select dropdown
3. **Sorting:** Default sorted by `DateFormatted` descending (most recent feedback first).
