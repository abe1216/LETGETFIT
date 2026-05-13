import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fitness Planner GUI", layout="wide")

# -----------------------------
# Functions
# -----------------------------

def calculate_bmr(weight_lbs, height_in, age, sex):
    weight_kg = weight_lbs * 0.453592
    height_cm = height_in * 2.54

    if sex == "Male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161


def calculate_calories(bmr, activity, goal):
    activity_factors = {
        "Low": 1.2,
        "Moderate": 1.55,
        "High": 1.725
    }

    calories = bmr * activity_factors[activity]

    if goal == "Bulk":
        calories += 300
    elif goal == "Cut":
        calories -= 400

    return calories


def calculate_macros(calories, weight_lbs, goal):
    protein = weight_lbs

    if goal == "Bulk":
        fat_percent = 0.25
    elif goal == "Cut":
        fat_percent = 0.20
    else:
        fat_percent = 0.25

    fat = (calories * fat_percent) / 9
    carbs = (calories - protein * 4 - fat * 9) / 4

    return protein, carbs, fat


def make_workout(days, off_days, goal):
    workouts = []

    if days == 3:
        split = [
            "Full Body A",
            "Full Body B",
            "Full Body C"
        ]
    elif days == 4:
        split = [
            "Upper Body",
            "Lower Body",
            "Upper Body",
            "Lower Body"
        ]
    elif days == 5:
        split = [
            "Push",
            "Pull",
            "Legs",
            "Upper Body",
            "Lower Body"
        ]
    else:
        split = [
            "Push",
            "Pull",
            "Legs",
            "Push",
            "Pull",
            "Legs"
        ]

    exercises = {
        "Push": [
            "Bench Press - 3x8",
            "Shoulder Press - 3x10",
            "Incline Dumbbell Press - 3x10",
            "Triceps Pushdown - 3x12",
            "Lateral Raises - 3x15"
        ],
        "Pull": [
            "Lat Pulldown - 3x10",
            "Seated Cable Row - 3x10",
            "Dumbbell Row - 3x10",
            "Face Pulls - 3x15",
            "Bicep Curls - 3x12"
        ],
        "Legs": [
            "Squat or Leg Press - 3x8",
            "Romanian Deadlift - 3x10",
            "Leg Extension - 3x12",
            "Leg Curl - 3x12",
            "Calf Raises - 3x15"
        ],
        "Upper Body": [
            "Bench Press - 3x8",
            "Lat Pulldown - 3x10",
            "Shoulder Press - 3x10",
            "Cable Row - 3x10",
            "Curls + Triceps - 3x12"
        ],
        "Lower Body": [
            "Squat or Leg Press - 3x8",
            "Romanian Deadlift - 3x10",
            "Lunges - 3x10",
            "Leg Curl - 3x12",
            "Core - 3 sets"
        ],
        "Full Body A": [
            "Squat - 3x8",
            "Bench Press - 3x8",
            "Lat Pulldown - 3x10",
            "Shoulder Press - 2x10",
            "Core - 3 sets"
        ],
        "Full Body B": [
            "Deadlift - 3x5",
            "Incline Press - 3x10",
            "Cable Row - 3x10",
            "Leg Curl - 3x12",
            "Biceps + Triceps - 3x12"
        ],
        "Full Body C": [
            "Leg Press - 3x10",
            "Dumbbell Press - 3x10",
            "Pull-ups or Pulldown - 3x10",
            "Lateral Raises - 3x15",
            "Core - 3 sets"
        ]
    }

    workout_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    available_days = [day for day in workout_days if day not in off_days]

    for i in range(days):
        day = available_days[i % len(available_days)]
        workout_type = split[i]
        workouts.append({
            "Day": day,
            "Workout": workout_type,
            "Exercises": "\n".join(exercises[workout_type]),
            "Time Limit": "About 60 minutes"
        })

    return pd.DataFrame(workouts)


def grocery_list(goal, budget):
    if goal == "Bulk":
        groceries = [
            ["Chicken breast", 12],
            ["Ground beef or turkey", 15],
            ["Eggs", 6],
            ["Greek yogurt", 6],
            ["Rice", 8],
            ["Potatoes", 6],
            ["Oats", 5],
            ["Bananas", 4],
            ["Frozen vegetables", 8],
            ["Peanut butter", 5],
            ["Milk", 5],
            ["Tortillas", 4]
        ]
    elif goal == "Cut":
        groceries = [
            ["Chicken breast", 14],
            ["Lean ground turkey", 15],
            ["Eggs", 6],
            ["Greek yogurt", 6],
            ["Rice", 6],
            ["Sweet potatoes", 6],
            ["Frozen vegetables", 10],
            ["Salad mix", 5],
            ["Fruit", 6],
            ["Cottage cheese", 5],
            ["Tuna cans", 6]
        ]
    else:
        groceries = [
            ["Chicken breast", 12],
            ["Ground turkey", 12],
            ["Eggs", 6],
            ["Greek yogurt", 6],
            ["Rice", 7],
            ["Potatoes", 6],
            ["Frozen vegetables", 8],
            ["Fruit", 6],
            ["Oats", 5],
            ["Milk", 5],
            ["Tortillas", 4]
        ]

    df = pd.DataFrame(groceries, columns=["Item", "Estimated Cost ($)"])
    total = df["Estimated Cost ($)"].sum()

    if total > budget:
        df = df.sort_values("Estimated Cost ($)", ascending=False)
        while df["Estimated Cost ($)"].sum() > budget and len(df) > 1:
            df = df.iloc[1:]

    return df


# -----------------------------
# App Title
# -----------------------------

st.title("Fitness, Nutrition, and Workout Planner")
st.write("This app calculates calories, macros, workouts, meals, and a grocery list using a Streamlit GUI.")

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("User Inputs")

weight = st.sidebar.number_input("Weight (lbs)", min_value=80, max_value=400, value=195)
height = st.sidebar.number_input("Height (inches)", min_value=48, max_value=84, value=68)
age = st.sidebar.number_input("Age", min_value=12, max_value=100, value=20)
sex = st.sidebar.selectbox("Sex", ["Male", "Female"])

goal = st.sidebar.selectbox("Goal", ["Bulk", "Cut", "Maintain"])
activity = st.sidebar.selectbox("Activity Level", ["Low", "Moderate", "High"])

days = st.sidebar.slider("How many days do you want to work out?", 3, 6, 5)

off_days = st.sidebar.multiselect(
    "Choose your off days",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    default=["Sunday"]
)

budget = st.sidebar.slider("Grocery Budget ($)", 50, 150, 100)

# -----------------------------
# Calculations
# -----------------------------

bmr = calculate_bmr(weight, height, age, sex)
calories = calculate_calories(bmr, activity, goal)
protein, carbs, fat = calculate_macros(calories, weight, goal)

# -----------------------------
# Tabs
# -----------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Calories",
    "Macros",
    "Workout Maker",
    "Meals & Grocery List",
    "Project Explanation"
])

# -----------------------------
# Tab 1: Calories
# -----------------------------

with tab1:
    st.header("Calorie Calculator")

    col1, col2 = st.columns(2)

    col1.metric("BMR", f"{bmr:.0f} calories")
    col2.metric("Daily Calorie Goal", f"{calories:.0f} calories")

    st.write("Your calories are adjusted based on your activity level and goal.")

    if goal == "Bulk":
        st.success("Bulking mode: Calories increased by 300.")
    elif goal == "Cut":
        st.info("Cutting mode: Calories decreased by 400.")
    else:
        st.warning("Maintenance mode: Calories stay near maintenance level.")

# -----------------------------
# Tab 2: Macros
# -----------------------------

with tab2:
    st.header("Macro Calculator")

    col1, col2, col3 = st.columns(3)

    col1.metric("Protein", f"{protein:.0f} g")
    col2.metric("Carbs", f"{carbs:.0f} g")
    col3.metric("Fat", f"{fat:.0f} g")

    macro_df = pd.DataFrame({
        "Macro": ["Protein", "Carbs", "Fat"],
        "Grams": [protein, carbs, fat],
        "Calories": [protein * 4, carbs * 4, fat * 9]
    })

    st.dataframe(macro_df)

    fig, ax = plt.subplots()
    ax.pie(
        macro_df["Calories"],
        labels=macro_df["Macro"],
        autopct="%1.1f%%"
    )
    ax.set_title("Macro Calorie Breakdown")
    st.pyplot(fig)

# -----------------------------
# Tab 3: Workout Maker
# -----------------------------

with tab3:
    st.header("Commercial Gym Workout Maker")

    if len(off_days) > 7 - days:
        st.error("You selected too many off days for the number of workout days.")
    else:
        workout_df = make_workout(days, off_days, goal)
        st.dataframe(workout_df)

        st.subheader("Workout Rules")
        st.write("""
        Each workout is designed to fit within about 1 hour.

        Recommended timing:
        - Warm-up: 5-10 minutes
        - Main workout: 40-45 minutes
        - Cooldown/stretch: 5 minutes
        - Rest between sets: 60-90 seconds
        """)

# -----------------------------
# Tab 4: Meals and Grocery List
# -----------------------------

with tab4:
    st.header("Meal Suggestions and Grocery List")

    if goal == "Bulk":
        meals = {
            "Meal": ["Breakfast", "Lunch", "Dinner", "Snack"],
            "Suggestion": [
                "Oats with milk, banana, and peanut butter",
                "Chicken rice bowl with vegetables",
                "Ground beef or turkey with potatoes",
                "Greek yogurt with fruit"
            ]
        }
    elif goal == "Cut":
        meals = {
            "Meal": ["Breakfast", "Lunch", "Dinner", "Snack"],
            "Suggestion": [
                "Eggs and fruit",
                "Chicken salad with rice",
                "Lean turkey with vegetables and sweet potato",
                "Greek yogurt or tuna snack"
            ]
        }
    else:
        meals = {
            "Meal": ["Breakfast", "Lunch", "Dinner", "Snack"],
            "Suggestion": [
                "Eggs, oats, and fruit",
                "Chicken bowl with rice and vegetables",
                "Turkey with potatoes and vegetables",
                "Greek yogurt with fruit"
            ]
        }

    meal_df = pd.DataFrame(meals)
    st.table(meal_df)

    st.subheader(f"Grocery List Under ${budget}")

    groceries = grocery_list(goal, budget)
    st.dataframe(groceries)

    total_cost = groceries["Estimated Cost ($)"].sum()
    st.metric("Estimated Total Cost", f"${total_cost:.2f}")

# -----------------------------
# Tab 5: Project Explanation
# -----------------------------

with tab5:
    st.header("Project Explanation")

    st.write("""
    This final project uses a Streamlit GUI to create a fitness and nutrition planner.

    The user enters personal information such as weight, height, age, sex,
    activity level, fitness goal, workout days, off days, and grocery budget.

    The program then calculates:
    - Daily calories
    - Macronutrients
    - Bulking, cutting, or maintenance mode
    - A commercial gym workout plan
    - Meal suggestions
    - A grocery list under budget

    This project demonstrates:
    - Python functions
    - Conditional statements
    - User input
    - Data tables
    - Graphs
    - Algorithmic decision making
    - GUI design using Streamlit
    """)