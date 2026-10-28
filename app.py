import streamlit as st
import pandas as pd
import os
from datetime import date

profile_file = "data/profile.csv"
habits_file = "data/habits.csv"

def ensure_data_folder():
    os.makedirs("data", exist_ok=True)  

goals = {
    "active_life": "🏃 Active Life",
    "healthy_growth": "🌱 Healthy Growth",
    "balance_life": "⚖️ Balance Life",
    "fitness": "💪 Fitness"
}

daily_targets = {
    "f_v": 5,
    "water": 8,
    "sleep_hours": 9,
    "exercise": 30
}

daily_target_labels = {
    "f_v": "🍎 Fruit and vegetables",
    "water": "💧 Water",
    "sleep_hours": "😴 Sleep",
    "exercise": "🏋️ Exercise"
}

def load_profiles() -> pd.DataFrame:
    ensure_data_folder()
    if os.path.exists(profile_file):
        return pd.read_csv(profile_file)



    return pd.DataFrame(columns=["name", "age", "activity_level", "goal"])

def save_profiles(name, age, activity_level, goal):
    df = load_profiles()

    df = df[df["name"] != name]  # Remove existing profile with the same name
    new_raw = pd.DataFrame([{"name": name, "age": age, "activity_level": activity_level, "goal": goal}])

    df = pd.concat([df, new_raw], ignore_index=True)
    df.to_csv(profile_file, index=False)

def load_habits():   
    ensure_data_folder()
    columns = ["name", "date", "f_v", "water", "sleep_hours", "exercise", "points"]
    if os.path.exists(habits_file):
        return pd.read_csv(habits_file)
    
    return pd.DataFrame(columns=columns)


def save_habits(entry: dict):
    df = load_habits()

    df = df[~((df['name' ] == entry['name' ]) & (df["date"] == entry["date"]))]

    df = pd. concat([df, pd. DataFrame([entry])] , ignore_index=True)

    df.to_csv(habits_file, index=False)


def calculate_points(f_v , water_cups, sleep_hours, exercise) -> int:
    points = 0
    points += min(f_v / daily_targets['f_v'], 1) * 25
    points += min(water_cups / daily_targets['water'], 1) * 25
    points += min(sleep_hours / daily_targets['sleep_hours'], 1) * 25
    points += min(exercise / daily_targets['exercise'], 1) * 25

    return round(points)

def get_badge(points: int) -> str :
    if points >= 90:
        return "🏆 بطل الصحه"
    elif points >= 70:
        return "⭐ نجم الصحه"
    elif points >= 50:
        return "📈 في تحسن مستمر"
    else:
        return "🌟 بدايه جميله استمر"

def generate_tips (goal, f_v, water_cups, sleep_hours, exercise) -> list:
    

    tips = []

    if f_v < daily_targets['f_v']:
        tips.append("🍎 حاول تزود حصص الفاكهه والخضار في اليوم")
    elif water_cups < daily_targets['water']:
        tips.append("💧 حاول تشرب مياه اكتر")
    elif sleep_hours < daily_targets['sleep_hours']:
        tips.append("😴 حاول تنام ساعات كافية")
    elif exercise < daily_targets['exercise']:
        tips.append("🏃 حاول ممارسة الرياضة")

    if goal == "active_life":
        tips.append("🥗 حافظ علي الاكل المتنوع والنوم الكويس")
    elif goal == "healthy_growth":
        tips.append("🌱 حافظ علي الاكل الصحي والنوم الكويس")
    elif goal == "balance_life":
        tips.append("⚖️ حافظ علي الاكل الصحي والنوم الكويس وممارسة الرياضة")
    elif goal == "fitness": 
        tips.append("💪 حافظ علي الاكل الصحي والنوم الكويس وممارسة الرياضة")

    if not tips:
        tips.append("🎉 حققت كل اهدافك النهارده")

    return tips 

st.set_page_config(
    page_title="تطبيق العادات الصحية",
    page_icon="❤️",
)

st.title("❤️ تطبيق العادات الصحية")

profiles = load_profiles()

st.sidebar.title("👤 New Profile")

existing_names = (profiles['name']. tolist() if not profiles.empty else [])

choice = st. sidebar.radio("👥 Choose profile", ["🆕 New user", "🔄 Old user"] if existing_names else ["🆕 New user"])

if choice == "🔄 Old user":
    name = st. sidebar. selectbox("👤 Choose your name", existing_names)

    profile_row = profiles[profiles["name"] == name].iloc[0]

    goal = profile_row["goal"]

    st.sidebar.success(f"👋 Welcome {name} again")
else:
    name = st.sidebar.text_input("✍️ Enter your name")
    age = st.sidebar.slider("🎂 Choose your age", min_value=10, max_value=80, value=20)
    activity_level = st.sidebar.selectbox("⚡ Choose your activity level", ["Low", "Medium", "High"])
    goal_labels = st.sidebar.selectbox("🎯 Choose your goal", list(goals.values()))
    goal = [k for k, v in goals.items() if v == goal_labels][0]
    if name and st.sidebar.button("💾 Save profile"):
        save_profiles(name, age, activity_level, goal)
        st.success("✅ Profile saved successfully!")
    if not name:
        st.info("ℹ️ Please enter your name to save the profile.")
        st.stop()

st.sidebar.markdown(" --- ")
st.sidebar.write(f"🎯 Your goal: {goals[goal]}")

today = date. today().isoformat()

with st.form("habits_form"):
    col1, col2 = st.columns(2)

    with col1:
        f_v = st.slider("🍎 Fruits & Veggies", 0, 10, 0)
        water_cups = st.slider("💧 Water Cups", 0, 15, 0)

    with col2:
        sleep_hours = st.slider("😴 Sleep Hours", 0, 12, 0)
        exercise = st.slider("🏋️ Exercise (minutes)", 0, 120, 0)

    submitted = st.form_submit_button("✅ Submit")

if submitted:
    points = calculate_points(f_v, water_cups, sleep_hours, exercise)
    badge = get_badge(points)

    save_habits({
        "name": name,           
        "date": today,
        "f_v": f_v,
        "water": water_cups,
        "sleep_hours": sleep_hours,
        "exercise": exercise,
        "points": points
    })

    st.success(f"✅ Data saved successfully! You earned {points} points today. {badge}")
    st.metric("🏆 Your Points", f"{points} points")
    st.subheader(badge)
    st.snow()

    st.markdown("---")

    tips = generate_tips(goal, f_v, water_cups, sleep_hours, exercise)
    for tip in tips:
        st.write(f"💡 {tip}")
    st.markdown("---")

st.header("📊 Your Progress")
habites=load_habits()
user_habits = habites[habites["name"] == name]

if user_habits.empty:
    st.info("📝 Please submit your daily data to see your progress.")
else:
    user_habits["date"] = pd.to_datetime(user_habits["date"])
    user_data = user_habits.sort_values("date")
    
    successful_days = (user_data['points' ] >= 70).sum()
    total_days = len(user_data)

    success_rate = round((successful_days / total_days) * 100)

    st.metric("📈 Success Rate", f"{success_rate}%")
    last_7_days = user_data.tail(7)

    
    st.write("🏆 Points")
st.bar_chart(last_7_days.set_index("date")[ ["points"]])

st.markdown(" --- ")
st.caption("Streamlit - CODEleader Academy مشروع تعليمي بسيط بلغة بايثون باستخدام Streamlit")