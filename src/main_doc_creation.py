from pathlib import Path
import sys

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from doc_generator_from_code import general_doc_generator
from docs_publisher_controller import base_doc_publisher


general_doc_generator.main()
base_doc_publisher.main()
