"""
All APPA tool implementations.
"""

import ast
import datetime
import json
import operator

import streamlit as st
from zoneinfo import ZoneInfo

from services.gmail_service import GmailService
from services.drive_service import DriveService
from services.calendar_service import CalendarService


TOOL_ERROR = "TOOL_ERROR:"


_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](
            _eval_node(node.left),
            _eval_node(node.right),
        )

    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](
            _eval_node(node.operand)
        )

    raise ValueError(
        "Only numbers and + - * / // % ** are supported."
    )
