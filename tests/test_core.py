import pytest

pd = pytest.importorskip("pandas")

from tableloom import build_table
from tableloom.core import dict_colors


def test_build_table_default_color():
    df = pd.DataFrame({"A": [1, 2]})
    html = build_table(df)
    # Default color is blue_light, header color is #305496, alternating cell bg is #D9E1F2
    assert "color: #305496" in html
    assert "background-color: #D9E1F2" in html


def test_build_table_empty_returns_empty_string():
    df = pd.DataFrame()
    assert build_table(df, color="blue_light") == ""


def test_build_table_basic_html_contains_values_and_styles():
    df = pd.DataFrame({"A": [1, 2], "B": ["x", "y"]})
    html = build_table(
        df,
        color="yellow_light",
        index=False,
        width="auto",
        width_dict=["50px", "60px"],
    )
    assert "A" in html
    assert "B" in html
    # header background color for "yellow_light" is "#FFF2CC"
    assert "background-color: #FFF2CC" in html
    # width from width_dict should be applied to first column
    assert "width: 50px" in html


def test_build_table_single_row():
    df = pd.DataFrame({"Name": ["Alice"], "Age": [30]})
    html = build_table(df, color="blue_light", index=False)
    assert "<table" in html
    assert "Name" in html
    assert "Age" in html
    assert "Alice" in html
    assert "30" in html


def test_build_table_multiple_rows_alternating_colors():
    df = pd.DataFrame({"Val": [1, 2, 3]})
    html = build_table(
        df,
        color="green_light",
        even_bg_color="#EFEFEF",
        odd_bg_color="#FFFFFF",
        index=False,
    )
    assert "background-color: #EFEFEF" in html
    assert "background-color: #FFFFFF" in html


def test_build_table_index_flag():
    df = pd.DataFrame({"Col": ["x", "y"]})
    html_without_index = build_table(df, color="grey_light", index=False)
    html_with_index = build_table(df, color="grey_light", index=True)

    assert "<th>Col</th>" in html_without_index or ">Col<" in html_without_index
    assert ">0<" in html_with_index
    assert ">1<" in html_with_index


@pytest.mark.parametrize("color_name", list(dict_colors.keys()))
def test_build_table_all_supported_colors(color_name):
    df = pd.DataFrame({"A": [10, 20]})
    html = build_table(df, color=color_name)
    assert "<table" in html
    # Check that the header background color is present in the output
    _, _, _, header_bg = dict_colors[color_name]
    assert header_bg in html


def test_build_table_missing_values():
    df = pd.DataFrame({"A": [1.0, None], "B": ["valid", float("nan")]})
    html = build_table(df, color="blue_light")
    assert "<table" in html
    assert "valid" in html


def test_build_table_float_formatting():
    df = pd.DataFrame({"Price": [19.9876, 5.4321]})
    html = build_table(df, color="orange_light", float_format="%.2f")
    assert "19.99" in html
    assert "5.43" in html


def test_build_table_html_escaping():
    df = pd.DataFrame({"Script": ["<script>alert(1)</script>"]})
    html_escaped = build_table(df, color="blue_light", escape=True)
    html_unescaped = build_table(df, color="blue_light", escape=False)

    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html_escaped
    assert "<script>alert(1)</script>" in html_unescaped


def test_build_table_custom_styling():
    df = pd.DataFrame({"Item": ["Widget"]})
    html = build_table(
        df,
        color="red_light",
        font_size="16px",
        font_family="Helvetica, Arial, sans-serif",
        text_align="right",
        padding="8px 12px",
        even_color="#111111",
        even_bg_color="#EEEEEE",
        border_bottom_color="3px solid #000000",
    )
    assert "font-size: 16px" in html
    assert "font-family: Helvetica, Arial, sans-serif" in html
    assert "text-align: right" in html
    assert "padding: 8px 12px" in html
    assert "border-bottom: 3px solid #000000" in html


def test_build_table_width_and_width_dict():
    df = pd.DataFrame({"A": [1], "B": [2]})
    html_fixed_width = build_table(df, color="blue_light", width="300px")
    assert "width: 300px" in html_fixed_width

    html_dict_width = build_table(df, color="blue_light", width_dict=["120px", "180px"])
    assert "width: 120px" in html_dict_width
    assert "width: 180px" in html_dict_width


def test_build_table_conditions():
    df = pd.DataFrame({"Score": [10, 50, 95]})
    conditions = {
        "Score": {
            "min": 25,
            "max": 80,
            "min_color": "red",
            "max_color": "green",
        }
    }
    html = build_table(df, color="blue_light", conditions=conditions)
    # Verify conditional colors are applied to matching values
    assert "color: red" in html
    assert "color: green" in html


def test_build_table_conditions_missing_column():
    df = pd.DataFrame({"Existing": [1, 2, 3]})
    conditions = {
        "NonExistent": {
            "min": 0,
            "max": 10,
            "min_color": "red",
            "max_color": "green",
        }
    }
    # Should emit a warning when condition references a column not in df
    with pytest.warns(
        UserWarning,
        match="Column 'NonExistent' specified in conditions does not exist in the DataFrame. Skipping this condition.",
    ):
        html = build_table(df, color="blue_light", conditions=conditions)
    assert "<table" in html


def test_build_table_conditions_does_not_mutate_caller_dict():
    df = pd.DataFrame({"Score": [10, 50, 95]})
    conditions = {
        "Score": {
            "min": 25,
            "max": 80,
            "min_color": "red",
            "max_color": "green",
        }
    }
    keys_before = set(conditions["Score"].keys())
    build_table(df, color="blue_light", conditions=conditions)
    assert set(conditions["Score"].keys()) == keys_before


def test_build_table_invalid_color_raises_error():
    df = pd.DataFrame({"A": [1]})
    with pytest.raises((ValueError, KeyError)):
        build_table(df, color="non_existent_color")


def test_build_table_html_structure_validity():
    df = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})
    html = build_table(df, color="blue_light")

    assert html.startswith("<p><table")
    assert html.endswith(("</table></p>\n", "</table></p>"))
    assert html.count("<table") == html.count("</table>") == 1
    assert html.count("<thead>") == html.count("</thead>") == 1
    assert html.count("<tbody>") == html.count("</tbody>") == 1
    # 1 header row + 3 data rows = 4 rows
    assert html.count("<tr") == html.count("</tr>") == 4
    # 2 header cells (<th ...>)
    assert (html.count("<th ") + html.count("<th>")) == html.count("</th>") == 2
    # 3 rows * 2 columns = 6 data cells
    assert html.count("<td") == html.count("</td>") == 6


def test_build_table_width_dict_mismatched_length_ignored():
    df = pd.DataFrame({"A": [1], "B": [2]})
    html = build_table(df, color="blue_light", width="auto", width_dict=["120px"])
    assert "width: 120px" not in html


def test_build_table_conditions_non_numeric_cells_gracefully_skipped():
    df = pd.DataFrame({"Score": ["not-a-number", "pending"]})
    conditions = {
        "Score": {
            "min": 10,
            "max": 50,
            "min_color": "red",
            "max_color": "green",
        }
    }
    html = build_table(df, color="blue_light", conditions=conditions)
    assert "not-a-number" in html
    assert "pending" in html


def test_build_table_conditions_float_values():
    df = pd.DataFrame({"Score": [10.5, 55.2, 90.8]})
    conditions = {
        "Score": {
            "min": 20.0,
            "max": 80.0,
            "min_color": "red",
            "max_color": "green",
        }
    }
    html = build_table(df, color="blue_light", conditions=conditions)
    assert "color: red" in html
    assert "color: green" in html


def test_build_table_conditions_only_min_or_only_max():
    df = pd.DataFrame({"Score": [10, 90]})
    cond_min_only = {"Score": {"min": 50, "min_color": "red"}}
    html_min = build_table(df, color="blue_light", conditions=cond_min_only)
    assert "color: red" in html_min

    cond_max_only = {"Score": {"max": 50, "max_color": "green"}}
    html_max = build_table(df, color="blue_light", conditions=cond_max_only)
    assert "color: green" in html_max
