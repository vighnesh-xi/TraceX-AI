from parsing.ast_parser import ASTParser
from parsing.doc_parser import DocParser
from parsing.config_parser import ConfigParser

def test_ast_parser_python():
    parser = ASTParser()
    file_info = {"content": "def hello():\n    pass\n", "relative_path": "test.py", "extension": ".py"}
    chunks = parser.parse(file_info)
    assert len(chunks) > 0
    assert any("hello" in c["name"] for c in chunks)

def test_doc_parser_markdown():
    parser = DocParser()
    file_info = {"content": "# Intro\nSome text\n## Section\nMore text", "relative_path": "readme.md", "extension": ".md"}
    chunks = parser.parse(file_info)
    assert len(chunks) > 0

def test_config_parser_yaml():
    parser = ConfigParser()
    file_info = {"content": "key: value\nport: 8080", "relative_path": "config.yaml", "extension": ".yaml"}
    chunks = parser.parse(file_info)
    assert chunks[0]["parsed"]["port"] == 8080