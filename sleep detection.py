
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# Generate sample data
np.random.seed(42)
X = np.column_stack([
    np.random.uniform(3, 10, 500),
    np.random.randint(0, 4, 500),
    np.random.uniform(0, 90, 500),
    np.random.uniform(0, 180, 500),
    np.random.randint(0, 11, 500),
    np.random.randint(0, 4, 500),
    np.random.randint(0, 2, 500)
])

score = X[:, 0]*2 - X[:, 1]*1.5 + X[:, 2]/20 - X[:, 3]/30 - X[:, 4]*0.8 + X[:, 5] - X[:, 6]*2
y = np.where(score >= 10, "Good", np.where(score >= 3, "Average", "Poor"))

# Split data
a, b, c, d = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale data
scaler = StandardScaler()
a_scaled = scaler.fit_transform(a)
b_scaled = scaler.transform(b)
X_scaled = scaler.transform(X)

# Define algorithms
models = {
    "Logistic Regression": LogisticRegression(max_iter=5000),
    "Random Forest": RandomForestClassifier(random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "SVM": SVC()
}

# Compare algorithms
results = {}
for name, clf in models.items():
    if name in ["Logistic Regression", "SVM"]:
        clf.fit(a_scaled, c)
        pred = clf.predict(b_scaled)
    else:
        clf.fit(a, c)
        pred = clf.predict(b)
    results[name] = accuracy_score(d, pred)

best = max(results, key=results.get)
model = models[best]

# Train best model on all data
if best in ["Logistic Regression", "SVM"]:
    model.fit(X_scaled, y)
else:
    model.fit(X, y)


def predict():
    try:
        v = [float(e.get().strip()) for e in entries]

        v += [
            int(caffeine.get()),
            int(mood.get()),
            int(interrupt.get())
        ]

        if not (0 < v[0] <= 24):
            raise ValueError("Sleep Hours must be between 0 and 24.")

        if not (0 <= v[1] <= 90):
            raise ValueError("Exercise Minutes must be between 0 and 90.")

        if not (0 <= v[2] <= 180):
            raise ValueError("Screen Time must be between 0 and 180.")

        if not (0 <= v[3] <= 10):
            raise ValueError("Stress Level must be between 0 and 10.")

        if not (0 <= v[4] <= 10):
            raise ValueError("Caffeine value is invalid.")

        if not (0 <= v[5] <= 3):
            raise ValueError("Mood value is invalid.")

        if v[6] not in (0, 1):
            raise ValueError("Sleep Interruptions must be 0 or 1.")

        if best in ["Logistic Regression", "SVM"]:
            prediction_input = scaler.transform([v])
        else:
            prediction_input = [v]

        ans = model.predict(prediction_input)[0]

        tips = {
            "Good": "Maintain your healthy sleep habits.",
            "Average": "Try reducing screen time before bed.",
            "Poor": "Review your daily sleep routine."
        }

        output.config(
            text=f"Sleep Quality: {ans}\n{tips[ans]}"
        )

    except (ValueError, TypeError) as error:
        messagebox.showerror("Input Error", str(error))


def chart():
    plt.bar(results.keys(), results.values())
    plt.ylabel("Accuracy")
    plt.title("Algorithm Accuracy Comparison")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.show()

# Create GUI
root = tk.Tk()
root.title("Sleep Quality Predictor")
root.geometry("390x610")

tk.Label(root, text="Sleep Quality Predictor",
         font=("Arial", 16, "bold")).pack(pady=10)

entries = []
for label in ["Sleep Hours (0-24)", "Exercise Minutes (0-90)",
              "Screen Time Minutes (0-180)", "Stress Level (0-10)"]:
    tk.Label(root, text=label).pack()
    e = tk.Entry(root)
    e.pack(pady=3)
    entries.append(e)

def combo(label, values, default):
    tk.Label(root, text=label).pack()
    cb = ttk.Combobox(root, values=values, state="readonly")
    cb.current(default)
    cb.pack(pady=3)
    return cb

caffeine = combo("Caffeine (0=None, 3=High)", [0, 1, 2, 3], 0)
mood = combo("Mood (0=Sad, 3=Happy)", [0, 1, 2, 3], 2)
interrupt = combo("Sleep Interruptions (0=No, 1=Yes)", [0, 1], 0)

tk.Button(root, text="Predict Sleep Quality",
          command=predict).pack(pady=10)

output = tk.Label(root, text="", wraplength=340)
output.pack(pady=8)

tk.Label(root, text=f"Selected Algorithm: {best}").pack()
tk.Button(root, text="Compare Algorithms", command=chart).pack(pady=8)

root.mainloop()
