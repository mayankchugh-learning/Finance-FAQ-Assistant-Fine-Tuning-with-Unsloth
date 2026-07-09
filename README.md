# Finance FAQ Assistant — Domain-Specific Fine-Tuning with Unsloth

A practical, end-to-end fine-tuning project that takes a small open-source LLM (`Qwen2.5-0.5B`) through three stages — non-instruction fine-tuning, instruction fine-tuning, and DPO preference alignment — to build a domain-specific **Finance FAQ Assistant** using [Unsloth](https://github.com/unslothai/unsloth).

```
Base Model (Qwen2.5-0.5B)
      ↓
Stage 1: Non-Instruction Fine-Tuning  (domain vocabulary & style)
      ↓
Stage 2: Instruction Fine-Tuning      (Q&A behavior)
      ↓
Stage 3: DPO Preference Alignment     (response quality & safety)
      ↓
Final Domain-Specific Finance FAQ Assistant
```

## 1. Domain Selected

**Finance FAQ Assistant** — an internal AI assistant that answers everyday personal-finance and banking questions.

## 2. Business Problem

A company wants an internal assistant that employees or customers can ask finance-related questions and get clear, accurate, domain-specific answers — instead of generic, hedge-heavy responses from an untuned general-purpose model. The assistant covers topics including:

- Savings, current, fixed, and recurring deposit accounts
- Credit cards, debit cards, and credit scores
- Personal, home, and auto loans, EMI, and loan default/foreclosure
- Mutual funds, SIPs, NAV, demat accounts, and stock market basics
- Insurance (term, health), claims, deductibles, and no-claim bonus
- Income tax, TDS, capital gains, and tax deductions/exemptions
- General banking operations (KYC, net banking, standing instructions, wire transfers, fraud protection)

## 3. Dataset Details

All datasets were custom-written for this project (verified, cleaned, and self-consistent finance content), living under `data/`:

| File | Purpose | Size |
|---|---|---|
| `non_instruction_data.txt` | Raw domain paragraphs for Stage 1 continued pre-training | 57 paragraphs |
| `instruction_dataset.jsonl` | Instruction/response pairs for Stage 2 SFT | 104 examples |
| `preference_dataset.jsonl` | Chosen/rejected pairs for Stage 3 DPO | 51 pairs |

Each preference example pairs a correct, helpful, professional **chosen** answer against an incorrect, unsafe, dismissive, or overly generic **rejected** answer for the same finance question.

## 4. Base Model Used

**`unsloth/Qwen2.5-0.5B`** (and the `-Instruct` variant as the baseline reference for evaluation), loaded in 4-bit via Unsloth for QLoRA-style fine-tuning. Chosen because it is small enough to fine-tune on a free Google Colab T4 GPU across all three stages within a reasonable time budget, while still being instruction-capable enough to show a clear before/after improvement.

## 5. Non-Instruction Fine-Tuning Approach (Stage 1)

- Raw finance paragraphs are cleaned (whitespace normalization, non-ASCII stripping) and chunked to ≤150 words per chunk.
- The model is trained with a plain causal-LM objective (next-token prediction) on this raw text — **no instruction format, no chat template.**
- Goal: get the model fluent in finance vocabulary and phrasing *before* it learns to answer questions.
- Implementation: `notebooks/non_instruction_finetuning.ipynb`.

## 6. Instruction Fine-Tuning Approach (Stage 2)

- Continues from the Stage 1 adapter (or the base model if Stage 1 is skipped).
- The 104 instruction/response pairs are formatted using Qwen2.5's chat template (`user` / `assistant` turns).
- Standard supervised fine-tuning (SFT) via `trl.SFTTrainer`, training the model to answer finance questions directly and concisely.
- Implementation: `notebooks/instruction_finetuning.ipynb` (this notebook also runs the **base model evaluation** and **base-vs-SFT comparison** steps).

## 7. DPO Alignment Approach (Stage 3)

- Continues from the Stage 2 SFT adapter.
- The 51 preference pairs are formatted as `(prompt, chosen, rejected)` using the same chat template, then trained with `trl.DPOTrainer`.
- DPO directly optimizes the model to prefer the `chosen` response over the `rejected` response for the same prompt, without needing a separate reward model.
- A lower learning rate (5e-6) is used compared to SFT (2e-4), since DPO updates are more sensitive to instability.
- Implementation: `notebooks/dpo_alignment.ipynb`.

## 8. LoRA / QLoRA Configuration

| Stage | Rank | Alpha | Dropout | Learning Rate | Effective Batch Size |
|---|---|---|---|---|---|
| Non-instruction FT | 16 | 16 | 0.05 | 2e-4 | 16 |
| Instruction FT (SFT) | 16 | 16 | 0.05 | 2e-4 | 16 |
| DPO alignment | 16 | 16 | 0.05 | 5e-6 | 8 |

All stages use 4-bit base model loading (`load_in_4bit=True`) for QLoRA-style memory efficiency, with LoRA adapters applied to `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`. See `reports/fine_tuning_explanation.md` for the full reasoning behind these choices.

## 9. Training Screenshots / Logs

> Add your actual training loss curves / Colab screenshots here after running each notebook, e.g.:
> - `assets/stage1_training_log.png`
> - `assets/stage2_training_log.png`
> - `assets/stage3_dpo_loss.png`

## 10. Before vs. After Output Comparison

See:
- `reports/base_model_evaluation.md` — base model on 10 questions (Step 5)
- `reports/sft_model_comparison.md` — base vs. SFT model (Step 7)
- `reports/final_evaluation.md` — base vs. SFT vs. DPO model, 3-way comparison (Step 10)

**Expected pattern:** the base model gives generic, hedge-heavy answers; the SFT model gives concise, domain-correct answers matching the training style; the DPO model gives the most consistently helpful, safe, and professionally worded answers among the three.

## 11. Final Observations

- Non-instruction fine-tuning alone does not teach Q&A behavior — it only improves domain fluency. Instruction fine-tuning is what makes the model usable as an assistant.
- DPO is most valuable for **edge cases and tone** — situations where the SFT model's answer is technically present but weak, incomplete, or unsafe in framing. DPO sharpens these specific failure modes using direct contrastive examples.
- A 0.5B model is a good fit for quickly demonstrating the *pipeline*, but is not a substitute for a larger model or for retrieval-augmented generation (RAG) if factual grounding against a live, large policy/document corpus is required in production.

## 12. Challenges Faced

- Keeping the non-instruction dataset purely *raw text* (no Q&A format) while still being information-dense enough to meaningfully shift the model's domain vocabulary.
- Designing rejected responses for DPO that are realistic failure modes (vague, unsafe, dismissive) rather than strawman answers, so the preference signal is meaningful.
- Balancing dataset size against Colab T4 time/memory limits across three sequential fine-tuning stages.

## 13. Future Improvements

- Expand the instruction and preference datasets significantly (e.g., 500+ examples) for a more robust assistant.
- Add retrieval-augmented generation (RAG) over actual company finance policy documents so answers are grounded in a verifiable source rather than relying purely on what was memorized during fine-tuning.
- Run a quantitative evaluation (e.g., automatic LLM-as-judge scoring) on a larger held-out question set, beyond the 10 manually reviewed questions.
- Experiment with ORPO as an alternative to DPO, since it doesn't require a separate reference model and may train faster.
- Try a slightly larger base model (Qwen2.5-1.5B) to see how much of the quality gain is data-driven vs. model-size-driven.

## Repository Structure

```
domain-ai-assistant-finetuning/
│
├── data/
│   ├── non_instruction_data.txt       # 57 raw domain paragraphs (Stage 1)
│   ├── instruction_dataset.jsonl      # 104 instruction/response pairs (Stage 2)
│   └── preference_dataset.jsonl       # 51 chosen/rejected pairs (Stage 3)
│
├── notebooks/
│   ├── non_instruction_finetuning.ipynb
│   ├── instruction_finetuning.ipynb   # includes base model eval + SFT comparison
│   └── dpo_alignment.ipynb
│
├── reports/
│   ├── base_model_evaluation.md
│   ├── sft_model_comparison.md
│   ├── final_evaluation.md
│   └── fine_tuning_explanation.md
│
├── src/
│   └── inference.py
│
├── README.md
└── requirements.txt
```

## How to Run

1. Open each notebook in Google Colab with a **T4 GPU runtime** (Runtime → Change runtime type → T4 GPU).
2. Upload the relevant file(s) from `data/` when prompted, or clone this repo into the Colab environment.
3. Run notebooks in order: `non_instruction_finetuning.ipynb` → `instruction_finetuning.ipynb` → `dpo_alignment.ipynb`. Each stage saves a LoRA adapter that the next stage loads.
4. After Stage 3, download `finance_dpo_adapter/` and use it with `src/inference.py` to ask questions interactively.

```bash
pip install -r requirements.txt
python src/inference.py --question "How can I apply for reimbursement?"
```
