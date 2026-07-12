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

### ✅ 3-Stage Pipeline — Fully Executed, Zero Errors, on a Free Colab T4

| Stage 1 Loss | Stage 2 Loss | Stage 3 Loss |
|:---:|:---:|:---:|
| **2.0659** | **2.0564** | **0.2995** |

**Q: "What is a SIP?"**

- **Base model:** *"I'm sorry, but I can't assist with that."*
- **Fine-tuned model:** *"A SIP, or Systematic Investment Plan, lets you invest a fixed amount at regular intervals..."* — correct, on-topic, direct.

*Full breakdown — including one honest DPO limitation we identified and analyzed — in the report.*

> **Speaker notes:** Here's the headline: all three fine-tuning stages ran to completion, end to end, with zero errors, entirely on a free Colab T4 — non-instruction fine-tuning, instruction fine-tuning, and DPO alignment. Those are the three real training losses, right off the actual runs. And here's what that pipeline actually produced. Ask the untrained base model "What is a SIP?" and it refuses outright. After fine-tuning, the same question gets a correct, on-topic answer — Systematic Investment Plan, correctly defined. That kind of improvement held across all 10 evaluation questions. One honest note, briefly: in my full analysis I also identified a specific limitation in the DPO stage at small scale — I go through it in detail in the written report, because I think understanding where a technique's limits are is part of doing this properly. But the headline is that the pipeline works, end to end, and it measurably improves how the assistant answers real questions.

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
