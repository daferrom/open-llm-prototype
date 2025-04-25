import sys
from pathlib import Path

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))

from client_api_ai.prompt_templates import doc_from_code_template_prompts , prompt_templates
from xhtml_generator.xhtml_doc_generator_from_code import create_xhtml_doc

def main():
     # Creates the xhtml general documentation and saves it in xhtml file for publishin on the confluence space
    create_xhtml_doc(input_query=prompt_templates["GENERAL_DOCUMENTATION"], doc_name="GENERAL_DOCUMENTATION")

    # Creates each one of the documentation types and saves the xhtml files
    for prompt_key , prompt_value in doc_from_code_template_prompts.items():
        create_xhtml_doc(input_query=prompt_value , doc_name=prompt_key)

    print("...XHTML Docs created and saved, ready for publishing ✅")


if __name__ == "__main__":
   main()