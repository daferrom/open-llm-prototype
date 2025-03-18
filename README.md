# Open LLM Prototype

This project is a prototype for automating the generation of documentation using GPT-4 and publishing it to Confluence. The workflow includes generating a diff file from the latest Git commits, summarizing the changes using GPT-4, and creating a Confluence page with the generated documentation.

## Project Structure

- `.github/workflows/update_docs.yml`: GitHub Actions workflow for automating the documentation generation and publishing process.
- `src/scripts/get_diff.py`: Script to generate a diff file from the latest Git commits.
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

### Running the Workflow Locally

1. **Generate the diff file:**
   ```sh
   python src/scripts/get_diff.py
   ```

2. **Generate documentation using GPT-4:**
   ```sh
   python src/scripts/gh_test_request.py
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

3. **Runr yml file locally**

   This simulates the Github Workflow locally
   ```sh
   act pull_request -e event.json --secret-file .secrets
   ```



### Running the Workflow on GitHub Actions

The workflow is triggered on every push to the `main` branch. It performs the following steps:
1. Checks out the code.
2. Sets up Python.
3. Installs dependencies.
4. Installs Asciidoctor.
5. Generates the diff file.
6. Generates documentation using GPT-4.
7. Publishes the documentation to Confluence.

## Contributing

Feel free to open issues or submit pull requests if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License.

