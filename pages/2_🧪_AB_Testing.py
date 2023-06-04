import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import seaborn as sns
from scipy import stats
from statsmodels.stats.power import TTestIndPower

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
experiment_param = parameter_expander.selectbox("Parameter to control", ["Sample Size", "Power"])
if experiment_param == "Sample Size":
    sample_size = parameter_expander.slider("Sample Size", 1, 100, 10, 1)
elif experiment_param == "Power":
    power = parameter_expander.slider("Power", 0.0, 1.0, 0.8, 0.1)
significance_level = parameter_expander.slider("Significance Level", 0.01, 0.1, 0.05, 0.01)
parameter_expander.write("Do not use the below button!")
parameter_expander.button("p-hacking")

# Generate engagement scores for two groups of employees (A and B), with both groups having different mean and standard deviation
# Group A
groupa_expander = st.sidebar.expander("Group A", expanded=False)
groupa_expander.markdown("## Group A")
mean_a = groupa_expander.slider("Mean of Group A", 0, 100, 50, 1)
std_a = groupa_expander.slider("Standard Deviation of Group A", 0.0, 20.0, 5.0, 0.1)

# Group B
groupb_expander = st.sidebar.expander("Group B", expanded=False)
groupb_expander.markdown("## Group B")
mean_b = groupb_expander.slider("Mean of Group B", 0, 100, 52, 1)
std_b = groupb_expander.slider("Standard Deviation of Group B", 0.0, 20.0, 5.0, 0.1)

# Determining the estimated effect size, and calculating the sample size needed to achieve a certain power
st.subheader("Experimentation design")
parameter_description = st.expander("Parameter Description", expanded=False)
parameter_description.markdown("""It is important to determine the effect size, sample size, power, and significance level before running the experiment:
- The **effect size** is the difference between the means of the two groups, divided by the pooled standard deviation. It sometimes needs to be estimated before running the experiment.
- The **sample size** is the number of employees in each group.
- The **power** is the probability of rejecting the null hypothesis when it is false. It is usually set to 0.8.
- The **significance level** is the probability of rejecting the null hypothesis when it is true. It is usually set to 0.05.
- (Optional) How long should the experiment run for? This depends on the number of employees in each group, and the number of employees that are surveyed each day.""")
col1, col2, col3, col4, col5 = st.columns(5)
effect_size = (mean_b - mean_a) / np.sqrt((std_a ** 2 + std_b ** 2) / 2)
if experiment_param == "Power":
    # Calculate the sample size needed to achieve a certain power
    sample_size = int(TTestIndPower().solve_power(effect_size=effect_size, power=power, alpha=significance_level))
elif experiment_param == "Sample Size":
    # Calculate the power of the test
    power = round(TTestIndPower().power(effect_size=effect_size, nobs1=sample_size, alpha=significance_level),2)

# Calculate the p-value using a t-test
engagement_scores_a = np.random.normal(mean_a, std_a, sample_size)
engagement_scores_b = np.random.normal(mean_b, std_b, sample_size)
t_stat, p_value = stats.ttest_ind(engagement_scores_a, engagement_scores_b)

# Display the parameters
col1, col2, col3, col4 = st.columns(4)
col1.metric("Effect Size", effect_size)
col2.metric("Sample Size", sample_size)
col3.metric("Power", power)
col4.metric("Significance Level", significance_level)

# Display the results of the experiment
st.subheader("Results of a t-test")

# Plot the distribution of the engagement scores for the two groups
fig = go.Figure()
fig.add_trace(go.Histogram(x=engagement_scores_a, name="Group A", marker_color="red"))
fig.add_trace(go.Histogram(x=engagement_scores_b, name="Group B", marker_color="sky blue"))
fig.update_layout(showlegend=True, title="Distribution of Engagement Scores for the Two Groups", xaxis_title="Engagement Score", yaxis_title="Count", barmode="overlay")
fig.update_traces(opacity=0.60)
st.plotly_chart(fig)

st.markdown("""The results of the experiment are displayed below:""")
col_a, col_b = st.columns(2)
col_a.metric("T-Statistic", round(t_stat, 2))
col_b.metric("P-Value", round(p_value, 2))