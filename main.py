import arxiv
import json
import time
from utils import download_pdf, extract_text
from analysis import analyze_paper
import sqlite3

def init_db():
    conn = sqlite3.connect("research_agent.db")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        searches TEXT  # JSON format
    )""")
    conn.close()

def save_search(username: str, query: str, results: list):
    conn = sqlite3.connect("research_agent.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, searches) VALUES (?, ?)", 
                  (username, json.dumps({"query": query, "results": results})))
    conn.commit()
    conn.close()
# arXiv's top-level categories
CATEGORIES = {
    "1": "cs.AI",
    "2": "cs.CL",
    "3": "cs.LG",
    "4": "cs.CV",
    "5": "stat.ML",
    "6": "cs.IR",
}


def fetch_papers(query: str, category: str, max_results: int = 3):
    try:
        refined_query = f"all:{query} AND cat:{category}"
        search = arxiv.Search(
            query=refined_query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )

        papers = []
        for result in search.results():
            paper = {
                "title": result.title,
                "summary": result.summary,
                "pdf_url": result.pdf_url,
                "published": result.published.date(),
                "authors": [author.name for author in result.authors],
                "category": category,
                "pdf_path": None,
                "extracted_text": None,
                "analysis": None
            }

            try:
                pdf_path = download_pdf(result.pdf_url)
                paper["pdf_path"] = pdf_path
                extracted = extract_text(pdf_path)
                paper["extracted_text"] = extracted[:1000] + "..." if extracted else None
                if extracted:
                    paper["analysis"] = analyze_paper(extracted)
            except Exception as e:
                print(f"⚠️ Failed to process {result.title}: {str(e)}")

            papers.append(paper)
            time.sleep(1)  # Be polite to arXiv's servers

        return papers

    except Exception as e:
        print(f"🚨 Error fetching papers: {str(e)}")
        return []


def main():
    print("📚 arXiv Paper Fetcher")

    # Get user input
    try:
        query = input("Research topic (e.g., 'attention mechanisms'): ").strip()
        if not query:
            print("❗ Please enter a valid query.")
            return
    except KeyboardInterrupt:
        return

    # Category selection
    print("\nCategories:")
    for num, cat in CATEGORIES.items():
        print(f"{num}. {cat}")

    try:
        choice = input("Category number (1-6): ").strip()
        category = CATEGORIES.get(choice, "cs.AI")
    except KeyboardInterrupt:
        return

    try:
        num_papers = int(input("Number of papers (1-50): ").strip())
        num_papers = max(1, min(50, num_papers))
    except (ValueError, KeyboardInterrupt):
        num_papers = 3

    # Fetch and display results
    papers = fetch_papers(query, category, num_papers)

    if not papers:
        print("\n❌ No papers found or error occurred")
        return

    print(f"\n🔍 Found {len(papers)} papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n📄 {i}. {paper['title']}")
        print(f"👤 Authors: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}")
        print(f"📅 Date: {paper['published']}")
        print(f"🔗 PDF: {paper['pdf_url']}")
        if paper['extracted_text']:
            print(f"\n📝 Extract: {paper['extracted_text']}")
        if paper['analysis']:
            print("\n📊 Analysis:")
            print(f"- {paper['analysis']['word_count']} words")
            print(f"- Top terms: {', '.join([w[0] for w in paper['analysis']['common_terms']])}")
            print(f"- ~{paper['analysis']['references']} references")

    # Save results
    try:
        with open("papers.json", "w") as f:
            json.dump(papers, f, indent=2, default=str)
        print("\n✅ Saved to papers.json")
    except Exception as e:
        print(f"❌ Failed to save: {str(e)}")


if __name__ == "__main__":
    main()
