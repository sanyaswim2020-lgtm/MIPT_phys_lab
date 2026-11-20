import sympy as sp
from pathlib import Path

# Дефолтный путь к .tex файлу, куда будут аппендиться данные: export/master_output.tex
export_dir = Path('./export') 
master_file = export_dir / 'master_output.tex'

def init_latex_export():
    """
    Функция вызывается в самом начале файла.
    Создает файл в локальной директории export/master_output.tex.
    Если такой файл существует - перезаписывает его.
    """
    export_dir.mkdir(parents=True, exist_ok=True)
    master_file.write_text('% Автоматически сгенерированный файл\n', encoding='utf-8')

def _append_to_latex(text):
    """
    Внутренняя функция, используется внутри других функций
    для импорта данных из .py/.ipynb в .tex.
    """
    with open(master_file, 'a', encoding='utf-8') as f:
        f.write(text + '\n')

def save_formulas(equations):
    """
    Сохраняет формулы из .py/.ipynb в .tex.

    Args:
        Итерируемый объект, содержащий формулы, например, [sympy.Eq], [r'$...$'].

    Returns:
        None    
    """
    text = ''
    for equation in equations:
        display(equation)
        text += r'\[\displaystyle ' + sp.latex(equation) + r'\]' + r'\vspace{4mm}' + '\n'
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

def save_table(table, column_format: str):
    """
    Переводит Pandas.DataFrame в Latex формат.

    Args:
        table: Pandas.DataFrame.
        column_format: расположение данных в столбцах таблицы ('c', 'r', 'l')
    
    Returns:
        None.
    """
    # У таблицы без столбцов нет содержимого для экспорта.
    if table.shape[1] == 0:
        return "Нельзя перевести пустую таблицу"

    latex = table.to_latex(
        index=False,
        escape=False,
        float_format=str,
        column_format=column_format * table.shape[1],
    )

    _append_to_latex(
        '\\par\n'
        '\\begin{center}\n'
        + latex
        + '\\end{center}\n'
    )


def save_results(lines):
    for line in lines:
        save_text(line)
    
def save_text(text):
    _append_to_latex(r'\par\noindent ' + text + r'\par\vspace{4mm}')

def save_figure(
    filename_pdf,
    fig,
    caption='',
    label='',
    width=r'0.7\textwidth',
):
    img_name = f"{export_dir}/{filename_pdf}.pdf"
    fig.savefig(img_name, format='pdf', bbox_inches='tight')

    text = (
        '\\par\n'
        '\\begin{figure}[H]\n'
        '    \\centering\n'
        f'    \\includegraphics[width={width}]{{{img_name}}}\n'
        f'    \\caption{{{caption}}}\n'
        f'    \\label{{{label}}}\n'
        '\\end{figure}\n'
    )
    _append_to_latex(text)