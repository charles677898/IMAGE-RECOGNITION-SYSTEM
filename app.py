import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from model import predict_image

from database import (
    create_database,
    save_prediction,
    get_history,
    get_total_predictions,
    get_average_confidence,
    get_most_common_prediction
)


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# Create database on startup
create_database()


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    if "image" not in request.files:

        return redirect(
            url_for("home")
        )

    file = request.files["image"]

    if file.filename == "":

        return redirect(
            url_for("home")
        )

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(image_path)

    predictions = predict_image(
        image_path
    )

    top_prediction = predictions[0]

    prediction_name = top_prediction[0]

    confidence = top_prediction[1]

    save_prediction(
        file.filename,
        prediction_name,
        confidence
    )

    return render_template(
        "index.html",
        image=file.filename,
        predictions=predictions,
        prediction=prediction_name,
        confidence=confidence
    )


@app.route("/history")
def history():

    data = get_history()

    return render_template(
        "history.html",
        history=data
    )


@app.route("/dashboard")
def dashboard():

    total = get_total_predictions()

    avg_confidence = (
        get_average_confidence()
    )

    common_prediction = (
        get_most_common_prediction()
    )

    return render_template(
        "dashboard.html",
        total=total,
        avg_confidence=avg_confidence,
        common_prediction=common_prediction
    )


@app.route(
    "/uploads/<filename>"
)
def uploaded_file(filename):

    return redirect(
        url_for(
            "static",
            filename=f"uploads/{filename}"
        )
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )