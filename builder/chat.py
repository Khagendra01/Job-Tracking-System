import os
import time

os.environ["REPLICATE_API_TOKEN"] = ""

import replicate

# Prompts
pre_prompt = "Is this text about some one just applied internship or is it company response to the application. Return one word, \"applied\" if the first condition is met or return \"rejected\" or \"accepted\"."
prompt_input = "Hi Khagendra, Thank you for your interest in Dune and taking the time to speak with our team about the Staff Software Engineer, Application position. After discussing with the team, we wanted to let you know that we have decided to move forward with other candidates who we feel are more suited to this particular role at our current stage. Thank you again and all the best for the future. -- Dune Team"
start_time = time.time()
# Generate LLM response
output = replicate.run('meta/meta-llama-3-8b-instruct', # LLM model
                        input={"prompt": f"{pre_prompt} {prompt_input} Assistant: ", # Prompts
                        "temperature":0.1, "top_p":0.9, "max_length":10, "repetition_penalty":1})  # Model parameters

full_response = ""

for item in output:
  full_response += item

print(full_response)
end_time = time.time()
print("\nTime taken to complete the response:", end_time - start_time, "seconds")
