from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

base_model_name = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
adapter_path = "model/training/output"

validation_file = "data/processed/validation.json"

dataset = load_dataset(
    "json",
    data_files={"validation": validation_file}
)

tokenizer = AutoTokenizer.from_pretrained(adapter_path)

base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name
)

model = PeftModel.from_pretrained(
    base_model,
    adapter_path
)

model.eval()

correct = 0
total = len(dataset["validation"])

for example in dataset["validation"]:

    question = example["messages"][0]["content"]
    expected_sql = example["messages"][1]["content"]

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_sql = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True
    ).strip()

    expected_sql = expected_sql.strip()

    if generated_sql.lower() == expected_sql.lower():
        correct += 1

accuracy = (correct / total) * 100

print("\nEvaluation Results")
print("==================")
print(f"Total examples: {total}")
print(f"Correct: {correct}")
print(f"Incorrect: {total - correct}")
print(f"Exact Match Accuracy: {accuracy:.2f}%")