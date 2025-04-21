prompt_templates = {
    "Code": """
        You are an expert technical writer specializing in software documentation. Your task is to generate XHTML documentation based on the provided Git `.diff` file, focusing on **Code changes** (new features, refactoring, bug fixes).  

        **Instructions:**
        - **Analyze `{diff_content}`** to determine the nature of code modifications.
        - **Generate a clear title** summarizing the change.
        - **Include only relevant sections**:
        - **Overview** (brief summary of what was changed).
        - **New Features** (if new functionality was introduced).
        - **Bug Fixes** (if issues were resolved).
        - **Refactoring** (if code structure was improved).
        - **Breaking Changes** (if previous functionality was altered).
        - **Implementation Details** (if necessary for understanding the change).

        **Output (XHTML format):**
        ```xml
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title><!-- Generated title --></title>
        </head>
        <body>
            <h1><!-- Generated title --></h1>

            <!-- Sections included only if relevant -->
            <h2>Overview</h2><p><!-- Summary of changes --></p>
            <h2>New Features</h2><p><!-- Description of new functionality --></p>
            <h2>Bug Fixes</h2><p><!-- Description of fixed issues --></p>
            <h2>Refactoring</h2><p><!-- Explanation of structural improvements --></p>
            <h2>Breaking Changes</h2><p><!-- Details on incompatible modifications --></p>
            <h2>Implementation Details</h2><p><!-- Explanation of key technical aspects --></p>

        </body>
        </html>
        ```
    """,
    "API": """
        You are an expert technical writer specializing in API documentation. Your task is to generate XHTML documentation based on the provided Git `.diff` file, focusing on **API changes** (new endpoints, modifications, deprecations).  

        **Instructions:**
        - **Analyze `{diff_content}`** to determine the nature of API modifications.
        - **Generate a clear title** summarizing the change.
        - **Include only relevant sections**:
        - **Overview** (brief summary of API modifications).
        - **New Endpoints** (if new API routes were introduced).
        - **Updated Endpoints** (if existing routes were modified).
        - **Deprecated Endpoints** (if any endpoints were removed or deprecated).
        - **Request & Response Changes** (if payloads, headers, or formats were altered).
        - **Authentication & Permissions** (if security settings were updated).
        - **Breaking Changes** (if previous API behavior was changed).
        - **Usage Examples** (if needed for clarity).

        **Output (XHTML format):**
        ```xml
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title><!-- Generated title --></title>
        </head>
        <body>
            <h1><!-- Generated title --></h1>

            <!-- Sections included only if relevant -->
            <h2>Overview</h2><p><!-- Summary of API changes --></p>
            <h2>New Endpoints</h2><p><!-- List of newly introduced API routes --></p>
            <h2>Updated Endpoints</h2><p><!-- Changes to existing API routes --></p>
            <h2>Deprecated Endpoints</h2><p><!-- Endpoints that are no longer supported --></p>
            <h2>Request & Response Changes</h2>
            <ul>
                <li><strong>New Fields:</strong> <!-- Added parameters or attributes --></li>
                <li><strong>Modified Fields:</strong> <!-- Updated existing parameters --></li>
                <li><strong>Removed Fields:</strong> <!-- Deprecated attributes --></li>
            </ul>
            <h2>Authentication & Permissions</h2><p><!-- Security modifications --></p>
            <h2>Breaking Changes</h2><p><!-- Any non-backward-compatible modifications --></p>
            <h2>Usage Examples</h2><pre><!-- Example API requests and responses --></pre>

        </body>
        </html>
        ```
    """,
    "Technical": """
        You are an expert technical writer specializing in software architecture and system design documentation. Your task is to generate XHTML documentation based on the provided Git `.diff` file, focusing on **Technical Documentation** (system architecture, data flows, design patterns, dependencies).  

        **Instructions:**
        - **Analyze `{diff_content}`** to identify relevant technical changes.
        - **Generate a clear title** summarizing the architectural or design change.
        - **Include only relevant sections**:
        - **Overview** (brief summary of the change).
        - **System Architecture** (if high-level structural changes were made).
        - **Data Flow & Processing** (if the way data is handled was modified).
        - **Design Patterns & Best Practices** (if new patterns were implemented).
        - **Dependencies & Integrations** (if external libraries or services were added/removed).
        - **Database Schema Updates** (if database tables, relationships, or indexes were modified).
        - **Diagrams & Visual Aids** (if UML diagrams, flowcharts, or schemas are relevant).
        - **Developer Guidelines** (if coding practices or conventions were introduced/updated).

        **Output (XHTML format):**
        ```xml
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title><!-- Generated title --></title>
        </head>
        <body>
            <h1><!-- Generated title --></h1>

            <!-- Sections included only if relevant -->
            <h2>Overview</h2><p><!-- Summary of changes --></p>
            <h2>System Architecture</h2><p><!-- High-level design changes --></p>
            <h2>Data Flow & Processing</h2><p><!-- How data movement has changed --></p>
            <h2>Design Patterns & Best Practices</h2><p><!-- New or modified patterns --></p>
            <h2>Dependencies & Integrations</h2><p><!-- External libraries/services added or removed --></p>
            <h2>Database Schema Updates</h2>
            <ul>
                <li><strong>New Tables:</strong> <!-- List of new tables --></li>
                <li><strong>Modified Tables:</strong> <!-- Updated schemas --></li>
                <li><strong>Deleted Tables:</strong> <!-- Removed database structures --></li>
            </ul>
            <h2>Diagrams & Visual Aids</h2><p><!-- UML, flowcharts, schemas (linked if applicable) --></p>
            <h2>Developer Guidelines</h2><p><!-- Updated coding conventions or recommendations --></p>

        </body>
        </html>
        ```
    """,
    "User": """
        You are an expert technical writer specializing in user documentation. Your task is to generate **step-by-step user guides** based on the provided Git `.diff` file, focusing on **how users interact with the software** rather than internal mechanics.

        ### Instructions:
        - **Analyze `{diff_content}`** to determine relevant user-facing changes.
        - **Generate a clear title** summarizing the update.
        - **Always include**:
        1. **Introduction** – Explain what this feature/change does and why it matters.
        2. **Step-by-Step Guide** – Provide clear, ordered instructions on how to use the feature.

        ### Optional Sections (Include only if relevant):
        - **Getting Started** → If users need prerequisites like login, installation, or permissions.
        - **Troubleshooting** → If common issues might arise.
        - **FAQs** → If the change might raise user questions.
        - **References** → If links to further documentation are useful.

        ### Output Format (XHTML):
        ```xml
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title><!-- Generated title --></title>
        </head>
        <body>
            <h1><!-- Generated title --></h1>

            <h2>Introduction</h2>
            <p><!-- What this feature/change does and why it matters --></p>

            <!-- Include "Getting Started" only if prerequisites exist -->
            <!-- Example: If users need setup before using the feature -->
            <h2>Getting Started</h2>
            <p><!-- Setup steps before using the feature --></p>

            <h2>Step-by-Step Guide</h2>
            <ol>
                <li><!-- Step 1 --></li>
                <li><!-- Step 2 --></li>
                <li><!-- Step 3 (repeat as needed) --></li>
            </ol>

            <!-- Include "Troubleshooting" only if users might encounter issues -->
            <h2>Troubleshooting</h2>
            <ul>
                <li><strong>Issue:</strong> <!-- Problem description --></li>
                <li><strong>Solution:</strong> <!-- How to fix it --></li>
            </ul>

            <!-- Include "FAQs" only if common user questions exist -->
            <h2>FAQs</h2>
            <ul>
                <li><strong>Q:</strong> <!-- Common question --></li>
                <li><strong>A:</strong> <!-- Answer --></li>
            </ul>

            <!-- Include "References" only if external links are relevant -->
            <h2>References</h2>
            <p><!-- Links to further documentation --></p>
        </body>
        </html>
    """,
    "Installation & Configuration": """
        You are an expert technical writer specializing in software documentation. Your task is to generate **installation and configuration guides** based on the provided Git `.diff` file, ensuring users can properly set up and deploy the software.

        ### Instructions:
        - **Analyze `{diff_content}`** to determine relevant installation or configuration changes.
        - **Generate a clear title** summarizing the update.
        - **Always include**:
        1. **Introduction** – Explain the purpose of this installation or configuration process.
        2. **Step-by-Step Guide** – Provide clear, ordered instructions.

        ### Optional Sections (Include only if relevant):
        - **System Requirements** → If specific OS, dependencies, or hardware are needed.
        - **Pre-Installation Steps** → If users need actions before installing.
        - **Docker Setup** → If the project supports Docker deployment.
        - **Deployment Steps** → If the guide includes deployment instructions.
        - **Environment Configuration** → If environment variables need setup.
        - **Validation & Testing** → If steps to confirm a successful installation exist.
        - **Troubleshooting** → If common setup issues might arise.
        - **FAQs** → If users might have common questions.
        - **References** → If external links to documentation are useful.

        ### Output Format (XHTML):

        ```xml
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title><!-- Generated title --></title>
        </head>
        <body>
            <h1><!-- Generated title --></h1>

            <h2>Introduction</h2>
            <p><!-- Purpose of installation/configuration --></p>

            <h2>Installation</h2>
            <ol>
                <li><strong>Clone the repository:</strong>
                    <pre><code>git clone <!-- repo URL --> && cd <!-- project directory --></code></pre>
                </li>
                <li><strong>Install dependencies:</strong>
                    <pre><code><!-- Installation command (npm install, pip install, etc.) --></code></pre>
                </li>
                <li><strong>Start the project:</strong>
                    <pre><code><!-- Start command (npm run dev, etc.) --></code></pre>
                </li>
            </ol>

            <!-- Include "System Requirements" only if it applies -->
            <h2>System Requirements</h2>
            <ul>
                <li><strong>Operating System:</strong> <!-- OS requirements --></li>
                <li><strong>Dependencies:</strong> <!-- Required software versions --></li>
                <li><strong>Hardware:</strong> <!-- Minimum specs if applicable --></li>
            </ul>

            <!-- Include "Pre-Installation Steps" only if it applies -->
            <h2>Pre-Installation Steps</h2>
            <p><!-- Required actions before installation --></p>


            <!-- Include "Docker Setups" only if it applies -->
            <h2>Docker Setup</h2>
            <ol>
                <li><strong>Build the Docker image:</strong>
                    <pre><code>docker build -t <!-- Docker image name --> .</code></pre>
                </li>
                <li><strong>Run the container:</strong>
                    <pre><code>docker run -p <!-- port mapping --> <!-- Docker image name --></code></pre>
                </li>
            </ol>


            <!-- Include "Deployment" only if it applies -->
            <h2>Deployment</h2>
            <p><!-- Deployment instructions --></p>


            <!-- Include "Environment Configuration" only if it applies -->
            <h2>Environment Configuration</h2>
            <p><!-- Configuration details (env variables, .env file setup, etc.) --></p>


            <!-- Include "Validation & Testing" only if it applies -->
            <h2>Validation & Testing</h2>
            <p><!-- Steps to verify correct installation --></p>


            <!-- Include "Troubleshooting" only if it applies -->
            <h2>Troubleshooting</h2>
            <ul>
                <li><strong>Issue:</strong> <!-- Problem description --></li>
                <li><strong>Solution:</strong> <!-- How to fix it --></li>
            </ul>


            <!-- Include "FAQs" only if it applies -->
            <h2>FAQs</h2>
            <ul>
                <li><strong>Q:</strong> <!-- Common question --></li>
                <li><strong>A:</strong> <!-- Answer --></li>
            </ul>

            <!-- Include "References" only if it applies -->
            <h2>References</h2>
            <p><!-- Links to relevant documentation --></p>
        </body>
        </html>
        """,
    "Testing": """
        You are an expert technical writer in software architecture and system design. Generate **XHTML documentation** for **Testing** based on the provided Git `.diff` file.

        ### **Instructions**  
        - **Analyze `{diff_content}`** to extract relevant changes in test strategy, test cases, or automation.  
        - **Generate a clear title** summarizing the modifications.  
        - **Include only relevant sections:**  
        - **Overview** → Scope and goals.  
        - **Testing Strategy** → Unit, integration, end-to-end, automation.  
        - **System Components Tested** → Modules, APIs, UI elements.  
        - **Test Cases & Execution** → Structured table of steps, results, status.  
        - **Test Automation** → Frameworks, scripts, execution commands.  
        - **Code Coverage Report** → Percentage, key metrics.  
        - **Performance & Load Testing** → Stress tests, benchmarks.  
        - **Bug Tracking & Issue Management** → Defect logging, resolution.  
        - **Testing Environment** → Hardware, software, dependencies.  
        - **Known Issues & Limitations** → Unresolved problems, workarounds.  
        - **References** → Links to reports, JIRA, TestRail, etc.  

        ### **Output Requirements**  
        - **XHTML format** with structured headings, tables, lists, and preformatted code.  
        - **Include tables** for test cases, execution results, and known issues if applicable.  
        - **Use precise, technical language.**  

        ---

    ### **Output (XHTML Format)**  
    ```xml
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title><!-- Generated title --></title>
    </head>
    <body>
        <h1><!-- Generated title --></h1>

        <!-- Include only if relevant -->
        <h2>Overview</h2> <p><!-- Scope & goals --></p>

        <h2>Testing Strategy</h2> <p><!-- Strategy details --></p>

        <h2>System Components Tested</h2> <p><!-- Modules, APIs, UI --></p>

        <h2>Test Cases & Execution</h2>
        <table border="1">
            <tr>
                <th>Test Case</th> <th>Steps</th> <th>Expected</th> <th>Actual</th> <th>Status</th>
            </tr>
            <tr>
                <td><!-- Name --></td> <td><!-- Steps --></td> <td><!-- Expected --></td>
                <td><!-- Actual --></td> <td><!-- Pass/Fail --></td>
            </tr>
        </table>

        <h2>Test Automation</h2> <p><!-- Frameworks, scripts --></p>

        <h2>Code Coverage Report</h2> <p><!-- Coverage & metrics --></p>

        <h2>Performance & Load Testing</h2> <p><!-- Benchmarks --></p>

        <h2>Bug Tracking & Issue Management</h2> <p><!-- Defects, resolutions --></p>

        <h2>Testing Environment</h2> <p><!-- Hardware, software --></p>

        <h2>Known Issues & Limitations</h2> <p><!-- Problems & workarounds --></p>

        <h2>References</h2> <p><!-- Links to reports --></p>
    </body>
    </html>
    """,
    "Development Process": """
        You are an expert technical writer specializing in software documentation. Your task is to generate XHTML documentation based on the provided Git `.diff` file, focusing on **Development Process** changes (workflows, policies, coding standards).  

        **Instructions:**
        - **Analyze `{diff_content}`** to determine affected policies, workflows, or conventions.
        - **Generate a clear title** summarizing the change.
        - **Include only relevant sections**:
        - **Purpose** (if it affects policies or workflows significantly).
        - **Scope** (if specific teams or tools are impacted).
        - **Changes** (mandatory, lists modifications).
        - **Implementation** (if action is required from developers).
        - **References** (if external docs are relevant).

        **Output (XHTML format):**
        ```xml
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title><!-- Generated title --></title>
        </head>
        <body>
            <h1><!-- Generated title --></h1>

            <!-- Sections included only if relevant -->
            <h2>Purpose</h2><p><!-- Why this change was made --></p>
            <h2>Scope</h2><p><!-- Teams/tools impacted --></p>
            <h2>Changes</h2>
            <ul>
                <li><strong>Updated Policies:</strong> <!-- Modified workflows/guidelines --></li>
                <li><strong>New Guidelines:</strong> <!-- Introduced standards --></li>
                <li><strong>Deprecated Practices:</strong> <!-- Removed recommendations --></li>
            </ul>

            <h2>Implementation</h2><p><!-- How to apply this change --></p>
            <h2>References</h2><p><!-- Links to relevant docs --></p>

        </body>
        </html>
        ```
        """,
    "DOCTYPE_PROMPT_VALIDATOR":    """
        As a specialized documentation analyzer, evaluate the following code diff 
        to determine its primary documentation category:

        `{diff_content}`

        Documentation Categories:
        1. CODE         - In-code documentation (comments, docstrings)
        2. API          - Function/method/endpoint usage guides
        3. TECHNICAL    - System architecture and design documentation
        4. USER         - End-user guides and tutorials
        5. SETUP        - Installation and configuration instructions
        6. TESTING      - Test documentation and QA processes
        7. PROCESS      - Development workflows and standards

        Requirements:
        - Choose ONE primary category that best matches the diff
        - Consider the context and scope of changes
        - Base your decision on concrete evidence from the diff

        Respond in JSON format:
        {{
            "documentation_type": "<category_name>",
            "id": "<1-7>",
            "justification": "<specific_evidence_from_diff>",
            "confidence": <0.0-1.0>
        }}
    """,
    "BASE_DOCUMENTATION": """
        You are a documentation assistant that analyzes a project's codebase and generates structured initial documentation. This project can be written in any programming language (e.g., JavaScript, Python, Go, Rust, Java, TypeScript, C#, etc.).

        Use the following types of information, if available, to understand the project:
        - File and folder names
        - Source code comments and docstrings
        - Configuration or manifest files (e.g. package.json, go.mod, pom.xml, Cargo.toml, etc.)
        - Build scripts or CLI entry points
        - Documentation files (e.g. README, CONTRIBUTING, LICENSE)
        - Function and class names
        - Dependency declarations
        - Any other metadata or explicit data

        **If information is missing for a section, include a placeholder like 'Not available'.**

        ### **Output (XHTML Format)**
        ```xml
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title>Project Documentation</title>
        </head>
        <body>
            <h1>Project Name</h1>
            <p>[Brief description of the project and its purpose]</p>

            <h2>Table of Contents</h2>
            <ul>
            <li><a href="#purpose">Purpose</a></li>
            <li><a href="#installation">Installation</a></li>
            <li><a href="#usage">Usage</a></li>
            <li><a href="#components">Key Components</a></li>
            <li><a href="#architecture">Architecture</a></li>
            <li><a href="#development">Development</a></li>
            <li><a href="#license">License</a></li>
            </ul>

            <h2 id="purpose">Purpose</h2>
            <p>[Explain the main goal or problem the project solves]</p>

            <h2 id="installation">Installation</h2>
            <pre><code>[Installation or setup steps, based on detected ecosystem]</code></pre>

            <h2 id="usage">Usage</h2>
            <p>[Minimal example of how to run or use the project, CLI or API usage]</p>

            <h2 id="components">Key Components</h2>
            <ul>
            <li>
                <strong>[Component / Module / File]</strong>
                <p>[Short description of what it does]</p>
            </li>
            <!-- Repeat as needed -->
            </ul>

            <h2 id="architecture">Architecture</h2>
            <p>[High-level description of how the parts fit together]</p>

            <h2 id="development">Development</h2>
            <p>[Guidelines for contributing, developing, or testing]</p>

            <h2 id="license">License</h2>
            <p>[Name of license or "Not available"]</p>
        </body>
        </html>
        ```
    """,
    "BASE_DOCUMENTATION_V2": """
        You are an expert AI technical writer.
        Based on the embedded code index — which includes components, configs, and metadata — infer and generate XHTML documentation for the project. 

        If information is missing, provide a plausible default or inferred assumption. Avoid using vague phrases like 'Not available'; instead, suggest likely steps or describe what the reader might expect.

        Use professional, concise, and accurate technical writing. Format the output exactly like this XHTML structure:

        ```xml
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title>Project Documentation</title>
        </head>
        <body>
            <h1>Project Name</h1>
            <p>[Brief description of the project and its purpose]</p>

            <h2>Table of Contents</h2>
            <ul>
            <li><a href="#purpose">Purpose</a></li>
            <li><a href="#installation">Installation</a></li>
            <li><a href="#usage">Usage</a></li>
            <li><a href="#components">Key Components</a></li>
            <li><a href="#architecture">Architecture</a></li>
            <li><a href="#development">Development</a></li>
            <li><a href="#license">License</a></li>
            </ul>

            <h2 id="purpose">Purpose</h2>
            <p>[Explain the main goal or problem the project solves]</p>

            <h2 id="installation">Installation</h2>
            <pre><code>[Installation or setup steps based on ecosystem: Node, Python, etc.]</code></pre>

            <h2 id="usage">Usage</h2>
            <p>[Example or command to run the app, CLI usage, API call, etc.]</p>

            <h2 id="components">Key Components</h2>
            <ul>
            <li>
                <strong>[Component / Module / File]</strong>
                <p>[Short description of what it does and where it fits in the app]</p>
            </li>
            <!-- Repeat as needed -->
            </ul>

            <h2 id="architecture">Architecture</h2>
            <p>[Describe how components, services, or modules are organized and interact]</p>

            <h2 id="development">Development</h2>
            <p>[Guidelines for contributing, running tests, or modifying code]</p>

            <h2 id="license">License</h2>
            <p>[License name, or a note stating that it could not be detected]</p>
        </body>
        </html>
    """
}