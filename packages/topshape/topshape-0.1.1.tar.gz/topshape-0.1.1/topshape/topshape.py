"""
This is the main topshape module.

Classes exported here:
 * TopShapeError: application-specific exception class
 * KeyHandler: handles keyboard interactions
 * EdgeText: handles drawing of the edge sections (Header, Footer)
 * BodyBox: handles drawing of the body of the application.
 * TopShape: main class for interacting with topshape
"""

from collections import namedtuple
from urwid import AttrMap, Text, CENTER, LEFT, RIGHT, Columns, ListBox,\
    SimpleListWalker, Frame, MainLoop, ExitMainLoop, Filler

ALIGNMENT_MAP = {'left': LEFT,
                 'right': RIGHT,
                 'center': CENTER}


class TopShapeError(Exception):
    """topshape's application-specific exception"""

    pass


class KeyHandler(namedtuple('KeyHandler', 'app key_map')):
    """Class for handling keypresses."""

    def handle(self, key):
        """
        Handle a single keypress.

        :param key: the key that got pressed
        :type key: str
        """
        if key == 'h':
            self.app.enter_help()
            return

        if (key == 'q' or key == 'esc') and self.app.on_help():
            self.app.exit_help()
            return

        method = self.key_map.get(key)
        if method is None:
            return
        method(self.app)
        self.app.draw_screen()


class EdgeText(Text):
    """Class of widget used to display the header and footer."""

    def __init__(self, func):
        """
        Initialize the object.

        :param func: function that returns text to be displayed
        :type func: function
        """
        super(EdgeText, self).__init__('')
        self.func = func
        self._cache = None

    def cache_update(self):
        """Update the cache."""
        self._cache = self.func()

    def update(self):
        """Update the text to be displayed."""
        self.set_text(self._cache)


class BodyBox(ListBox):
    """Class of widget that displays the body."""

    def __init__(self, columns, func, sorting_column=None,
                 default_column_size=10, default_column_alignment='center',
                 default_column_order='desc'):
        """
        Initialize the object.

        :param columns: tuple (or list) of columns. Each column is a dict
                        with keys 'label', 'size', 'alignment' and 'order'.
                        Only 'label' is required.
        :type columns: tuple (or list) of dicts
        :param func: generator function that returns tuples (or lists) of str
                     objects.
        :type func: function
        :param sorting_column: sorting column
        :type sorting_column: str
        :param default_column_size: default column size
        :type default_column_size: int
        :param default_column_alignment: default column alignment
        :type default_column_alignment: str
        :param default_column_order: default column order. 'asc' or 'desc'
        :type default_column_order: str
        """
        super(BodyBox, self).__init__(SimpleListWalker([]))
        if len(columns) == 0:
            raise TopShapeError('You need at least one column.')
        self.default_column_size = default_column_size
        self.default_column_alignment = default_column_alignment
        self.default_column_order = default_column_order
        self.columns = columns
        self.func = func
        self.sorting_column = sorting_column or columns[0]['label']
        self._cache = None

    def _sort_key(self, row):
        """
        Sorting key function for rows.

        :param row: a row
        :type row: tuple (or list)
        :return: value of the current sorting column in row
        :rtype: str
        """
        index = self.column_names.index(self.sorting_column)
        for _type in (int, float):
            try:
                return _type(row[index])
            except ValueError:
                pass
        return row[index]

    @property
    def sorting_column(self):
        """
        Return the current sorting column.

        :return: current sorting column
        :rtype: str
        """
        return self._sorting_column

    @sorting_column.setter
    def sorting_column(self, sorting_column):
        """
        Set the current sorting column

        :param sorting_column: column name
        :type sorting_column: str
        """
        if sorting_column not in self.column_names:
            raise TopShapeError('Not a valid body column name.')
        self._sorting_column = sorting_column

    @property
    def column_names(self):
        """
        Return the column names.

        :return: column names
        :rtype: list of str
        """
        return [column['label'] for column in self.columns]

    @property
    def columns(self):
        """
        Return the columns.

        :return: the columns
        :rtype: list of tuples
        """
        return self._columns

    @columns.setter
    def columns(self, columns):
        """
        Set the columns.

        :param columns: the columns to store
        :type columns: list (or tuple) of tuples
        """
        self._columns = []

        for column in columns:
            new_column = {'size': self.default_column_size,
                          'alignment': self.default_column_alignment,
                          'order': self.default_column_order}

            new_column.update(column)

            if 'label' not in new_column.keys():
                raise TopShapeError('Column {} is missing the \'label\' '
                                    'key.'.format(str(new_column)))

            self._columns.append(new_column)

    def cache_update(self):
        """Update the cache."""
        self._cache = self.func()

    def update(self):
        """Update the state of the BodyBox object."""
        columns = []
        for column in self.columns:
            label, size, alignment, _ = [column[key] for key in
                                         ('label',
                                          'size',
                                          'alignment',
                                          'order')]
            columns.append((size, AttrMap(Text(('reversed', label),
                                               align=ALIGNMENT_MAP[alignment],
                                               wrap='clip'),
                                          'reversed')))

        # Set the column headers
        self.body[:] = [AttrMap(Columns(columns, 1), 'reversed')]

        column_index = self.column_names.index(self.sorting_column)
        reverse = self.columns[column_index]['order'] == 'desc'
        for row in sorted(self._cache, key=self._sort_key, reverse=reverse):
            columns = []
            for index, column in enumerate(self.columns):
                columns.append((column['size'], Text(row[index],
                                                     align=ALIGNMENT_MAP[
                                                         column['alignment']],
                                                     wrap='clip')))
            self.body.append(Columns(columns, 1))

    def move_sort_right(self):
        """
        Move the sorting column to the right of the current sorting column.
        If the current column is the rightmost column, this results in a no-op.
        """
        index = self.column_names.index(self.sorting_column)
        if index == len(self.column_names)-1:  # we're at the rightmost column
            return
        self.sorting_column = self.column_names[index+1]
        self.update()

    def move_sort_left(self):
        """
        Move the sorting column to the left of the current sorting column.
        If the current column is the leftmost column, this results in a no-op.
        """
        index = self.column_names.index(self.sorting_column)
        if index == 0:  # we're at the leftmost column
            return
        self.sorting_column = self.column_names[index-1]
        self.update()


class TopShape(MainLoop):
    """
    Main class for interacting with topshape.

    You instantiate an object of this class by calling the
    TopShape.create_app() function.
    """

    def __init__(self, frame, key_mapping, refresh_rate, help_text):
        """
        Initialize the object.

        :param frame: frame object
        :type frame: Frame
        :param key_mapping: maps keys to key handler functions
        :type key_mapping: dict
        :param refresh_rate: refresh rate (in seconds)
        :type refresh_rate: int
        :param help_text: text to display in help widget
        :type help_text: str
        """
        self.refresh_rate = refresh_rate
        self.frame = frame
        self._key_handler = KeyHandler(self, key_mapping)
        self.help_text = help_text
        self._saved_widget = None

        palette = [('reversed', 'black', 'light gray')]
        super(TopShape, self).__init__(
            self.frame, palette,
            unhandled_input=self._key_handler.handle)

    def cache_update(self):
        """Call cache_update() on all widgets."""
        self.frame.header.cache_update()
        self.frame.body.cache_update()
        self.frame.footer.cache_update()

        self.set_alarm_in(self.refresh_rate,
                          lambda x, y: self.cache_update())

    def update(self):
        """
        Update the state of the TopShape object and set the next update event.
        """
        self.frame.header.update()
        self.frame.body.update()
        self.frame.footer.update()

        self.set_alarm_in(self.refresh_rate,
                          lambda x, y: self.update())

    def run(self):
        """Run the application loop."""
        self.cache_update()
        self.update()
        super(TopShape, self).run()

    def enter_help(self):
        """Cause the help output to be displayed."""
        if self.on_help():
            return
        self._saved_widget = self.widget
        self.widget = Filler(Text(self.help_text), 'top')

    def exit_help(self):
        """Cause the help output to disappear."""
        if not self.on_help():
            return
        self.widget = self._saved_widget
        self._saved_widget = None

    def on_help(self):
        """
        Return whether or not we are currently displaying the help screen.

        :return: True if help screen is currently displayed, False otherwise.
        :rtype: bool
        """
        return isinstance(self.widget, Filler)

    def move_sort_right(self):
        """
        Move the sorting column to the right. Results in no-op if current
        sorting column is the rightmost column.
        """
        if self.on_help():
            return
        self.widget.body.move_sort_right()

    def move_sort_left(self):
        """
        Move the sorting column to the left. Results in no-op if current
        sorting column is the leftmost column.
        """
        if self.on_help():
            return
        self.widget.body.move_sort_left()

    @staticmethod
    def exit():
        """Causes main loop to exit."""
        raise ExitMainLoop()

    @classmethod
    def create_app(cls, columns, body_func, header_func=None,
                   footer_func=None, key_mapping=None, refresh_rate=2,
                   sorting_column=None, help_text=None):
        """
        Function that creates the TopShape object.

        :param columns: tuple (or list) of columns. Each column is a dict
                        with keys 'label', 'size', 'alignment' and 'order'.
                        Only 'label' is required and must be a string.
                        'size' must be an integer and is a number of
                        characters. 'alignment' must be one of 'center',
                        'right' or 'left'. 'order' must be either
                        'asc' or 'desc'
        :type columns: tuple (or list) of dicts
        :param body_func: function that returns tuples (or lists) of strings
                          to be displayed in the body. Each item in the tuple
                          must correspond to a column defined in columns.
                          This function will be called for every iteration of
                          the loop.
        :type body_func: function
        :param header_func: function that returns a string that will be the
                            content of the header section. If not specified,
                            there will be no header section. This function will
                            be called for every iteration of the loop.
        :type header_func: function
        :param footer_func: function that returns a string that will be the
                            content of the footer section. If not specified,
                            there will be no footer section. This function will
                            be called for every iteration of the loop.
        :type footer_func: function
        :param key_mapping: maps keypresses to functions. When a key is
                            pressed the corresponding function will be called
                            with the the TopShape object as an argument.
                            If key_mapping is None, the mapping will be set to
                            {'q': lambda app: app.exit()}.
        :type key_mapping: dict
        :param refresh_rate: period of the loop in seconds.
        :type refresh_rate: int
        :param sorting_column: name of column to sort by. Must exist in
                               columns.
        :type sorting_column: str
        :param help_text: text to be displayed in the help output.
        :type help_text: str
        :return: the TopShape object
        :rtype: TopShape
        """

        header = EdgeText(header_func)
        body = BodyBox(columns, body_func, sorting_column)
        footer = EdgeText(footer_func)
        frame = Frame(body, header, footer)

        if key_mapping is None:
            key_mapping = {'q': lambda app: app.exit()}
        help_text = help_text or ''

        return cls(frame, key_mapping, refresh_rate, help_text)
