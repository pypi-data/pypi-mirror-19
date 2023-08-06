from .logical_operator import Base


class BaseComparator(Base):
    """
    Base comparator class
    """
    _condition_template = 'base comparator. operand={operand}'
    operand = None

    def __init__(self, operand):
        self.operand = operand

    def get_condition_text(self):
        return self._condition_template.format(operand=self.operand)

    def is_valid(self, value):
        raise NotImplementedError("comparator must implement 'is_valid(self, value)' method")


class GT(BaseComparator):
    """
    Greater then comparator
    use it for check that value > operand

    :example:

    GT(10).is_valid(5)  # False
    GT(10).get_error(5) # must be greater than 10
    """
    _condition_template = "must be greater than {operand}"

    def is_valid(self, value):
        return value > self.operand


class GTE(BaseComparator):
    """
    Greater then or equal to comparator
    use it for check that value >= operand

    :example:

    GTE(10).is_valid(5)  # False
    GTE(10).get_error(5) # must be greater or equal to 10
    """

    _condition_template = "must be greater than or equal to {operand}"

    def is_valid(self, value):
        return value >= self.operand


class LT(BaseComparator):
    """
    less then comparator
    use it for check that value < operand

    :example:

    LT(10).is_valid(50)  # False
    LT(10).get_error(50) # must be less than 10
    """
    _condition_template = "must be less than {operand}"

    def is_valid(self, value):
        return value < self.operand


class LTE(BaseComparator):
    """
    less then or equal comparator
    use it for check that value <= operand

    :example:

    LTE(10).is_valid(50)  # False
    LTE(10).get_error(50) # must be less than or equal to 10
    """

    _condition_template = "must be less than or equal to {operand}"

    def is_valid(self, value):
        return value <= self.operand


class EQ(BaseComparator):
    """
    equal comparator
    use it for check that value = operand

    :example:

    EQ(10).is_valid(50)  # False
    EQ(10).get_error(50) # must be equal to 10
    """
    _condition_template = "must be equal to {operand}"

    def is_valid(self, value):
        return value == self.operand


class NotEQ(BaseComparator):
    """
    NOT equal comparator
    use it for check that value <> operand

    :example:

    NotEQ(10).is_valid(10)  # False
    NotEQ(10).get_error(10) # must NOT be equal to 10
    """

    _condition_template = "must NOT be equal to {operand}"

    def is_valid(self, value):
        return not value == self.operand


class Any(BaseComparator):
    # TODO: rename to In ?
    # TODO: tests

    _condition_template = "must be any of ({operands})"

    def __init__(self, *values):
        if len(values) == 1 and isinstance(values[0], (list, tuple)):
            values = values[0]
        super(Any, self).__init__(operand=values)

    def is_valid(self, value):
        return value in self.operand

    def get_condition_text(self):
        return self._condition_template.format(operands=", ".join(str(item) for item in self.operand))

# just aliases
# In = Any
# AnyOf = In


class Between(BaseComparator):
    _condition_template = "must be between {min_value} and {max_value}"

    def __init__(self, min_value, max_value):
        super(Between, self).__init__(operand=(min_value, max_value))

    def is_valid(self, value):
        return self.operand[0] <= value <= self.operand[1]

    def get_condition_text(self):
        return self._condition_template.format(min_value=self.operand[0], max_value=self.operand[1])


