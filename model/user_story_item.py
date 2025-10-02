class UserStoryItem:
    def __init__(self, uid, title, content, criteria):
        self.uid = uid
        self.title = title
        self.content = content
        self.criteria = criteria

    @property
    def full_description(self):
        return (
            self.content
            + "\n\nAcceptance Criteria:\n"
            + self.criteria
        )
