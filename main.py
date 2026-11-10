import argparse
import json
import ollama
import sys

# نام مدلی که ساختیم
MODEL_NAME = "qwen-local" 

def solve_problem(problem_text):
    prompt = f"""
    You are an expert AI reasoning agent. 
    Analyze the following problem and solve it carefully step by step.
    
    Problem:
    {problem_text}
    
    Instructions:
    1. Think step by step to find the correct answer.
    2. Your final output MUST contain ONLY the final answer exactly in the format requested by the problem.
    3. Do NOT include any markdown formatting (like ```), do NOT include explanations, and do NOT include extra words.
    
    Final Answer:
    """
    
    print("Waiting for the local model to respond (this might take a few seconds)...")
    
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[
            {"role": "user", "content": prompt}
        ])
        
        raw_answer = response['message']['content'].strip()
        
        # تمیز کردن خروجی
        clean_answer = raw_answer.replace("```json", "").replace("```", "").strip()
        
        if "Final Answer:" in clean_answer:
            clean_answer = clean_answer.split("Final Answer:")[-1].strip()
            
        return clean_answer
    except Exception as e:
        print(f"Error calling Ollama: {e}", file=sys.stderr)
        return "ERROR"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    problem_id = data.get("id", "unknown")
    problem_text = data.get("problem", "")

    print(f"Processing ID: {problem_id}")
    
    final_answer = solve_problem(problem_text)

    output_data = {
        "id": problem_id,
        "answer": final_answer
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved to {args.output}")

if __name__ == "__main__":
    main()