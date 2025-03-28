import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
def doctypeValidator(diff_content):
    return f"""
        You are an expert technical writer specializing in software documentation.
        Your task is to analyze the changes in the following diff:

        {diff_content}

        Based on these changes, identify the most appropriate documentation type from the following categories:

        1. **Code**: Documentation within the code, including inline comments and docstrings.
        2. **API**: Guides on how to use functions, methods, and API endpoints. Often generated using tools like Swagger/OpenAPI, JSDoc, or Sphinx.
        3. **Technical**: Describes system architecture, data flows, design patterns, and dependencies.
        4. **User**: Provides step-by-step guides, tutorials, or user manuals on how to use the software.
        5. **Installation & Configuration**: Covers setup instructions, deployment steps, and environment configurations.
        6. **Testing**: Documents test cases, testing strategies (unit, integration, end-to-end), and quality assurance processes.
        7. **Development Process**: Explains methodologies, Git workflows, Definition of Done, PR policies, code conventions, style guides, and quality standards.

        Identify the most relevant documentation type based on the changes in the diff.

        ### Output Format:
        Return your response as a JSON object with the following structure:
        ```json
        {{
        "documentation_type": "<Selected documentation type>",
        "justification": "<Brief explanation based on the diff content>",
        "confidence": <Confidence score between 0 and 1>
        }}
        """