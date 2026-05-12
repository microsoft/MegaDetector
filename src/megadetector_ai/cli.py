"""
MegaDetector command-line interface.

Usage:
    megadetector detect --input ./images/
    megadetector detect --input photo.jpg --output results.json
    megadetector detect --input ./images/ --model MDV6-apa-rtdetr-e --threshold 0.2
    megadetector detect --input ./images/ --device cpu
    megadetector train --config ./config.yaml
    megadetector validate --config ./config.yaml
    megadetector inference --config ./config.yaml
"""

import argparse
import json
import sys
from pathlib import Path


def detect(args):
    """Run MegaDetector on images."""
    from megadetector_ai import MegaDetectorV6

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} does not exist", file=sys.stderr)
        sys.exit(1)

    device = args.device
    if device is None:
        import torch
        device = "cuda:0" if torch.cuda.is_available() else "cpu"

    print(f"Loading MegaDetector ({args.model}) on {device}...")
    model = MegaDetectorV6(device=device, pretrained=True, version=args.model)

    if input_path.is_file():
        print(f"Processing {input_path}...")
        results = model.single_image_detection(str(input_path))
        detections = _format_detections(str(input_path), results, args.threshold)
        all_results = [detections]
    elif input_path.is_dir():
        extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
        image_files = sorted(
            p for p in input_path.rglob("*") if p.suffix.lower() in extensions
        )
        if not image_files:
            print(f"No image files found in {input_path}", file=sys.stderr)
            sys.exit(1)

        print(f"Found {len(image_files)} images in {input_path}")
        all_results = []
        for i, img_path in enumerate(image_files):
            results = model.single_image_detection(str(img_path))
            detections = _format_detections(str(img_path), results, args.threshold)
            all_results.append(detections)
            if (i + 1) % 100 == 0 or (i + 1) == len(image_files):
                print(f"  Processed {i + 1}/{len(image_files)}")
    else:
        print(f"Error: {input_path} is not a file or directory", file=sys.stderr)
        sys.exit(1)

    total_detections = sum(len(r["detections"]) for r in all_results)
    images_with_animals = sum(
        1 for r in all_results
        if any(d["category"] == "animal" for d in r["detections"])
    )

    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w") as f:
            json.dump(all_results, f, indent=2)
        print(f"\nResults saved to {output_path}")
    else:
        print(json.dumps(all_results, indent=2))

    print(f"\nSummary: {len(all_results)} images, {total_detections} detections, "
          f"{images_with_animals} images with animals")


def _format_detections(image_path, results, threshold):
    """Format detection results as a dict."""
    CLASS_NAMES = {0: "animal", 1: "person", 2: "vehicle"}
    detections = []

    if results["detections"] is not None:
        for xyxy, conf, cls_id in zip(
            results["detections"].xyxy,
            results["detections"].confidence,
            results["detections"].class_id,
        ):
            if conf >= threshold:
                detections.append({
                    "category": CLASS_NAMES.get(int(cls_id), "unknown"),
                    "confidence": round(float(conf), 4),
                    "bbox": [round(float(x), 1) for x in xyxy],
                })

    return {
        "file": image_path,
        "detections": detections,
    }


def train(args):
    """Train a detection model."""
    from megadetector_ai.training import train as run_training

    config_path = args.config
    if not Path(config_path).exists():
        print(f"Error: Config file {config_path} does not exist", file=sys.stderr)
        sys.exit(1)

    print(f"Starting training with config: {config_path}")
    results = run_training(config_path)
    print("Training completed successfully")
    return results


def validate(args):
    """Validate a detection model."""
    from megadetector_ai.training import validate as run_validation

    config_path = args.config
    if not Path(config_path).exists():
        print(f"Error: Config file {config_path} does not exist", file=sys.stderr)
        sys.exit(1)

    print(f"Starting validation with config: {config_path}")
    metrics = run_validation(config_path)
    print("Validation completed successfully")
    return metrics


def inference(args):
    """Run inference on test data."""
    from megadetector_ai.training import inference as run_inference

    config_path = args.config
    if not Path(config_path).exists():
        print(f"Error: Config file {config_path} does not exist", file=sys.stderr)
        sys.exit(1)

    print(f"Starting inference with config: {config_path}")
    results = run_inference(config_path)
    print("Inference completed successfully")
    return results


def main():
    parser = argparse.ArgumentParser(
        prog="megadetector",
        description="MegaDetector: AI-powered wildlife detection for camera trap images",
    )
    subparsers = parser.add_subparsers(dest="command")

    detect_parser = subparsers.add_parser(
        "detect", help="Run MegaDetector on images"
    )
    detect_parser.add_argument(
        "--input", "-i", required=True,
        help="Path to an image file or directory of images",
    )
    detect_parser.add_argument(
        "--output", "-o", default=None,
        help="Path to save JSON results (prints to stdout if omitted)",
    )
    detect_parser.add_argument(
        "--model", "-m", default="MDV6-yolov9-c",
        help="Model variant (default: MDV6-yolov9-c)",
    )
    detect_parser.add_argument(
        "--threshold", "-t", type=float, default=0.2,
        help="Confidence threshold (default: 0.2)",
    )
    detect_parser.add_argument(
        "--device", "-d", default=None,
        help="Device: cuda:0, cpu, mps (default: auto-detect)",
    )

    train_parser = subparsers.add_parser(
        "train", help="Train a detection model"
    )
    train_parser.add_argument(
        "--config", "-c", default="./config.yaml",
        help="Path to training config file (default: ./config.yaml)",
    )

    validate_parser = subparsers.add_parser(
        "validate", help="Validate a detection model"
    )
    validate_parser.add_argument(
        "--config", "-c", default="./config.yaml",
        help="Path to validation config file (default: ./config.yaml)",
    )

    inference_parser = subparsers.add_parser(
        "inference", help="Run inference on test data"
    )
    inference_parser.add_argument(
        "--config", "-c", default="./config.yaml",
        help="Path to inference config file (default: ./config.yaml)",
    )

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "detect":
        detect(args)
    elif args.command == "train":
        train(args)
    elif args.command == "validate":
        validate(args)
    elif args.command == "inference":
        inference(args)


if __name__ == "__main__":
    main()
