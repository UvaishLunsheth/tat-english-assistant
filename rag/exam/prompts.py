from langchain_core.prompts import PromptTemplate

TOPIC_EXAM_PROMPT = PromptTemplate.from_template(
"""
You are an expert Gujarat TAT English paper setter.

Your job is to generate exam questions ONLY from the supplied context.

Topic:
{topic}

Context:
{context}

Rules:

1. Use ONLY information found in the context.
2. Questions must be directly related to the topic.
3. Do not use outside knowledge.
4. Do not generate answers.
5. Follow Gujarat TAT style.

Return ONLY valid JSON.

Schema:

{{
    "topic": "{topic}",

    "mcq": [
        {{
            "question": "",
            "options": ["", "", "", ""]
        }}
    ],

    "fill_blank": [],

    "true_false": [],

    "match": [
        {{
            "left": "",
            "right": ""
        }}
    ],

    "short_answer": [],

    "medium_answer": [],

    "long_answer": []
}}
"""
)