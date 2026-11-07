import copy
import io
from warnings import warn

# Reformat table_color as dict of tuples

dict_colors = {
    "yellow_light": ("#BF8F00", "2px solid #BF8F00", "#FFF2CC", "#FFFFFF"),
    "grey_light": ("#808080", "2px solid #808080", "#EDEDED", "#FFFFFF"),
    "blue_light": ("#305496", "2px solid #305496", "#D9E1F2", "#FFFFFF"),
    "orange_light": ("#C65911", "2px solid #C65911", "#FCE4D6", "#FFFFFF"),
    "green_light": ("#548235", "2px solid #548235", "#E2EFDA", "#FFFFFF"),
    "red_light": ("#823535", "2px solid #823535", "#efdada", "#FFFFFF"),
    "yellow_dark": ("#FFFFFF", "2px solid #BF8F00", "#FFF2CC", "#BF8F00"),
    "grey_dark": ("#FFFFFF", "2px solid #808080", "#EDEDED", "#808080"),
    "blue_dark": ("#FFFFFF", "2px solid #305496", "#D9E1F2", "#305496"),
    "orange_dark": ("#FFFFFF", "2px solid #C65911", "#FCE4D6", "#C65911"),
    "green_dark": ("#FFFFFF", "2px solid #548235", "#E2EFDA", "#548235"),
    "red_dark": ("#FFFFFF", "2px solid #823535", "#efdada", "#823535"),
}


def build_table(
    df,
    color: str = "blue_light",
    font_size: str = "medium",
    font_family: str = "Century Gothic, sans-serif",
    text_align: str = "left",
    width: str = "auto",
    index: bool = False,
    even_color: str = "black",
    even_bg_color: str = "white",
    odd_bg_color: str | None = None,
    border_bottom_color: str | None = None,
    escape: bool = True,
    width_dict: list | None = None,
    padding: str = "0px 20px 0px 0px",
    float_format: str | None = None,
    conditions: dict | None = None,
) -> str:
    """
    Build an HTML table from a pandas DataFrame with customizable styling options.

    Args:
        df (pd.DataFrame): The DataFrame to convert to an HTML table.
        color (str): The color scheme to use for the table. Must be one of the keys in dict_colors.
        font_size (str): The font size for the table text.
        font_family (str): The font family for the table text.
        text_align (str): The text alignment for the table cells.
        width (str): The width of the table. Can be a fixed value (e.g., "500px") or "auto".
        index (bool): Whether to include the DataFrame index in the table.
        even_color (str): The text color for even rows.
        even_bg_color (str): The background color for even rows.
        odd_bg_color (str): The background color for odd rows. If None, the default from dict_colors is used.
        border_bottom_color (str): The color of the bottom border of the table. If None, the default from dict_colors is used.
        escape (bool): Whether to escape HTML characters in the DataFrame values.
        width_dict (list): A list of widths for each column. If provided, must match the number of columns in the DataFrame.
        padding (str): The padding for the table cells.
        float_format (str): A format string for floating-point numbers (e.g., "%.2f").
        conditions (dict): A dictionary specifying conditional formatting rules for specific columns.
    Returns:
        str: An HTML string representing the styled table.
    """
    width_dict = list(width_dict) if width_dict is not None else []
    conditions = copy.deepcopy(conditions) if conditions is not None else {}
    if df.empty:
        return ""

    if color not in dict_colors:
        raise ValueError(
            f"Invalid color '{color}'. Supported colors are: {', '.join(sorted(dict_colors.keys()))}"
        )

    # Set color
    color, border_bottom, odd_background_color, header_background_color = dict_colors[
        color
    ]

    if odd_bg_color:
        odd_background_color = odd_bg_color

    if border_bottom_color:
        border_bottom = border_bottom_color

    body = ""
    a = 0
    while a != len(df):
        if a == 0:
            df_html_output = df.iloc[[a]].to_html(
                na_rep="",
                index=index,
                border=0,
                escape=escape,
                float_format=float_format,
            )
            # change format of header
            if index:
                df_html_output = df_html_output.replace(
                    "<th>",
                    '<th style = "background-color: '
                    + header_background_color
                    + ";font-family: "
                    + font_family
                    + ";font-size: "
                    + str(font_size)
                    + ";color: "
                    + color
                    + ";text-align: "
                    + text_align
                    + ";border-bottom: "
                    + border_bottom
                    + ";padding: "
                    + padding
                    + ";width: "
                    + str(width)
                    + '">',
                    len(df.columns) + 1,
                )

                df_html_output = df_html_output.replace(
                    "<th>",
                    '<th style = "background-color: '
                    + odd_background_color
                    + ";font-family: "
                    + font_family
                    + ";font-size: "
                    + str(font_size)
                    + ";text-align: "
                    + text_align
                    + ";padding: "
                    + padding
                    + ";width: "
                    + str(width)
                    + '">',
                )

            else:
                df_html_output = df_html_output.replace(
                    "<th>",
                    '<th style = "background-color: '
                    + header_background_color
                    + ";font-family: "
                    + font_family
                    + ";font-size: "
                    + str(font_size)
                    + ";color: "
                    + color
                    + ";text-align: "
                    + text_align
                    + ";border-bottom: "
                    + border_bottom
                    + ";padding: "
                    + padding
                    + ";width: "
                    + str(width)
                    + '">',
                )

            # change format of table
            df_html_output = df_html_output.replace(
                "<td>",
                '<td style = "background-color: '
                + odd_background_color
                + ";font-family: "
                + font_family
                + ";font-size: "
                + str(font_size)
                + ";text-align: "
                + text_align
                + ";padding: "
                + padding
                + ";width: "
                + str(width)
                + '">',
            )
            body = """<p>""" + format(df_html_output)

            a = 1

        elif a % 2 == 0:
            df_html_output = df.iloc[[a]].to_html(
                na_rep="", index=index, header=False, escape=escape
            )

            # change format of index
            df_html_output = df_html_output.replace(
                "<th>",
                '<th style = "background-color: '
                + odd_background_color
                + ";font-family: "
                + font_family
                + ";font-size: "
                + str(font_size)
                + ";text-align: "
                + text_align
                + ";padding: "
                + padding
                + ";width: "
                + str(width)
                + '">',
            )

            # change format of table
            df_html_output = df_html_output.replace(
                "<td>",
                '<td style = "background-color: '
                + odd_background_color
                + ";font-family: "
                + font_family
                + ";font-size: "
                + str(font_size)
                + ";text-align: "
                + text_align
                + ";padding: "
                + padding
                + ";width: "
                + str(width)
                + '">',
            )

            body = body + format(df_html_output)

            a += 1

        elif a % 2 != 0:
            df_html_output = df.iloc[[a]].to_html(
                na_rep="", index=index, header=False, escape=escape
            )

            # change format of index
            df_html_output = df_html_output.replace(
                "<th>",
                '<th style = "background-color: '
                + even_bg_color
                + "; color: "
                + even_color
                + ";font-family: "
                + font_family
                + ";font-size: "
                + str(font_size)
                + ";text-align: "
                + text_align
                + ";padding: "
                + padding
                + ";width: "
                + str(width)
                + '">',
            )

            # change format of table
            df_html_output = df_html_output.replace(
                "<td>",
                '<td style = "background-color: '
                + even_bg_color
                + "; color: "
                + even_color
                + ";font-family: "
                + font_family
                + ";font-size: "
                + str(font_size)
                + ";text-align: "
                + text_align
                + ";padding: "
                + padding
                + ";width: "
                + str(width)
                + '">',
            )
            body = body + format(df_html_output)

            a += 1

    body = body + """</p>"""

    body = body.replace(
        """</td>
    </tr>
  </tbody>
</table>
            <table border="1" class="dataframe">
  <tbody>
    <tr>""",
        """</td>
    </tr>
    <tr>""",
    ).replace(
        """</td>
    </tr>
  </tbody>
</table><table border="1" class="dataframe">
  <tbody>
    <tr>""",
        """</td>
    </tr>
    <tr>""",
    )

    if conditions:
        for k in conditions:
            if k not in df.columns:
                warn(
                    f"Column '{k}' specified in conditions does not exist in the DataFrame. Skipping this condition."
                )
                continue
            col_index = list(df.columns).index(k)
            cond = conditions[k]
            has_min = "min" in cond and "min_color" in cond
            has_max = "max" in cond and "max_color" in cond
            if not has_min and not has_max:
                continue

            width_body = ""
            w = 0
            for line in io.StringIO(body):
                updated_body = False
                if w == col_index:
                    try:
                        cell_text = repr(line).split(">")[1].split("<")[0]
                        cell_val = float(cell_text)
                        color_to_apply = None
                        if has_min and cell_val < cond["min"]:
                            color_to_apply = cond["min_color"]
                        elif has_max and cell_val > cond["max"]:
                            color_to_apply = cond["max_color"]

                        if color_to_apply:
                            if "color: black" in repr(line):
                                width_body = (
                                    width_body
                                    + repr(line).replace(
                                        "color: black",
                                        "color: " + color_to_apply,
                                    )[1:]
                                )
                            elif "color: white" in repr(line):
                                width_body = (
                                    width_body
                                    + repr(line).replace(
                                        "color: white",
                                        "color: " + color_to_apply,
                                    )[1:]
                                )
                            else:
                                width_body = (
                                    width_body
                                    + repr(line).replace(
                                        '">',
                                        "; color: " + color_to_apply + '">',
                                    )[1:]
                                )
                            updated_body = True
                    except (ValueError, IndexError):
                        pass
                if not updated_body:
                    width_body = width_body + repr(line)[1:]

                if (
                    str(repr(line))[:10] == "'      <td"
                    or str(repr(line))[:10] == "'      <th"
                ):
                    if w == len(df.columns) - 1:
                        w = 0
                    else:
                        w += 1
            body = width_body[: len(width_body) - 1]

    if len(width_dict) == len(df.columns):
        width_body = ""
        w = 0
        if conditions:
            for line in body.split(r"\n'"):
                width_body = (
                    width_body
                    + repr(line).replace("width: auto", "width: " + width_dict[w])[1:]
                )
                if (
                    str(repr(line))[:10] == "'      <td"
                    or str(repr(line))[:10] == "'      <th"
                ):
                    if w == len(df.columns) - 1:
                        w = 0
                    else:
                        w += 1
        else:
            for line in io.StringIO(body):
                line = line.replace("\n", "")
                width_body = (
                    width_body
                    + repr(line).replace("width: auto", "width: " + width_dict[w])[1:]
                )
                if (
                    str(repr(line))[:10] == "'      <td"
                    or str(repr(line))[:10] == "'      <th"
                ):
                    if w == len(df.columns) - 1:
                        w = 0
                    else:
                        w += 1
        return width_body[: len(width_body) - 1].replace("'", "")
    else:
        return body.replace(r"\n'", "")
