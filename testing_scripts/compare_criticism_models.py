import json
import difflib
from collections import defaultdict
import ast

def load_output(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()
    try:
        return ast.literal_eval(data)
    except Exception as e:
        print("⚠️ Error loading file:", filename)
        print("Error:", e)
        print("\nFirst 500 characters of the file for debugging:")
        print(data[:500])  # Print a snippet to help you debug
        raise

def get_point_key(point_obj):
    # Using point text and sentiment_score as a unique key.
    return (point_obj["point"], point_obj["sentiment_score"])

def compare_outputs(output1, output2):
    """
    Compare two outputs (lists of point objects) and return:
      - Points missing in one output versus the other (i.e. dropped points).
      - For points that exist in both, their 'criticism_exists' flag and the detailed criticisms.
      - A diff of the criticisms text for common points.
    """
    # Build dictionaries keyed by (point, sentiment_score)
    dict1 = { get_point_key(pt): pt for pt in output1 }
    dict2 = { get_point_key(pt): pt for pt in output2 }
    
    all_keys = set(dict1.keys()).union(set(dict2.keys()))
    
    removed_in_1 = []  # Present in output2, missing in output1
    removed_in_2 = []  # Present in output1, missing in output2
    common_points = {}
    
    for key in all_keys:
        in1 = key in dict1
        in2 = key in dict2
        if not in1:
            removed_in_1.append(key)
        if not in2:
            removed_in_2.append(key)
        if in1 and in2:
            common_points[key] = (dict1[key], dict2[key])
    
    diff_details = {}
    for key, (pt1, pt2) in common_points.items():
        criticisms1 = "\n".join([f"ID {crit['comment_id']}: {crit['criticism']} (Score: {crit['validity_score']})" 
                                 for crit in pt1.get("criticisms", [])])
        criticisms2 = "\n".join([f"ID {crit['comment_id']}: {crit['criticism']} (Score: {crit['validity_score']})" 
                                 for crit in pt2.get("criticisms", [])])
        diff = list(difflib.ndiff(criticisms1.splitlines(), criticisms2.splitlines()))
        diff_details[key] = diff

    return {
        "removed_in_output1": removed_in_1,
        "removed_in_output2": removed_in_2,
        "common_points": common_points,
        "diff_details": diff_details
    }

def save_comparison_report(comp, filename="comparison_report.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== Comparison Report ===\n\n")

        f.write("Points dropped in output1 (present in output2 but missing in output1):\n")
        for key in comp["removed_in_output1"]:
            f.write(f"  Point: {key[0]} (Sentiment: {key[1]})\n")

        f.write("\nPoints dropped in output2 (present in output1 but missing in output2):\n")
        for key in comp["removed_in_output2"]:
            f.write(f"  Point: {key[0]} (Sentiment: {key[1]})\n")

        f.write("\n=== Detailed Comparison for Common Points ===\n\n")
        for key, (pt1, pt2) in comp["common_points"].items():
            f.write(f"Point: {key[0]} (Sentiment: {key[1]})\n")
            f.write(f"  Output1 - Criticism Exists: {pt1.get('criticism_exists')}, Criticisms:\n")
            for crit in pt1.get("criticisms", []):
                f.write(f"    Comment {crit['comment_id']}: {crit['criticism']} (Score: {crit['validity_score']})\n")
            f.write(f"  Output2 - Criticism Exists: {pt2.get('criticism_exists')}, Criticisms:\n")
            for crit in pt2.get("criticisms", []):
                f.write(f"    Comment {crit['comment_id']}: {crit['criticism']} (Score: {crit['validity_score']})\n")
            f.write("  Differences in criticisms:\n")
            for line in comp["diff_details"][key]:
                f.write(f"    {line}\n")
            f.write("-" * 40 + "\n")

if __name__ == "__main__":
    # Load outputs from the two models.
    output_o3 = load_output("output_o3_mini.json")
    output_gpt4 = load_output("output_gpt4o.json")
    
    comp = compare_outputs(output_o3, output_gpt4)
    save_comparison_report(comp)
