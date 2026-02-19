"""
User Information Manipulation

This script is an introductory Python exercise focusing on list and dictionary
operations. It demonstrates common data manipulation tasks such as sorting,
indexing, adding and removing elements, handling duplicates, and working with
nested data structures.

The goal of this exercise is to practice practical operations on built-in data
structures rather than implementing complex algorithms.

This file is part of the "Python Foundations to Automation" learning repository.
"""

from pprint import pprint

# input
user_info = {
    "name": "Mike",
    "age": 25,
    "favourite_meals": [
        "pizza",
        "carbonara",
        "sushi"
    ],
    "phone_contacts": {
        "Mary": "+36701234567",
        "Tim": "+36207654321",
        "Tim2": "+36304567321",
        "Jim": "+364005000"
    }
}

# Request 4 programming languages from the user and store them as "skills"
program_languages = input(f'\nPlease enter 4 programming languages, separated by commas (no spaces):  ')
program_languages_list = program_languages.strip().split(',')

user_info['skills'] = program_languages_list

# sorting favourite meals
user_info["favourite_meals"].sort()

# printing second-to-last item of favourite_meals:
print(f"\nSecond-to-last item of user's favourite meals is {user_info['favourite_meals'][-2]}.\n")

# extending favourite_meals with 'spaghetti'
user_info["favourite_meals"].append('spaghetti')

# extending favourite_meals with its 3rd and 4th items again
user_info["favourite_meals"].extend(user_info["favourite_meals"][2:4])

# remove duplicates
user_info["favourite_meals"] = list(set(user_info["favourite_meals"]))
user_info["favourite_meals"].sort()

# changing 1st and last element of user_info["favourite_meals"] list
temp = user_info["favourite_meals"][0]
user_info["favourite_meals"][0] = user_info["favourite_meals"][-1]
user_info["favourite_meals"][-1] = temp

# changing 1st and last element of user_info["favourite_meals"] list using tuple unpacking assignment statement
## Demonstration: tuple unpacking swap
user_info["favourite_meals"][0], user_info["favourite_meals"][-1] = (user_info["favourite_meals"][-1], user_info["favourite_meals"][0])

# extending "phone_contacts" with new name and phone number
user_info["phone_contacts"]['Lily'] = "+361505505"

# removing Tim from the phonebook
user_info["phone_contacts"].pop("Tim")

# renaming Tim2 to Tim
user_info["phone_contacts"]["Tim"] = user_info["phone_contacts"]["Tim2"]
user_info["phone_contacts"].pop("Tim2")

# Add a new contact with two phone numbers
user_info["phone_contacts"]['Vivi'] = ["+361505505", "+361505555"]  # value can be a string (single number) or a list (multiple numbers)


# printing last 3 elements of skills in descending order
user_info["skills"].sort()
print(f'Last 3 elements of skills in descending order: {sorted(user_info["skills"][-3:], reverse=True)}\n')

print(f"Let's look at the user_info dictionary:  ")
pprint(user_info)
print()

