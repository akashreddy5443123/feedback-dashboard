# Power BI Technical Interview Master Guide
### Data Analyst, Decision Scientist & BI Developer Preparation

This document provides in-depth, interview-ready answers to the 15 architectural and conceptual questions required for technical interviews, plus 10 challenging follow-up interview questions.

---

## 1. The 15 Core Technical Interview Questions

### Q1: What is Microsoft Power BI?
> **Answer:**  
> Power BI is Microsoft's enterprise business intelligence and data visualization platform. It connects to hundreds of relational, file, and cloud data sources, transforms messy data through its **Power Query (M)** ETL engine, models entities using a high-performance in-memory columnar database called **VertiPaq**, calculates dynamic business logic via **Data Analysis Expressions (DAX)**, and publishes secure, interactive executive dashboards across web and mobile.

---

### Q2: Why was Power BI added to this project?
> **Answer:**  
> While Python and Streamlit are exceptional for exploratory data analysis, data cleaning, and machine learning prototyping, enterprise organizations rely on standardized BI tools for executive consumption. Power BI was added to:
> 1. Provide an executive-ready reporting layer with standardized self-service slicing and drill-downs.
> 2. Implement an enterprise **Star Schema** data model separating dimensions from facts.
> 3. Calculate dynamic KPI measures (such as Net Promoter Score, CSAT, and Month-over-Month rating trajectories) that automatically adjust to user filter context.
> 4. Offer corporate reporting capabilities like scheduled cloud refresh, PDF/PowerPoint report export, and mobile access.

---

### Q3: Why are both Streamlit and Power BI used together?
> **Answer:**  
> Streamlit and Power BI solve complementary, non-overlapping problems in the analytics lifecycle:
> - **Streamlit acts as the Operational & ML Application Interface:** It gives users a live interface to upload raw files, run the Python cleaning pipeline, test ad-hoc Scikit-learn NLP sentiment models, and inspect contradictions.
> - **Power BI acts as the Enterprise BI & Governance Layer:** Once data is validated and cleaned by Python, it is delivered to Power BI for governed executive reporting, multi-page visual storytelling, and self-service departmental slicing.

---

### Q4: What is the key difference between Streamlit and Power BI?
> **Answer:**  
> | Feature | Streamlit | Power BI |
> |---|---|---|
> | **Primary User** | Data scientists, ML engineers, developers | Business analysts, executive leadership, operations |
> | **Execution Model** | Imperative Python script rerun top-to-bottom on widget events | Declarative visual query engine driven by DAX filter context |
> | **Data Storage** | Ephemeral RAM (Pandas DataFrame per user session) | VertiPaq in-memory columnar compressed database |
> | **Machine Learning** | Native execution of Scikit-learn, PyTorch, Hugging Face | Limited (Python/R visual scripts or Azure ML integration) |
> | **Access Control** | Requires custom code or reverse proxy | Native enterprise Azure AD, Row-Level Security (RLS) |

---

### Q5: How do Python and Power BI communicate in this architecture?
> **Answer:**  
> They communicate through a decoupled, file-based analytical data interface:
> 1. **Ingestion & ETL:** The Python layer (`modules/data_processor.py`) ingests raw CSV/Excel files, parses corrupt dates, clips rating anomalies to $[1, 5]$, and derives sentiment.
> 2. **Export Engine:** The export module (`modules/power_bi_export.py`) shapes the clean DataFrame into a normalized Star Schema (`Fact_CustomerFeedback.csv` and 5 dimension tables) and a single-table flat export (`cleaned_customer_feedback.csv`).
> 3. **Consumption:** Power Query in Power BI Desktop reads the exported files directly, builds relationships, and executes DAX calculations.
> 4. **Future Path:** The file interface can be replaced with an automated PostgreSQL database or REST API without altering either layer's internal logic.

---

### Q6: What does Power Query do?
> **Answer:**  
> Power Query is the data preparation and transformation engine inside Power BI and Excel. It uses the **M formula language** to execute repeatable ETL steps: connecting to data sources, pivoting/unpivoting, changing data types, merging tables, and filtering rows. In our architecture, the heavy lifting of cleaning corrupt dates and clipping rating outliers is performed upstream by Python/Pandas, allowing Power Query to remain lightweight and focus strictly on schema typing and ingestion.

---

### Q7: What is DAX?
> **Answer:**  
> **DAX (Data Analysis Expressions)** is the formula and query language used in Power BI, Analysis Services, and Power Pivot in Excel. Unlike Excel formulas which reference specific cell coordinates (e.g. `A1:A10`), DAX operates over entire tables and columns. DAX dynamically recalculates aggregations (sums, averages, counts, time intelligence) on the fly based on the user's active visual and slicer filter context.

---

### Q8: What is the difference between a DAX Measure and a Calculated Column?
> **Answer:**  
> This is one of the most frequently asked BI interview questions:
> - **Calculated Column:**
>   - Evaluated row-by-row during dataset refresh.
>   - Stored permanently in RAM as part of the table in the VertiPaq engine.
>   - Consumes memory and inflates `.pbix` file size.
>   - Uses **Row Context**.
>   - Example: Adding `FeedbackLength = LEN(Fact_CustomerFeedback[FeedbackText])`.
> - **Measure:**
>   - Evaluated on-the-fly at query time when a user interacts with a visual or slicer.
>   - Consumes **zero** persistent RAM storage.
>   - Uses **Filter Context** (adapts dynamically to active page filters).
>   - Example: `Average Rating = AVERAGE(Fact_CustomerFeedback[Rating])` or `NPS Score`.

---

### Q9: What does data modeling mean in Power BI?
> **Answer:**  
> Data modeling is the process of structuring multiple data tables and defining relationships between them using primary and foreign keys. It determines how filters propagate across entities, enables calculations across disparate datasets, and optimizes query performance. A well-modeled dataset ensures accurate aggregations, eliminates circular dependencies, and maximizes VertiPaq compression.

---

### Q10: What is a Star Schema, and why is it preferred over a single flat table?
> **Answer:**  
> A **Star Schema** is a dimensional modeling pattern where a central **Fact Table** (containing numerical transactional measurements and foreign keys) connects radially to multiple surrounding **Dimension Tables** (containing descriptive attributes):
> - **Why it's preferred over a flat table:**
>   1. **VertiPaq Dictionary Compression:** In a flat table, repeating long text strings (e.g., product names or review text across 1,000,000 rows) bloats memory. In a Star Schema, the string exists only once in the dimension table; the fact table stores a lightweight integer or short surrogate key.
>   2. **Simpler DAX Calculations:** Writing Time Intelligence (MoM, YoY) over a dedicated `Dim_Date` table is cleaner and less error-prone than over a flat transactional table.
>   3. **Query Performance:** VertiPaq scans narrow numeric columns significantly faster than wide text-heavy rows.

---

### Q11: What are relationships in Power BI, and what do cardinality and cross-filter direction mean?
> **Answer:**  
> Relationships connect two tables using common keys:
> - **Cardinality:** The uniqueness of keys on both sides:
>   - **One-to-Many ($1:*$):** The enterprise standard. The primary key is unique in the dimension table (1) and appears multiple times in the fact table (*).
>   - **Many-to-Many ($*:*$):** Both tables contain duplicates. Prone to performance degradation and should be avoided or bridged.
> - **Cross-Filter Direction:**
>   - **Single Direction:** Filters applied on the dimension table automatically filter the fact table, but filters on the fact table do NOT filter the dimension. This is the recommended practice.
>   - **Bi-directional:** Filters flow in both directions. Can create circular filter paths and unexpected DAX results.

---

### Q12: How does data refresh work in Power BI?
> **Answer:**  
> In Power BI Desktop, clicking **Refresh** re-executes Power Query M scripts, connects to the underlying data sources (CSVs, database, API), pulls updated data into RAM, recalculates calculated columns, and rebuilds VertiPaq compression dictionaries.  
> In the enterprise **Power BI Service (Cloud)**:
> - For on-premises or local files, an **On-Premises Data Gateway** is configured to bridge cloud-to-local communication.
> - Refreshes can be scheduled up to 8 times daily (Power BI Pro) or 48 times daily (Power BI Premium).

---

### Q13: How could this architecture scale in a real enterprise company?
> **Answer:**  
> To scale from hundreds of rows to tens of millions of records:
> 1. **Persistent Database:** Migrate storage to **PostgreSQL**, **Snowflake**, or **Databricks**.
> 2. **Automated ETL Pipeline:** Use an orchestration tool like **Apache Airflow** or **Prefect** to trigger Python cleaning jobs on a schedule.
> 3. **Hybrid Power BI Storage (Composite Models):**
>    - Use **Import Mode** for high-speed dimension slicing and recent 90-day history.
>    - Use **DirectQuery** for historical data spanning 5+ years, querying the cloud warehouse on demand without loading billions of rows into RAM.
> 4. **Incremental Refresh:** Power BI only refreshes partitions with newly modified records rather than reloading the entire historical table.

---

### Q14: What are the limitations of the current implementation?
> **Answer:**  
> 1. **File-Based Storage:** Relies on local CSV/Excel exports rather than a live transactional SQL database.
> 2. **Manual Refresh Trigger:** Updating Power BI Desktop requires re-exporting from Python and clicking Refresh.
> 3. **Single-Node Execution:** Ingestion and cleaning occur in single-machine memory using Pandas.
> 4. **No Automated Security:** Lacks enterprise Row-Level Security (RLS) tied to corporate Single Sign-On (SSO).

---

### Q15: What are potential future improvements?
> **Answer:**  
> 1. **PostgreSQL / Azure SQL Backend:** Replace CSV files with an ACID-compliant transactional database.
> 2. **FastAPI Webhook Service:** Stream feedback directly from Zendesk, App Store, and Stripe APIs into the database in real time.
> 3. **Automated Cloud Refresh via OneDrive / SharePoint:** Export cleaned CSVs directly to SharePoint Online, enabling zero-gateway scheduled refresh in Power BI Service.
> 4. **Row-Level Security (RLS):** Configure regional security roles (`Dim_Region[RegionName] = USERPRINCIPALNAME()`) so regional managers only see their territory's feedback.

---

## 2. Top 10 Follow-Up Technical Interview Questions

### 1. "How do you calculate Net Promoter Score (NPS) in DAX?"
```dax
NPS Score = 
VAR TotalCount = COUNTROWS('Fact_CustomerFeedback')
VAR Promoters = CALCULATE(COUNTROWS('Fact_CustomerFeedback'), 'Fact_CustomerFeedback'[Rating] >= 4)
VAR Detractors = CALCULATE(COUNTROWS('Fact_CustomerFeedback'), 'Fact_CustomerFeedback'[Rating] <= 2)
RETURN
IF(TotalCount > 0, ROUND(DIVIDE(Promoters - Detractors, TotalCount, 0) * 100, 1), 0)
```
*Key interview point:* Mention `DIVIDE()` handles division-by-zero safely without raising exceptions.

### 2. "Why use `DIVIDE()` instead of `/` in DAX?"
`DIVIDE(numerator, denominator, alternate_value)` prevents runtime crashes when the denominator is 0 or blank, returning the alternate value (or blank) gracefully.

### 3. "What happens if you use `CALCULATE()` without any filter arguments?"
`CALCULATE(Expression)` transitions existing row context into equivalent filter context (known as **Context Transition**). This is critical when invoking measures inside iterating functions like `SUMX()` or calculated columns.

### 4. "How did you avoid the `SettingWithCopyWarning` in Pandas?"
Used explicit DataFrame copies (`df.copy()`) and modified subsets using `.loc[condition, column]` instead of chained indexing (`df[col][condition]`).

### 5. "Why did you mark `Dim_Date` as the official Date Table in Power BI?"
Marking as Date Table disables Power BI's automatic hidden date hierarchies (which generate bloat tables for every datetime column) and ensures DAX Time Intelligence functions (`PREVIOUSMONTH`, `DATESMTD`) evaluate correctly over standard continuous date keys.

### 6. "How do you handle bimodal rating distributions (high 1s and high 5s)?"
A bimodal distribution means the average rating (e.g. 3.2) is misleading. We supplement the mean with **Rating Distribution Bar Charts** and **NPS (Promoters vs. Detractors)** to highlight customer polarization.

### 7. "How do you detect contradictions between star ratings and review text?"
In Python, we train a TF-IDF Logistic Regression classifier with negation preservation. If `Rating == 5` but the text classifier outputs `Negative`, the review is flagged as an anomaly or accidental misclick.

### 8. "What is VertiPaq, and how does it achieve high compression?"
VertiPaq is the in-memory columnar database powering Power BI. It uses **Value Encoding** (storing differences from a base value), **Dictionary Encoding** (replacing distinct strings with small integers), and **Run-Length Encoding (RLE)** (compressing repeated values in sorted columns).

### 9. "What is the difference between `ALL()` and `ALLEXCEPT()` in DAX?"
- `ALL(TableOrColumn)` clears all filter context from the specified table or column.
- `ALLEXCEPT(Table, Column1, Column2)` clears filter context from all columns in the table *except* the specified columns. We used `ALLEXCEPT` in `[Average Rating by Product]` to hold the product filter while clearing regional or channel slicers.

### 10. "If an interviewer asks: Can Power BI run Python scripts natively?"
Yes. Power BI supports Python in two ways:
1. **Python Script Data Connector in Power Query:** Allows running Pandas transformation scripts during data ingestion.
2. **Python Visual in Report Canvas:** Renders Matplotlib or Seaborn plots directly onto the Power BI report canvas.
*(In production, however, running heavy Python scripts upstream before Power BI is preferred for reliability, speed, and cloud refresh compatibility).*
