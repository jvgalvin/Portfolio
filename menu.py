# Import necessary packages

import pandas as pd
import webbrowser

#--------------------------------
# Import Cocktail, Appetizer, MainCourse, and Dessert files as data frames

cocktail_df = pd.read_csv("./Cocktail.csv")
appetizer_df = pd.read_csv("./Appetizer.csv")
main_course_df = pd.read_csv("./MainCourse.csv")
dessert_df = pd.read_csv("./Dessert.csv")

#--------------------------------
# Format output for terminal window

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_colwidth', None)

#--------------------------------
# Define classes

class Cocktail:
	"""Representation of a Cocktail object which will be placed on the Menu

	Attributes
	----------
	name: str, name of the cocktail
	primary_liquor: str, base liquor of the cocktail
	flavor_profile: str, bold, bitter, sweet, citrusy
	how_served: str, up or on the rocks
	garnish: str, description of what garnishes the cocktail
	season_served: str, typical season in which the cocktail is enjoyed
	mood_pairing: str, casual or sophisticated
	occasion_pairing: str, events where the cocktail is appropriate
	directions_url: url link to direction for how to make the cocktail

	Methods
	----------
	init: initializes a Cocktail object
	get_user_input: guides the user through questions about preferences to select a cocktail
	str: formats printing the object
	repr: formats representation of the object
	"""


	def __init__(self, name, primary_liquor=None, flavor_profile=None, how_served=None, garnish=None, season_served=None, mood_pairing=None, occasion_pairing=None, directions_url=None):

		self.name = name
		self.primary_liquor = cocktail_df.loc[cocktail_df["name"] == self.name, "primary_liquor"].to_string(index=False)
		self.flavor_profile = cocktail_df.loc[cocktail_df["name"] == self.name, "flavor_profile"].to_string(index=False)
		self.how_served = cocktail_df.loc[cocktail_df["name"] == self.name, "how_served"].to_string(index=False)
		self.garnish = cocktail_df.loc[cocktail_df["name"] == self.name, "garnish"].to_string(index=False)
		self.season_served = cocktail_df.loc[cocktail_df["name"] == self.name, "season_served"].to_string(index=False)
		self.mood_pairing = cocktail_df.loc[cocktail_df["name"] == self.name, "mood_pairing"].to_string(index=False)
		self.occasion_pairing = cocktail_df.loc[cocktail_df["name"] == self.name, "occasion_pairing"].to_string(index=False)
		self.directions_url = cocktail_df.loc[cocktail_df["name"] == self.name, "directions_url"].to_string(index=False)


	@classmethod
	def get_user_input(self):
		"""Prompts the user for input about his or her preferences
		and returns the user's cocktail choice as a string"""
		primary_liquor_user = input("\nLet's start with a COCKTAIL. Which type of liquor would you like? \n \nYour options are bourbon, whisky, gin, rum, tequila, vodka, and cognac: ").lower().strip()
		print ("\n")
		
		#Error checking if the liquor entered does not match one available
		while cocktail_df["primary_liquor"].str.contains(primary_liquor_user).any() == False:
			print ("Invalid input - enter a valid liquor please \n")
			primary_liquor_user = input("\nWhich type of liquor would you like? \n \nYour options are bourbon, whisky, gin, rum, tequila, vodka, and cognac: ").lower().strip()
			print ("\n")
		flavor_profile_user = input("Are you feeling something bold, sweet, citrusy, or bitter? ").lower().strip()
		print ("\n")

		#Error checking if the flavor profile does not match one available or the liquor + flavor combo does not exist
		while cocktail_df["flavor_profile"].str.contains(flavor_profile_user).any() == False or cocktail_df[(cocktail_df["primary_liquor"].str.contains(primary_liquor_user)) & (cocktail_df["flavor_profile"].str.contains(flavor_profile_user))].empty == True:
			print ("You either entered an invalid input or that combination doesn't exist. \n")
			flavor_profile_user = input("Are you feeling something bold, sweet, citrusy, or bitter? ").lower().strip()
			print ("\n")
		new_df = cocktail_df[(cocktail_df["primary_liquor"].str.contains(primary_liquor_user)) & (cocktail_df["flavor_profile"].str.contains(flavor_profile_user))]
		
		#Print out what the available options are
		available_options = []
		for index, row in new_df.iterrows():
			print ("A " + row["name"].upper() + " is typically served " + row["how_served"] + " with a " + row["garnish"] + " in " + row["season_served"] + ".")
			print ("It suits " + row["mood_pairing"] + " moods " + "and can be served at " + row["occasion_pairing"] + ".")
			print ("\n")
			available_options.append(row["name"].upper())
		user_choice = input("\nSo, which cocktail do you want? Just type in the name as it appears above: ").upper().lstrip()
		
		#Error checking if the user choice does not match an available option
		while user_choice not in available_options:
			print ("\nSorry, that's not an available option.\nAgain, they are:\n")
			for option in available_options:
				print (option)
			user_choice = input("\nSo, which cocktail do you want? Just type in the name as it appears above: ").upper().lstrip()
		print (f"\nNice, you chose a {user_choice.upper()}!")
		return user_choice.title()

	def __str__(self):
		return cocktail_df.loc[cocktail_df["name"] == self.name, "name"].to_string(index=False).lstrip()

	def __repr__(self):
		return cocktail_df.loc[cocktail_df["name"] == self.name, "name"].to_string(index=False).lstrip()

class Appetizer:
	"""Representation of an Appetizer object which will be placed on the Menu

	Attributes
	----------
	name: str, name of the dish
	cuisine_type: str, origin or ethnicity associated with the dish
	health_rating: str, describes if the item is (low, medium, or high) healthy
	prep_effort: str, describes the level of effort (low, medium, high) required to cook the dish
	mood_pairing: str, casual or sophisticated
	occasion_pairing: str, events where the cocktail is appropriate
	directions_url: url link to direction for how to make the item

	Methods
	----------
	init: initializes an Appetizer object
	get_user_input: guides the user through questions about preferences to select an appetizer
	str: formats printing the object
	repr: formats representation of the object
	"""


	def __init__(self, name, cuisine_type=None, health_rating=None, prep_effort=None, mood_pairing=None, occasion_pairing=None, directions_url=None):

		self.name = name
		self.cuisine_type = appetizer_df.loc[appetizer_df["name"] == self.name, "cuisine_type"].to_string(index=False)
		self.health_rating = appetizer_df.loc[appetizer_df["name"] == self.name, "health_rating"].to_string(index=False)
		self.prep_effort = appetizer_df.loc[appetizer_df["name"] == self.name, "prep_effort"].to_string(index=False)
		self.mood_pairing = appetizer_df.loc[appetizer_df["name"] == self.name, "mood_pairing"].to_string(index=False)
		self.occasion_pairing = appetizer_df.loc[appetizer_df["name"] == self.name, "occasion_pairing"].to_string(index=False)
		self.directions_url = appetizer_df.loc[appetizer_df["name"] == self.name, "directions_url"].to_string(index=False)


	@classmethod
	def get_user_input(self):
		"""Prompts the user for input about his or her preferences
		and returns the user's appetizer choice as a string"""
		prep_effort_user = input("\nNext, let's pick an APPETIZER. How much effort do you want to exert? Choices are low, medium, or high: ").lower().strip()
		print ("\n")

		#Error checking if prep effort entered does not match one available
		while appetizer_df["prep_effort"].str.contains(prep_effort_user).any() == False:
			print ("Invalid input - enter a valid prep effort, please. \n")
			prep_effort_user = input("\nHow much effort do you want to exert? Choices are low, medium, or high: ").lower().strip()
			print ("\n")
		health_rating_user = input("\nHow healthy of a dish do you want to cook? Choices are low, medium, or high: ").lower().strip()
		print ("\n")

		#Error checking if health rating entered does not match one available or the effort + health combo does not exist
		while appetizer_df["health_rating"].str.contains(health_rating_user).any() == False or appetizer_df[(appetizer_df["prep_effort"].str.contains(prep_effort_user)) & (appetizer_df["health_rating"].str.contains(health_rating_user))].empty == True:
			print ("You either entered an invalid input or that combination doesn't exist. \n")
			health_rating_user = input("\nHow healthy of a dish do you want to cook? Choices are low, medium, or high: ").lower().strip()
			print ("\n")
		new_df = appetizer_df[(appetizer_df["prep_effort"].str.contains(prep_effort_user)) & (appetizer_df["health_rating"].str.contains(health_rating_user))]

		#Print out what the available options are
		available_options = []
		for index, row in new_df.iterrows():
			print (row["name"].upper() + " is a " + row["cuisine_type"].title() + " dish. Its health rating is " + row["health_rating"] + " and its prep effort is " + row["prep_effort"] + ".")
			print ("It suits " + row["mood_pairing"] + " moods " + "and can be served at " + row["occasion_pairing"] + ".")
			print ("\n")
			available_options.append(row["name"].upper())
		user_choice = input("\nSo, which appetizer do you want? Just type in the name as it appears above: ").upper().lstrip()

		#Error checking if the user choice does not match an available option
		while user_choice not in available_options:
			print ("\nSorry, that's not an available option.\nAgain, they are:\n")
			for option in available_options:
				print (option)
			user_choice = input("\nSo, which appetizer do you want? Just type in the name as it appears above: ").upper().lstrip()
		print (f"\nNice, you chose {user_choice.upper()}!")
		return user_choice.title()
	
	def __str__(self):
		return appetizer_df.loc[appetizer_df["name"] == self.name, "name"].to_string(index=False).lstrip()

	def __repr__(self):
		return appetizer_df.loc[appetizer_df["name"] == self.name, "name"].to_string(index=False).lstrip()

class MainCourse:
	"""Representation of a MainCourse object which will be placed on the Menu

	Attributes
	----------
	name: str, name of the dish
	cuisine_type: str, origin or ethnicity associated with the dish
	primary_protein: str, the primary protein (if not vegetarian) for the dish
	health_rating: str, describes if the item is (low, medium, or high) healthy
	prep_effort: str, describes the level of effort (low, medium, high) required to cook the dish
	mood_pairing: str, casual or sophisticated
	occasion_pairing: str, events where the cocktail is appropriate
	directions_url: url link to direction for how to make the item

	Methods
	----------
	init: initializes a MainCourse object
	get_user_input: guides the user through questions about preferences to select a MainCourse
	str: formats printing the object
	repr: formats representation of the object
	"""


	def __init__(self, name, cuisine_type=None, primary_protein=None, health_rating=None, prep_effort=None, mood_pairing=None, occasion_pairing=None, directions_url=None):

		self.name = name
		self.cuisine_type = main_course_df.loc[main_course_df["name"] == self.name, "cuisine_type"].to_string(index=False)
		self.primary_protein = main_course_df.loc[main_course_df["name"] == self.name, "primary_protein"].to_string(index=False)
		self.health_rating = main_course_df.loc[main_course_df["name"] == self.name, "health_rating"].to_string(index=False)
		self.prep_effort = main_course_df.loc[main_course_df["name"] == self.name, "prep_effort"].to_string(index=False)
		self.mood_pairing = main_course_df.loc[main_course_df["name"] == self.name, "mood_pairing"].to_string(index=False)
		self.occasion_pairing = main_course_df.loc[main_course_df["name"] == self.name, "occasion_pairing"].to_string(index=False)
		self.directions_url = main_course_df.loc[main_course_df["name"] == self.name, "directions_url"].to_string(index=False)


	@classmethod
	def get_user_input(self):
		"""Prompts the user for input about his or her preferences
		and returns the user's main course choice as a string"""
		primary_protein_user = input("\nOk, onto the MAIN COURSE! Do you want to cook fish, chicken, pork, turkey, beef, lamb, veal, or vegetarian: ").lower().strip()
		print ("\n")

		#Error checking if protein entered does not match one available
		while main_course_df["primary_protein"].str.contains(primary_protein_user).any() == False:
			print ("Invalid input - enter a valid protein, please. \n")
			primary_protein_user = input("\nDo you want to cook fish, chicken, pork, turkey, beef, lamb, veal, or vegetarian: ").lower().strip()
			print ("\n")
		health_rating_user = input("\nHow healthy of a dish do you want to cook? Choices are low, medium, or high: ").lower().strip()
		print ("\n")

		#Error checking if health rating entered does not match one available or the protein + health combo does not exist
		while main_course_df["health_rating"].str.contains(health_rating_user).any() == False or main_course_df[(main_course_df["primary_protein"].str.contains(primary_protein_user)) & (main_course_df["health_rating"].str.contains(health_rating_user))].empty == True:
			print ("You either entered an invalid input or that combination doesn't exist. \n")
			health_rating_user = input("\nHow healthy of a dish do you want to cook? Choices are low, medium, or high: ").lower().strip()
			print ("\n")
		new_df = main_course_df[(main_course_df["primary_protein"].str.contains(primary_protein_user)) & (main_course_df["health_rating"].str.contains(health_rating_user))]

		#Print out what the available options are
		available_options = []
		for index, row in new_df.iterrows():
			print (row["name"].upper() + " is a " + row["cuisine_type"].title() + " dish. Its health rating is " + row["health_rating"] + " and its prep effort is " + row["prep_effort"] + ".")
			print ("It suits " + row["mood_pairing"] + " moods " + "and can be served at " + row["occasion_pairing"] + ".")
			print ("\n")
			available_options.append(row["name"].upper())
		user_choice = input("\nSo, which Main Course do you want? Just type in the name as it appears above: ").upper().lstrip()

		#Error checking if the user choice does not match an available option
		while user_choice not in available_options:
			print ("\nSorry, that's not an available option.\nAgain, they are:\n")
			for option in available_options:
				print (option)
			user_choice = input("\nSo, which Main Course do you want? Just type in the name as it appears above: ").upper().lstrip()
		print (f"\nNice, you chose {user_choice.upper()}!")
		return user_choice.title()
	
	def __str__(self):
		return main_course_df.loc[main_course_df["name"] == self.name, "name"].to_string(index=False).lstrip()

	def __repr__(self):
		return main_course_df.loc[main_course_df["name"] == self.name, "name"].to_string(index=False).lstrip()

class Dessert:
	"""Representation of a Dessert object which will be placed on the Menu

	Attributes
	----------
	name: str, name of the dish
	has_chocolate: str, indicator (yes or no) if the dish has chocolate
	prep_effort: str, describes the level of effort (low, medium, high) required to cook the dish
	mood_pairing: str, casual or sophisticated
	occasion_pairing: str, events where the cocktail is appropriate
	directions_url: url link to direction for how to make the item

	Methods
	----------
	init: initializes a Dessert object
	get_user_input: guides the user through questions about preferences to select a Dessert
	str: formats printing the object
	repr: formats representation of the object
	"""


	def __init__(self, name, has_chocolate=None, prep_effort=None, mood_pairing=None, occasion_pairing=None, directions_url=None):

		self.name = name
		self.has_chocolate = dessert_df.loc[dessert_df["name"] == self.name, "has_chocolate"].to_string(index=False)
		self.prep_effort = dessert_df.loc[dessert_df["name"] == self.name, "prep_effort"].to_string(index=False)
		self.mood_pairing = dessert_df.loc[dessert_df["name"] == self.name, "mood_pairing"].to_string(index=False)
		self.occasion_pairing = dessert_df.loc[dessert_df["name"] == self.name, "occasion_pairing"].to_string(index=False)
		self.directions_url = dessert_df.loc[dessert_df["name"] == self.name, "directions_url"].to_string(index=False)


	@classmethod
	def get_user_input(self):
		"""Prompts the user for input about his or her preferences
		and returns the user's dessert choice as a string"""
		has_chocolate_user = input("\nFinally, let's pick a DESSERT. Do you want something with chocolate? Enter yes or no: ").lower().strip()
		print ("\n")

		#Error checking if chocolate preference entered does not match one available
		while dessert_df["has_chocolate"].str.contains(has_chocolate_user).any() == False:
			print ("Invalid input - enter yes or no, please. \n")
			has_chocolate_user = input("\nDo you want something with chocolate? Enter yes or no: ").lower().strip()
			print ("\n")
		new_df = dessert_df[dessert_df["has_chocolate"].str.contains(has_chocolate_user)]

		#Print out what the available options are
		available_options = []
		for index, row in new_df.iterrows():
			print (row["name"].upper() + " requires " + row["prep_effort"] + " effort to prepare.")
			print ("It suits " + row["mood_pairing"] + " moods " + "and can be served at " + row["occasion_pairing"] + ".")
			print ("\n")
			available_options.append(row["name"].upper())
		user_choice = input("\nSo, which dessert do you want? Just type in the name as it appears above: ").upper().lstrip()

		#Error checking if the user choice does not match an available option
		while user_choice not in available_options:
			print ("\nSorry, that's not an available option.\nAgain, they are:\n")
			for option in available_options:
				print (option)
			user_choice = input("\nSo, which dessert do you want? Just type in the name as it appears above: ").upper().lstrip()
		print (f"\nNice, you chose {user_choice.upper()}!")
		return user_choice.title()

	def __str__(self):
		return dessert_df.loc[dessert_df["name"] == self.name, "name"].to_string(index=False).lstrip()

	def __repr__(self):
		return dessert_df.loc[dessert_df["name"] == self.name, "name"].to_string(index=False).lstrip()

class Menu:
	"""Representation of an entire Menu object

	Attributes
	----------
	None

	Methods
	----------
	init: initializes a Menu object
	build_menu: controls flow of the program - either randomly chooses dishes to place on the Menu or guides the user through selection of each item
	display_menu: prints a nicely-formatted menu to the console
	open_links: opens the url for each item on the menu in the user's default web browser
	str: formats printing the object
	repr: formats representation of the object
	"""


	def __init__(self):
		print ("\nWELCOME TO THE MENU BUILDER PROGRAM! LET'S BUILD A MENU TOGETHER \n")


	@classmethod
	def build_menu(self):
		"""Returns a list of items that will be placed on the Menu.
		This also controls the flow of the program."""
		menu_items = []
		print ("\nAlright, let's begin!\nYou have several options for how to use the MENU BUILDER.\n\nEnter 'GUIDED' if you want to be guided through steps to pick your own items.\nEnter 'RANDOM' if you want the program to pick the items for you.\nEnter 'MOOD' if you want to enter a mood and have the program pick the items for you.\nEnter 'OCCASION' if you want to enter an occasion and have the program pick the items for you.\nEnter 'HELP' for a help screen.\nEnter 'QUIT' to exit the program.\n\n")
		mode = input("So, which mode do you want: ").lower().strip()

		#Print out a help screen if user inputs 'help'
		while mode == "help":
			print ("\nThere are 4 different ways to build your menu.\n\n1. The first way is GUIDED - this means you will be asked several questions about your preferences and shown different options from which to choose.\n2. The second way is RANDOM - this is the quickest way to build the menu, as the program will randomly choose items for you.\n3. The third way is by choosing a MOOD and letting the program pick the items that fit that mood.\n4. Finally, the fourth way is by choosing an OCCASION and letting the program pick the items that fit that occasion.")
			mode = input("\nSo, which mode do you want: ").lower().strip()

		#Error checking if mode entered by user is invalid
		while mode not in ["guided", "random", "mood", "occasion", "help", "quit"]:
			print ("\nSorry, that's an invalid input. Remember, the modes are:\n\n")
			for item in ["guided", "random", "mood", "occasion", "quit"]:
				print (item.upper())
			mode = input("\nSo, which mode do you want: ").lower().strip()
		
		if mode == "guided":
			#Guide the user through building each item on the Menu
			cocktail = Cocktail(Cocktail.get_user_input())
			menu_items.append(cocktail)
			appetizer = Appetizer(Appetizer.get_user_input())
			menu_items.append(appetizer)
			main_course = MainCourse(MainCourse.get_user_input())
			menu_items.append(main_course)
			dessert = Dessert(Dessert.get_user_input())
			menu_items.append(dessert)
			return menu_items
		
		elif mode == "random":
			#Randomly choose each item for the Menu
			cocktail = cocktail_df.sample()["name"].to_string(index=False).lstrip()
			menu_items.append(cocktail)
			appetizer = appetizer_df.sample()["name"].to_string(index=False).lstrip()
			menu_items.append(appetizer)
			main_course = main_course_df.sample()["name"].to_string(index=False).lstrip()
			menu_items.append(main_course)
			dessert = dessert_df.sample()["name"].to_string(index=False).lstrip()
			menu_items.append(dessert)
			return menu_items
		
		elif mode == "mood":
			#Randomly choose each item for the Menu based on the mood
			mood_choice = input("\nOk, you chose to pair with a mood. Enter 'CASUAL' or 'SOPHISTICATED': ").lower().strip()

			#Error checking if mood_choice entered by user is invalid
			while mood_choice not in ["casual", "sophisticated"]:
				print ("\nSorry, that's an invalid input. Remember, the choices are:\n")
				print ("CASUAL\nSOPHISTICATED")
				mood_choice = input("\nOk, you chose to pair with a mood. Enter 'CASUAL' or 'SOPHISTICATED': ").lower().strip()

			cocktail = cocktail_df[cocktail_df["mood_pairing"].str.contains(mood_choice)].sample()["name"].to_string(index=False).lstrip()
			menu_items.append(cocktail)
			appetizer = appetizer_df[appetizer_df["mood_pairing"].str.contains(mood_choice)].sample()["name"].to_string(index=False).lstrip()
			menu_items.append(appetizer)
			main_course = main_course_df[main_course_df["mood_pairing"].str.contains(mood_choice)].sample()["name"].to_string(index=False).lstrip()
			menu_items.append(main_course)
			dessert = dessert_df[dessert_df["mood_pairing"].str.contains(mood_choice)].sample()["name"].to_string(index=False).lstrip()
			menu_items.append(dessert)
			return menu_items
		
		elif mode == "occasion":
			#Randomly choose each item for the Menu based on the occasion
			occasion_choice = input("\nOk, you chose to pair with an occasion. Enter 'DINNER WITH FRIENDS' or 'DINNER PARTY' or 'DATE NIGHT' or 'WEEKNIGHT': ").lower()
			
			#Error checking if occasion_chioce entered by user is invalid
			while occasion_choice not in ["dinner with friends", "dinner party", "date night", "weeknight"]:
				print ("\nSorry, that's an invalid input. Remember, the choices are:\n")
				for item in ["dinner with friends", "dinner party", "date night", "weeknight"]:
					print (item.upper())
				occasion_choice = input("\nOk, you chose to pair with an occasion. Enter 'DINNER WITH FRIENDS' or 'DINNER PARTY' or 'DATE NIGHT' or 'WEEKNIGHT': ").lower()

			cocktail = cocktail_df[cocktail_df["occasion_pairing"].str.contains(occasion_choice)].sample()["name"].to_string(index=False).lstrip()
			menu_items.append(cocktail)
			appetizer = appetizer_df[appetizer_df["occasion_pairing"].str.contains(occasion_choice)].sample()["name"].to_string(index=False).lstrip()
			menu_items.append(appetizer)
			main_course = main_course_df[main_course_df["occasion_pairing"].str.contains(occasion_choice)].sample()["name"].to_string(index=False).lstrip()
			menu_items.append(main_course)
			dessert = dessert_df[dessert_df["occasion_pairing"].str.contains(occasion_choice)].sample()["name"].to_string(index=False).lstrip()
			menu_items.append(dessert)
			return menu_items
		
		elif mode == "quit":
			print ("\nOk, all good - looks like you'll be ordering takeout ;) ")
			return

	def display_menu(menu_items):
		"""Prints out a nicely formatted menu to the console"""
		if not menu_items:
			pass
		else:
			print ("\nMENU FOR THE NIGHT")
			print ("-" * 70)
			print ("COCKTAIL: ", menu_items[0])
			print ("LINK TO INSTRUCTIONS: ", cocktail_df.loc[cocktail_df["name"] == str(menu_items[0]), "directions_url"].to_string(index=False))
			print ("-" * 70)
			print ("APPETIZER: ", menu_items[1])
			print ("LINK TO INSTRUCTIONS: ", appetizer_df.loc[appetizer_df["name"] == str(menu_items[1]), "directions_url"].to_string(index=False))
			print ("-" * 70)
			print ("MAIN COURSE: ", menu_items[2])
			print ("LINK TO INSTRUCTIONS: ", main_course_df.loc[main_course_df["name"] == str(menu_items[2]), "directions_url"].to_string(index=False))
			print ("-" * 70)
			print ("DESSERT: ", menu_items[3])
			print ("LINK TO INSTRUCTIONS: ", dessert_df.loc[dessert_df["name"] == str(menu_items[3]), "directions_url"].to_string(index=False))
			print ("\n\n")

	def open_links(menu_items):
		"""Opens the directions url links for each item on the menu in a web broswer"""
		webbrowser.open(cocktail_df.loc[cocktail_df["name"] == str(menu_items[0]), "directions_url"].to_string(index=False).lstrip())
		webbrowser.open(appetizer_df.loc[appetizer_df["name"] == str(menu_items[1]), "directions_url"].to_string(index=False).lstrip())
		webbrowser.open(main_course_df.loc[main_course_df["name"] == str(menu_items[2]), "directions_url"].to_string(index=False).lstrip())
		webbrowser.open(dessert_df.loc[dessert_df["name"] == str(menu_items[3]), "directions_url"].to_string(index=False).lstrip())

	def __str__(self):
		return list(menu_items)

	def __repr__(self):
		return list(menu_items)

#--------------------------------
# Run the program

my_menu = Menu.build_menu()
try:
	Menu.display_menu(my_menu)
	Menu.open_links(my_menu)
except TypeError:
	print ("Bye!")	


















