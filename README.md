### How to use the weird shadow detector function
0. install the necessary packages:
    ```=bash
    pip install -r requirements.txt
    ```
1. Create a .env file for openai api key
   * the format should be API_KEY="your_api_key"
2. Prepare your target image
3. do the following (like test.py):
    ```=python
    from weird_shadow_detector import weird_shadow_detector

    image = "path_to_the_target_image"
    response = weird_shadow_detector(image, fewshot=False)
    ```
4. the **response** would be a boolean (True: the image has weird shadow issue.)