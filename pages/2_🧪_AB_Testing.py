import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="A/B Testing", page_icon="🧪")

st.markdown("# A/B Testing")
st.sidebar.header("A/B Testing")
st.write(
    """In this page, we will simulate an A/B Testing Experiment. We're generating a bunch of random numbers in a loop.
    We will then compare the results of the two groups.
    The two groups represent employees in two distinct departments, and the metric is the engagement score from a survey."""
)

# Add parameters for the sample size, power, and significance level
# Put in collapse section
parameter_expander = st.sidebar.expander("Parameters", expanded=False)
parameter_expander.markdown("## Testing Parameters")
sample_size = parameter_expander.slider("Sample Size", 10, 1000, 100, 10)
power = parameter_expander.slider("Power", 0.0, 1.0, 0.8, 0.1)
significance_level = parameter_expander.slider("Significance Level", 0.0, 1.0, 0.05, 0.01)

# Generate engagement scores for two groups of employees (A and B), with both groups having different mean and standard deviation
# Group A
groupa_expander = st.sidebar.expander("Group A", expanded=False)
groupa_expander.markdown("## Group A")
mean_a = groupa_expander.slider("Mean of Group A", 0, 100, 75, 1)
std_a = groupa_expander.slider("Standard Deviation of Group A", 0.0, 20.0, 5.0, 0.1)
engagement_scores_a = np.random.normal(mean_a, std_a, sample_size)

# Group B
groupb_expander = st.sidebar.expander("Group B", expanded=False)
groupb_expander.markdown("## Group B")
mean_b = groupb_expander.slider("Mean of Group B", 0, 100, 55, 1)
std_b = groupb_expander.slider("Standard Deviation of Group B", 0.0, 20.0, 5.0, 0.1)
engagement_scores_b = np.random.normal(mean_b, std_b, sample_size)

# Plot the distribution of the engagement scores for the two groups
fig, ax = plt.subplots()
sns.histplot(engagement_scores_a, ax=ax, color="blue", label="Group A")
sns.histplot(engagement_scores_b, ax=ax, color="red", label="Group B")
ax.set_xlabel("Engagement Score")
ax.set_ylabel("Count")
ax.set_title("Distribution of Engagement Scores for the Two Groups")
ax.legend()
st.pyplot(fig)

# Calculate the p-value
p_value = np.sum(engagement_scores_b > engagement_scores_a) / len(engagement_scores_b)
st.write(f"The p-value is {p_value:.4f}")