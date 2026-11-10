import json
import ollama
import time

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
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
        raw_answer = response['message']['content'].strip()
        clean_answer = raw_answer.replace("```json", "").replace("```", "").strip()
        if "Final Answer:" in clean_answer:
            clean_answer = clean_answer.split("Final Answer:")[-1].strip()
        return clean_answer
    except Exception as e:
        print(f"Error: {e}")
        return "ERROR"

# لیست ۱۰ مسئله استاد
problems = [
    {"id": "test_001", "problem": "نیما، سارا و رضا در مجموع 72 ژتون دارند. تعداد ژتون‌های نیما دو برابر رضا است و سارا 12 ژتون بیشتر از رضا دارد. هرکدام چند ژتون دارند؟ پاسخ را دقیقاً با فرمت زیر برگردانید: <Nima=<integer>, Sara=<integer>, Reza=<integer>>"},
    {"id": "test_002", "problem": "پنج کار A, B, C, D, E باید دقیقاً یک بار در جایگاه های 1 تا 5 اجرا شوند. قیود: B باید قبل از D باشد. A باید بالفاصله بعد از C باشد. E نمی تواند اولین یا آخرین کار باشد. D باید آخرین کار باشد. اگر فقط یک ترتیب معتبر وجود داشته باشد، کدام کار در جایگاه اول قرار می گیرد؟ فقط حرف آن کار را برگردانید."},
    {"id": "test_003", "problem": "دقیقاً یکی از سه گزاره زیر درست است: A: کلید در جعبه 2 است. B: کلید در جعبه 2 نیست. C: کلید در جعبه 1 است. کلید دقیقاً در یکی از جعبه‌های 1، 2 یا 3 قرار دارد. کلید در کدام جعبه است؟ فقط یکی از اعداد 1 یا 2 یا 3 را برگردانید."},
    {"id": "test_004", "problem": "یک پروژه چهار فعالیت دارد: طراحی 3 روز زمان می‌برد. پیاده‌سازی 5 روز زمان می‌برد و فقط بعد از پایان طراحی می‌تواند شروع شود. بررسی حقوقی 4 روز زمان می‌برد و همزمان با طراحی می‌تواند آغاز شود. استقرار 2 روز زمان می‌برد و فقط بعد از پایان هر دو فعالیت پیاده‌سازی و بررسی حقوقی می‌تواند شروع شود. روز 0 را زمان شروع پروژه فرض کنید. زودترین زمان پایان پروژه چند روز پس از شروع است؟ فقط عدد صحیح را برگردانید."},
    {"id": "test_005", "problem": "در یک کلاس 40 دانشجو وجود دارد: 24 نفر Python می‌خوانند، 18 نفر Java می‌خوانند و 10 نفر هر دو را می‌خوانند. چند دانشجو هیچ کدام از Python و Java را نمی‌خوانند؟ فقط عدد صحیح را برگردانید."},
    {"id": "test_006", "problem": "یک فروشگاه ابتدا قیمت کالایی را 25% افزایش می‌دهد. سپس در یک کمپین، روی قیمت افزایش‌یافته 20% تخفیف می‌دهد. مشتری پس از این دو تغییر 600 واحد پرداخت می‌کند. قیمت اولیه کالا قبل از افزایش چقدر بوده است؟ فقط عدد صحیح را برگردانید."},
    {"id": "test_007", "problem": "چهار پژوهشگر آرمان، بهار، کوروش و دریا هرکدام در یکی از روزهای دوشنبه تا پنج‌شنبه ارائه دارند و هیچ دو نفری در یک روز ارائه ندارند. قیود: آرمان زودتر از کوروش ارائه می‌دهد. بهار پنج‌شنبه ارائه می‌دهد. دریا دوشنبه ارائه نمی‌دهد. کوروش دقیقاً یک روز بعد از دریا ارائه می‌دهد. آرمان در چه روزی ارائه می‌دهد؟ فقط یکی از این چهار عبارت را برگردانید: Monday, Tuesday, Wednesday, Thursday"},
    {"id": "test_008", "problem": "در یک جزیره هر فرد یا همیشه راست می‌گوید یا همیشه دروغ می‌گوید. علی می‌گوید: بیتا دروغگو است. بیتا می‌گوید: من و علی از دو نوع متفاوت هستیم. وضعیت علی و بیتا چیست؟ دقیقاً یکی از گزینه‌های زیر را برگردانید: Ali=Truth, Bita=Truth یا Ali=Truth, Bita=Lie یا Ali=Lie, Bita=Truth یا Ali=Lie, Bita=Lie"},
    {"id": "test_009", "problem": "یک ربات از مختصات (0,0) روی یک شبکه شروع می‌کند و باید به (4,3) برسد. در هر حرکت دقیقاً یک خانه به بالا، پایین، چپ یا راست می‌رود. خانه‌های (1,0)، (1,1) و (1,2) مسدود هستند. ربات نمی‌تواند از محدوده X<=4 و Y<=3 خارج شود. حداقل چند حرکت برای رسیدن به مقصد لازم است؟ فقط عدد صحیح را برگردانید."},
    {"id": "test_010", "problem": "یک کد سه رقمی از سه رقم متمایز از مجموعه {1,2,3,4,5} ساخته شده است. قیود: رقم اول از رقم دوم بزرگ‌تر است. رقم سوم برابر تفاضل رقم اول و دوم است. مجموع سه رقم برابر 8 است. رقم 5 استفاده نشده است. کد چیست؟ فقط کد سه رقمی را برگردانید."}
]

print(f"Starting test for {len(problems)} problems...")

for i, p in enumerate(problems, 1):
    print(f"\n--- Solving Problem {i} (ID: {p['id']}) ---")
    ans = solve_problem(p['problem'])
    
    output_data = {
        "id": p['id'],
        "answer": ans
    }
    
    filename = f"output_{i}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print(f"Saved to {filename} -> Answer: {ans}")
    time.sleep(2) # کمی صبر می‌کنیم تا سیستم نفس بکشه

print("\nAll tests completed successfully!")