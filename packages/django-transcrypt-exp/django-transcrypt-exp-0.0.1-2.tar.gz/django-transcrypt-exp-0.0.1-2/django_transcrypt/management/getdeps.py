import ast
import imp
import os


class ImportLister(ast.NodeVisitor):

    fileList = []
    moduleList = []

    def _process_names(self, names, module=None):
        for item in names:
            item_module = item.name
            if module is not None:
                item_module = module + "." + item_module
            self.moduleList.append(item_module)

    def find_modules(self, prefix=[]):
        """
        Returns a list of paths to dependencies
        """
        for pack in set(self.moduleList):
            module_path = pack.split(".")
            module = module_path[-1]
            path = module_path[0:-1]

            try:
                f, n, o = imp.find_module(module, path)
                self.fileList.append(os.path.abspath(f.name))
            except ImportError:
                if len(prefix) > 0:
                    try:
                        prefixed_path = prefix + path
                        ospath = os.path.join(*prefixed_path)
                        f, n, o = imp.find_module(module, [ospath])
                        self.fileList.append(os.path.abspath(f.name))
                    except ImportError:
                        pass

    def visit_Import(self, node):
        self._process_names(node.names)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self._process_names(node.names, node.module)
        self.generic_visit(node)


def _get_filename_deps(filename):
    with open(filename, encoding='utf-8') as f:
        code = f.read()
    tree = ast.parse(code)
    path = list(os.path.split(filename)[:-1])
    importLister = ImportLister()
    importLister.generic_visit(tree)
    importLister.find_modules(path)

    return importLister.fileList


def getdeps(filename):
    # Initial run

    deps = set(_get_filename_deps(filename))
    deps_count = 0
    while deps_count != len(deps):
        deps_count = len(deps)
        for dep in deps:
            deps = deps | set(_get_filename_deps(dep))

    return list(deps)
