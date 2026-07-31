# APPA Architecture

## Current Structure

streamlit_app.py

* UI
* Agent Runtime
* Tool Definitions
* Tool Implementations
* Google Authentication
* Gmail
* Calendar
* Google Drive
* Memory
* Session State

Problems

* One file contains too many responsibilities.
* Circular import risk.
* Difficult to test.
* Difficult to extend.


---

## Target Architecture

streamlit_app.py
│
├── UI
│
└── Agent
│
├── Tool Registry
├── Memory
├── LLM
└── Tools
├── Core Tools
├── Web Tools
├── Gmail Tools
├── Calendar Tools
└── Drive Tools