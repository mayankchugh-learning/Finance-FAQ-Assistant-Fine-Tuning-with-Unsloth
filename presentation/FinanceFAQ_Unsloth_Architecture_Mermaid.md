# Fine-Tuning a Finance FAQ Assistant — Architecture (Mermaid)
### by Mayank Chugh · Finance FAQ Assistant Fine-Tuning with Unsloth

Full pipeline: base model → Stage 1 (non-instruction FT) → Stage 2 (SFT) → Stage 3 (DPO) → final assistant.
Adapters are chained between stages via the Hugging Face Hub, not manual re-upload — that distinction is called
out directly in the diagram because it's the fix for a real `RuntimeError` hit during this project.

```mermaid
flowchart TD
    Base(("Base Model<br/>Qwen2.5-0.5B<br/>500M params"))

    Base --> S1Data["57 raw finance paragraphs<br/><i>non_instruction_data.txt</i>"]

    subgraph S1["STAGE 1 · Non-Instruction Fine-Tuning"]
        S1Data --> S1Train["LoRA r=16 · α=16 · dropout=0.05<br/>SFTTrainer, plain causal-LM objective<br/>lr 2e-4 · 3 epochs · 12 steps"]
        S1Train --> S1Loss["loss = 2.0658821066220603"]
    end

    S1Loss --> S1Adapter[["finance_stage1_adapter<br/>pushed to HF Hub"]]
    S1Adapter -. snapshot_download .-> S2Data

    S2Data["104 instruction-response pairs<br/><i>instruction_dataset.jsonl</i>"]

    subgraph S2["STAGE 2 · Instruction Fine-Tuning (SFT)"]
        S2Data --> S2Train["Continue LoRA from Stage 1<br/>Qwen2.5 chat template<br/>lr 2e-4 · 5 epochs · 35 steps"]
        S2Train --> S2Loss["loss = 2.056434644971575"]
    end

    S2Loss --> S2Adapter[["finance_sft_adapter<br/>pushed to HF Hub"]]
    S2Adapter -. snapshot_download .-> S3Data

    S3Data["51 chosen/rejected pairs<br/><i>preference_dataset.jsonl</i>"]

    subgraph S3["STAGE 3 · DPO Preference Alignment"]
        S3Data --> S3Train["DPOTrainer · beta=0.1<br/>lr 5e-6 (lower than SFT)<br/>3 epochs · 21 steps"]
        S3Train --> S3Loss["loss = 0.2994556086403983 *"]
    end

    S3Loss --> S3Adapter[["finance_dpo_adapter<br/>pushed to HF Hub"]]
    S3Adapter --> Final(("Final Assistant<br/>generate_answer()"))

    Eval{{"Same 10 eval questions<br/>asked after every stage"}}
    Eval -.-> S1Loss
    Eval -.-> S2Loss
    Eval -.-> S3Loss

    Bug1["⚠ First DPO attempt:<br/>RuntimeError — adapter not found<br/>Fixed by HF Hub push/pull"]
    Bug1 -.-> S3Data

    Bug2["⚠ Honest finding:<br/>DPO regressed on 'What is a SIP?'<br/>vs SFT's correct answer"]
    S3Loss -.-> Bug2

    classDef base fill:#0B1F2A,stroke:#D4AF37,stroke-width:2px,color:#EAF2F5
    classDef stage fill:#163244,stroke:#D4AF37,stroke-width:1px,color:#EAF2F5
    classDef hub fill:#D4AF37,stroke:#0B1F2A,stroke-width:1px,color:#0B1F2A
    classDef final fill:#1FAA59,stroke:#0B1F2A,stroke-width:2px,color:#FFFFFF
    classDef warn fill:#E2543A,stroke:#0B1F2A,stroke-width:1px,color:#FFFFFF
    classDef eval fill:#112D3E,stroke:#9FB8C4,stroke-width:1px,color:#EAF2F5

    class Base base
    class S1Data,S1Train,S1Loss,S2Data,S2Train,S2Loss,S3Data,S3Train,S3Loss stage
    class S1Adapter,S2Adapter,S3Adapter hub
    class Final final
    class Bug1,Bug2 warn
    class Eval eval
```

## Reading the Diagram

- **Gold boxes** are the LoRA adapters — each one is saved locally, then pushed to the Hugging Face Hub so the *next* notebook (a fresh Colab session) can pull it back down reliably.
- **Dashed arrows into the loss nodes** show the same 10 evaluation questions being re-asked after every single stage, which is what keeps the three stages directly comparable.
- **Red boxes** are the two honest findings from this run: the `RuntimeError` that broke the first DPO attempt (fixed via Hub chaining, not manual re-upload), and the DPO regression on the SIP question relative to SFT.
- **Green node** is the final deliverable — the assignment's required `generate_answer()` function, running on the DPO-aligned adapter.

*Made with ❤️ by Mayank Chugh*
