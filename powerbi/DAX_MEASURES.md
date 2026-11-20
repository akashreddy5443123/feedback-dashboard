# Power BI DAX Measures Specification & Dictionary

This document details all DAX measures implemented in `powerbi/dax_measures.dax`. Each measure is explained with its formula, return type, business purpose, and equivalent Python/Pandas logic.

---

## 1. Core Volume Measures

### 1. `Total Feedback`
```dax
Total Feedback = COUNTROWS('Fact_CustomerFeedback')
```
- **Data Type:** Whole Number (Format: `#,##0`)
- **Business Purpose:** Total number of customer feedback records currently visible within the active filter context.
- **Filter Context:** Automatically updates when users filter by Date, Product, Region, or Channel.
- **Python Equivalent:** `len(filtered_df)`

### 2. `Total Products`
```dax
Total Products = DISTINCTCOUNT('Fact_CustomerFeedback'[ProductKey])
```
- **Data Type:** Whole Number
- **Business Purpose:** Number of unique products evaluated in the selected slice.
- **Python Equivalent:** `filtered_df['product'].nunique()`

### 3. `Total Customers`
```dax
Total Customers = DISTINCTCOUNT('Fact_CustomerFeedback'[CustomerName])
```
- **Data Type:** Whole Number
- **Business Purpose:** Unique customer accounts submitting feedback.
- **Python Equivalent:** `filtered_df['customer_name'].nunique()`

---

## 2. Rating & Satisfaction Measures

### 4. `Average Rating`
```dax
Average Rating = ROUND(AVERAGE('Fact_CustomerFeedback'[Rating]), 2)
```
- **Data Type:** Decimal Number (Format: `0.00`)
- **Business Purpose:** Primary operational satisfaction score across products and touchpoints.
- **Python Equivalent:** `round(filtered_df['rating'].mean(), 2)`

### 5. `Average Rating by Product`
```dax
Average Rating by Product = 
CALCULATE(
    [Average Rating],
    ALLEXCEPT('Fact_CustomerFeedback', 'Dim_Product'[ProductName])
)
```
- **Data Type:** Decimal Number (Format: `0.00`)
- **Business Purpose:** Fixes the calculation at the product level, ignoring non-product page filters to show true product benchmark ratings.
- **Python Equivalent:** `df.groupby('product')['rating'].mean()`

---

## 3. Sentiment Breakdown Measures

### 6. `Positive Feedback Count`
```dax
Positive Feedback Count = 
CALCULATE(
    COUNTROWS('Fact_CustomerFeedback'),
    'Fact_CustomerFeedback'[IsPositive] = 1
)
```
- **Data Type:** Whole Number
- **Business Purpose:** Volume of submissions classified as Positive.
- **Python Equivalent:** `(filtered_df['sentiment'] == 'Positive').sum()`

### 7. `Negative Feedback Count`
```dax
Negative Feedback Count = 
CALCULATE(
    COUNTROWS('Fact_CustomerFeedback'),
    'Fact_CustomerFeedback'[IsNegative] = 1
)
```
- **Data Type:** Whole Number
- **Business Purpose:** Volume of submissions classified as Negative (complaints/issues).
- **Python Equivalent:** `(filtered_df['sentiment'] == 'Negative').sum()`

### 8. `Neutral Feedback Count`
```dax
Neutral Feedback Count = 
CALCULATE(
    COUNTROWS('Fact_CustomerFeedback'),
    'Fact_CustomerFeedback'[IsNeutral] = 1
)
```
- **Data Type:** Whole Number
- **Business Purpose:** Volume of neutral feedback (3-star ratings or non-polarized text).
- **Python Equivalent:** `(filtered_df['sentiment'] == 'Neutral').sum()`

### 9. `Positive Feedback Percentage`
```dax
Positive Feedback Percentage = 
VAR TotalCount = [Total Feedback]
VAR PosCount = [Positive Feedback Count]
RETURN
IF(TotalCount > 0, DIVIDE(PosCount, TotalCount, 0), 0)
```
- **Data Type:** Percentage (Format: `0.0%`)
- **Business Purpose:** Percentage of customer interactions that are positive.
- **Python Equivalent:** `(pos_count / total_count) * 100`

### 10. `Negative Feedback Percentage`
```dax
Negative Feedback Percentage = 
VAR TotalCount = [Total Feedback]
VAR NegCount = [Negative Feedback Count]
RETURN
IF(TotalCount > 0, DIVIDE(NegCount, TotalCount, 0), 0)
```
- **Data Type:** Percentage (Format: `0.0%`)
- **Business Purpose:** Key risk indicator: high negative percentage triggers operational review.
- **Python Equivalent:** `(neg_count / total_count) * 100`

---

## 4. Channel Aggregations

### 11. `Feedback Count by Channel`
```dax
Feedback Count by Channel = 
CALCULATE(
    COUNTROWS('Fact_CustomerFeedback'),
    ALLEXCEPT('Fact_CustomerFeedback', 'Dim_Channel'[ChannelName])
)
```
- **Data Type:** Whole Number
- **Business Purpose:** Total volume handled per channel touchpoint.
- **Python Equivalent:** `filtered_df['channel'].value_counts()`

---

## 5. Time Intelligence & Monthly Trends

### 12. `Monthly Feedback Count`
```dax
Monthly Feedback Count = 
CALCULATE(
    [Total Feedback],
    DATESMTD('Dim_Date'[Date])
)
```
- **Data Type:** Whole Number
- **Business Purpose:** Month-to-date feedback volume. Uses `DATESMTD` over the formal `Dim_Date` dimension.
- **Python Equivalent:** `filtered_df.set_index('date').resample('ME').size()`

### 13. `Monthly Average Rating`
```dax
Monthly Average Rating = 
CALCULATE(
    [Average Rating],
    DATESMTD('Dim_Date'[Date])
)
```
- **Data Type:** Decimal Number (Format: `0.00`)
- **Business Purpose:** Monthly satisfaction trajectory.
- **Python Equivalent:** `filtered_df.set_index('date')['rating'].resample('ME').mean()`

### 14. `MoM Rating Delta`
```dax
MoM Rating Delta = 
VAR CurrentRating = [Average Rating]
VAR PriorRating = CALCULATE([Average Rating], PREVIOUSMONTH('Dim_Date'[Date]))
RETURN
IF(ISBLANK(PriorRating), BLANK(), CurrentRating - PriorRating)
```
- **Data Type:** Decimal Number (Format: `+0.00;-0.00;0.00`)
- **Business Purpose:** Month-over-Month rating trajectory. Positive values indicate improving satisfaction; negative values highlight service degradation.
- **Python Equivalent:** `monthly_series.diff()`

---

## 6. Executive Decision Science: NPS & CSAT

### 15. `NPS Score`
```dax
NPS Score = 
VAR TotalCount = [Total Feedback]
VAR Promoters = CALCULATE(COUNTROWS('Fact_CustomerFeedback'), 'Fact_CustomerFeedback'[Rating] >= 4)
VAR Detractors = CALCULATE(COUNTROWS('Fact_CustomerFeedback'), 'Fact_CustomerFeedback'[Rating] <= 2)
RETURN
IF(TotalCount > 0, ROUND(DIVIDE(Promoters - Detractors, TotalCount, 0) * 100, 1), 0)
```
- **Data Type:** Decimal Number (Scale: `-100.0` to `+100.0`)
- **Business Purpose:** Net Promoter Score. Standard benchmark metric for customer loyalty.
- **Python Equivalent:** `((promoters - detractors) / total) * 100`

### 16. `CSAT Percentage`
```dax
CSAT Percentage = 
DIVIDE(
    CALCULATE(COUNTROWS('Fact_CustomerFeedback'), 'Fact_CustomerFeedback'[Rating] >= 4),
    [Total Feedback],
    0
)
```
- **Data Type:** Percentage (Format: `0.0%`)
- **Business Purpose:** Customer Satisfaction score (Promoters / Total).
- **Python Equivalent:** `promoters / total * 100`
