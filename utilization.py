# ============================================================
# SUNRISE RESOURCE UTILISATION - EDA & KPI ANALYSIS
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1. LOAD CSV
# ------------------------------------------------------------

file_name = "sunrise_resource_utilisation.csv"

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
# 5. SHOW ALL NUMERICAL COLUMNS
# ------------------------------------------------------------

print("\n================ NUMERICAL COLUMNS ================\n")

numeric_columns = df.select_dtypes(
    include=np.number
).columns.tolist()

print(numeric_columns)


# ------------------------------------------------------------
# 6. FIND UTILISATION COLUMN
# ------------------------------------------------------------

utilisation_column = None

for column in df.columns:

    if column in [
        "utilisation",
        "utilization",
        "utilisation_rate",
        "utilization_rate",
        "utilisation_percentage",
        "utilization_percentage"
    ]:

        utilisation_column = column
        break


if utilisation_column is None:

    for column in df.columns:

        if (
            "utilisation" in column
            or "utilization" in column
            or "occupancy" in column
        ):

            utilisation_column = column
            break


print(
    "\nUtilisation column:",
    utilisation_column
)


# ------------------------------------------------------------
# 7. IF COLUMN WAS NOT AUTOMATICALLY FOUND
# ------------------------------------------------------------

if utilisation_column is None:

    print("\nCould not automatically identify the utilisation column.")

    print(
        "Please check the column names printed above."
    )


# ------------------------------------------------------------
# 8. CONVERT UTILISATION TO NUMERIC
# ------------------------------------------------------------

if utilisation_column is not None:

    df[utilisation_column] = pd.to_numeric(
        df[utilisation_column],
        errors="coerce"
    )

    print(
        "\nUtilisation statistics:"
    )

    print(
        df[utilisation_column].describe()
    )


# ------------------------------------------------------------
# KPI 1 - AVERAGE UTILISATION
# ------------------------------------------------------------

if utilisation_column is not None:

    average_utilisation = (
        df[utilisation_column].mean()
    )

else:

    average_utilisation = 0


print("\n================ KPI 1 ================\n")

print(
    "Average Resource Utilisation:",
    round(average_utilisation, 2)
)


# ------------------------------------------------------------
# KPI 2 - MAXIMUM UTILISATION
# ------------------------------------------------------------

if utilisation_column is not None:

    maximum_utilisation = (
        df[utilisation_column].max()
    )

else:

    maximum_utilisation = 0


print("\n================ KPI 2 ================\n")

print(
    "Maximum Resource Utilisation:",
    round(maximum_utilisation, 2)
)


# ------------------------------------------------------------
# KPI 3 - MINIMUM UTILISATION
# ------------------------------------------------------------

if utilisation_column is not None:

    minimum_utilisation = (
        df[utilisation_column].min()
    )

else:

    minimum_utilisation = 0


print("\n================ KPI 3 ================\n")

print(
    "Minimum Resource Utilisation:",
    round(minimum_utilisation, 2)
)


# ------------------------------------------------------------
# KPI 4 - NUMBER OF RESOURCE RECORDS
# ------------------------------------------------------------

total_records = len(df)

print("\n================ KPI 4 ================\n")

print(
    "Total Resource Records:",
    total_records
)


# ------------------------------------------------------------
# KPI 5 - HIGH UTILISATION RATE
# ------------------------------------------------------------

if utilisation_column is not None:

    # Treat values >= 80 as high utilisation
    high_utilisation_count = (
        df[utilisation_column] >= 80
    ).sum()

    valid_records = (
        df[utilisation_column].notna().sum()
    )

    if valid_records > 0:

        high_utilisation_rate = (
            high_utilisation_count
            / valid_records
            * 100
        )

    else:

        high_utilisation_rate = 0

else:

    high_utilisation_rate = 0


print("\n================ KPI 5 ================\n")

print(
    "High Utilisation Rate:",
    round(high_utilisation_rate, 2),
    "%"
)


# ------------------------------------------------------------
# 9. RESOURCE COLUMN
# ------------------------------------------------------------

resource_column = None

for column in df.columns:

    if column in [
        "resource",
        "resource_name",
        "resource_type",
        "facility",
        "equipment"
    ]:

        resource_column = column
        break


if resource_column is None:

    for column in df.columns:

        if (
            "resource" in column
            or "facility" in column
            or "equipment" in column
        ):

            resource_column = column
            break


print(
    "\nResource column:",
    resource_column
)


# ------------------------------------------------------------
# 10. RESOURCE-WISE UTILISATION
# ------------------------------------------------------------

if (
    resource_column is not None
    and utilisation_column is not None
):

    resource_analysis = (
        df.groupby(resource_column)
        [utilisation_column]
        .mean()
        .sort_values(ascending=False)
    )

    print(
        "\n================ RESOURCE-WISE UTILISATION ================\n"
    )

    print(resource_analysis)


# ------------------------------------------------------------
# 11. RESOURCE UTILISATION CHART
# ------------------------------------------------------------

if (
    resource_column is not None
    and utilisation_column is not None
):

    plt.figure(figsize=(10, 6))

    plt.bar(
        resource_analysis.index.astype(str),
        resource_analysis.values
    )

    plt.title(
        "Average Resource Utilisation"
    )

    plt.xlabel(
        "Resource"
    )

    plt.ylabel(
        "Average Utilisation"
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


# ------------------------------------------------------------
# 12. TOP 5 MOST UTILIZED RESOURCES
# ------------------------------------------------------------

if (
    resource_column is not None
    and utilisation_column is not None
):

    print(
        "\n================ TOP 5 UTILIZED RESOURCES ================\n"
    )

    print(
        resource_analysis.head(5)
    )


# ------------------------------------------------------------
# 13. BOTTOM 5 / UNDER-UTILIZED RESOURCES
# ------------------------------------------------------------

if (
    resource_column is not None
    and utilisation_column is not None
):

    print(
        "\n================ BOTTOM 5 UTILIZED RESOURCES ================\n"
    )

    print(
        resource_analysis.tail(5)
    )


# ------------------------------------------------------------
# 14. UTILISATION DISTRIBUTION
# ------------------------------------------------------------

if utilisation_column is not None:

    plt.figure(figsize=(10, 5))

    plt.hist(
        df[utilisation_column].dropna(),
        bins=20
    )

    plt.title(
        "Resource Utilisation Distribution"
    )

    plt.xlabel(
        "Utilisation"
    )

    plt.ylabel(
        "Frequency"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.show()


# ------------------------------------------------------------
# 15. OUTLIER DETECTION
# ------------------------------------------------------------

if utilisation_column is not None:

    plt.figure(figsize=(8, 5))

    plt.boxplot(
        df[utilisation_column].dropna()
    )

    plt.title(
        "Resource Utilisation - Outlier Detection"
    )

    plt.ylabel(
        "Utilisation"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.show()


# ------------------------------------------------------------
# 16. DATE COLUMN
# ------------------------------------------------------------

date_column = None

for column in df.columns:

    if "date" in column:

        date_column = column
        break


print(
    "\nDate column:",
    date_column
)


# ------------------------------------------------------------
# 17. TREND ANALYSIS
# ------------------------------------------------------------

if (
    date_column is not None
    and utilisation_column is not None
):

    df[date_column] = pd.to_datetime(
        df[date_column],
        errors="coerce"
    )

    date_data = df.dropna(
        subset=[date_column]
    )

    if len(date_data) > 0:

        monthly_utilisation = (
            date_data
            .set_index(date_column)
            [utilisation_column]
            .resample("ME")
            .mean()
        )

        print(
            "\n================ MONTHLY UTILISATION ================\n"
        )

        print(monthly_utilisation)


        plt.figure(figsize=(12, 5))

        plt.plot(
            monthly_utilisation.index,
            monthly_utilisation.values,
            marker="o"
        )

        plt.title(
            "Monthly Resource Utilisation Trend"
        )

        plt.xlabel(
            "Month"
        )

        plt.ylabel(
            "Average Utilisation"
        )

        plt.xticks(rotation=45)

        plt.grid(True)

        plt.tight_layout()

        plt.show()


# ------------------------------------------------------------
# 18. FINAL KPI SUMMARY
# ------------------------------------------------------------

print("\n")
print("======================================================")
print("          RESOURCE UTILISATION KPI SUMMARY")
print("======================================================")

print(
    "KPI 1 - Average Utilisation:",
    round(average_utilisation, 2)
)

print(
    "KPI 2 - Maximum Utilisation:",
    round(maximum_utilisation, 2)
)

print(
    "KPI 3 - Minimum Utilisation:",
    round(minimum_utilisation, 2)
)

print(
    "KPI 4 - Total Resource Records:",
    total_records
)

print(
    "KPI 5 - High Utilisation Rate:",
    round(high_utilisation_rate, 2),
    "%"
)

print("======================================================")


# ------------------------------------------------------------
# 19. TOP 3 PATTERNS / FINDINGS
# ------------------------------------------------------------

print("\n================ TOP 3 FINDINGS ================\n")

print(
    "1. Average resource utilisation is:",
    round(average_utilisation, 2)
)

print(
    "2. Maximum resource utilisation is:",
    round(maximum_utilisation, 2)
)

print(
    "3. High utilisation rate is:",
    round(high_utilisation_rate, 2),
    "%"
)


print(
    "\nResource utilisation analysis completed successfully!"
)