# from pprint import pprint
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


def area_check(user):
    """
    Ensure user is aware of Local Gigs catchment area
    before calling relevant get_(user)_data function
    """
    user_type = user
    while True:
        print("Just a quick check before we begin!")
        print("Please confirm you're in the North East Area!\n")

        if user_type == "venue":
            venue_location = input('Is your venue in the North East?:(y/n)\n')
            if venue_location == "y":
                print("\nOK, just making sure! Now let's Find you an act!\n")
                get_venue_data()
            else:
                print('Sorry, Late gigs only operates in the NE Area\n')
                input('Press Enter to exit to menu...\n')
                main()
        elif user_type == "artist":
            artist_location = input('Is your act in the North East?:(y/n)\n')
            if artist_location == "y":
                print("OK, just making sure! Now let's Find you a venue!\n")
            else:
                print("Sorry, That's not a valid option\n")
                input('Press Enter to exit to menu...\n')
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
        name = input('Enter your venue name here: ')
        if len(name) >= 2:
            venue_data.append(name.lower())
            break
        else:
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
        genre = input("Enter genre here: ")
        if genre in genre_list:
            venue_data.append(genre.lower())
            break
        else:
            print("\n")
            print(f'{genre} is not a valid genre')
            print("\nType one of the following options:")
            print("\nRock, Blues, Pop, Jazz, Metal, R&b,")
            print("Indie, Country or Irish trad \n")
            continue

    print("\nNice! Hopefully your patrons will be enjoying some")
    print(f"live {genre} at {name} soon!")
    print("\n")

    print("Lets keep going!?\n")
    print("What day this weekend do you need the act?")
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
            print("\n")
            print(f'{day} is not a valid gig day... Try again!')
            print("\nType one of the following options:\n")
            print("Friday, Saturday or Sunday")
            continue

    print("\nyExcellent! So far so good?")
    print("Here's what we have so far!\n")
    print(f"Your venue: {name} is looking for a {genre}")
    print(f"act for this coming {day}?")
    print("\n")

    while True:
        data_correct = input('Are you happy with this so far?:(y/n)\n')
        if data_correct == "y":
            print("\nOK cool! Now let's keep going!\n")
            break
        else:
            print("That's ok, lets try again\n")
            get_venue_data()
            main()

    print("Tell us how the maximum fee you are willing to pay your act.\n")
    print("Hint: Artist fees vary depending on many factors such as,")
    print("length of set, number of band members ect.\n")
    print("Aim to set your maximum fee between €200 and €600 to increase")
    print("your chances of finding a suitable act")
    while True:
        try:
            fee = int(input("Enter max fee here: €"))
        except ValueError:
            print("Nope! We need a number here... try again!")
            continue
        else:
            break

    venue_data.append(fee)
    print("\nOutstanding! We're almost there! \n")

    print("What is the maximum number of performers")
    print(f"{name} stage can hold?")
    print("\n")
    while True:
        try:
            members = int(input(
                "Type a number between 1 and the maximum required: "))
        except ValueError:
            print("Sorry, only a number will do in this case. Try again!")
            continue
        else:
            break

    venue_data.append(members)

    print("\nExcellent! Ok, just one last thing!\n")
    print("How long should the act play for?")
    print("\nExample: A two and a half hour set would be: 2.5 \n")

    exit()


def main():
    """
    Display Welcome message and get user type via menu options
    """
    while True:
        print("\nWelcome to Late Gigs!")
        print('The Last-Minute Booking Service for Live Music!\n')
        print('1. Find an Artist')
        print('2. Find A Venue')
        print('3. Exit\n')
        print('Choose the number from the options above and press enter')

        user_option = input('Enter your choice here: ')

        if user_option == '1':
            print('\nFind an Artist... Ok Great! Lets Get started!\n')
            user_is = "venue"
            area_check(user_is)
        elif user_option == '2':
            print('\nFind a Venue... Ok Great! Lets Get started!\n')
            user_is = "artist"
            area_check(user_is)
        elif user_option == '3':
            print('\nBetter luck next time... Be sure to check back soon!')
            exit()
        else:
            print('\nInvalid option! Please type either 1, 2, or 3\n')
            input('Press Enter to try again...\n')


main()
