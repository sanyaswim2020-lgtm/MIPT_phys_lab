import sympy as sp
from pathlib import Path


def init_latex_export():
    """
    Вызывайте эту функцию в самой первой ячейке ноутбука.
    Она очищает файл от результатов предыдущих запусков.
    """
    export_dir.mkdir(parents=True, exist_ok=True)
    master_file.write_text('% Автоматически сгенерированный файл\n', encoding='utf-8')

def _append_to_latex(text):
    """Базовая функция для добавления контента в конец файла."""
    with open(master_file, 'a', encoding='utf-8') as f:
        f.write(text + '\n')

def save_formulas(equations):
    text = ''
    for equation in equations:
        display(equation)
        text += r'\[\displaystyle ' + sp.latex(equation) + r'\]' + '\n'
    _append_to_latex(text)

def error_formulas(name, expression, variables):
    # Эта функция не производит запись в файл, оставляем без изменений[cite: 1]
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

def save_table(table):
    text = table.to_latex(index=False, escape=False, float_format=str)
    _append_to_latex(text)

def save_results(lines):
    text = ''
    for line in lines:
        text += r'\noindent $' + line + r'$\par\vspace{3mm}' + '\n'
    _append_to_latex(text)

def save_figure(filename_pdf, fig, caption='', label='', width=r'0.8\textwidth'):
    """
    Сохраняет PDF с графиком отдельно[cite: 1], 
    но код вставки графика добавляет в общий .tex файл.
    """
    img_name = f"{filename_pdf}.pdf"
    fig.savefig(export_dir / img_name, format='pdf', bbox_inches='tight')
    
    text = (
        r'\begin{figure}[htbp]' + '\n'
        r'    \centering' + '\n'
        f'    \\includegraphics[width={width}]{{{img_name}}}\n'
        f'    \\caption{{{caption}}}\n'
        f'    \\label{{{label}}}\n'
        r'\end{figure}' + '\n'
    )
    _append_to_latex(text)