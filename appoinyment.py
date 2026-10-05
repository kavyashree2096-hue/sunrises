# ============================================================
# HEALTHCARE APPOINTMENTS - EDA & KPI ANALYSIS
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1. LOAD CSV FILE
# ------------------------------------------------------------

file_name = "da_healthcare_appointments (2).csv"

df = pd.read_csv(file_name)

print("\n================ FIRST 5 ROWS ================\n")
print(df.head())

print("\n================ DATASET SHAPE ================\n")
print(df.shape)

print("\n================ COLUMN NAMES ================\n")
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

print("\n================ CLEANED COLUMNS ================\n")
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
# 5. FIND IMPORTANT COLUMNS
# ------------------------------------------------------------

print("\n================ COLUMN CHECK ================\n")

print("Available columns:")
for column in df.columns:
    print("-", column)


# ------------------------------------------------------------
# 6. FIND STATUS COLUMN
# ------------------------------------------------------------

status_column = None

for column in df.columns:
    if column in ["status", "appointment_status", "attendance_status"]:
        status_column = column
        break

if status_column is None:
    for column in df.columns:
        if "status" in column:
            status_column = column
            break

print("\nStatus column:", status_column)


# ------------------------------------------------------------
# 7. APPOINTMENT STATUS ANALYSIS
# ------------------------------------------------------------

if status_column is not None:

    print("\n================ APPOINTMENT STATUS ================\n")

    print(df[status_column].value_counts())

    print("\nStatus percentages:")

    status_percentage = (
        df[status_column]
        .value_counts(normalize=True)
        * 100
    )

    print(status_percentage.round(2))


# ------------------------------------------------------------
# 8. TOTAL APPOINTMENTS
# ------------------------------------------------------------

total_appointments = len(df)

print("\n================ KPI 1 ================\n")
print("Total Appointments:", total_appointments)


# ------------------------------------------------------------
# 9. NO-SHOW ANALYSIS
# ------------------------------------------------------------

no_show_count = 0

if status_column is not None:

    status_values = (
        df[status_column]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    no_show_count = status_values.isin([
        "no-show",
        "no show",
        "noshow",
        "no_show"
    ]).sum()

print("\n================ KPI 2 ================\n")
print("No-show Appointments:", no_show_count)


# ------------------------------------------------------------
# 10. NO-SHOW RATE
# ------------------------------------------------------------

if total_appointments > 0:

    no_show_rate = (
        no_show_count / total_appointments
    ) * 100

else:

    no_show_rate = 0

print("\n================ KPI 3 ================\n")
print(
    "No-show Rate:",
    round(no_show_rate, 2),
    "%"
)


# ------------------------------------------------------------
# 11. CANCELLATION ANALYSIS
# ------------------------------------------------------------

cancelled_count = 0

if status_column is not None:

    cancelled_count = status_values.isin([
        "cancelled",
        "canceled",
        "cancel"
    ]).sum()

print("\n================ KPI 4 ================\n")
print("Cancelled Appointments:", cancelled_count)


# ------------------------------------------------------------
# 12. CANCELLATION RATE
# ------------------------------------------------------------

if total_appointments > 0:

    cancellation_rate = (
        cancelled_count / total_appointments
    ) * 100

else:

    cancellation_rate = 0

print("\n================ KPI 5 ================\n")
print(
    "Cancellation Rate:",
    round(cancellation_rate, 2),
    "%"
)


# ------------------------------------------------------------
# 13. APPOINTMENT STATUS CHART
# ------------------------------------------------------------

if status_column is not None:

    plt.figure(figsize=(8, 5))

    df[status_column].value_counts().plot(
        kind="bar"
    )

    plt.title("Appointment Status Distribution")
    plt.xlabel("Appointment Status")
    plt.ylabel("Number of Appointments")

    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# 14. FIND DEPARTMENT COLUMN
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

print("\nDepartment column:", department_column)


# ------------------------------------------------------------
# 15. NO-SHOW RATE BY DEPARTMENT
# ------------------------------------------------------------

if department_column is not None and status_column is not None:

    temp = df.copy()

    temp["is_no_show"] = (
        temp[status_column]
        .astype(str)
        .str.lower()
        .str.strip()
        .isin([
            "no-show",
            "no show",
            "noshow",
            "no_show"
        ])
    )

    department_analysis = (
        temp.groupby(department_column)
        .agg(
            total_appointments=(
                status_column,
                "count"
            ),
            no_show_count=(
                "is_no_show",
                "sum"
            )
        )
    )

    department_analysis["no_show_rate"] = (
        department_analysis["no_show_count"]
        / department_analysis["total_appointments"]
        * 100
    )

    department_analysis = (
        department_analysis
        .sort_values(
            "no_show_rate",
            ascending=False
        )
    )

    print(
        "\n================ NO-SHOW RATE BY DEPARTMENT ================\n"
    )

    print(department_analysis)


# ------------------------------------------------------------
# 16. DEPARTMENT CHART
# ------------------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.bar(
        department_analysis.index.astype(str),
        department_analysis["no_show_rate"]
    )

    plt.title("No-show Rate by Department")
    plt.xlabel("Department")
    plt.ylabel("No-show Rate (%)")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# 17. FIND DATE COLUMN
# ------------------------------------------------------------

date_column = None

for column in df.columns:

    if "date" in column:

        date_column = column
        break

print("\nDate column:", date_column)


# ------------------------------------------------------------
# 18. TREND ANALYSIS
# ------------------------------------------------------------

if date_column is not None:

    df[date_column] = pd.to_datetime(
        df[date_column],
        errors="coerce"
    )

    date_data = df.dropna(
        subset=[date_column]
    )

    if len(date_data) > 0:

        monthly_appointments = (
            date_data
            .set_index(date_column)
            .resample("ME")
            .size()
        )

        print(
            "\n================ MONTHLY APPOINTMENTS ================\n"
        )

        print(monthly_appointments)

        plt.figure(figsize=(12, 5))

        plt.plot(
            monthly_appointments.index,
            monthly_appointments.values,
            marker="o"
        )

        plt.title("Monthly Appointment Trend")
        plt.xlabel