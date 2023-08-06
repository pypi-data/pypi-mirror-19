import sys
import solar_corr

import warnings

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    # This needs a lot of work
    if len(sys.argv) < 3:
        print("python -m solar_correlation_map CSV_FILE_PATH SUN_VARIABLE [IMAGE_FILE_NAME]")
        print("example: python -m solar_correlation_map jedi.csv JEDI jedi.png")

    image_path = sys.argv[3] if len(sys.argv) > 3 else "solar.png"
    solar_corr.main(sys.argv[1], sys.argv[2], image_path)

