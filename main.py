import datetime


# ==============================
# Book Class
# ==============================
class Book:
    def __init__(self, book_id, title, author, isbn, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity

    def __str__(self):
        return f"[{self.book_id}] {self.title} by {self.author} (ISBN: {self.isbn}) | Copies: {self.quantity}"


# ==============================
# Member Class
# ==============================
class Member:
    def __init__(self, member_id, name, phone):
        self.member_id = member_id
        self.name = name
        self.phone = phone

    def __str__(self):
        return f"MemberID: {self.member_id} | Name: {self.name} | Phone: {self.phone}"


# ==============================
# IssueRecord Class
# ==============================
class IssueRecord:
    def __init__(self, member_id, book_id, issue_date):
        self.member_id = member_id
        self.book_id = book_id
        self.issue_date = issue_date
        self.return_date = None

    def mark_returned(self):
        self.return_date = datetime.date.today()

    def is_returned(self):
        return self.return_date is not None

    def __str__(self):
        return f"MemberID {self.member_id} -> BookID {self.book_id} | Issued: {self.issue_date} | Returned: {self.return_date}"


# ==============================
# Library System Main Class
# ==============================
class LibrarySystem:
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"

    def __init__(self):
        self.books = []
        self.members = []
        self.issues = []
        self.logged_in = False
        self.next_book_id = 1
        self.next_member_id = 1

    # --------------------------
    # Login / Logout
    # --------------------------
    def login(self):
        print("\n--- Admin Login ---")
        username = input("Username: ")
        password = input("Password: ")

        if username == self.ADMIN_USERNAME and password == self.ADMIN_PASSWORD:
            self.logged_in = True
            print("\nLogin successful.")
        else:
            print("\nInvalid credentials.")

    def logout(self):
        self.logged_in = False
        print("\nLogged out successfully.")

    # --------------------------
    # Book Management
    # --------------------------
    def add_book(self):
        print("\n--- Add Book ---")
        title = input("Title: ")
        author = input("Author: ")
        isbn = input("ISBN: ")
        quantity = int(input("Quantity: "))

        book = Book(self.next_book_id, title, author, isbn, quantity)
        self.books.append(book)
        self.next_book_id += 1
        print("Book added successfully.")

    def display_books(self):
        print("\n--- All Books ---")
        if not self.books:
            print("No books found.")
            return

        for b in self.books:
            print(b)

    def search_books(self):
        print("\n--- Search Books ---")
        print("1. By Title")
        print("2. By Author")
        print("3. By ISBN")

        choice = input("Choose: ")

        keyword = input("Enter search keyword: ").lower()

        found = []
        for b in self.books:
            if choice == "1" and keyword in b.title.lower():
                found.append(b)
            elif choice == "2" and keyword in b.author.lower():
                found.append(b)
            elif choice == "3" and keyword in b.isbn.lower():
                found.append(b)

        if not found:
            print("No books found.")
        else:
            print("Search Results:")
            for b in found:
                print(b)

    # --------------------------
    # Member Management
    # --------------------------
    def add_member(self):
        print("\n--- Register Member ---")
        name = input("Name: ")
        phone = input("Phone: ")

        m = Member(self.next_member_id, name, phone)
        self.members.append(m)
        self.next_member_id += 1
        print("Member registered.")

    def find_member(self, member_id):
        for m in self.members:
            if m.member_id == member_id:
                return m
        return None

    # --------------------------
    # Issue / Return
    # --------------------------
    def issue_book(self):
        print("\n--- Issue Book ---")

        member_id = int(input("Enter Member ID: "))
        book_id = int(input("Enter Book ID: "))

        member = self.find_member(member_id)
        if not member:
            print("Member not found.")
            return

        book = None
        for b in self.books:
            if b.book_id == book_id:
                book = b
                break

        if not book:
            print("Book not found.")
            return

        # Check availability
        issued_count = sum(1 for i in self.issues if i.book_id == book_id and not i.is_returned())
        if issued_count >= book.quantity:
            print("No copies available to issue.")
            return

        record = IssueRecord(member_id, book_id, datetime.date.today())
        self.issues.append(record)
        print("Book issued successfully.")

    def return_book(self):
        print("\n--- Return Book ---")
        member_id = int(input("Member ID: "))
        book_id = int(input("Book ID: "))

        for i in self.issues:
            if i.member_id == member_id and i.book_id == book_id and not i.is_returned():
                i.mark_returned()
                print("Book returned successfully.")
                return

        print("No matching issue record found.")

    def display_issues(self):
        print("\n--- Issued Book Records ---")
        if not self.issues:
            print("No issued books found.")
            return

        for i in self.issues:
            print(i)

    # --------------------------
    # Menu System
    # --------------------------
    def main_menu(self):
        while True:
            if not self.logged_in:
                print("\n--- Login Menu ---")
                print("1. Login")
                print("2. Exit")
                choice = input("Choose: ")

                if choice == "1":
                    self.login()
                elif choice == "2":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice.")

            else:
                print("\n--- Library Menu (Admin) ---")
                print("1. Add Book")
                print("2. Register Member")
                print("3. Issue Book")
                print("4. Return Book")
                print("5. Display All Books")
                print("6. Search Books")
                print("7. View Issued Records")
                print("8. Logout")
                print("9. Exit")

                choice = input("Choose: ")

                if choice == "1":
                    self.add_book()
                elif choice == "2":
                    self.add_member()
                elif choice == "3":
                    self.issue_book()
                elif choice == "4":
                    self.return_book()
                elif choice == "5":
                    self.display_books()
                elif choice == "6":
                    self.search_books()
                elif choice == "7":
                    self.display_issues()
                elif choice == "8":
                    self.logout()
                elif choice == "9":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice.")


# ==============================
# Run application
# ==============================
if __name__ == "__main__":
    app = LibrarySystem()
    app.main_menu()