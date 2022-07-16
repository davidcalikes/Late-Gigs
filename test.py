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


test_members_code()
