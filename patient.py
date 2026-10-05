# ============================================================
# SUNRISE PATIENT SATISFACTION - EDA & KPI ANALYSIS
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1. LOAD CSV
# ------------------------------------------------------------

file_name = "sunrise_patient_satisfaction.csv"

df = pd.read_csv(file_name)

print("\n================ FIRST 5 ROWS ================\n")
print(df.head())

print("\n================ DATASET SHAPE ================\n")
print(df.shape)

print("\n================ COLUMNS ================\n")
print(df.columns.tolist())

print("\n================ DATA TYPES ================\n")
print(df.dtypes)

print("\n================ MISSING VALUES ================\n")
print(df.isnull().sum())

print("\n================ DUPLICATES ================\n")
print(df.duplicated().sum())


# ------------------------------------------------------------
# 2. CLEAN COLUMN NAMES
# ------------------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nCleaned columns:")
print(df.columns.tolist())


# ------------------------------------------------------------
# 3. REMOVE DUPLICATES
# ------------------------------------------------------------

df = df.drop_duplicates()

print("\nRows after removing duplicates:", len(df))


# ------------------------------------------------------------
# 4. BASIC STATISTICS
# ------------------------------------------------------------

print("\n================ STATISTICS ================\n")
print(df.describe(include="all"))


# ------------------------------------------------------------
# 5. FIND SATISFACTION COLUMN
# ------------------------------------------------------------

satisfaction_column = None

for column in df.columns:

    if column in [
        "satisfaction",
        "satisfaction_score",
        "patient_satisfaction",
        "rating",
        "rating_score"
    ]:
        satisfaction_column = column
        break

if satisfaction_column is None:

    for column in df.columns:

        if (
            "satisfaction" in column
            or "rating" in column
        ):
            satisfaction_column = column
            break

print(
    "\nSatisfaction column:",
    satisfaction_column
)


# ------------------------------------------------------------
# 6. CONVERT SATISFACTION TO NUMBER
# ------------------------------------------------------------

if satisfaction_column is not None:

    df[satisfaction_column] = pd.to_numeric(
        df[satisfaction_column],
        errors="coerce"
    )

    print(
        "\nSatisfaction statistics:"
    )

    print(
        df[satisfaction_column].describe()
    )


# ------------------------------------------------------------
# 7. KPI 1 - AVERAGE SATISFACTION
# ------------------------------------------------------------

if satisfaction_column is not None:

    average_satisfaction = (
        df[satisfaction_column].mean()
    )

else:

    average_satisfaction = 0

print("\n================ KPI 1 ================\n")

print(
    "Average Patient Satisfaction:",
    round(average_satisfaction, 2)
)


# ------------------------------------------------------------
# 8. KPI 2 - HIGHEST SATISFACTION
# ------------------------------------------------------------

if satisfaction_column is not None:

    highest_satisfaction = (
        df[satisfaction_column].max()
    )

else:

    highest_satisfaction = 0

print("\n================ KPI 2 ================\n")

print(
    "Highest Satisfaction Score:",
    highest_satisfaction
)


# ------------------------------------------------------------
# 9. KPI 3 - LOWEST SATISFACTION
# ------------------------------------------------------------

if satisfaction_column is not None:

    lowest_satisfaction = (
        df[satisfaction_column].min()
    )

else:

    lowest_satisfaction = 0

print("\n================ KPI 3 ================\n")

print(
    "Lowest Satisfaction Score:",
    lowest_satisfaction
)


# ------------------------------------------------------------
# 10. KPI 4 - NUMBER OF PATIENT RESPONSES
# ------------------------------------------------------------

total_responses = len(df)

print("\n================ KPI 4 ================\n")

print(
    "Total Patient Responses:",
    total_responses
)


# ------------------------------------------------------------
# 11. KPI 5 - POSITIVE SATISFACTION RATE
# ------------------------------------------------------------

if satisfaction_column is not None:

    maximum_score = df[satisfaction_column].max()

    # Consider scores >= 80% of maximum as positive
    positive_limit = maximum_score * 0.80

    positive_patients = (
        df[satisfaction_column]
        >= positive_limit
    ).sum()

    positive_rate = (
        positive_patients
        / df[satisfaction_column].notna().sum()
        * 100
    )

else:

    positive_rate = 0

print("\n================ KPI 5 ================\n")

print(
    "Positive Satisfaction Rate:",
    round(positive_rate, 2),
    "%"
)


# ------------------------------------------------------------
# 12. SATISFACTION DISTRIBUTION
# ------------------------------------------------------------

if satisfaction_column is not None:

    plt.figure(figsize=(10, 5))

    plt.hist(
        df[satisfaction_column].dropna(),
        bins=10
    )

    plt.title(
        "Patient Satisfaction Distribution"
    )

    plt.xlabel(
        "Satisfaction Score"
    )

    plt.ylabel(
        "Number of Patients"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.show()


# ------------------------------------------------------------
# 13. FIND DEPARTMENT COLUMN
# ------------------------------------------------------------

department_column = None

for column in df.columns:

    if column in [
        "department",
        "dept",
        "department_name"
    ]:

        department_column = column
        break

if department_column is None:

    for column in df.columns:

        if "department" in column:

            department_column = column
            break

print(
    "\nDepartment column:",
    department_column
)


# ------------------------------------------------------------
# 14. SATISFACTION BY DEPARTMENT
# ------------------------------------------------------------

if (
    department_column is not None
    and satisfaction_column is not None
):

    department_satisfaction = (
        df.groupby(department_column)
        [satisfaction_column]
        .mean()
        .sort_values(ascending=False)
    )

    print(
        "\n================ SATISFACTION BY DEPARTMENT ================\n"
    )

    print(
        department_satisfaction
    )


# ------------------------------------------------------------
# 15. DEPARTMENT CHART
# ------------------------------------------------------------

if (
    department_column is not None
    and satisfaction_column is not None
):

    plt.figure(figsize=(10, 6))

    plt.bar(
        department_satisfaction.index.astype(str),
        department_satisfaction.values
    )

    plt.title(
        "Average Patient Satisfaction by Department"
    )

    plt.xlabel(
        "Department"
    )

    plt.ylabel(
        "Average Satisfaction"
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


# ------------------------------------------------------------
# 16. HIGHEST & LOWEST DEPARTMENT
# ------------------------------------------------------------

if (
    department_column is not None
    and satisfaction_column is not None
    and len(department_satisfaction) > 0
):

    highest_department = (
        department_satisfaction.idxmax()
    )

    lowest_department = (
        department_satisfaction.idxmin()
    )

    print(
        "\nHighest satisfaction department:",
        highest_department
    )

    print(
        "Lowest satisfaction department:",
        lowest_department
    )


# ------------------------------------------------------------
# 17. BOX PLOT - OUTLIERS
# ------------------------------------------------------------

if satisfaction_column is not None:

    plt.figure(figsize=(8, 5))

    plt.boxplot(
        df[satisfaction_column].dropna()
    )

    plt.title(
        "Patient Satisfaction - Outlier Detection"
    )

    plt.ylabel(
        "Satisfaction Score"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.show()


# ------------------------------------------------------------
# 18. FINAL KPI SUMMARY
# ------------------------------------------------------------

print("\n")
print("====================================================")
print("          PATIENT SATISFACTION KPI SUMMARY")
print("====================================================")

print(
    "KPI 1 - Average Satisfaction:",
    round(average_satisfaction, 2)
)

print(
    "KPI 2 - Highest Satisfaction:",
    highest_satisfaction
)

print(
    "KPI 3 - Lowest Satisfaction:",
    lowest_satisfaction
)

print(
    "KPI 4 - Total Patient Responses:",
    total_responses
)

print(
    "KPI 5 - Positive Satisfaction Rate:",
    round(positive_rate, 2),
    "%"
)

print("====================================================")


# ------------------------------------------------------------
# 19. TOP 3 FINDINGS
# ------------------------------------------------------------

print("\n================ TOP 3 FINDINGS ================\n")

print(
    "1. Average patient satisfaction is",
    round(average_satisfaction, 2)
)

print(
    "2. The positive satisfaction rate is",
    round(positive_rate, 2),
    "%"
)

if (
    department_column is not None
    and satisfaction_column is not None
    and len(department_satisfaction) > 0
):

    print(
        "3. The department with the highest average "
        "satisfaction is:",
        highest_department
    )

print("\nPatient satisfaction analysis completed successfully!")