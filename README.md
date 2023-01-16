# Jotted
#### Video Demo: <https://youtu.be/VDIn7vtJk8g>

#### Description: 

Jotted is a list or a notes maker website which is powered by a strong flask python backend running in a properly configured application factory that remembers a users jots (lists, text, plans, tables, sheets,code, images and embedded video, links etc.).  
It helps keep track of things you want to remember in a customisable way. Jotted can keep track of user's edits, delete or update them and move recently edited or updated entries to the top with a date and time stamp.
To make this possible, I have used a self hosted version of TinyMce, an open source rich text editor as a way for users to improve formatting of their jots.( includes alignment, fonts, formats, colours etc. ). You have the ability to add links, images, embedded videos , do wordcounts, insert date time, find and replace all from inside the editor and much more.  You can also preview notes, fullscreen them or print your notes through the editor.

<br>

## Run this application locally on your machine
1. Make sure you have [python3](https://www.python.org/) with `pip` installed on your machine
2. Install [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/index.html) using the command: `pip install waitress`
    - Waitress is the production-quality pure-Python WSGI server used to run this application
3. Download my application's distribution file from [here](https://github.com/PrachiNayakCS/jotted/blob/main/dist/flaskr-1.0.0-py3-none-any.whl) and open the folder containing the downloaded file in powershell or your terminal 
   - **OR** you can also clone/download this project's repository from my GitHub account: https://github.com/PrachiNayakCS/jotted.git and change directory into this projects `dist` folder by using the command `cd project/Jotted/dist`
4. Once you're in the folder containing the application's distribution file called `flaskr-1.0.0-py3-none-any.whl`:
   - run `pip install flaskr-1.0.0-py3-none-any.whl` - this step will ensure your machine has all the dependencies it needs to run the application
   - if running this application for the first time, run `flask --app flaskr init-db` - this will initialise a local SQLite3 database to be used by the application
5. Run the following command, to start the application server locally: `waitress-serve --host localhost --port 8080 --call 'flaskr:create_app'`
6. Open your browser and go to [http://localhost:8080/](http://localhost:8080/) to open the application and start using it!

> **NOTE:** These steps donot set up a local development environment to develop or change this application. They are a simple way to run this application as built, quickly on your machine, to check out all its features

<br>

## Technologies and frameworks I have learned and used while doing this project:
- [VSCode](https://code.visualstudio.com/) desktop to understand how to setup a remote project and Git to commit and push changes to Git Hub
- [Tailwind CSS](https://tailwindcss.com/) to improve the design elements to keep the website responsive and mobile optimised. I started out with bootstrap but changed my mind half way through as tailwind blocks served my design better
- [Flask](https://palletsprojects.com/p/flask/) WSGI web app framework(with Werkzeug and Jinja) and Python to write my code
- [SQLite](https://www.sqlite.org/index.html) as the database
- [Wheel](https://peps.python.org/pep-0491/) to create a distribution file 
- [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/) server to deploy to production

<br>

#### The Code 
The python files that help control and execute this application are in the `flaskr` folder. Rather than registering views and other code directly with the application, they are registered with a blueprint. Then the blueprint is registered with the application when it is available in the factory function.

My app has two blueprints, one for authentication functions and one for the blog posts functions.  

<br>

## PYTHON FILES

----------------------------------

<br>

**__init__.py :**

This is the main python file which creates the app and controls all the other blueprint python files. It imports and registers the blueprints from the factory using `app.register_blueprint()` for both auth.py and blog.py blueprints and uses them to configure the app . It also imports the database initialisation and closing function from the db.py file.


### The Blueprint files auth.py and blog.py

**auth.py :**


This python file imports a number of functions to make it possible to have users register and login by checking their credentials and creating sessions onto rendering the right templates based on whether the authorisation was succesful. It checks the login and register routes and the database to make sure everything is right before a user is allowed through to their account. ( imported libraries from flask: `Blueprint`, flash, g, redirect, render_template, request, session, `url_for`) . It also imports functools library and with method wraps uses the wrapper function of the decorator and copies the attributes of the passed function in the decorator. As a result, it preserves passed function information. This way I created a login_required authentication in other views/routes and could check it for each view it’s applied to. This blueprint also contains logout function which removes the user id from the session so that load_logged_in_user won’t load a user on subsequent requests. 

The two views inside auth are register, login:

<br>

1. #### **Register route:**
 
<br>

- When user visits the /auth/register URL, the register view will return HTML with a form for them to fill out. On submit, it will validate their input and either show the form again with an error message or create the new user and go to the login page.
- @bp.route:  When Flask receives a request to /auth/register, it will call the register view and use the return value as the response. If the user submitted the form, request.method will be 'POST'. In this case, start validating the input. Validate that username and password are not empty. If validation succeeds, insert the new user data into the database.
- For security, `generate_password_hash()` is used to securely hash the password, and that hash is stored. `db.commit()` needs to be called afterwards to save the changes. 
- An `sqlite3.IntegrityError` will occur if the username already exists, which should be shown to the user as another validation error.
- After storing the user, they are redirected to the login page. `url_for()` generates the URL for the login view based on its name. `redirect()` generates a redirect response to the generated URL.
- If validation fails, the error is shown to the `user. flash()` stores messages that can be retrieved when rendering the template.

<br>

2. #### **Login route:** 

<br>

- The user is queried first and stored in a variable for later use. fetchone() returns one row from the query. If the query returned no results, it returns None.
- `check_password_hash()` hashes the submitted password in the same way as the stored hash and securely compares them. If they match, the password is valid.
- session is a dict that stores data across requests. When validation succeeds, the user’s id is stored in a new session. The data is stored in a cookie that is sent to the browser, and the browser then sends it back with subsequent requests. Flask securely signs the data so that it can’t be tampered with. Now that the user’s id is stored in the session, it will be available on subsequent requests. At the beginning of each request, if a user is logged in their information should be loaded and made available to other views.
- `bp.before_app_request()` registers a function that runs before the view function, no matter what URL is requested. load_logged_in_user checks if a user id is stored in the session and gets that user’s data from the database, storing it on g.user, which lasts for the length of the request. If there is no user id, or if the id doesn’t exist, g.user will be None. To log out, you need to remove the user id from the session. Then load_logged_in_user won’t load a user on subsequent requests.


<br>


**blog.py :**

Once the user is logged in . This blueprint is used. It first imports in the login_required function from the auth.py file. So that it can be attached under every route once the user has been logged in. Creating, editing, and deleting blog posts will require a user to be logged in. . Basically so that these routes only load if users are logged in . 

- The index view will show all of the posts, most recent first. A JOIN is used so that the author information from the user table is available in the result. 
- The create view works the same as the auth register view. Either the form is displayed, or the posted data is validated and the post is added to the database or an error is shown.
- The update function takes an argument, id. That corresponds to the <int:id> in the route. To generate a URL to the update page, `url_for()` needs to be passed the id so it knows what to fill in: `url_for('blog.update', id=post['id'])`. 
- The delete view doesn’t have its own template, the delete button is part of update.html and posts to the /<id>/delete URL. Since there is no template, it will only handle the POST method and then redirect to the index view.

--------------------------


## STATIC

I have used tailwind to build my css and use watch to change and rebuild the css template everytime I make changes to the html files.( `$ ./tailwindcss -i ./flaskr/static/input.css -o ./flaskr/static/output.css --watch`). These two css files are inside my static folder. The static folder also includes my Tinymce editor js file and config folder

<br>

--------------

## TEMPLATES

The templates used in the routes/views are all controlled by the base.html template and jinja has been used to extend this base template to have additional templating to override specific sections. 

- base.html

  - `g` is automatically available in templates. Based on if `g.user` is set (from `load_logged_in_user`), either the username and a log out link are displayed, or links to register and log in are displayed. `url_for()` is also automatically available, and is used to generate URLs to views instead of writing them out manually. After the page title, and before the content, the template loops over each message returned by `get_flashed_messages()`. You used flash() in the views to show error messages, and this is the code that will display them.

- `login.html` and `register.html` are inside the auth folder in templates. Both use simple tailwind style forms with id and name fields matching the routes in python file `auth.py`

- `index.html`, `create.html` and `update.html` are inside the blog folder in templates. These also use simple tailwind style forms with id's, names matching the routes in python file `blog.py`

<br>

--------------------
## Making the project installable

`setup.py` and `MANIFEST.in` include instructions to make the project installable in other environments.

<p>

**Deploy to production**

To make it possible to deploy I installed wheel via pip and ran `$ python setup.py bdist_wheel` to create a distribution file.

I copied the whl file from the dist folder to another machine, set up a new virtualenv, then install the file with pip to check that it works.

```
pip install flaskr-1.0.0-py3-none-any.whl 
flask --app flaskr init-db
```
> NOTE: when Flask detects that it’s installed (not in editable mode), it uses a different directory for the instance folder. You can find it at `venv/var/flaskr-instance` instead.

<p>

**Run with a production server**

I used waitress with the following commands

```
pip install waitress
waitress-serve --host localhost --port 80 --call 'flaskr:create_app'
```



