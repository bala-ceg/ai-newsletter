from langchain.prompts import ChatPromptTemplate

#  Primary Newsletter Template
NEWSLETTER_TEMPLATE = ChatPromptTemplate.from_template("""
Write a professional AI and Data Analytics newsletter with the following topic:
{user_input}

Format it with:
1. **Headline**
2. **Introduction**
3. **Main content with subsections**
4. **Key takeaways**

Write in a **clear, professional style**. Provide the newsletter content **directly without any meta-commentary**.
If you need to think through your process, wrap that text in <think> tags.
""")

#  Refinement Template
REFINEMENT_TEMPLATE = ChatPromptTemplate.from_template("""
Here is a newsletter section:
{current_content}

Revise it according to these instructions:
{refinement_instructions}

Provide only the revised content without any explanations.
If you need to think through your process, wrap that text in <think> tags.
""")

#  Entertainment Template
ENTERTAINMENT_TEMPLATE = ChatPromptTemplate.from_template("""
Here is a newsletter section:
{current_content}

Revise it to make it more **entertaining and engaging** for readers interested in AI and Data Analytics.
Use a **lively tone** and add **interesting anecdotes or examples** where appropriate.

Provide only the revised content without any explanations.
If you need to think through your process, wrap that text in <think> tags.
""")
