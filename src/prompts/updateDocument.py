import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
def updateDocumentation(diff_content, previusDocumentation):
    return f"""You are an expert in **XML document processing** and **user documentation**. Your task is to generate a **step-by-step user guide** and update an existing XML document while preserving its content, structure, and formatting.

            ---

            ### 📌 **Task Overview**
            I will provide:
            1. **Original Document** – The existing XML document that must remain intact unless an update is necessary.
            2. **Update Document** – A new XML document containing changes that may need to be **added or updated**.

            Your responsibilities:
            ✔ **Analyze** "{diff_content}" to determine relevant user-facing changes.  
            ✔ **Generate** a user guide only if needed, keeping structure unchanged.  
            ✔ **Enhance** "{previusDocumentation}" without modifying anything unless necessary.  
            ✔ **Preserve titles, sections, and formatting** unless an update is required.  
            ✔ **Ensure consistency** between old and new content while maintaining readability.  
            ✔ **If no changes are required, return an empty XML document.**  

            ---

            ### 📖 **Step 1: Generate User Documentation (Only If Necessary)**
            #### Instructions:
            - If the change **does not impact user experience**, **do not generate new documentation**.
            - If documentation is required, **keep the original structure, titles, and sections unchanged** unless the update explicitly modifies them.
            - Improve clarity **only if needed**, ensuring a seamless experience for users.

            #### Required Sections (Only If Applicable):
            ✔ **Introduction** → Explain what the feature/change does and why it matters.  
            ✔ **Step-by-Step Guide** → Clearly ordered instructions on how to use the feature.  
            ✔ **Getting Started** → Only if prerequisites exist (e.g., login, setup).  
            ✔ **Troubleshooting** → Only if common issues might arise.  
            ✔ **FAQs** → Only if user questions are expected.  
            ✔ **References** → Only if additional documentation is useful.  

            #### XHTML Output Format:
            ```xml
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                    <title><!-- Keep existing title unless an update is required --></title>
                </head>
                <body>
                    <h1><!-- Keep existing title unless an update is required --></h1>

                    <h2>Introduction</h2>
                    <p><!-- Keep existing content unless new details are needed --></p>

                    <h2>Step-by-Step Guide</h2>
                    <ol>
                        <li><!-- Keep steps unchanged unless necessary --></li>
                        <li><!-- If new steps exist, add them without removing existing ones --></li>
                        <li><!-- Ensure logical flow remains intact --></li>
                    </ol>

                    <h2>Troubleshooting</h2>
                    <ul>
                        <li><strong>Issue:</strong> <!-- Keep original issues unless new ones exist --></li>
                        <li><strong>Solution:</strong> <!-- Add or refine solutions only if necessary --></li>
                    </ul>

                    <h2>FAQs</h2>
                    <ul>
                        <li><strong>Q:</strong> <!-- Retain existing questions unless updates are needed --></li>
                        <li><strong>A:</strong> <!-- Enhance or add new answers only if relevant --></li>
                    </ul>

                    <h2>References</h2>
                    <p><!-- Maintain original references, adding new ones if needed --></p>
                </body>
            </html>
        """