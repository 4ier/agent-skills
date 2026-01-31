# OFFLOAD2 — Design Brief for Agent Implementation

## 0. Read This First (Non-Negotiable)

**OFFLOAD2 is NOT a system, service, memory, or logging platform.**
It is a **local agent skill** whose only purpose is to act as a **cognitive pressure release valve** during execution.

If you design it as:

* a reusable memory
* a debugging framework
* a reliable logging system
* a distributed or shared component

then you have misunderstood the task.

---

## 1. What Problem OFFLOAD2 Solves

During execution, agents frequently generate internal states that:

* are not final answers
* are not safe to carry forward
* increase reasoning pressure
* would degrade output quality if forced into conclusions

Normally, these states are silently discarded.

**OFFLOAD2 exists to make these invisible pressure points visible to prompt engineers**, without affecting the agent’s behavior.

OFFLOAD2 does **not** help the agent solve the task.
It helps **humans understand where the prompt causes friction**.

---

## 2. What OFFLOAD2 Is (Conceptually)

OFFLOAD2 is:

* a **one-way action**
* a **non-blocking side effect**
* a **deliberately unreliable sink**
* a **local-only artifact**

It represents this semantic act:

> “This internal state cannot be carried forward.
> I am explicitly letting it go.”

That’s it.

---

## 3. What OFFLOAD2 Is NOT

OFFLOAD2 must **not** become any of the following:

* ❌ agent memory
* ❌ long-term storage
* ❌ retrievable knowledge
* ❌ input to future reasoning
* ❌ a correctness signal
* ❌ something the agent depends on

The agent must behave **identically** whether OFFLOAD2 succeeds or fails.

---

## 4. Behavioral Contract (Strict)

When the OFFLOAD2 skill is invoked:

1. Accept arbitrary text from stdin
2. Attach session metadata (provided externally)
3. Append it to a **local log file**
4. Return **no meaningful output**
5. If anything fails → **silently ignore and continue**

**Failure is acceptable. Silence is correct behavior.**

---

## 5. Scope and Environment

### 5.1 Execution Environment

* Must run using **only OS-native tools**

  * Bash
  * echo / printf
  * file append (`>>`)
* No services
* No network
* No background processes
* No daemons
* No dependencies

### 5.2 Platform Coverage

* Linux
* macOS
* Windows (Git Bash / WSL)

---

## 6. Session Semantics (Very Important)

OFFLOAD2 requires **session context**, but:

* session ≠ identity
* session ≠ authentication
* session ≠ user tracking

Session exists solely to group offloads from the same run.

### Required session properties:

* `session_id` (string)
* `timestamp` (UTC)

### Optional (but recommended):

* agent name
* task name
* prompt version
* turn index

Session data is **provided via environment variables**, not computed by the agent.

The agent must **not infer or invent session meaning**.

---

## 7. Data Format Requirements

* Output format: **JSON Lines (.jsonl)**
* Append-only
* One record per offload
* Human-readable
* Machine-greppable

Example record shape:

```json
{
  "ts": "...",
  "session_id": "...",
  "agent": "...",
  "task": "...",
  "prompt_version": "...",
  "turn": 7,
  "content": "text"
}
```

No indexing. No querying. No guarantees.

---

## 8. Security & Sensitivity (Minimal but Required)

Because this is local and private:

* Do **not** over-engineer security
* Do **not** block writes due to sensitive content
* Do **basic masking only** (optional but recommended)

Minimum acceptable masking:

* obvious API keys
* obvious tokens

Do **not** attempt full secret detection.
Prompt engineers remain responsible for local data handling.

---

## 9. Agent Usage Rules (Must Be Followed)

When using OFFLOAD2, the agent must understand:

* OFFLOAD2 is **not feedback**
* OFFLOAD2 is **not confirmation**
* OFFLOAD2 is **not persistence**

The agent should offload when:

* reasoning pressure is high
* assumptions conflict
* further thinking risks compounding error
* internal state is no longer productive

The agent should **never**:

* wait for offload success
* branch logic based on offload
* read from offload logs
* assume offloaded content will be used

---

## 10. Failure Semantics (Critical)

If OFFLOAD2 fails:

* the agent continues normally
* no retries
* no fallback
* no error handling logic

This is intentional.

OFFLOAD2 is **permission**, not infrastructure.

---

## 11. Why This Matters (For You, the Implementing Agent)

If you implement OFFLOAD2 correctly:

* it will feel almost useless
* it will look trivial
* it will not improve agent output directly

That is expected.

Its value exists **outside the agent**, in how prompt engineers observe and refine prompts.

If it starts feeling “important” or “foundational” to execution, you’ve implemented it wrong.

---

## 12. One-Sentence Mental Model (Remember This)

> **OFFLOAD2 is not for the agent.
> It is for the human who designs the agent.**

---

## 13. Final Instruction

Implement OFFLOAD2 exactly as described:

* minimal
* local
* silent
* ignorable
* append-only
* disposable

Do not extend it.
Do not optimize it.
Do not generalize it.

If in doubt, **remove functionality**.
