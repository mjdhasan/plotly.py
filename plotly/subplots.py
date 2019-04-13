# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Constants
# ---------
# Subplot types that are each individually positioned with a domain
#
# Each of these subplot types has a `domain` property with `x`/`y`
# properties.
# Note that this set does not contain `xaxis`/`yaxis` because these behave a
# little differently.
import collections

_subplot_types = {'scene', 'geo', 'polar', 'ternary', 'mapbox'}

# For most subplot types, a trace is associated with a particular subplot
# using a trace property with a name that matches the subplot type. For
# example, a `scatter3d.scene` property set to `'scene2'` associates a
# scatter3d trace with the second `scene` subplot in the figure.
#
# There are a few subplot types that don't follow this pattern, and instead
# the trace property is just named `subplot`.  For example setting
# the `scatterpolar.subplot` property to `polar3` associates the scatterpolar
# trace with the third polar subplot in the figure
_subplot_prop_named_subplot = {'polar', 'ternary', 'mapbox'}


# Named tuple to hold an xaxis/yaxis pair that represent a single subplot
SubplotXY = collections.namedtuple('SubplotXY', ('xaxis', 'yaxis'))
SubplotDomain = collections.namedtuple('SubplotDomain', ('x', 'y'))


def _get_initial_max_subplot_ids():
    max_subplot_ids = {subplot_type: 0
                       for subplot_type in _subplot_types}
    max_subplot_ids['xaxis'] = 0
    max_subplot_ids['yaxis'] = 0
    return max_subplot_ids


def make_subplots(
        rows=1,
        cols=1,
        shared_xaxes=False,
        shared_yaxes=False,
        start_cell='top-left',
        print_grid=True,
        horizontal_spacing=None,
        vertical_spacing=None,
        subplot_titles=None,
        column_widths=None,
        row_heights=None,
        specs=None,
        insets=None,
        column_titles=None,
        row_titles=None,
        x_title=None,
        y_title=None,
        **kwargs
):
    """
    Return an instance of plotly.graph_objs.Figure with predefined subplots
    configured in 'layout'.

    Parameters
    ----------
    rows: int (default 1)
        Number of rows in the subplot grid. Must be greater than zero.

    cols: int (default 1)
        Number of columns in the subplot grid. Must be greater than zero.

    shared_xaxes: boolean or str (default False)
        Assign shared (linked) x-axes for 2D cartesian subplots

          - True or 'columns': Share axes among subplots in the same column
          - 'rows': Share axes among subplots in the same row
          - 'all': Share axes across all subplots in the grid.

    shared_yaxes: boolean or str (default False)
        Assign shared (linked) y-axes for 2D cartesian subplots

          - 'columns': Share axes among subplots in the same column
          - True or 'rows': Share axes among subplots in the same row
          - 'all': Share axes across all subplots in the grid.

    start_cell: 'bottom-left' or 'top-left' (default 'top-left')
        Choose the starting cell in the subplot grid used to set the
        domains_grid of the subplots.

          - 'top-left': Subplots are numbered with (1, 1) in the top
                        left corner
          - 'bottom-left': Subplots are numbererd with (1, 1) in the bottom
                           left corner

    print_grid: boolean (default True):
        If True, prints a string representation of the plot grid.  Grid may
        also be printed using the `Figure.print_grid()` method on the
        resulting figure.

    horizontal_spacing: float (default 0.2 / cols)
        Space between subplot columns in normalized plot coordinates. Must be
        a float between 0 and 1.

        Applies to all columns (use 'specs' subplot-dependents spacing)

    vertical_spacing: float (default 0.3 / rows)
        Space between subplot rows in normalized plot coordinates. Must be
        a float between 0 and 1.

        Applies to all rows (use 'specs' subplot-dependents spacing)

    subplot_titles: list of str or None (default None)
        Title of each subplot as a list in row-major ordering.

        Empty strings ("") can be included in the list if no subplot title
        is desired in that space so that the titles are properly indexed.

    specs: list of lists of dictionaries or None (default None)
        Per subplot specifications of subplot type, row/column spanning, and
        spacing.

        ex1: specs=[[{}, {}], [{'colspan': 2}, None]]

        ex2: specs=[[{'rowspan': 2}, {}], [None, {}]]

        - Indices of the outer list correspond to subplot grid rows
          starting from the top, if start_cell='top-left',
          or bottom, if start_cell='bottom-left'.
          The number of rows in 'specs' must be equal to 'rows'.

        - Indices of the inner lists correspond to subplot grid columns
          starting from the left. The number of columns in 'specs'
          must be equal to 'cols'.

        - Each item in the 'specs' list corresponds to one subplot
          in a subplot grid. (N.B. The subplot grid has exactly 'rows'
          times 'cols' cells.)

        - Use None for a blank a subplot cell (or to move past a col/row span).

        - Note that specs[0][0] has the specs of the 'start_cell' subplot.

        - Each item in 'specs' is a dictionary.
            The available keys are:
            * type (string, default 'xy'): Subplot type. One of
                - 'xy': 2D Cartesian subplot type for scatter, bar, etc.
                - 'scene': 3D Cartesian subplot for scatter3d, cone, etc.
                - 'polar': Polar subplot for scatterpolar, barpolar, etc.
                - 'ternary': Ternary subplot for scatterternary
                - 'mapbox': Mapbox subplot for scattermapbox
                - 'domain': Subplot type for traces that are individually
                            positioned. pie, parcoords, parcats, etc.
            * colspan (int, default 1): number of subplot columns
                for this subplot to span.
            * rowspan (int, default 1): number of subplot rows
                for this subplot to span.
            * l (float, default 0.0): padding left of cell
            * r (float, default 0.0): padding right of cell
            * t (float, default 0.0): padding right of cell
            * b (float, default 0.0): padding bottom of cell

        - Note: Use 'horizontal_spacing' and 'vertical_spacing' to adjust
          the spacing in between the subplots.

    insets: list of dictionaries or None (default None):
        Inset specifications.  Insets are subplots that overlay grid subplots

        - Each item in 'insets' is a dictionary.
            The available keys are:

            * cell (tuple, default=(1,1)): (row, col) index of the
                subplot cell to overlay inset axes onto.
            * type (string, default 'xy'): Subplot type
            * l (float, default=0.0): padding left of inset
                  in fraction of cell width
            * w (float or 'to_end', default='to_end') inset width
                  in fraction of cell width ('to_end': to cell right edge)
            * b (float, default=0.0): padding bottom of inset
                  in fraction of cell height
            * h (float or 'to_end', default='to_end') inset height
                  in fraction of cell height ('to_end': to cell top edge)

    column_widths: list of numbers or None (default None)
        list of length `cols` of the relative widths of each column of suplots.
        Values are normalized internally and used to distribute overall width
        of the figure (excluding padding) among the columns.

        For backward compatibility, may also be specified using the
        `column_width` keyword argument.

    row_heights: list of numbers or None (default None)
        list of length `rows` of the relative heights of each row of subplots.
        If start_cell='top-left' then row heights are applied top to bottom.
        Otherwise, if start_cell='bottom-left' then row heights are applied
        bottom to top.

        For backward compatibility, may also be specified using the
        `row_width` kwarg. If specified as `row_width`, then the width values
        are applied from bottom to top regardless of the value of start_cell.
        This matches the legacy behavior of the `row_width` argument.

    column_titles: list of str or None (default None)
        list of length `cols` of titles to place above the top subplot in
        each column.

    row_titles: list of str or None (default None)
        list of length `rows` of titles to place on the right side of each
        row of subplots. If start_cell='top-left' then row titles are
        applied top to bottom. Otherwise, if start_cell='bottom-left' then
        row titles are applied bottom to top.

    x_title: str or None (default None)
        Title to place below the bottom row of subplots,
        centered horizontally

    y_title: str or None (default None)
        Title to place to the left of the left column of subplots,
       centered vertically

    Examples
    --------
    Example 1:
    # Stack two subplots vertically, and add a scatter trace to each
    >>> from plotly.subplots import make_subplots
    ... import plotly.graph_objs as go
    ... fig = tools.make_subplots(rows=2)

    This is the format of your plot grid:
    [ (1,1) xaxis1,yaxis1 ]
    [ (2,1) xaxis2,yaxis2 ]

    >>> fig.add_scatter(y=[2, 1, 3], row=1, col=1)
    ... fig.add_scatter(y=[1, 3, 2], row=2, col=1)

    # or see Figure.append_trace

    Example 2:
    # Stack a scatter plot
    >>> fig = make_subplots(rows=2, shared_xaxes=True)

    This is the format of your plot grid:
    [ (1,1) xaxis1,yaxis1 ]
    [ (2,1) xaxis2,yaxis2 ]

    >>> fig.add_scatter(y=[2, 1, 3], row=1, col=1)
    ... fig.add_scatter(y=[1, 3, 2], row=2, col=1)

    Example 3:
    # irregular subplot layout (more examples below under 'specs')
    fig = tools.make_subplots(rows=2, cols=2,
                              specs=[[{}, {}],
                                     [{'colspan': 2}, None]])

    This is the format of your plot grid:
    [ (1,1) xaxis1,yaxis1 ]  [ (1,2) xaxis2,yaxis2 ]
    [ (2,1) xaxis3,yaxis3           -              ]

    >>> fig.add_trace(go.Scatter(x=[1,2,3], y=[2,1,2]), row=1, col=1)
    ... fig.add_trace(go.Scatter(x=[1,2,3], y=[2,1,2]), row=1, col=2)
    ... fig.add_trace(go.Scatter(x=[1,2,3], y=[2,1,2]), row=2, col=1)

    Example 4:
    # insets
    >>> fig = make_subplots(insets=[{'cell': (1,1), 'l': 0.7, 'b': 0.3}])

    This is the format of your plot grid:
    [ (1,1) xaxis1,yaxis1 ]

    With insets:
    [ xaxis2,yaxis2 ] over [ (1,1) xaxis1,yaxis1 ]

    >>> fig.add_scatter(x=[1,2,3], y=[2,1,1])
    ... fig.add_scatter(x=[1,2,3], y=[2,1,2], xaxis='x2', yaxis='y2')

    Example 5:
    # include subplot titles
    >>> fig = make_subplots(rows=2, subplot_titles=('Plot 1','Plot 2'))

    This is the format of your plot grid:
    [ (1,1) x1,y1 ]
    [ (2,1) x2,y2 ]

    >>> fig.add_scatter(x=[1,2,3], y=[2,1,2], row=1, col=1)
    >>> fig.add_bar(x=[1,2,3], y=[2,1,2], row=2, col=1)

    Example 6:
    Subplot with mixed subplot types

    >>> fig = make_subplots(rows=2, cols=2,
    ...                     specs=[[{'type': 'xy'},    {'type': 'polar'}],
    ...                            [{'type': 'scene'}, {'type': 'ternary'}]])

    >>> fig.add_traces(
    ...     [go.Scatter(y=[2, 3, 1]),
    ...      go.Scatterpolar(r=[1, 3, 2], theta=[0, 45, 90]),
    ...      go.Scatter3d(x=[1, 2, 1], y=[2, 3, 1], z=[0, 3, 5]),
    ...      go.Scatterternary(a=[0.1, 0.2, 0.1],
    ...                        b=[0.2, 0.3, 0.1],
    ...                        c=[0.7, 0.5, 0.8])],
    ...     rows=[1, 1, 2, 2],
    ...     cols=[1, 2, 1, 2])
    """

    # Make sure we're in future subplots mode
    from _plotly_future_ import _future_flags
    if 'v4_subplots' not in _future_flags:
        raise ValueError("""
plotly.subplots.make_subplots may only be used in the
v4_subplots _plotly_future_ mode.  To try it out, run

>>> from _plotly_future_ import v4_subplots

before importing plotly.
""")

    import plotly.graph_objs as go

    # Handle backward compatibility
    # -----------------------------
    use_legacy_row_heights_order = 'row_width' in kwargs
    row_heights = kwargs.pop('row_width', row_heights)
    column_widths = kwargs.pop('column_width', column_widths)

    if kwargs:
        raise TypeError(
            'make_subplots() got unexpected keyword argument(s): {}'
            .format(list(kwargs)))

    # Validate coerce inputs
    # ----------------------
    #  ### rows ###
    if not isinstance(rows, int) or rows <= 0:
        raise ValueError("""
The 'rows' argument to make_suplots must be an int greater than 0.
    Received value of type {typ}: {val}""".format(
            typ=type(rows), val=repr(rows)))

    #  ### cols ###
    if not isinstance(cols, int) or cols <= 0:
        raise ValueError("""
The 'cols' argument to make_suplots must be an int greater than 0.
    Received value of type {typ}: {val}""".format(
            typ=type(cols), val=repr(cols)))

    # ### start_cell ###
    if start_cell == 'bottom-left':
        col_dir = 1
        row_dir = 1
    elif start_cell == 'top-left':
        col_dir = 1
        row_dir = -1
    else:
        raise ValueError("""
The 'start_cell` argument to make_subplots must be one of \
['bottom-left', 'top-left']
    Received value of type {typ}: {val}""".format(
            typ=type(start_cell), val=repr(start_cell)))

    # ### horizontal_spacing ###
    if horizontal_spacing is None:
        horizontal_spacing = 0.2 / cols

    # ### vertical_spacing ###
    if vertical_spacing is None:
        if subplot_titles:
            vertical_spacing = 0.5 / rows
        else:
            vertical_spacing = 0.3 / rows

    # ### subplot titles ###
    if not subplot_titles:
        subplot_titles = [""] * rows * cols

    # ### column_widths ###
    if row_titles:
        # Add a little breathing room between row labels and legend
        max_width = 0.98
    else:
        max_width = 1.0
    if column_widths is None:
        widths = [(max_width - horizontal_spacing * (cols - 1)) / cols] * cols
    elif isinstance(column_widths, (list, tuple)) and len(column_widths) == cols:
        cum_sum = float(sum(column_widths))
        widths = []
        for w in column_widths:
            widths.append(
                (max_width - horizontal_spacing * (cols - 1)) * (w / cum_sum)
            )
    else:
        raise ValueError("""
The 'column_widths' argument to make_suplots must be a list of numbers of \
length {cols}.
    Received value of type {typ}: {val}""".format(
            cols=cols, typ=type(cols), val=repr(column_widths)))

    # ### row_heights ###
    if row_heights is None:
        heights = [(1. - vertical_spacing * (rows - 1)) / rows] * rows
    elif isinstance(row_heights, (list, tuple)) and len(row_heights) == rows:
        cum_sum = float(sum(row_heights))
        heights = []
        for h in row_heights:
            heights.append(
                (1. - vertical_spacing * (rows - 1)) * (h / cum_sum)
            )
        if row_dir < 0 and not use_legacy_row_heights_order:
            heights = list(reversed(heights))
    else:
        raise ValueError("""
The 'row_heights' argument to make_suplots must be a list of numbers of \
length {rows}.
    Received value of type {typ}: {val}""".format(
            rows=rows, typ=type(cols), val=repr(row_heights)))

    # ### Helper to validate coerce elements of lists of dictionaries ###
    def _check_keys_and_fill(name, arg, defaults):
        def _checks(item, defaults):
            if item is None:
                return
            if not isinstance(item, dict):
                raise ValueError("""
Elements of the '{name}' argument to make_suplots must be dictionaries \
or None.
    Received value of type {typ}: {val}""".format(
                    name=name, typ=type(item), val=repr(item)
                ))

            for k in item:
                if k not in defaults:
                    raise ValueError("""
Invalid key specified in an element of the '{name}' argument to \
make_subplots: {k}
    Valid keys include: {valid_keys}""".format(
                        k=repr(k), name=name,
                        valid_keys=repr(list(defaults))
                    ))
            for k, v in defaults.items():
                item.setdefault(k, v)

        for arg_i in arg:
            if isinstance(arg_i, (list, tuple)):
                # 2D list
                for arg_ii in arg_i:
                    _checks(arg_ii, defaults)
            elif isinstance(arg_i, dict):
                # 1D list
                _checks(arg_i, defaults)

    # ### specs ###
    if specs is None:
        specs = [[{} for c in range(cols)] for r in range(rows)]
    elif not (
            isinstance(specs, (list, tuple))
            and specs
            and all(isinstance(row, (list, tuple)) for row in specs)
            and len(specs) == rows
            and all(len(row) == cols for row in specs)
            and all(all(v is None or isinstance(v, dict)
                        for v in row)
                    for row in specs)
    ):
        raise ValueError("""
The 'specs' argument to make_subplots must be a 2D list of dictionaries with \
dimensions ({rows} x {cols}).
    Received value of type {typ}: {val}""".format(
            rows=rows, cols=cols, typ=type(specs), val=repr(specs)
        ))

    # For backward compatibility, convert is_3d flag to type='scene' kwarg
    for row in specs:
        for spec in row:
            if spec and spec.pop('is_3d', None):
                spec['type'] = 'scene'

    spec_defaults = dict(
        type='xy',
        colspan=1,
        rowspan=1,
        l=0.0,
        r=0.0,
        b=0.0,
        t=0.0,
    )
    _check_keys_and_fill('specs', specs, spec_defaults)

    # ### insets ###
    if insets is None or insets is False:
        insets = []
    elif not (
            isinstance(insets, (list, tuple)) and
            all(isinstance(v, dict) for v in insets)
    ):
        raise ValueError("""
The 'insets' argument to make_suplots must be a list of dictionaries.
    Received value of type {typ}: {val}""".format(
            typ=type(insets), val=repr(insets)))

    if insets:
        for inset in insets:
            if inset and inset.pop('is_3d', None):
                inset['type'] = 'scene'

        inset_defaults = dict(
            cell=(1, 1),
            type='xy',
            l=0.0,
            w='to_end',
            b=0.0,
            h='to_end'
        )
        _check_keys_and_fill('insets', insets, inset_defaults)

    # ### shared_xaxes / shared_yaxes
    valid_shared_vals = [None, True, False, 'rows', 'cols', 'all']
    shared_err_msg = """
The {arg} argument to make_subplots must be one of: {valid_vals}
    Received value of type {typ}: {val}"""

    if shared_xaxes not in valid_shared_vals:
        val = shared_xaxes
        raise ValueError(shared_err_msg.format(
            arg='shared_xaxes',
            valid_vals=valid_shared_vals,
            typ=type(val),
            val=repr(val)
        ))
    if shared_yaxes not in valid_shared_vals:
        val = shared_yaxes
        raise ValueError(shared_err_msg.format(
            arg='shared_yaxes',
            valid_vals=valid_shared_vals,
            typ=type(val),
            val=repr(val)
        ))

    # ### column_titles / row_titles ###
    if column_titles and not isinstance(column_titles, (list, tuple)):
        raise ValueError("""
The column_titles argument to make_subplots must be a list or tuple
    Received value of type {typ}: {val}""".format(
            typ=type(column_titles), val=repr(column_titles)))

    if row_titles and not isinstance(row_titles, (list, tuple)):
        raise ValueError("""
The row_titles argument to make_subplots must be a list or tuple
    Received value of type {typ}: {val}""".format(
            typ=type(row_titles), val=repr(row_titles)))



    # Init layout
    # -----------
    layout = go.Layout()

    # Build grid reference
    # --------------------
    # Built row/col sequence using 'row_dir' and 'col_dir'
    col_seq = range(cols)[::col_dir]
    row_seq = range(rows)[::row_dir]

    # Build 2D array of tuples of the start x and start y coordinate of each
    # subplot
    grid = [
        [
            (
                (sum(widths[:c]) + c * horizontal_spacing),
                (sum(heights[:r]) + r * vertical_spacing)
            ) for c in col_seq
        ] for r in row_seq
    ]

    domains_grid = [[None for _ in range(cols)] for _ in range(rows)]

    # Initialize subplot reference lists for the grid and insets
    grid_ref = [[None for c in range(cols)] for r in range(rows)]

    list_of_domains = []  # added for subplot titles

    max_subplot_ids = _get_initial_max_subplot_ids()

    # Loop through specs -- (r, c) <-> (row, col)
    for r, spec_row in enumerate(specs):
        for c, spec in enumerate(spec_row):

            if spec is None:  # skip over None cells
                continue

            # ### Compute x and y domain for subplot ###
            c_spanned = c + spec['colspan'] - 1  # get spanned c
            r_spanned = r + spec['rowspan'] - 1  # get spanned r

            # Throw exception if 'colspan' | 'rowspan' is too large for grid
            if c_spanned >= cols:
                raise Exception("Some 'colspan' value is too large for "
                                "this subplot grid.")
            if r_spanned >= rows:
                raise Exception("Some 'rowspan' value is too large for "
                                "this subplot grid.")

            # Get x domain using grid and colspan
            x_s = grid[r][c][0] + spec['l']

            x_e = grid[r][c_spanned][0] + widths[c_spanned] - spec['r']
            x_domain = [x_s, x_e]

            # Get y domain (dep. on row_dir) using grid & r_spanned
            if row_dir > 0:
                y_s = grid[r][c][1] + spec['b']
                y_e = grid[r_spanned][c][1] + heights[r_spanned] - spec['t']
            else:
                y_s = grid[r_spanned][c][1] + spec['b']
                y_e = grid[r][c][1] + heights[-1 - r] - spec['t']
            y_domain = [y_s, y_e]

            list_of_domains.append(x_domain)
            list_of_domains.append(y_domain)

            domains_grid[r][c] = [x_domain, y_domain]

            # ### construct subplot container ###
            subplot_type = spec['type']
            grid_ref_element = _init_subplot(
                layout, subplot_type, x_domain, y_domain, max_subplot_ids)
            grid_ref_element['spec'] = spec
            grid_ref[r][c] = grid_ref_element

    _configure_shared_axes(layout, grid_ref, 'x', shared_xaxes, row_dir)
    _configure_shared_axes(layout, grid_ref, 'y', shared_yaxes, row_dir)

    # Build inset reference
    # ---------------------
    # Loop through insets
    insets_ref = [None for inset in range(len(insets))] if insets else None
    if insets:
        for i_inset, inset in enumerate(insets):

            r = inset['cell'][0] - 1
            c = inset['cell'][1] - 1

            # Throw exception if r | c is out of range
            if not (0 <= r < rows):
                raise Exception("Some 'cell' row value is out of range. "
                                "Note: the starting cell is (1, 1)")
            if not (0 <= c < cols):
                raise Exception("Some 'cell' col value is out of range. "
                                "Note: the starting cell is (1, 1)")

            # Get inset x domain using grid
            x_s = grid[r][c][0] + inset['l'] * widths[c]
            if inset['w'] == 'to_end':
                x_e = grid[r][c][0] + widths[c]
            else:
                x_e = x_s + inset['w'] * widths[c]
            x_domain = [x_s, x_e]

            # Get inset y domain using grid
            y_s = grid[r][c][1] + inset['b'] * heights[-1 - r]
            if inset['h'] == 'to_end':
                y_e = grid[r][c][1] + heights[-1 - r]
            else:
                y_e = y_s + inset['h'] * heights[-1 - r]
            y_domain = [y_s, y_e]

            list_of_domains.append(x_domain)
            list_of_domains.append(y_domain)

            subplot_type = inset['type']

            inset_ref_element = _init_subplot(
                layout, subplot_type, x_domain, y_domain, max_subplot_ids)

            insets_ref[i_inset] = inset_ref_element

    # Build grid_str
    # This is the message printed when print_grid=True
    grid_str = _build_grid_str(specs, grid_ref, insets, insets_ref, row_seq)

    # Add subplot titles
    plot_title_annotations = _build_subplot_title_annotations(
        subplot_titles,
        list_of_domains,
    )

    layout['annotations'] = plot_title_annotations

    # Add column titles
    if column_titles:
        domains_list = []
        if row_dir > 0:
            for c in range(cols):
                domain_pair = domains_grid[-1][c]
                if domain_pair:
                    domains_list.extend(domain_pair)
        else:
            for c in range(cols):
                domain_pair = domains_grid[0][c]
                if domain_pair:
                    domains_list.extend(domain_pair)

        # Add subplot titles
        column_title_annotations = _build_subplot_title_annotations(
            column_titles,
            domains_list,
        )

        layout['annotations'] += tuple(column_title_annotations)

    if row_titles:
        domains_list = []
        if row_dir < 0:
            rows_iter = range(rows - 1, -1, -1)
        else:
            rows_iter = range(rows)

        for r in rows_iter:
            domain_pair = domains_grid[r][-1]
            if domain_pair:
                domains_list.extend(domain_pair)

        # Add subplot titles
        column_title_annotations = _build_subplot_title_annotations(
            row_titles,
            domains_list,
            title_edge='right'
        )

        layout['annotations'] += tuple(column_title_annotations)

    if x_title:
        domains_list = [(0, max_width), (0, 1)]

        # Add subplot titles
        column_title_annotations = _build_subplot_title_annotations(
            [x_title],
            domains_list,
            title_edge='bottom',
            offset=30
        )

        layout['annotations'] += tuple(column_title_annotations)

    if y_title:
        domains_list = [(0, 1), (0, 1)]

        # Add subplot titles
        column_title_annotations = _build_subplot_title_annotations(
            [y_title],
            domains_list,
            title_edge='left',
            offset=40
        )

        layout['annotations'] += tuple(column_title_annotations)

    # Handle displaying grid information
    if print_grid:
        print(grid_str)

    # Build resulting figure
    fig = go.Figure(layout=layout)

    # Attach subpot grid info to the figure
    fig.__dict__['_grid_ref'] = grid_ref
    fig.__dict__['_grid_str'] = grid_str

    return fig


def _configure_shared_axes(layout, grid_ref, x_or_y, shared, row_dir):
    rows = len(grid_ref)
    cols = len(grid_ref[0])

    layout_key_ind = ['x', 'y'].index(x_or_y)

    if row_dir < 0:
        rows_iter = range(rows-1, -1, -1)
    else:
        rows_iter = range(rows)

    def update_axis_matches(first_axis_id, ref, remove_label):
        if ref is None:
            return first_axis_id

        if x_or_y == 'x':
            span = ref['spec']['colspan']
        else:
            span = ref['spec']['rowspan']

        if ref['subplot_type'] == 'xy' and span == 1:
            if first_axis_id is None:
                first_axis_name = ref['layout_keys'][layout_key_ind]
                first_axis_id = first_axis_name.replace('axis', '')
            else:
                axis_name = ref['layout_keys'][layout_key_ind]
                axis_to_match = layout[axis_name]
                axis_to_match.matches = first_axis_id
                if remove_label:
                    axis_to_match.showticklabels = False

        return first_axis_id

    if shared == 'columns' or (x_or_y == 'x' and shared is True):
        for c in range(cols):
            first_axis_id = None
            ok_to_remove_label = x_or_y == 'x'
            for r in rows_iter:
                ref = grid_ref[r][c]
                first_axis_id = update_axis_matches(
                    first_axis_id, ref, ok_to_remove_label)

    elif shared == 'rows' or (x_or_y == 'y' and shared is True):
        for r in rows_iter:
            first_axis_id = None
            ok_to_remove_label = x_or_y == 'y'
            for c in range(cols):
                ref = grid_ref[r][c]
                first_axis_id = update_axis_matches(
                    first_axis_id, ref, ok_to_remove_label)

    elif shared == 'all':
        first_axis_id = None
        for c in range(cols):
            for ri, r in enumerate(rows_iter):
                ref = grid_ref[r][c]

                if x_or_y == 'y':
                    ok_to_remove_label = c > 0
                else:
                    ok_to_remove_label = ri > 0 if row_dir > 0 else r < rows - 1

                first_axis_id = update_axis_matches(
                    first_axis_id, ref, ok_to_remove_label)


def _init_subplot_xy(
        layout, x_domain, y_domain, max_subplot_ids=None
):
    if max_subplot_ids is None:
        max_subplot_ids = _get_initial_max_subplot_ids()

    # Get axis label and anchor
    x_cnt = max_subplot_ids['xaxis'] + 1
    y_cnt = max_subplot_ids['yaxis'] + 1

    # Compute x/y labels (the values of trace.xaxis/trace.yaxis
    x_label = "x{cnt}".format(cnt=x_cnt)
    y_label = "y{cnt}".format(cnt=y_cnt)

    # Anchor x and y axes to each other
    x_anchor, y_anchor = y_label, x_label

    # Build layout.xaxis/layout.yaxis containers
    xaxis_name = 'xaxis{cnt}'.format(cnt=x_cnt)
    yaxis_name = 'yaxis{cnt}'.format(cnt=y_cnt)
    x_axis = {'domain': x_domain, 'anchor': x_anchor}
    y_axis = {'domain': y_domain, 'anchor': y_anchor}

    layout[xaxis_name] = x_axis
    layout[yaxis_name] = y_axis

    ref_element = {
        'subplot_type': 'xy',
        'layout_keys': (xaxis_name, yaxis_name),
        'trace_kwargs': {'xaxis': x_label, 'yaxis': y_label}
    }

    # increment max_subplot_ids
    max_subplot_ids['xaxis'] = x_cnt
    max_subplot_ids['yaxis'] = y_cnt

    return ref_element


def _init_subplot_single(
        layout, subplot_type, x_domain, y_domain, max_subplot_ids=None
):
    if max_subplot_ids is None:
        max_subplot_ids = _get_initial_max_subplot_ids()

    # Add scene to layout
    cnt = max_subplot_ids[subplot_type] + 1
    label = '{subplot_type}{cnt}'.format(subplot_type=subplot_type, cnt=cnt)
    scene = dict(domain={'x': x_domain, 'y': y_domain})
    layout[label] = scene

    trace_key = ('subplot'
                 if subplot_type in _subplot_prop_named_subplot
                 else subplot_type)

    ref_element = {
        'subplot_type': subplot_type,
        'layout_keys': (label,),
        'trace_kwargs': {trace_key: label}}

    # increment max_subplot_id
    max_subplot_ids['scene'] = cnt

    return ref_element


def _init_subplot_domain(x_domain, y_domain):
    # No change to layout since domain traces are labeled individually
    ref_element = {
        'subplot_type': 'domain',
        'layout_keys': (),
        'trace_kwargs': {'domain': {'x': x_domain, 'y': y_domain}}}

    return ref_element


def _init_subplot(
        layout, subplot_type, x_domain, y_domain, max_subplot_ids=None
):
    if max_subplot_ids is None:
        max_subplot_ids = _get_initial_max_subplot_ids()

    # Clamp domain elements between [0, 1].
    # This is only needed to combat numerical precision errors
    # See GH1031
    x_domain = [max(0.0, x_domain[0]), min(1.0, x_domain[1])]
    y_domain = [max(0.0, y_domain[0]), min(1.0, y_domain[1])]

    if subplot_type == 'xy':
        ref_element = _init_subplot_xy(
            layout, x_domain, y_domain, max_subplot_ids
        )
    elif subplot_type in _subplot_types:
        ref_element = _init_subplot_single(
            layout, subplot_type, x_domain, y_domain, max_subplot_ids
        )
    elif subplot_type == 'domain':
        ref_element = _init_subplot_domain(x_domain, y_domain)
    else:
        raise ValueError('Invalid subplot type {subplot_type}'
                         .format(subplot_type=subplot_type))

    return ref_element


def _get_cartesian_label(x_or_y, r, c, cnt):
    # Default label (given strictly by cnt)
    label = "{x_or_y}{cnt}".format(x_or_y=x_or_y, cnt=cnt)
    return label


def _build_subplot_title_annotations(
        subplot_titles,
        list_of_domains,
        title_edge='top',
        offset=0
):

    # If shared_axes is False (default) use list_of_domains
    # This is used for insets and irregular layouts
    # if not shared_xaxes and not shared_yaxes:
    x_dom = list_of_domains[::2]
    y_dom = list_of_domains[1::2]
    subtitle_pos_x = []
    subtitle_pos_y = []

    if title_edge == 'top':
        text_angle = 0
        xanchor = 'center'
        yanchor = 'bottom'

        for x_domains in x_dom:
            subtitle_pos_x.append(sum(x_domains) / 2.0)
        for y_domains in y_dom:
            subtitle_pos_y.append(y_domains[1])

        yshift = offset
        xshift = 0
    elif title_edge == 'bottom':
        text_angle = 0
        xanchor = 'center'
        yanchor = 'top'

        for x_domains in x_dom:
            subtitle_pos_x.append(sum(x_domains) / 2.0)
        for y_domains in y_dom:
            subtitle_pos_y.append(y_domains[0])

        yshift = -offset
        xshift = 0
    elif title_edge == 'right':
        text_angle = 90
        xanchor = 'left'
        yanchor = 'middle'

        for x_domains in x_dom:
            subtitle_pos_x.append(x_domains[1])
        for y_domains in y_dom:
            subtitle_pos_y.append(sum(y_domains) / 2.0)

        yshift = 0
        xshift = offset
    elif title_edge == 'left':
        text_angle = -90
        xanchor = 'right'
        yanchor = 'middle'

        for x_domains in x_dom:
            subtitle_pos_x.append(x_domains[0])
        for y_domains in y_dom:
            subtitle_pos_y.append(sum(y_domains) / 2.0)

        yshift = 0
        xshift = -offset
    else:
        raise ValueError("Invalid annotation edge '{edge}'"
                         .format(edge=title_edge))

    plot_titles = []
    for index in range(len(subplot_titles)):
        if not subplot_titles[index] or index >= len(subtitle_pos_y):
            pass
        else:
            annot = {
                'y': subtitle_pos_y[index],
                'xref': 'paper',
                'x': subtitle_pos_x[index],
                'yref': 'paper',
                'text': subplot_titles[index],
                'showarrow': False,
                'font': dict(size=16),
                'xanchor': xanchor,
                'yanchor': yanchor,
            }

            if xshift != 0:
                annot['xshift'] = xshift

            if yshift != 0:
                annot['yshift'] = yshift

            if text_angle != 0:
                annot['textangle'] = text_angle

            plot_titles.append(annot)
    return plot_titles


def _build_grid_str(specs, grid_ref, insets, insets_ref, row_seq):

    # Compute rows and columns
    rows = len(specs)
    cols = len(specs[0])

    # Initialize constants
    sp = "  "  # space between cell
    s_str = "[ "  # cell start string
    e_str = " ]"  # cell end string

    s_top = '⎡ '  # U+23A1
    s_mid = '⎢ '  # U+23A2
    s_bot = '⎣ '  # U+23A3

    e_top = ' ⎤'  # U+23A4
    e_mid = ' ⎟'  # U+239F
    e_bot = ' ⎦'  # U+23A6

    colspan_str = '       -'  # colspan string
    rowspan_str = '       :'  # rowspan string
    empty_str = '    (empty) '  # empty cell string
    # Init grid_str with intro message
    grid_str = "This is the format of your plot grid:\n"

    # Init tmp list of lists of strings (sorta like 'grid_ref' but w/ strings)
    _tmp = [['' for c in range(cols)] for r in range(rows)]

    # Define cell string as function of (r, c) and grid_ref
    def _get_cell_str(r, c, ref):
        ref_str = ','.join(ref['layout_keys'])
        return '({r},{c}) {ref}'.format(
            r=r + 1,
            c=c + 1,
            ref=ref_str)

    # Find max len of _cell_str, add define a padding function
    cell_len = max([len(_get_cell_str(r, c, ref))
                    for r, row_ref in enumerate(grid_ref)
                    for c, ref in enumerate(row_ref)
                    if ref]) + len(s_str) + len(e_str)

    def _pad(s, cell_len=cell_len):
        return ' ' * (cell_len - len(s))

    # Loop through specs, fill in _tmp
    for r, spec_row in enumerate(specs):
        for c, spec in enumerate(spec_row):

            ref = grid_ref[r][c]
            if ref is None:
                if _tmp[r][c] == '':
                    _tmp[r][c] = empty_str + _pad(empty_str)
                continue

            if spec['rowspan'] > 1:
                cell_str = s_top + _get_cell_str(r, c, ref)
            else:
                cell_str = s_str + _get_cell_str(r, c, ref)

            if spec['colspan'] > 1:
                for cc in range(1, spec['colspan'] - 1):
                    _tmp[r][c + cc] = colspan_str + _pad(colspan_str)

                if spec['rowspan'] > 1:
                    _tmp[r][c + spec['colspan'] - 1] = \
                        (colspan_str + _pad(colspan_str + e_str)) + e_top
                else:
                    _tmp[r][c + spec['colspan'] - 1] = \
                        (colspan_str + _pad(colspan_str + e_str)) + e_str
            else:
                padding = ' ' * (cell_len - len(cell_str) - 2)
                if spec['rowspan'] > 1:
                    cell_str += padding + e_top
                else:
                    cell_str += padding + e_str

            if spec['rowspan'] > 1:
                for cc in range(spec['colspan']):
                    for rr in range(1, spec['rowspan']):
                        row_str = rowspan_str + _pad(rowspan_str)
                        if cc == 0:
                            if rr < spec['rowspan'] - 1:
                                row_str = s_mid + row_str[2:]
                            else:
                                row_str = s_bot + row_str[2:]

                        if cc == spec['colspan'] - 1:
                            if rr < spec['rowspan'] - 1:
                                row_str = row_str[:-2] + e_mid
                            else:
                                row_str = row_str[:-2] + e_bot

                        _tmp[r + rr][c + cc] = row_str

            _tmp[r][c] = cell_str + _pad(cell_str)

    # Append grid_str using data from _tmp in the correct order
    for r in row_seq[::-1]:
        grid_str += sp.join(_tmp[r]) + '\n'

    # Append grid_str to include insets info
    if insets:
        grid_str += "\nWith insets:\n"
        for i_inset, inset in enumerate(insets):
            r = inset['cell'][0] - 1
            c = inset['cell'][1] - 1
            ref = grid_ref[r][c]

            grid_str += (
                    s_str + ','.join(insets_ref[i_inset]['layout_keys']) + e_str +
                    ' over ' +
                    s_str + _get_cell_str(r, c, ref) + e_str + '\n'
            )
    return grid_str


def _set_trace_grid_reference(trace, layout, grid_ref, row, col):
    if row <= 0:
        raise Exception("Row value is out of range. "
                        "Note: the starting cell is (1, 1)")
    if col <= 0:
        raise Exception("Col value is out of range. "
                        "Note: the starting cell is (1, 1)")
    try:
        ref = grid_ref[row - 1][col - 1]
    except IndexError:
        raise Exception("The (row, col) pair sent is out of "
                        "range. Use Figure.print_grid to view the "
                        "subplot grid. ")

    if ref is None:
        raise ValueError("""
No subplot specified at grid position ({row}, {col})""".format(
            row=row,
            col=col
        ))

    for k in ref['trace_kwargs']:
        if k not in trace:
            raise ValueError("""\
Trace type '{typ}' is not compatible with subplot type '{subplot_type}'
at grid position ({row}, {col}) 

See the docstring for the specs argument to plotly.subplots.make_subplot 
for more information on subplot types""".format(
                typ=trace.type,
                subplot_type=ref['subplot_type'],
                row=row,
                col=col
            ))

    # Update trace reference
    trace.update(ref['trace_kwargs'])


def _get_grid_subplot(fig, row, col):
    # Make sure we're in future subplots mode
    from _plotly_future_ import _future_flags
    if 'v4_subplots' not in _future_flags:
        raise ValueError("""
    plotly.subplots.get_subplots may only be used in the
    v4_subplots _plotly_future_ mode.  To try it out, run

    >>> from _plotly_future_ import v4_subplots

    before importing plotly.
    """)

    try:
        grid_ref = fig._grid_ref
    except AttributeError:
        raise Exception("In order to reference traces by row and column, "
                        "you must first use "
                        "plotly.tools.make_subplots "
                        "to create the figure with a subplot grid.")

    rows = len(grid_ref)
    cols = len(grid_ref[0])

    # Validate row
    if not isinstance(row, int) or row < 1 or rows < row:
        raise ValueError("""
The row argument to get_subplot must be an integer where 1 <= row <= {rows}
    Received value of type {typ}: {val}""".format(
            rows=rows,
            typ=type(row),
            val=repr(row)
        ))

    if not isinstance(col, int) or col < 1 or cols < col:
        raise ValueError("""
The col argument to get_subplot must be an integer where 1 <= row <= {cols}
    Received value of type {typ}: {val}""".format(
            cols=cols,
            typ=type(col),
            val=repr(col)
        ))

    ref = fig._grid_ref[row - 1][col - 1]
    if ref is None:
        return None

    layout_keys = ref['layout_keys']
    if len(layout_keys) == 0:
        return SubplotDomain(**ref['trace_kwargs']['domain'])
    elif len(layout_keys) == 1:
        return fig.layout[layout_keys[0]]
    elif len(layout_keys) == 2:
        return SubplotXY(
            xaxis=fig.layout[layout_keys[0]],
            yaxis=fig.layout[layout_keys[1]])
    else:
        raise ValueError("""
Unexpected subplot type with layout_keys of {}""".format(layout_keys))
