from langchain_core.prompts import PromptTemplate

TOPIC_EXAM_PROMPT = PromptTemplate.from_template(
"""
You are an expert Gujarat TAT English paper setter.

Topic: {topic}

Context: {context}

Rules:
1. Use ONLY information from the supplied context.
2. Do NOT use outside knowledge.
3. Generate questions suitable for Gujarat TAT preparation.
4. Generate answers along with questions.
5. Answers must come only from the supplied context.
6. Assign marks to each question exactly as specified in the schema below.
7. Return ONLY valid JSON.
8. No markdown.
9. No explanations.

Return schema:
{{
  "topic":"{topic}",
  "mcq":[
    {{
      "question":"",
      "options":["","","",""],
      "answer":"",
      "marks": 1
    }}
  ],
  "fill_blank":[
    {{
      "question":"",
      "answer":"",
      "marks": 1
    }}
  ],
  "true_false":[
    {{
      "statement":"",
      "answer": true,
      "marks": 1
    }}
  ],
  "match":[
    {{
      "left":"",
      "right":"",
      "marks": 1
    }}
  ],
  "short_answer":[
    {{
      "question":"",
      "answer":"",
      "marks": 2
    }}
  ],
  "medium_answer":[
    {{
      "question":"",
      "answer":"",
      "marks": 4
    }}
  ],
  "long_answer":[
    {{
      "question":"",
      "answer":"",
      "marks": 6
    }}
  ]
}}
"""
)



CHAPTER_NOTES_PROMPT = PromptTemplate.from_template(
"""
You are an expert Gujarat TAT English mentor.

Topic: {topic}
Source: {source}

Context:
{context}

If source = textbook:
Generate notes focusing on: author, theme, summary, important_points, important_words, mcq, fill_blank, one_mark, short_answer, long_answer.

If source = pedagogy_1 or pedagogy_2:
Generate notes focusing on: definition, characteristics, principles, merits, demerits, summary, important_points, important_words, mcq, fill_blank, one_mark, short_answer, long_answer.

Rules:
1. Use ONLY the supplied context.
2. Do NOT use outside knowledge.
3. Create exam-oriented revision notes.
4. Focus on important concepts likely to help in TAT preparation.
5. Extract important words and meanings if available.
6. Generate concise but complete notes.
7. If a field in the schema does not apply to the source (e.g., no 'author' for pedagogy), leave it as an empty string "" or empty list [].
8. Return ONLY valid JSON.
9. No markdown.
10. No explanations outside JSON.

Return schema:
{{
  "topic": "{topic}",
  "source": "{source}",
  "author": "",
  "theme": "",
  "definition": "",
  "characteristics": [],
  "principles": [],
  "merits": [],
  "demerits": [],
  "summary": "",
  "important_points": [
    ""
  ],
  "important_words": [
    {{
      "word": "",
      "meaning": ""
    }}
  ],
  "mcq": [
    {{
      "question": "",
      "options": ["", "", "", ""],
      "answer": ""
    }}
  ],
  "fill_blank": [
    {{
      "question": "",
      "answer": ""
    }}
  ],
  "one_mark": [
    {{
      "question": "",
      "answer": ""
    }}
  ],
  "short_answer": [
    {{
      "question": "",
      "answer": ""
    }}
  ],
  "long_answer": [
    {{
      "question": "",
      "answer": ""
    }}
  ]
}}

Requirements:
* Summary: 400-500 words.
* Important Points: 10 points.
* Important Words: 10 words with meanings whenever available.
* MCQ: 5 questions.
* Fill Blank: 5 questions.
* One Mark: 5 questions.
* Short Answer: 3 questions.
* Long Answer: 2 questions.
"""
)
