

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sooraj@1607",
        database="testdb"
    )

# ─────────────────────────────────────────
# CREATE
# ─────────────────────────────────────────
def add_student(Name, Age, Physics, Maths, Chemistry):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        Total = Physics + Maths + Chemistry
        Average = round(Total / 3, 2)
        cursor.execute(
            "INSERT INTO students (Name, Age, Physics, Maths, Chemistry, Total, Average) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (Name, Age, Physics, Maths, Chemistry, Total, Average)
        )
        conn.commit()
        print(f"Student '{Name}' added successfully!")
        print(f"Total: {Total} | Average: {Average}\n")
    except mysql.connector.Error as e:
        print(f"Database error: {e}\n")
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────
# READ — all students
# ─────────────────────────────────────────
def get_all_students():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        if rows:
            print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Physics':<10} {'Maths':<10} {'Chemistry':<12} {'Total':<8} {'Average':<8}")
            print("-" * 80)
            for row in rows:
                print(f"{row['Id']:<5} {row['Name']:<20} {row['Age']:<5} {row['Physics']:<10} "
                      f"{row['Maths']:<10} {row['Chemistry']:<12} {row['Total']:<8} {row['Average']:<8}")
        else:
            print("No students found.\n")
        return rows
    except mysql.connector.Error as e:
        print(f"Database error: {e}\n")
        return []
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────
# READ — single student by ID
# ─────────────────────────────────────────
def get_student_by_id(student_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        row = cursor.fetchone()
        if row:
            print(f"\nStudent found:")
            for key, value in row.items():
                print(f"  {key}: {value}")
        else:
            print(f"No student found with ID {student_id}.\n")
        return row
    except mysql.connector.Error as e:
        print(f"Database error: {e}\n")
        return None
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────
# UPDATE
# ─────────────────────────────────────────
def update_student(student_id, Name=None, Age=None, Physics=None, Maths=None, Chemistry=None):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch existing record first
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        existing = cursor.fetchone()
        if not existing:
            print(f"No student found with ID {student_id}.\n")
            return

        # Use new value if provided, else keep existing
        Name      = Name      if Name      is not None else existing["Name"]
        Age       = Age       if Age       is not None else existing["Age"]
        Physics   = Physics   if Physics   is not None else existing["Physics"]
        Maths     = Maths     if Maths     is not None else existing["Maths"]
        Chemistry = Chemistry if Chemistry is not None else existing["Chemistry"]

        Total   = Physics + Maths + Chemistry
        Average = round(Total / 3, 2)

        cursor.execute(
            "UPDATE students SET Name=%s, Age=%s, Physics=%s, Maths=%s, "
            "Chemistry=%s, Total=%s, Average=%s WHERE id=%s",
            (Name, Age, Physics, Maths, Chemistry, Total, Average, student_id)
        )
        conn.commit()
        print(f"Student ID {student_id} updated successfully!")
        print(f"New Total: {Total} | New Average: {Average}\n")
    except mysql.connector.Error as e:
        print(f"Database error: {e}\n")
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────
def delete_student(student_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Name FROM students WHERE id = %s", (student_id,))
        row = cursor.fetchone()
        if not row:
            print(f"No student found with ID {student_id}.\n")
            return
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
        print(f"Student '{row['Name']}' (ID {student_id}) deleted successfully!\n")
    except mysql.connector.Error as e:
        print(f"Database error: {e}\n")
    finally:
        cursor.close()
        conn.close()


# ─────────────────────────────────────────
# MENU (optional interactive runner)
# ─────────────────────────────────────────
def menu():
    while True:
        print("\n===== Student Management =====")
        print("1. Add student")
        print("2. View all students")
        print("3. View student by ID")
        print("4. Update student")
        print("5. Delete student")
        print("6. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            name      = input("Name: ")
            age       = int(input("Age: "))
            physics   = float(input("Physics marks: "))
            maths     = float(input("Maths marks: "))
            chemistry = float(input("Chemistry marks: "))
            add_student(name, age, physics, maths, chemistry)

        elif choice == "2":
            get_all_students()

        elif choice == "3":
            sid = int(input("Enter student ID: "))
            get_student_by_id(sid)

        elif choice == "4":
            sid = int(input("Enter student ID to update: "))
            print("Press Enter to keep existing value.")
            name      = input("New Name: ")      or None
            age_in    = input("New Age: ")       or None
            phy_in    = input("New Physics: ")   or None
            mat_in    = input("New Maths: ")     or None
            chem_in   = input("New Chemistry: ") or None
            update_student(
                sid,
                Name      = name,
                Age       = int(age_in)    if age_in   else None,
                Physics   = float(phy_in)  if phy_in   else None,
                Maths     = float(mat_in)  if mat_in   else None,
                Chemistry = float(chem_in) if chem_in  else None,
            )

        elif choice == "5":
            sid = int(input("Enter student ID to delete: "))
            confirm = input(f"Are you sure you want to delete student ID {sid}? (yes/no): ")
            if confirm.lower() == "yes":
                delete_student(sid)

        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()


