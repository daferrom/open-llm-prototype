# Open LLM Prototype

Automated Documentation Update in Confluence using LLMs (Language Learning Models)
This project automates the process of detecting code changes in a GitHub repository and updating the corresponding documentation in Confluence using modern LLMs.

## How It Works

1. **Detect Code Changes** → The system uses git diff to track modifications in the latest commit.

2. **Validate Documentation Type** → Uses LLMs to analyze changes and classify into appropriate documentation categories:
   - Code documentation
   - API documentation
   - Technical documentation
   - User documentation
   - Installation & Configuration
   - Testing documentation
   - Development Process documentation

3. **Generate Documentation** → Uses LLMs (Qwen2.5, GPT-4) to generate XHTML documentation based on the detected changes.

4. **Vectorize & Index** → Utilizes LlamaIndex and ChromaDB to:
   - Create embeddings of existing documentation
   - Index content for semantic search
   - Enable intelligent document updating

5. **Publish to Confluence** → GitHub Actions workflow triggers documentation updates via Confluence API.

## Tech Stack

- **LLMs**: Qwen2.5-Coder-32B, GPT-4
- **Vector DB**: ChromaDB
- **Embeddings**: HuggingFace (BAAI/bge-small-en-v1.5)
- **Indexing**: LlamaIndex
- **CI/CD**: GitHub Actions
- **Documentation**: Confluence API
- **Languages**: Python
- **Observability**: Phoenix/OpenTelemetry

## Project Structure

```
src/
├── client_api_ai/          # LLM client configurations and prompt templates
├── config/                 # Application configuration
├── confluence_service/     # Confluence API integration
├── docs_loader/            # Documents loaders
├── docs_publisher_controller/  # Documentation publishing logic controller and decision making functions
├── doctype_diff_validator/    # Validates the type of documention that should be created according to the change
├── llama_idx_prototype/       # LlamaIndex integration first approach
├── prompts/                   # LLM prompt templates
├── scripts/                   # Utility scripts
├── utils/                     # Helper functions
└── xhtml_generator/          # XHTML document generation
diff.txt                      # Temporary files where the changes are written
summary.xhtml                 # The draft summary documentation generated saved in this file for publishing
api_ai_response.json          # This file is to save the validation of the documentatio ntype based on the changes
event.json                    # This files let "act" library to simulate a pull request merged and close on local
```

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/daferrom/open-llm-prototype.git
   cd open-llm-prototype
   ```

2. **Activate a virtual environment for python packages_
   ```sh
      source venv/bin/activate
   ```

2. **Install dependencies:**
   ```sh
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   Create a `.env` file with:
   ```env
   MY_EMAIL=your-email@example.com
   CONFLUENCE_API_TOKEN=your-confluence-api-token          # Get from: https://id.atlassian.com/manage-profile/security/api-tokens
   CONFLUENCE_SPACE_KEY=your-confluence-space-key         # Found in Confluence Space Settings
   GH_GPT4_API_KEY=your-gpt4-api-key                     # Get from: https://platform.openai.com/api-keys
   HF_API_TOKEN=your-huggingface-token                   # Get from: https://huggingface.co/settings/tokens
   PHOENIX_API_KEY=your-phoenix-api-key                  # Get from: https://phoenix.arize.com/settings/api-keys
   ```

## Usage

### Merging Strategy
We recommend always use squash stratategy merging to maintain clean git history.

### Local Development Workflow

1. **Generate diff file:**
   ```sh
   python src/scripts/get_diff.py
   ```

2. **Validate documentation type:**
   ```sh
   python src/doctype_diff_validator/doc_type_diff_validator_llama_idx.py
   ```

4. **Update Confluence:**
   ```sh
   python src/docs_publisher_controller/gen_doc_controller.py
   ```

### Testing GitHub Actions Locally

1. **Install act:**
   ```sh
   # macOS
   brew install act
   # Linux
   curl -s https://raw.githubusercontent.com/nektos/act/main/install.sh | sudo bash
   # Windows
   scoop install act
   ```

2. **Setup Docker:**
   ```sh
   # macOS
   brew install --cask docker
   # Windows
   winget install Docker.DockerDesktop
   ```

3. **Run workflow:**

    *** For diferences in the own CoDA repo ***

    This runs the [update_docs.yml](.github/workflows/update_docs.yml) as a GithubAction on your local.

    It simulates locally with the help of library "act" the  as a trigger pull-request or merge_request closed The event simulated is on this file [event.json](./event.json)
    More trigger events can be configured for the project requirements.

    For more info about githubActions check this : [update_docs.yml ](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions)

   ```sh
   cp .env .secrets
   act pull_request -e event.json --secret-file .secrets
   ```

   FOr M1 Architecture --container-architecture linux/amd64
   ```sh
   cp .env .secrets
   act pull_request -e event.json --secret-file .secrets
   ```

    Run to generate DOCs from zero
    #TODO: Required to  setup config docker container and image
    ```sh
    act push -e event_push_simulated.json --secret-file .secrets --container-architecture linux/amd64
    ```
### GitHub Actions Workflow

Triggered on PR merge to main, the workflow:
1. Checks out code
2. Configures Python
3. Installs dependencies
4. Generates diff
5. Validates documentation type
6. Generates documentation using LLMs
7. Updates Confluence

### To generate base documentation code from zero

Add the repo code folder on the folder src/code_repos/

Then run the command:

```sh
    python3 src/main_doc_creation.py
```
python3 src/chatbot_coda/chatbot_env_monitor_app.py

## Docs related

[https://developer.atlassian.com/cloud/confluence/rest/v2/intro/#about](Confluence API V2 Docs)
[https://huggingface.co/llamaindex] (Llama index docs)



## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## License

MIT License - see LICENSE file for details

## Contributors

- Diego Ferro
- Jhonatan Ascencio

