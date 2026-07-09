# Base Model Evaluation — Finance FAQ Assistant

**Model:** `unsloth/Qwen2.5-0.5B-Instruct` (no fine-tuning)
**Domain:** Finance FAQ Assistant
**Purpose:** Establish a "before" baseline so we can measure the impact of non-instruction fine-tuning, instruction fine-tuning, and DPO alignment.

> **How to fill this in:** Run `notebooks/instruction_finetuning.ipynb`, Section 2 ("Load the BASE model and test it"). It will save `base_model_answers.json`. Paste each answer into the table below, then fill in the "Problem" column based on what you observe.

## Evaluation Table

| # | Question | Base Model Answer | Problem |
|---|----------|--------------------|---------|
| 1 | How can I apply for a personal loan? | *[paste generated answer]* | Generic — doesn't reflect our domain-specific application process or required documents. |
| 2 | What is the difference between a credit card and a debit card? | *[paste generated answer]* | Often correct at a high level, but lacks domain-specific detail (interest-free period, EMI on credit, etc.). |
| 3 | What happens if I only pay the minimum amount due on my credit card? | *[paste generated answer]* | May miss the compounding-interest consequence that is central to good financial guidance. |
| 4 | What is a SIP? | *[paste generated answer]* | Small base models often hallucinate or give an overly generic definition without mentioning rupee cost averaging. |
| 5 | What is the ideal credit utilization ratio? | *[paste generated answer]* | May not state the commonly recommended 30% threshold, or may give an answer with no actionable number. |
| 6 | What is the difference between fixed and floating interest rates? | *[paste generated answer]* | Tends to be correct conceptually but verbose and not tailored to a finance-assistant tone. |
| 7 | What documents do I need to open a savings account? | *[paste generated answer]* | Often vague ("identification documents") instead of specific (ID proof, address proof, photograph). |
| 8 | What happens if I default on a secured loan? | *[paste generated answer]* | May omit the collateral repossession consequence specific to secured loans. |
| 9 | How can I improve my credit score? | *[paste generated answer]* | Generic self-help advice rather than concrete, finance-specific levers (utilization, on-time payment, credit history length). |
| 10 | What is the difference between TDS and income tax? | *[paste generated answer]* | Small base models frequently confuse or conflate these two related-but-distinct concepts. |

## Summary Observations

- The base model tends to produce **generic, textbook-style answers** rather than the concise, direct, domain-grounded responses expected of an internal finance assistant.
- Domain-specific terminology (TDS, SIP, NAV, credit utilization ratio, no-claim bonus) is either explained imprecisely or with low confidence.
- Answers are often **longer than necessary** and contain disclaimers or hedging that an instruction-tuned, domain-specific assistant should reduce.
- This baseline motivates Stage 1 (non-instruction fine-tuning for domain vocabulary) and Stage 2 (instruction fine-tuning for direct Q&A behavior).
