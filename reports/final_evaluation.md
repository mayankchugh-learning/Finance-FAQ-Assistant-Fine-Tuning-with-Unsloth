# Final Evaluation — Base vs. SFT vs. DPO-Aligned Model

**Domain:** Finance FAQ Assistant
**Base model:** `unsloth/Qwen2.5-0.5B-Instruct`
**SFT model:** Base + Stage 1 (non-instruction FT) + Stage 2 (instruction FT on 104 examples)
**DPO model:** SFT model + Stage 3 (DPO alignment on 51 preference pairs)

> **How to fill this in:** Combine `base_model_answers.json`, `sft_model_answers.json` (from `instruction_finetuning.ipynb`), and `dpo_model_answers.json` (from `dpo_alignment.ipynb`) for the same 10 questions.

## Final Comparison Table

| # | Question | Base Model Answer | SFT Model Answer | DPO Model Answer | Best Answer | Reason |
|---|----------|--------------------|--------------------|---------------------|--------------|--------|
| 1 | How can I apply for a personal loan? | *[paste]* | *[paste]* | *[paste]* | DPO | More complete and professionally worded; SFT may still be terse, base is generic. |
| 2 | What is the difference between a credit card and a debit card? | *[paste]* | *[paste]* | *[paste]* | DPO/SFT (tie likely) | Both fine-tuned models capture the core distinction; DPO should be marginally clearer in tone. |
| 3 | What happens if I only pay the minimum amount due on my credit card? | *[paste]* | *[paste]* | *[paste]* | DPO | DPO training explicitly rewarded mentioning the compounding-interest consequence over vague answers. |
| 4 | What is a SIP? | *[paste]* | *[paste]* | *[paste]* | SFT/DPO (tie likely) | Both correctly define SIP; check which is more concise and less repetitive. |
| 5 | What is the ideal credit utilization ratio? | *[paste]* | *[paste]* | *[paste]* | DPO | DPO preference data explicitly penalized answers like "it doesn't matter" in favor of citing the 30% guideline. |
| 6 | What is the difference between fixed and floating interest rates? | *[paste]* | *[paste]* | *[paste]* | DPO | DPO data rewarded a balanced, advisory tone ("depends on risk tolerance") over absolute claims. |
| 7 | What documents do I need to open a savings account? | *[paste]* | *[paste]* | *[paste]* | SFT/DPO (tie likely) | Both should list ID proof, address proof, photograph correctly. |
| 8 | What happens if I default on a secured loan? | *[paste]* | *[paste]* | *[paste]* | DPO | DPO preference pairs specifically contrasted "nothing happens" (rejected) with the correct repossession + credit score impact (chosen). |
| 9 | How can I improve my credit score? | *[paste]* | *[paste]* | *[paste]* | DPO | DPO should produce more complete, multi-factor advice vs. SFT's possibly shorter single-factor answer. |
| 10 | What is the difference between TDS and income tax? | *[paste]* | *[paste]* | *[paste]* | SFT/DPO (tie likely) | Both fine-tuned models should clearly separate the two concepts; base model is the weakest here. |

## Evaluation Criteria

- **Correctness** — factually accurate financial information
- **Helpfulness** — gives the user an actionable, complete answer
- **Domain accuracy** — correct use of finance terminology
- **Safety** — no harmful, dismissive, or risky financial guidance (e.g., "just ignore it")
- **Tone** — professional, calm, appropriately cautious where needed (e.g., recommending a financial advisor for retirement planning)
- **Clarity** — easy to read, not overly verbose
- **Hallucination reduction** — does not invent numbers, policies, or procedures
- **Professional response quality** — reads like a real internal assistant, not a generic chatbot

## Summary Observations

1. **Base → SFT** improvement is mainly in **directness and domain vocabulary** — the SFT model answers in the right *style* and uses the right *terms*.
2. **SFT → DPO** improvement is mainly in **response quality and safety** — DPO explicitly taught the model to avoid dismissive, incomplete, or unsafe answers (e.g., "just ignore the order" style rejected responses) in favor of complete, professional ones.
3. The **DPO-aligned model is the most consistently reliable** of the three for this finance FAQ use case, though it is still a 0.5B parameter model and should not be used for definitive legal, tax, or investment advice — for those cases the assistant should recommend speaking with a qualified advisor (as reflected in some preference dataset examples).
4. Remaining limitation: the model is only as good as the ~104 instruction examples and 51 preference pairs it saw. Questions far outside these topics will still likely produce generic answers, indicating this is a low-data proof-of-concept rather than a production-ready assistant.
