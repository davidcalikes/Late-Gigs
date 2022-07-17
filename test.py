def test_members():
    while True:
        members = 15
        if 0 <= members <= 15:
            print("In Range")
            exit()
        else:
            print("not in range")
            exit()


def test_members_code():
    while True:
        try:
            members = int(input("""
            Type the number of performers in your act: \n
            """))
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


def test_set_length():
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


# def get_match_email(match_email):
#     """
#     Check's the database for any available venues
#     that match user requirements.
#     """
#     user_data_sheet = SHEET.worksheet("user_details").get_all_values()

#     print(len(user_data_sheet))
#     user_item = user_data_sheet.pop(1)
#     user_name = user_item[0]
#     print(user_name)

#     while True:
#         if match_email == user_name:
#             print("\nEmail Found\n")
#             print("Name:", user_item[0].title())
#             item_list_index = len(user_data_sheet) + 1
#             print(item_list_index)
#         elif len(user_data_sheet) >= 2:
#             user_item = user_data_sheet.pop(1)
#             print("next item is", user_item)
#             print("Venue name:", user_item[0].title())
#         else:
#             print("Error... match email not found!")
#             exit()
