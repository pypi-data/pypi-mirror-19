def index(self, value):
    """
    Return index of the first child containing the specified value.

    :param str value: text value to look for
    :returns: index of the first child containing the specified value
    :rtype: int
    :raises ValueError: if the value is not found
    """
    self.logger.info('getting index of "{}" within {}'.format(value, self._log_id_short))
    self.logger.debug('getting index of "{}" within page object; {}'.format(value, self._log_id_long))
    index = self.text_values.index(value)
    self.logger.info('index of "{}" within {} is {}'.format(value, self._log_id_short, index))
    self.logger.debug('index of "{}" within page object is {}; {}'.format(value, index, self._log_id_long))
    return index

