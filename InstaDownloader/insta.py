from instaloader import Instaloader, Profile

L = Instaloader()

def download(PROFILE, num):
    profile = Profile.from_username(L.context, PROFILE)
    posts_sorted_by_likes = sorted(profile.get_posts(), key=lambda post: post.likes, reverse=True)
    selected_range = posts_sorted_by_likes[:num]
    for post in selected_range:
        L.download_post(post, PROFILE)

PROFILE = input("Enter the profile name: ").strip()

if not PROFILE:
    print("Please enter a valid username.")
else:
    num = input("How many posts do you want to download? ")
    if not num.isdigit() or int(num) <= 0:
        print("Please enter a valid positive number.")
    else:
        download(PROFILE, int(num))
