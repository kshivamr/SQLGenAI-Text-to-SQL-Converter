from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

base_model_name = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
adapter_path = "model/training/output"

tokenizer = AutoTokenizer.from_pretrained(adapter_path)

base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name
)

model = PeftModel.from_pretrained(
    base_model,
    adapter_path
)

model.eval()

print("Fine-tuned model loaded successfully!")

questions = [
    "Show the top 5 employees with the highest salary.",
    "Find all employees who work in the IT department.",
    "What is the average salary of all employees?",
    "Show the employee with the lowest salary."
]

for question in questions:

    messages = [
        {
            "role": "user",
            "content": f"Convert the following question into SQL:\n\n{question}"
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
            max_new_tokens=100,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    response = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True
    )

    print("\n" + "=" * 60)
    print(f"Question: {question}")
    print("Generated SQL:")
    print(response)

print("\nAll questions completed!")