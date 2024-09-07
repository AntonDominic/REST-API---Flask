This is a simple RESTful API built using Flask and Flask-RESTful that provides user authentication and profile management. 
The API uses JWT (JSON Web Token) for secure user authentication, and SQLite as the database for persistence.

Features:
  User Registration: Register a new user with name, email, password, and role.
  User Login: Login using email and password to receive a JWT token.
  Protected Routes: Access user profile and update profile details with JWT-based authentication.
  Profile Management: Retrieve and update user profile information.

Database:
  SQLite 3

API End points:

#'/register':[POST]
      1. Import Resource from flask_restful.
      2. Create a class named "Register" and pass the "Resoure" as an argument to the class.
      3. Create a variable called user_post_args and pass the value "reqparse.RequestParser()" so that the class is initialised on to the variable.
      4. Use the method "add_argument" onto the user_post_args and pass the necessary attributes such as name, email, password and role as in seperate line and                 mention the keyword, "required=True" so that every attribute must be filled in order to register a user
      5. Use the POST method under the class, 'Register'. Parse the arguments under user_post_args onto args variable.
      6. Use filter_by method as a query to our User Model Database to check if the email provided already exists and if so, pass the argument for the same and abort           the function.
      7. Else, pass the name, email, role as a key value pair or jsons to the args variable.
      8. use hash_password method to encrypt the password provided as a security measure.
      9. Add the new_user to our database.
      10. Return the json, "Registered Successfully".

#'/login':[POST]
      1. Create a class named "Login" and pass the class "Resource" as an argument.
      2. Use the POST method under the class and initialise a variable login_args by passing reqparse.RequestParser() module.
      3. Use add_argument method and pass the email and password provided by the user onto login_args seperately.
      4. Parse the given arguments onto the variable args using parse_args method.
      5. use filter_by query on our database to check if the user provides a valid registered email and check the matching password for the provided email using        verify_password function that we defined in our database model. if these cases do not satisfy abort the request and return "Invalid Credentials" message.
      6. If the user credentials are valid, create a JWT from create_access_token function inherited from lask_jwt_extended module.
      7. Return the JWT 

#'/profile':[GET]
      1. Create a class UserProfile and pass the Resource class as an argument.
      2. Make use of @jwt_required() decorator/function to look for valid JSON web tokens.
      3. Use get_jwt_identity() to get the associated user_id and pass it to our database to fetch the user.  
      4. If the user is valid, fetch the user details and return it. 
      5. If it is invalid, return "User not found".

#'/profile/update':[PUT]
      1. Create a class UpdateProfile and pass the Resource class as an argument.
      2. Request parser for updating user profile and add each argument onto user_update_args using ad_argument method.
      3. @jwt_required() decorator is used to check for the valid JWT.
      4. Use PUT method for the API endpoint and get the user_id associated with the token by get_jwt_identity() function.
      5. Pass the user_id to our database model to get the user details
      6. Update the fields provided by the user and in case if the user updated email, check with the alfready registered emails in our database.
      7. if the given email matches with any previosuly registered emails, pass the message, "Email already in use".
      8. commit the updates fields onto our database and return "User profile updated successfully!"

 Tested the APIs in Postman 

 Postman Url Link: https://web.postman.co/workspace/a092db62-373d-41d1-89a4-2f7a67aa1017/collection/38136116-89c0f27a-ace1-4d70-bf5c-5977c10764aa
      
      
      
