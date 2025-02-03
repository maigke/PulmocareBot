# 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

from openai import OpenAI
import os

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="mi_Token",
)


input_text = input("Ingresa tu texto: ")

completion = client.chat.completions.create(
  #extra_headers={
  #  "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
  #  "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  #},
  model="deepseek/deepseek-r1:free",
  messages=[
    {
      "role": "user",
      "content": input_text
    }
  ]
)
#print(completion.choices[0].message.content)
print(completion.choices[0].message.content)