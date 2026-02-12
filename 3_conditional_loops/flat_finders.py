"""
Flat Finder - Conditional Logic Exercise

This script translates a real-world, natural language description
into structured Python decision logic using conditional statements
(if / elif / else).

Sarah's preferences:
- She loves New York and San Francisco and would move there
  if the monthly rent is below 4000 USD.
- She refuses to live in Washington under any circumstances.
- She loves Chicago and would move there regardless of the price.
- For any other city, she would move only if the rent is
  3000 USD or less per month.

Based on user input (city and monthly rent), the program evaluates
whether Sarah would be willing to move to the given location.

Part of the "Python Foundations to Automation" learning path.
"""

reply = ''
yes_reply = "Yes, Sarah would"
no_reply = "Unfortunately, Sarah wouldn't"

print("\n    Hello, \n"
    "To check whether the flat meets Sarah's preferences,"
    )
flat_city = input('please enter the city where the flat is located: ')
flat_city = flat_city.strip().lower()


if flat_city == "washington":
    flat_price = "any"
    reply = no_reply
elif flat_city == "chicago":
    flat_price = "any"
    reply = yes_reply
else:
    flat_price = float(input('Thanks. What is the monthly rent in USD? '))
    
    if ((flat_city in ["new york", "san francisco"] and flat_price < 4000) 
        or 
        (flat_price <= 3000)):
        reply = yes_reply

    else:
        reply = no_reply


print(f'{reply} be willing to move to a flat in {flat_city} for {flat_price} rent per month.')