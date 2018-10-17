# innovacer-platform

The given project will save the community from all the spoilers of their favourite tv series hovering around.

The main aim of the project is to send an email to the user that contains the information about the Air Date of episode of the TV series a user likes ( air date = Date on which the episode will be broadcasted)

Input :
  User email
  List of Tv series user like

 <p align="center">
  <img src="home/jainish/Pictures/INPUT_INNOVACER.png" width="350" title="hover text">
</p>
 

Using OMDB API the program will get the IMDB  ID of user's favourite TV series.

The IMDB ID is scrapped from Json file :

<p>
    <img src="home/jainish/Pictures/omdb.png" width="350" title="hover text">
  </p>


Information about the TV series is scrapped from imdb page of the series using the ID :

<p>
  <img src="home/jainish/Pictures/imdb1.png" width="350" title="hover text">
</p>
 
 
 
 <p>
  <img src="home/jainish/Pictures/imdb2.png" width="350" title="hover text">
</p>
 
 

The information is then stored in a string and using SMTP protocol all this information is sent to the user's email id:

 <p>
  <img src="home/jainish/Pictures/mail.png" width="350" title="hover text">
</p>



The deatils of the user and the his/her favourite tv series is stored in local mysql database 

 <p>
  <img src="home/jainish/Pictures/DB.png" width="350" title="hover text">
</p>



 
