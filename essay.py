"""This class initializes each essay as an object
and is used by the class corpus."""


class Essay(object):
    """This class initializes an essay object with an id.
    Subsequently, more info for each essay can be added, namely
    whether the essay was written at the beginning (T1) or end (T2)
    of the schoolyear, as well as the prompt, the overall raters' score
    the numbers of metaphors (tlms and cms) and the essay's text."""
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
                f'cms: {self.number_cm}, essay text: {self.text}.\n')
