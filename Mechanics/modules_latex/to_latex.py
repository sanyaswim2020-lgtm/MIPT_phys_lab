def save_formulas(filename, equations):
    text = ''
    for equation in equations:
        display(equation)
        text += r'\[\displaystyle ' + sp.latex(equation) + r'\]' + '\n'
    (export_dir / filename).write_text(text, encoding='utf-8')


def error_formulas(name, expression, variables):
    result = sp.Symbol(name)
    function = sp.Function(name)(*variables)
    equations = [sp.Eq(result, expression)]
    variance = 0
    for variable in variables:
        derivative = sp.diff(expression, variable)
        equations.append(sp.Eq(sp.Derivative(function, variable), derivative))
        uncertainty = sp.Symbol(r'\sigma_{' + sp.latex(variable) + '}', positive=True)
        variance += (derivative * uncertainty)**2
    error = sp.sqrt(variance)
    equations.append(sp.Eq(sp.Symbol(r'\sigma_{' + sp.latex(result) + '}'), error))
    return equations

def save_table(filename, table):
    text = table.to_latex(index=False, escape=False, float_format=str)
    (export_dir / filename).write_text(text, encoding='utf-8')


def save_results(filename, lines):
    text = ''
    for line in lines:
        text += r'\noindent $' + line + r'$\par\vspace{3mm}' + '\n'
    (export_dir / filename).write_text(text, encoding='utf-8')