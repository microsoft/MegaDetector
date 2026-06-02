---
title: "MegaDetector Output Format, detection JSON schema"
description: "MegaDetector output format: the JSON schema for detection results, file path, category, confidence score, and bounding box, and how to use it downstream."
tags:
  - megadetector output json
  - detection schema
  - bounding box format
  - camera trap AI
  - megadetector results
---

# Output Format

MegaDetector writes its results as JSON. Whether you run the [`megadetector` CLI](cli.md) or the Python API, the structure is the same: a list of per-image records, each holding the image path and the objects detected in it.

## Schema

The top level is a JSON **list**. Each element describes one image:

```json
[
  {
    "file": "images/IMG_0001.jpg",
    "detections": [
      { "category": "animal",  "confidence": 0.93, "bbox": [102.4, 88.1, 540.7, 470.2] },
      { "category": "person",  "confidence": 0.81, "bbox": [12.0, 40.5, 96.3, 510.9] }
    ]
  },
  {
    "file": "images/IMG_0002.jpg",
    "detections": []
  }
]
```

An image with no detections above the threshold has an empty `detections` list, that is how blank frames are represented.

## Fields

| Field | Type | Description |
| --- | --- | --- |
| `file` | string | Path to the image, as supplied to the detector |
| `detections` | list | One object per detection kept above the threshold (empty if none) |
| `detections[].category` | string | `animal`, `person`, or `vehicle` |
| `detections[].confidence` | float | Detection confidence from 0 to 1, rounded to 4 decimals |
| `detections[].bbox` | list of 4 floats | Bounding box as `[x1, y1, x2, y2]` (top-left and bottom-right pixel coordinates), rounded to 1 decimal |

The category names map from the model's class IDs: `0 → animal`, `1 → person`, `2 → vehicle`.

## Thresholding

Only detections whose confidence is greater than or equal to your chosen threshold are written; everything below is dropped. The CLI default is `0.2`, and most projects tune within `0.15–0.3` for the animal category. Lowering the threshold favors recall (fewer missed animals) at the cost of more false positives; raising it does the reverse.

## Using the output

The JSON is designed to flow straight into the rest of a camera-trap workflow:

- **Review**, import it into a tool such as Timelapse to verify and annotate detections (see [Camera-Trap Software](camera-trap-software.md)).
- **Filter**, drop images whose `detections` list is empty to clear blank frames in bulk.
- **Classify**, crop each `bbox` and pass it to a species classifier (see the two-stage pipeline in the [FAQ](faq.md)).

## Next steps

- [CLI reference](cli.md): the `detect` command that produces this JSON
- [Camera-Trap Software](camera-trap-software.md): review and analysis tools that consume it
- [Model Zoo](model_zoo.md): choose the variant that produced your detections
