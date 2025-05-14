from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from agent_logic import sql_chain
from db_config import get_schema, run_query
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import re
import os
import threading
import webbrowser

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

def extract_sql(llm_output):
    match = re.search(r"```(?:sql)?\s*(.*?)```", llm_output, re.DOTALL)
    if match:
        return match.group(1).strip()
    lines = llm_output.splitlines()
    return " ".join([line.strip() for line in lines if any(kw in line.upper() for kw in ["SELECT", "INSERT", "UPDATE", "DELETE", "FROM"])])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    db_name = data.get("db_name")
    question = data.get("question")

    if not db_name or not question:
        return jsonify({"error": "Missing db_name or question"}), 400

    os.environ["DB_NAME"] = db_name
    schema = get_schema()

    if schema.startswith("Error"):
        return jsonify({"error": schema}), 400

    try:
        translated_question = GoogleTranslator(source='auto', target='en').translate(question)
        llm_response = sql_chain.run({"schema": schema, "question": translated_question})
        
        print("LLM response:", llm_response)

        sql = extract_sql(llm_response)
        print("Extracted SQL:", sql)

        if not sql:
            return jsonify({"error": "Failed to extract SQL query."}), 500

        result = run_query(sql)
        print("Query result:", result)

        print("Generated SQL:", sql)
        print("Query result:", result)

        return jsonify({
            "sql": sql,
            "result": result
        })

    except Exception as e:
        print("Error during /ask:", str(e))
        return jsonify({"error": str(e)}), 500


def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
