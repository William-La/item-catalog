# Item Catalog Project

Item catalog is a web application that allows users to browse categories and items stored in a database. Authenticated users are able to post, edit, and delete items. Users are authenticated through a third-party authentication service. The theme used for the sample database is a movie catalog website, where users can submit movie reviews. This project is a requirement for Udacity's Full Stack Web Developer Nanodegree.

Required Software
-----------------

It is recommended to run this project in a linux virtual machine. The tools [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and [Vagrant](https://www.vagrantup.com/) allow us to host the virtual machine. For information regarding their installation, please reference [this Udacity github page](https://github.com/udacity/fullstack-nanodegree-vm).

Set Up
------

Usage
-----

Program Design
--------------

This web app utilizes the Flask web framework to create a front end which is responsive to users' requests and inputs. It also utilizes SQLalchemy to interact with the web app's backend. User authentication occurs through Google's OAuth API, which allows users to interact with the site with one of their existing accounts. 