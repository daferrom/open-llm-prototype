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
    """,
    "GENERAL_DOCUMENTATION" : """
        Act as a AI senior software engineer technical writer.

        Based on the embedded code index — which includes components, configs, and metadata — infer and generate XHTML professional technical overview of the project for the project.

        If information is missing, provide a plausible default or inferred assumption. Avoid using vague phrases like 'Not available'; instead, suggest likely steps or describe what the reader might expect.


        Format the output following this XHTML structure:

        ### **Output (XHTML Format)**
        ```xml
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title>[Project Documentation name]</title>
        </head>
        <body>
            <h1>Project Name</h1>
            <p>[Brief description of the project and its purpose]</p>

            <h2>Table of Contents</h2>
            <ul>
                <li><a href="#general-purpose">General Purpose</a></li>
                <li><a href="#problem-or-need">Problem or Need</a></li>
                <li><a href="#target-audience">Target Audience </li>
                <li><a href="#main-functionality">Main Functionality</a></li>
                <li><a href="#components">Key Components</a></li>
                <li><a href="#architecture">Architecture</a></li>
                <li><a href="#technologies-used"> Technologies used </a></li>
                <li><a href="#basic-usage-flow"> Basic usage flow </a></li>
                <li><a href="#development">Development</a></li>
                <li><a href="#license">License</a></li>
            </ul>

            <h2 id="general-purpose">General purpose</h2>
                <p>[What does this project do?]</p>

            <h2 id="problem">Problem or Need</h2>
            <p>[What problem does it solve?]</p>

            <h2 id="main-functionality"> Main functionality </h2>
                <p>[Summarize the key features or components]</p>

            <h2 id="target-audience"> Target Audience</h2>
                <p>[Who should use this system?s]</p>

            <h2 id="components">Key Components </h2>
                <ul>
                    <li>
                        <strong>[Component / Module / File]</strong>
                        <p>[Short description of what it does and where it fits in the app]</p>
                    </li>
                    <!-- Repeat as needed -->
                </ul>
            <h2 id="architecture"> Architecture </h2>
                <p>[Describe how components, services, or modules are organized and interact]</p>

            <h2 id="technologies-used"> Technologies used </h2>
                <ul>
                    [List programming languages, frameworks, key libraries.]
                    <li>
                        <strong>[Technology (programming languages, framework and/or key libraries)]</strong>
                        <p>[Short description of what it does in the app]</p>
                    </li>
                    <!-- Repeat as needed -->
                </ul>

            <h2 id="basic-usage-flow"> Basic Usage Flow </h2>
                <p>[Briefly describe how the system or one of its main features is used.]</p>
                    <ul>
                        [List each one of the commmand if applies]
                        <li>
                            <p>[Briefly explanation of what the command does]<p>
                            <pre><code>[Example(s) or command(s) to run the app, CLI usage, API call, etc.]</code></pre>
                        </li>
                        <!-- Repeat as needed -->
                    </ul>

            <h2 id="installation-setup">Set-up / installation</h2>
                <p>[Briefly explanation of the setup process and/or installation]<p>
                    <ul>
                        <li>
                            <p>[Briefly explanation of what the command does]<p>
                            <pre><code>[Installation or setup steps based on ecosystem: Node, Python, etc.]</code></pre>
                        </li>
                        <!-- Repeat as needed -->
                    </ul>
            <h2 id="development">Development</h2>
                <p>[Guidelines for contributing, running tests, or modifying code]</p>

            <h2 id="license">License</h2>
                <p>[License name, or a note stating that it could not be detected]</p>
        </body>
        </html>
        ```
    """,
}




doc_from_code_template_prompts = {
    "CODE_DOCS_OVERVIEW": """
            You are an expert technical writer specializing in software documentation. Your task is to generate the main **Code Documentation Overview Page** in XHTML format based on the provided embedded code index. This page introduces the system, its modules, and structure.

            **Instructions:**
            - **Analyze `{code_index}`** to understand the high-level architecture and main areas of functionality.
            - **Generate a clear and informative title** for the documentation home page.
            - **Describe the project as a whole**, including:
                - What it does
                - Its main modules or components
                - How it's organized (folders, layers, domains)
                - What technologies it uses (if evident)
            - **This is not about code changes**, but about giving a first-time reader context and structure.

            **Output (XHTML format):**
            ```xml
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <title><!-- Documentation Home Title --></title>
            </head>
            <body>
                <h1><!-- Documentation Home Title --></h1>

                <h2>Project Overview</h2>
                <p><!-- What this system is and what it does --></p>

                <h2>Modules and Structure</h2>
                <p><!-- High-level description of modules and code structure --></p>

                <h2>Technologies and Tools</h2>
                <p><!-- Mention of frameworks, libraries, or languages used --></p>

                <h2>Navigation Guide</h2>
                <p><!-- Links or descriptions of where to go next in the documentation (e.g., components, APIs, setup) --></p>

            </body>
            </html>
    """,
    "API_DOCS_OVERVIEW": """
            You are a technical writer specialized in API documentation.
            Your task is to generate the **main index page for the API documentation**, using the information retrieved from this index.
            If information is missing, provide a plausible default or inferred assumption. Avoid using vague phrases like 'Not available'; instead, suggest likely steps or describe what the reader might expect.

            ---

            **Instructions**:
            - Retrieve all available **API modules**, sections, or services described in the codebase.
            - For each one, extract:
            - A clear title (e.g., "User Management API")
            - An optional short description (from docblocks or headings)
            - A normalized filename link (e.g., `user-management.html`)
            - Organize them in a simple HTML/XHTML page that serves as the **table of contents**.
            - ** Your response will be only and exclusively in the OUTPUT format on XHTML nothing more.

            ---

            **Output format** (XHTML 1.0 Strict):
            ```xml
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                    <title>API Documentation Index</title>
                </head>
                <body>
                    <h1>API Documentation</h1>

                    <h2>Overview</h2>
                    <p>This page lists all available API modules discovered from the embedded code documentation. Each section links to its detailed reference.</p>

                    <h2>API Modules</h2>
                    <ul>
                        <!-- Repeat this block per module discovered -->
                        <li>
                            <strong><a href="{normalized-filename}.html">{Module Title}</a></strong><br/>
                            <em>{Optional one-line description}</em>
                        </li>
                        <!-- End repeat -->
                    </ul>
                </body>
                </html>
            ```
        """,
    "TECHNICAL_DOCS_OVERVIEW": """

            You are a technical writer specializing in system architecture and design documentation. Your task is to generate **Technical Documentation** based on the embedded code index — which includes components, configs, and metadata — infer and generate XHTML professional technical overview for the project.

            If information is missing, provide a plausible default or inferred assumption. Avoid using vague phrases like 'Not available'; instead, suggest likely steps or describe what the reader might expect.
            ---

            **Instructions**:
            - Retrieve information from the embedded index about:
                - **System Architecture** (e.g., key components, high-level design, interactions)
                - **Data Flows** (e.g., how data moves across the system, pipelines)
                - **Design Patterns** (e.g., Singleton, Factory, MVC, etc.)
                - **Dependencies** (e.g., libraries, tools, platforms)
                - **UML Diagrams** (or references to UML diagram files)
                - **Database Schemas** (or references to schema diagrams)
                - **Developer Guides** (e.g., how to set up, best practices)
                - 

            - Organize this information into a structured XHTML page, providing a clear overview with internal links to sub-sections for each category.

            ---
            **Output format** (XHTML 1.0 Strict):
                ```xml
                    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
                    <html xmlns="http://www.w3.org/1999/xhtml">
                        <head>
                            <title>Technical Documentation</title>
                        </head>
                            <body>
                                <h1>Technical Documentation</h1>

                                <h2>Overview</h2>
                                <p>This document provides an overview of the architecture, design patterns, data flows, and dependencies in the system.</p>

                                <h2>System Architecture</h2>
                                <p>{System Architecture Overview}</p>
                                <h3>Key Components</h3>
                                <ul>
                                    <!-- List major components or services -->
                                    <li>{Component Name}: {Short Description}</li>
                                    <!-- Repeat for each component -->
                                </ul>

                                <h2>Data Flows</h2>
                                <p>{Overview of data flows in the system, how data is processed and moved between components}</p>

                                <h2>Design Patterns</h2>
                                <p>{Overview of design patterns implemented in the system (e.g., Singleton, Factory, MVC, etc.)}</p>
                                <ul>
                                    <!-- List design patterns -->
                                    <li>{Design Pattern Name}: {Brief Description}</li>
                                    <!-- Repeat for each pattern -->
                                </ul>

                                <h2>Dependencies</h2>
                                <p>{List of critical dependencies, libraries, platforms, etc.}</p>
                                <ul>
                                    <!-- List dependencies -->
                                    <li>{Dependency Name}: {Description}</li>
                                    <!-- Repeat for each dependency -->
                                </ul>

                                <h2>UML Diagrams</h2>
                                <p>{References to UML diagrams or embedded diagrams}</p>

                                <h2>Database Schemas</h2>
                                <p>{References or images of database schemas, ER diagrams, etc.}</p>

                                <h2>Developer Guide</h2>
                                <p>{Overview of development setup, guidelines, and best practices}</p>
                            </body>
                    </html>
                ```
            """,
    "USER_DOCS_OVERVIEW": """
                You are a technical writer specializing in creating **User Documentation**. Your task is to generate user-friendly guides and tutorials based on the embedded code index — which includes components, configs, and metadata — infer and generate XHTML professional user overview for the project.

                Your focus should be on how to guide users to effectively use it.

                If information is missing, provide a plausible default or inferred assumption. Avoid using vague phrases like 'Not available'; instead, suggest likely steps or describe what the reader might expect.

                ---

                **Instructions**:
                - Retrieve or infer information from the embedded index about:
                    - **Step-by-Step Guides** (instructions on how to perform specific tasks within the software)
                    - **Tutorials** (more in-depth, task-focused walkthroughs)
                    - **User Manual** (comprehensive document detailing the software's functionality, including sections for different user needs)
                    - **Screenshots or Illustrations** (if available, embed or link to relevant images or diagrams)
                    - ** Your response will be only and exclusively in the OUTput format on XHTML nothing else.

                - Organize this information into a user-friendly, easy-to-read HTML page with clear instructions, links to additional resources, and visual aids.

                ---

                ### **Output (XHTML Format)**
                ```xml
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                    <title>User Documentation</title>
                </head>
                <body>
                    <h1>User Documentation</h1>

                    <h2>Overview</h2>
                    <p>This document serves as the main guide to help you use the software efficiently and get the most out of its features.</p>

                    <h2>Getting Started</h2>
                    <p>Here is a brief introduction to the software and how to set it up for the first time.</p>

                    <h3>Installation</h3>
                    <p>{Installation Instructions}</p>

                    <h3>Initial Setup</h3>
                    <p>{Step-by-step guide to initial configuration or setup process}</p>

                    <h2>Step-by-Step Guides</h2>
                    <p>{Detailed, easy-to-follow instructions on how to complete common tasks or features of the software}</p>
                    <ul>
                        <!-- List common tasks -->
                        <li><a href="#task1">{Task 1 Name}</a></li>
                        <li><a href="#task2">{Task 2 Name}</a></li>
                        <!-- Repeat for each task -->
                    </ul>

                    <h2>Tutorials</h2>
                    <p>{More in-depth tutorials for specific user scenarios or workflows. Explain how to achieve specific outcomes using the software.}</p>

                    <h3>{Tutorial Title 1}</h3>
                    <p>{Detailed instructions for the tutorial}</p>

                    <h3>{Tutorial Title 2}</h3>
                    <p>{Detailed instructions for the tutorial}</p>

                    <h2>User Manual</h2>
                    <p>This section contains the full user manual for the software, including all features,
            """,
    "INSTALLATION_AND_CONFIGURATION_OVERVIEW": """
            You are a technical writer focused on developer experience. Your task is to generate **Installation & Configuration Documentation** based on the embedded code index.

            This documentation is intended to help new developers or DevOps engineers set up the development environment and configure the application.

            If information is missing, provide a plausible default or inferred assumption. Avoid using vague phrases like 'Not available'; instead, suggest likely steps or describe what the reader might expect.

            ---

            **Instructions**:
            - Extract relevant installation and configuration steps from the embedded index.
            - Include details on:
                - Project setup (cloning, dependency installation, scripts)
                - Required environment variables
                - Configuration files (e.g., `.env`, `config.yaml`)
                - Docker setup (Dockerfiles, docker-compose)
                - Deployment instructions (for staging, production, etc.)
                - Your response will be only and exclusively in the OUTput format on XHTML nothing else.

            - Format the documentation in valid XHTML for structured internal documentation.

            ---

            **Output format** (XHTML 1.0 Strict):
            ```xml
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                    <title>Installation & Configuration</title>
                </head>
                <body>
                    <h1>Installation & Configuration</h1>

                    <h2>Clone the Repository</h2>
                    <p>Use the following command to clone the project:</p>
                    <pre><code>git clone https://github.com/your-org/your-project.git</code></pre>

                    <h2>Install Dependencies</h2>
                    <p>Install project dependencies:</p>
                    <pre><code>npm install</code></pre>

                    <h2>Environment Variables</h2>
                    <p>Set the following environment variables (typically stored in a `.env` file):</p>
                    <ul>
                        <li><code>API_URL=https://api.example.com</code></li>
                        <li><code>PORT=3000</code></li>
                        <li><code>NODE_ENV=development</code></li>
                    </ul>

                    <h2>Start the Project</h2>
                    <p>Run the development server:</p>
                    <pre><code>npm run dev</code></pre>

                    <h2>Docker Setup</h2>
                    <p>To run the project using Docker:</p>
                    <pre><code>docker-compose up --build</code></pre>

                    <h2>Deployment</h2>
                    <p>Follow these steps to deploy the application:</p>
                    <ol>
                        <li>Build the application: <code>npm run build</code></li>
                        <li>Start the production server: <code>npm start</code></li>
                        <li>Optional: Deploy using CI/CD or infrastructure-as-code tools</li>
                    </ol>

                </body>
                </html>
            ```
    """,
    "TESTING_DOCS_OVERVIEW": """
                You are a technical writer specializing in creating **Testing Documentation**. Your task is to generate comprehensive testing documentation based on based on the embedded code index.

                If information is missing, provide a plausible default or inferred assumption, Avoid using vague phrases like 'Not available'; instead make testing proposal for the embedded project according to the XHTML,mentioning that is is explicitly a proposal.
                ---

                **Instructions**:
                - Retrieve or infer information from the embedded index about:
                    - **Testing Strategies** (unit tests, integration tests, end-to-end tests)
                    - **Test Cases** (description of the various test cases, including the expected outcomes)
                    - **Code Coverage Reports** (if available, embed or link to coverage reports such as `jest --coverage`)
                    - **Test Management Tools** (links to TestRail, JIRA, or other tools used to manage and track tests)
                    - ** Your response will be exclusively in the OUTPUT format on XHTML nothing more. Any extra comment that you have can be included Notes section.

                - Organize this information into a structured, easy-to-read HTML page with sections clearly defined for each testing aspect.

                ---

                ### **Output (XHTML Format)**
                ```xml
                    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
                    <html xmlns="http://www.w3.org/1999/xhtml">
                    <head>
                        <title>Testing Documentation</title>
                    </head>
                    <body>
                        <h1>Testing Documentation</h1>

                        <h2>Overview</h2>
                        <p>This document outlines the testing strategies, test cases, and code coverage for the software project.</p>

                        <h2>Testing Strategies</h2>
                        <p>Here we describe the different strategies used to test the software, including unit tests, integration tests, and end-to-end tests.</p>

                        <h3>Unit Testing</h3>
                        <p>{Description of unit tests, framework used, and key test cases}</p>

                        <h3>Integration Testing</h3>
                        <p>{Description of integration tests, testing of interactions between components, and key test cases}</p>

                        <h3>End-to-End Testing</h3>
                        <p>{Description of end-to-end tests, testing of the full application workflow, and key test cases}</p>

                        <h2>Test Cases</h2>
                        <p>Here we describe the various test cases used in the software, the scenarios they cover, and their expected outcomes.</p>
                        <ul>
                            <li><b>Test Case 1:</b> {Test case description, including expected results}</li>
                            <li><b>Test Case 2:</b> {Test case description, including expected results}</li>
                            <!-- Repeat for each test case -->
                        </ul>

                        <h2>Code Coverage</h2>
                        <p>{Link to or description of the code coverage report, such as Jest's coverage output}</p>
                        <p>Coverage Report: <a href="{coverage_report_link}">View Coverage Report</a></p>

                        <h2>Test Management Tools</h2>
                        <p>This section contains links to the tools used for managing and tracking tests.</p>
                            <ul>
                                <li><a href="{TestRail_link}">TestRail</a> - Test case management tool</li>
                                <li><a href="{JIRA_link}">JIRA</a> - Issue and project tracking tool</li>
                                <!-- Add more tools if necessary -->
                            </ul>
                        <h2>Notes</h2>
                        <p>This section contains any extra information or consideration about the testing</p>
                    </body>
                    </html>
                ```
            """,
    "DEV_DOCS_PROCESS_OVERVIEW": """
                You are a technical writer specializing in software development methodologies and workflows. Your task is to generate **Development Process Documentation** based on the embedded code index

                If information is missing, provide a plausible default or inferred assumption. Avoid using vague phrases like 'Not available'; instead, suggest likely steps or describe what the reader might expect. And make the inferences to create the descriptions of the development lifecycle, version control strategies, code conventions, and team policies.

                ---

                **Instructions**:
                - Extract and organize information from the embedded index related to:
                - **Development Methodology** (Agile, Scrum, Kanban, etc.)
                - **Git Workflow** (Git Flow, trunk-based development, etc.)
                - **Definition of Done**
                - **Pull Request Policies**
                - **Code Conventions & Style Guides**
                - **Quality Standards** (e.g., linters, static analysis, CI/CD policies)

                - Format the documentation in structured XHTML, suitable for a centralized documentation hub.
                - ** Your response will be only and exclusively in the OUTPUT format on XHTML nothing else.

                ---

                **Output format** (XHTML 1.0 Strict):
                    ```xml
                        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
                        <html xmlns="http://www.w3.org/1999/xhtml">
                        <head>
                            <title>Development Process Documentation</title>
                        </head>
                        <body>
                            <h1>Development Process Documentation</h1>

                            <h2>Development Methodology</h2>
                            <p>{Describe the methodology in use (Agile, Scrum, etc.), including sprints, ceremonies, and team roles}</p>

                            <h2>Git Workflow</h2>
                            <p>{Explain the version control model used, e.g., Git Flow or trunk-based development. Include diagrams if necessary}</p>

                            <h2>Definition of Done</h2>
                            <p>{Clearly define what constitutes a completed task or feature. May include testing, documentation, review, and deployment}</p>

                            <h2>Pull Request Policies</h2>
                            <p>{Outline how PRs should be created, reviewed, and merged. Include approval requirements and CI checks}</p>

                            <h2>Code Conventions & Style Guides</h2>
                            <p>{List and describe the coding standards, style guides, linters, and formatting tools used in the project}</p>

                            <h2>Quality Standards</h2>
                            <p>{Define code quality requirements such as coverage thresholds, CI pipelines, code review requirements, and performance checks}</p>

                        </body>
                        </html>
                    ```
            """,
}
