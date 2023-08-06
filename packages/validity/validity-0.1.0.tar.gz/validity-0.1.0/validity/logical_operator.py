

class Base(object):
    """
    Base class.
    """

    def get_error(self, value):
        """
        check value end return error description if value is not valid.
        If value is valid returns None
        :param value: value fo check
        :return: None of value is valid. condition text if value is not valid
        :rtype: None or str
        """
        return None if self.is_valid(value) else self.get_condition_text()

    def is_valid(self, value):
        """
        check if given value is valid
        :param value: value for checking
        :type value: object
        :return: true if value is valid
        :rtype: bool
        """
        raise NotImplementedError()

    def get_condition_text(self):
        """
        get condition text representation.
        :return: condition text representation
        :rtype: str
        """
        raise NotImplementedError()

    def __str__(self):
        return self.get_condition_text()

    def __unicode__(self):
        return self.get_condition_text()

    def Or(self, *args):
        # pylint: disable=invalid-name
        if not len(args):
            raise ValueError("at least one operand must be specified")
        return Or(self, *args)

    def And(self, *args):
        # pylint: disable=invalid-name
        if not len(args):
            raise ValueError("at least one operand must be specified")
        return And(self, *args)

    def Not(self):
        # pylint: disable=invalid-name
        return Not(self)

    def is_valid(self, value):
        raise NotImplementedError()

    def get_condition_text(self):
        raise NotImplementedError()


class BaseLogicalOperator(Base):
    """
    Base logical operator class
    """

    _condition_template = "base logical operator. always falls. operands={operands}"
    operands = None

    def __init__(self, *operands):
        if not len(operands):
            raise ValueError("at least one operand must be specified")

        if not all([isinstance(operand, Base) for operand in operands]):
            raise ValueError("all operands mast be instances of validity.Base class")

        self.operands = operands

    def get_condition_text(self):
        return self._condition_template.format(operands=self.get_operands_text())

    def get_operands_text(self):
        return ", ".join([str(operand) for operand in self.operands])

    def is_valid(self, value):
        raise NotImplementedError("operator must implement 'is_valid(self, value)' method")


class Or(BaseLogicalOperator):
    _condition_template = "({operands})"

    def is_valid(self, value):
        # return any([operand.is_valid(value) for operand in self.operands])
        for operand in self.operands:
            if operand.is_valid(value):
                return True
        return False

    def get_operands_text(self):
        return " OR ".join([str(operand) for operand in self.operands])


class And(BaseLogicalOperator):
    _condition_template = "({operands})"

    def is_valid(self, value):
        return all([operand.is_valid(value) for operand in self.operands])

    def get_operands_text(self):
        return " AND ".join([str(operand) for operand in self.operands])


class Not(BaseLogicalOperator):
    _condition_template = "NOT({operands})"

    def __init__(self, condition):
        super(Not, self).__init__(condition)

    def is_valid(self, value):
        for operand in self.operands:
            if not operand.is_valid(value):
                return True
        return False

    def get_operands_text(self):
        return str(self.operands[0])
