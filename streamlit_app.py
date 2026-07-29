"""
A minimal AI agent: LLM + tools + a loop + a chat UI.

Runs on Streamlit Community Cloud (free) using a free LLM API.
Set GEMINI_API_KEY in the app's Secrets before running.
"""

import ast
import datetime
import json
import operator
import os
from zoneinfo import ZoneInfo

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="My First Agent", page_icon="🤖")

# ---------------------------------------------------------------------------
# 1. LLM client
#
# We talk to Gemini through its OpenAI-compatible endpoint, so the request
# format is the widely-documented OpenAI one.
#
# PROVIDER SWAP — if Gemini keeps failing, change these three constants and
# the SECRET_NAME below, then add the new key in Streamlit's Secrets box:
#
#   Groq (free, no thought-signature weirdness):
#       MODEL       = "llama-3.3-70b-versatile"   # check console.groq.com/docs/models
#       BASE_URL    = "https://api.groq.com/openai/v1"
#       SECRET_NAME = "GROQ_API_KEY"
# ---------------------------------------------------------------------------

MODEL = "gemini-3-flash-preview"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
SECRET_NAME = "GEMINI_API_KEY"

MAX_STEPS = 6  # hard stop so a confused agent can't loop forever

SYSTEM_PROMPT = (
    "You are a helpful assistant with access to tools. "
    "Use a tool when it gives you a more accurate answer than guessing — "
    "especially for arithmetic and for the current date or time. "
    "Never invent a tool result. If a tool returns an error, say so plainly."
)


def get_api_key():
    """Read the key from Streamlit secrets, falling back to an env var locally."""
    try:
        return st.secrets[SECRET_NAME]
    except Exception:
        return os.environ.get(SECRET_NAME)


@st.cache_resource
def get_client(api_key: str, base_url: str) -> OpenAI:
    # Cached so we don't rebuild the client on every Streamlit rerun.
    return OpenAI(api_key=api_key, base_url=base_url)


API_KEY = get_api_key()
if not API_KEY:
    st.error(
        f"No API key found. Add a secret named {SECRET_NAME} in "
        "Manage app → Settings → Secrets, then reboot the app."
    )
    st.stop()

client = get_client(API_KEY, BASE_URL)

# ---------------------------------------------------------------------------
# 2. Tools
#
# A tool is just a Python function plus a JSON description the model can read.
# Keep them small, and return a string that reads well to the model.
# ---------------------------------------------------------------------------

# Only these operators are allowed. We walk the parsed syntax tree instead of
# calling eval(), because this app is reachable by anyone with the URL and
# eval() on user input is remote code execution.
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
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("Only numbers and + - * / // % ** are supported.")


def calculate(expression: str) -> str:
    try:
        return str(_eval_node(ast.parse(expression, mode="eval").body))
    except Exception as exc:
        return f"Calculation failed: {exc}"


def get_current_time(timezone: str = "UTC") -> str:
    try:
        now = datetime.datetime.now(ZoneInfo(timezone))
        # Include the offset: %Z alone gives "PST" for Asia/Manila (Philippine
        # Standard Time), which reads like US Pacific and misleads the model.
        return now.strftime("%Y-%m-%d %H:%M:%S %Z (UTC%z)")
    except Exception as exc:
        return f"Could not read the time for {timezone!r}: {exc}"


# The schema is what the model actually sees. Vague descriptions here are the
# most common reason an agent picks the wrong tool or fills in bad arguments.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a numeric arithmetic expression exactly.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "An arithmetic expression, e.g. '1450 * 0.12'.",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time in a given timezone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "IANA timezone name, e.g. 'Asia/Manila'. Defaults to UTC.",
                    }
                },
                "required": [],
            },
        },
    },
]

TOOL_IMPLS = {
    "calculate": calculate,
    "get_current_time": get_current_time,
}


# ---------------------------------------------------------------------------
# 3. The agent loop
# ---------------------------------------------------------------------------


def _tool_call_payload(tool_call) -> dict:
    """Rebuild a tool call for the next request, keeping vendor extras.

    Gemini 3 "thinks" before calling a tool, signs that reasoning, and hangs
    the signature off a non-standard field (extra_content.google.
    thought_signature). It must be echoed back verbatim or the next request is
    rejected with a 400. A stock OpenAI client silently drops the field —
    since we build this dict ourselves, we can keep it.
    """
    payload = {
        "id": tool_call.id,
        "type": "function",
        "function": {
            "name": tool_call.function.name,
            "arguments": tool_call.function.arguments,
        },
    }

    extra = getattr(tool_call, "extra_content", None)
    if extra is None:
        model_extra = getattr(tool_call, "model_extra", None) or {}
        extra = model_extra.get("extra_content")

    if extra is not None:
        # Pydantic objects need flattening before they can be re-serialised.
        if hasattr(extra, "model_dump"):
            extra = extra.model_dump(exclude_none=True)
        payload["extra_content"] = extra

    return payload


def run_agent(user_message: str, history: list) -> tuple[str, list]:
    """Call the model; run any tool it asks for; feed the result back. Repeat.

    Returns (answer, trace) so the UI can show what the agent actually did.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    trace = []

    for _ in range(MAX_STEPS):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
            )
        except Exception as exc:
            return f"The model call failed: {exc}", trace

        message = response.choices[0].message

        # No tool requested — this is the final answer.
        if not message.tool_calls:
            return (message.content or "(empty response)"), trace

        payloads = [_tool_call_payload(tc) for tc in message.tool_calls]

        # Visible in the UI so you can confirm the signature survived.
        signed = sum(1 for p in payloads if "extra_content" in p)
        trace.append(f"[debug] {len(payloads)} tool call(s), {signed} carrying extra_content")

        messages.append(
            {
                "role": "assistant",
                "content": message.content,
                "tool_calls": payloads,
            }
        )

        for tool_call in message.tool_calls:
            name = tool_call.function.name
            raw_args = tool_call.function.arguments or "{}"
            impl = TOOL_IMPLS.get(name)

            if impl is None:
                result = f"No tool named {name}."
            else:
                try:
                    result = impl(**json.loads(raw_args))
                except Exception as exc:
                    # Hand the error back to the model rather than crashing —
                    # it can usually fix its own arguments and retry.
                    result = f"Tool error: {exc}"

            trace.append(f"{name}({raw_args})\n  -> {result}")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

    return "I used too many steps without reaching an answer. Try a narrower question.", trace


# ---------------------------------------------------------------------------
# 4. UI
#
# Streamlit reruns this whole file on every interaction, so the conversation
# lives in session_state rather than in a local variable.
# ---------------------------------------------------------------------------

st.title("🤖 My First Agent")
st.caption(f"Two tools: exact arithmetic, and current time by timezone. Model: {MODEL}")

with st.sidebar:
    st.subheader("What this is")
    st.write(
        "An LLM that can call Python functions. Ask something that needs a "
        "tool, then open **Tools used** under the answer to see what it did."
    )
    if st.button("Clear conversation"):
        st.session_state.history = []
        st.rerun()

if "history" not in st.session_state:
    st.session_state.history = []

for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        st.markdown(turn["content"])

prompt = st.chat_input("Ask me something…")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    # Pass the history from before this message, so the model has context.
    prior = list(st.session_state.history)
    st.session_state.history.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            answer, trace = run_agent(prompt, prior)
        st.markdown(answer)
        if trace:
            with st.expander(f"Tools used ({len(trace)})"):
                for line in trace:
                    st.code(line, language="text")

    st.session_state.history.append({"role": "assistant", "content": answer})
