from tree_sitter import Language

Language.build_library(
    "/home/zewen/test-3/demo/java_analysis/lib/language_parser.so",
    [
        'lib/tree-sitter-go',  # git clone https://github.com/tree-sitter/tree-sitter-go
        'lib/tree-sitter-javascript',
        'lib/tree-sitter-python',
        'lib/tree-sitter-cpp',
        'lib/tree-sitter-java',
    ]
)