"""
APPA Core Tool Implementations
"""

import ast
import datetime
import operator
from zoneinfo import ZoneInfo

import streamlit as st

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


def calculate(expression: str) -> str:
    try:
        return str(
            _eval_node(
                ast.parse(
                    expression,
                    mode="eval",
                ).body
            )
        )
    except Exception as exc:
        return f"{TOOL_ERROR} calculation failed: {exc}"


def get_current_time(timezone: str = "UTC") -> str:
    try:
        now = datetime.datetime.now(
            ZoneInfo(timezone)
        )
        return now.strftime(
            "%Y-%m-%d %H:%M:%S %Z (UTC%z)"
        )
    except Exception as exc:
        return (
            f"{TOOL_ERROR} "
            f"could not read the time for "
            f"{timezone!r}: {exc}"
        )

from memory.memory_manager import MemoryManager


def remember_information(key: str, value: str) -> str:
    """
    Store user information in long-term memory.
    """

    try:
        MemoryManager.remember(key, value)
        return f"I'll remember that your '{key}' is '{value}'."

    except Exception as exc:
        return f"{TOOL_ERROR} {exc}"
