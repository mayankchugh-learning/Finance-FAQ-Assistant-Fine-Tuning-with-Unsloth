"""
Simple inference script for the Finance FAQ Assistant.

Loads the final DPO-aligned model (LoRA adapter on top of Qwen2.5-0.5B,
trained via Unsloth across Stage 1 -> Stage 2 -> Stage 3) and lets a
user ask a finance-related question from the command line.

Usage:
    python src/inference.py
    python src/inference.py --question "How can I apply for reimbursement?"
    python src/inference.py --adapter_path path/to/finance_dpo_adapter
"""

import argparse

from unsloth import FastLanguageModel


DEFAULT_ADAPTER_PATH = "finance_dpo_adapter"  # output of notebooks/dpo_alignment.ipynb
MAX_SEQ_LENGTH = 512


def load_model(adapter_path: str = DEFAULT_ADAPTER_PATH):
    """Load the fine-tuned, DPO-aligned model and tokenizer."""
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=adapter_path,
        max_seq_length=MAX_SEQ_LENGTH,
        dtype=None,
        load_in_4bit=True,
    )
    FastLanguageModel.for_inference(model)
    return model, tokenizer


def generate_answer(question: str, model, tokenizer, max_new_tokens: int = 150) -> str:
    """Generate an answer to a single finance question."""
    messages = [{"role": "user", "content": question}]
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    ).to("cuda")

    outputs = model.generate(
        input_ids=inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        temperature=0.1,
    )

    response_tokens = outputs[0][inputs.shape[1]:]
    answer = tokenizer.decode(response_tokens, skip_special_tokens=True)
    return answer.strip()


def main():
    parser = argparse.ArgumentParser(description="Finance FAQ Assistant — inference script")
    parser.add_argument(
        "--adapter_path",
        type=str,
        default=DEFAULT_ADAPTER_PATH,
        help="Path or Hugging Face Hub repo of the fine-tuned (DPO-aligned) adapter",
    )
    parser.add_argument(
        "--question",
        type=str,
        default=None,
        help="A single question to ask. If omitted, starts an interactive loop.",
    )
    args = parser.parse_args()

    print(f"Loading model from: {args.adapter_path} ...")
    model, tokenizer = load_model(args.adapter_path)
    print("Model loaded. Ready to answer finance questions.\n")

    if args.question:
        question = args.question
        answer = generate_answer(question, model, tokenizer)
        print(f"Q: {question}")
        print(f"A: {answer}")
        return

    print("Type a finance question (or 'exit' to quit):\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not question:
            continue
        answer = generate_answer(question, model, tokenizer)
        print(f"Assistant: {answer}\n")


if __name__ == "__main__":
    # Example (matches the assignment's example usage):
    #
    #   question = "How can I apply for reimbursement?"
    #   answer = generate_answer(question, model, tokenizer)
    #   print(answer)
    #
    main()
