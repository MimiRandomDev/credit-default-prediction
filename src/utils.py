# utils.py
import re
from collections.abc import Iterable as ABCIterable
from html import escape
from pathlib import Path
from typing import Any, Iterable, Literal

import numpy as np
import pandas as pd
from IPython.display import display, HTML, Markdown

_NUMPY_SCALAR_REPR_RE = re.compile(r"np\.\w+\(([^)]+)\)")

_SUMMARY_PLACEHOLDER_RE = re.compile(r"^\[(?:ndarray|Series|Index) with \d+ elements?\]$")


def format_list_to_string(data: Any, max_items: int = 20) -> str:
    """
    Formats a list, tuple, set, NumPy array, or pandas Series/Index into a clean,
    human-readable comma-separated string, converting NumPy scalar types
    (e.g., np.int64, np.float64) into native Python values and truncating
    the output when it exceeds a configurable item limit.

    Parameters
    ----------
    data : Any
        The collection to format (list, tuple, set, np.ndarray, pd.Series, pd.Index).
        Non-iterable scalars are wrapped into a single-element list.
    max_items : int, optional
        Maximum number of elements to display before truncating. Defaults to 20.

    Returns
    -------
    str
        A comma-separated string of elements (e.g. "1, 2, 3"), or, if the
        collection exceeds `max_items`, a truncated string with a suffix
        indicating how many elements were omitted
        (e.g. "1, 2, 3 ... (+36 elements)"). Returns an empty string for
        `None` or empty collections.

    Examples
    --------
    >>> format_list_to_string(np.array([1, 2, 3]))
    '1, 2, 3'
    >>> format_list_to_string(pd.Series([1, 2, 3, 4, 5, 6]), max_items=3)
    '1, 2, 3 ... (+3 elements)'
    """
    if data is None:
        return ""

    if isinstance(data, (pd.Series, pd.Index, np.ndarray)):
        items_list = data.tolist()
    elif isinstance(data, (list, tuple, set)):
        items_list = list(data)
    elif isinstance(data, ABCIterable) and not isinstance(data, str):
        items_list = list(data)
    else:
        items_list = [data]

    # Unwrap NumPy scalar types (np.int64, np.float64, etc.) into native Python values
    cleaned_items = [
        str(item.item()) if hasattr(item, "item") and callable(getattr(item, "item")) else str(item)
        for item in items_list
    ]

    total_elements = len(cleaned_items)
    if total_elements == 0:
        return ""

    if total_elements <= max_items:
        return ", ".join(cleaned_items)

    visible_items = ", ".join(cleaned_items[:max_items])
    remaining_count = total_elements - max_items
    return f"{visible_items} ... (+{remaining_count} elements)"


def format_section(
        title: str,
        subtitle: str | None = None,
        style: Literal["html", "markdown"] = "html",
        render: bool = True
) -> str | None:
    """
    Formats a professionally styled section header banner for notebook use, in either
    HTML or Markdown.

    Designed for seamless integration in PyCharm and Jupyter Notebook environments,
    maintaining high visual contrast across both light and dark themes when using
    the HTML style.

    Parameters
    ----------
    title : str
        The main header title to be displayed in the section banner.
    subtitle : str, optional
        Optional description or contextual details rendered beneath the title. Defaults to None.
    style : {"html", "markdown"}, optional
        Output format — "html" for a styled banner card, "markdown" for a plain
        Markdown heading with an italic subtitle. Defaults to "html".
    render : bool, optional
        If True, displays the result via IPython (Markdown or HTML) and returns None.
        If False, returns the formatted string instead of rendering it. Defaults to True.

    Returns
    -------
    str | None
        None if `render` is True, otherwise the formatted string (Markdown or HTML).

    Examples
    --------
    >>> format_section("1. Exploratory Data Analysis", "Initial dataset inspection")
    """
    if style == "markdown":
        output = f"## ▸ {title}"
        if subtitle:
            output += f"\n\n*{subtitle}*"

        if render:
            display(Markdown(output))
            return None
        return output

    # style == "html"
    subtitle_block = (
        f'''<p style="
            margin: 6px 0 0 0;
            color: #94a3b8;
            font-size: 13px;
            font-weight: 400;
            line-height: 1.4;
            letter-spacing: 0.1px;
        ">{subtitle}</p>'''
        if subtitle else ""
    )

    output = f"""
    <div style="
        position: relative;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 5px solid #3b82f6;
        padding: 16px 20px 16px 22px;
        border-radius: 8px;
        margin: 22px 0 14px 0;
        box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(148, 163, 184, 0.08);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: 0; right: 0;
            width: 120px; height: 100%;
            background: radial-gradient(circle at top right, rgba(59, 130, 246, 0.12), transparent 70%);
            pointer-events: none;
        "></div>

        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 22px; height: 22px;
                border-radius: 6px;
                background: rgba(59, 130, 246, 0.15);
                color: #60a5fa;
                font-size: 13px;
                font-weight: 700;
                flex-shrink: 0;
            ">▸</span>
            <h3 style="
                margin: 0;
                color: #f8fafc;
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 0.4px;
                line-height: 1.2;
            ">
                {title}
            </h3>
        </div>
        {subtitle_block}
    </div>
    """

    if render:
        display(HTML(output))
        return None
    return output


def format_code_block(
        block: Iterable[Any],
        language: str = "",
        title: str | None = None,
        style: Literal["html", "markdown"] = "html",
        render: bool = False
) -> str | None:
    """
    Formats a single iterable of lines as a styled HTML code card or a Markdown code fence.

    Parameters
    ----------
    block : Iterable[Any]
        An iterable of lines (or values convertible to str) that make up the code block.
    language : str, optional
        The syntax highlighting identifier (e.g., 'python', 'sql'). Defaults to "".
    title : str, optional
        Optional label shown in the block header (e.g., a table or file name).
        Ignored in Markdown style. Defaults to None.
    style : {"html", "markdown"}, optional
        Output format — "html" for a styled card, "markdown" for a plain code fence.
        Defaults to "html".
    render : bool, optional
        If True, displays the result via IPython (Markdown or HTML) and returns None.
        If False, returns the formatted string instead of rendering it. Defaults to False.

    Returns
    -------
    str | None
        None if `render` is True, otherwise the formatted string (Markdown or HTML).

    Examples
    --------
    >>> format_code_block(["SELECT * FROM clientes;"], language="sql", title="clientes", render=True)
    """
    block_content = "\n".join(str(item) for item in block)

    if style == "markdown":
        output = f"```{language}\n{block_content}\n```"

        if render:
            display(Markdown(output))
            return None
        return output

    # style == "html"
    title_html = ""
    if title:
        title_html = f'''
        <div style="
            display: flex; align-items: center; justify-content: space-between;
            padding: 6px 14px;
            background: rgba(59, 130, 246, 0.1);
            border-bottom: 1px solid rgba(148, 163, 184, 0.15);
            font-size: 12px; font-weight: 600; letter-spacing: 0.3px;
            color: #93c5fd; font-family: -apple-system, sans-serif;
        ">
            <span>{title}</span>
            <span style="
                text-transform: uppercase; font-size: 10px;
                color: #64748b; letter-spacing: 0.5px;
            ">{language}</span>
        </div>'''

    output = f'''
    <div style="
        background: #0f172a;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 8px;
        margin: 14px 0;
        overflow: hidden;
        box-shadow: 0 2px 8px -2px rgba(0,0,0,0.3);
    ">
        {title_html}
        <pre style="
            margin: 0;
            padding: 14px 18px;
            overflow-x: auto;
            font-family: 'Fira Code', 'JetBrains Mono', Consolas, monospace;
            font-size: 13px;
            line-height: 1.5;
            color: #e2e8f0;
        "><code>{escape(block_content)}</code></pre>
    </div>'''

    if render:
        display(HTML(output))
        return None
    return output


def format_code_blocks(
        blocks: Iterable[Iterable[Any]],
        language: str = "",
        titles: Iterable[str] | None = None,
        style: Literal["html", "markdown"] = "html",
        render: bool = False
) -> str | None:
    """
    Formats multiple iterable blocks by delegating each one to `format_code_block`,
    then joins the results into a single output.

    Parameters
    ----------
    blocks : Iterable[Iterable[Any]]
        An iterable containing sub-iterables of lines, one per code block.
    language : str, optional
        The syntax highlighting identifier applied to all blocks. Defaults to "".
    titles : Iterable[str], optional
        Optional labels, one per block, matched by position. Ignored in Markdown style.
    style : {"html", "markdown"}, optional
        Output format. Defaults to "html".
    render : bool, optional
        If True, displays the joined result via IPython and returns None.
        If False, returns the formatted string instead of rendering it. Defaults to False.

    Returns
    -------
    str | None
        None if `render` is True, otherwise the formatted string (Markdown or HTML).

    Examples
    --------
    >>> format_code_blocks([["SELECT 1;"], ["SELECT 2;"]], language="sql", titles=["a", "b"], render=True)
    """
    titles = list(titles) if titles else []
    separator = "\n\n" if style == "markdown" else ""

    formatted = [
        format_code_block(
            block,
            language=language,
            title=titles[i] if i < len(titles) else None,
            style=style,
            render=False,
        )
        for i, block in enumerate(blocks)
    ]

    output = separator.join(formatted)

    if render:
        if style == "markdown":
            display(Markdown(output))
        else:
            display(HTML(output))
        return None
    return output


def format_table(
        headers: list[str],
        data: Iterable[Iterable[Any]],
        title: str | None = None,
        style: Literal["html", "markdown"] = "html",
        render: bool = False
) -> str | None:
    """
    Formats column headers and row data as a styled HTML table or an aligned Markdown table.

    In Markdown style, calculates maximum column widths to ensure perfect alignment
    in both raw text and rendered Markdown view. In HTML style, renders a card
    consistent with the visual language of format_section and format_code_block,
    sizing the card to the table's natural content width (not the full notebook
    width) and scrolling horizontally only when the table itself is wider than
    the available space.

    Parameters
    ----------
    headers : list[str]
        A list of column titles.
    data : Iterable[Iterable[Any]]
        A two-dimensional iterable representing the dataset rows.
    title : str, optional
        Optional label shown above the table (HTML style only). Defaults to None.
    style : {"html", "markdown"}, optional
        Output format — "html" for a styled table card, "markdown" for an aligned
        Markdown table. Defaults to "html".
    render : bool, optional
        If True, displays the result via IPython (Markdown or HTML) and returns None.
        If False, returns the formatted string instead of rendering it. Defaults to False.

    Returns
    -------
    str | None
        None if `render` is True, otherwise the formatted string (Markdown or HTML).

    Examples
    --------
    >>> headers = ["cliente_id", "edad", "limite_credito"]
    >>> data = [[1, 24, 20000.0], [2, 26, 120000.0]]
    >>> format_table(headers, data, render=True)
    """
    header_strs = [str(h) for h in headers]
    data_rows = [[str(item) for item in row] for row in data]

    if style == "markdown":
        all_rows = [header_strs] + data_rows
        col_widths = [max(len(row[i]) for row in all_rows) for i in range(len(headers))]

        header_line = "| " + " | ".join(val.ljust(col_widths[i]) for i, val in enumerate(header_strs)) + " |"
        separator_line = "| " + " | ".join("-" * col_widths[i] for i in range(len(headers))) + " |"
        body_lines = [
            "| " + " | ".join(val.ljust(col_widths[i]) for i, val in enumerate(row)) + " |"
            for row in data_rows
        ]

        output = "\n".join([header_line, separator_line] + body_lines)

        if render:
            display(Markdown(output))
            return None
        return output

    # style == "html"
    title_html = ""
    if title:
        title_html = f'''
        <div style="
            padding: 6px 14px;
            background: rgba(59, 130, 246, 0.1);
            border-bottom: 1px solid rgba(148, 163, 184, 0.15);
            font-size: 12px; font-weight: 600; letter-spacing: 0.3px;
            color: #93c5fd; font-family: -apple-system, sans-serif;
        ">{title}</div>'''

    thead_cells = "".join(
        f'''<th style="
            text-align: left; padding: 8px 16px;
            font-size: 12px; font-weight: 600; letter-spacing: 0.3px;
            color: #93c5fd; border-bottom: 1px solid rgba(148, 163, 184, 0.2);
            white-space: nowrap;
        ">{escape(h)}</th>'''
        for h in header_strs
    )

    body_rows_html = "".join(
        "<tr>" + "".join(
            f'''<td style="
                padding: 7px 16px;
                font-family: 'Fira Code', 'JetBrains Mono', Consolas, monospace;
                font-size: 13px; color: #e2e8f0;
                border-bottom: 1px solid rgba(148, 163, 184, 0.08);
                white-space: nowrap;
            ">{escape(val)}</td>'''
            for val in row
        ) + "</tr>"
        for row in data_rows
    )

    output = f'''
    <div style="
        display: inline-block;
        width: fit-content;
        max-width: 100%;
        background: #0f172a;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 8px;
        margin: 14px 0;
        overflow: hidden;
        box-shadow: 0 2px 8px -2px rgba(0,0,0,0.3);
    ">
        {title_html}
        <div style="overflow-x: auto; max-width: 100%;">
            <table style="border-collapse: collapse; table-layout: auto;">
                <thead><tr>{thead_cells}</tr></thead>
                <tbody>{body_rows_html}</tbody>
            </table>
        </div>
    </div>'''

    if render:
        display(HTML(output))
        return None
    return output


def format_tables(
        tables: Iterable[tuple[list[str], Iterable[Iterable[Any]]]],
        titles: Iterable[str] | None = None,
        style: Literal["html", "markdown"] = "html",
        render: bool = False
) -> str | None:
    """
    Formats multiple (headers, data) table pairs by delegating each one to
    format_table, then joins the results into a single output.

    Parameters
    ----------
    tables : Iterable[tuple[list[str], Iterable[Iterable[Any]]]]
        An iterable of (headers, data) pairs, one per table.
    titles : Iterable[str], optional
        Optional labels, one per table, matched by position. Defaults to None.
    style : {"html", "markdown"}, optional
        Output format applied to all tables. Defaults to "html".
    render : bool, optional
        If True, displays the joined result via IPython and returns None.
        If False, returns the formatted string instead of rendering it. Defaults to False.

    Returns
    -------
    str | None
        None if `render` is True, otherwise the formatted string (Markdown or HTML).
    """
    titles = list(titles) if titles else []
    separator = "\n\n" if style == "markdown" else ""

    formatted = [
        format_table(
            headers,
            data,
            title=titles[i] if i < len(titles) else None,
            style=style,
            render=False,
        )
        for i, (headers, data) in enumerate(tables)
    ]

    output = separator.join(formatted)

    if render:
        if style == "markdown":
            display(Markdown(output))
        else:
            display(HTML(output))
        return None
    return output


def format_dict(
        data_map: dict[str, Any],
        headers: tuple[str, str] = ("Metric", "Value"),
        title: str | None = None,
        style: Literal["html", "markdown"] = "html",
        render: bool = False
) -> str | None:
    """
    Formats a generic dictionary as a two-column table (HTML or Markdown) by
    delegating the actual table rendering to format_table.

    Automatically handles complex data types (e.g., pandas Series/Index, NumPy
    arrays, lists, tuples, sets, or NumPy scalar types) by formatting them into
    a clean, comma-separated, human-readable string via `format_list_to_string`
    instead of collapsing them into a generic placeholder like
    "[ndarray with N elements]". Long collections are truncated (default 20
    items) rather than fully hidden, so the table stays readable without
    losing the underlying data structure.

    Parameters
    ----------
    data_map : dict[str, Any]
        The input dictionary containing key-value pairs to display.
    headers : tuple[str, str], optional
        Column names for keys and values. Defaults to ("Metric", "Value").
    title : str, optional
        Optional label shown above the table (HTML style only). Defaults to None.
    style : {"html", "markdown"}, optional
        Output format. Defaults to "html".
    render : bool, optional
        If True, displays the result via IPython and returns None.
        If False, returns the formatted string instead of rendering it. Defaults to False.

    Returns
    -------
    str | None
        None if `render` is True, otherwise the formatted string (Markdown or HTML).

    Examples
    --------
    >>> metrics = {"column_name": "edad", "mean": 35.48, "unique_values": np.array([1, 2, 3])}
    >>> format_dict(metrics, headers=("Property", "Value"), render=True)
    """
    rows = []

    for key, val in data_map.items():
        # Unwrap NumPy scalar types (np.int64, np.float64, etc.) before type checks
        if isinstance(val, np.generic):
            val = val.item()

        # Handle complex iterable structures with a readable, truncated format
        if isinstance(val, (pd.Series, pd.Index, np.ndarray, list, tuple, set)):
            val_str = format_list_to_string(val, max_items=20)
        elif isinstance(val, (float, np.floating)):
            val_str = f"{val:,.4f}".rstrip("0").rstrip(".") if not pd.isna(val) else "NaN"
        else:
            val_str = str(val) if val is not None else "N/A"

        clean_key = str(key).replace("\n", " ")
        clean_val = val_str.replace("\n", " ")

        # Markdown table syntax breaks on unescaped pipes; irrelevant for HTML
        if style == "markdown":
            clean_key = clean_key.replace("|", "\\|")
            clean_val = clean_val.replace("|", "\\|")

        rows.append([clean_key, clean_val])

    return format_table(list(headers), rows, title=title, style=style, render=render)


def format_dataframe(
        df: pd.DataFrame,
        include_index: bool = True,
        title: str | None = None,
        style: Literal["html", "markdown"] = "html",
        render: bool = False
) -> str | None:
    """
    Formats a pandas DataFrame as a styled table by delegating to format_table.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to format.
    include_index : bool, optional
        If True, prepends the DataFrame's index as the first column. Defaults to True.
    title : str, optional
        Optional label shown above the table (HTML style only). Defaults to None.
    style : {"html", "markdown"}, optional
        Output format. Defaults to "html".
    render : bool, optional
        If True, displays the result and returns None.
        If False, returns the formatted string instead of rendering it. Defaults to False.

    Returns
    -------
    str | None
        None if `render` is True, otherwise the formatted string (Markdown or HTML).

    Examples
    --------
    >>> format_dataframe(df.head(), title="Muestra Inicial del Dataset", render=True)
    """
    headers = [str(c) for c in df.columns.tolist()]
    rows = df.values.tolist()

    if include_index:
        index_name = str(df.index.name) if df.index.name else ""
        headers = [index_name] + headers
        rows = [[idx] + row for idx, row in zip(df.index.tolist(), rows)]

    return format_table(headers, rows, title=title, style=style, render=render)


def read_file_content(file_path: str | Path, encoding: str = "utf-8") -> str:
    """
    Reads and returns the complete text content of a file from a given path.

    Handles cross-platform paths seamlessly and supports standard text file formats
    such as .sql, .txt, .md, .py, or .json.

    Parameters
    ----------
    file_path : str | Path
        The relative or absolute file path to read.
    encoding : str, optional
        The character encoding to open the file with. Defaults to 'utf-8'.

    Returns
    -------
    str
        The file contents as a UTF-8 decoded string.

    Raises
    ------
    FileNotFoundError
        If the specified file path does not exist.
    IsADirectoryError
        If the specified path points to a directory instead of a file.

    Examples
    --------
    >>> query_str = read_file_content("queries/extract_clients.sql")
    >>> print(query_str)
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"No file found at specified path: '{path.resolve()}'")

    if not path.is_file():
        raise IsADirectoryError(f"Target path is a directory, not a file: '{path.resolve()}'")

    return path.read_text(encoding=encoding)


if __name__ == "__main__":
    pass
