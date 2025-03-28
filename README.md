# Open LLM Prototype

Automated Documentation Update in Confluence
This project automates the process of detecting code changes in a GitHub repository and updating the corresponding documentation in Confluence.

How It Works:
Detect Code Changes → The system uses git diff to track modifications in the latest commit.

Generate Documentation → If required, the system extracts relevant information from the code changes and formats it into an XHTML file.

Publish to Confluence → A GitHub Actions workflow runs upon merging code into a specific branch (e.g., develop or main), triggering a Python script that updates Confluence via its API.

Automation via GitHub Actions → The workflow handles dependency installation, documentation generation, and the publishing process seamlessly.

Tech Stack:
GitHub Actions → Automates the workflow.

Python → Processes Git changes and interacts with the Confluence API.

XHTML → Standardized format for documentation.

Confluence API → Updates or creates documentation pages dynamically.

This setup ensures that documentation stays up to date with minimal manual effort, improving developer efficiency and project maintainability.

## Project Structure

- `.github/workflows/update_docs.yml`: GitHub Actions workflow for automating the documentation generation and publishing process.
- `src/scripts/get_diff.py`: Script to generate a diff file from the latest Git commits.
- `src/doctype_diff_validator.py/doctype_diff_validator.py`: Validates the diff file to classify the changes on six types of docs:
    1. **Code**: Documentation within the code, including inline comments and docstrings.
    2. **API**: Guides on how to use functions, methods, and API endpoints. Often generated using tools like Swagger/OpenAPI, JSDoc, or Sphinx.
    3. **Technical**: Describes system architecture, data flows, design patterns, and dependencies.
    4. **User**: Provides step-by-step guides, tutorials, or user manuals on how to use the software.
    5. **Installation & Configuration**: Covers setup instructions, deployment steps, and environment configurations.
    6. **Testing**: Documents test cases, testing strategies (unit, integration, end-to-end), and quality assurance processes.
    7. **Development Process**: Explains methodologies, Git workflows, Definition of Done, PR policies, code conventions, style guides, and quality standards.

- `src/scripts/gh_test_request.py`: Script to generate documentation using GPT-4 based on the diff file.
- `src/scripts/create_confluence_doc.py`: Script to publish the generated documentation to Confluence.

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/open-llm-prototype.git
   cd open-llm-prototype
   ```

2. **Install dependencies:**
   ```sh
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory and add the following variables:
   ```env
   MY_EMAIL=your-email@example.com
   CONFLUENCE_API_TOKEN=your-confluence-api-token
   CONFLUENCE_SPACE_KEY=your-confluence-space-key
   GH_GPT4_API_KEY=your-gpt4-api-key
   ```

## Usage

ALWAYS MERGE THE WITH GIT SQUASH STRATEGY

### Running the Workflow Locally

1. **Generate the diff file:**
   ```sh
   python src/scripts/get_diff.py
   ```

2. **Validate documentation using GPT-4**
   ```sh
   python src/doctype_diff_validator/doctype_diff_validator.py
   ```

2. **Generate documentation on XHTML using GPT-4:**
   ```sh
   python src/xhtml_generator/xhtml_generator.py
   ```

3. **Publish documentation to Confluence:**
   ```sh
   python src/scripts/create_confluence_doc.py
   ```

## Running yml GitHub Actions workflow locally

1. **Install act**

   *On Mac or Linux*

   ```sh
   brew install act
   ```
   or

   ```sh
   curl -s https://raw.githubusercontent.com/nektos/act/main/install.sh | sudo bash
   ```

   *On Windows*

   ```sh
   scoop install act
   ```

2. **Install Docker** #TODO: UPDATE DOCS...

   *On Mac or Linux*
   Install Docker using brew

   ```sh
      brew install --cask docker
   ```

   Then open Docker from LAunchPad or

   ```sh
      open /Applications/Docker.app
   ```

   *On Windows*

   ```sh
   winget install --id Docker.DockerDesktop -e
   ```

   *Verify docker version*

   ```sh
      docker --version
   ```

3. **Run yml file locally**

   Open Docker Desktop

   Copy your .env file with local env variables in a .secrets file to simulate Github actions enviroment secrets
   ```sh
      cp .env .secrets
   ```

   This simulates the Github Workflow locally
   ```sh
   act pull_request -e event.json --secret-file .secrets
   ```


### Running the Workflow on GitHub Actions

The workflow is triggered on every pull request merged to the `main` branch. It performs the following steps:
1. Checks out the code.
2. Sets up Python.
3. Installs dependencies.
4. Generates the diff file.
5. Generates documentation using GPT-4.
6. Publishes the documentation to Confluence.

## Contributing

Feel free to open issues or submit pull requests if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License.

