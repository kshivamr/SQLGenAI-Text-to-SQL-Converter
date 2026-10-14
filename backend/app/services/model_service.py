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

def generate_sql(question):
    schema = """
Database schema:

Table: employees
Columns:
- id
- name
- department
- salary
"""

    messages = [
        {
            "role": "user",
            "content": f"""
{schema}

Convert the following question into SQL.

Question:
{question}
"""
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
            max_new_tokens=128,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_sql = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True
    ).strip()

    return generated_sql