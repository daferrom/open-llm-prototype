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
├── docs_publisher_controller/  # Documentation publishing logic
├── doctype_diff_validator/    # Change type classification
├── llama_idx_prototype/       # LlamaIndex integration
├── prompts/                   # LLM prompt templates
├── scripts/                   # Utility scripts
├── utils/                     # Helper functions
└── xhtml_generator/          # XHTML document generation
```

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
   Create a `.env` file with:
   ```env
   MY_EMAIL=your-email@example.com
   CONFLUENCE_API_TOKEN=your-confluence-api-token
   CONFLUENCE_SPACE_KEY=your-confluence-space-key
   GH_GPT4_API_KEY=your-gpt4-api-key
   MY_HF_TOKEN=your-huggingface-token
   PHOENIX_API_KEY=your-phoenix-api-key
   ```

## Usage

### Merging Strategy
Always use squash merging to maintain clean git history.

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
   ```sh
   cp .env .secrets
   act pull_request -e event.json --secret-file .secrets
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

