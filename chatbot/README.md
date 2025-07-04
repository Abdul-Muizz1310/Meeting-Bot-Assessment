# 🧠 Intent-Aware, Memory-Enhanced LLM Chatbot Engine

A modular chatbot system that can classify user intent, route requests dynamically, maintain session context, and trace all activity with observability tools.

---

## ⭐️ Features

This chatbot system offers:

- **Intent Classification**  
  - Dynamically identifies the user's underlying goal (e.g., summarization, question answering).
  - Uses an LLM prompt to enforce strict, predictable labels for routing.

- **Dynamic Routing**  
  - Routes user input to the appropriate LangChain pipeline based on the classified intent.
  - Supports easy addition of new intents and chains in a plug-and-play fashion.

- **Session-Level Memory**  
  - Stores complete conversation history per user/session.
  - Uses LangChain's `ConversationBufferMemory` to maintain context across multiple turns.

- **LLM-Powered Chains**  
  - Predefined LangChain chains for tasks like summarization and question answering.
  - Each chain can be swapped out or improved without changing the overall architecture.

- **Observability with Langfuse**  
  - Every invocation of the engine is traced and logged using Langfuse’s open-source tracing tools.
  - Enables detailed debugging and performance monitoring.

- **Modular Utility Design**  
  - Clean separation of concerns:
    - Engine orchestration
    - Intent classification
    - Session memory
    - Tracing and logging

---

## 🩺 The Solution Overview

✅ Classifying user intent with a dedicated LLM prompt.  
✅ Routing messages to different LangChain chains for specialized tasks.  
✅ Maintaining per-session memory to preserve conversational context.  
✅ Adding observability and traceability to all LLM calls using Langfuse.  

The result is a robust, modular, and extensible architecture that can be adapted for many production use-cases (customer support, summarization assistants, internal knowledge bots, etc.).

---

## 🛠️ How the Solution Was Built

The system is structured around four main modules:

### 1️⃣ Engine Orchestration (`engine.py`)
- Entry point with a single `respond()` function.
- Accepts a user message and session data (including chat history).
- Uses LangChain’s `ConversationBufferMemory` to retrieve/store history.
- Calls the **Intent Router** to classify the message and select a processing chain.
- Executes the selected chain and appends the result to the chat history.
- Returns the assistant's response.

### 2️⃣ Intent Classification & Routing (`utils/intent_router.py`)
- Defines a `PromptTemplate` for strict intent classification.
- Uses OpenAI GPT-4o-mini to label messages as `"summarization"`, `"question_answering"`, or `"something_else"`.
- Based on the detected intent, dynamically selects and runs the appropriate LangChain chain.
- Uses `LLMChain` for consistent execution of prompts.

### 3️⃣ Session-Level Memory (`utils/session_memory.py`)
- Implements an in-memory session store using Python dictionaries.
- Each session ID maps to a `ConversationBufferMemory` instance.
- Ensures all user conversations maintain context, even across multiple turns.

### 4️⃣ Observability with Langfuse (`utils/langfuse_tracer.py`)
- Decorator-based tracing using Langfuse’s Python SDK.
- Automatically wraps the `respond()` call with observability.
- Captures inputs, outputs, errors, and latency for analysis in the Langfuse UI.

---

## ⚙️ Tech Stack & Rationale

| Technology | Purpose | Pros |
|------------|---------|------|
| **Python** | Core programming language | Readable, widely adopted for AI work, rich ecosystem. |
| **LangChain** | LLM pipeline orchestration | Modular, supports chains, memory, prompt management. |
| **OpenAI GPT-4o-mini** | Language model backend | Fast, cost-effective, capable of nuanced classification. |
| **Langfuse** | Observability & tracing | Production-grade monitoring for LLM flows. |
| **ConversationBufferMemory** | Context storage | Maintains complete chat history for natural conversation continuity. |

**Design Choices:**
- Used LangChain for composability and standardization.
- Picked OpenAI GPT-4o-mini for strong performance at lower cost.
- Added Langfuse for traceability and easier debugging of complex flows.

---

### 🧭 Design Choices & Rationale

#### **Why We Didn't Use FAISS, Chroma, or a Vector Store**

This project deliberately avoids adding a vector database (like FAISS, Chroma, or AstraDB).  

✅ **Reasoning:**
- The current scale of the chatbot **doesn't involve millions of documents** or large-scale retrieval needs.
- There's no requirement for **long-term persistence** of embeddings between sessions.
- Adding a full vector store would be **overengineering**, consuming more resources (RAM, disk, compute) without delivering meaningful value in this use-case.
- Instead, the system uses **LangChain’s native ConversationBufferMemory**, which is:
  - Ephemeral
  - Session-scoped
  - Lightweight
  - Cheap to run

✅ **Benefits of This Choice:**
- Minimal resource consumption.
- Lower operational overhead.
- Simpler deployment (no extra DB setup or hosting).
- Easier maintenance for small-scale or prototype deployments.
- Leaves room for **easy upgrades** later if requirements change.

---

##✅ Conclusion:
> By focusing on a leaner design, this project aligns its architecture with its actual scale and avoids unnecessary complexity.

---

## 🗺️ High-Level Architecture

### 📜 Text Description
The chatbot engine acts as an orchestrator:

1️⃣ Receives user message and retrieves session context.  
2️⃣ Uses a classification prompt to detect the intent (e.g., summarization vs question answering).  
3️⃣ Routes the message to the appropriate LangChain pipeline based on intent.  
4️⃣ Executes the selected chain, returning the LLM’s result.  
5️⃣ Logs the entire process with Langfuse for observability.  
6️⃣ Updates the chat history in memory for future turns.  

---

### 🎨 ASCII Diagram

```text
                                                                 ┌──────────────────────┐
                                                                 │     User Input       │
                                                                 └─────────┬────────────┘
                                                                           │
                                                                 ┌─────────▼────────────┐
                                                                 │ Retrieve Session     │
                                                                 │   Conversation Memory│
                                                                 └─────────┬────────────┘
                                                                           │
                                                                 ┌─────────▼────────────┐
                                                                 │ Intent Classification│
                                                                 │   (LLM Prompt)       │
                                                                 └─────────┬────────────┘
                                                                           │
                                                                   ┌───────▼─────────────┐
                                                                   │ Intent Router       │
                                                                   │ - Summarization     │
                                                                   │ - Question Answering│
                                                                   │ - Fallback          │
                                                                   └───────┬─────────────┘
                                                                           │
                                                                   ┌───────▼────────────┐
                                                                   │ Selected Chain     │
                                                                   │ (LangChain LLM)    │
                                                                   └───────┬────────────┘
                                                                           │
                                                                 ┌─────────▼────────────┐
                                                                 │   Langfuse Tracing   │
                                                                 │   - Logs Input/Output│
                                                                 │   - Observability    │
                                                                 └─────────┬────────────┘
                                                                           │
                                                                 ┌─────────▼─────────────┐
                                                                 │     Chatbot Reply     │
                                                                 └───────────────────────┘

