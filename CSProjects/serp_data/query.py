class Query:
    def __init__(self, start_date, end_date, num_of_obs, category,query_text):
        self.start_date = start_date
        self.end_date = end_date
        self.num_of_obs = num_of_obs
        self.category = category
        self.query_text = query_text
