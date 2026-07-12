---
marp: true
theme: default
paginate: true
---

<!-- Slide 1 -->

# Finance FAQ Assistant
### Fine-Tuned with Unsloth — Non-Instruction FT → SFT → DPO

Qwen2.5-0.5B · a single free Google Colab T4, start to finish

---

<!-- Slide 2 -->

## 🏆 The Final Result

### ✅ 3-Stage Pipeline — Fully Executed, Zero Errors, on a Free Colab T4

| Stage 1 Loss | Stage 2 Loss | Stage 3 Loss |
|:---:|:---:|:---:|
| **2.0659** | **2.0564** | **0.2995** |

**Q: "What is a SIP?"**

- **Base model:** *"I'm sorry, but I can't assist with that."*
- **Fine-tuned model:** *"A SIP, or Systematic Investment Plan, lets you invest a fixed amount at regular intervals..."* — correct, on-topic, direct.

*Full breakdown — including one honest DPO limitation we identified and analyzed — in the report.*

---

<!-- Slide 3 -->

## Problem Statement

### ❌ A general-purpose LLM is not a domain assistant.

Untrained Qwen2.5-0.5B-Instruct on *"How can I apply for a personal loan?"*: generic AI-disclaimer opener, three vague bullet points that could apply to any financial product.

### 🎯 Goal

Build a Finance FAQ Assistant that answers real customer questions — savings & current accounts, loans, credit cards, mutual funds, insurance, tax — accurately and directly, entirely on a free-tier GPU. No paid API, no large model, no proprietary infrastructure.

---

<!-- Slide 4 -->

## 💾 Type of Data — 3 Stages, 3 Formats

| Stage | Data | Format | Teaches |
|---|---|---|---|
| **Stage 1 — Raw Text** | 57 raw finance paragraphs (`non_instruction_data.txt`) | No Q&A structure — plain domain text | Vocabulary |
| **Stage 2 — Instruction Pairs** | 104 instruction-response pairs (`instruction_dataset.jsonl`) | Real Q&A format | The behavior of answering |
| **Stage 3 — Preference Pairs** | 51 chosen/rejected pairs (`preference_dataset.jsonl`) | Two answers per prompt | Which answer is preferred |

---

<!-- Slide 5 -->

## ▶️ Let's See It Live

Switching to the notebook — non-instruction FT → SFT → DPO, real outputs, no cuts

>
> `[SWITCH TO NOTEBOOK / COLAB]`
