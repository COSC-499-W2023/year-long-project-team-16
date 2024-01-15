Fetching Data from the Login_detail database to the Settings page.

Binding of the user information into the settings page happens in the settings rout using Jinja2

@app.route('/settings.html')
@login_required # Ensure that the user is logged in
def settings_html():
user_id = current_user.get_id()
user = users_collection.find_one({"\_id": ObjectId(user_id)})
if user:

        return render_template('settings.html', user=user)
    else:
        flash("User not found.")
        return redirect(url_for('index'))

1. the user ID is fetched from the "current_user" which is from Flask-Login.
2. query is made to the collection on MongoDB using the "user_id"
3. if a user is found, render_template is called which is where Jinja2 is used to render settings.html
4. The 'user' object is passed to the template as a context variable.
5. jinja2 syntax to access the user's properties: {{ user.get('first_name', '') }}

---

client feed back:

- to make the 'change password' function fully functional
- add the difficulty level to the settings.

Password Function

- Have a form in HTML that sends POST requests to the '/change_password' route (FOLLOW THE SAME PATH TO CHANGE ACCOUNT SETTINGS)

  - user enters current, new, confirm password
  - figure out how to fetch the stored password from the database for the current user, it will be hashed.
  - I will have to use the same hashing algo used when storing the original password for the current password entered.
  - check if the hash of the entered current password matches the stored hash.
  - Provide clear error messages for texts that do not match.

- All forms should have the method of submission 'POST' in order to communicate the information chnaged by the user to the form.
- EXAMPLE : <form action="{{ url_for('change_password') }}" method="post"> || @app.route('/change_password', methods=['POST'])
- This must be done for ALL settings.

Minor changes:

- change the third settings option from "AI assitant" to "preferences" - Add notification settings - Add the difficulty level
- Add an avatar as the default profile picture.
