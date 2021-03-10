![VG Review logo](readmelinks/logo.png)

# VG Reviews Testing

## Manual Testing

Manual testing for this project was performed continually throughout the development process as new features were implemeneted to ensure that features worked and that they didn't have unintended consequences for other previously implemented features. For the purposes of this testing document I am going to perform my manual testing using Heroku, working through the app in a logical order from the landing page.

### Landing page

[- first I tested the navigation links returning to the landing page each time to ensure that all links work from that page.] <br/>
[- Then I tried all of the social media links to ensure that they link to the relevant websites and also that they open in a new window.] <br/>
[- Next I clicked the call to action button to navigate to the registration page] <br/>

### Registration page

[- To get the easy one out of the way first I tested the redirect to the login page button at the bottom of the page.] (/readmelinks/redirect.png)<br/>
[- Then I tried to submit the form with no fields filled in to ensure that it threw up an error message.] (/readmelinks/blank.png) <br/>
[- Then I tried to register using illegal characters in my username to ensure that the validation was functioning .] (/readmelinks/illegal.png) <br/>
[- From this testing procedure I discovered that I wasn't allowing numbers in my username validation so I went back and changed that and tested it here.] (/readmelinks/register.png) <br/>
[- I then checked that the username and hashed out password was posted to mongoDB, no screenshot included due to security concerns .] <br/>
[- Next I tried to register with a username that I know already exists to ensure that it would be caught in my validation .] (/readmelinks/already-exists.png) <br/>

### Login page

[- Again getting the easy one out of the way first I tested the redirect to the register page button at the bottom of the page.] (/readmelinks/redirect-2.png)<br/>
[- As previously I tried to submit the form with no fields filled in to ensure that it threw up an error message.] (/readmelinks/blank-2.png) <br/>
[- Next I tried to log in with a username I know doesn't exist and got an error message as expected.] (/readmelinks/noexist.png) <br/>
[- Finally I logged in as Admin to test the functionality of the login form and to begin further testing elsewhere through the site.] <br/>

### Home page

[- Logging in redirected me to the home page as expected and as we can see the welcome message displays the username as expected.] (/readmelinks/loggedadmin.png)<br/>
[- We can also see that the recent review carousel is functioning as intended] <br/>
[- Next I clicked the button to view reviews written by the user and was redirected as expected ] (/readmelinks/profile-reviews.png) <br/>

### Profile review page

[- Reviews are displaying correctly and are paginated] <br/>
[- I cross checked the displayed reviews with the mongoDB entries to ensure that they are all their and are in the correct order (newest first)] <br/>
[- I checked that the add review button redirects the user to the add review form, I left testing this for now as it is also linked to on the review page] (/readmelinks/addrev.png) <br/>


### About page

[- Not much to check here, everything displays as expected <br/>

### Reviews page

[- Reviews are displaying correctly and are paginated] <br/>
[- Again, I cross checked the displayed reviews with the mongoDB entries to ensure that they are all their and are in the correct order (newest first)] <br/>
[- I checked that the add review button redirects the user to the add review form <br/>

### add review page

[- First I tried to submit a blank form to ensure that the validation is working for that] (/readmelinks/add-blank.png) <br/>
[- As before I realised when testing my validation that I wasn't allowing numbers to be used in the game name which would obviously cause issues, I fixed this and tested it and was correctly redirected to the game images page] <br/>
[- I then posted multiple reviews testing all the ratings radio buttons to ensure that the stars display correctly on the reviews] <br/>
[- Next I tested the review text area, I exceeded the character limit and also put less than the necessary amount to test validation] (/readmelinks/too-short.png) <br/>
[- I filled the form out with gibberish and when no games were found the redirect to the review page and the flash message displayed as expected] (/readmelinks/nogames.png)<br/>
[- Finally I filled the form out correctly with a game that I know exists and returned the game images page] <br/>

### add image page

[- In the previous section I filled out a review, this review was for call of duty and returned images] (/readmelinks/image-page.png) <br/>
[- I then selected the correct image and it posted as required] (/readmelinks/posted.png) <br/>

### edit functionality

[- In the previous section I filled out a review, this review was for call of duty and returned images] (/readmelinks/image-page.png) <br/>
[- I went through the same tests as I did with the add game form and all worked as expected] <br/>

### Delete functionality

[- I deleted the call of Duty review to ensure that delete works as required. I also logged in as another user to make sure that the delete option doesnn't appear for the other user.] <br/>

### Pagination

[-I scrolled through the pages, added and deleted reviews to increase and decrease the number of pages and they worked as intended.] <br/>

### Search Page

[-First I searched a gibberish string to make sure that my validation worked correctly.] (/readmelinks/no-search.png) <br/>
[-Then I searched a game I knew exists to make sure that my search function worked correctly, it returned the results as intended.] <br/>
[-To wrap up the testing of the search page I clicked the reset button to test that the page would be returned to its initial form. I also tested that the link for adding a review worked correctly] <br/>

### Pagination

[-I scrolled through the pages, added and deleted reviews to increase and decrease the number of pages and they worked as intended.] <br/>

### log out functionality

[-I clicked the log out navigation link to make sure that the session is exited.] <br/>

### Responsive design

Below are some images demonstrating the responsiveness of the webpage on different viewport sizes.

- Desktop sizes: <br/>
[- image of the homepage](/readmelinks/dhome.png) <br/>
[- image of the about page](/readmelinks/dabout.png) <br/>
[- image of how the forms look](/readmelinks/dforms.png) <br/>
[- image of logged in home page](/readmelinks/dlogged.png) <br/>
[- image of review slider](/readmelinks/dslider.png) <br/>
[- image of review page](/readmelinks/dreviews.png) <br/>

- Tablet sizes: <br/>
[- image of the homepage](/readmelinks/thome.png) <br/>
[- image of the about page](/readmelinks/tabout.png) <br/>
[- image of how the forms look](/readmelinks/tforms.png) <br/>
[- image of logged in home page](/readmelinks/tlogged.png) <br/>
[- image of review slider](/readmelinks/tslider.png) <br/>
[- image of review page](/readmelinks/treviews.png) <br/>

- Mobile sizes: <br/>
[- image of the homepage](/readmelinks/mhome.png) <br/>
[- image of the about page](/readmelinks/mabout.png) <br/>
[- image of how the forms look](/readmelinks/mforms.png) <br/>
[- image of logged in home page](/readmelinks/mlogged.png) <br/>
[- image of review slider](/readmelinks/mslider.png) <br/>
[- image of review page](/readmelinks/mreviews.png) <br/>


This wraps up the manual testing section.





