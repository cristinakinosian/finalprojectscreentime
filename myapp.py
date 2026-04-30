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

# -----------------------------
# Page setup: customization
# -----------------------------
st.set_page_config(page_icon="☯︎")
st.set_page_config(layout="centered")

# Font style

#<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#1f1f1f"><path d="M852-212 732-332l56-56 120 120-56 56ZM708-692l-56-56 120-120 56 56-120 120Zm-456 0L132-812l56-56 120 120-56 56ZM108-212l-56-56 120-120 56 56-120 120Zm246-75 126-76 126 77-33-144 111-96-146-13-58-136-58 135-146 13 111 97-33 143ZM233-120l65-281L80-590l288-25 112-265 112 265 288 25-218 189 65 281-247-149-247 149Zm247-361Z"/></svg>")


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


# Top of web page

st.title("Optimize Your Health and Happiness by Minimizing Sedentary Screen Time")
st.write("a project by :rainbow[**Cristina Kinosian**]")
st.header("Background")
st.subheader('You are likely accumulating sedentary screen time while reading this sentence right now.')
st.markdown('In the last decade, sedentary screen time has increased exponentially, with research consistently concluding that screen-based sedentary activities increase the risk of poor physical and mental health. In fact, sedentary *screen* time specifically is more detrimental to health than any other sedentary non-screen activities, according to research by Keadle et. al. in 2025.')
st.subheader('So, how can we change our screen habits to improve longevity and quality of life?')
with st.expander(":rainbow[Click here]", expanded=False, key=None, icon=None, width="stretch", on_change="ignore", args=None, kwargs=None):
    st.write('''Author James Clear may have answers for you. In his best-selling 2018 book, Atomic Habits, Clear describes his well-researched techniques for successful habit formation and habit cessation. The central idea is to effectively decrease friction by making it easier to choose a good habit, and increase friction by making it harder to choose a bad habit. A combination of both will therefore yield the best results, thus we will explore various examples of specific strategies to accomplish this goal. After completing this interactive questionnaire, you will be armed with a customized plan for improving your health through specific sedentary screen time interventions that work for you and your circumstances. You will also be able to estimate your daily screen time, compare it with common averages, reflect on possible side effects, and choose personalized strategies for reducing sedentary screen use, backed by habit formation theory.''')

st.divider()

# user screen habits 

st.header("What are your current screen habits?")
st.write("***If you have a smartphone, you can find your average daily screen time in your device settings.***")

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
        "Unavoidable work and/or school screen time approximation, in hours",
        min_value=0.0,
        max_value=24.0,
        value=3.0,
        step=0.25,
    )

with col3:
    recreational_screen_time = st.number_input(
        "Other daily recreational screen time approximation, **not including smartphone**, in hours",
        min_value=0.0,
        max_value=24.0,
        value=2.0,
        step=0.25,
    )

total_screen_time = phone_screen_time + non_leisure_screen_time + recreational_screen_time

st.subheader("Your Average vs. Others")
show_bar_graph(
    ["Your Average", "U.S. Average", "Worldwide Average"],
    [phone_screen_time, US_AVERAGE, WORLD_AVERAGE],
    "Daily Smartphone Screen Time Comparison",
)

st.warning(f":rainbow[Your estimated total daily screen time is **{total_screen_time:.2f} hours**.]")
st.caption("Note: Information gathered from World Health Organization and Statista, as of 2024. Full works cited list available in the final section of this app.")

show_2nd_bar_graph(
    ["Phone\nScreen Time", "Other Leisure\nScreen Time", "Unavoidable\nScreen Time", "Total\nScreen Time"],
    [phone_screen_time, recreational_screen_time, non_leisure_screen_time, total_screen_time],
    "Screen Time Source Distribution by Category",
)

st.divider()

# Screen time threshold guess 

st.header("2. Recreational screen-time threshold")
st.write(
    "Screen time for recreation can feel relaxing, but excessive sedentary recreational screen time "
    "is consistently linked to negative health outcomes."
)

guess = st.slider(
    "Use the slider to guess how many hours of recreational screen time per day is the threshold for negative health outcomes",
    min_value=0.0,
    max_value=18.0,
    value=3.0,
    step=0.5,
)

with st.expander(":rainbow[Click here to reveal answer!]", expanded=False, key=None, icon=None, width="stretch", on_change="ignore", args=None, kwargs=None):
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
show_table(symptom_results, "Opportunities for QOL Improvement: Your Symptom List")

if number_of_symptoms == 0:
    st.success("Wow, that's great! You may not be noticing obvious side effects right now.")
else:
    st.info(
        "You're not alone. Excessive sedentary screen time has been associated with sleep problems, "
        "mental health challenges, eye strain, headaches, and body pain."
    )

st.divider()


# -----------------------------
# to continue or not to continue...that is the question
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
# current strategies 
# -----------------------------
st.header("5. Current screen-time reduction strategies")
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
    "1) Movement during unavoidable screen time, such as work or school,"
    "2) Increasing friction against recreational screen use, i.e., making it less convenient to use screens," 
    "3) Decreasing friction for physical activity, i.e., making it easier and more rewarding to choose active alternatives."
)
with st.expander("LEARN MORE ABOUT HABIT FORMATION PRINCIPLES", expanded=False, key=None, icon=None, width="stretch", on_change="ignore", args=None, kwargs=None):
    st.write(
        "The habit formation principles that guide the strategy categories are based on the idea of manipulating cues, cravings, responses, and rewards to make good habits more likely and bad habits less likely (Clear, 2018). "
        "For example, increasing friction against recreational screen use involves making it less convenient or attractive to engage in that behavior, while decreasing friction for physical activity involves making it easier and more rewarding to choose active alternatives."
        "For more information on the habit formation principles and how they apply to behavior change, check out James Clear's book *Atomic Habits* or his website at https://jamesclear.com/."
    )

# -----------------------------
# section 6: Strategy checklist
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
with st.expander("CLICK HERE TO VIEW MY ANNOTATED BIBLIOGRAPHY AND LEARN MORE", expanded=False, key=None, icon=None, width="stretch", on_change="ignore", args=None, kwargs=None):
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
    
