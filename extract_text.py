import sys

def extract_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    file_path = sys.argv[1]
    text = extract_text(file_path)
    print("\n--- Extracted Text ---\n")
    print(text[:1000])  # print first 1000 characters
