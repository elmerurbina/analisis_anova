import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


# Function to calculate ANOVA
def calculate_anova(groups):
    k = len(groups)  # Number of groups
    n = sum(len(group) for group in groups)  # Total number of observations

    # Group means and overall mean
    group_means = [np.mean(group) for group in groups]
    overall_mean = np.mean([item for group in groups for item in group])

    # Sum of Squares Between (SSB)
    SSB = sum(len(group) * (mean - overall_mean) ** 2 for group, mean in zip(groups, group_means))

    # Sum of Squares Within (SSW)
    SSW = sum(sum((item - mean) ** 2 for item in group) for group, mean in zip(groups, group_means))

    # Total Sum of Squares (SST)
    SST = SSB + SSW

    # Degrees of freedom
    df_between = k - 1
    df_within = n - k

    # Mean Squares
    MSB = SSB / df_between
    MSW = SSW / df_within

    # F-statistic
    F = MSB / MSW

    # Critical F-value and p-value
    alpha = 0.05
    F_crit = stats.f.ppf(1 - alpha, df_between, df_within)
    p_value = stats.f.sf(F, df_between, df_within)

    return {
        "Group Means": group_means,
        "Overall Mean": overall_mean,
        "SSB": SSB,
        "SSW": SSW,
        "SST": SST,
        "df_between": df_between,
        "df_within": df_within,
        "MSB": MSB,
        "MSW": MSW,
        "F": F,
        "F_crit": F_crit,
        "p_value": p_value,
    }


# Visualization
def visualize_results(groups, group_means):
    labels = [f"Group {i + 1}" for i in range(len(groups))]
    plt.bar(labels, group_means, color='skyblue')
    plt.xlabel("Groups")
    plt.ylabel("Mean")
    plt.title("Comparison of Group Means")
    plt.show()


# Main program
if __name__ == "__main__":
    groups = []
    print(
        "Enter data for each group separated by commas (e.g., 1, 2, 3). Press Enter to add the next group or type 'X' to finish:")

    while True:
        user_input = input("Enter data for group (or 'X' to finish): ").strip()
        if user_input.upper() == "X":
            break
        try:
            group = [float(x) for x in user_input.split(",")]
            groups.append(group)
        except ValueError:
            print("Invalid input. Please enter numeric values separated by commas.")

    if len(groups) < 2:
        print("At least two groups are required for ANOVA.")
    else:
        # Perform ANOVA
        results = calculate_anova(groups)
        print("\nANOVA Results:")
        for key, value in results.items():
            print(f"{key}: {value}")

        # Visualize results
        visualize_results(groups, results["Group Means"])
