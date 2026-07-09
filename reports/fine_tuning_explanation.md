# Fine-Tuning Explanation — LoRA, QLoRA, Non-Instruction FT, SFT, and DPO

## 1. Why is full fine-tuning expensive?

Full fine-tuning means updating **every single weight** in the model during training. Even a "small" model like Qwen2.5-0.5B has 500 million parameters, and most useful open-source models are far larger. Updating all of them requires:

- Storing **gradients** and **optimizer states** (e.g., Adam keeps two extra moving averages per parameter) for every parameter, which can be 3-4x the model's own memory footprint.
- Enough GPU memory to hold the full model, its gradients, and optimizer states simultaneously — often requiring multiple high-end GPUs (A100s/H100s) for anything beyond a few billion parameters.
- Significant compute time, since every forward and backward pass touches the entire network.

For a single person on a free Colab T4 GPU (about 16GB VRAM), full fine-tuning of even a 1-3B model is usually infeasible. This is why parameter-efficient fine-tuning methods like LoRA exist.

## 2. What does LoRA do?

LoRA (Low-Rank Adaptation) freezes the original model weights and instead injects small, trainable **low-rank matrices** into specific layers (typically the attention projection layers: `q_proj`, `k_proj`, `v_proj`, `o_proj`, and the MLP layers `gate_proj`, `up_proj`, `down_proj`).

Instead of learning a full weight update matrix `ΔW` (which would be huge), LoRA approximates it as the product of two much smaller matrices: `ΔW ≈ A × B`, where `A` and `B` have a small inner dimension called the **rank (r)**. Only `A` and `B` are trained — the original weights stay frozen.

This means:
- Far fewer trainable parameters (often <1% of the full model).
- Much lower memory usage for gradients and optimizer states.
- The adapter (just `A` and `B` matrices) can be saved separately and is typically only a few megabytes, instead of saving a full multi-gigabyte model copy.

## 3. What does QLoRA do?

QLoRA combines LoRA with **4-bit quantization** of the frozen base model. Instead of loading the base model's weights in 16-bit or 32-bit precision, QLoRA loads them in 4-bit precision (using a technique like NF4), which drastically reduces the memory needed just to hold the base model in GPU memory.

The LoRA adapters themselves are still trained in higher precision (typically bfloat16/float16), so we get the best of both: a tiny memory footprint for the frozen base model, and full-precision-quality updates for the small number of trainable LoRA parameters.

## 4. Why is QLoRA useful on a limited GPU (like a free Colab T4)?

A T4 GPU has about 16GB of VRAM. Loading a model at full 16-bit precision uses roughly 2 bytes per parameter, plus extra memory for activations, gradients, and optimizer states during training. For models in the 1B-7B range, this can easily exceed 16GB without quantization.

QLoRA's 4-bit loading cuts the base model's memory footprint to roughly a quarter of what 16-bit loading would need, and since the base weights are frozen (no gradients or optimizer states needed for them), the remaining memory is mostly used by the small LoRA adapter and the activations for the current batch. This is what makes it possible to fine-tune models like Qwen2.5-0.5B (and even larger 1-3B models) comfortably on a free T4 instance.

## 5. What is non-instruction fine-tuning?

Non-instruction fine-tuning (also called continued pre-training or domain-adaptive pre-training) trains the model on **raw, unstructured domain text** using the same objective the model was originally pre-trained on: predicting the next token in a sequence. There is no question/answer format — just plain paragraphs of domain text (in this project, 57 paragraphs about savings accounts, loans, credit cards, mutual funds, insurance, and taxes).

The goal is **not** to teach the model how to answer questions yet. It's to expose the model to domain-specific vocabulary, phrasing, and background facts so that later instruction tuning has a better starting point — the model already "speaks the language" of finance before it learns the Q&A behavior.

## 6. What is instruction fine-tuning?

Instruction fine-tuning (often called Supervised Fine-Tuning, or SFT) trains the model on **paired instruction-response examples** — in this project, 104 `{instruction, response}` pairs covering finance FAQs. Unlike non-instruction fine-tuning, this stage explicitly teaches the model the *behavior* of answering a user's question directly and helpfully, in a consistent style.

This is the stage that converts a model from "knows about the domain" (Stage 1) to "can act as a helpful Q&A assistant for the domain" (Stage 2).

## 7. What is DPO?

DPO (Direct Preference Optimization) is an alignment technique that trains the model using **pairs of responses to the same prompt** — one marked as `chosen` (preferred) and one marked as `rejected` (less preferred) — without needing a separate reward model, unlike classic RLHF with PPO.

DPO works by adjusting the model so that it assigns a higher probability to generating the `chosen` response and a lower probability to generating the `rejected` response, relative to a reference model (often the SFT model itself, before DPO). In this project, 51 preference pairs contrast correct, helpful, professional finance answers (chosen) against vague, unsafe, or dismissive answers (rejected).

## 8. Difference between SFT and DPO

| | SFT (Instruction Fine-Tuning) | DPO (Preference Alignment) |
|---|---|---|
| **Data format** | Single `(instruction, response)` examples | Paired `(prompt, chosen, rejected)` examples |
| **What it teaches** | *How* to respond / the right format and behavior | *Which* of two responses is better |
| **Objective** | Maximize likelihood of the target response | Maximize the gap between chosen and rejected response likelihoods |
| **When used** | After base/non-instruction model, to teach Q&A behavior | After SFT, to refine response quality, safety, and helpfulness |
| **Typical effect** | Model learns to answer in the right format at all | Model learns to prefer better answers among plausible ones |

In short: **SFT teaches the model what a good answer looks like; DPO teaches the model to prefer good answers over bad ones when multiple answers are plausible.**

## 9. Hyperparameters Used in This Project

| Stage | Rank (r) | Alpha | Dropout | Learning Rate | Batch Size (effective) |
|---|---|---|---|---|---|
| Stage 1 — Non-instruction FT | 16 | 16 | 0.05 | 2e-4 | 4 (per device) × 4 (grad accum) = 16 |
| Stage 2 — Instruction FT (SFT) | 16 | 16 | 0.05 | 2e-4 | 4 (per device) × 4 (grad accum) = 16 |
| Stage 3 — DPO alignment | 16 | 16 | 0.05 | 5e-6 | 2 (per device) × 4 (grad accum) = 8 |

**Notes on these choices:**
- **Rank 16 / Alpha 16** is a common, balanced starting point for small models — enough capacity to learn domain adaptation without overfitting on a small dataset (57 paragraphs / 104 examples / 51 pairs).
- **Dropout 0.05** adds light regularization, important given the small dataset sizes used here.
- **Learning rate 2e-4** is a typical LoRA/QLoRA learning rate for SFT-style training on small models.
- **DPO uses a much lower learning rate (5e-6)** than SFT, because DPO updates are more sensitive — large updates can destabilize the model or cause it to diverge from sensible, fluent outputs while chasing the preference signal.
- **Batch sizes are kept small** (with gradient accumulation to simulate a larger effective batch) to fit within the ~16GB VRAM of a free Colab T4 GPU.
