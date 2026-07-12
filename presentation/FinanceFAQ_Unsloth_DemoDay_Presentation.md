---
marp: true
theme: default
paginate: true
---

<!-- Slide 1 -->

# Finance FAQ Assistant
### Fine-Tuned with Unsloth — Non-Instruction FT → SFT → DPO

Qwen2.5-0.5B · a single free Google Colab T4, start to finish

*by Mayank Chugh*

> **Speaker notes:** Good [morning/afternoon] everyone. I'm Mayank Chugh, and today I'm presenting my Finance FAQ Assistant — fine-tuned with Unsloth through three real stages: non-instruction fine-tuning, instruction fine-tuning, and DPO preference alignment. All on a single free Colab T4 GPU. I'm going to show you the result first, then walk back through the problem, the data, and a live demo.

---

<!-- Slide 2 -->

## 🏆 The Final Result

### ✅ SFT: Refusal → Correct Answer

**Q: "What is a SIP?"**

- Base: *"I'm sorry, but I can't assist with that."*
- SFT: *"A SIP, or Systematic Investment Plan, lets you invest a fixed amount at regular intervals..."*

Real, measurable improvement in the first sentence — every one of the 10 eval questions.

### ⚠️ DPO: A Real Regression

**Same question, after DPO:**

- DPO: *"A SIP (Simple Account Payment) is a prepaid bill..."* — hallucinated, wrong.

With only 51 preference pairs and 3 epochs, DPO did not uniformly improve the model — **kept in, not edited out.**

> **Speaker notes:** Let me start with what actually happened, both the win and the honest miss. On the left: the core success. Ask the untrained base model "What is a SIP?" and it refuses outright. After instruction fine-tuning, the same question gets a correct, on-topic answer — Systematic Investment Plan, correctly defined. That kind of improvement held across all 10 evaluation questions. On the right: I want to be upfront about something. DPO — the final alignment stage — is supposed to be the polish step. On this exact question, it made the answer worse. It invented "Simple Account Payment," which isn't a real term. With only 51 preference pairs and 3 training epochs, DPO didn't uniformly improve the model. I'm not editing that out — it's a genuine finding about DPO at small scale, and it's more useful to show you than to hide.

---

<!-- Slide 3 -->

## Problem Statement

### ❌ A general-purpose LLM is not a domain assistant.

Untrained Qwen2.5-0.5B-Instruct on *"How can I apply for a personal loan?"*: generic AI-disclaimer opener, three vague bullet points that could apply to any financial product.

### 🎯 Goal

Build a Finance FAQ Assistant that answers real customer questions — savings & current accounts, loans, credit cards, mutual funds, insurance, tax — accurately and directly, entirely on a free-tier GPU. No paid API, no large model, no proprietary infrastructure.

> **Speaker notes:** Why does this need fine-tuning at all? Because a general-purpose model isn't a domain assistant out of the box. Ask the untrained base model how to apply for a personal loan, and you get a hedging AI-disclaimer opener followed by generic bullet points that could apply to literally any financial product. The goal: build a Finance FAQ Assistant that answers real customer questions directly and accurately, across savings accounts, loans, credit cards, mutual funds, insurance, and tax — and do it entirely on a free-tier GPU, no paid API required.

---

<!-- Slide 4 -->

## 💾 Type of Data — 3 Stages, 3 Formats

| Stage | Data | Format | Teaches |
|---|---|---|---|
| **Stage 1 — Raw Text** | 57 raw finance paragraphs (`non_instruction_data.txt`) | No Q&A structure — plain domain text | Vocabulary |
| **Stage 2 — Instruction Pairs** | 104 instruction-response pairs (`instruction_dataset.jsonl`) | Real Q&A format | The behavior of answering |
| **Stage 3 — Preference Pairs** | 51 chosen/rejected pairs (`preference_dataset.jsonl`) | Two answers per prompt | Which answer is preferred |

> **Speaker notes:** Three stages, three different data formats, on purpose. Stage 1 is 57 raw finance paragraphs — no question-answer structure, just plain text to build domain vocabulary. Stage 2 is 104 real instruction-response pairs, teaching the model the actual behavior of answering a question. Stage 3 is 51 preference pairs — for each prompt, a chosen answer and a rejected answer, teaching the model which response a user would actually prefer. Each stage's data format matches what that stage is trying to teach — that's deliberate, not incidental.

---

<!-- Slide 5 -->

## ▶️ Let's See It Live

Switching to the notebook — non-instruction FT → SFT → DPO, real outputs, no cuts

> **Speaker notes:** That's the setup. Now let's see it live — I'm switching over to the notebook now, and I'll walk through all three stages with real outputs, including the parts that didn't go perfectly. No cuts, no cherry-picking.
>
> `[SWITCH TO NOTEBOOK / COLAB]`
