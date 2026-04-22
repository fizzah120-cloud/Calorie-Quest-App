import streamlit as st
from datetime import date

# -----------------------------
# App Setup
# -----------------------------
st.set_page_config(page_title="Calorie Quest", page_icon="🍎", layout="centered")

# -----------------------------
# Session State Init
# -----------------------------
if "xp" not in st.session_state:
    st.session_state.xp = 0

if "level" not in st.session_state:
    st.session_state.level = 1

if "log" not in st.session_state:
    st.session_state.log = []

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "today" not in st.session_state:
    st.session_state.today = str(date.today())

if "daily_limit" not in st.session_state:
    st.session_state.daily_limit = 2000

if "calories_consumed" not in st.session_state:
    st.session_state.calories_consumed = 0

# -----------------------------
# Level System
# -----------------------------
def update_level():
    st.session_state.level = (st.session_state.xp // 100) + 1

# -----------------------------
# Title
# -----------------------------
st.title("🍎 Calorie Quest")
st.write("Turn your diet into a game. Earn XP, level up, and complete quests!")

# -----------------------------
# Sidebar Stats
# -----------------------------
st.sidebar.header("⚔️ Your Hero Stats")
st.sidebar.write(f"⭐ Level: {st.session_state.level}")
st.sidebar.write(f"✨ XP: {st.session_state.xp}")
st.sidebar.write(f"🔥 Streak: {st.session_state.streak} days")
st.sidebar.write(f"🍽️ Calories Today: {st.session_state.calories_consumed}/{st.session_state.daily_limit}")

# -----------------------------
# Daily Quest System
# -----------------------------
st.subheader("🎯 Daily Quest")

quest_done = st.checkbox("Stay under your calorie limit today")

if quest_done:
    st.success("Quest Completed! +50 XP 🎉")
    if "quest_rewarded" not in st.session_state:
        st.session_state.xp += 50
        st.session_state.quest_rewarded = True
        update_level()

# -----------------------------
# Food Logging
# -----------------------------
st.subheader("🍔 Log Your Food")

food = st.text_input("Food item")
calories = st.number_input("Calories", min_value=0, step=50)

if st.button("Add Food"):
    if food:
        st.session_state.log.append((food, calories))
        st.session_state.calories_consumed += calories

        # XP system
        gained_xp = max(5, calories // 50)
        st.session_state.xp += gained_xp

        update_level()

        st.success(f"Added {food} (+{calories} cal) | +{gained_xp} XP earned!")

# -----------------------------
# Food Log Display
# -----------------------------
st.subheader("📜 Food Log")

if st.session_state.log:
    for item, cal in st.session_state.log[::-1]:
        st.write(f"🍽️ {item} — {cal} kcal")
else:
    st.info("No food logged yet. Start your quest!")

# -----------------------------
# Level Rewards
# -----------------------------
st.subheader("🏆 Level Rewards")

if st.session_state.level >= 5:
    st.success("Unlocked: Iron Discipline Badge 🛡️")
elif st.session_state.level >= 3:
    st.info("Unlocked: Consistency Badge 🔥")
else:
    st.warning("Keep going to unlock rewards!")

# -----------------------------
# Reset Button
# -----------------------------
st.divider()

if st.button("🔄 Reset Game"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
