# Item Catalog Project

Item catalog is a web application that allows users to browse categories and items stored in a database. Authenticated users are able to post, edit, and delete items. Users are authenticated through a third-party authentication service. The theme used for the sample database is a movie catalog website, where users can submit movie reviews. 


Required Software
-----------------

It is recommended to run this project in a linux virtual machine. The tools [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and [Vagrant](https://www.vagrantup.com/) allow us to host the virtual machine. For information regarding their installation, please reference the "Install VirtualBox" and "Install Vagrant" headers on [this Udacity github page](https://github.com/udacity/fullstack-nanodegree-vm). 


Set Up
------
### Repository and Virtual Machine
Clone, download, or fork this repository and create a copy of the repository on your local computer. To clone the repository, run the following line in your terminal (replace the placeholder directory name).

```terminal
$ git clone https://github.com/William-La/item-catalog.git <DIRECTORY-NAME-HERE>
```

After creating a local copy of the repository, `cd` into the directory and then `cd` into the "vagrant" folder. Once in the vagrant directory, run the following to set up and start the virtual machine. This may take a while the first time it is ran.

```terminal
$ vagrant up
```

Once the virtual machine is started, log into it with the following command.

```terminal
$ vagrant ssh
```


### Download Requirements
After you've logged into the virtual machine, there are a few requirements that must be installed. These requirements are listed in the `requirements.txt` file, and can be installed by running the following code snipet while in your linux virtual machine.

```terminal
$ sudo pip install --upgrade -r requirements.txt
```


### Google OAuth2 Credentials
A Google API project and an OAuth 2.0 Client ID must be created to be able to run this project. To create a project, go to the [Google Developer API site](http://console.developers.google.com), click on "Select a project", and press the "NEW PROJECT" button. Once you've created and selected your new project, go to the "Credentials" tab on the same [Google Developer API site](http://console.developers.google.com) site. Go to the "OAuth consent screen" tab. Fill out the "Application Name" section, make sure there is a "Support email" selected, and then press save at the bottom. 

To create an OAuth 2.0 client ID, go back to the "Credentials" tab, press "Create credentials", then select "OAuth client ID". For "Application type", select "Web application". Next, under "Authorized JavaScript origins" add `http://localhost:8000'` and under "Authorized redirect URIs" add `http://localhost:8000/googleoauth`. After you've created the OAuth client ID, download the JSON file and rename it to `client_secrets.json`. Include this file in the catalog directory of the git repository.

### Database
Once you're in the virtual machine (after running the `vagrant ssh` command above), `cd` into the catalog directory by running the following.

```terminal
$ cd /vagrant/catalog
```

Next, initalize and fill up the database for the web app with the folowing command.

```terminal
$ python database_setup.py
$ python fill_database.py
```


Usage
-----

To start the web app, run the following line while in the catalog directory of the virtual machine.

```terminal
$ python application.py
```

Once it is up and running, go to `http://localhost:8000` in your web browser. You should be on the landing page of the web application. You can then browse through the site to see the various entries present in the database.

To be able to create, edit, or delete items, you must log in through the Google Sign-in button. Once logged in, you will be able to see buttons which allow you to add, edit, and delete items as well as a sign out button. 

### JSON API Endpoints

While the project is running, the user can access three different JSON endpoints. Going to `http://localhost:8000/json` allows access to the catalog's entire JSON file.

To access the JSON endpoint for a specific category, the user simply needs to navigate to the category's page on the web app and add `/json` to the end of the URL. For example, to access the JSON endpoint for the "Action" category, the user can first navigate to the "Action" category by clicking on "Action" in the sidebar menu or going to `http://localhost:8000/catalog/Action`. Then, they can add `/json` to the end of the URL, making it `http://localhost:8000/catalog/Action/json`. 

Accessing the JSON endpoint for a specific item is fairly similar to the category endpoints. The user can navigate to the item's page on the web app and add `/json` to the end of the URL. For example, to access the JSON endpoint for the item "Abu", the user can first navigate to the "Fantasy" category and then click on the "Abu" item, taking them to `http://localhost:8000/catalog/Fantasy/Abu`. After adding `/json` to make the URL `http://localhost:8000/catalog/Fantasy/Abu/json`, they will see the JSON configuration. 

If the category name or item title has spaces in it, such as "Science Fiction", the spaces will appear as `%20` in the URL, like `http://localhost:8000/catalog/Science%20Fiction`. The JSON endpoint will still appear if `/json` is added to the end of these URLs. 


Program Design
--------------

This web app utilizes the Flask web framework to create a front end which is responsive to users' requests and inputs. It also utilizes SQLalchemy to interact with the web app's backend. User authentication occurs through Google's OAuth2 API, which allows users to interact with the site with one of their existing Google accounts. 


Points to Consider
------------------

This web app is very much a development app. Factors that should be changed if moving to a production site include the creating a secure Flask key, removing debug mode, and including more forms of third party authentication.


Acknowledgements
----------------
[Udacity](https://www.udacity.com/)

My Udacity Mentor, Tim Nelson

The Full Stack Web Developer Nanodegree Community

[Google OAuth Documentation](https://developers.google.com/identity/sign-in/web/sign-in)

[Nicolas Hanout](https://github.com/nicolash92/) for assistance with Google OAuth
