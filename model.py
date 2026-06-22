import numpy as np

from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)

from tensorflow.keras.preprocessing import image


# Load pretrained model once
model = MobileNetV2(weights="imagenet")


def predict_image(image_path):

    img = image.load_img(
        image_path,
        target_size=(224, 224)
    )

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    img_array = preprocess_input(
        img_array
    )

    predictions = model.predict(
        img_array,
        verbose=0
    )

    results = decode_predictions(
        predictions,
        top=3
    )[0]

    final_results = []

    for result in results:

        class_name = result[1]

        confidence = round(
            float(result[2]) * 100,
            2
        )

        final_results.append(
            (
                class_name,
                confidence
            )
        )

    return final_results