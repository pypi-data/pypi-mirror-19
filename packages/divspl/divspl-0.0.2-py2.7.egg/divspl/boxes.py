from rply.token import BaseBox


class MainBox(BaseBox):
    def __init__(self, range_box, assignments):
        self.range_box = range_box
        self.assignments = assignments

    def eval(self):
        lines = []
        for i in self.range_box.range():
            line = ""
            for assignment in self.assignments.foobar():
                line += assignment.eval_with(i)
            lines.append(line or str(i))
        return "\n".join(lines) + "\n"


class AssignmentBox(BaseBox):
    def __init__(self, word_token, number_token):
        self.word_token = word_token
        self.number_token = number_token

    def eval_with(self, i):
        if not i % self.number_token.int():
            return self.word_token.str()
        return ''


class AssignmentsBox(BaseBox):
    def __init__(self, assignments_box=None, assignment_box=None):
        self.assignments_box = assignments_box
        self.assignment_box = assignment_box

    def foobar(self):
        if self.assignments_box:
            return self.assignments_box.foobar() + [self.assignment_box]
        return []


class RangeBox(BaseBox):
    def __init__(self, low_token, high_token):
        self.low_token = low_token
        self.high_token = high_token

    def range(self):
        return range(self.low_token.int(), self.high_token.int() + 1)


class IntBox(BaseBox):
    def __init__(self, value):
        self.value = int(value.getstr())

    def int(self):
        return self.value


class WordBox(BaseBox):
    def __init__(self, value):
        self.value = value.getstr()

    def str(self):
        return self.value
