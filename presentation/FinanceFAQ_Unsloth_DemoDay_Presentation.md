---
marp: true
theme: default
paginate: true
---


# Finance FAQ Assistant
### Fine-Tuned with Unsloth — Non-Instruction FT → SFT → DPO

Qwen2.5-0.5B · a single free Google Colab T4, start to finish

---


## 🏆 The Final Result

### ✅ 3-Stage Pipeline — Fully Executed, Zero Errors, on a Free Colab T4

| Stage 1 Loss | Stage 2 Loss | Stage 3 Loss |
|:---:|:---:|:---:|
| **2.0659** | **2.0564** | **0.2995** |

**Q: "What is a SIP?"**

- **Base model:** *"I'm sorry, but I can't assist with that."*
- **Fine-tuned model:** *"A SIP, or Systematic Investment Plan, lets you invest a fixed amount at regular intervals..."* — correct, on-topic, direct.

---

## ⚙️ Engineering Under the Hood

| Stage | LoRA r/α | LR | Epochs | Steps |
|---|:---:|:---:|:---:|:---:|
| 1 · Non-Instruct | 16 / 16 | 2e-4 | 3 | 12 |
| 2 · SFT | 16 / 16 | 2e-4 | 5 | 35 |
| 3 · DPO | 16 / 16 | **5e-6 ↓** | 3 | 21 |

Only 8,798,208 of 502,830,976 params trainable (1.75%) — every stage, same LoRA config, all on a free T4.

### ⚠️ A real bug, not a hypothetical one

First DPO run: `RuntimeError` — `finance_sft_adapter` not found. Each notebook runs in a fresh Colab session; the adapter was never re-uploaded. **Fixed** by pushing every stage's adapter to the Hugging Face Hub and downloading it fresh at the top of the next notebook — no more manual zip re-uploads.


---

<!-- Slide 4 -->

## ▶️ Let's See It Live

Switching to the notebook — non-instruction FT → SFT → DPO, real outputs

