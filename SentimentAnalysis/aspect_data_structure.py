'''
Dataclass to describe the aspect and keep track of which rule was used to extract it 
'''

from dataclasses import dataclass, field


@dataclass
class Aspect:
    aspect: str
    rule: int = field(compare=False)
    sentiment: int = field(init=False, default=None, compare=False)

    def __repr__(self):
        return f"<Aspect - {self.aspect} | sentiment compound - {self.sentiment} |Rule {self.rule}>"

    def __str__(self):
        return self.__repr__()
