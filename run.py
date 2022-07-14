# from pprint import pprint
import os
import gspread
from google.oauth2.service_account import Credentials

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
                print("\nOK, just making sure! Now let's find you an act!\n")
                get_venue_data()
            else:
                clear_page()
                print("Sorry, Late gigs only operates in the NE Area\n")
                input("Press Enter to exit to menu...\n")
                main()
        elif user_type == "act":
            act_location = input("Is your act in the North East?:(y/n)\n")
            if act_location == "y":
                clear_page()
                print("OK, just making sure! Now let's find you a venue!\n")
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
    print(f"live {genre} at {name} soon!")
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
    print(f"Your venue: '{name}' is looking for a {genre}")
    print(f"act for this coming {day}?")
    print("\n")

    while True:
        data_correct = input("Are you happy to continue?:(y/n)\n")
        if data_correct == "y":
            clear_page()
            print("\nOK cool! Now let's keep going!\n")
            break
        else:
            clear_page()
            print("That's ok, let's try again\n")
            get_venue_data()
            main()

    print("Tell us the maximum fee you are willing to pay your act.\n")
    print("Hint: Act fees vary depending on many factors, such as")
    print("length of set, number of band members ect.\n")
    print("Aim to set your maximum fee between €200 and €600 to increase")
    print("your chances of finding a suitable act\n")
    while True:
        try:
            fee = int(input("Enter max fee in € here: \n"))
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
    print(f"the stage at {name} can hold?")
    print("\n")
    while True:
        members = input("Type a number between 1 and the maximum required: \n")
        try:
            members = int(members)
        except ValueError:
            clear_page()
            print("Sorry, only a number will do in this case. Try again!")
            continue
        if 1 < members:
            break
        else:
            print("Number must be more than 0. Try again!")

    venue_data.append(members)
    clear_page()

    print("\nExcellent! Ok, just one last thing!\n")
    print("How long should the act play for?")
    print("\nExample: A two and a half hour set would be: 2.5 \n")
    while True:
        try:
            set_length = float(input("Enter length of set required: \n"))
        except ValueError:
            clear_page()
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
    print(f" with {members} member(s)")
    print(f"that will play for {set_length} hours")
    print(f"for a fee of no more than €{fee}")
    print("\n")

    properties = venue_data
    user = "venue"

    while True:
        print("Would you like to search the database for a suitable act?\n")

        data_ver = input("Confirm search?:(y/n)\n")
        if data_ver == "y":
            clear_page()
            print("\nOK, just making sure! Now let's find you an act!\n")
            check_database(properties, user)
        elif data_ver == "n":
            print("Are you sure don't want to proceed?")
            print("All data will be lost!\n")
            confirm_no = input(
                "Type 'y' to return to menu or 'n' to search database:\n")
            if confirm_no == "y":
                main()
            else:
                check_database(properties, user)
        else:
            clear_page()
            print("Sorry invalid input, please type either 'y' or 'n'")
            continue

    check_database(properties, user)

    exit()


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
    print(f"Cool! What genre of music does {name} mostly play?")
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
    print(f"Nice! Hopefully fans of {name} will be enjoying some")
    print(f"live {genre} this weekend!")
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
    print(f"Your act: '{name}' is looking for a {genre}")
    print(f"venue for this coming {day}?")
    print("\n")

    while True:
        data_correct = input(
            "Is this correct? Are you happy to continue?:(y/n)\n")
        if data_correct == "y":
            clear_page()
            print("\nOK cool! Now let's keep going!\n")
            break
        else:
            clear_page()
            print("That's ok, let's try again\n")
            get_venue_data()
            main()

    print("Tell us the minimum fee you will accept per gig.\n")
    print("Hint: Artist fees generally range between €200 and €600")
    print("Aim to set your minimum fee within this range to increase")
    print("your chances of finding a suitable venue\n")
    while True:
        try:
            fee = int(input("Enter min fee in € here: \n"))
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
        members = input("Type a number between 1 and the maximum required: \n")
        try:
            members = int(members)
        except ValueError:
            clear_page()
            print("Sorry, only a number will do in this case. Try again!")
            continue
        if 1 < members:
            break
        else:
            print("Number must be more than 0. Try again!")

    act_data.append(members)
    clear_page()

    print("\nExcellent! Ok, just one last thing!\n")
    print(f"What is the typical set length of a {name} gig?")
    print("\nExample: A two and a half hour set would be: 2.5 \n")
    while True:
        try:
            set_length = float(input("Enter length of set required: \n"))
        except ValueError:
            clear_page()
            print("Whoopsie! This value needs to be a number. Try again!")
            continue
        else:
            break
    act_data.append(set_length)
    clear_page()
    print("\n")
    print(f"All done! Here's the gig requirements for {name}:")
    print("\n")
    print(f"You are a {genre} act with no more than")
    print(f"{members} member(s) looking for a gig on {day}")
    print(f"that will play for {set_length} hours")
    print(f"for a fee of no less than €{fee}")
    print("\n")

    properties = act_data
    user = "act"

    while True:
        print("Would you like to search the database for a suitable venue?\n")

        data_ver = input("Confirm search?:(y/n)\n")
        if data_ver == "y":
            clear_page()
            print("\nOK, just making sure! Now let's find you an venue!\n")
            check_database(properties, user)
        elif data_ver == "n":
            print("Are you sure don't want to proceed?")
            print("All data will be lost!\n")
            confirm_no = input(
                "Type 'y' to return to menu or 'n' to search database:\n")
            if confirm_no == "y":
                main()
            else:
                check_database(properties, user)
        else:
            clear_page()
            print("Sorry invalid input, please type either 'y' or 'n'")
            continue

    check_database(properties, user)


def check_database(properties, user):
    """
    Check's the database for any object instances
    that match the users requirements.
    """
    print("\nUser is...", user)
    print("\n")
    print("Looking for match in relevant database...\n")

    while True:
        if user == "venue":
            check_standby_list(properties, user)
        elif user == "act":
            check_venue_list(properties, user)
        else:
            print("Whoops! Something went wrong... returning to main menu")
            main()


def check_standby_list(properties, user):
    """
    Check's the database for any available acts
    that match user requirements.
    """
    acts = SHEET.worksheet("standby").get_all_values()

    print(len(acts))
    item = acts.pop(1)
    venue_name = properties[0]
    print(venue_name)
    check_list = properties
    print(check_list)
    orig_list_len = len(acts)
    print(orig_list_len)

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
            print("Name:", item[0].title())
            act_name = item[0]
            item_list_index = orig_list_len - len(acts) + 1
            print("List Index =", item_list_index)
            act_day = item[2]
            act_fee = item[3]
            act_set_len = float(item[5])
            make_gig(item_list_index, act_name, venue_name,
                     act_day, act_genre, act_fee, user)
        elif len(acts) >= 2:
            item = acts.pop(1)
            print("next item is", item)
            act_genre = (item[1])
            act_day = item[2]
            act_fee = int(item[3])
            act_members = int(item[4])
            act_set_len = float(item[5])
            act_conv = [act_genre, act_day, act_fee, act_members, act_set_len]
            print("Act name:", item[0].title())
        else:
            print("End of List... no matches")
            exit()

    print("venue details:", venue_conv)
    print("act details", act_conv)
    print(user)
    exit()


def check_venue_list(properties, user):
    """
    Check's the database for any available venues
    that match user requirements.
    """
    venues = SHEET.worksheet("venues").get_all_values()

    print(len(venues))
    item = venues.pop(1)
    act_name = properties[0]
    print(act_name)
    check_list = properties
    print(check_list)
    orig_list_len = len(venues)
    print(orig_list_len)

    venue_genre = item[1]
    venue_day = item[2]
    venue_fee = int(item[3])
    venue_members = int(item[4])
    venue_set_len = float(item[5])

    venue_conv = [venue_genre, venue_day, venue_fee, venue_members,
                  venue_set_len]
    print(venue_conv)

    act_genre = check_list[1]
    act_day = check_list[2]
    act_fee = int(check_list[3])
    act_members = int(check_list[4])
    act_set_len = float(check_list[5])

    act_conv = [act_genre, act_day, act_fee, act_members,
                act_set_len]
    print(act_conv)

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
            make_gig(item_list_index, act_name, venue_name,
                     venue_day, venue_genre, venue_fee, user)
        elif len(venues) >= 2:
            item = venues.pop(1)
            print("next item is", item)
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
            exit()


def make_gig(item_list_index, act_name, venue_name,
             user_day, user_genre, user_fee, user):
    """
    Adds match to gig database and removes act from standby sheet
    """
    while True:
        user_choice = input('Do you want to create this gig?:(y/n)\n')
        properties = [act_name, venue_name, user_day, user_genre, user_fee]
        item_index = item_list_index
        print("DB index =", item_index)
        if user_choice == "y" and user == "venue":
            print("\nBooya! Lets do it... Updating Databases!\n")
            print(f"removing {act_name.title()} from standby list")
            print("Updating gig listings...")
            SHEET.worksheet("gig_list").append_row(properties)
            print("Success!")
            exit()
        elif user_choice == "y" and user == "act":
            print(f"removing {venue_name.title()} from waiting list")
            print("Updating gig listings...")
            SHEET.worksheet("gig_list").append_row(properties)
            print("Success!")
            exit()


def update_data_sheet(properties, user):
    """
    Updates relevant data sheet for venues or artists
    """
    if user == "venue":
        print("\nUpdating venue database...\n")
        print(properties, user)
    elif user == "artist":
        print("\nUpdating standby database...\n")
        print(properties, user)
    else:
        print("Error! I guess I gotta go pick a whole bunch of")
        print("whoopsie daisies!")
        main()

    print(user.title(), "database updated succesfully!")
    print("Thank you for using Late Gigs!\n")
    print("A gig will be created Automatically if")
    print("we find you an act in the coming days!\n")
    exit()


def main():
    """
    Display Welcome message and get user type via menu options
    """
    while True:
        print("\nWelcome to Late Gigs!")
        print("The Last-Minute Booking Service for Live Music!\n")
        print("1. Find an Act")
        print("2. Find A Venue")
        print("3. Exit\n")
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
            print("\nBetter luck next time... Be sure to check back soon!")
            exit()
        else:
            clear_page()
            print("\nInvalid option! Please type either 1, 2, or 3\n")
            input("Press Enter to try again...\n")


main()
