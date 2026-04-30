"""Streamlit app: Improving health through reducing sedentary screen time.

Run locally with:
    streamlit run myapp.py
"""
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from mpl_toolkits import mplot3d
import plotly.graph_objects as go


# -----------------------------
# Page setup: customization
# -----------------------------
st.set_page_config(page_icon="☯︎")
st.set_page_config(layout="centered")

# Font style

#<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#1f1f1f"><path d="M852-212 732-332l56-56 120 120-56 56ZM708-692l-56-56 120-120 56 56-120 120Zm-456 0L132-812l56-56 120 120-56 56ZM108-212l-56-56 120-120 56 56-120 120Zm246-75 126-76 126 77-33-144 111-96-146-13-58-136-58 135-146 13 111 97-33 143ZM233-120l65-281L80-590l288-25 112-265 112 265 288 25-218 189 65 281-247-149-247 149Zm247-361Z"/></svg>")

# --- Sidebar Inputs ---
st.sidebar.header("User Settings")
current_age = st.sidebar.number_input("Current Age", min_value=1, max_value=100, value=25)
life_expectancy = st.sidebar.number_input("Life Expectancy", min_value=1, max_value=120, value=80)


US_AVERAGE = 7 + 2 / 60        # 7 hours 2 minutes
WORLD_AVERAGE = 6 + 54 / 60    # 6 hours 54 minutes
NEGATIVE_THRESHOLD = 2         # 2 hours recreational screen time


# graph display functions

def show_bar_graph(labels, values, title, ylabel="Hours per day", colors=['#D18AA1','#7D98B5', '#FFE68F']):
    """display streamlit-compatible bar graph."""
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.bar(labels, values, color=colors)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def show_2nd_bar_graph(labels, values, title, ylabel="Hours per day", colors2=['#D18AA1','#FFC296', '#DCE0B8', '#BAAFC7']):
    """display streamlit-compatible bar graph."""
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(labels, values, color=colors2)
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
        st.info("No strategies were selected, so no chart can be displayed yet.")
        return

    fig, ax = plt.subplots(figsize=(5, 5))
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

def rainbow_spiral():
    """Display an interactive 3D spiral slide/ramp in Streamlit."""

    # Parameters for spiral slide
    theta = np.linspace(0, 6 * np.pi, 200)
    r = np.linspace(0.8, 2.2, 50)

    theta, r = np.meshgrid(theta, r)

    # Parametric surface equations
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = theta * 0.5

    # Create interactive surface
    fig = go.Figure(
        data=[
            go.Surface(
                x=x,
                y=y,
                z=z,
                surfacecolor=z,
                colorscale="HSV",
                showscale=True,
                colorbar=dict(title="Height")
            )
        ]
    )

    fig.update_layout(
        title="Click and Drag to Change Your Perspective",
        scene=dict(
            xaxis_title="X Axis",
            yaxis_title="Y Axis",
            zaxis_title="Height"
        ),
        width=800,
        height=700
    )

    st.plotly_chart(fig, use_container_width=True)
    
# Top of web page

st.title("Optimize Your Health and Happiness by Minimizing Your Superfluous Sedentary Screen Time")
st.write("a project by :rainbow[**Cristina Kinosian**]")
st.header("Background")
st.subheader('You are likely accumulating sedentary screen time while reading this sentence right now.')
st.markdown('In the last decade, sedentary screen time has increased exponentially, with research consistently concluding that screen-based sedentary activities increase the risk of poor physical and mental health. In fact, sedentary *screen* time specifically is more detrimental to health than any other sedentary non-screen activities, according to research by Keadle et. al. in 2025.')
st.subheader('So, how can we change our screen habits to improve longevity and quality of life?')
with st.expander(":rainbow[Click here]", expanded=False, key=None, icon=None, width="stretch", on_change="ignore", args=None, kwargs=None):
    st.write('''Author James Clear may have answers for you. In his best-selling 2018 book, Atomic Habits, Clear describes his well-researched techniques for successful habit formation and habit cessation. The central idea is to effectively decrease friction by making it easier to choose a good habit, and increase friction by making it harder to choose a bad habit. A combination of both will therefore yield the best results, thus we will explore various examples of specific strategies to accomplish this goal. After completing this interactive questionnaire, you will be armed with a customized plan for improving your health through specific sedentary screen time interventions that work for you and your circumstances. You will also be able to estimate your daily screen time, compare it with common averages, reflect on possible side effects, and choose personalized strategies for reducing sedentary screen use, backed by habit formation theory.''')

st.divider()

# user screen habits 

st.header("Your Average Daily Screen Time")
st.subheader("***If you have a smartphone, you can find your average daily screen time in your device settings.***")
st.subheader("Enter your best estimate of your average daily screen time, **in hours**, for each category.")

col1, col2, col3 = st.columns(3)

with col1:
    phone_screen_time = st.number_input(
        "Smartphone screen time",
        min_value=0.0,
        max_value=24.0,
        value=4.0,
        step=0.25,
        icon="📲"
    )

with col2:
    non_leisure_screen_time = st.number_input(
        "Work and/or school screen time",
        min_value=0.0,
        max_value=24.0,
        value=3.0,
        step=0.25,
        icon="🖥️"
    )

with col3:
    recreational_screen_time = st.number_input(
        "Other screen time, e.g., video games, television, tablet",
        min_value=0.0,
        max_value=24.0,
        value=2.0,
        step=0.25,
        icon="🎮"
    )

total_screen_time = phone_screen_time + non_leisure_screen_time + recreational_screen_time


show_2nd_bar_graph(
    ["Phone\nScreen Time", "Other Leisure\nScreen Time", "Unavoidable\nScreen Time", "Total\nScreen Time"],
    [phone_screen_time, recreational_screen_time, non_leisure_screen_time, total_screen_time],
    "Screen Time Source Distribution by Category",
)

st.warning(f":rainbow[YOUR TOTAL DAILY SCREEN TIME IS **{total_screen_time:.2f} HOURS**.]")

st.subheader("Your Average vs. Others")
show_bar_graph(
    ["Your Average", "U.S. Average", "Worldwide Average"],
    [phone_screen_time, US_AVERAGE, WORLD_AVERAGE],
    "Daily Smartphone Screen Time Comparison",
)
st.caption("Note: Information gathered from World Health Organization and Statista, as of 2024. Full works cited list available in the final section of this app.")

st.divider()

# Screen time threshold guess 

st.subheader("Use the slider to guess how many hours of recreational screen time we can have before we are at risk of negative side effects and longterm negative health outcomes")
st.write(
    "Screen time for recreation can feel relaxing and is okay in moderation, but excessive sedentary recreational screen time "
    "is consistently linked to negative health outcomes."
)

guess = st.slider(
    "Guess the maximum number of daily recreational sedentary screen time hours that is recommended to avoid negative health outcomes",
    min_value=0.0,
    max_value=18.0,
    value=3.0,
    step=0.5,
)

with st.expander(":rainbow[Click here to reveal answer!]", expanded=False, key=None, icon="❓", width="stretch", on_change="ignore", args=None, kwargs=None):
    if guess == NEGATIVE_THRESHOLD:
        st.success("Precisely! The threshold is about 2 hours per day, according to the World Health Organization and many studies.")
    elif guess < NEGATIVE_THRESHOLD:
        st.warning("Not quite — the threshold used in this project is a little higher: about 2 hours per day.")
    else:
        st.warning("It is actually less than that: only 2 hours per day.")

st.write(
    "If the excessive recreational screen-time threshold is regularly exceeded, being otherwise physically active "
    "may not fully offset the negative health effects of long sedentary periods (Keadle et al., 2025)"
)

st.divider()

# -----------------------------
# symptoms checklist 
#-----------------------------

st.header("Screen Use Side Effects")
st.write("Do you experience any of the following side effects, especially after high-screen-time days?")

symptoms = [
    "difficulty sleeping",
    "anxiety",
    "depression",
    "eye strain",
    "headaches",
    "neck, shoulder, or back pain",
    "difficulty focusing",
]

symptom_results = []
for symptom in symptoms:
    experienced = st.checkbox(f"{symptom}", key=f"symptom_{symptom}")
    symptom_results.append({
        "Symptom": symptom,
        "User Experiences This?": "Yes" if experienced else "No",
    })

number_of_symptoms = sum(row["User Experiences This?"] == "Yes" for row in symptom_results)
show_table(symptom_results, "Opportunities for Quality of Life Improvement if Screen Time is Reduced")

if number_of_symptoms == 0:
    st.info(
        "Wow, that's great! You may not be noticing obvious side effects right now. Excessive sedentary screen time has been associated with sleep problems, mental health challenges, eye strain, headaches, and body pain (Devi & Singh, 2023)."
    )
else:
    st.info(
        "You're not alone. Excessive sedentary screen time has been associated with sleep problems, mental health challenges, eye strain, headaches, and body pain (Devi & Singh, 2023)."
    )

st.divider()


# -----------------------------
# to continue or not to continue...that is the question
# -----------------------------
st.header("Continue?")

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
# current strategies 
# -----------------------------
st.header("Current screen-time reduction strategies")
st.write("Do you already use any of the following strategies?")

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
# add bridge here about habit formation principles and how they will be applied in the next section
st.header("How to choose effective strategies for you")
st.write(
    "The most effective strategies for reducing sedentary screen time are those that fit well with your lifestyle, preferences, and environment. "
    "In the next section, you will be able to choose from a variety of evidence-based strategies, organized into three categories based on habit formation principles: "
)

st.subheader(":rainbow[1. Incorporating movement during unavoidable screen time, such as work or school.]")
st.write("In some environments, such as work or school, screen use is often unavoidable. Therefore, to reduce sedentary screen behavior, the best interventions are those that allow for physical activity during screen use. Tools such as walking pads, pedal devices, stationary bikes, and standing desks allow individuals to remain engaged with screens while still being physically active. In a 2020 umbrella review spanning 17 different systematic reviews and meta-analyses, workplace interventions that allow for physical activity were shown to decrease sedentary time drastically, by 40–100 minutes per workday (Nguyen, et. al., 2020). Of all the strategies examined, such environmental changes were “shown to yield the most significant effect size” (Nguyen et. al., 2020). The most common environmental modification of this type seen in adult studies was the implementation of a tool aimed at decreasing sedentary time, and standing desks as a tool were associated with the most improvement. Additionally, interventions that targeted sedentary screen behavior specifically were more effective than interventions focused solely on increasing physical activity. (Nguyen, P. et. al., 2020). ")


st.subheader(":rainbow[2. Increasing friction against screen use during your free time, i.e., making it less convenient to use screens.]")
st.write("Interventions that make excessive screen use inconvenient are also proven to be highly effective. Examples of successful device-oriented strategies include digital lockouts, deleting or hiding apps, screen time limits, and reminder prompts on devices. These techniques introduce barriers that discourage prolonged use and have been shown to result in “consistent reductions in daily screen time across studies” [CK4.1](Buchanan, L.R. et. al., 2016). In Atomic Habits, James Clear states “before you try to increase your willpower, try to decrease the friction in your environment” (Clear, 2018). [CK5.1]Environmental modifications, such as increasing physical distance from devices, creating phone-free zones, or rearranging physical spaces, all function to encourage alternative activities[CK6.1]. Social environment also influences behavior, for example, family-based and socially supported interventions further enhance effectiveness by addressing broader environmental and social influences (Perrino et. al., 2022). Social, device-based, and environmental modifications all work synergistically to effectively reduce screen time.")


st.subheader(":rainbow[3. Decreasing friction to engage in physical activity, i.e., making it easier and more rewarding to choose active alternative activities.]")
st.write("Incorporating movement into screen time, rather than eliminating screen time altogether, is also effective in a recreational setting. Strategies like temptation bundling, environmental modifications, and choosing active video games improve health by replacing sedentary screen time with active screen time. Temptation bundling is the act of pairing an action you need to do with an action you want to do, such as only watching your favorite TV show while walking on a treadmill (Clear, 2018). Similarly, environmental modifications can look like introducing visual cues in typical sedentary screen time areas of the home; for example, placing a yoga mat in front of the TV to remind you to stretch while watching a show. Lastly, the strategic use of physically engaging screen-based games encourages movement. Examples of active video gaming include the use of Wii Fit, Dance Dance Revolution, Nintendo Switch fitness games, and Virtual Reality based games, all of which can be played from home. This strategy is particularly favorable, as recent research on virtual reality exercise demonstrates that immersive, movement-based screen experiences enhance enjoyment, perceived competence, and motivation to exercise, making them a promising tool for reducing sedentary behavior (Banerski et. Al., 2025).")


with st.expander("LEARN MORE ABOUT HABIT FORMATION PRINCIPLES", expanded=False, key=None, icon=None, width="stretch", on_change="ignore", args=None, kwargs=None):
    st.write(
        "The habit formation principles that guide the strategy categories are based on the idea of manipulating cues, cravings, responses, and rewards to make good habits more likely and bad habits less likely (Clear, 2018). "
        "For example, increasing friction against recreational screen use involves making it less convenient or attractive to engage in that behavior, while decreasing friction for physical activity involves making it easier and more rewarding to choose active alternatives."
        "For more information on the habit formation principles and how they apply to behavior change, check out James Clear's book *Atomic Habits* or his website at https://jamesclear.com/."
    )


st.divider()

# -----------------------------
# section 6: Strategy checklist
# -----------------------------

st.header("☆ Build Your Personalized Plan")

strategy_categories = {
    "Movement During Unavoidable Screen Time": [
        "working at a standing desk",
        "using a walking pad or treadmill while working",
        "using an under-desk pedal or elliptical",
        "scheduling frequent movement breaks during work",
        "finding a coworker to take daily walking breaks with",
    ],
    "Increasing Friction Against Recreational Screen Use": [
        "setting up automated app time limits/lockouts",
        "disabling non-essential notifications",
        "deleting or hiding distracting apps",
        "keeping devices in another room when unneeded",
        "establishing screen-free zones/hours at home",
    ],
    "Decreasing Friction for Physical Activity": [
        "placing workout equipment in visible areas",
        "only using screens as a reward during/after exercise",
        "using VR fitness or active video games",
        "scheduling non-screen activities on a regular basis",
        "wearing a smartwatch that prompts movement"
    ],
}

strategy_results = []
category_scores = {}
custom_strategies = []

for category, strategies in strategy_categories.items():
    st.subheader(category)
    used_count = 0

    for strategy in strategies:
        interested = st.checkbox(
            f"Interested in: {strategy}",
            key=f"interested_{category}_{strategy}",
        )

        if interested:
            used_count += 1

        strategy_results.append({
            "Category": category,
            "Strategy": strategy,
            "Interested?": "Yes" if interested else "No",
        })
        if interested:
            custom_strategies.append({
                "Category": category,
                "Strategy": strategy,
                "Interested?": "Yes",
            })

    category_scores[category] = used_count

strategy_df = show_table(custom_strategies, "Your Screen-Time Strategy Checklist")

show_donut_chart(
    list(category_scores.keys()),
    list(category_scores.values()),
    "Distribution of Screen-Time Strategies You're Interested In",
)

st.divider()


# -----------------------------
# Section 7: Personalized recommendations
# -----------------------------
st.header("Balancing Your Strategies")

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

recommendation_df = show_table(recommendations, "Recommendations for Optimization")

st.divider()


# -----------------------------
# Section 8: Interpolation and curve fitting example
# -----------------------------
st.header("Your Risk of Experiencing Side Effects")
st.write(
    "This section uses interpolation and curve fitting to estimate a simple trend: as sedentary screen time hours increase, so does the risk of experiencing negative symptoms. "
)

sample_hours = np.array([0, 1, 2, 3, 4, 5, 6], dtype=float)
sample_risk_score = np.array([1, 1.2, 1.8, 2.7, 3.9, 5.2, 6.8], dtype=float)

interpolator = interp1d(sample_hours, sample_risk_score, kind="linear", fill_value="extrapolate")
estimated_risk_score = float(interpolator(total_screen_time))

fit_params, _ = curve_fit(linear_model, sample_hours, sample_risk_score)
modeled_x = np.linspace(0, 6, 100)
modeled_y = linear_model(modeled_x, *fit_params)

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(sample_hours, sample_risk_score, label="Your screen risk data", color="orange")
ax.plot(modeled_x, modeled_y, label="Curve fit trend")
ax.scatter([recreational_screen_time], [estimated_risk_score], label="Your estimate")
ax.set_xlabel("Recreational screen time, in hours")
ax.set_ylabel("Estimated risk score")
ax.set_title("Your Risk of Experiencing Negative Symptoms due to Screen Time")
ax.legend()
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.caption(
    f"This simple interpolation model estimates your risk score to be {estimated_risk_score:.2f}. "
    "Note: This is a visualization tool, not a medical diagnostic."
)
# maybe an if statement based on their score, categorizing them as low, moderate, or high risk, with a corresponding message about how reducing recreational screen time could potentially improve their health outcomes.
if estimated_risk_score < 3:
    st.info("Your estimated risk score is low. Consider maintaining your current screen time habits.")
elif estimated_risk_score < 5:
    st.warning("Your estimated risk score is moderate. Reducing recreational screen time would improve your health outcomes.")
else:
    st.error("Your estimated risk score is high. Reducing recreational screen time is strongly recommended.")

st.divider()


st.title("⌛ How much time will you have lost looking at screens over the course of your life?")
st.write("Visualize how much of your life is spent on screens.")


# --- Calculations ---
# Hours per year = total_screen_time * 365.25
# Years wasted = (Hours per year * years_span) / (24 * 365.25)
# Simplified: Years wasted = (total_screen_time / 24) * years_span

future_ages = np.arange(current_age, life_expectancy + 1, 1)
years_passed = future_ages - current_age
years_wasted = (total_screen_time / 24) * years_passed

# Create DataFrame
df = pd.DataFrame({
    'Age': future_ages,
    'Years Wasted': years_wasted
})
df.set_index('Age', inplace=True)

# --- Visualization ---
st.subheader(f"Projection for {total_screen_time} hours/day")
st.line_chart(df)

# --- Metrics ---
total_wasted = years_wasted[-1]
st.metric(label="Total Years Wasted by Life Expectancy", value=f"{total_wasted:.2f} years",border=True)

st.subheader(f"At {total_screen_time} hours per day, you spend roughly "
        f"{((total_screen_time/24)*100):.1f}% of your time alive looking at screens.")


# -----------------------------
# Section 9: Final summary
# -----------------------------
st.header("Analysis and Summary of Your Results")

strongest_category = max(category_scores, key=category_scores.get)
weakest_category = min(category_scores, key=category_scores.get)

summary_col1, summary_col2, summary_col3 = st.columns(3)
summary_col1.metric("Total daily screen time", f"{total_screen_time:.2f} hr")
summary_col2.metric("Recreational screen time", f"{recreational_screen_time:.2f} hr")
summary_col3.metric("Strategies of interest", sum(category_scores.values()))

st.write(f"**Strongest strategy category:** {strongest_category}")
st.write(f"**Needs the most improvement:** {weakest_category}")

st.success(
    "Remember: the most effective approach is usually not one single strategy. "
    "A stronger plan is composite, incorporating strategies from all three categories: movement during unavoidable screen time, more friction against recreational screen use, "
    "and easier access to physical activity or active alternatives."
)

st.write("By tailoring multiple interventions to both the individual and their environment, it becomes more possible to create long-term reductions in sedentary screen time, thereby maximizing improvements in overall health and well-being. "
        )
st.subheader("However, any strategy can fall flat if implemented half-heartedly or mindlessly. The only viable path to success requires mindfulness of our behavioral intentions, goals, and awareness, thus intentional implementation of strategies is necessary to change deeply ingrained habits related to screen use. This understanding creates the best opportunity for success, creating an intrinsic motivation to combine behavioral, environmental, and technological approaches into a tailored, comprehensive solution. For example, Keadle et. al. found that intervention models combining multiple strategies such as education of health risks, earning screen time through exercise, automated app time limits, and text reminders of goals led to a tremendous decrease in screen use, exceeding reductions achieved by education-only approaches (Keadle et. al., 2025). These findings suggest that behavior change is most effectively achieved when interventions simultaneously target excessive screen use from behavioral, physical, and digital perspectives.")

st.title("What Progress Actually Looks Like")
rainbow_spiral()


with st.expander("VIEW MY ANNOTATED BIBLIOGRAPHY TO LEARN MORE", expanded=False, key=None, icon=None, width="stretch", on_change="ignore", args=None, kwargs=None):
    st.write('''
             Banerski, G., Abramczuk, K., Muczyński, B., & Cnotkowski, D. (2025). Transforming Sedentary Lifestyles: The impact of remote VR and flat-screen interventions on affective attitudes towards physical exertion, guided by avatar or human trainers. Psychology of Sport and Exercise, 76(102740). https://doi.org/10.1016/j.psychsport.2024.102740 
This study analyzed the replacement of flat-screen use with active digital physical activity via Virtual Reality. The authors investigate how virtual reality (VR) exercise compares to traditional flat-screen workouts in shaping attitudes toward physical exertion. Using a factorial design, 108 participants completed short home-based HIIT workouts through the use of either a flat-screen human-led exercise video, or a VR digital trainer-led exercise game. The study found that VR exercise significantly improved participants’ attitudes toward physical activity, while flat-screen workouts produced no meaningful change. The results suggest that immersive VR environments enhance enjoyment, perceived competence, and motivation to exercise, making them a promising tool for reducing sedentary behavior.
Buchanan, L.R., Rooks-Peck, C.R., Finnie, R.K.C., Wethington, H.R., Jacob, V., Janet, E.F., Johnson, D.B., Kahwati, L.C., Pratt, C.A., Ramirez, G., Mercer, S.L., & Glanz, K. (2016). Reducing Recreational Sedentary Screen Time: A Community Guide Systematic Review. American Journal of Preventive Medicine, 50(3), 402-415. https://doi.org/10.1016/j.amepre.2015.09.030
Buchanan et al. present a systematic review, evaluating 49 studies on interventions aimed at reducing recreational sedentary screen time, primarily among children and adolescents. The review found strong evidence that behavioral interventions such as self-monitoring, goal setting, and education effectively reduce screen time. Many other successful programs incorporated environmental and/or family-based components, such as limiting access to screens or modifying home environments. Overall, the review concludes that multi-component interventions targeting both behavior and environment are the most effective for reducing recreational sedentary screen use.
Clear, J. (2018). Atomic Habits: An easy & proven way to build good habits & break bad ones. Avery. 
James Clear presents a conceptual framework for behavior change based on the “habit loop” (cue, craving, response, reward), explaining how our habits are maintained through repeated reinforcement cycles. Atomic Habits describes the “Four Laws of Behavior Change:” making good behaviors obvious, attractive, easy, and satisfying, and reversing these principles for bad behaviors, making them less visible, unattractive, difficult, and inconvenient (Clear, 2018). The book emphasizes small, incremental changes, as well as smart environmental design (e.g., habit cue manipulation) as key mechanisms for behavioral modification. Clear also advocates for a systems-based approach, focusing on daily processes and identity shifts, instead of a goal-based approach. 
Friedrich, R.R., Polet, J.P., Schuch, I., & Wagner, M.B. (2014). Effect of intervention programs in schools to reduce screen time: a meta‐analysis. Jornal de Pediatria, 90(3) 232-241. https://doi.org/10.1016/j.jped.2014.01.003
This meta-analysis examined school-based interventions designed to reduce screen time among children and adolescents. Analyzing 16 studies, the authors found that educational interventions alone produced small but statistically significant reductions in daily screen use. Programs that incorporated educational components, behavioral strategies (such as goal setting), and parental involvement were found to be more effective than those using a single approach. Findings suggest that while school-based interventions can help reduce screen time, their impact is limited without broader environmental or multi-context support. 
Keadle, S., Hasanaj K., Leonard, K.S., Fernandez, A., Freid, L., Weiss, S., Legato, M., Anand, H., Hagobian, T.A., Phillips, S.M., Phelan, S., Guastaferro, K., Seltzer, R.G.N., & Buman, M.P.  (2025). StandUPTV: a full-factorial optimization trial to reduce sedentary screen time among adults. International Journal of Behavioral Nutrition and Physical Activity, 22(77). https://doi.org/10.1186/s12966-025-01771-2
This study used a randomized full-factorial trial within the Multiphase Optimization Strategy (MOST) framework over the course of 16 weeks to test combinations of mHealth intervention components aimed at reducing recreational sedentary screen time (rSST) in adults. All participants received the same baseline interventions: self-monitoring, education, and goal-setting (50% reduction). Additional strategies were systematically assigned to evaluate their individual and combined effects. Intervention strategies included restricting screen access once limits were reached, sending text messages with behavioral prompts and feedback, and providing the option to earn more screen time via physical activity. Screen time was measured using tools such as Fitbits, to track physical activity; Wifi-enabled smart plugs, to track TV time; and an app, to track smartphone use. Results indicated the most effective strategy was providing the option to earn more screen time via physical activity. A similar level of effectiveness was found through the combination of all interventions. 
Keadle, S., Hasanaj K., Leonard, K.S., Tolas, A., Crosley-Lyons, R., Pfisterer, B., Legato, M., Fernandez, A., Lowell, E., Hollingshead, K., Yu, T., Phelan, S., Phillips, S.M., Watson, N., Hagobian, T., Guastaferro, K., & Buman, M.P. (2023). StandUPTV: Preparation and Optimization phases of a mHealth intervention to reduce sedentary screen time in adults. Contemporary Clinical Trials, 136(107402), https://doi.org/10.1016/j.cct.2023.107402
The study outlines the preparation phase (including user-centered design and component selection) and the protocol for a randomized optimization trial using a factorial design to monitor outcomes of 240 participants. The three strategies for sedentary screen time reduction include: digital lock out (e.g., automatic screen limits on devices), text prompts (pop-up reminders on devices), and earning screen time minutes through physical activity. Participants are assigned different combinations of these components with the goal of reducing screen time by 50%, allowing researchers to determine the most effective intervention combination.
Nguyen, P., Khanh-Dao, L.L., Nguyen, D., Gao, L., Dunstan, D. W., & Moodie, M. (2020). The effectiveness of sedentary behaviour interventions on sitting time and screen time in children and adults: an umbrella review of systematic reviews, International Journal of Behavioral Nutrition and Physical Activity, 17(117), 1-11. https://doi.org/10.1186/s12966-020-01009-3 
This umbrella review analyzed results from 17 different systematic reviews and meta-analyses, with a total of 219 trials, all focusing on interventions to reduce sedentary behavior across children and adults. The umbrella review concluded that interventions were most effective for adults in workplace settings, as sitting time decreased by between 40–100 minutes per workday, with standing desk implementation producing the best results. Reductions in children’s screen time were found to be minimal, but still statistically significant. Interventions that targeted sedentary behavior directly were more effective than interventions focused solely on physical activity. However, long-term effects of behavior change resulting from interventions remain unclear. 
             
Perrino, T., Brincks, A. M., Estrada, Y., Messiah, S. E., & Prado, G. (2022). Reducing Screen-Based Sedentary Behavior Among Overweight and Obese Hispanic Adolescents Through a Family-Based Intervention. Journal of Physical Activity & Health, 19(7), 509–517. https://doi-org.libprox1.slcc.edu/10.1123/jpah.2022-0050 
This study examined the effectiveness of family-based interventions in reducing screen-based sedentary behavior among overweight and obese Hispanic adolescents. Using a randomized controlled design with 280 participants, the study tracked participant outcomes over 24 months. Strategies included the combination of educational group discussions for parents, group physical activity sessions for youth, and individualized family sessions led by facilitators to create environmental changes in the home. Results showed that the intervention significantly reduced adolescents’ sedentary screen time but was ineffective in reducing parents’ sedentary screen time. Overall, the study demonstrates that family-centered, culturally tailored interventions can effectively reduce adolescent screen time, but the education intervention strategy alone was found to be ineffective. 
              

             )'''
             )
with st.expander("Additional References & Data Sources Listed Here", expanded=False, key=None, icon=None, width="stretch", on_change="ignore", args=None, kwargs=None):
    st.write('''
        Devi, Khumukcham A.; Singh, Sudhakar K.1. The hazards of excessive screen time: Impacts on physical health, mental health, and overall well-being. Journal of Education and Health Promotion 12(1):413, November 2023. | DOI: 10.4103/jehp.jehp_447_23 
        ''')
    

# st.metric(label="Temp", value="273 K", delta="1.2 K")
 
