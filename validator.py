import pandas as pd
import sys

def validate_dataset(file_path: str) -> bool:
    """
    Validates scraped data against quality standards before delivery.
    Critical for Mindrift's requirement of 'accurate, reliable datasets'.
    """
    try:
        df = pd.read_csv(file_path)
        issues = []
        
        # Check 1: Empty dataset
        if df.empty:
            issues.append("CRITICAL: Dataset is empty")
            
        # Check 2: Missing values in key columns
        missing = df.isnull().sum()
        if missing.sum() > 0:
            issues.append(f"WARNING: {missing.sum()} missing values found")
            
        # Check 3: Duplicate rows
        dupes = df.duplicated().sum()
        if dupes > 0:
            issues.append(f"WARNING: {dupes} duplicate rows detected")
            
        # Check 4: Schema validation (example)
        required_cols = ["Quote", "Author"]
        missing_cols = [c for c in required_cols if c not in df.columns]
        if missing_cols:
            issues.append(f"CRITICAL: Missing columns: {missing_cols}")
            
        if issues:
            print("VALIDATION FAILED:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("✅ VALIDATION PASSED: Dataset meets quality standards")
            return True
            
    except FileNotFoundError:
        print(f"ERROR: File '{file_path}' not found")
        return False
    except Exception as e:
        print(f"ERROR: Validation failed - {e}")
        return False

if __name__ == "__main__":
    file_to_check = sys.argv[1] if len(sys.argv) > 1 else "scraped_quotes.csv"
    is_valid = validate_dataset(file_to_check)
    sys.exit(0 if is_valid else 1)