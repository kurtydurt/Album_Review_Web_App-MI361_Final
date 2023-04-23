import musicbrainzngs



def album_search():
    musicbrainzngs.set_useragent('SWS_class_proj', '0.0', contact='kurtzma4@msu.edu')
    album_search = input("Search for an Album")
    result = musicbrainzngs.search_release_groups(album_search)
    search_dict = {}
    for i, album in enumerate(result['release-group-list']):
        if i == 51:
            break
        try:
            if album['primary-type'] == 'Album':
                search_dict[i] = album
                print(str(i) + ": " + u"{id} - {name}".format(id=album['title'], name=album['artist-credit'][0]['artist']['name']))
        except KeyError:
            pass

    return search_dict


class Profile:
    def __init__(self):
        self.username = input("\nEnter your new username:\n")
        self.password = input("\nPlease set your password:\n")
        self.reviews = {}
        self.review_count = 0

    def __repr__(self):
        return f"username: {self.username}\npassword: {self.password}\nThis user has {len(self.reviews)} reviews."

    def new_review(self):
        print(Review(self))


class Review:
    def __init__(self, profile: Profile):
        search_dict = album_search()
        inp = input("\n Choose an album to review:\n")
        if int(inp) in search_dict:
            album = search_dict[int(inp)]
            print(u"\nYou selected {id} - {name}".format(id=album['title'], name=album['artist-credit'][0]['artist']['name']))

        self.album_info = album
        self.title = album['title']
        self.artist = album['artist-credit'][0]['artist']['name']
        self.main_txt = input("Enter your review here:\n")
        self.rating = input("Enter your rating out of 10:\n")
        self.profile = profile
        profile.review_count += 1
        self.profile.reviews[profile.review_count] = self

    def __repr__(self):
        return f"{self.title} - {self.artist}\n{self.rating} out of 10.\n{self.main_txt}"


class Interface:
    def __init__(self):
        self.users = {}
        self.login()
        self.curr_user = None

    def login(self):
        log_on = input(
            "\nWelcome to SWS Album Review\nEnter your selection on the keyboard then press enter to confirm.\nPlease sign in or create an account:\n0: Sign In\n1: Create Account\n2: Exit\n")
        if log_on == '0':
            self.new_account()
        elif log_on == '1':
            user = Profile()
            self.users[user.username] = (user, user.password)
            self.curr_user = user
            print(f"\nAccount Created! Welcome to SWS, {user.username}.")
            self.main_page()
        elif log_on == '2':
            pass
        else:
            print("\nPlease indicate whether you'd like to sign in or make an account.")
            self.login()

    def new_account(self):
        username = input("\nEnter your username:\n")
        if username in self.users:
            pw = input("\nEnter your password:\n")
            user = self.users[username][0]
            if pw == user.password:
                self.curr_user = user
                print(f"\nSign in successful! Welcome back to SWS, {user.username}.\n")
                self.main_page()
            else:
                print("\nIncorrect Password.\n")
                self.new_account()
        else:
            print("User not found.")
            self.login()

    def main_page(self):
        inp = input(
            f"\nUser: {self.curr_user.username}\n0:Create a new review\n1:Show My Reviews\n2:Search Users\n3:Log Off\n")
        if inp == '0':
            self.curr_user.new_review()
            self.main_page()
        elif inp == '1':
            self.list_reviews(self.curr_user)
        elif inp == '2':
            self.list_users()
        elif inp == '3':
            print(f"\nPeace out, {self.curr_user.username}.\n")
            self.curr_user = None
            self.login()
        else:
            print("\nPlease choose a valid option.\n")
            self.main_page()

    def list_reviews(self, profile):
        # add search functionality
        print(f"\nHere are all of {profile.username}'s reviews:\n")
        if profile.review_count == 0:
            print("\nThis user has no reviews yet. Check back soon!\n")
            self.main_page()
        for review in profile.reviews:
            print(str(review) + " - " + profile.reviews[review].album)
        inp = input(f"\n0:Return to main menu\nEnter the corresponding number to read the review:\n")
        if inp == '0':
            self.main_page()
        else:
            try:
                print(profile.reviews[int(inp)])
                self.list_reviews(profile)
            except KeyError:
                print("\nReview number not found. Try another.")
                self.list_reviews(profile)

    def list_users(self):
        for user in self.users:
            print(user + ": " + str(self.users[user][0].review_count) + " reviews.\n")









if __name__ == '__main__':
    y = Interface()
