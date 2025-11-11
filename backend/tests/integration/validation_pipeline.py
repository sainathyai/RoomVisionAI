"""
Validation Pipeline - Tests room detection accuracy against ground truth.

Calculates IoU (Intersection over Union) and other metrics for validation.
"""

import json
from pathlib import Path
from typing import List, Dict, Tuple
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.src.domain.value_objects.bounding_box import BoundingBox


class ValidationPipeline:
    """Validates room detection results against ground truth."""
    
    @staticmethod
    def calculate_iou(pred_box: List[float], true_box: List[float]) -> float:
        """
        Calculate Intersection over Union (IoU) between two bounding boxes.
        
        Args:
            pred_box: Predicted bounding box [x_min, y_min, x_max, y_max]
            true_box: Ground truth bounding box [x_min, y_min, x_max, y_max]
            
        Returns:
            IoU value between 0 and 1
        """
        pred_bbox = BoundingBox.from_list(pred_box)
        true_bbox = BoundingBox.from_list(true_box)
        
        # Calculate intersection
        x1 = max(pred_bbox.x_min, true_bbox.x_min)
        y1 = max(pred_bbox.y_min, true_bbox.y_min)
        x2 = min(pred_bbox.x_max, true_bbox.x_max)
        y2 = min(pred_bbox.y_max, true_bbox.y_max)
        
        if x2 <= x1 or y2 <= y1:
            return 0.0
        
        intersection = (x2 - x1) * (y2 - y1)
        
        # Calculate union
        pred_area = pred_bbox.area
        true_area = true_bbox.area
        union = pred_area + true_area - intersection
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    @staticmethod
    def match_rooms(predicted_rooms: List[Dict], ground_truth_rooms: List[Dict], 
                   iou_threshold: float = 0.5) -> List[Tuple[Dict, Dict, float]]:
        """
        Match predicted rooms to ground truth rooms based on IoU.
        
        Args:
            predicted_rooms: List of predicted room dictionaries
            ground_truth_rooms: List of ground truth room dictionaries
            iou_threshold: Minimum IoU for a match
            
        Returns:
            List of tuples (predicted_room, ground_truth_room, iou)
        """
        matches = []
        used_gt_indices = set()
        
        for pred_room in predicted_rooms:
            best_match = None
            best_iou = 0.0
            best_gt_idx = -1
            
            for idx, gt_room in enumerate(ground_truth_rooms):
                if idx in used_gt_indices:
                    continue
                
                iou = ValidationPipeline.calculate_iou(
                    pred_room["bounding_box"],
                    gt_room["bounding_box"]
                )
                
                if iou > best_iou and iou >= iou_threshold:
                    best_iou = iou
                    best_match = gt_room
                    best_gt_idx = idx
            
            if best_match:
                matches.append((pred_room, best_match, best_iou))
                used_gt_indices.add(best_gt_idx)
        
        return matches
    
    @staticmethod
    def calculate_metrics(predicted_rooms: List[Dict], ground_truth_rooms: List[Dict]) -> Dict:
        """
        Calculate comprehensive validation metrics.
        
        Args:
            predicted_rooms: List of predicted rooms
            ground_truth_rooms: List of ground truth rooms
            
        Returns:
            Dictionary with metrics
        """
        matches = ValidationPipeline.match_rooms(predicted_rooms, ground_truth_rooms)
        
        # Calculate IoU for matched rooms
        ious = [match[2] for match in matches]
        avg_iou = sum(ious) / len(ious) if ious else 0.0
        
        # Detection rate
        detection_rate = len(matches) / len(ground_truth_rooms) if ground_truth_rooms else 0.0
        
        # False positive rate
        false_positives = len(predicted_rooms) - len(matches)
        false_positive_rate = false_positives / len(predicted_rooms) if predicted_rooms else 0.0
        
        # Precision and Recall
        precision = len(matches) / len(predicted_rooms) if predicted_rooms else 0.0
        recall = detection_rate
        
        # F1 Score
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        return {
            "total_ground_truth": len(ground_truth_rooms),
            "total_detected": len(predicted_rooms),
            "matched": len(matches),
            "false_positives": false_positives,
            "false_negatives": len(ground_truth_rooms) - len(matches),
            "average_iou": avg_iou,
            "detection_rate": detection_rate,
            "false_positive_rate": false_positive_rate,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "ious": ious
        }
    
    @staticmethod
    def validate_blueprint(predicted_path: str, ground_truth_path: str) -> Dict:
        """
        Validate a single blueprint's predictions.
        
        Args:
            predicted_path: Path to predicted rooms JSON
            ground_truth_path: Path to ground truth JSON
            
        Returns:
            Validation metrics dictionary
        """
        with open(predicted_path, 'r') as f:
            predicted_data = json.load(f)
        
        with open(ground_truth_path, 'r') as f:
            ground_truth_data = json.load(f)
        
        predicted_rooms = predicted_data.get("rooms", [])
        ground_truth_rooms = ground_truth_data.get("ground_truth", [])
        
        return ValidationPipeline.calculate_metrics(predicted_rooms, ground_truth_rooms)
    
    @staticmethod
    def run_validation_suite(test_suite_dir: str, results_dir: str) -> Dict:
        """
        Run validation on entire test suite.
        
        Args:
            test_suite_dir: Directory containing test blueprints
            results_dir: Directory containing prediction results
            
        Returns:
            Aggregate metrics dictionary
        """
        test_suite_path = Path(test_suite_dir)
        results_path = Path(results_dir)
        
        # Load manifest
        manifest_path = test_suite_path / "test_suite_manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        all_metrics = []
        
        # Process each level
        for level_name, level_data in manifest.get("levels", {}).items():
            for blueprint_info in level_data.get("blueprints", []):
                blueprint_id = blueprint_info["id"]
                
                # Find ground truth
                gt_path = test_suite_path / "ground-truth" / f"{blueprint_id}_ground_truth.json"
                
                # Find predictions (if they exist)
                pred_path = results_path / f"{blueprint_id}_predicted.json"
                
                if not gt_path.exists():
                    print(f"Warning: Ground truth not found for {blueprint_id}")
                    continue
                
                if not pred_path.exists():
                    print(f"Warning: Predictions not found for {blueprint_id}")
                    continue
                
                metrics = ValidationPipeline.validate_blueprint(str(pred_path), str(gt_path))
                metrics["blueprint_id"] = blueprint_id
                metrics["level"] = level_name
                all_metrics.append(metrics)
        
        # Calculate aggregate metrics
        if not all_metrics:
            return {"error": "No validations performed"}
        
        aggregate = {
            "total_blueprints": len(all_metrics),
            "average_iou": sum(m["average_iou"] for m in all_metrics) / len(all_metrics),
            "average_detection_rate": sum(m["detection_rate"] for m in all_metrics) / len(all_metrics),
            "average_precision": sum(m["precision"] for m in all_metrics) / len(all_metrics),
            "average_recall": sum(m["recall"] for m in all_metrics) / len(all_metrics),
            "average_f1_score": sum(m["f1_score"] for m in all_metrics) / len(all_metrics),
            "blueprint_metrics": all_metrics
        }
        
        return aggregate


if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate room detection results")
    parser.add_argument("--test-suite", required=True, help="Path to test suite directory")
    parser.add_argument("--results", required=True, help="Path to results directory")
    parser.add_argument("--output", help="Output JSON file for metrics")
    
    args = parser.parse_args()
    
    metrics = ValidationPipeline.run_validation_suite(args.test_suite, args.results)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"Metrics saved to {args.output}")
    else:
        print(json.dumps(metrics, indent=2))

