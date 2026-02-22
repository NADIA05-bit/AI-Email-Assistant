# mission_control.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Mission Control", layout="wide")

# CUSTOM CSS
st.markdown("""
    <style>
        /* Change background color */
        .main {
            background-color: #f5f7fa;
        }

        /* Style the metric cards */
        div[data-testid="metric-container"] {
            background-color: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        /* Title styling */
        h1 {
            color: #1a3e72;
            font-weight: 700;
        }

        /* Subheader styling */
        h3 {
            color: #2c4a7a;
            margin-top: 40px;
        }

        /* Table styling */
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)


# 1. TITLE PAGE
st.title("♛ Mission Control – Team Manager Dashboard")
st.caption("AI Email Assistance")

# 2. SAMPLE DATA
owners = ["Zainab", "Zunaira", "Ruksana", "Nadia"]
statuses = ["Blocked", "In Progress", "At Risk", "On Track"]
sentiments = ["‼️Very Negative", "❗️Negative", "🔷Neutral", "🟩Positive", "✅Very Positive"]

def generate_sample_tasks(n=10):
    tasks = []
    for i in range(n):
        tasks.append({
            "Task": f"Task #{i+1}",
            "Owner": random.choice(owners),
            "Status": random.choice(statuses),
            "Deadline": datetime.today().date() + timedelta(days=random.randint(-2, 7)),
            "Sentiment": random.choice(sentiments)
        })
    return pd.DataFrame(tasks)

tasks_df = generate_sample_tasks(12)


# 3. METRICS / SUMMARY

today = datetime.today().date()

urgent_issues = tasks_df[
    (tasks_df["Status"].isin(["Blocked", "At Risk"])) |
    (tasks_df["Deadline"] < today)
]

upcoming_deadlines = tasks_df[
    (tasks_df["Deadline"] >= today) &
    (tasks_df["Deadline"] <= today + timedelta(days=3))
]

sentiment_score_map = {
    "Very Negative": -2,
    "Negative": -1,
    "Neutral": 0,
    "Positive": 1,
    "Very Positive": 2
}
tasks_df["SentimentScore"] = tasks_df["Sentiment"].map(sentiment_score_map)
avg_sentiment = tasks_df["SentimentScore"].mean()

if avg_sentiment <= -1:
    sentiment_label = "Negative"
elif avg_sentiment < 1:
    sentiment_label = "Neutral"
else:
    sentiment_label = "Positive"

# 4. TOP SUMMARY CARDS

st.subheader("📡 Mission Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Urgent Issues", len(urgent_issues))
col2.metric("Upcoming Deadlines (3 days)", len(upcoming_deadlines))
col3.metric("Team Sentiment", sentiment_label)

# 5. AI ASSISTANCE

st.subheader("🔍 Insights for You")

insights = []

if len(urgent_issues) > 0:
    insights.append(f"There are {len(urgent_issues)} tasks that are either blocked, at risk, or overdue.")

if len(upcoming_deadlines) > 0:
    owner_counts = upcoming_deadlines["Owner"].value_counts()
    overloaded_owner = owner_counts.idxmax()
    overloaded_count = owner_counts.max()
    insights.append(
        f"{overloaded_owner} has {overloaded_count} tasks due in the next 3 days. Consider rebalancing workload."
    )

if sentiment_label == "Negative":
    insights.append("Team sentiment is trending negative. You may want to check in with the team.")
elif sentiment_label == "Neutral":
    insights.append("Team sentiment is neutral. There might be hidden friction—review blocked or at-risk tasks.")
else:
    insights.append("Team sentiment looks positive. Keep an eye on upcoming deadlines to maintain momentum.")

if not insights:
    insights.append("No major issues detected. This is a good time for strategic planning.")

for i, text in enumerate(insights, start=1):
    st.info(f"Insight {i}: {text}")

# 6. TASK OVERVIEW WITH FILTERS

st.subheader("📅 Tasks Overview")

with st.expander("Filters", expanded=True):
    selected_owner = st.selectbox("Filter by owner", ["All"] + owners)
    selected_status = st.multiselect("Filter by status", statuses, default=statuses)

filtered = tasks_df.copy()

if selected_owner != "All":
    filtered = filtered[filtered["Owner"] == selected_owner]

if selected_status:
    filtered = filtered[filtered["Status"].isin(selected_status)]

st.dataframe(
    filtered[["Task", "Owner", "Status", "Deadline", "Sentiment"]],
    use_container_width=True
)

# 7. RISK / STATUS SUMMARY

st.subheader("⚠️ Status Breakdown")

status_counts = tasks_df["Status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]

col_chart, col_table = st.columns(2)

# 8. SIDE BAR
with col_chart:
    st.bar_chart(
        status_counts.set_index("Status"),
        use_container_width=True
    )

with col_table:
    st.table(status_counts)

with st.sidebar:
    st.title("⚙️ Controls")
    st.write("Adjust your dashboard view")

    selected_owner = st.selectbox("Filter by owner", ["All"] + owners)
    selected_status = st.multiselect("Filter by status", statuses, default=statuses)

    st.markdown("---")
    st.write("Theme")
    theme_choice = st.radio("Choose theme", ["Light", "Dark"])

def color_status(val):
    colors = {
        "Blocked": "background-color: #eb1818;",
        "At Risk": "background-color: #ffcf6d;",
        "In Progress": "background-color: #6db9ff;",
        "On Track": "background-color: #16c44c;"
    }
    return colors.get(val, "")

st.dataframe(
    filtered.style.applymap(color_status, subset=["Status"]),
    use_container_width=True
)

st.progress(70)
