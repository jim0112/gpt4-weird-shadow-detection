from weird_shadow_detector import weird_shadow_detector

image = "2_cn_True_p_3_o_2.png"
response = weird_shadow_detector(image, fewshot=True)
print(response)
