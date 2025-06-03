import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta

def calculate_tdee(weight, age, gender, height_cm):
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161
    return bmr * 1.2  # Sedentary by default

def estimate_days_to_goal(tdee, daily_calories, current_weight, goal_weight):
    if tdee is None or daily_calories is None:
        return 0
    daily_deficit = tdee - daily_calories
    if daily_deficit <= 0:
        return float('inf')
    weight_to_lose = current_weight - goal_weight
    total_deficit_needed = weight_to_lose * 7700  # Approx calories per kg
    return int(total_deficit_needed / daily_deficit)

def update_fields():
    try:
        unit = unit_var.get()
        weight = float(entry_weight.get())
        age = int(entry_age.get())
        gender = gender_var.get()
        goal_weight = float(entry_goal_weight.get())

        if unit == "Metric":
            height_cm = float(entry_height.get())
        else:
            ft = float(entry_height_ft.get())
            inch = float(entry_height_in.get())
            height_cm = (ft * 30.48) + (inch * 2.54)
            weight *= 0.453592  # lbs to kg
            goal_weight *= 0.453592

        tdee = calculate_tdee(weight, age, gender, height_cm)

        calorie_values = []
        for entry in calorie_entries:
            try:
                calorie_values.append(float(entry.get()))
            except:
                continue

        avg_calories = sum(calorie_values) / len(calorie_values) if calorie_values else None
        days_needed = estimate_days_to_goal(tdee, avg_calories, weight, goal_weight)

        result = f"TDEE: {round(tdee)} kcal/day\n"
        if avg_calories:
            result += f"Avg Intake: {round(avg_calories)} kcal/day\n"
            result += f"Estimated days to goal: {days_needed} days\n"
            result += f"Estimated goal date: {(datetime.now() + timedelta(days=days_needed)).strftime('%Y-%m-%d')}"
        else:
            result += "Please enter calorie intake data."

        label_result.config(text=result)
    except Exception as e:
        messagebox.showerror("Error", str(e))



def refresh_profile_dropdown():
    files = [f.replace(".json", "") for f in os.listdir() if f.endswith(".json")]
    profile_dropdown["values"] = files

def save_session():
    if not profile_name.get().strip():
        messagebox.showerror("Error", "Please enter a profile name.")
        return
    try:
        data = {
            "unit": unit_var.get(),
            "weight": entry_weight.get(),
            "age": entry_age.get(),
            "gender": gender_var.get(),
            "goal_weight": entry_goal_weight.get(),
            "height": entry_height.get(),
            "height_ft": entry_height_ft.get(),
            "height_in": entry_height_in.get(),
            "calorie_entries": [entry.get() for entry in calorie_entries]
        }
        with open(f"{profile_name.get()}.json", "w") as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Saved", "Session saved successfully.")
        refresh_profile_dropdown()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save session: {e}")

def load_session():
    selected = profile_dropdown.get()
    if not selected:
        messagebox.showerror("Error", "No profile selected.")
        return
    try:
        with open(f"{selected}.json", "r") as f:
            data = json.load(f)
        unit_var.set(data["unit"])
        entry_weight.delete(0, tk.END)
        entry_weight.insert(0, data["weight"])
        entry_age.delete(0, tk.END)
        entry_age.insert(0, data["age"])
        gender_var.set(data["gender"])
        entry_goal_weight.delete(0, tk.END)
        entry_goal_weight.insert(0, data["goal_weight"])
        entry_height.delete(0, tk.END)
        entry_height.insert(0, data["height"])
        entry_height_ft.delete(0, tk.END)
        entry_height_ft.insert(0, data["height_ft"])
        entry_height_in.delete(0, tk.END)
        entry_height_in.insert(0, data["height_in"])

        for i, value in enumerate(data["calorie_entries"]):
            if i < len(calorie_entries):
                calorie_entries[i].delete(0, tk.END)
                calorie_entries[i].insert(0, value)
        update_fields()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load session: {e}")

# GUI Setup
root = tk.Tk()
root.title("Weight Loss Tracker")
root.geometry("400x950")

unit_var = tk.StringVar(value="Metric")
tk.Label(root, text="Unit").grid(row=0, column=0)
ttk.Combobox(root, textvariable=unit_var, values=["Metric", "Imperial"]).grid(row=0, column=1)

tk.Label(root, text="Weight").grid(row=1, column=0)
entry_weight = tk.Entry(root)
entry_weight.grid(row=1, column=1)

tk.Label(root, text="Age").grid(row=2, column=0)
entry_age = tk.Entry(root)
entry_age.grid(row=2, column=1)

tk.Label(root, text="Gender").grid(row=3, column=0)
gender_var = tk.StringVar(value="Male")
ttk.Combobox(root, textvariable=gender_var, values=["Male", "Female"]).grid(row=3, column=1)

tk.Label(root, text="Goal Weight").grid(row=4, column=0)
entry_goal_weight = tk.Entry(root)
entry_goal_weight.grid(row=4, column=1)

tk.Label(root, text="Height (cm)").grid(row=5, column=0)
entry_height = tk.Entry(root)
entry_height.grid(row=5, column=1)

tk.Label(root, text="Height ft").grid(row=6, column=0)
entry_height_ft = tk.Entry(root)
entry_height_ft.grid(row=6, column=1)

tk.Label(root, text="Height in").grid(row=7, column=0)
entry_height_in = tk.Entry(root)
entry_height_in.grid(row=7, column=1)

tk.Label(root, text="Calories (14 entries)").grid(row=8, column=0, columnspan=2)
calorie_entries = []
tk.Label(root, text="Day 1").grid(row=9, column=0)
entry = tk.Entry(root, width=10)
entry.grid(row=9, column=1)
calorie_entries.append(entry)
tk.Label(root, text="Day 2").grid(row=9, column=2)
entry = tk.Entry(root, width=10)
entry.grid(row=9, column=3)
calorie_entries.append(entry)
tk.Label(root, text="Day 3").grid(row=10, column=0)
entry = tk.Entry(root, width=10)
entry.grid(row=10, column=1)
calorie_entries.append(entry)
tk.Label(root, text="Day 4").grid(row=10, column=2)
entry = tk.Entry(root, width=10)
entry.grid(row=10, column=3)
calorie_entries.append(entry)
tk.Label(root, text="Day 5").grid(row=11, column=0)
entry = tk.Entry(root, width=10)
entry.grid(row=11, column=1)
calorie_entries.append(entry)
tk.Label(root, text="Day 6").grid(row=11, column=2)
entry = tk.Entry(root, width=10)
entry.grid(row=11, column=3)
calorie_entries.append(entry)
tk.Label(root, text="Day 7").grid(row=12, column=0)
entry = tk.Entry(root, width=10)
entry.grid(row=12, column=1)
calorie_entries.append(entry)
tk.Label(root, text="Day 8").grid(row=12, column=2)
entry = tk.Entry(root, width=10)
entry.grid(row=12, column=3)
calorie_entries.append(entry)
tk.Label(root, text="Day 9").grid(row=13, column=0)
entry = tk.Entry(root, width=10)
entry.grid(row=13, column=1)
calorie_entries.append(entry)
tk.Label(root, text="Day 10").grid(row=13, column=2)
entry = tk.Entry(root, width=10)
entry.grid(row=13, column=3)
calorie_entries.append(entry)
tk.Label(root, text="Day 11").grid(row=14, column=0)
entry = tk.Entry(root, width=10)
entry.grid(row=14, column=1)
calorie_entries.append(entry)
tk.Label(root, text="Day 12").grid(row=14, column=2)
entry = tk.Entry(root, width=10)
entry.grid(row=14, column=3)
calorie_entries.append(entry)
tk.Label(root, text="Day 13").grid(row=15, column=0)
entry = tk.Entry(root, width=10)
entry.grid(row=15, column=1)
calorie_entries.append(entry)
tk.Label(root, text="Day 14").grid(row=15, column=2)
entry = tk.Entry(root, width=10)
entry.grid(row=15, column=3)
calorie_entries.append(entry)

calorie_entries.append(entry)

tk.Label(root, text="Select Profile").grid(row=16, column=0)
profile_dropdown = ttk.Combobox(root, state="readonly")
profile_dropdown.grid(row=16, column=1)
refresh_profile_dropdown()

tk.Label(root, text="Or enter new profile name").grid(row=17, column=0)
profile_name = tk.StringVar()
tk.Entry(root, textvariable=profile_name).grid(row=17, column=1)

tk.Button(root, text="Save Profile", command=save_session).grid(row=18, column=0)
tk.Button(root, text="Load Profile", command=load_session).grid(row=18, column=1)

label_result = tk.Label(root, text="Your results will appear here", justify="left")
label_result.grid(row=19, column=0, columnspan=2)


tk.Button(root, text="Calculate", command=update_fields).grid(row=20, column=0, columnspan=2)

root.mainloop()
