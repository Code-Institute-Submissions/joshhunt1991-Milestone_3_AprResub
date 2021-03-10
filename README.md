![VG Review logo](readmelinks/logo.png)

# VG Reviews

# Description

VG review is a web application that allows users to store and view reviews for video games from a variety of platforms. The web app is connected to RAWG video game API allowing the user to choose the correct image to validate their game and then automatically returning the release date of that game to be displayed in the review. The User has a personal review page to view their own reviews and a public review page to view other user reviews.

# Deployment and Demo

It has been deployed to heroku and can be viewed [here](https://vg-review.herokuapp.com/).

The deployment process is shown below:

[- first in the CLI you must create a requirements.txt file to tell heroku which applications and dependencies are neededclea](/readmelinks/requirements.png) <br/>
[- Next use the echo command to create a procfile, this tells heroku which file runs the app](/readmelinks/procfile.png) <br/>
[- login to heroku and on the dashboard click create a new app](/readmelinks/create.png) <br/>
[- name your app and select the region, the standard syntax is lower case letters seperated by dashes. Click create app.](/readmelinks/name-app.png) <br/>
[- to connect the app to heroku I used automatic deployment from github. First go to the deploy tab](/readmelinks/deploy-tab.png) <br/>
[- scroll down, select github as the deployment method, search for your repo name in the "app connected to github" section and once it finds it click connect. ](/readmelinks/connect.png) <br/>
[- before you click enable automatic deploys you need to set the config vars so that heroku can access the hidden environment variables in your env.py file. Go to settings and scroll down, reveal config vars and fill in the necessary variables](/readmelinks/config.png) <br/>
[- now you can enable automatic deploys which will build your app](/readmelinks/auto.png) <br/>

- This will generate a live page for your app.

# User experience

## Goals and Aims

This project is a spiritual successor to my previous milestone project, VG Search, which can be found on my github. The goal is to expand on the concept showcased in the previous project and focus on the functionality of CRUD to allow the user to create posts, read other peoples posts, update their own posts when necessary and delete their own posts.

## User Stories

-   As a user, I want to be able to post reviews in a simple, straightforward and self explanatory way.
-   As a gamer, I want to be able to search for games by name to see other users opinions on that game
-   As a user, I want to be able to access all my previous reviews in a single location to allow myself to easily update or delete reviews
-   As a user, I want my reviews to display an image and possibly other information relevant to the game reviewed for aesthetic and informative purposes
-   As a user, I want to be able to understand the purpose of the site through the use of an "about" page and clear headers and where necessary instructional information.
-   As a user, I want to reviews to be displayed in an aesthetically pleasing manner
-   As a user, I want my app to be fully responsive to all viewport sizes so I can access my profile on mobiles, tablets, laptops and desktop computers

## Wireframes

Using these goals as a guide I drew up some wireframes as an initial design using MS paint.

[- home page](/readmelinks/Landing-page.png) <br/>
[- registration page](/readmelinks/sign-up.png) <br/>
[- log in page](/readmelinks/log-in.png) <br/>
[- logged in home page](/readmelinks/logged-in.png) <br/>
[- about page](/readmelinks/about-page.png) <br/>
[- game reviews page](/readmelinks/reviews.png) <br/>
[- review form page](/readmelinks/review.png) <br/>
[- reviewed game page](/readmelinks/reviewed-game.png) <br/>
[- failed search page](/readmelinks/search-failed.png) <br/>
[- successful search page](/readmelinks/search-success.png) <br/>

The final design naturally evolved from this in the following ways:

-   The search bar was moved from the top of the displayed reviews page onto its own seperate page to prevent clashes with flask paginate.
-   The reviews were displayed in single file and much larger than the wireframe as I preferred the aesthetic and larger images, therefore less results were displayed per page.
-   The image on the landing page was displayed differently as it didn't look right displayed in a circle as previously planned.
-   The "reviewed game" page was deemed unneccesary as no benefit was achieved by having this option

Here is the final list of pages after these changes

- landing page: Contains a welcome message with a little information about the purpose of the site, a nice image for aesthetics and a call to action for the user to sign up.
- About page: Contains a write up about the purpose of the website and three images to convey the theme and give examples of gaming platforms.
- The login page: Contains a form to allow existing users to log in.
- The registration page: Contains a form to allow new users to sign up.
- The review page: Once logged in the user has access to the review page which displays all the previously created reviews from all users in paginated format using flask paginate
- The profile review page: Once logged in the user has access to the profile review page which displays all the previously created reviews the current user in paginated format using flask paginate
- The add game page: From the review page and the profile review page the user has the option to add a review which will take them to the add game page which displays a form allowing the user to submit a review
- The game images page: Once the review is written and submit is clicked the user is redirected to a page populated by images that should be relevant to that game, the user is prompted to select the correct image and that image is displayed on the review
- The edit game page: Users can edit their own reviews using the edit button and will be taken the a form which is populated by the previously written review
- The search page: The search page contains a search bar that displays relevant games when they are available
- The page not found page: Displays a 404 error when an address is used that doesn't exist.


# Visual Identity

- [Canva](https://www.looka.com/) for the logo design.

- The color scheme was a continuation of my previous VG Search project. That project was designed around space invaders and vintage gaming so to continue that theme I went with black backgrounds and light blue colours to still get the same sort of contrast but I also tried to implement a softer look with different shades of grey.

# Typography

I used Teko as my standard font across the site as I think its clear and easy to read while also fitting well with the theme

# Features

## Registration

-   New users can register for an account by crerating a username and password
-   For the account to be created, all fields must pass validation:
    -   Username must be less than 30 characters
    -   Password can use any characters but must be between 6 and 15 characters in length

## Log in

-   Existing users can log in via their username and password
-   All fields must pass validation
-   While logged in users can edit and delete their reviews
-   Users can log out and close the session

## Post reviews

-   Users can post reviews using the add review link
-   The following fields are required

    -   The name of the review
    -   The rating between 1 and 5 stars
    -   The review text
    
-   Once these are filled, on submit the user is provided with relevant images if available and once selected this image will be displayed in the review.

## Edit and Delete

-   Reviews can be edited or deleted
-   Only reviews written by the current session user can be deleted unless logged in as admin

# Security

The following security measures were implemented

-   The user's password is hashed this ensures the password can't be found in the code.
-   Data validation was used to ensure that only valid data is able to be submitted. The solution I used here was inspired by another code institute students project which can be found here: https://github.com/LukeGarnham/Wired-and-Wiser-MS3

# Validation and code clean up

- I used W3C mark up validation service to validate my code [W3C Markup Validator](https://validator.w3.org/) <br/>
- I used freeformatter.com's HTML formatter to format all my code [freeformatter HTML Formatter](https://www.freeformatter.com/html-formatter.html) <br/>
- I used freeformatter.com's CSS beautifier to beautify all my CSS [freeformatter CSS Beautifier](https://www.freeformatter.com/css-beautifier.html) <br/>

[- image of form validation code](/readmelinks/s13.png) <br/>

# Testing

A seperate file covering testing can be found [here](TESTING.md)

# Bugs and issues

- *SOLVED* Once pagination was implemented it broke my search functionality. Originally the search bar was on the review page, I had been thinking the search may be better on its own seperate page and this bug pushed me to implement that.

- *SOLVED* Pagination was missing the first 3 results from the database which I later found was caused by a mistake in the value of the offset variable

# Features to be implemented in future updates

-   The search pages results will need to be paginated once the app grows in number of reviews.
-   A password recovery system.
-   A password confirmation to ensure that no typos are made when signing up.

# Technologies Used

-   HTML
-   CSS
-   Materialize CSS
-   JavaScript / JQuery
-   Python
-   Flask
-   Flask paginate
-   Font awesome
-   Requests

# Media

I have used different resources for the API images and my logo, I'll list all below:

- [Looka](https://www.looka.com/) for the logo design
- [Pexels](https://unsplash.com/s/photos/video-game) for the landing page image and the three images on the about page.
    https://www.pexels.com/photo/technology-keyboard-lighting-candy-3165335/  (landing page image)
    https://www.pexels.com/photo/xbox-one-controller-beside-three-xbox-one-cases-139038/ (xbox image)
    https://www.pexels.com/photo/black-dualshock-4-2885014/  (ps4 controller)
    https://www.pexels.com/photo/close-up-photo-of-gaming-keyboard-2115257/ (pc keyboard)
- [Font Awesome](https://fontawesome.com/6?next=%2Fstart) for the magnifying glass on the search bar, controller on the sign up button, the social media links and the icons on all the forms
- [Rapid API](https://rapidapi.com/accujazz/api/rawg-video-games-database/) I used the RawG video games database API which is hosted on Rapid API.
- [favicon.io](https://favicon.io/favicon-generator/) for the favicon

# Testing

Website has been tested using GTmetrix see results below:

[- GT Metrix test results screenshot](/readmelinks/gtmetrix.png) <br/>

- [full test results](https://gtmetrix.com/reports/vg-review.herokuapp.com/pNiXfCRh/)

The page has a fully loaded time of 2.5 seconds which can be improved in further updates by resizing the images I have used to closer to their final size as suggested in the summary.


I also validated my code using the following resources:

**HTML** - All pages were successfully checked with [W3C HTML Validator](https://validator.w3.org/).

**CSS** - CSS validation was performed with W3C's [Jigsaw Validator](https://jigsaw.w3.org/css-validator/) which returned no errors.

**Python** - All Python code was checked with the [PEP8 online validator](http://pep8online.com/).

# Thanks to

- My Mentor, Felipe Alarcon, who has been excellent from the start and a massive part of my continued development as a coder
- The code institute tutor team who have got me through every technical difficulty that was too much to figure out on my own.
- Font awesome community for developing this great resource
- Materialize css developers for the great resource and documentation
- Python developers for designing and maintaining my favourite coding language so far
- Looka for the great and easy to use log design service
- Rapid API and RawG video games database for the impressive database of video games and information and the well documented platform.

# License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) license.

Copyright 2021 Joshua Connor Hunt.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.