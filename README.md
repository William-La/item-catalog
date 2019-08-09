# Item Catalog Project

Item catalog is a web application that allows users to browse categories and items stored in a database. Authenticated users are able to post, edit, and delete items. Users are authenticated through a third-party authentication service. The theme used for the sample database is a movie catalog website, where users can submit movie reviews. This project is a requirement for Udacity's Full Stack Web Developer Nanodegree.

Required Software
-----------------

It is recommended to run this project in a linux virtual machine. The tools [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and [Vagrant](https://www.vagrantup.com/) allow us to host the virtual machine. For information regarding their installation, please reference the "Install VirtualBox" and "Install Vagrant" headers on [this Udacity github page](https://github.com/udacity/fullstack-nanodegree-vm). 

Set Up
------
## Repository and Virtual Machine
Clone, download, or fork this repository and create a copy of the repository on your local computer. To clone the repository, run the following line in your terminal (replace the placeholder directory name).

```terminal
git clone https://github.com/William-La/item-catalog.git <DIRECTORY-NAME-HERE>
```

After creating a local copy of the repository, `cd` into the directory and then `cd` into the Vagrant folder. Once in the vagrant directory, run the following to set up and start the virtual machine.

```terminal
vagrant up
```

Once the virtual machine is started, log into it with the following command.

```terminal
vagrant ssh
```

## Google OAuth2 Credentials
A Google API project and an OAuth 2.0 Client ID must be created to be able to run this project. To create a project, go to the [Google Developer API site](http://console.developers.google.com), click on "Select a project", and press the "NEW PROJECT" button. Once you've created and selected your new project, go to the "Credentials" tab on the same [Google Developer API site](http://console.developers.google.com) site. Go to the "OAuth consent screen" tab. Fill out the "Application Name" section, make sure there is a "Support email" select, and then press save at the bottom. 

To create an OAuth 2.0 client ID, go back to the "Credentials" tab, press "Create credentials", then select "OAuth client ID". For "Application type", select "Web application". Next, under "Authorized JavaScript origins" add 'http://localhost:8000' and under "Authorized redirect URIs" add 'http://localhost:8000/googleoauth'. After you've created the OAuth client ID, download the JSON file and rename it to 'client_secrets.json'. Include this file in the 'catalog' directory of the git repository.

## Database
Once you're in the virtual machine (after running the `vagrant ssh` command above), `cd` into the catalog directory by running the following.

```terminal
cd /vagrant/catalog
```

Next, initalize and fill up the database for the web app with the folowing command.

```terminal
python database_setup.py
python fill_database.py
```

Usage
-----

Program Design
--------------

This web app utilizes the Flask web framework to create a front end which is responsive to users' requests and inputs. It also utilizes SQLalchemy to interact with the web app's backend. User authentication occurs through Google's OAuth2 API, which allows users to interact with the site with one of their existing Google accounts. 