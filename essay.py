class Essay(object):
    def __init__(self, id):
        self.id = id
        self.T = ""
        self.prompt = ""
        self.overall_score = 0
        self.number_tlm = 0
        self.number_cm = 0
        self.text = ""

    def __str__(self):
        return (f'Id: {self.id}, T: {self.T}, prompt: {self.prompt}, '
                f'score: {self.overall_score}, tlms: {self.number_tlm}, '
                f'cms: {self.number_cm}.')
