# This is the main menu.
def main():
	print ("Welcome to the Alberta Auto Registration System!")
	choice = 7
	while (choice != 6):
		print ("----------------------------------------")
		print ("""Please Select from the following:
		1:New Vehicle Registration
		2:Auto Transaction
		3:Driver Licence Registration
		4:Violation Record
		5:Search Engine
		6:Exit""")
		choice = 7
		while (choice == 7):
			try:
				choice = eval(input("Choice (1-6): "))
				if (not (choice >= 1 and choice <=6)):
					choice = 7  # Will cause a loop back to get new entry (choice was invalid)
					print ("Invalid Input!", end = " ")
			except:
				choice = 7  # Will cause a loop back to get new entry (choice was invalid)
				print ("Invalid Input!", end = " ")
				
		if choice == 1:
			newVehicle()
		elif choice == 2:
			autoTrans()
		elif choice == 3:
			licenceReg()
		elif choice == 4:
			violationRec()
		elif choice == 5:
			searchEngine()
		elif choice == 6:
			break
		else:
			choice = 7  # Will cause a loop back to get new entry (choice was invalid)
			print ("Invalid Input!", end = " ")
		print (choice)
# This will display the menu and handle input to the menu
def newVehicle():
	return

def autoTrans():
	return

def licenceReg():
	return

def violationRec():
	return

def searchEngine():
	return

main()  # run the main function
