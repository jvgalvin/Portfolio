**Project**

This is an individual project that will focus on the object-oriented principles. Your project needs to implement object oriented principles and should be interactive so that the user can play around with it. The code base needs to be entirely composed of objects (at least 5 should be in your creation) and should be called from the command line as a .py file so it can be easily ported to to a production scenario.
Some examples:  A popular board or card game  a flower shop (you create and manage inventory, a simple cash register, etc)  An adventure game where characters can do things like 1) explore a world 2) trade with other characters. Coding some element of chance into the world has made these even more interesting.  Something relating to your everyday work, maybe some process you would like to model or code up

**Requirements & Limits**

You should aim for around 300 to 500 lines of code. You will not be graded on the number of lines of code you write nor will this be a comparison of projects implemented by your peers. For example, a project with 500 lines of code is not guaranteed to do better than a project with 300 lines of code. As we've seen, it's not necessarily the number of lines, it's the value in those lines. Being concise is a good thing and if you're at all worried that you're not going to hit that soft requirement please let us know.
  * This project must be composed entirely of objects, with only scripting outside of objects when absolutely necessary
  * This project must not exceed 750 lines of code.
  * For example, if you have a text game you can put the text in a separate file.
  * The line count requirement does not include whitespace or comments (please include both to make your code readable).
  * Your code should be sufficiently complex to require at least 5 separate classes (but are not likely to need more than 10 classes).
  * The objects should be different levels of complexity, for example some may be basic containers and others should manage those containers (i.e. a menu-serving object and/or a game-play object) as well as demonstrating various flow control and data types.
  * The project will be run from the command line as a .py file.
  * The project needs to have a user-interface and be interactive with a user.
  * The project needs to do some user error checking as well as have a help 'screen' or printed instructions for the user.
  * All code needs to be well commented with both comments and docstrings.
  * Without specific permission, you may not use anything outside of the standard Anaconda-installed libraries.
  * Please include all references that you used to build out your application.
  * While it is acceptable and even desirable to take inspiration and learn specific syntax from previous projects and stackoverflow code, this code base must be your own work.

**Context**  
  * Cooking is fun, can be healthy, and is highly social. Figuring out what to cook, however, is not (at least for me).
  * This program has 4 different modes to speed up the menu selection process:
    * “GUIDED” - the program will guide the user through selection of a cocktail, appetizer, main course, and dessert based on the user’s preferences
    * “RANDOM” - the program will choose a cocktail, appetizer, main course, and dessert at random
    * “MOOD” - the program asks the user to enter a mood (casual or sophisticated) and selects a cocktail, appetizer, main course, and dessert which each match that mood
    * “OCCASION” - the program asks the user to enter an occasion (dinner with friends, date night, weeknight, or dinner party) and selects a cocktail, appetizer, main course, and dessert which each match that occasion

**Data**

  * Although the recipes are not my own, they are some of my favorites.
  * I personally assembled and structured the 4 csv files

**Instructions for Using the Menu Builder**

  * Download the 4 csv files (Cocktail, Appetizer, MainCourse, and Dessert) to a directory
  * Download the menu.py file and place it in the same directory as the 4 csv files
  * From the Terminal window, run ‘python menu.py’ or ‘python3 menu.py’
  * The program will automatically open 4 windows in your default browser after it runs to bring you to the webpages with the recipe and directions for each dish on your menu

