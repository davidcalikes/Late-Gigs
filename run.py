import os
import re
import random
import gspread
from google.oauth2.service_account import Credentials
from mail import email_verify, notify_user_gig

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('late_gigs')


def clear_page():
    """
    Clear page of text clutter after user interaction to improve UX
    Code used is from:
    https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def area_check(user):
    """
    Ensure user is aware of Local Gigs catchment area
    before calling relevant get_(user)_data function
    """
    user_type = user
    while True:
        print("Just a quick check before we begin.")
        print("Please confirm you're in the North East Area.\n")

        if user_type == "venue":
            venue_location = input("Is your venue in the North East?:(y/n)\n")
            if venue_location == "y":
                clear_page()
                print("\nOK, just making sure!\n")
                print("\nNow let's find you an act!\n")
                get_venue_data()
            elif venue_location == "n":
                clear_page()
                print("Sorry, Late gigs only operates in the NE Area\n")
                input("Press Enter to exit to menu...\n")
                clear_page()
                main()
            else:
                print("Invalid input! Type either y or n!")
        elif user_type == "act":
            act_location = input("Is your act in the North East?:(y/n)\n")
            if act_location == "y":
                clear_page()
                print("\nOK, just making sure!")
                print("\nNow let's find you a venue!\n")
                get_act_data()
            else:
                print("Sorry, That's not a valid option\n")
                input("Press Enter to exit to menu...\n")
                main()


def get_venue_data():
    """
    Get data from the user incrementally
    that lists the properties of the venue object.
    Validates data at every input to improve UX and
    reduce risk of TypeErrors while working with
    a list containing different data types.
    """
    venue_data = []

    while True:
        name = input("Enter your venue name here: \n")
        if len(name) >= 2:
            venue_data.append(name.lower())
            break
        else:
            clear_page()
            print("\n")
            print(f'{name} is not a valid name')
            print("\nVenue names must contain more than")
            print("two characters!")
            print("\nPlease Try Again!\n")
            continue

    print("\n")
    print(f"Cool! What genre of music do you prefer at {name}?")
    print("\n")
    print("Type one of the following options:")
    print("Rock, Blues, Pop, Jazz, Metal, R&b, Indie, Country, Irish trad \n")
    genre_list = ["Rock", "rock", "ROCK", "Blues", "blues", "BLUES",
                  "Pop", "pop", "POP", "Jazz", "jazz", "JAZZ", "Metal",
                  "metal", "METAL", "R&b", "r&b", "R&B", "Indie", "indie",
                  "Country", "country", "COUNTRY",
                  "Irish Trad", "irish trad", "IRISH TRAD"]
    while True:
        genre = input("Enter genre here: \n")
        if genre in genre_list:
            venue_data.append(genre.lower())
            break
        else:
            clear_page()
            print("\n")
            print(f"{genre} is not a valid genre")
            print("\nType one of the following options:")
            print("\nRock, Blues, Pop, Jazz, Metal, R&b,")
            print("Indie, Country or Irish trad \n")
            continue

    clear_page()
    print("\nNice! Hopefully your patrons will be enjoying some")
    print(f"live {genre.title()} at {name.title()} soon!")
    print("\n")

    print("Let's keep going!\n")
    print("What day this weekend do you need an act?")
    print("Type: Friday, Saturday or Sunday \n")
    day_list = ["Friday", "friday", "FRIDAY",
                "Saturday", "saturday", "SATURDAY",
                "Sunday", "sunday", "SUNDAY"]
    while True:
        day = input("Enter required day: \n")
        if day in day_list:
            venue_data.append(day.lower())
            break
        else:
            clear_page()
            print("\n")
            print(f"{day} is not a valid gig day... Try again!")
            print("\nType one of the following options:\n")
            print("Friday, Saturday or Sunday")
            continue
    clear_page()
    print("\nExcellent!")
    print("Here's what we have so far...\n")
    print(f"Your venue: '{name}' is looking for an act")
    print(f"to play some {genre} for this coming {day}?")
    print("\n")

    while True:
        data_correct = input("Are you happy to continue?:(y/n)\n")
        if data_correct == "y":
            clear_page()
            print("\nOK cool! Now let's keep going!\n")
            break
        elif data_correct == "n":
            clear_page()
            print("That's ok, type y to restart or n to exit\n")
            user_choice = input("Type y or n here: \n")
            if user_choice == "y":
                get_venue_data()
            elif user_choice == "n":
                main()
            else:
                print("Invalid option! y or n please!")
                continue
        else:
            print("Not a valid choice please type y/n")
            continue

    print("Tell us the maximum fee you are willing to pay your act.\n")
    print("Hint: Act fees vary depending on many factors, such as")
    print("length of set, number of band members ect.\n")
    print("Aim to set your maximum fee between €200 and €600 to increase")
    print("your chances of finding a suitable act.\n")
    while True:
        try:
            fee = int(input("Enter max fee in € here: \n"))
            if 100 <= fee <= 1000:
                pass
            else:
                print("Fee is too far outside Late Gigs recommended range!")
                print("You can deviate a little, but not too much.")
                print("please try again")
                continue
        except ValueError:
            clear_page()
            print("Nope! We need a number here... try again!")
            continue
        else:
            break

    venue_data.append(fee)
    clear_page()
    print("\nOutstanding! We're almost there!\n")

    print("What is the maximum number of performers")
    print(f"the {genre} act should have?")
    print("\n")
    while True:
        try:
            members = int(input("Type number of members here: \n"))
            if 1 <= members <= 15:
                print("in range")
            elif members == 0:
                print("Number must be more than 0. Try again!")
                continue
            else:
                print("Sorry. Thats's too many members for a Late Gigs Venue")
                print("Venues have a maximum stage capacity of 15")
                print("Please try again... ")
                print("(maybe give the scissors player a night off ;) )")
                continue
        except ValueError:
            print("Sorry, only a number will do in this case. Try again!")
            continue
        else:
            break

    venue_data.append(members)
    clear_page()

    print("\nExcellent!\n")
    print("How long should the act play for?")
    print("Sets can be between 1 and 5 hours")
    print("and can be written in half hour increments...")
    print("Example: 1 hour = 1")
    print("Example: 3 and a half hours = 3.5")
    while True:
        try:
            length_list = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
            set_length = float(input("Enter length of set: \n"))
            if 1 <= set_length <= 5 and set_length in length_list:
                print("Valid set length")
            else:
                print("Invalid set length! Sets can be between 1 and 5 hours")
                print("and can be written in half hour increments...")
                print("Example: 1 hour = 1")
                print("Example: 3 and a half hours = 3.5")
                continue
        except ValueError:
            print("Whoopsie! This value needs to be a number. Try again!")
            continue
        else:
            break
    venue_data.append(set_length)
    clear_page()
    print("\n")
    print(f"All done! Here's the gig requirements for {name}:")
    print("\n")
    print(f"You require an act to play {genre} on {day}")
    print(f"with {members} member(s) that will play for {set_length} hours")
    print(f"for a fee of no more than €{fee}")
    print("\n")
    user = "venue"
    properties = venue_data

    while True:
        print("Would you like to search the database for a suitable venue?\n")
        data_ver = input("Confirm search?:(y/n)\n")
        if data_ver == "y":
            clear_page()
            print("\nGreat Stuff! Now let's find you an act!\n")
            regex_check(properties, name, user)
        elif data_ver == "n":
            clear_page()
            print("\nAre you sure don't want to proceed?")
            print("All data will be lost!\n")
            confirm_no = input(
                "Type 'y' to return to menu or 's' to search database:\n")
            if confirm_no == "y":
                clear_page()
                main()
            elif confirm_no == "s":
                print("That's Ok! Here we go")
                regex_check(properties, name, user)
            else:
                print("Sorry invalid input, type 'y' or 'n'")
        else:
            clear_page()
            print("Sorry invalid input, please type either 'y' or 'n'")
            continue


def get_act_data():
    """
    Get data from the user incrementally
    that lists the properties of the act object.
    Validates data at every input to improve UX and
    reduce risk of TypeErrors while working with
    a list containing different data types.
    """
    act_data = []

    while True:
        name = input("Enter the name of your act here: \n")
        if len(name) >= 2:
            act_data.append(name.lower())
            break
        else:
            clear_page()
            print("\n")
            print(f'{name} is not a valid name')
            print("\nAct names must contain more than")
            print("two characters!")
            print("\nPlease Try Again!\n")
            continue

    print("\n")
    print(f"Cool! What genre of music do(es) {name} mostly play?")
    print("\n")
    print("Type one of the following options:")
    print("Rock, Blues, Pop, Jazz, Metal, R&b, Indie, Country, Irish trad \n")
    genre_list = ["Rock", "rock", "ROCK", "Blues", "blues", "BLUES",
                  "Pop", "pop", "POP", "Jazz", "jazz", "JAZZ", "Metal",
                  "metal", "METAL", "R&b", "r&b", "R&B", "Indie", "indie",
                  "Country", "country", "COUNTRY",
                  "Irish Trad", "irish trad", "IRISH TRAD"]
    while True:
        genre = input("Enter genre here: \n")
        if genre in genre_list:
            act_data.append(genre.lower())
            break
        else:
            clear_page()
            print("\n")
            print(f"{genre} is not a valid genre")
            print("\nType one of the following options:")
            print("\nRock, Blues, Pop, Jazz, Metal, R&b,")
            print("Indie, Country or Irish trad \n")
            continue

    clear_page()
    print("\n")
    print(f"Nice! Hopefully fans of {name.title()} will be enjoying some")
    print(f"live {genre.title()} this weekend!")
    print("\n")

    print("Let's keep going!\n")
    print("What day this weekend do you want to perform?")
    print("Type: Friday, Saturday or Sunday \n")
    day_list = ["Friday", "friday", "FRIDAY",
                "Saturday", "saturday", "SATURDAY",
                "Sunday", "sunday", "SUNDAY"]
    while True:
        day = input("Enter required day: \n")
        if day in day_list:
            act_data.append(day.lower())
            break
        else:
            clear_page()
            print("\n")
            print(f"{day} is not a valid gig day... Try again!")
            print("\nType one of the following options:\n")
            print("Friday, Saturday or Sunday")
            continue
    clear_page()
    print("\nExcellent!")
    print("Here's what we have so far...\n")
    print(f"Your act: '{name.title()}' is looking for a(n) {genre.title()}")
    print(f"venue for this coming {day.title()}?")
    print("\n")

    while True:
        data_correct = input("Are you happy to continue?:(y/n)\n")
        if data_correct == "y":
            clear_page()
            print("\nOK cool! Now let's keep going!\n")
            break
        elif data_correct == "n":
            clear_page()
            print("That's ok, type y to restart or n to exit\n")
            user_choice = input("Type y or n here: \n")
            if user_choice == "y":
                get_act_data()
            elif user_choice == "n":
                main()
            else:
                print("Invalid option! y or n please!")
                continue
        else:
            print("Not a valid choice please type y/n")
            continue

    print("Tell us the minimum fee you will accept per gig.\n")
    print("Hint: Act fees generally range between €200 and €600")
    print("\nAim to set your minimum fee within this range to increase")
    print("your chances of finding a suitable venue.\n")
    while True:
        try:
            fee = int(input("Enter min fee in € here: \n"))
            if 100 <= fee <= 1000:
                pass
            else:
                print("Fee is too far outside Late Gigs recommended range!")
                print("You can deviate a little, but not too much.")
                print("please try again")
                continue
        except ValueError:
            clear_page()
            print("Nope! We need a number here... try again!")
            continue
        else:
            break

    act_data.append(fee)
    clear_page()
    print("\nOutstanding! We're almost there!\n")

    print("How many members make up your act?\n")
    while True:
        try:
            members = int(input("Type number of members here: \n"))
            if 1 <= members <= 15:
                print("in range")
            elif members == 0:
                print("Number must be more than 0. Try again!")
                continue
            else:
                print("Sorry. Thats's too many members for a Late Gigs Venue")
                print("Venues have a maximum stage capacity of 15")
                print("Please try again... ")
                print("(maybe give the scissors player a night off ;) )")
                continue
        except ValueError:
            print("Sorry, only a number will do in this case. Try again!")
            continue
        else:
            break

    act_data.append(members)
    clear_page()

    print("\nExcellent!\n")
    print(f"What is the typical set length of a {name.title()} gig?")
    print("Sets can be between 1 and 5 hours")
    print("and can be written in half hour increments...")
    print("Example: 1 hour = 1")
    print("Example: 3 and a half hours = 3.5")
    while True:
        try:
            length_list = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
            set_length = float(input("Enter length of set: \n"))
            if 1 <= set_length <= 5 and set_length in length_list:
                print("Valid set length")
            else:
                print("Invalid set length! Sets can be between 1 and 5 hours")
                print("and can be written in half hour increments...")
                print("Example: 1 hour = 1")
                print("Example: 3 and a half hours = 3.5")
                continue
        except ValueError:
            print("Whoopsie! This value needs to be a number. Try again!")
            continue
        else:
            break
    act_data.append(set_length)
    clear_page()
    print("\n")
    print(f"All done! Here's the gig requirements for {name.title()}:")
    print("\n")
    print(f"You are a(n) {genre.title()} act with no more than")
    print(f"{members} member(s) looking for a gig on {day.title()}")
    print(f"that will play for {set_length} hours")
    print(f"for a fee of no less than €{fee}")
    print("\n")
    user = "act"
    properties = act_data

    while True:
        print("Would you like to search the database for a suitable venue?\n")
        data_ver = input("Confirm search?:(y/n)\n")
        if data_ver == "y":
            clear_page()
            print("\nGreat Stuff! Now let's find you an act!\n")
            regex_check(properties, name, user)
        elif data_ver == "n":
            clear_page()
            print("\nAre you sure don't want to proceed?")
            print("All data will be lost!\n")
            confirm_no = input(
                "Type 'y' to return to menu or 's' to search database:\n")
            if confirm_no == "y":
                clear_page()
                main()
            elif confirm_no == "s":
                print("That's Ok! Here we go")
                regex_check(properties, name, user)
            else:
                print("Sorry invalid input, type 'y' or 'n'")
        else:
            clear_page()
            print("Sorry invalid input, please type either 'y' or 'n'")
            continue


def regex_check(properties, name, user):
    """
    Validate email address input using regular expressions method.
    """
    while True:
        print("\nWe just need your email address to begin the search! \n")
        email = input("Type a valid email address here: \n")
        check_email_structure = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if re.match(check_email_structure, email):
            print("email is valid")
            send_user_pin(properties, name, user, email)
        else:
            print("Doesn't appear to be a valid email address. Try again!")
            continue


def send_user_pin(properties, name, user, email):
    """
    Send email to user with pin for account validation
    """
    user_email_address = email
    user_pin = random.randint(1111, 9999)
    email_verify(name, user, user_email_address, user_pin)
    validate_user_pin(properties, name, user, user_email_address, user_pin)


def validate_user_pin(properties, name, user, user_email_address, user_pin,):
    """
    Use pin to verify email account
    """
    while True:
        pin = user_pin
        print(f"enter the pin we sent to {user_email_address}")
        pin_attempt = input("enter the pin here:")
        pin_int = int(pin_attempt)
        if pin_int == pin:
            print("\nExcellent! Valid Pin! Now let's keep going!\n")
            details = [name.lower(), user_email_address, user_pin]
            user_details_worksheet = SHEET.worksheet("user_details")
            user_details_worksheet.append_row(details)
            check_database(properties, user, user_email_address)
            break
        else:
            clear_page()
            print("\n")
            print("Sorry! Incorrect Pin! Have another Go!")
            continue


def check_database(properties, user, user_email_address):
    """
    Check's the database for any object instances
    that match the users requirements.
    """
    print("\nUser is...", user)
    print("\n")
    print("Looking for match in relevant database...\n")

    while True:
        if user == "venue":
            check_standby_list(properties, user, user_email_address)
        elif user == "act":
            check_venue_list(properties, user, user_email_address)
        else:
            print("Whoops! Something went wrong... returning to main menu")
            main()


def check_standby_list(properties, user, user_email_address):
    """
    Check's the database for any available acts
    that match user requirements.
    """
    acts = SHEET.worksheet("standby").get_all_values()

    item = acts.pop(1)
    venue_name = properties[0]
    print("Looking for act for", venue_name.title())
    check_list = properties
    orig_list_len = len(acts)
    print(orig_list_len - 1, "acts on standby list")
    print("Checking first item...")

    act_genre = item[1]
    act_day = item[2]
    act_fee = int(item[3])
    act_members = int(item[4])
    act_set_len = float(item[5])

    act_conv = [act_genre, act_day, act_fee, act_members, act_set_len]

    venue_genre = check_list[1]
    venue_day = check_list[2]
    venue_fee = int(check_list[3])
    venue_members = int(check_list[4])
    venue_set_len = float(check_list[5])

    venue_conv = [venue_genre, venue_day, venue_fee, venue_members,
                  venue_set_len]

    while True:
        if act_conv == venue_conv:
            print("\nMatch Found!\n")
            print("An act has been found for your venue that")
            print("meets all your requirements")
            print("Act Name:", item[0].title())
            act_name = item[0]
            item_list_index = orig_list_len - len(acts) + 1
            act_day = item[2]
            act_fee = item[3]
            act_set_len = float(item[5])
            match_email = act_name
            make_gig(item_list_index, act_name, venue_name,
                     act_day, act_genre, act_fee, user, user_email_address,
                     match_email)
        elif len(acts) >= 2:
            print("Not a match!")
            item = acts.pop(1)
            print("next item is...")
            act_genre = (item[1])
            act_day = item[2]
            act_fee = int(item[3])
            act_members = int(item[4])
            act_set_len = float(item[5])
            act_conv = [act_genre, act_day, act_fee, act_members, act_set_len]
            print("Act name:", item[0].title())
        else:
            print("End of List... no matches")
            venue_double_booking_check(properties, user)


def check_venue_list(properties, user, user_email_address):
    """
    Check's the database for any available venues
    that match user requirements.
    """
    venues = SHEET.worksheet("venues").get_all_values()

    item = venues.pop(1)
    act_name = properties[0]
    print("Looking for venue for", act_name)
    check_list = properties
    orig_list_len = len(venues)
    print(orig_list_len - 1, "venues on the waiting list!")
    print("Checking first item...")

    venue_genre = item[1]
    venue_day = item[2]
    venue_fee = int(item[3])
    venue_members = int(item[4])
    venue_set_len = float(item[5])

    venue_conv = [venue_genre, venue_day, venue_fee, venue_members,
                  venue_set_len]

    act_genre = check_list[1]
    act_day = check_list[2]
    act_fee = int(check_list[3])
    act_members = int(check_list[4])
    act_set_len = float(check_list[5])

    act_conv = [act_genre, act_day, act_fee, act_members,
                act_set_len]

    while True:
        if venue_conv == act_conv:
            print("\nMatch Found\n")
            print("Name:", item[0].title())
            venue_name = item[0]
            item_list_index = orig_list_len - len(venues) + 1
            print("List Index =", item_list_index)
            venue_day = item[2]
            venue_fee = item[3]
            venue_set_len = float(item[5])
            match_email = venue_name
            make_gig(item_list_index, act_name, venue_name,
                     venue_day, venue_genre, venue_fee, user,
                     user_email_address, match_email)
        elif len(venues) >= 2:
            print("Not a match!")
            item = venues.pop(1)
            print("next up is...")
            venue_genre = (item[1])
            venue_day = item[2]
            venue_fee = int(item[3])
            venue_members = int(item[4])
            venue_set_len = float(item[5])
            venue_conv = [venue_genre, venue_day, venue_fee, venue_members,
                          venue_set_len]
            print("Venue name:", item[0].title())
        else:
            print("End of List... no matches")
            act_double_booking_check(properties, user)


def make_gig(item_list_index, act_name, venue_name,
             user_day, user_genre, user_fee, user, user_email_address,
             match_email):
    """
    Adds match to gig database and removes match from venues/standby sheet
    """
    while True:
        user_choice = input('Do you want to create this gig?:(y/n)\n')
        properties = [act_name, venue_name, user_day, user_genre, user_fee]
        item_index = item_list_index
        print("DB index =", item_index)
        if user_choice == "y" and user == "venue":
            clear_page()
            print("\nBooya! Lets do it... Updating Databases!\n")
            print("Updating gig listings...")
            SHEET.worksheet("gig_list").append_row(properties)
            print(f"removing {act_name.title()} from standby list")
            SHEET.worksheet("standby").delete_rows(item_index + 1)
            print("Success!")
            get_match_email(properties, user, user_email_address, match_email)
            print(match_email)
            exit()
        elif user_choice == "y" and user == "act":
            clear_page()
            print("Updating gig listings...")
            SHEET.worksheet("gig_list").append_row(properties)
            print(f"removing {venue_name.title()} from waiting list")
            SHEET.worksheet("venues").delete_rows(item_index + 1)
            print("Success!")
            get_match_email(properties, user, user_email_address, match_email)
            exit()
        else:
            clear_page()
            print('Sorry, Try Again another time')
            input('Press Enter to exit to menu...\n')
            main()


def get_match_email(properties, user, user_email_address, match_email):
    """
    Check's the database for the correct email address
    to notify user on relevent waiting list
    """
    print("retrieving contact info for", match_email.title())
    user_data_sheet = SHEET.worksheet("user_details").get_all_values()

    user_item = user_data_sheet.pop(1)
    user_name = user_item[0]

    while True:
        if user_name == match_email:
            print("\nDetails Found\n")
            print("for", user_item[0].title())
            list_user_email = user_item[1]
            notify_user_gig(properties, user, user_email_address,
                            list_user_email)
            main()
        elif len(user_data_sheet) >= 2:
            print("Still looking!")
            user_item = user_data_sheet.pop(1)
            user_name = user_item[0]
            print("Checking next item...")
            print("User name:", user_item[0].title())
        else:
            clear_page()
            print("Error... match details not found!")
            print("Please contact Late Gigs via email")
            print("about this error:")
            print("Email: lategigs@davidcalikes.com")
            main()


def venue_double_booking_check(properties, user):
    """
    Ensures user doesn't already have a gig booked for day required
    """
    gig_list = SHEET.worksheet("gig_list").get_all_values()

    user_item = gig_list.pop(1)
    user_name = user_item[1]
    day = properties[2]
    print("user name is:", properties[0])
    print("gig list item:", user_name)
    print("\nChecking gig list to prevent double bookings...")

    while True:
        if user_name == properties[0] and day == user_item[2]:
            print("\nGig Found\n")
            print(f"Gig already exists for {user_name.title()} on {day}")
            print("Sorry, no double bookings allowed")
            print("Returning to main menu")
            main()
        elif len(gig_list) >= 2:
            print("Still looking!")
            user_item = gig_list.pop(1)
            user_name = user_item[1]
            print("Checking next item...")
            print("User name:", user_item[1].title())
        else:
            update_data_sheet(properties, user)
            exit()


def act_double_booking_check(properties, user):
    """
    Ensures user doesn't already have a gig booked for day required
    """
    gig_list = SHEET.worksheet("gig_list").get_all_values()

    user_item = gig_list.pop(1)
    user_name = user_item[0]
    day = properties[2]
    print(user_name)
    print("user name is:", properties[0])
    print("\nChecking gig list to prevent double bookings...")

    while True:
        if user_name == properties[0] and day == user_item[2]:
            print("\nGig Found\n")
            print(f"Gig already exists for {user_name.title()} on {day}")
            print("Sorry, no double bookings allowed")
            print("Returning to main menu")
            main()
        elif len(gig_list) >= 2:
            print("Still looking!")
            user_item = gig_list.pop(1)
            user_name = user_item[0]
            print("Checking next item...")
            print("User name:", user_item[0].title())
            print(user_item)
        else:
            update_data_sheet(properties, user)
            exit()


def update_data_sheet(properties, user):
    """
    Updates relevant data sheet for both venues and artists
    """
    venue_worksheet = SHEET.worksheet("venues")
    standby_worksheet = SHEET.worksheet("standby")

    if user == "venue":
        print("\nUpdating venue database...\n")
        venue_worksheet.append_row(properties)
    elif user == "act":
        print("\nUpdating standby database...\n")
        standby_worksheet.append_row(properties)
    else:
        clear_page()
        print("Error! I guess we gotta go pick a whole bunch of")
        print("whoopsie daisies!")
        main()

    print(user.title(), "database updated succesfully!")
    print("Thank you for using Late Gigs!\n")
    print("A gig will be created automatically if")
    print("we find you a suitable match in the coming days!\n")
    print("We will notify you by email if a Late Gig")
    print("is created!")
    exit()


def remove_from_list():
    """
    Gets user type before calling secondary function
    """
    print("Ok! What type of user are you... Venue or Act?")
    while True:
        user_type = input("Enter user type here: ")
        if user_type.lower() == "venue":
            get_venue_details()
        elif user_type.lower() == "act":
            get_act_details()
        else:
            print("Invalid input! Type either 'Venue' or 'Act'")


def get_venue_details():
    """
    Establish if venues credentials are correct
    """
    day_list = ["friday", "Friday", "FRIDAY", "saturday", "Saturday",
                "SATURDAY", "sunday", "Sunday", "SUNDAY"]

    print("Please type the name of your venue.")
    while True:
        venue_id = input("Type venue name here: ")
        if len(venue_id) >= 2:
            break
        else:
            print("\n")
            print(f'{venue_id} is not a venue name!')
            print("\nVenue names must contain more than")
            print("two characters!")
            print("\nPlease try again!\n")
            continue
    print("Which day were you originally looking for?")
    day = input("Type day here:")
    if day in day_list:
        print("data valid")
    else:
        print("Invalid input! Try again!")

    print("And finally, the unique pin number we sent you")
    pin = input("Type pin here:")
    if pin.isdigit() and len(pin) == 4:
        print("Checking Pin!")
    else:
        print("Invalid pin try again! (4 digit number)")

    venue_details = SHEET.worksheet("user_details").get_all_values()

    user = "venue"
    user_item = venue_details.pop(1)
    user_name = user_item[0]
    print("\nValidating user data... one moment!")

    while True:
        if user_name == venue_id and pin == user_item[2]:
            print("\nValid pin")
            print(f"Removing {user_name.title()} from the database for {day}")
            print("Sorry to see you go!")
            remove_entry(venue_id, day, user)
            print("Returning to main menu")
            main()
        elif len(venue_details) >= 2:
            print("Still looking!")
            user_item = venue_details.pop(1)
            user_name = user_item[0]
            print("Checking next item...")
            print("User name:", user_item[0].title())
        else:
            clear_page()
            print("No such gig found! Exiting to main menu")
            main()


def get_act_details():
    """
    Establish if act credentials are correct
    """
    day_list = ["friday", "Friday", "FRIDAY",
                "saturday", "Saturday", "SATURDAY",
                "sunday", "Sunday", "SUNDAY"]

    print("Please type the name of your act.")
    while True:
        act_id = input("Type act name here: ")
        if len(act_id) >= 2:
            break
        else:
            print("\n")
            print(f'{act_id} is not a act name!')
            print("\nAct names must contain more than")
            print("two characters!")
            print("\nPlease try again!\n")
            continue

    print("Which day were you originally looking for?")
    day = input("Type day here:")
    if day in day_list:
        print("data valid")
    else:
        print("Invalid input! Try again!")

    print("And finally, the unique pin number we sent you")
    pin = input("Type pin here:")
    if pin.isdigit() and len(pin) == 4:
        print("Pin valid!")
    else:
        print("Invalid pin try again!")

    acts_details = SHEET.worksheet("user_details").get_all_values()

    user = "act"
    user_item = acts_details.pop(1)
    user_name = user_item[0]
    print("\nValidating user data... one moment!")

    while True:
        if user_name == act_id and pin == user_item[2]:
            print("\nValid pin")
            print(f"Removing {user_name.title()} from database for {day}")
            print("Sorry to see you go!")
            remove_entry(act_id, day, user)
            print("Returning to main menu")
            main()
        elif len(acts_details) >= 2:
            print("Still looking!")
            user_item = acts_details.pop(1)
            user_name = user_item[0]
            print("Checking next item...")
            print("User name:", user_item[0].title())
        else:
            print("No matching user details found! Exiting to main menu")
            exit()


def remove_entry(user_id, day, user):
    """
    Removes user entry from database
    """
    venue_details = SHEET.worksheet("venues").get_all_values()
    act_details = SHEET.worksheet("standby").get_all_values()

    venue_item = venue_details.pop(1)
    orig_venue_list_len = len(venue_details)
    venue_list_index = 1

    act_item = act_details.pop(1)
    orig_standby_list_len = len(act_details)
    act_list_index = 1

    venue_name = venue_item[0]
    act_name = act_item[0]
    print("\nChecking list to remove entry!")
    while True:
        if user == "venue":
            if venue_name == user_id and day == venue_item[2]:
                print("\nListing Found\n")
                print(f"Removing {venue_name.title()} from database for {day}")
                SHEET.worksheet("venues").delete_rows(venue_list_index + 1)
                print("Sorry to see you go!")
                print("Returning to main menu")
                main()
            elif len(venue_details) >= 2:
                print("Still looking!")
                venue_item = venue_details.pop(1)
                venue_name = venue_item[0]
                venue_list_index = orig_venue_list_len - len(venue_details) + 1
                print(venue_list_index)
                print("Checking next item...")
                print("Venue name:", venue_item[0].title())
        elif user == "act":
            if act_name == user_id and day == act_item[2]:
                print("\nListing Found\n")
                print(act_list_index)
                print(f"Removing {act_name.title()} from database for {day}")
                SHEET.worksheet("standby").delete_rows(act_list_index + 1)
                print("Sorry to see you go!")
                print("Returning to main menu")
                main()
            elif len(venue_details) >= 2:
                print("Still looking!")
                print(user_id)
                act_item = act_details.pop(1)
                act_name = act_item[0]
                act_list_index = orig_standby_list_len - len(act_details) + 1
                print(act_list_index)
                print("Checking next item...")
                print("Act name:", act_item[0].title())
        else:
            print("No such listing! Returning to main menu!")
            main()
            exit()


def main():
    """
    Display Welcome message and get user type via menu options
    """
    while True:
        print("\nWelcome to Late Gigs! (North East)")
        print("The Last-Minute Booking Service for Live Music!\n")
        print("1. Find an act.")
        print("2. Find a venue.")
        print("3. About Late Gigs.")
        print("4. Remove user listing.\n")
        print("Choose the number from the options above and press enter")

        user_option = input("Enter your choice here: \n")

        if user_option == "1":
            clear_page()
            print("\nFind an Act... Ok Great! Let's get started!\n")
            user_is = "venue"
            area_check(user_is)
        elif user_option == "2":
            clear_page()
            print("\nFind a Venue... Ok Great! Let's get started!\n")
            user_is = "act"
            area_check(user_is)
        elif user_option == "3":
            clear_page()
            print("""\nLate Gigs is a last-minute booking service operating
throughout the North East of Ireland
\nRecently, almost every live music venue and act across
the region has been affected by a sudden gig cancellation due
to the ongoing Covid pandemic.
\nThis application has been designed to help pubs, clubs and
other venues as well as artists, bands and other acts
create gigs as quickly and efficiently as possible by firstly,
searching through a database of available acts and venues to
find a suitable match.
\nIf no match is initially found, Late Gigs will store
the users information on a waiting list that will
automatically create a gig for them if a match is found.
""")
            print("Why not give it a try!")
            input("Press Enter get started...\n")
            clear_page()
        elif user_option == "4":
            clear_page()
            remove_from_list()
        else:
            clear_page()
            print("\nInvalid option! Please type either 1, 2, 3 or 4\n")
            input("Press Enter to try again...\n")


main()
