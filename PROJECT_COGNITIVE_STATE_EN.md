# 🤖 PROJECT_COGNITIVE_STATE.md (English Version)
# (When starting a new conversation, copy and paste the entire contents of this file)

---

## 1. Core Instructions (COGNITIVE_CORE)
# (AI must reload these instructions upon each resume)

* **Role:** Cognitive Architecture Learning Engine.
* **Principle 1 (CLT):** Assume I am a novice. Minimize extraneous load. Use "less is more", "signaling", and "dual coding" (text diagrams).
* **Principle 2 (Expertise):** Must use "direct instruction" and "blocked practice". No "inquiry-based learning".
* **Principle 3 (Retrieval):** Reject passivity. Each teaching unit must have "generative" "knowledge retrieval challenges".
* **Principle 4 (State):** Must parse `LEARNING_STATE` and automatically execute `[Next Action]`. Must generate complete update of this file at end of each response.

---

## 2. Learning Progress (LEARNING_STATE)

**Project Goal:** LangChain is a Python framework for building AI agents and LLM-powered applications. It simplifies complex AI application development through composable abstractions (Runnable, Messages, Prompts, Chat Models, etc.) and provides integrations with third-party services.

**Learning Outline (Teaching Schema):**
* [X] **Module 1: Architecture & Core Concepts** - Understanding Monorepo structure, design philosophy, and the "why" of core abstractions
* [X] **Module 2: Message System** - Mastering LangChain's message objects (HumanMessage, AIMessage, SystemMessage)
* [X] **Module 3: Prompt Engineering** - Learning prompt template system and best practices
* [X] **Module 4: Core Runnable Abstraction** - Deep dive into Runnable protocol (invoke, batch, stream)
* [X] **Module 5: Chat Models** - Understanding BaseChatModel abstraction and model integrations
* [X] **Module 6: Chain Composition (LCEL)** - Learning to compose components using LangChain Expression Language
* [X] **Module 7: Tools & Agents** - Implementing tool calling and building autonomous agents
* [X] **Module 8: Advanced Features** - Callbacks, Streaming, Retrieval Augmented Generation (RAG)
* [ ] **Final Stage: Interleaved Practice & Real Projects** - Applying all concepts to build complete applications

**Current Status:**
* **Completed Modules:** ✅ All 8 core modules completed! (2025-11-16)
    * ✅ Module 1: Architecture & Core Concepts
        - Monorepo structure, three design principles
    * ✅ Module 2: Message System
        - HumanMessage, AIMessage, SystemMessage, ToolMessage
    * ✅ Module 3: Prompt Engineering
        - PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
    * ✅ Module 4: Core Runnable Abstraction
        - invoke/batch/stream/ainvoke, RunnableSequence, RunnableParallel
    * ✅ Module 5: Chat Models
        - BaseChatModel, bind_tools, with_structured_output
    * ✅ Module 6: Chain Composition (LCEL)
        - Pipe operator, parallel composition, conditional branching, RAG chains
    * ✅ Module 7: Tools & Agents
        - @tool decorator, agent loops, LangGraph introduction
    * ✅ Module 8: Advanced Features
        - Callbacks, Streaming, Memory, Caching, Output Parsers

* **Complete Learning Materials:** See `LEARNING_MODULES_COMPLETE_EN.md`

* **Next Actions:**
    * **[Recommended] -> Hands-on Practice** - Build a technical documentation Q&A system (see Module 8 final challenge)
    * **[Recommended] -> Read Source Code** - Deep dive into test cases in `libs/core/tests/`
    * **[Recommended] -> Review Examples** - Browse real-world case studies in official docs

---

## 3. Learning Notes (LEARNING_NOTES)
# (This area records your personal notes, questions, and key insights)

### Module 1 Key Points
* **Mental Map Established:** LangChain = composable LEGO blocks, core is `Runnable` protocol
* **Remember Path:** `/home/user/langchain/libs/core/langchain_core/` (core code location)
* **4 Must-Remember Methods:** `invoke()`, `batch()`, `stream()`, `ainvoke()`
* **Pipe Symbol:** `component1 | component2` = RunnableSequence (automatically supports all methods)

---

## 4. Metadata (META)

* **Created:** 2025-11-16
* **Last Updated:** 2025-11-16 (All modules completed)
* **Project Path:** `/home/user/langchain`
* **Current Branch:** `claude/cognitive-learning-engine-01NCgLE2JZcoqsgED5Ye76Ep`
* **LangChain Core Module Path:** `/home/user/langchain/libs/core/langchain_core/`
