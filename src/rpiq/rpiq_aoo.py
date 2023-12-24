#list)ofRPS
# Description: RPIQ AOO is a python program that generates a random RPIQ AOO
rpList = ['Active_Listening_Workshop', 'Change_Management_Scenario', 'Conflict_Resolution_Exercise', 'Cultural_Competency_Training', 'Customer_Relationship_Management_Exercise', 'Dealing_with_Difficult_People', 'Enhanced_Active_Empathy_Workshop', 'Enhanced_Adaptability_Challenge', 'Enhanced_Creative_Thinking_Workshop', 'Enhanced_Critical_Thinking_Exercise']

# display the list of RPs for the user to choose from
print("Here is a list of RPs you can choose from:")
for rp in rpList:
    print(rp)
# ask the user to choose a RP
rp = input("Which RP would you like to do? ")
# check if the user input is valid
