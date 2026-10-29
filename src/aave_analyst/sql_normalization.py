"""Narrow, audited translation of quoted ISO date operands for DuckDB."""
from datetime import datetime
import re
from sqlglot import exp
from .database import validate_sql


def normalize_datetime_quotes(sql):
    if not isinstance(sql, str):
        return sql, []
    try:
        tree = validate_sql(sql)
    except Exception:
        # Keep the original for the ordinary SQL guard/error path.
        return sql, []
    # CTE column lists and date-shaped aliases can define real identifiers.
    # Do not reinterpret those ambiguous queries as literal-date comparisons.
    if tree.find(exp.CTE) or any(re.match(r'^\d{4}-\d{2}-\d{2}', alias.alias)
                               for alias in tree.find_all(exp.Alias)):
        return sql, []
    changes = []
    assets={'dai':'DAI','usdc':'USDC','usdt':'USDT','usde':'USDe','weth':'WETH'}
    # Only equality against the actual asset column; never rename columns globally.
    for comparison in list(tree.find_all(exp.EQ)):
        for column,value in ((comparison.this,comparison.expression),(comparison.expression,comparison.this)):
            if not isinstance(column,exp.Column) or column.name.lower()!='asset':continue
            quoted_identifier=isinstance(value,exp.Column) and not value.table and value.this.args.get('quoted')
            string_literal=isinstance(value,exp.Literal) and value.is_string
            if not (quoted_identifier or string_literal):continue
            raw=value.name if quoted_identifier else value.this
            canonical=assets.get(raw.casefold())
            if canonical and (quoted_identifier or raw!=canonical):
                value.replace(exp.Literal.string(canonical))
                changes.append({'kind':'asset_operand_to_canonical_literal','original':raw,'value':canonical})

    def time_column(node):
        return isinstance(node, exp.Column) and node.name.lower() in {'time', 'hour', 'source_timestamp'}

    def convert(node):
        if not isinstance(node, exp.Column) or node.table or not node.this.args.get('quoted'):
            return
        value = node.name
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:[T ][0-9:.+\-]+Z?)?', value):
            return
        try:
            datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            return
        node.replace(exp.Literal.string(value))
        changes.append({'kind': 'iso_datetime_identifier_to_literal', 'value': value})

    for comparison in list(tree.find_all(exp.EQ, exp.NEQ, exp.GT, exp.GTE, exp.LT, exp.LTE)):
        if time_column(comparison.this):
            convert(comparison.expression)
        elif time_column(comparison.expression):
            convert(comparison.this)
    for between in tree.find_all(exp.Between):
        if time_column(between.this):
            convert(between.args.get('low'))
            convert(between.args.get('high'))
    if not changes:
        return sql, []
    normalized = tree.sql(dialect='duckdb')
    validate_sql(normalized)
    return normalized, changes
