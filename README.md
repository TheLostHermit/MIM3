# MIM3
The prototype of a dedicated forum for entities addressing climate change to showcase their work while interacting with individuals interested in their cause.

## Running this Application
### Downloads Required
Python 3.9 was used to run this application but subsequent releases should be compatible. The following can be installed using python's preferred installer program (pip). It is recommended that these be installed in a python virtual environment rather than globally on your computer:
- django (4.1.5) : The web development framework required to run the site
- pillow (9.4.0) : used to serve static files in django
- django-crispy-forms (1.14.0) : used to style forms in django
- pytz (2022.7.1) : used to perform operations involving timezones

### Starting the Application on the Local Server
Once these have been installed on your computer/virtual environment and you have downloaded this repository you should be able to run the program as follows:
- navigate to the directory on the same level as manage.py
- run `python manage.py makemigrations`
- run `python manage.py migrate`
- run `python manage.py runserver`

## General Use of this Application
the ‘Home’ page of the web
application shows a feed of articles on current
or past local projects targeting climate change
mitigation. After registering or logging in, users
have access to other features of the website.
For individuals interested in
following or supporting such entities the
‘Dashboard’ page shows all the events
they have applied to take part in, as well
as their acceptance status.
Additionally registered
entities' members have an ‘Organization Dashboard’ page. They can post and edit articles, as well as view
and screen participants interested
in a posted event. They can also send short text messages to participants, as well as copy mailing lists for select groups. All members can ‘pin’ specific organisations they wish to
follow, as well as maintain profiles showing their
own information to others. Information on overall organizations have a dedicated page as well. 
All users are required to log in, in order to link their activities
on the website to the site’s database.

## Pages on this Application
The HTML pages of this web application can be found in `MIM3/Forum/templates/Forum` and are categorized based on function. Note that page names were created throughout development of the project, so they may not best describe them now.

### Layouts (`layouts`)
- `basic_layout.html`: The essential layout of an HTML template page. It is not used in the actual application but was used to quickly populate other layouts with html elements.
- `nonsidebar_layout.html`: The template for a page without the sidebar on it. The `signup` and `signin` pages extend this layout
- `sidebar_layout.html`: The template for a page with a sidebar, which contains links to other pages. It is used for all other pages on the site.

### Authentication Pages (`auth_pages`)
- `signin.html`: Page where the user signs in
- `signup.html`: Page where the user signs up

### Dashboard Pages (`dash_pages`)
- `org_posts.html`: Page where an organization member can manage the organization's posts
- `user_bids.html`: Page where a user can manage events which they have applied to

### Detail Pages (`detail_pages`)
- `org_details.html`: Page showing the details (name, icon, email, 'about' etc.) of an organization on the site
- `profile_details.html`: Page showing the details (username, first name, last name, birthday etc.) of users on the site

### Main Pages (`main_pages`)
- `index.html`: Page which renders the feed of posts in reverse chronological order, along with associated images and events.
- `pinned.html`: Page which lists all the organizations the user has pinned, with the option to view their details, posts from them exclusively or remove their pin.

### Message Pages (`message_pages`)
- `received_messages.html`: Renders all messages received by the user
- `sent_messages.html`: Renders all messages sent by the user
- `send_messages.html`: A view allowing an organization member to send a message

### Management Pages (`mngmt_pages`)
- `edit_profile_page.html`: Page allowing a user to edit their profile
- `mng_events.html`: Page allowing organization members to add, delete and edit events associated with a post
- `mng_post_imgs.html`: Page allowing organization members to add or delete images associated with a post
- `participant_list.html`: Page allowing organization members to change status of applications, as well as copy mailing lists of applicants

### Post Pages (`post_pages`)
- `change_post.html`: Page allowing organization members to change the title or body of a post
- `create_post.html`: Page allowing organization members to create a post with optionla associated images and events
- `view_post.html`: Page allowing users to view posts

### Utility Pages (`util_pages`)
- `delete_page.html`: Page used to confirm deletion of an object
- `error_page.html`: Page used to notify a user of an authentication or miscellaneous error
## Other Files of This Application
Generally, the function of each file not mentioned above is in accordance with the general functioning of a Django application. In order to assess which backend
function in `views.py` serves which HTML file, look for the path of the HTML file in the variable `HTML_PAGE` for function based views and `template_name` for class
based views. 

### Javascript
These are found in `MIM3/Forum/static/Forum/script`. With exception of the extension name, javascript files have the same name as the html files which they service. `util.js` is the only javascript file named
otherwise, and it serves all the web pages because it is inherited through the `layouts`. 
