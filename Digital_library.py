# Digital Library Management System
# Streamlit Version (Advanced – Allowed as per SMIT PDF)

import streamlit as st

# =========================
# BOOK CLASS
# =========================
class Book:
    def __init__(self, title, author, book_id, total_copies):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.total_copies = total_copies
        self.available_copies = total_copies


# =========================
# LIBRARY CLASS
# =========================
class Library:
    def __init__(self):
        self.books = []
        self.borrowed_records = {}

    def add_book(self, title, author, book_id, copies):
        self.books.append(Book(title, author, book_id, copies))

    def search_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def search_by_author(self, author):
        return [book for book in self.books if author.lower() in book.author.lower()]

    def borrow_book(self, user, book_id):
        for book in self.books:
            if book.book_id == book_id:
                if book.available_copies > 0:
                    book.available_copies -= 1
                    self.borrowed_records[user] = book.title
                    return True
                return False
        return None

    def return_book(self, user):
        if user not in self.borrowed_records:
            return False

        title = self.borrowed_records[user]
        for book in self.books:
            if book.title == title:
                book.available_copies += 1
                del self.borrowed_records[user]
                return True


# =========================
# STREAMLIT APP
# =========================
st.set_page_config(page_title="Digital Library System", layout="centered")

st.title("📚 Digital Library Management System")

# Initialize library in session
if "library" not in st.session_state:
    st.session_state.library = Library()

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Book",
        "Search by Title",
        "Search by Author",
        "Borrow Book",
        "Return Book",
        "View All Books",
    ],
)

library = st.session_state.library

# =========================
# ADD BOOK
# =========================
if menu == "Add Book":
    st.subheader("➕ Add New Book")

    title = st.text_input("Book Title")
    author = st.text_input("Author Name")
    book_id = st.text_input("Book ID")
    copies = st.number_input("Total Copies", min_value=1, step=1)

    if st.button("Add Book"):
        library.add_book(title, author, book_id, copies)
        st.success("Book added successfully!")

# =========================
# SEARCH BY TITLE
# =========================
elif menu == "Search by Title":
    st.subheader("🔍 Search Book by Title")
    title = st.text_input("Enter title")

    if st.button("Search"):
        results = library.search_by_title(title)
        if results:
            for book in results:
                st.write(
                    f"**{book.title}** | {book.author} | "
                    f"{book.available_copies}/{book.total_copies} available"
                )
        else:
            st.warning("No book found.")

# =========================
# SEARCH BY AUTHOR
# =========================
elif menu == "Search by Author":
    st.subheader("🔍 Search Book by Author")
    author = st.text_input("Enter author name")

    if st.button("Search"):
        results = library.search_by_author(author)
        if results:
            for book in results:
                st.write(
                    f"**{book.title}** | {book.author} | "
                    f"{book.available_copies}/{book.total_copies} available"
                )
        else:
            st.warning("No book found.")

# =========================
# BORROW BOOK
# =========================
elif menu == "Borrow Book":
    st.subheader("📖 Borrow Book")

    user = st.text_input("Your Name")
    book_id = st.text_input("Book ID")

    if st.button("Borrow"):
        result = library.borrow_book(user, book_id)
        if result:
            st.success("Book borrowed successfully!")
        elif result is False:
            st.error("Book not available.")
        else:
            st.error("Invalid Book ID.")

# =========================
# RETURN BOOK
# =========================
elif menu == "Return Book":
    st.subheader("↩️ Return Book")

    user = st.text_input("Your Name")

    if st.button("Return"):
        if library.return_book(user):
            st.success("Book returned successfully!")
        else:
            st.error("No borrowed book found.")

# =========================
# VIEW ALL BOOKS
# =========================
elif menu == "View All Books":
    st.subheader("📚 All Books")

    if not library.books:
        st.info("Library is empty.")
    else:
        for book in library.books:
            st.write(
                f"**{book.title}** | {book.author} | "
                f"{book.available_copies}/{book.total_copies}"
            )
