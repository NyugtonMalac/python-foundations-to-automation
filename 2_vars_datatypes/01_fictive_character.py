"""
Fictive Character Generator

This script demonstrates basic Python fundamentals such as user input handling,
string normalization, type conversion, simple arithmetic, boolean logic, and
formatted output using f-strings.

A simplified leap year model is used to approximate age in days.
    
"""

name = input("Hello, please enter your character's name: ")
name = name.strip().capitalize()

age_years = int(input(f"Please enter {name}'s age (in whole years):"))
age_days = age_years * 365 +age_years // 4  # simplified leap year model

python_experience_in_years = int(input(f"How many whole years of Python experience does {name} have? "))

pro = input(f"Would {name} like to become a professional Python developer (Yes or No)? ")
pro = True if (pro.strip().lower()) == 'yes' else False

if pro:
    ans_extension = 'want'
else:
    ans_extension = "do not want"



print(f'''
      My character is {age_days} days old. Their name is {name} and they have 
      {python_experience_in_years} years of experience.
      They {ans_extension} to become a professional Python developer.
      '''
      )