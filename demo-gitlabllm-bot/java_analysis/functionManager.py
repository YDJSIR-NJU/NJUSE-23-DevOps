from tree_sitter import Language, Parser
import re


class FunctionManager:
    def __init__(self, file, lib="/home/zewen/test-3/demo/java_analysis/lib/language_parser.so"):
        end = file.split('.')[-1]  # 通过后缀名判断语言
        if end == "js":
            self.lan = "javascript"
        elif end == "py":
            self.lan = "python"
        elif end == "java":
            self.lan = "java"
        elif end == "go":
            self.lan = "go"
        elif end in ["c", "cpp", "cc", "h", "hpp"]:
            self.lan = "cpp"
        else:
            raise ValueError("Unsupported code language.")

        self.parser = Parser()
        languages = {
            "go": Language(lib, "go"),
            "javascript": Language(lib, "javascript"),
            "python": Language(lib, "python"),
            "java": Language(lib, "java"),
            "cpp": Language(lib, "cpp"),
        }
        self.parser.set_language(languages[self.lan])

        with open(file, "rb") as f:
            self.tree = self.parser.parse(f.read())

        self.functions = []

        old_children = self.tree.root_node.children
        new_children = []

        while old_children:  # 层次遍历
            for child in old_children:
                if child.type in ["function_definition", "function_declaration", "method_declaration"]:
                    self.functions.append(((child.start_point[0], child.end_point[0]), child.text))
                if child.children:
                    new_children.extend(child.children)
            old_children = new_children
            new_children = []

    def get_function(self, diff):
        group = re.search("@@ -(\d+),(\d+) \+(\d+),(\d+) @@", diff)  # 从diff头获取行数

        if not group:
            raise ValueError("Diff head not matched!")

        start = int(group.group(3))
        offset = 2  # 上下文为3行，偏移到变更位置

        if start <= 3:  # 上下文为3行
            first_lines = diff.split("\n")
            for i in range(3):
                if first_lines[i+1].startswith('+') or first_lines[i+1].startswith('-'):
                    offset = -1  # 如果变更在开头则不构建偏移，以防产生错误
                    #  解析器是从0开始计算行，diff从1开始计算行，因此使用-1对齐

        for pos, text in self.functions:
            if start+offset >= pos[0] and start+offset <= pos[1]:
                return text

        raise ValueError("Function not found!")


# 测试代码
if __name__ == '__main__':
    manager = FunctionManager("test/fullFile.java")
    with open("test/test_diff.txt", "r") as f:
        diff = f.read()
        print(manager.get_function(diff).decode())
