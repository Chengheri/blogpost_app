class Task:
    def __init__(self, topic:str, num_words:int=100):
        self.topic = topic
        self.num_words = num_words

    def get_task(self):
        return f'''
        Write a concise but engaging blogpost about
        {self.topic}. Make sure the blogpost is
        within {self.num_words} words.
    '''