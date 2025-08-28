import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# --- App Title ---
st.title("🏋️ Personal Training & Nutrition Log")

# --- Session State for Data ---
if "workouts" not in st.session_state:
    st.session_state.workouts = []
if "nutrition" not in st.session_state:
    st.session_state.nutrition = []
if "metrics" not in st.session_state:
    st.session_state.metrics = []

# --- Sidebar Navigation ---
page = st.sidebar.radio("Navigate", ["Log Workout", "Log Nutrition", "Log Body Metrics", "Dashboard", "Export Data"])

# --- Workout Logging ---
if page == "Log Workout":
    st.header("Log Workout")
    date = st.date_input("Date")
    exercise = st.text_input("Exercise Name")
    sets = st.number_input("Sets", min_value=1, value=3)
    reps = st.number_input("Reps", min_value=1, value=10)
    weight = st.number_input("Weight (kg)", min_value=0.0, value=0.0)
    run_distance = st.number_input("Run Distance (km)", min_value=0.0, value=0.0)
    run_time = st.number_input("Run Time (minutes)", min_value=0.0, value=0.0)

    if st.button("Save Workout"):
        st.session_state.workouts.append({
            "date": date,
            "exercise": exercise,
            "sets": sets,
            "reps": reps,
            "weight": weight,
            "run_distance": run_distance,
            "run_time": run_time
        })
        st.success("Workout logged!")

    if st.session_state.workouts:
        st.subheader("Workout History")
        df = pd.DataFrame(st.session_state.workouts)
        st.dataframe(df)

# --- Nutrition Logging ---
elif page == "Log Nutrition":
    st.header("Log Nutrition")
    date = st.date_input("Date", key="nutrition_date")
    calories = st.number_input("Calories", min_value=0, value=2000)
    protein = st.number_input("Protein (g)", min_value=0, value=100)
    carbs = st.number_input("Carbs (g)", min_value=0, value=200)
    fats = st.number_input("Fats (g)", min_value=0, value=70)
    water = st.number_input("Water Intake (L)", min_value=0.0, value=2.0)

    if st.button("Save Nutrition"):
        st.session_state.nutrition.append({
            "date": date,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fats": fats,
            "water": water
        })
        st.success("Nutrition logged!")

    if st.session_state.nutrition:
        st.subheader("Nutrition History")
        df = pd.DataFrame(st.session_state.nutrition)
        st.dataframe(df)

# --- Body Metrics Logging ---
elif page == "Log Body Metrics":
    st.header("Log Body Metrics")
    date = st.date_input("Date", key="metrics_date")
    weight = st.number_input("Weight (kg)", min_value=0.0, value=70.0)
    body_fat = st.number_input("Body Fat (%)", min_value=0.0, value=15.0)
    waist = st.number_input("Waist (cm)", min_value=0.0, value=80.0)

    if st.button("Save Metrics"):
        st.session_state.metrics.append({
            "date": date,
            "weight": weight,
            "body_fat": body_fat,
            "waist": waist
        })
        st.success("Metrics logged!")

    if st.session_state.metrics:
        st.subheader("Metrics History")
        df = pd.DataFrame(st.session_state.metrics)
        st.dataframe(df)

# --- Dashboard ---
elif page == "Dashboard":
    st.header("📊 Dashboard & Trends")
    if st.session_state.metrics:
        df = pd.DataFrame(st.session_state.metrics)
        df["lean_mass"] = df["weight"] * (1 - df["body_fat"]/100)
        fig, ax = plt.subplots()
        ax.plot(df["date"], df["weight"], label="Weight (kg)")
        ax.plot(df["date"], df["lean_mass"], label="Lean Mass (kg)")
        ax.set_ylabel("Kg")
        ax.legend()
        st.pyplot(fig)
        st.subheader("Latest Metrics")
        st.write(df.tail(1))
    else:
        st.info("Log some metrics to see trends here.")

# --- Export Data ---
elif page == "Export Data":
    st.header("💾 Export All Data to CSV")

    def convert_df(data):
        return pd.DataFrame(data).to_csv(index=False).encode('utf-8')

    if st.session_state.workouts:
        st.download_button("Download Workouts CSV", convert_df(st.session_state.workouts), "workouts.csv")
    if st.session_state.nutrition:
        st.download_button("Download Nutrition CSV", convert_df(st.session_state.nutrition), "nutrition.csv")
    if st.session_state.metrics:
        st.download_button("Download Metrics CSV", convert_df(st.session_state.metrics), "metrics.csv")

    if not (st.session_state.workouts or st.session_state.nutrition or st.session_state.metrics):
        st.info("No data to export yet.")
