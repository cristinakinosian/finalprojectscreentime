"""Streamlit app: Improving health through reducing sedentary screen time.

Run locally with:
    streamlit run streamlit_final_project_clean.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit


# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Reducing Sedentary Screen Time",
    page_icon="📱",
    layout="wide",
)

US_AVERAGE = 7 + 2 / 60        # 7 hours 2 minutes
WORLD_AVERAGE = 6 + 54 / 60    # 6 hours 54 minutes
NEGATIVE_THRESHOLD = 2         # 2 hours recreational screen time


# -----------------------------
# Helper functions
# -----------------------------
def show_bar_graph(labels, values, title, ylabel="Hours per day"):
    """Create and display a Streamlit-compatible bar graph."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, values)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def show_table(data, title):
    """Display a pandas DataFrame with a title and return the DataFrame."""
    st.subheader(title)
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    return df


def show_donut_chart(labels, data, title):
    """Create and display a donut chart."""
    if sum(data) == 0:
        st.info("No strategies were selected, so no donut chart can be displayed yet.")
        return

    fig, ax = plt.subplots(figsize=(7, 7))
    explode = [0.05] * len(data)

    ax.pie(
        data,
        labels=labels,
        explode=explode,
        autopct="%1.1f%%",
        pctdistance=0.82,
        startangle=90,
    )

    centre_circle = plt.Circle((0, 0), 0.65, fc="white")
    ax.add_artist(centre_circle)
    ax.set_title(title)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def linear_model(x, m, b):
    """Simple linear model used for curve fitting."""
    return m * x + b


# -----------------------------
# App title and introduction
# -----------------------------
st.title("Final Project: Improving Health Through Reducing Sedentary Screen Time")

st.write(
    "This interactive project helps estimate your daily screen time, compare it with common averages, "
    "reflect on possible side effects, and choose personalized strategies for reducing sedentary screen use."
)

st.divider()


# -----------------------------
# Section 1: Screen habits
# -----------------------------
st.header("1. What are your screen habits?")
st.write("If you have a smartphone, you can find your average daily screen time in your device settings.")

col1, col2, col3 = st.columns(3)

with col1:
    phone_screen_time = st.number_input(
        "Daily smartphone screen time average, in hours",
        min_value=0.0,
        max_value=24.0,
        value=4.0,
        step=0.25,
    )

with col2:
    non_leisure_screen_time = st.number_input(
        "Unavoidable non-leisure screen time, in hours",
        min_value=0.0,
        max_value=24.0,
        value=3.0,
        step=0.25,
    )

with col3:
    recreational_screen_time = st.number_input(
        "Other recreational screen time, not including smartphone, in hours",
        min_value=0.0,
        max_value=24.0,
        value=2.0,
        step=0.25,
    )

total_screen_time = phone_screen_time + non_leisure_screen_time + recreational_screen_time

st.subheader("Daily Screen Time Comparison")
show_bar_graph(
    ["Your Phone Use", "U.S. Average", "Worldwide Average"],
    [phone_screen_time, US_AVERAGE, WORLD_AVERAGE],
    "Daily Smartphone Screen Time Comparison",
)

st.info(f"Your estimated total daily screen time is **{total_screen_time:.2f} hours**.")
st.caption("Note: Total screen time is an approximation based on your self-reported inputs.")

show_bar_graph(
    ["Phone\nScreen Time", "Other Leisure\nScreen Time", "Unavoidable\nScreen Time", "Total\nScreen Time"],
    [phone_screen_time, recreational_screen_time, non_leisure_screen_time, total_screen_time],
    "Your Estimated Daily Screen Time",
)

st.divider()


# -----------------------------
# Section 2: Recreational screen-time threshold
# -----------------------------
st.header("2. Recreational screen-time threshold")
st.write(
    "Screen time for recreation can feel relaxing, but too much sedentary recreational screen time "
    "may be linked to negative health outcomes."
)

guess = st.slider(
    "How many hours of recreational screen time per day do you think is the threshold for negative health outcomes?",
    min_value=0.0,
    max_value=8.0,
    value=3.0,
    step=0.5,
)

if guess == NEGATIVE_THRESHOLD:
    st.success("Precisely! The threshold used in this project is about 2 hours per day.")
elif guess < NEGATIVE_THRESHOLD:
    st.warning("Not quite — the threshold used in this project is a little higher: about 2 hours per day.")
else:
    st.warning("It is actually less than that: about 2 hours per day.")

st.write(
    "If the excessive recreational screen-time threshold is regularly exceeded, being physically active "
    "may not fully offset the negative health effects of long sedentary periods."
)

st.divider()


# -----------------------------
# Section 3: Symptom checklist
# -----------------------------
st.header("3. Symptom checklist")
st.write("Which of the following have you experienced after high-screen-time days?")

symptoms = [
    "difficulty sleeping",
    "anxiety",
    "depression",
    "eye strain or headaches",
    "neck, shoulder, or back pain",
    "difficulty focusing",
]

symptom_results = []
for symptom in symptoms:
    experienced = st.checkbox(f"I have experienced {symptom}", key=f"symptom_{symptom}")
    symptom_results.append({
        "Symptom": symptom,
        "User Experiences This?": "Yes" if experienced else "No",
    })

number_of_symptoms = sum(row["User Experiences This?"] == "Yes" for row in symptom_results)
show_table(symptom_results, "Your Symptom Checklist")

if number_of_symptoms == 0:
    st.success("Wow, that's great! You may not be noticing obvious side effects right now.")
else:
    st.info(
        "You're not alone! Excessive sedentary screen time has been associated with sleep problems, "
        "mental health challenges, eye strain, headaches, and body pain."
    )

st.divider()


# -----------------------------
# Section 4: Motivation / continue logic
# -----------------------------
st.header("4. Motivation check")

wants_to_continue = st.radio(
    "Do you want to proceed and learn how to improve your quality of life and reduce these symptoms?",
    ["Yes", "No"],
    horizontal=True,
)

if wants_to_continue == "Yes":
    st.success("Great :) let's continue!")
else:
    st.write(
        "Even if you live an otherwise healthy, active lifestyle, excessive passive screen time may still "
        "affect long-term health. The same behavior-change principles can also apply to many other habits."
    )
    fallback_choice = st.radio(
        "Would you like to continue anyway?",
        ["Continue and learn", "Stop here"],
        horizontal=True,
    )
    if fallback_choice == "Stop here":
        st.stop()

st.divider()


# -----------------------------
# Section 5: Current strategies
# -----------------------------
st.header("5. Current screen-time reduction strategies")
st.write("Which of the following strategies do you already use?")

current_strategies = [
    "Use app time limits",
    "Disable non-essential notifications",
    "Have a screen-free time of day, such as before bed",
    "Keep your phone out of reach while studying or working",
]

used_strategies = []
for strategy in current_strategies:
    if st.checkbox(strategy, key=f"current_{strategy}"):
        used_strategies.append(strategy)

st.write(f"You currently use **{len(used_strategies)}** screen-time reduction strategies.")

if len(used_strategies) == 0:
    st.info("That's okay — this gives you a clear starting point.")
elif len(used_strategies) <= 2:
    st.success("Nice start! There is still room to add a few more supports.")
else:
    st.success("Great job — you already have several helpful strategies in place.")

st.divider()


# -----------------------------
# Section 6: Strategy checklist
# -----------------------------
st.header("6. Screen-time reduction strategies you might use")

strategy_categories = {
    "Movement During Unavoidable Screen Time": [
        "standing desk",
        "walking pad",
        "under-desk pedal device",
        "taking movement breaks during work/school screen time",
    ],
    "Increasing Friction Against Recreational Screen Use": [
        "app time limits",
        "disabling non-essential notifications",
        "deleting or hiding distracting apps",
        "keeping phone away from bed",
        "creating screen-free zones",
    ],
    "Decreasing Friction for Physical Activity": [
        "placing workout equipment in visible areas",
        "watching TV only while walking/stretching",
        "using VR fitness or active video games",
        "planning non-screen hobbies in advance",
    ],
}

strategy_results = []
category_scores = {}

for category, strategies in strategy_categories.items():
    st.subheader(category)
    used_count = 0

    for strategy in strategies:
        interested = st.checkbox(
            f"I would use this strategy: {strategy}",
            key=f"interested_{category}_{strategy}",
        )

        if interested:
            used_count += 1

        strategy_results.append({
            "Category": category,
            "Strategy": strategy,
            "Interested?": "Yes" if interested else "No",
        })

    category_scores[category] = used_count

strategy_df = show_table(strategy_results, "Your Screen-Time Strategy Checklist")

show_donut_chart(
    list(category_scores.keys()),
    list(category_scores.values()),
    "Distribution of Screen-Time Strategies You're Interested In",
)

st.divider()


# -----------------------------
# Section 7: Personalized recommendations
# -----------------------------
st.header("7. Personalized intervention recommendations")

recommendations = []
for category, strategies in strategy_categories.items():
    selected_in_category = category_scores[category]
    total_in_category = len(strategies)

    if selected_in_category == 0:
        recommendation = "High priority: consider implementing at least one strategy from this category."
    elif selected_in_category < total_in_category / 2:
        recommendation = "Moderate priority: you selected some strategies, but could add more support."
    else:
        recommendation = "Strong area: you selected several strategies here."

    recommendations.append({
        "Intervention Category": category,
        "Strategies Selected": f"{selected_in_category}/{total_in_category}",
        "Recommendation": recommendation,
    })

recommendation_df = show_table(recommendations, "Personalized Intervention Recommendations")

st.divider()


# -----------------------------
# Section 8: Interpolation and curve fitting example
# -----------------------------
st.header("8. Simple modeling example")
st.write(
    "This section uses interpolation and curve fitting to estimate a simple trend. "
    "It is included to help satisfy the coding requirement involving interpolation, solving, or curve fitting."
)

sample_hours = np.array([0, 1, 2, 3, 4, 5, 6], dtype=float)
sample_risk_score = np.array([1, 1.2, 1.8, 2.7, 3.9, 5.2, 6.8], dtype=float)

interpolator = interp1d(sample_hours, sample_risk_score, kind="linear", fill_value="extrapolate")
estimated_risk_score = float(interpolator(recreational_screen_time))

fit_params, _ = curve_fit(linear_model, sample_hours, sample_risk_score)
modeled_x = np.linspace(0, 6, 100)
modeled_y = linear_model(modeled_x, *fit_params)

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(sample_hours, sample_risk_score, label="Sample data")
ax.plot(modeled_x, modeled_y, label="Curve fit trend")
ax.scatter([recreational_screen_time], [estimated_risk_score], label="Your estimate")
ax.set_xlabel("Recreational screen time, in hours")
ax.set_ylabel("Estimated risk score")
ax.set_title("Modeled Relationship Between Recreational Screen Time and Risk")
ax.legend()
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.caption(
    f"Based on the interpolation model, your estimated risk score is {estimated_risk_score:.2f}. "
    "This is a simplified demonstration model, not a medical diagnostic tool."
)

st.divider()


# -----------------------------
# Section 9: Final summary
# -----------------------------
st.header("9. Final summary")

strongest_category = max(category_scores, key=category_scores.get)
weakest_category = min(category_scores, key=category_scores.get)

summary_col1, summary_col2, summary_col3 = st.columns(3)
summary_col1.metric("Total daily screen time", f"{total_screen_time:.2f} hr")
summary_col2.metric("Recreational screen time", f"{recreational_screen_time:.2f} hr")
summary_col3.metric("Strategies of interest", sum(category_scores.values()))

st.write(f"**Strongest strategy category:** {strongest_category}")
st.write(f"**Needs the most improvement:** {weakest_category}")

st.success(
    "Main takeaway: the most effective approach is usually not one single strategy. "
    "A stronger plan combines movement during unavoidable screen time, more friction against recreational screen use, "
    "and easier access to physical activity or active alternatives."
)
