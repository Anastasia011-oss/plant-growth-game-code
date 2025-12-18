class Mission:
    def __init__(self, mid, description, mtype, target, reward):
        self.id = mid
        self.description = description
        self.type = mtype
        self.target = target
        self.reward = reward
        self.progress = 0
        self.completed = False

    def add_progress(self, value=1):
        if self.completed:
            return False

        self.progress += value
        if self.progress >= self.target:
            self.completed = True
            return True
        return False