import os
from flask import Flask, render_template, request
from main import fetch_papers
from analysis import summarize

app = Flask(__name__,template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get form data
        query = request.form.get("query", "").strip()
        category = request.form.get("category", "cs.AI")
        num_papers = int(request.form.get("num_papers", 5))
        # Fetch papers (reuse your terminal logic)
        papers = fetch_papers(query, category,max_results= num_papers)
        
        # Add summaries
        for paper in papers:
            paper["summary"] = summarize(paper.get("extracted_text", ""))
        
        return render_template("results.html", papers=papers)
    
    # Show search form for GET requests
    return render_template("search.html")

if __name__ == "__main__":
    print("Current working directory:", os.getcwd())

    app.run(debug=True, port=5000)