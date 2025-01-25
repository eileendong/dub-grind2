

class Husky:
    def __init__(self, name="Husky"):
        self.name = name
        self.happiness = 100
        self.health = 100
        self.energy = 100
        self.daily_goal = 0  # Daily study goal in hours
        self.studied_today = 0  # Hours studied today

    def study(self, hours):
        self.studied_today += hours
        self.happiness = min(100, self.happiness + hours * 5)
        self.health = min(100, self.health + hours * 4)
        self.energy = min(100, self.energy + hours * 3)

    def decay(self):
        if self.studied_today < self.daily_goal:
            self.happiness = max(0, self.happiness - 10)
            self.health = max(0, self.health - 8)
            self.energy = max(0, self.energy - 5)

    def reset_daily_study(self):
        self.studied_today = 0


# Dictionary to store Husky stats for each user
user_huskies = {}


# Helper function to get or create a Husky for a user
def get_user_husky(ctx):
    user_id = ctx.author.id
    display_name = ctx.author.display_name
    if user_id not in user_huskies:
        user_huskies[user_id] = Husky(name=f"{display_name}'s Husky")
    return user_huskies[user_id]
