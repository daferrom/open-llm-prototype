from pathlib import Path
from tree_sitter import Parser
from tree_sitter_language_pack import get_parser
from llama_index.core.node_parser import CodeSplitter

def get_parser_for_language(language: str) -> Parser:
    """Returns a configured parser for a programming language tree-sitter-language-pack."""
    try:
        parser = get_parser(language)
        return parser
    except Exception as e:
        print(f"❌ The parser couldn't be obtained for {language}: {e}")
        return None

def split_docs_by_prog_lang(documents):
    all_nodes =[]
    omitted_docs_per_file_type = 0
    omitted_parsers = 0
    for doc in documents:

        # language = doc.metadata.get("file_type", None)
        file_extension = Path(doc.metadata['file_path']).suffix.lower()

        # Cleaning dot of string
        language = file_extension.lstrip('.')
        # print("Extension without dot", ext)

        if not language:
            print(f"⚠️ Document {language} without 'file_type', omitted ⏭️")
            continue

        print(f"🧩 Splitting DOC : {doc.metadata.get('file_path')} as {language}...")

        # For allowing parser for typescript files with tsx parser 
        # TODO: This is a temp fix it should be handled better the equivalent parser names
        if language == "ts":
            language = "tsx"
        if language == "md":
            language = "markdown"

        parser_by_doc_ext = get_parser_for_language(language)

        if not parser_by_doc_ext:
            print(f"⚠️  Parser not available for {language}, Parser ommited. ⏭️")
            omitted_parsers = omitted_parsers + 1
            continue

        print("✂️ Splitting code in fragments...")
        splitter = CodeSplitter(parser=parser_by_doc_ext, language=language, chunk_lines=100)
        split_nodes = splitter.get_nodes_from_documents([doc])
        all_nodes.extend(split_nodes)

    print("ommited docs per type", omitted_docs_per_file_type)
    print("ommitted_parsers", omitted_parsers)
    return all_nodes


if __name__ == "__main__":
    print("...Code splitter run")