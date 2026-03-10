import whisper
from neo4j import GraphDatabase
from neo4j.exceptions import CypherSyntaxError
import openai
import re

# Initialize the Whisper model
model = whisper.load_model("small")

def transcribe_audio(audio_file_path):
    result = model.transcribe(audio_file_path)
    return result['text']


#將輸入翻譯成英文
def translate_to_english(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Help me to translate the input into English."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message['content'].strip()

#將主詞替換成使用者
def preprocess_question(question, user_name="Benny"):
    return question.replace("I", user_name)


def classify_intent(question):
    messages = [
        {"role": "system", "content": "Analyze the following statement and classify its intent, considering it might relate to querying, updating, or creating data in a Neo4j database:"},
        {"role": "user", "content": question}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=50
    )
    intent = response.choices[0].message['content'].strip().lower()
    print("Intent detected:", intent)
    return response.choices[0].message['content'].strip().lower()

def is_food_related_intent(question):
    food_keywords = ['dinner', 'lunch', 'eat', 'meal', 'food']
    return any(keyword in question.lower() for keyword in food_keywords)


node_properties_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE NOT type = "RELATIONSHIP" AND elementType = "node"
WITH label AS nodeLabels, collect(property) AS properties
RETURN {labels: nodeLabels, properties: properties} AS output

"""

rel_properties_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE NOT type = "RELATIONSHIP" AND elementType = "relationship"
WITH label AS nodeLabels, collect(property) AS properties
RETURN {type: nodeLabels, properties: properties} AS output
"""

rel_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE type = "RELATIONSHIP" AND elementType = "relationship"
RETURN {source: label, relationship: property, target: other} AS output
"""

def schema_text(node_props, rel_props, rels):
    return f"""
  This is the schema representation of the Neo4j database.
  Node properties are the following:
  {node_props}
  Relationship properties are the following:
  {rel_props}
  Relationship point from source to target nodes
  {rels}
  Make sure to respect relationship types and directions
  """

#將全形轉半形
def clean_text_before_translation(text):
    conversions = {ord('，'): ',', ord('。'): '.', ord('！'): '!', ord('？'): '?', ord('：'): ':'}
    return text.translate(conversions)

#結果翻譯成繁體中文
def translate_to_chinese(text, target_language="zh-TW"):
    if isinstance(text, list):
        text = ':'.join(str(item) for item in text)
    text = clean_text_before_translation(text)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Translate the following text to {target_language}: {text}"}
        ]
    )
    translation = response.choices[0].message['content'].strip()
    print(text)
    print(translation)
    return response.choices[0].message['content'].strip()

#處理上傳和回應生成
def handle_file_upload(file_path, neo4j_gpt):
    try:
        transcription = transcribe_audio(file_path)
        print("Transcription: ", transcription)  # Debugging output
        translated_text = translate_to_english(transcription)
        print("Translated Text: ", translated_text)  # Debugging output
        processed_question = preprocess_question(translated_text)
        print("Processed Question: ", processed_question)  # Debugging output
        response = neo4j_gpt.run(processed_question)
        return response
    except Exception as e:
        return "An error occurred: " + str(e)

class Neo4jGPTQuery:
    def __init__(self, url, user, password, openai_api_key, user_name="Benny"):
        self.driver = GraphDatabase.driver(url, auth=(user, password))
        openai.api_key = openai_api_key
        self.user_name = user_name
        self.schema = self.generate_schema()

    #from Neo4j獲取節點 屬性 關係 data
    def generate_schema(self):
        node_props = self.query_database(node_properties_query)
        rel_props = self.query_database(rel_properties_query)
        rels = self.query_database(rel_query)
        return schema_text(node_props, rel_props, rels)
    #刷新
    def refresh_schema(self):
        self.schema = self.generate_schema()
        print("Schema updated to reflect latest database state.")

    def get_system_message(self):
        return f"""
        Task: Generate Cypher queries to interact with a Neo4j graph database. This includes querying, updating, and creating data based on user input.
        Instructions:
        - Use provided relationship types and properties for constructing queries.
        - Feel free to propose new nodes and relationships if the user's input suggests new data should be added.
        - Ensure that new data fits within the overall schema and database design.
        - If a query or creation command cannot be generated based on the user input or schema constraints, explain the reason to the user.
        Schema:
        {self.schema}

        Hello, {self.user_name}! I'm here to assist you with both querying and updating the Neo4j database based on your needs.

        Note: Focus on clear and actionable Cypher commands. Do not include any unnecessary explanations or apologies in your responses.
        """

    #執行Cypher query and merge
    def query_database(self, neo4j_query, params={}):
        with self.driver.session() as session:
            try:
                result = session.run(neo4j_query, params)
                output = [r.values() for r in result]
                output.insert(0, result.keys())
                return output
            except Exception as e:
                print("Error executing Cypher query:", str(e))
                return str(e)

    #調用GPT生成Cypher
    def construct_cypher(self, question, history=None):
        prompt = f"Given the question '{question}', generate a Cypher query for the Neo4j database. \
        Use direct Cypher command format without additional text or markdown.\
        Please format all node and property Location's name such that every property name starts with an 'lowercase letter'.For example, use (l:Location {{name: 'hospital'}} instead of (l:Location {{name: 'Hospital'}}.\
        Ensure to use the actual node labels, relationship types, and properties as per the schema. \
        For instance, use 'Person' and 'Location' for node labels, 'GO_TO' for relationship type, \
        and include 'time' for properties of both the 'Location' node and the relationships where applicable."
        messages = [
            {"role": "system", "content": self.get_system_message()},
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
        if history:
            messages.extend(history)
        completions = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0.0,
            max_tokens=100,
            messages=messages
        )
        return completions.choices[0].message['content'].strip()

    def construct_cypher_for_creation(self, question):
        
        prompt=f"""
        
        Generate a Cypher statement to merge new nodes and relationships based on {self.user_name} input.\
        For example:If the location does not exist, create a new node with the name 'school' and add details about the times {self.user_name} has to attend.\
        Ensure to use the actual node labels, relationship types, and properties as per the schema.
        Use direct Cypher command format without additional text or markdown.\
        Use the following format for the Cypher statement:\
        MERGE (p:Person{{name:'Benny'}})\
        MERGE (l:Location {{name: 'school'}})\
        ON CREATE SET l.time = 'every Tuesday and Wednesday'\
        ON MATCH SET l.time = 'every Tuesday and Wednesday'\
        ON CREATE SET r.time = 'every Tuesday and Wednesday'\
        ON MATCH SET r.time = 'every Tuesday and Wednesday'\
        MERGE (p)-[r:GO_TO]->(l)
        RETURN p, r, l
        """
        messages = [
            {"role": "system", "content": self.get_system_message()},
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
        # return "已記錄"

    def handle_general_chat(self, question):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message['content'].strip()

    def get_age_and_generate_food_suggestion(self, user_name="Benny"):
        try:
            query = f"MATCH (p:Person {{name: '{user_name}'}}) RETURN p.age AS Age"
            result = self.query_database(query)
            age = result[1][0]
            prompt = f"Generate a healthy meal suggestion for a {age}-year-old."
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            return "Unable to generate food suggestion due to an error."

    def run(self, question, history=None, retry=True):
        print("Received question:", question)
        intent = classify_intent(question)
        if is_food_related_intent(question):
            return self.get_age_and_generate_food_suggestion(self.user_name)
        elif "doesn't" in intent or "does not" in intent or "is not related to querying" in intent or "non-applicable" in intent:
            return self.handle_general_chat(question)
        elif "query" in intent or "querying" in intent:
            cypher = self.construct_cypher(question, history)
            print("Query Cypher:",cypher)
            try:
                return self.query_database(cypher)
            except CypherSyntaxError as e:
                if not retry:
                    return "Invalid Cypher syntax"
                return self.run(question, [{"role": "assistant", "content": cypher}, {"role": "user", "content": f"This query returns an error: {str(e)}"}], retry=False)
        #創造
        elif "record" in intent or "creating" in intent or "create" in intent or "updating" in intent or "update" in intent:
            cypher = self.construct_cypher_for_creation(question)
            print("Generated Cypher:", cypher)
            try:
                result = self.query_database(cypher)
                self.refresh_schema()
                return "Okay" or result
            except CypherSyntaxError as e:
                if not retry:
                    return "Invalid Cypher syntax"
                return self.run(question, [{"role": "assistant", "content": cypher}, {"role": "user", "content": f"This query returns an error: {str(e)} Please correct it."}], retry=False)
