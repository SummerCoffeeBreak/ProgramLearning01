# import os
# from langchain.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_community.utilities import WikipediaAPIWrapper
#
# # if 'OPENAI_API_KEY' in os.environ:
# #     print("API key is set.")
# # else:
# #     print("API key is not set.")
#
# def generate_script(subject, video_length,
#                     creativity, api_key):
#     title_template = ChatPromptTemplate.from_messages(
#         [
#             ("human", "请为'{subject}'这个主题的视频像一个吸引人的标题")
#         ]
#     )
#     script_template = ChatPromptTemplate.from_messages(
#         [
#             ("human",
#              """你是短视频频道的博主。根据以下标题和相关信息，为短视频频道撰写一段视频脚本。
#             视频标题：{title}，视频时长：{duration} 分钟，生成的脚本长度尽量遵循视频时长的要求。
#             要求开头抓眼球，中间提供干货内容，结尾有惊喜，脚本格式也按照【开头、中间、结尾】分隔。
#             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
#             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
#             '''{wikipedia_search}'''""")
#         ]
#     )
#     model = ChatOpenAI(openai_api_key=api_key, temperature=creativity)
#     title_chain = title_template | model
#     script_chain = script_template | model
#
#     title = title_chain.invoke({"subject": subject}).content
#
#     search = WikipediaAPIWrapper(lang="zh")
#     search_result = search.run(subject)
#
#     script = script_chain.invoke({"title": title, "duration": video_length, "wikipedia_search":search_result}).content
#
#     return search_result, title, script

#print(generate_script("sora模型",1, 0.7, os.getenv("OPENAI_API_KEY")))

import os
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

def generate_script(subject, video_length, creativity, api_key):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频像一个吸引人的标题")
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是短视频频道的博主。根据以下标题和相关信息，为短视频频道撰写一段视频脚本。
             视频标题：{title}，视频时长：{duration} 分钟，生成的脚本长度尽量遵循视频时长的要求。
             要求开头抓眼球，中间提供干货内容，结尾有惊喜，脚本格式也按照【开头、中间、结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             '''{wikipedia_search}'''""")
        ]
    )

    model = ChatOpenAI(openai_api_key=api_key, temperature=creativity)
    title_chain = title_template | model
    script_chain = script_template | model

    try:
        # 生成视频标题
        title = title_chain.invoke({"subject": subject}).content
        print(f"Generated Title: {title}")

        # 从维基百科获取信息
        search = WikipediaAPIWrapper(lang="zh")
        search_result = search.run(subject)
        print(f"Wikipedia Search Result: {search_result}")

        # 生成视频脚本
        script = script_chain.invoke({"title": title, "duration": video_length, "wikipedia_search": search_result}).content
        print(f"Generated Script: {script}")

        return search_result, title, script
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None

# # 获取环境变量中的 API 密钥
# api_key = os.getenv("OPENAI_API_KEY")
#
# if api_key:
#     print(generate_script("sora模型", 1, 0.7, api_key))
# else:
#     print("Please set the OPENAI_API_KEY environment variable.")