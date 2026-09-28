import os

from flask import Flask, jsonify, redirect, render_template, request

app = Flask(__name__)

notes = []  # in-memory data: {"id", "title", "subject", "author", "content", "likes"}
COMMIT = os.getenv("RENDER_GIT_COMMIT", "local")[:7]


def matches(note, query, subject):
    text = f"{note['title']} {note['content']} {note['author']}".lower()
    if query and query.lower() not in text:
        return False
    return not subject or note["subject"].lower() == subject.lower()


@app.route("/")
def home():
    query = request.args.get("q", "").strip()
    subject = request.args.get("subject", "").strip()
    shown = [n for n in notes if matches(n, query, subject)]
    subjects = sorted({n["subject"] for n in notes})
    return render_template("index.html", notes=shown, total=len(notes),
                           subjects=subjects, query=query,
                           subject=subject, commit=COMMIT)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    author = request.form.get("author", "").strip()
    content = request.form.get("content", "").strip()
    if not (title and subject and author and content):
        return "Title, subject, author and content are required", 400
    if len(title) > 100 or len(content) > 2000:
        return "Title max 100 and content max 2000 characters", 400
    notes.append({"id": len(notes) + 1, "title": title, "subject": subject,
                  "author": author, "content": content, "likes": 0})
    return redirect("/")


@app.route("/like/<int:note_id>", methods=["POST"])
def like(note_id):
    for n in notes:
        if n["id"] == note_id:
            n["likes"] += 1
            return redirect("/")
    return "Note not found", 404


@app.route("/api/notes")
def api_notes():
    subject = request.args.get("subject", "").strip()
    query = request.args.get("q", "").strip()
    return jsonify([n for n in notes if matches(n, query, subject)])


@app.route("/health")
def health():
    return {"status": "ok", "commit": COMMIT}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
