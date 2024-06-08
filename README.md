# Library System

## Project Description

This project implements an online management system for book borrowings at a library. It includes functionalities for managing books, users, and borrowings, ensuring an optimized and user-friendly service.

## Features

- **Book Management**: Allows library administrators to add, update, and delete books from the inventory. Users can view the list of available books and detailed information about each book. The system ensures that only administrators have the permissions to modify the book inventory.

- **User Management**: Enables user registration, authentication, and profile management. Users can register an account, log in using JWT authentication, and update their profile information. This service also includes functionalities for issuing and refreshing JWT tokens to maintain secure user sessions.

- **Borrowing Management**: Manages the borrowing and returning of books. Users can borrow available books, specifying the expected return date. The system automatically tracks the borrowing date and validates that the book inventory is updated accordingly. When returning a book, the system ensures the book cannot be marked as returned more than once and updates the inventory to reflect the return.

- **Filtering and Permissions**: The system includes robust filtering options for borrowings. Users can filter their borrowings based on active status and other criteria. Administrators have enhanced filtering options, allowing them to view borrowings by any user. The system ensures that only authenticated users can access borrowing functionalities, and only administrators can see borrowings of all users.

## Authentication

- **JWT Authentication**: The system uses JWT (JSON Web Tokens) for secure authentication. Upon logging in, users receive a JWT token that must be included in the headers of subsequent requests to authenticate the user. This approach ensures secure and stateless authentication.

## Custom Actions

- **Return Book**: A custom endpoint is provided to handle the return of borrowed books. This endpoint updates the actual return date and increments the book’s inventory. The system checks that a book is not marked as returned more than once, preventing duplicate return operations.

## Testing

The project includes comprehensive tests to ensure the reliability and correctness of the implemented functionalities. Tests cover models, serializers, views, and permissions, ensuring that the core functionalities work as expected and that the system handles edge cases gracefully.

## Project Setup

1. **Clone the repository**:
    ```sh
    git clone <https://github.com/March1205/library-system.git>
    cd library_system
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv .venv
    source .venv/bin/activate
    ```
   On Windows use: 
   ```sh
   .venv\Scripts\activate
   ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```sh
    python manage.py migrate
    ```

5. **Run the server**:
    ```sh
    python manage.py runserver
    ```
