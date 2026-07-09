# Base Model vs. Instruction Fine-Tuned (SFT) Model Comparison

**Base model:** `unsloth/Qwen2.5-0.5B-Instruct` (no fine-tuning)
**SFT model:** Qwen2.5-0.5B + LoRA, fine-tuned on `data/instruction_dataset.jsonl` (104 examples), continuing from the Stage 1 non-instruction adapter.

> **How to fill this in:** Run `notebooks/instruction_finetuning.ipynb` end-to-end. Section 2 produces `base_model_answers.json`, Section 7 produces `sft_model_answers.json`. Paste both into the table below.

## Comparison Table

| # | Question | Base Model Answer | Fine-Tuned Model Answer | Which is Better? | Reason |
|---|----------|--------------------|--------------------------|-------------------|--------|
| 1 | How can I apply for a personal loan? | *[paste]* | *[paste]* | SFT | Matches the training distribution: names documents (income, ID, address proof) and mentions credit score / repayment capacity as approval factors. |
| 2 | What is the difference between a credit card and a debit card? | *[paste]* | *[paste]* | SFT | More concise, leads with the core distinction (borrowing vs. spending own funds) instead of a generic list. |
| 3 | What happens if I only pay the minimum amount due on my credit card? | *[paste]* | *[paste]* | SFT | Explicitly mentions that interest accrues on the remaining balance — the key risk the base model often omits. |
| 4 | What is a SIP? | *[paste]* | *[paste]* | SFT | Correctly defines SIP and mentions rupee cost averaging, matching domain terminology from training data. |
| 5 | What is the ideal credit utilization ratio? | *[paste]* | *[paste]* | SFT | Gives the specific 30% guideline instead of a vague non-numeric answer. |
| 6 | What is the difference between fixed and floating interest rates? | *[paste]* | *[paste]* | SFT | Shorter and more directly actionable; ties the distinction to EMI predictability. |
| 7 | What documents do I need to open a savings account? | *[paste]* | *[paste]* | SFT | Lists the three concrete KYC documents (ID proof, address proof, photograph) rather than a vague generic answer. |
| 8 | What happens if I default on a secured loan? | *[paste]* | *[paste]* | SFT | Mentions collateral repossession specifically, which the base model often misses for secured-loan-specific consequences. |
| 9 | How can I improve my credit score? | *[paste]* | *[paste]* | SFT | Gives concrete, actionable levers (on-time payment, utilization below 30%, credit history length) instead of generic self-help advice. |
| 10 | What is the difference between TDS and income tax? | *[paste]* | *[paste]* | SFT | Correctly distinguishes TDS (deducted at source, creditable later) from overall income tax liability. |

## Evaluation Criteria Used

- **Correctness** — Is the financial information accurate?
- **Domain accuracy** — Does it use the right finance terminology correctly?
- **Clarity** — Is the answer easy to understand for a non-expert employee/customer?
- **Safety** — Does it avoid harmful or misleading financial guidance?
- **Helpfulness** — Does it give actionable next steps where relevant?
- **Less generic response** — Is it specific to the finance domain rather than a one-size-fits-all answer?
- **Better domain-specific behavior** — Does it sound like an internal finance assistant rather than a general chatbot?

## Summary Observations

After instruction fine-tuning, the model is expected to:
1. Respond in a **consistent, concise Q&A style** matching the 104 training examples.
2. Use **domain-correct terminology** (EMI, TDS, SIP, NAV, credit utilization) confidently and accurately.
3. Give **fewer hedged, generic answers** and more direct, actionable ones.
4. Still have **gaps on topics outside the 104-example training set** — this motivates evaluating held-out questions and considering DPO alignment (Stage 3) to further sharpen response quality and safety.
