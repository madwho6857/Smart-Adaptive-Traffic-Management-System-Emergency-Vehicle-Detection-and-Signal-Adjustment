# Generating an NLP Summary of the vehicle data
def generate_summary(avg_total, avg_emergency):
    summary = (
        f"Throughout the day, an average of {avg_total:.2f} vehicles were detected per interval. "
        f"This includes approximately {avg_emergency:.2f} emergency vehicles."
    )
    return summary

# Call the function with the average values
summary = generate_summary(5, 2)  # Example values
print(summary)
