import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from validator import validate_format, get_domain, check_mx, is_disposable
from bulk_validator import validate_bulk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import shutil
import os


# 🔍 Validate Email
def check_email():
    email = entry.get().strip()

    if not email:
        update_result("⚠️ Enter an email", "warning")
        return

    if not validate_format(email):
        update_result("❌ Invalid Format", "error")
    else:
        domain = get_domain(email)

        if is_disposable(domain):
            update_result("⚠️ Disposable Email", "warning")
        elif not check_mx(domain):
            update_result("❌ No MX Record", "error")
        else:
            update_result("✅ Valid Email", "success")


# 🎯 Update result color
def update_result(text, status):
    colors = {
        "success": "#2ecc71",
        "error": "#e74c3c",
        "warning": "#f1c40f"
    }
    result_label.config(text=text, foreground=colors.get(status, "white"))


# 📂 Bulk Upload + GRAPH
def bulk_upload():
    global last_result_file

    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    if file_path:
        total, valid, invalid, disposable = validate_bulk(file_path, "results.csv")

        last_result_file = "results.csv"

        stats_label.config(
            text=f"Total: {total}   ✔ {valid}   ❌ {invalid}   ⚠ {disposable}"
        )

        show_graph(valid, invalid, disposable)


# 📈 Graph inside GUI
def show_graph(valid, invalid, disposable):
    for widget in graph_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(5, 3))

    labels = ["Valid", "Invalid", "Disposable"]
    values = [valid, invalid, disposable]
    colors = ["#2ecc71", "#e74c3c", "#f39c12"]

    bars = ax.bar(labels, values, color=colors)

    ax.set_title("Email Stats", fontsize=12, fontweight='bold')
    ax.set_ylabel("Count")

    for i, v in enumerate(values):
        ax.text(i, v + 0.5, str(v), ha='center', fontsize=9)

    ax.grid(axis='y', linestyle='--', alpha=0.4)

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


# 💾 Download Results
def download_results():
    if not os.path.exists("results.csv"):
        messagebox.showerror("Error", "No results found. Run validation first.")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save Results As"
    )

    if save_path:
        shutil.copy("results.csv", save_path)
        messagebox.showinfo("Success", "Results downloaded successfully!")


# 🧹 Clear
def clear_input():
    entry.delete(0, tk.END)
    result_label.config(text="")
    stats_label.config(text="")

    for widget in graph_frame.winfo_children():
        widget.destroy()


# 🪟 Window
app = tk.Tk()
app.title("Smart Email Validator")
app.geometry("650x680")
app.configure(bg="#12121c")


# 🎨 Style
style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="#12121c", foreground="white", font=("Segoe UI", 11))
style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))

style.configure("TEntry",
                fieldbackground="#1e1e2f",
                foreground="white",
                padding=8)

style.configure("Primary.TButton",
                background="#6c5ce7",
                foreground="white",
                padding=8,
                font=("Segoe UI", 10, "bold"))

style.configure("Danger.TButton",
                background="#e74c3c",
                foreground="white",
                padding=8,
                font=("Segoe UI", 10, "bold"))

style.configure("Info.TButton",
                background="#0984e3",
                foreground="white",
                padding=8,
                font=("Segoe UI", 10, "bold"))

style.configure("Success.TButton",
                background="#00b894",
                foreground="white",
                padding=8,
                font=("Segoe UI", 10, "bold"))


# 📦 Main Frame
frame = tk.Frame(app, bg="#1e1e2f", padx=25, pady=25)
frame.pack(pady=20)


# 📌 Title
title = ttk.Label(frame, text="📧 Email Validator", style="Title.TLabel")
title.grid(row=0, column=0, columnspan=3, pady=10)


# 📥 Input
entry = ttk.Entry(frame, width=40, font=("Segoe UI", 13))
entry.grid(row=1, column=0, columnspan=3, pady=10, ipady=5)

entry.bind("<Return>", lambda event: check_email())


# 🔘 Buttons
validate_btn = ttk.Button(frame, text="Validate", style="Primary.TButton", command=check_email)
validate_btn.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

clear_btn = ttk.Button(frame, text="Clear", style="Danger.TButton", command=clear_input)
clear_btn.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

download_btn = ttk.Button(frame, text="⬇ Download", style="Success.TButton", command=download_results)
download_btn.grid(row=2, column=2, padx=5, pady=10, sticky="ew")


# 📂 Bulk Upload
bulk_btn = ttk.Button(frame, text="📂 Upload CSV", style="Info.TButton", command=bulk_upload)
bulk_btn.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")


# 📊 Result
result_label = ttk.Label(frame, text="", font=("Segoe UI", 13))
result_label.grid(row=4, column=0, columnspan=3, pady=8)


# 📈 Stats
stats_label = ttk.Label(frame, text="", font=("Segoe UI", 10))
stats_label.grid(row=5, column=0, columnspan=3, pady=5)


# 📉 Graph Frame
graph_frame = tk.Frame(app, bg="#12121c")
graph_frame.pack(pady=10)


# 📌 Footer (BIGGER)
footer = ttk.Label(
    app,
    text="✨ Built with Python • Developed by Pratyasha Panda",
    font=("Segoe UI", 12, "bold"),
    background="#12121c",
    foreground="#aaaaaa"
)
footer.pack(pady=10)


# ▶️ Run
app.mainloop()