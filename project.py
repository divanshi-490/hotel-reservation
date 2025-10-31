import sqlite3
from tkinter import *
from tkinter import messagebox

# ---------------------- Database Setup ----------------------
conn = sqlite3.connect("hotel_reservation.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    room_type TEXT NOT NULL,
    check_in TEXT NOT NULL,
    check_out TEXT NOT NULL,
    num_days INTEGER NOT NULL,
    num_guests INTEGER NOT NULL
)
""")
conn.commit()

# ---------------------- Functions ----------------------
def add_reservation():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    room_type = room_var.get()
    check_in = entry_checkin.get()
    check_out = entry_checkout.get()
    days = entry_days.get()
    guests = entry_guests.get()

    if name == "" or phone == "" or check_in == "" or check_out == "" or days == "" or guests == "":
        messagebox.showwarning("Input Error", "All required fields must be filled.")
        return

    cursor.execute("""
        INSERT INTO reservations (customer_name, phone, email, room_type, check_in, check_out, num_days, num_guests)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, phone, email, room_type, check_in, check_out, days, guests))
    conn.commit()

    messagebox.showinfo("Success", "Reservation saved successfully!")
    clear_fields()

def view_reservations():
    cursor.execute("SELECT * FROM reservations")
    rows = cursor.fetchall()

    view_window = Toplevel(root)
    view_window.title("All Reservations")
    view_window.geometry("900x500")
    view_window.config(bg="#FAF3E0")

    Label(view_window, text="Hotel Reservation Records", font=("Poppins", 20, "bold"),
          bg="#FAF3E0", fg="#5B3A29").pack(pady=10)

    if not rows:
        Label(view_window, text="No reservations found.", bg="#FAF3E0",
              font=("Poppins", 14)).pack()
        return

    # Scrollable frame
    canvas = Canvas(view_window, bg="#FAF3E0", highlightthickness=0)
    scrollbar = Scrollbar(view_window, orient=VERTICAL, command=canvas.yview)
    scroll_frame = Frame(canvas, bg="#FAF3E0")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill="both", expand=True, padx=10)
    scrollbar.pack(side=RIGHT, fill="y")

    # Display each record
    for i, row in enumerate(rows):
        record_frame = Frame(scroll_frame, bg="#FFF7E6", bd=1, relief="solid")
        record_frame.pack(fill="x", padx=15, pady=6)

        Label(
            record_frame,
            text=f"{i+1}. {row[1]} | {row[2]} | {row[4]} | Check-In: {row[5]} | Check-Out: {row[6]} | Guests: {row[8]}",
            font=("Poppins", 11),
            bg="#FFF7E6",
            anchor="w",
            wraplength=650
        ).pack(side=LEFT, padx=10, pady=8, fill="x", expand=True)

        Button(record_frame, text="Update", bg="#D4A373", fg="black",
               font=("Poppins", 9, "bold"), width=10,
               command=lambda rid=row[0]: update_reservation(rid)).pack(side=RIGHT, padx=5, pady=5)

        Button(record_frame, text="Delete", bg="#A0522D", fg="white",
               font=("Poppins", 9, "bold"), width=10,
               command=lambda rid=row[0], vw=view_window: delete_reservation(rid, vw)).pack(side=RIGHT, padx=5, pady=5)

def delete_reservation(res_id, view_window):
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
    if confirm:
        cursor.execute("DELETE FROM reservations WHERE id=?", (res_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Record deleted successfully.")
        view_window.destroy()
        view_reservations()

def update_reservation(res_id):
    cursor.execute("SELECT * FROM reservations WHERE id=?", (res_id,))
    record = cursor.fetchone()

    if not record:
        messagebox.showerror("Error", "Record not found.")
        return

    update_window = Toplevel(root)
    update_window.title("Update Reservation")
    update_window.geometry("400x550")
    update_window.config(bg="#FAEED1")

    Label(update_window, text="Update Reservation", font=("Poppins", 18, "bold"),
          bg="#5B3A29", fg="white", pady=10).pack(fill=X)

    labels = ["Customer Name:", "Phone:", "Email:", "Room Type:", "Check-In:", "Check-Out:", "Days:", "Guests:"]
    entries = []

    for label in labels:
        Label(update_window, text=label, bg="#FAEED1", font=("Poppins", 12)).pack(pady=(10, 0))
        entry = Entry(update_window, width=35, font=("Poppins", 11))
        entry.pack(pady=3)
        entries.append(entry)

    for i, value in enumerate(record[1:]):
        entries[i].insert(0, value)

    def save_update():
        cursor.execute("""
            UPDATE reservations
            SET customer_name=?, phone=?, email=?, room_type=?, check_in=?, check_out=?, num_days=?, num_guests=?
            WHERE id=?
        """, tuple(e.get() for e in entries) + (res_id,))
        conn.commit()
        messagebox.showinfo("Updated", "Reservation updated successfully!")
        update_window.destroy()
        view_reservations()

    Button(update_window, text="Save Changes", bg="#8B5E3C", fg="white",
           font=("Poppins", 12, "bold"), width=20, command=save_update).pack(pady=20)

def clear_fields():
    entry_name.delete(0, END)
    entry_phone.delete(0, END)
    entry_email.delete(0, END)
    entry_checkin.delete(0, END)
    entry_checkout.delete(0, END)
    entry_days.delete(0, END)
    entry_guests.delete(0, END)
    room_var.set("Single")

# ---------------------- GUI Setup ----------------------
root = Tk()
root.title("GuestEase Booking System")
root.geometry("600x750")
root.config(bg="#FAEED1")

Label(root, text="GuestEase Booking System", font=("Poppins", 22, "bold"),
      bg="#5B3A29", fg="white", pady=15).pack(fill=X)

Label(root, text="Please fill the details below:", font=("Poppins", 13),
      bg="#FAEED1", fg="#5B3A29").pack(pady=10)

# Fields
entry_name = Entry(root, width=40, font=("Poppins", 12))
entry_phone = Entry(root, width=40, font=("Poppins", 12))
entry_email = Entry(root, width=40, font=("Poppins", 12))
entry_checkin = Entry(root, width=40, font=("Poppins", 12))
entry_checkout = Entry(root, width=40, font=("Poppins", 12))
entry_days = Entry(root, width=40, font=("Poppins", 12))
entry_guests = Entry(root, width=40, font=("Poppins", 12))
room_var = StringVar(value="Single")

fields = [
    ("Customer Name:", entry_name),
    ("Phone Number:", entry_phone),
    ("Email (optional):", entry_email),
    ("Room Type:", None),
    ("Check-In Date (YYYY-MM-DD):", entry_checkin),
    ("Check-Out Date (YYYY-MM-DD):", entry_checkout),
    ("Number of Days:", entry_days),
    ("Number of Guests:", entry_guests)
]

for label, widget in fields:
    Label(root, text=label, font=("Poppins", 12, "bold"), bg="#FAEED1", fg="#5B3A29").pack()
    if label == "Room Type:":
        OptionMenu(root, room_var, "Single", "Double", "Deluxe", "Suite").pack(pady=4)
    else:
        widget.pack(pady=4)

# Buttons
Button(root, text="Add Reservation", command=add_reservation, bg="#8B5E3C", fg="white",
       font=("Poppins", 13, "bold"), width=25).pack(pady=10)

Button(root, text="View All Reservations", command=view_reservations, bg="#D4A373", fg="black",
       font=("Poppins", 13, "bold"), width=25).pack(pady=10)

Button(root, text="Clear Fields", command=clear_fields, bg="#A0522D", fg="white",
       font=("Poppins", 13, "bold"), width=25).pack(pady=10)

root.mainloop()
