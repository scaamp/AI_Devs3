import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AIDEVS_API_KEY = os.getenv("AIDEVS_API_KEY")

url = "https://centrala.ag3nts.org/apidb"
url_report = "https://centrala.ag3nts.org/report"

def get_database_tables():
    params = {
        "task": "database",
        "apikey": AIDEVS_API_KEY,
        "query": "show tables"
    }
    
    response = requests.post(url, json=params)
    return response.json()

def get_table_structure(table_name):
    params = {
        "task": "database",
        "apikey": AIDEVS_API_KEY,
        "query": f"show create table {table_name}"
    }
    
    response = requests.post(url, json=params)
    return response.json()

def generate_sql_query(question, table_structures):
    prompt = f"""Based on the following database table structures and the question, generate a SQL query.
    Return ONLY the SQL query without any additional explanation.

    Question: {question}

    Table structures:
    {json.dumps(table_structures, indent=2)}
    """
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4.1",
        "messages": [
            {"role": "system", "content": "You are a SQL expert. Generate only the SQL query without any additional text. "},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )
    
    return response.json()["choices"][0]["message"]["content"].strip()

def execute_query(query):
    params = {
        "task": "database",
        "apikey": AIDEVS_API_KEY,
        "query": query
    }
    
    response = requests.post(url, json=params)
    return response.json()

def send_result_to_report(result):
    # Extract the actual data from the result
    if 'reply' in result and result['reply']:
        # Extract manager IDs from the result
        data = [row['dc_id'] for row in result['reply']]
        print("\nManager IDs:", data)
    else:
        data = []
        print("no data")
    
    # Send the data to the report endpoint
    params = {
        "task": "database",
        "apikey": AIDEVS_API_KEY,
        "answer": data
    }
    
    print("\nSending to report:", json.dumps(params, indent=2))
    
    response = requests.post(url_report, json=params)
    return response.json()

if __name__ == "__main__":
    # Get all tables
    tables_result = get_database_tables()
    print("Available tables:", tables_result)
    
    # Extract table names from the response
    if 'reply' in tables_result and tables_result['reply']:
        tables = [table['Tables_in_banan'] for table in tables_result['reply']]
        print("\nFound tables:", tables)
        
        # Get structure for each table
        table_structures = {}
        for table in tables:
            print(f"\nStructure for table {table}:")
            structure = get_table_structure(table)
            print(structure)
            if 'reply' in structure and structure['reply']:
                table_structures[table] = structure['reply'][0]['Create Table']
        
        # First, let's check the correct_order table for the hidden flag
        query = """
        SELECT base_id, letter, weight 
        FROM correct_order 
        ORDER BY weight ASC
        """
        
        print("\nExecuting query for correct_order...")
        result = execute_query(query)
        
        if 'reply' in result and result['reply']:
            print("\nCorrect order data:")
            for row in result['reply']:
                print(f"base_id: {row['base_id']}, letter: {row['letter']}, weight: {row['weight']}")
            
            # Try to find any patterns or hidden messages
            letters = [row['letter'] for row in result['reply']]
            print("\nLetters in order:", ''.join(letters))
        
        # Now, let's handle the datacenter query
        question = "które aktywne datacenter (DC_ID) są zarządzane przez pracowników, którzy są na urlopie (is_active=0)"
        print("\nGenerating SQL query for question:", question)
        generated_query = generate_sql_query(question, table_structures)
        print("\nGenerated SQL query:", generated_query)
        
        print("\nExecuting datacenter query...")
        dc_result = execute_query(generated_query)
        print("\nQuery result:", dc_result)
        
        # Send datacenter result to report endpoint
        print("\nSending datacenter result to report...")
        report_response = send_result_to_report(dc_result)
        print("\nReport response:", report_response)
    else:
        print("Error getting tables:", tables_result.get('error', 'Unknown error'))

