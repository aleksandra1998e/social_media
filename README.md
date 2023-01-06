<h1>Social Networking API</h1>

This is the API for a social networking application. It allows users to sign up, log in, create, edit, delete, and view posts, and like or dislike other users' posts.

<ul> 
<li> Python 3.8+ </li>
<li> FastAPI 0.50.0+
<li> A database management system (DBMS) such as Sqlite, PostgreSQL, or MySQL </li>
<li> Clearbit (optional) </li>
<li> EmailHunter (optional) </li>
</ul>

<h3> Installation </h3>

Clone the repository: <br>
<code> git clone https://github.com/aleksandra1998e/social_media </code> <br>

Install the required dependencies:<br>
<code> pip install -r requirements.txt </code> <br>

<p>Create a .env file in the root directory of the project and set the following environment variables:<br>
<ul> 
<li> DATABASE_URL: URL of the database (e.g. postgresql://user:password@localhost/database) </li>
<li> JWT_SECRET_KEY: Secret key for JWT authentication </li>
</ul>

Run the app: <br>

<code> uvicorn main:app --reload </code> <br>
The API will now be running at http://localhost:8000.

<h3> Documentation </h3>

You can view the API documentation at http://localhost:8000/docs.

<h3> Deployment </h3>

To deploy the API, you can use a service like Heroku or AWS Elastic Beanstalk.

<h3> Testing </h3>

To test the API, you can use a tool like Postman to send HTTP requests to the API endpoints and observe the responses.
