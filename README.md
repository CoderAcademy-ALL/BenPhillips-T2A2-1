# BenPhillips-T2A2


R1 	Identification of the problem you are trying to solve by building this particular app.

This app is not necessarily trying to solve a problem, I would rather say that it's fulfilling a gap in the market. The gap being that there isn't a popular application out right now that is designed for connecting book lovers and creating a social network centred around books. 

R2 	Why is it a problem that needs solving?

There are several reasons why I think this problem needs addressing. Firstly, it can be very difficult sometimes for readers to find books that they want to read so if they're able to connect with like minded individuals then it will be easier for them to choose books that are more suited to their interests. Moreover, there is a lack of a centralised book social network so I think this app would be able to create this community that many book lovers would appreciate. 

R3 Why have you chosen this database system. What are the drawbacks compared to others?

For my project I have chosen to use SQL to create a relational database system. I have chosen SQL for various reasons. SQL excels at handling structured data, the application requires data to be well-defined and organized and also needs clear relationships between entities so SQL is ideal for this. Moreover, the app needs all information to be accurate, robust and consistent, and SQL provides this by ensuring the integrity of all data by compliance with ACID properties. Transactions in SQL are secure and reliable so the data in my app will always be consistent. SQL also provides querying capabilities which the app needs for retrieving and manipulating data. On the other hand, in comparison to other database systems, a drawback of SQL is it's limited scalability. SQL can have issues scaling horizontally across multiple servers while a database system like NoSQL is designed for horizontal scaling so it's better suited to scalable apps with vast volumes of data. Moreover, the rigidity of SQL schemas can be a drawback as all schemas are fixed and data must be predefined. This is a challenge when data models are rapidly evolving or when an app requires flexibility to handle loosely structure data. In comparison, NoSQL offers schema-less models which allow for easy adapatation to changing data requirements. 

R4 	Identify and discuss the key functionalities and benefits of an ORM

A key functionality of an ORM is object-oriented data access. ORM enables developers to work with database entities as objects in their programming language. For example, for this project I will be using Python in order to interact with my relational database in SQL. Developers can use an ORM to manipulate data with concepts they're already familiar with such as classes, inheritance, and relationships this simplifying the developement process. ORM frameworks (such as Flask for this project) allow for data modeling and schema generation. They provide means for defining data models using high-level abstractions like classes and attributes. With a defined model, the ORM can generate the database schema. This maintains the consistency of the data in the applications data model and the database schema. Additionally, ORM frameworks can take care of data relationships and inregrity. ORMs can handle the mapping of all types of data relationships such as many-to-one, one-to-one etc. ORMs can do this by enforcing referential integrity constraints and managing foreign key relationships. Therefore, managing complicated data relationships is simplified, data is more consistent and manual error-prone code can be avoided. 

R5 	Document all endpoints for your API

    Books:
        GET /books: Retrieve a list of books along with their reviews and review comments
        GET /book_details/{bookId}: Retrieve details of a specific book
        POST /add_book: Create a new book
        PUT /update_book: Update details of a specific book
        DELETE /delete_book/{bookId}: Delete a specific book

    Reviews:
        POST /add_review: Create a new review for a specific book
        PUT /update_review: Update details of a specific review
        DELETE /delete_review: Delete a specific review

    Comments:
        POST /add_comment: Create a new comment for a specific review
        PUT /edit_comment/{commentId}: Update details of a specific comment
        DELETE /delete_comment/{commentId}: Delete a specific comment

    Users:
        POST /register: Register a new user
        PUT /login: Login as a user


R6 	An ERD for your app

![Entity relationship diagram](Final_ERD.png)

R7 	Detail any third party services that your app will use

The API requires various third party services in order to function. I will be using Flask, a web framework that provides a set of tools, libraries and conventions used for making web applications. Flask is for Python and is known for its flexibility and simplicity. Flask will be useful for its extension, routing, and request handling capabilities in this project. SQLAlchemy is an Object-Relational Mapping (ORM) library for Python that will be utilised in the project. This service will allow me to interact with my databases by using Python objects. Flask-JWT-Extended is a Flask extension that provides support for creating JSON Web Tokens (JWT) for the authentication and authorization required in the app. The Token is attached to a specific user and is used to validate whether or not they are who they claim to be. BCrypt is a password-hashing library for securing, storing and verifying passwords. It will be used to protect user credentials. Finally, Marshmallow is an object serialization-deserialization library for Python. It is used for converting complex data types like objects into JSON making them compatible with the API. 

R8 	Describe your projects models in terms of the relationships they have with each other

The Book model represents a book in the database. Book model has a one to many relationship with the review model. The book schema includes nested fields for reviews related to the books. The Comment model represents a comment on a book review in the database. Comment model has a many-to-one relationship with the User model and the Review model and is accessible through the user and review attribute in comment model. The comment schema includes nested fields for related user and review. The Review model represents a book review. Review model has a many-to-one relationship with User and Book models and a one-to-many with Comment model. The review schema includes nested fields for related user, book and comments. The User model represents a user in the database. User model has a one-to-many relationship with the Review and Comment models. User model also includes nested fields for reviews and comments that the user has done.

R9 	Discuss the database relations to be implemented in your application

Starting from the Books model, we can see that from the Book ID stems a one (mandatory) to a many (optional) relational line connecting with the Book ID in Reviews so Book ID is a foreign key in Reviews. From the reviews table, the review ID (primary key) also has a one (mandatory) to many (optional) relational line coming out of it and connecting with the review ID in the reviews table. In the other direction, from the users table we can see a one (mandatory) to many (optional) relational line coming out of User ID in the Users table and connecting with the User IDs in the Comments and Reviews table. 

R10 	Describe the way tasks are allocated and tracked in your project

I will be tracking the progress of my work using the Kanban website 'Trello'. I started work on this project on June 24rd so the following plan is designed with that in mind.

https://trello.com/invite/b/sOnxtJrs/ATTIdda6d1c2e1de6ef72717b5bfb591dd8b4D95F3EF/t2a2-board

Day 1 (June 24th):

    Complete all initial project documentation and planning
        Define the project objectives, scope, and target audience.
        Identify the core features and functionality required for the API.
        Create ERD
        Define API endpoints
        Answer all necessary documentation questions

Day 2 (June 25th):

    Set up the development environment, including programming languages and frameworks.
    Create a Git repository
    Implement the foundational API structure and basic endpoints.

Day 3 (June 26th):

    Develop authentication and authorization mechanisms for the API.
    Handle validation and error handling for API requests.

Day 4 (June 27th):

    Implement database integration.
    Ensure data security and privacy measures are in place.

Day 5 (June 28th):

    Perform API testing and debugging to ensure proper functionality.
    Review and refactor code for quality and maintainability.

Day 6 (June 29th):

    Conduct thorough testing of the API, including functional, integration, and performance testing.
    Fix any identified bugs or issues and retest the fixed functionality.

Day 7 (June 30th):

    Conduct a final review of the API's documentation and ensure it is accurate and up to date.
    Address any outstanding issues or bugs found during testing and deployment.

Day 8 (July 1st):

    Finalise all documentation
    Upload project
