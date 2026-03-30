from dotenv import load_dotenv
from openai import OpenAI
from google import genai
import os
import json

load_dotenv()

# Clients
openai_client = OpenAI()
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# 🔹 OpenAI Response
def get_openai_response(query):
    response = openai_client.chat.completions.create(
        model="gpt-4.1", messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content.strip()


# 🔹 Gemini Response
def get_gemini_response(query):
    response = gemini_client.models.generate_content(model="gemini-2.5-flash-lite", contents=query)
    return response.text


# 🔥 Judge Model
def judge_responses(query, openai_res, gemini_res):
    judge_prompt = f"""
    You are an AI judge.

    Compare the two responses for the given query and decide:
    1. Which answer is more correct
    2. Which has better reasoning
    3. Final best answer

    Return ONLY JSON:
    {{
        "winner": "openai" or "gemini",
        "reason": "short explanation",
        "final_answer": "best combined answer"
    }}

    Query: {query}

    OpenAI Response:
    {openai_res}

    Gemini Response:
    {gemini_res}
    """

    response = openai_client.chat.completions.create(
        model="gpt-4.1",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": judge_prompt}],
    )

    return json.loads(response.choices[0].message.content)


# 🔥 MAIN FLOW
query = input("👉 Enter your query: ")

openai_output = get_openai_response(query)
gemini_output = get_gemini_response(query)

print("\n🧠 OpenAI:\n", openai_output)
print("\n🧪 Gemini:\n", gemini_output)

judgement = judge_responses(query, openai_output, gemini_output)

print("\n⚖️ Judge Decision:")
print("Winner:", judgement["winner"])
print("Reason:", judgement["reason"])
print("Final Answer:", judgement["final_answer"])

## output example

""" 
👉 Enter your query: find the squeare root of 134232 upto 5 decimal

🧠 OpenAI:
 Let's calculate the square root of **134232** up to **5 decimal places**.

sqrt{134232} \approx 366.39748


**Answer:**  
sqrt{134232} = \boxed{366.39748}

🧪 Gemini:
 Here's how to find the square root of 134232 up to 5 decimal places:

**1. Estimation:**

* We know that $300^2 = 90000$ and $400^2 = 160000$. So the square root of 134232 will be between 300 and 400.
* Let's try a value in the middle, say 350. $350^2 = 122500$. This is a bit too low.
* Let's try 360. $360^2 = 129600$. This is closer.
* Let's try 370. $370^2 = 136900$. This is a bit too high.

So, the square root is between 360 and 370.

**2. Using a Calculator (Most Practical Method):**

The most efficient and accurate way to find the square root to a specific decimal place is to use a calculator.

Enter `sqrt(134232)` into your calculator.

**3. Manual Calculation (Long Division Method - More involved but demonstrates the process):**

While a calculator is the easiest way, here's the outline of the long division method for finding square roots, which you could use manually if needed. This method is quite tedious for many decimal places.

* **Step 1: Group digits:** Group the digits of 134232 in pairs from right to left: `13 42 32`. If there's an odd number of digits, the leftmost group will have only one digit.

* **Step 2: Find the largest square:** Find the largest integer whose square is less than or equal to the first group (13). This is 3 ($3^2 = 9$). Write 3 as the first digit of the square root. Subtract 9 from 13, leaving 4.

    ```
       3
      ---
    √13 42 32
     -9
     ---
      4
    ```

* **Step 3: Bring down the next group:** Bring down the next pair of digits (42) to form 442.

    ```
       3
      ---
    √13 42 32
     -9
     ---
      4 42
    ```

* **Step 4: Double the current root and find the next digit:** Double the current root (3 * 2 = 6). Now, find a digit (let's call it 'x') such that when you append it to 6 (making it 6x) and multiply by x, the result is less than or equal to 442.
    * Try x=6: 66 * 6 = 396.
    * Try x=7: 67 * 7 = 469 (too large).
    So, the next digit is 6. Write 6 next to the 3 in the root. Subtract 396 from 442, leaving 46.

    ```
       36
      ----
    √13 42 32
     -9
     ---
      4 42
     -3 96
     ----
       46
    ```

* **Step 5: Repeat the process:** Bring down the next pair of digits (32) to form 4632. Double the current root (36 * 2 = 72). Find a digit 'x' such that 72x * x is less than or equal to 4632.
    * Try x=6: 726 * 6 = 4356.
    * Try x=7: 727 * 7 = 5089 (too large).
    So, the next digit is 6. Write 6 next to the 36 in the root. Subtract 4356 from 4632, leaving 276.

    ```
       366
      -----
    √13 42 32
     -9
     ---
      4 42
     -3 96
     ----
       46 32
      -43 56
      ------
        276
    ```

* **Step 6: Add decimals and zeros:** To get decimal places, add a decimal point to the root and bring down pairs of zeros.
    * Bring down `00` to make it 27600. Double the current root (366 * 2 = 732). Find 'x' such that 732x * x is less than or equal to 27600.
        * Try x=3: 7323 * 3 = 21969.
        * Try x=4: 7324 * 4 = 29296 (too large).
    So, the next digit is 3. Write 3 after the decimal point. Subtract 21969 from 27600, leaving 5631.

    ```
       366.3
      ------
    √13 42 32.00
     -9
     ---
      4 42
     -3 96
     ----
       46 32
      -43 56
      ------
        276 00
       -219 69
       -------
         5631
    ```

* **Step 7: Continue for more decimal places:**
    * Bring down `00` to make it 563100. Double the current root (3663 * 2 = 7326). Find 'x' such that 7326x * x is less than or equal to 563100.
        * Try x=7: 73267 * 7 = 512869.
        * Try x=8: 73268 * 8 = 586144 (too large).
    So, the next digit is 7. Write 7 after the 3. Subtract 512869 from 563100, leaving 50231.

    ```
       366.37
      -------
    √13 42 32.00 00
     -9
     ---
      4 42
     -3 96
     ----
       46 32
      -43 56
      ------
        276 00
       -219 69
       -------
         5631 00
        -5128 69
        --------
          50231
    ```

* **Step 8: One more decimal place:**
    * Bring down `00` to make it 5023100. Double the current root (36637 * 2 = 73274). Find 'x' such that 73274x * x is less than or equal to 5023100.
        * Try x=6: 732746 * 6 = 4396476.
        * Try x=7: 732747 * 7 = 5129229 (too large).
    So, the next digit is 6. Write 6 after the 7. Subtract 4396476 from 5023100, leaving 626624.

    ```
       366.376
      --------
    √13 42 32.00 00 00
     -9
     ---
      4 42
     -3 96
     ----
       46 32
      -43 56
      ------
        276 00
       -219 69
       -------
         5631 00
        -5128 69
        --------
          50231 00
         -43964 76
         ---------
           626624
    ```

* **Step 9: The fifth decimal place:**
    * Bring down `00` to make it 62662400. Double the current root (366376 * 2 = 732752). Find 'x' such that 732752x * x is less than or equal to 62662400.
        * Try x=8: 7327528 * 8 = 58620224.
        * Try x=9: 7327529 * 9 = 65947761 (too large).
    So, the next digit is 8. Write 8 after the 6.

    ```
       366.3768
      ---------
    √13 42 32.00 00 00
     ... (previous steps) ...
           50231 00
          -43964 76
          ---------
            626624 00
           -586202 24
           ----------
             4042176
    ```

**Rounding to 5 Decimal Places:**

The number we have is 366.3768... To round to 5 decimal places, we look at the sixth decimal place. Since it's 8 (which is 5 or greater), we round up the fifth decimal place.

Therefore, the square root of 134232 up to 5 decimal places is **366.37688**.

**Final Answer using Calculator:**

The most straightforward way is to use a calculator:

√134232 ≈ **366.37688**

⚖️ Judge Decision:
Winner: gemini
Reason: Gemini not only provides the correct value for the square root of 134232 up to 5 decimal places (366.37688), but also demonstrates the reasoning process both with estimation and a manual long division method, which is educational. OpenAI's answer gives an incorrect value (366.39748), which is both less accurate and lacks explanation or calculation steps.
Final Answer: The square root of 134232 up to 5 decimal places is 366.37688.
(venv) mohitaggarwal@192 CompareLLM % 
"""
