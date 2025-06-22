# Regular Expression to DFA Converter 🚀

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![Graphviz](https://img.shields.io/badge/Graphviz-visualize-F7931E?style=for-the-badge&logo=graphviz)](https://graphviz.org/)

A Python-based tool that implements classic compiler design algorithms to convert any given Regular Expression (RE) into an equivalent Deterministic Finite Automaton (DFA). The process involves two major stages: converting the RE to a Non-deterministic Finite Automaton with epsilon transitions (ε-NFA) using Thompson's Construction, and then converting the ε-NFA to a DFA using the Subset Construction algorithm.

The tool provides detailed console output and automatically generates visual graphs for both the intermediate NFA and the final DFA.

---

## ✨ Key Features

-   **RE to ε-NFA Conversion:** Implements **Thompson's Construction** algorithm to reliably convert a regular expression into an equivalent NFA.
-   **Infix to Postfix Notation:** Automatically converts the input infix regular expression into postfix notation using the Shunting-yard algorithm to prepare it for the construction process.
-   **ε-NFA to DFA Conversion:** Uses the **Subset Construction** (powerset construction) algorithm, including the calculation of `ε-closures`, to convert the NFA into a minimal DFA.
-   **Automatic Graph Visualization:** Leverages the **Graphviz** library to generate clear, easy-to-read diagrams of the resulting state machines.
-   **Detailed Console Output:** Prints the full transition table and transition functions of the final DFA for detailed analysis.
-   **JSON Intermediate Representation:** The generated NFA is saved as an `output.json` file, allowing the two stages of the process to be run independently.

---

## 🤖 How It Works: The Theory

This project is a practical implementation of two fundamental algorithms in automata theory:

1.  **Part 1: Regular Expression to ε-NFA (Thompson's Construction)**
    -   The input regular expression (e.g., `(a+b)*`) is first augmented with explicit concatenation operators (e.g., `(a+b)*.c`).
    -   This infix expression is converted to postfix (Reverse Polish Notation) using the Shunting-yard algorithm to make it easy to evaluate.
    -   The postfix expression is then parsed. Each operator (`*`, `+`, `.`) corresponds to a specific rule in Thompson's Construction for combining smaller NFAs into a larger one, resulting in the final ε-NFA.

2.  **Part 2: ε-NFA to DFA (Subset Construction)**
    -   The algorithm starts with the `ε-closure` (all states reachable from the NFA's start state using only epsilon transitions) as the initial state of the DFA.
    -   For each new DFA state, it computes the set of states reachable for every symbol in the alphabet.
    -   The `ε-closure` of this new set of states forms another DFA state.
    -   This process is repeated until no new DFA states are discovered. Any DFA state containing one of the original NFA's final states becomes a final state in the DFA.

---

## 🛠️ Technology Stack

-   **Language:** Python 3
-   **Visualization:** `graphviz` (Python library and system package)
-   **Data Interchange:** `json`

---

## 🚀 How to Run Locally

### Prerequisites

1.  **Python 3.x**
2.  **Graphviz System Package:** You must install the Graphviz command-line tools on your system. This is a separate step from installing the Python library.
    -   **On macOS (using Homebrew):**
        ```sh
        brew install graphviz
        ```
    -   **On Ubuntu/Debian:**
        ```sh
        sudo apt-get update
        sudo apt-get install graphviz
        ```
    -   **On Windows:** Download from the [official Graphviz website](https://graphviz.org/download/) and add it to your system's PATH.

### Installation & Execution

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/YOUR_USERNAME/RE-NFA-DFA.git
    cd RE-NFA-DFA
    ```

2.  **Install Python dependencies:**
    *(It's recommended to do this in a virtual environment)*
    ```sh
    pip install -r requirements.txt
    ```

3.  **Run the Two-Step Process:**
    The conversion is a two-part process. You must run the scripts in this order.

    -   **Step 1: Convert RE to NFA**
        Run the first script. It will prompt you to enter a regular expression.
        ```sh
        python Re_to_NFA_main.py
        ```
        This will create `output.json` and `nfa_graph.png`.

    -   **Step 2: Convert NFA to DFA**
        Run the second script. It will automatically read `output.json`.
        ```sh
        python NFA_to_DFA_main.py
        ```
        This will generate the final `dfa.pdf`, display the DFA transition table in the console, and open the generated PDF.
