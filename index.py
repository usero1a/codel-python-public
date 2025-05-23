import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    try:
        # Get search query from the URL
        query = request.args.get("q", "").strip()
        
        if not query:
            return render_template('search.html', results=[], message="No search query provided.")

        url = ""
        headers = {
            "content-type": "application/json",
            "x-api-key": ""
        }
        data = {
            "query": f"find {query} on GitHub, GitLab and npm and make sure to show result for all three",  # Use the actual user input as the query
            "contents": {
                "text": {"maxCharacters": 1000}
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Ensure the response is successful
        
        results = response.json()  # Parse JSON response
        
        # Debugging: Print response to check structure
        print("API Response:", results)

        # Extract search results from response
        search_results = results.get("results", [])  # Ensure it's always a list
        
        return render_template('search.html', results=search_results, query=query)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500
      
@app.route("/search-code")
def search_code():
    try:
      
    
        query = request.args.get("q", "").strip() 
        # Directly use 'python' in the API URL
        url = f""
        
        # Send GET request
        response = requests.get(url)
        response.raise_for_status()  # Ensure the response was successful

        results = response.json()  # Parse JSON response

        # Extract search results safely
        search_results = results.get("results", []) if isinstance(results, dict) else []

        return render_template('search-code.html', results=search_results)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route("/test")
def test():
    return render_template("spare.html")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
