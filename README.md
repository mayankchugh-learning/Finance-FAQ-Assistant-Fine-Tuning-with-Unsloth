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

**Walkthrough video:** [YouTube — Finance FAQ Fine-Tuning with Unsloth](https://youtu.be/YHtjQjd981g)

Architecture diagram (Mermaid) and walkthrough slides live under [`presentation/`](presentation/).

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
- Typical run: LoRA r=16, α=16, dropout=0.05, lr `2e-4`, 3 epochs (~12 steps); final loss ≈ **2.066**.
- Implementation: `notebooks/non_instruction_finetuning_annotated.ipynb`.
- Adapter artifact: `finance_stage1_adapter` (zipped under `outputs/`).

## 6. Instruction Fine-Tuning Approach (Stage 2)

- Continues from the Stage 1 adapter (loaded via Hugging Face Hub `snapshot_download` between Colab sessions).
- The 104 instruction/response pairs are formatted using Qwen2.5's chat template (`user` / `assistant` turns).
- Standard supervised fine-tuning (SFT) via `trl.SFTTrainer`, training the model to answer finance questions directly and concisely.
- Typical run: continue LoRA from Stage 1, lr `2e-4`, 5 epochs (~35 steps); final loss ≈ **2.056**.
- Implementation: `notebooks/instruction_finetuning_annotated.ipynb` (also runs **base model evaluation** and **base-vs-SFT comparison**).
- Adapter artifact: `finance_sft_adapter` (zipped under `outputs/`).

## 7. DPO Alignment Approach (Stage 3)

- Continues from the Stage 2 SFT adapter (again via Hub push/pull between sessions).
- The 51 preference pairs are formatted as `(prompt, chosen, rejected)` using the same chat template, then trained with `trl.DPOTrainer` (`beta=0.1`).
- DPO directly optimizes the model to prefer the `chosen` response over the `rejected` response for the same prompt, without needing a separate reward model.
- A lower learning rate (`5e-6`) is used compared to SFT (`2e-4`), since DPO updates are more sensitive to instability.
- Typical run: 3 epochs (~21 steps); final DPO loss ≈ **0.299**.
- Implementation: `notebooks/dpo_alignment_annotated.ipynb`.
- Adapter artifact: `finance_dpo_adapter` (zipped under `outputs/run-2-08Jul26/`).

## 8. LoRA / QLoRA Configuration

| Stage | Rank | Alpha | Dropout | Learning Rate | Effective Batch Size |
|---|---|---|---|---|---|
| Non-instruction FT | 16 | 16 | 0.05 | 2e-4 | 16 (4 × 4 grad accum) |
| Instruction FT (SFT) | 16 | 16 | 0.05 | 2e-4 | 16 (4 × 4 grad accum) |
| DPO alignment | 16 | 16 | 0.05 | 5e-6 | 8 (2 × 4 grad accum) |

All stages use 4-bit base model loading (`load_in_4bit=True`) for QLoRA-style memory efficiency, with LoRA adapters applied to `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`. See `reports/fine_tuning_explanation.md` for the full reasoning behind these choices.

## 9. Training Runs & Artifacts

Saved LoRA adapters from Colab runs:

| Run folder | Contents |
|---|---|
| `outputs/run-1-09Jul26/` | `finance_stage1_adapter.zip`, `finance_sft_adapter.zip` |
| `outputs/run-2-08Jul26/` | `finance_stage1_adapter.zip`, `finance_sft_adapter.zip`, `finance_dpo_adapter.zip` (full 3-stage chain) |

**Measured losses (representative run):**

| Stage | Steps | Final loss |
|---|---|---|
| Stage 1 — Non-instruction FT | ~12 | ≈ 2.066 |
| Stage 2 — SFT | ~35 | ≈ 2.056 |
| Stage 3 — DPO | ~21 | ≈ 0.299 |

Pipeline diagram with Hub chaining and known issues: [`presentation/FinanceFAQ_Unsloth_Architecture_Mermaid.md`](presentation/FinanceFAQ_Unsloth_Architecture_Mermaid.md). Slide deck: [`presentation/FinanceFAQ_Unsloth_YouTube.pdf`](presentation/FinanceFAQ_Unsloth_YouTube.pdf). Video: [youtu.be/YHtjQjd981g](https://youtu.be/YHtjQjd981g).

## 10. Before vs. After Output Comparison

See:

- `reports/base_model_evaluation.md` — base model on 10 questions
- `reports/sft_model_comparison.md` — base vs. SFT model
- `reports/final_evaluation.md` — base vs. SFT vs. DPO, 3-way comparison

**Expected pattern:** the base model gives generic, hedge-heavy answers; the SFT model gives concise, domain-correct answers matching the training style; the DPO model is usually the most consistently helpful, safe, and professionally worded — with occasional regressions (e.g. SIP wording vs. SFT) that are called out in the architecture notes.

## 11. Final Observations

- Non-instruction fine-tuning alone does not teach Q&A behavior — it only improves domain fluency. Instruction fine-tuning is what makes the model usable as an assistant.
- DPO is most valuable for **edge cases and tone** — situations where the SFT model's answer is technically present but weak, incomplete, or unsafe in framing. DPO sharpens these specific failure modes using direct contrastive examples.
- Adapter handoff between Colab sessions is more reliable via **Hugging Face Hub push + `snapshot_download`** than manual zip re-upload (avoids missing-adapter `RuntimeError`s).
- A 0.5B model is a good fit for quickly demonstrating the *pipeline*, but is not a substitute for a larger model or for retrieval-augmented generation (RAG) if factual grounding against a live, large policy/document corpus is required in production.

## 12. Challenges Faced

- Keeping the non-instruction dataset purely *raw text* (no Q&A format) while still being information-dense enough to meaningfully shift the model's domain vocabulary.
- Designing rejected responses for DPO that are realistic failure modes (vague, unsafe, dismissive) rather than strawman answers, so the preference signal is meaningful.
- Balancing dataset size against Colab T4 time/memory limits across three sequential fine-tuning stages.
- Chaining LoRA adapters across fresh Colab runtimes without breaking the Stage 1 → 2 → 3 dependency.

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
│   ├── non_instruction_data.txt              # 57 raw domain paragraphs (Stage 1)
│   ├── instruction_dataset.jsonl             # 104 instruction/response pairs (Stage 2)
│   └── preference_dataset.jsonl              # 51 chosen/rejected pairs (Stage 3)
│
├── notebooks/
│   ├── non_instruction_finetuning_annotated.ipynb
│   ├── instruction_finetuning_annotated.ipynb    # base eval + SFT comparison
│   └── dpo_alignment_annotated.ipynb
│
├── outputs/
│   ├── run-1-09Jul26/                        # stage1 + sft adapters
│   └── run-2-08Jul26/                        # stage1 + sft + dpo adapters
│
├── presentation/
│   ├── FinanceFAQ_Unsloth_Architecture_Mermaid.md
│   └── FinanceFAQ_Unsloth_YouTube.pdf
│
├── reports/
│   ├── base_model_evaluation.md
│   ├── sft_model_comparison.md
│   ├── final_evaluation.md
│   └── fine_tuning_explanation.md
│
├── src/
│   └── inference.py                          # CLI Q&A on the DPO adapter
│
├── README.md
└── requirements.txt
```

## How to Run

1. Open each notebook in Google Colab with a **T4 GPU runtime** (Runtime → Change runtime type → T4 GPU).
2. Upload the relevant file(s) from `data/`, or clone this repo into the Colab environment.
3. Run notebooks in order:
   - `non_instruction_finetuning_annotated.ipynb`
   - `instruction_finetuning_annotated.ipynb`
   - `dpo_alignment_annotated.ipynb`  
   Each stage saves a LoRA adapter; push it to the Hugging Face Hub (or unzip the matching file from `outputs/`) so the next stage can load it.
4. After Stage 3, point `src/inference.py` at `finance_dpo_adapter` (unzipped from `outputs/run-2-08Jul26/` or downloaded from the Hub) and ask questions interactively.

```bash
pip install -r requirements.txt

# Unzip the final adapter first, e.g.:
# Expand-Archive outputs/run-2-08Jul26/finance_dpo_adapter.zip -DestinationPath .

python src/inference.py --adapter_path finance_dpo_adapter --question "How can I apply for a personal loan?"
```

Omit `--question` to enter an interactive loop.
