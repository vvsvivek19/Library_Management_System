📌 Key Features to Implement
We can break the features into core features (required) and additional features (enhancements for later).

1️⃣ Core Features (Essential for MySQL Integration)

✅ Database Connection & Setup
- Connect Python to MySQL using mysql-connector-python or SQLAlchemy. --> Done
- Create a database (LibraryDB) and required tables (Books, BorrowedBooks, Users). --> Done

✅ User System:
- Login: Both as Admin and User
- Register: Both Admin and User
- Forgot Password: Both Admin and User

✅ Book Management
- Add books (store title, author, ISBN, status). --> Done
- Remove books (delete from database by ISBN). --> Done
- Search books (by title, author, or ISBN). --> Done
- Display available books. --> Pending
- Update book details (e.g., changing the author or title). -->Pending

✅ Borrow & Return System
Borrow a book (mark as borrowed, store user details). --> Pending
- In this step, you will implement the functionality to borrow a book, which involves:
    ✅ Checking if the user is new or already exists. If new then register them and then move borrowing
    ✅ Prevent duplicate borrowing (a book can’t be borrowed twice until returned).
    ✅ Checking if the book exists in the library.
    ✅ Ensuring there are available copies to borrow.
    ✅ Updating the Books table (reducing available copies).
    ✅ Adding an entry in the BorrowedBooks table.
- Return a book (update availability status). --> Pending
 Show borrowed books (list books currently borrowed).

✅ User Management (Basic)
- Users should enter their name before borrowing a book.
- Store user details in a separate Users table (optional).
- Allow users to see their borrowing history.

2️⃣ Additional Features (Future Enhancements)
🚀 Advanced User System
- Admin Registration process --> Done
- Register & login functionality for users. --> PEnding
- Admin & normal users (admin can add/remove books, normal users can only borrow/return).

🚀 Book Reservation System
- Users can reserve books and get notified when available. --> Pending

🚀 Fine Calculation System
- If a book is not returned within X days, calculate fine. --> Pending

🚀 Detailed Book Info
- Add book category, published year, total copies. --> Pending

🚀 Logs & Reports
- Keep logs of all transactions (who borrowed what & when). --> Pending
- Generate reports (most borrowed books, active users). --> Pending

💡 How to Proceed?
1️⃣ Step 1 – Setup MySQL Database & Tables
2️⃣ Step 2 – Implement Add, Remove, Search, Display using MySQL
3️⃣ Step 3 – Implement Borrow & Return using MySQL
4️⃣ Step 4 – Enhance with User Management & Extra Features