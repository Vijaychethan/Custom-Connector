from flask import Flask, jsonify, request
import puremagic

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message":"File Validation API - TrueType Validator"})

@app.route("/validate", methods=["POST"])
def validate():

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    file.stream.seek(0)
    from_stream = puremagic.from_stream(file.stream)

    file.stream.seek(0)
    magic_stream = puremagic.magic_stream(file.stream)

    return jsonify({
        "success": True,
        "filename": file.filename,
        "from_stream": from_stream,
        "matches": [
            {
                "extension": m.extension,
                "confidence": m.confidence
            }
            for m in magic_stream
        ]
    })

if __name__ == "__main__":
    app.run(debug=True)