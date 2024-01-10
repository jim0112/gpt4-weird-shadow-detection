import base64
import requests
import os
import json
from dotenv import load_dotenv

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# OpenAI API Key
load_dotenv()
api_key = os.environ['API_KEY']
print(api_key)
initial_prompt = "I am going to showcase some images to you, and you should determine whether the lighting and shadow effects in those images are abnormal. Can you first tell me how would you define an abnormal lighting and shadow effect?"
initial_content = [{"type": "text", "text": initial_prompt}]
initial_reply = {'role': 'assistant', 'content': [{"type": "text", "text": 'An abnormal lighting and shadow effect would be one that does not follow the natural laws of physics and how light interacts with objects and surfaces. This could include shadows that are cast in the wrong direction, lighting that appears to be coming from multiple sources when there is only one light source, or shadows and highlights that are inconsistent with the shape and texture of the object being lit. It could also include lighting and shadows that are too harsh or too soft for the given environment or that do not match the overall mood and atmosphere of the image.'}]}

def weird_shadow_detector(image, fewshot=True):
    base_messages = [{"role": "user", "content": initial_content}, initial_reply]
    if fewshot:
        # show one positive image and one negative image
        pos_image, neg_image = encode_image("./few_shots/few_shot_pos.png"), encode_image("./few_shots/few_shot_neg.png")

        pos_content = {"role": "user", "content": [
                {
                    "type": "text",
                    "text": "This is an example image with abnormal lighting annd shadow effect."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{pos_image}"
                    }
                }
            ]
        }

        neg_content = {"role": "user", "content": [
                {
                    "type": "text",
                    "text": "This is an example image without abnormal lighting annd shadow effect."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{neg_image}"
                    }
                }
            ]
        }
        # combine all the prompts
        base_messages = [{"role": "user", "content": initial_content}, initial_reply, pos_content, neg_content]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    from collections import Counter
    tmp = Counter()

    round = 0

    while round < 3:
        # path to the tested image
        base64_image = encode_image(image)

        query = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": '''Based on your definition of abnormal lighting and shadow effect. Does this image have abnormal lighting and shadow effect? Please respond in JSON format like below, without markdown and newline:
            {"abnormal_lighting_and_shadow_effect": bool, "reason": string}
            '''
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": base_messages + [query],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response = response.json()
        try:
            content = json.loads(response['choices'][0]['message']['content'])
            tmp[content['abnormal_lighting_and_shadow_effect']] += 1
            round += 1
        except:
            print('illegal format, retry...')

    if tmp[True] > tmp[False]:
        return True
    return False