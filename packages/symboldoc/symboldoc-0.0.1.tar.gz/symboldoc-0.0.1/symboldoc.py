import ast
import sys


class BaseFlavor:
    """
    Basic description for class {name}
    """

    def method(self):
        """
        Basic description for method {name}
        """
        pass

    @classmethod
    def lstrip(cls, string):
        """Helper method to remove left padding from docstrings"""
        return '\n'.join((line.lstrip(' '*4) for line in string.split('\n')))

    @classmethod
    def with_quotes(cls, string):
        """Return the rendered template between quotes"""
        return ''.join(('"""', string, '"""'))

    @classmethod
    def render_class_template(cls, node):
        """Renders the class docstring"""
        base = cls.lstrip(cls.__doc__)
        return cls.with_quotes(base.format(name=node.name))

    @classmethod
    def render_method_template(cls, node):
        """Renders the method docstring"""
        base = cls.lstrip(cls.method.__doc__)
        return cls.with_quotes(base.format(name=node.name))


class SphinxTemplate(BaseFlavor):
    """
    Basic description for class {name}
    """

    def method(self):
        """Brief summary for method {name}

        The first line is brief explanation, which may be completed with
        a longer one.

        - **parameters**, **types**, **return** and **return types**::

        {parameters}
        :return: return description
        :rtype: The return type description
        """
        pass

    @classmethod
    def get_docstring_for_arguments(cls, node):
        pass

    @classmethod
    def get_docstring_for_return(cls, node):
        pass

    @classmethod
    def render_method_template(cls, node):
        base = cls.lstrip(cls.method.__doc__)
        arguments = []
        for arg in node.args.args:
            name = arg.arg
            if name not in ('self', 'cls'):
                annotation = arg.annotation.id if arg.annotation else ''
                arguments.append(
                    ':param %s: Description for %s' % (name, name))
                arguments.append(':type %s: %s' % (name, annotation))

        rendered = base.format(
            name=node.name,
            parameters='\n'.join(arguments))

        return cls.with_quotes(rendered)


FLAVORS = {
    'default': BaseFlavor,
    'sphinx': SphinxTemplate,
}


def get_ast_tree(module):
    raw_file = open(module).read()

    tree = ast.parse(raw_file)

    return tree


def iter_tree(item):
    yield item
    if 'body' in item._fields:
        for child in item.body:
            # Python 3.3+: yield from iter_tree(child)
            for grandchild in iter_tree(child):
                yield grandchild


# TODO allow find by symbol type so we can do Class.method
def find_symbol_in_tree(tree, symbol):
    for item in iter_tree(tree):
        name = getattr(item, 'name', None)
        if name == symbol:
            return item


def render_template_for_symbol(node, flavor):
    if isinstance(node, ast.FunctionDef):
        return FLAVORS[flavor].render_method_template(node)

    if isinstance(node, ast.ClassDef):
        return FLAVORS[flavor].render_class_template(node)


def get_docstring_for_symbol(tree, symbol, flavor):
    node = find_symbol_in_tree(tree, symbol)
    template = render_template_for_symbol(node, flavor)

    return template


def cli():
    try:
        module_path = sys.argv[1]
        symbol = sys.argv[2]
        flavor = 'sphinx'

        if len(sys.argv) >= 4:
            if sys.argv[3] in FLAVORS.keys():
                flavor = sys.argv[3]

    except IndexError:
        print('Usage: <path to module> <symbol>')
        sys.exit(1)

    result = get_docstring_for_symbol(
        get_ast_tree(module_path),
        symbol,
        flavor)

    if not result:
        print('Symbol %s not found in %s' % (symbol, module_path))
        sys.exit(2)

    print(result)


if __name__ == '__main__':
    cli()
