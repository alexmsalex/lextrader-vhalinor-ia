import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import time
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum
import threading

# Data Types
class CodeAnalysisType(Enum):
    CORRECTION = "CORRECTION"
    OPTIMIZATION = "OPTIMIZATION"
    SECURITY = "SECURITY"
    DOCUMENTATION = "DOCUMENTATION"
    TEST_GENERATION = "TEST_GENERATION"
    TRANSLATION = "TRANSLATION"
    DEBUG = "DEBUG"

class OutputTab(Enum):
    CODE = "CODE"
    EXPLANATION = "EXPLANATION"
    METRICS = "METRICS"

@dataclass
class CodeMetrics:
    complexity: str
    performance: str
    security_score: int

@dataclass
class CodeAnalysisResult:
    generated_code: str
    explanation: str
    issues: List[str]
    suggestions: List[str]
    metrics: Optional[CodeMetrics]

# Mock AI Code Analysis Service
class CodeArchitectService:
    def __init__(self):
        self.languages = {
            'python': 'Python',
            'javascript': 'JavaScript',
            'typescript': 'TypeScript',
            'rust': 'Rust',
            'cpp': 'C++',
            'go': 'Go'
        }
        
        self.sample_responses = {
            CodeAnalysisType.CORRECTION: {
                'code': """# Corrigido - Adicionada validação de entrada e tipagem
from typing import Optional

def funcao_exemplo(x: float) -> float:
    \"\"\"Retorna o dobro do valor de entrada.
    
    Args:
        x: Valor numérico de entrada
        
    Returns:
        O dobro do valor de entrada
    \"\"\"
    if not isinstance(x, (int, float)):
        raise TypeError(f"Esperado número, recebeu {type(x).__name__}")
    
    return x * 2""",
                'explanation': """Detectei um código funcional mas sem validações robustas. Adicionei:

1. **Validação de tipo**: Verifica se a entrada é numérica
2. **Docstring**: Documentação clara da função
3. **Type hints**: Tipagem estática para melhor manutenção
4. **Tratamento de erros**: Mensagem de erro mais descritiva

Isso previne bugs comuns de tipo e melhora a documentação automática.""",
                'issues': [
                    "Falta validação de entrada",
                    "Ausência de documentação",
                    "Sem tipagem estática"
                ],
                'suggestions': [
                    "Adicionar testes unitários",
                    "Considerar usar `@property` para acesso controlado",
                    "Implementar logging para debugging"
                ]
            },
            CodeAnalysisType.OPTIMIZATION: {
                'code': """# Otimizado - Algoritmo O(n) com caching
from functools import lru_cache

@lru_cache(maxsize=128)
def funcao_exemplo(x: float) -> float:
    \"\"\"Retorna o dobro do valor de entrada com caching.
    
    Cache LRU para cálculos repetidos.
    \"\"\"
    return x * 2""",
                'explanation': """Otimizei o código adicionando:

1. **Caching LRU**: Para entradas repetidas, evita recálculo
2. **Decorator pattern**: Mantém interface limpa
3. **Eficiência O(1) para cache hits**: Dramaticamente mais rápido para cálculos repetidos

O cache de 128 entradas reduz o tempo de execução em ~90% para workloads repetitivos.""",
                'issues': [
                    "Potencial computação redundante",
                    "Sem otimização para inputs frequentes"
                ],
                'suggestions': [
                    "Ajustar maxsize baseado no uso real",
                    "Adicionar métricas de hit/miss ratio",
                    "Considerar cache distribuído para sistemas grandes"
                ]
            },
            CodeAnalysisType.SECURITY: {
                'code': """# Versão segura - Sanitizada e validada
import re
from typing import Union

def funcao_exemplo(x: Union[int, float, str]) -> float:
    \"\"\"Processa entrada segura e retorna o dobro.
    
    Args:
        x: Valor numérico ou string convertível
        
    Returns:
        O dobro do valor numérico
        
    Raises:
        ValueError: Se entrada não puder ser convertida
        OverflowError: Se resultado exceder limites
    \"\"\"
    # Sanitização de entrada
    if isinstance(x, str):
        if not re.match(r'^-?\d+(\.\d+)?$', x):
            raise ValueError(f"String inválida: {x}")
        x = float(x)
    
    # Validação de tipo
    if not isinstance(x, (int, float)):
        raise TypeError(f"Tipo inválido: {type(x).__name__}")
    
    # Verificação de limites
    result = x * 2
    if abs(result) > 1e308:
        raise OverflowError("Resultado excede limites numéricos")
    
    return result""",
                'explanation': """Refatoração completa focada em segurança:

1. **Sanitização de strings**: Regex para validar formatos numéricos
2. **Validação de overflow**: Prevenção de erros numéricos
3. **Conversão segura**: Evita injeção de código
4. **Tratamento exaustivo de erros**: Mensagens claras e específicas

Reduz vulnerabilidades comuns em 95% segundo análise estática.""",
                'issues': [
                    "Injeção de código potencial via string",
                    "Possíveis overflows numéricos",
                    "Falta de sanitização de entrada"
                ],
                'suggestions': [
                    "Adicionar rate limiting",
                    "Implementar auditoria de logs",
                    "Considerar sandboxing para eval() se necessário"
                ]
            },
            CodeAnalysisType.TRANSLATION: {
                'code': """// Convertido para TypeScript
interface MathOperation {
    (x: number): number;
}

/**
 * Retorna o dobro do valor de entrada
 * @param x - Valor numérico de entrada
 * @returns O dobro do valor de entrada
 */
const funcaoExemplo: MathOperation = (x: number): number => {
    if (typeof x !== 'number' || isNaN(x)) {
        throw new TypeError(`Esperado número, recebeu ${typeof x}`);
    }
    
    return x * 2;
};

export default funcaoExemplo;""",
                'explanation': """Tradução para TypeScript com:

1. **TypeScript interface**: Tipagem forte
2. **Arrow function**: Sintaxe moderna ES6
3. **Export/import**: Compatível com módulos ES6
4. **Validação de NaN**: Tratamento específico do JavaScript
5. **Documentação JSDoc**: Compatível com IDEs

Mantém equivalência funcional com melhor tipagem estática.""",
                'issues': [
                    "Diferenças de tipagem entre Python e TypeScript",
                    "Tratamento diferente de NaN"
                ],
                'suggestions': [
                    "Adicionar testes de equivalência cross-language",
                    "Considerar decorators TypeScript para validação",
                    "Implementar error boundaries para React"
                ]
            }
        }
    
    def analyze_code(self, code: str, analysis_type: CodeAnalysisType, 
                    source_lang: str, target_lang: str = None) -> CodeAnalysisResult:
        """Mock AI code analysis - replace with actual AI service"""
        time.sleep(1)  # Simulate AI processing
        
        if analysis_type == CodeAnalysisType.TRANSLATION:
            # Use translation-specific response
            response = self.sample_responses.get(CodeAnalysisType.TRANSLATION, 
                                                self.sample_responses[CodeAnalysisType.CORRECTION])
            
            # Modify code based on target language
            if target_lang == 'rust':
                response['code'] = """// Convertido para Rust
/// Retorna o dobro do valor de entrada
/// 
/// # Arguments
/// * `x` - Valor numérico de entrada (f64)
/// 
/// # Returns
/// O dobro do valor de entrada
/// 
/// # Examples
/// ```
/// let result = funcao_exemplo(2.5);
/// assert_eq!(result, 5.0);
/// ```
pub fn funcao_exemplo(x: f64) -> f64 {
    x * 2.0
}"""
                response['explanation'] = "Tradução para Rust com ownership system e documentação rustdoc."
            
            elif target_lang == 'go':
                response['code'] = """// Convertido para Go
package main

// FuncaoExemplo retorna o dobro do valor de entrada
func FuncaoExemplo(x float64) float64 {
    return x * 2
}"""
                response['explanation'] = "Tradução para Go com convenções de nomenclatura e pacote."
        
        else:
            response = self.sample_responses.get(analysis_type, 
                                                self.sample_responses[CodeAnalysisType.CORRECTION])
        
        # Generate metrics
        metrics = CodeMetrics(
            complexity=random.choice(["Baixa", "Média", "Alta"]),
            performance=f"{random.randint(80, 99)}% mais rápido",
            security_score=random.randint(60, 95)
        )
        
        return CodeAnalysisResult(
            generated_code=response['code'],
            explanation=response['explanation'],
            issues=response.get('issues', []),
            suggestions=response.get('suggestions', []),
            metrics=metrics
        )

# Main Application
class CodeArchitectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ARQUITETO DE CÓDIGO v2.0")
        self.root.geometry("1400x800")
        self.root.configure(bg="#0a0a0a")
        
        # Initialize services
        self.code_architect = CodeArchitectService()
        
        # State variables
        self.input_code = """# Cole seu código Python aqui

def funcao_exemplo(x):
    return x * 2"""
        
        self.language = "python"
        self.target_lang = "typescript"
        self.is_processing = False
        self.result = None
        self.active_tab = OutputTab.CODE
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the complete user interface"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg="#0a0a0a")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.setup_header()
        
        # Main content area
        self.setup_content()
    
    def setup_header(self):
        """Setup the application header"""
        header_frame = tk.Frame(self.main_frame, bg="#1a1a2e", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Left side: Logo and title
        left_frame = tk.Frame(header_frame, bg="#1a1a2e")
        left_frame.pack(side=tk.LEFT, padx=20)
        
        # Icon
        icon_frame = tk.Frame(left_frame, bg="#4c1d95", relief=tk.RAISED, 
                             borderwidth=1, padx=10, pady=10)
        icon_frame.pack(side=tk.LEFT, padx=(0, 15))
        tk.Label(icon_frame, text="💻", font=("Arial", 16), 
                bg="#4c1d95", fg="#a855f7").pack()
        
        # Text
        text_frame = tk.Frame(left_frame, bg="#1a1a2e")
        text_frame.pack(side=tk.LEFT)
        
        tk.Label(text_frame, text="ARQUITETO DE CÓDIGO v2.0", 
                font=("Arial", 16, "bold"), fg="#ffffff", bg="#1a1a2e").pack(anchor=tk.W)
        
        tk.Label(text_frame, text="NEURAL CODE REFACTORING ENGINE", 
                font=("Courier", 10), fg="#a855f7", bg="#1a1a2e").pack(anchor=tk.W)
        
        # Right side: Controls
        right_frame = tk.Frame(header_frame, bg="#1a1a2e")
        right_frame.pack(side=tk.RIGHT, padx=20)
        
        # Language selector
        lang_frame = tk.Frame(right_frame, bg="#1a1a2e")
        lang_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        self.lang_var = tk.StringVar(value=self.language.upper())
        lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.lang_var,
            values=["PYTHON", "JAVASCRIPT", "TYPESCRIPT", "RUST", "CPP"],
            state="readonly",
            width=12,
            font=("Courier", 10, "bold"),
            style="Dark.TCombobox"
        )
        lang_combo.pack()
        lang_combo.bind("<<ComboboxSelected>>", 
                       lambda e: setattr(self, 'language', self.lang_var.get().lower()))
        
        # Processing indicator
        self.processing_label = tk.Label(
            right_frame,
            text="",
            font=("Courier", 10),
            fg="#fbbf24",
            bg="#1a1a2e"
        )
        self.processing_label.pack(side=tk.LEFT)
        
        # Configure combobox style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Dark.TCombobox",
                       fieldbackground="black",
                       background="black",
                       foreground="#a855f7",
                       arrowcolor="#a855f7",
                       borderwidth=1)
    
    def setup_content(self):
        """Setup the main content area"""
        content_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Split left and right panels
        left_panel = tk.Frame(content_frame, bg="#0a0a0a")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_panel = tk.Frame(content_frame, bg="#1a1a2e")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Left panel: Input
        self.setup_input_panel(left_panel)
        
        # Right panel: Output
        self.setup_output_panel(right_panel)
    
    def setup_input_panel(self, parent):
        """Setup the input code panel"""
        # Header
        input_header = tk.Frame(parent, bg="black", height=30)
        input_header.pack(fill=tk.X, side=tk.TOP)
        input_header.pack_propagate(False)
        
        tk.Label(
            input_header,
            text="SOURCE_INPUT",
            font=("Courier", 9),
            fg="#666666",
            bg="black"
        ).pack(side=tk.LEFT, padx=10)
        
        clear_btn = tk.Button(
            input_header,
            text="Clear",
            command=self.clear_input,
            font=("Arial", 8),
            bg="transparent",
            fg="#666666",
            activebackground="#333333",
            activeforeground="#ffffff",
            borderwidth=0,
            padx=10
        )
        clear_btn.pack(side=tk.RIGHT, padx=10)
        
        # Code input area
        self.code_input = scrolledtext.ScrolledText(
            parent,
            bg="#1a1a2e",
            fg="#ffffff",
            font=("Courier", 11),
            insertbackground="white",
            wrap=tk.WORD,
            borderwidth=0,
            highlightthickness=0
        )
        self.code_input.pack(fill=tk.BOTH, expand=True, padx=1, pady=(0, 1))
        self.code_input.insert(1.0, self.input_code)
        
        # Toolbar
        self.setup_toolbar(parent)
    
    def setup_toolbar(self, parent):
        """Setup the action toolbar"""
        toolbar = tk.Frame(parent, bg="#1a1a2e", height=100)
        toolbar.pack(fill=tk.X, side=tk.BOTTOM)
        toolbar.pack_propagate(False)
        
        # Action buttons (first row)
        first_row = tk.Frame(toolbar, bg="#1a1a2e")
        first_row.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        actions = [
            ("CORRIGIR", "🐛", "#2563eb", CodeAnalysisType.CORRECTION),
            ("OTIMIZAR", "⚡", "#ca8a04", CodeAnalysisType.OPTIMIZATION),
            ("SEGURANÇA", "🛡️", "#dc2626", CodeAnalysisType.SECURITY),
            ("DOCS", "📚", "#16a34a", CodeAnalysisType.DOCUMENTATION),
        ]
        
        for text, icon, color, action_type in actions:
            btn_frame = tk.Frame(first_row, bg="#1a1a2e")
            btn_frame.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
            
            btn = tk.Button(
                btn_frame,
                text=f"{icon}\n{text}",
                command=lambda at=action_type: self.execute_action(at),
                font=("Arial", 9),
                bg=f"{color}20",
                fg=color,
                activebackground=f"{color}40",
                activeforeground=color,
                relief=tk.RAISED,
                borderwidth=1,
                padx=10,
                pady=5,
                compound=tk.TOP
            )
            btn.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons (second row)
        second_row = tk.Frame(toolbar, bg="#1a1a2e")
        second_row.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        second_actions = [
            ("TESTES", "💻", "#db2777", CodeAnalysisType.TEST_GENERATION),
            ("DEBUG", "🔍", "#ea580c", CodeAnalysisType.DEBUG),
        ]
        
        for text, icon, color, action_type in second_actions:
            btn_frame = tk.Frame(second_row, bg="#1a1a2e")
            btn_frame.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
            
            btn = tk.Button(
                btn_frame,
                text=f"{icon}\n{text}",
                command=lambda at=action_type: self.execute_action(at),
                font=("Arial", 9),
                bg=f"{color}20",
                fg=color,
                activebackground=f"{color}40",
                activeforeground=color,
                relief=tk.RAISED,
                borderwidth=1,
                padx=10,
                pady=5,
                compound=tk.TOP
            )
            btn.pack(fill=tk.BOTH, expand=True)
        
        # Translation section
        trans_frame = tk.Frame(second_row, bg="#1a1a2e")
        trans_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Language selection for translation
        lang_select_frame = tk.Frame(trans_frame, bg="#0a0a0a", relief=tk.SUNKEN, borderwidth=1)
        lang_select_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(
            lang_select_frame,
            text="🌐",
            font=("Arial", 12),
            fg="#666666",
            bg="#0a0a0a"
        ).pack(side=tk.LEFT, padx=5)
        
        self.target_lang_var = tk.StringVar(value="typescript")
        trans_combo = ttk.Combobox(
            lang_select_frame,
            textvariable=self.target_lang_var,
            values=["TypeScript", "Python", "Rust", "Go"],
            state="readonly",
            width=12,
            font=("Arial", 9)
        )
        trans_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        trans_combo.bind("<<ComboboxSelected>>", 
                        lambda e: setattr(self, 'target_lang', self.target_lang_var.get().lower()))
        
        # Convert button
        convert_btn = tk.Button(
            trans_frame,
            text="CONVERTER",
            command=lambda: self.execute_action(CodeAnalysisType.TRANSLATION),
            font=("Arial", 9, "bold"),
            bg="#7c3aed",
            fg="white",
            activebackground="#8b5cf6",
            activeforeground="white",
            padx=15
        )
        convert_btn.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_output_panel(self, parent):
        """Setup the output results panel"""
        # Tab selector
        tab_frame = tk.Frame(parent, bg="#1a1a2e")
        tab_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.code_tab = tk.Button(
            tab_frame,
            text="OUTPUT_CODE",
            command=lambda: self.switch_tab(OutputTab.CODE),
            font=("Courier", 9),
            bg="#1e40af" if self.active_tab == OutputTab.CODE else "transparent",
            fg="#60a5fa" if self.active_tab == OutputTab.CODE else "#666666",
            activebackground="#1e40af",
            activeforeground="#60a5fa",
            borderwidth=0,
            padx=10,
            pady=5
        )
        self.code_tab.pack(side=tk.LEFT)
        
        self.explanation_tab = tk.Button(
            tab_frame,
            text="EXPLICAÇÃO",
            command=lambda: self.switch_tab(OutputTab.EXPLANATION),
            font=("Courier", 9),
            bg="#1e40af" if self.active_tab == OutputTab.EXPLANATION else "transparent",
            fg="#60a5fa" if self.active_tab == OutputTab.EXPLANATION else "#666666",
            activebackground="#1e40af",
            activeforeground="#60a5fa",
            borderwidth=0,
            padx=10,
            pady=5
        )
        self.explanation_tab.pack(side=tk.LEFT)
        
        self.metrics_tab = tk.Button(
            tab_frame,
            text="MÉTRICAS",
            command=lambda: self.switch_tab(OutputTab.METRICS),
            font=("Courier", 9),
            bg="#1e40af" if self.active_tab == OutputTab.METRICS else "transparent",
            fg="#60a5fa" if self.active_tab == OutputTab.METRICS else "#666666",
            activebackground="#1e40af",
            activeforeground="#60a5fa",
            borderwidth=0,
            padx=10,
            pady=5
        )
        self.metrics_tab.pack(side=tk.LEFT)
        
        # Output content area
        self.output_content = tk.Frame(parent, bg="#0a0a0a")
        self.output_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Initial placeholder
        self.show_placeholder()
    
    def show_placeholder(self):
        """Show placeholder content"""
        for widget in self.output_content.winfo_children():
            widget.destroy()
        
        placeholder = tk.Frame(self.output_content, bg="#0a0a0a")
        placeholder.pack(expand=True, fill=tk.BOTH)
        
        if self.is_processing:
            tk.Label(
                placeholder,
                text="🔄",
                font=("Arial", 48),
                fg="#fbbf24",
                bg="#0a0a0a"
            ).pack(pady=(100, 20))
            
            tk.Label(
                placeholder,
                text="ANALISANDO VETORES LÓGICOS...",
                font=("Courier", 12),
                fg="#fbbf24",
                bg="#0a0a0a"
            ).pack()
        else:
            tk.Label(
                placeholder,
                text="💻",
                font=("Arial", 48),
                fg="#666666",
                bg="#0a0a0a"
            ).pack(pady=(100, 20))
            
            tk.Label(
                placeholder,
                text="AGUARDANDO INPUT DE CÓDIGO",
                font=("Courier", 12),
                fg="#666666",
                bg="#0a0a0a"
            ).pack()
    
    def show_code_output(self):
        """Show code output tab"""
        for widget in self.output_content.winfo_children():
            widget.destroy()
        
        code_output = scrolledtext.ScrolledText(
            self.output_content,
            bg="#0a0a0a",
            fg="#10b981",
            font=("Courier", 11),
            wrap=tk.WORD,
            borderwidth=0,
            highlightthickness=0
        )
        code_output.pack(fill=tk.BOTH, expand=True)
        
        if self.result:
            code_output.insert(1.0, self.result.generated_code)
            code_output.config(state='disabled')  # Make read-only
    
    def show_explanation_output(self):
        """Show explanation tab"""
        for widget in self.output_content.winfo_children():
            widget.destroy()
        
        # Create scrollable frame for explanation
        canvas = tk.Canvas(self.output_content, bg="#0a0a0a", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.output_content, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0a0a0a")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        if self.result:
            # Analysis section
            analysis_frame = tk.Frame(
                scrollable_frame,
                bg="#1e3a8a",
                relief=tk.RAISED,
                borderwidth=1,
                padx=15,
                pady=15
            )
            analysis_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            tk.Label(
                analysis_frame,
                text="ANÁLISE NEURAL",
                font=("Arial", 10, "bold"),
                fg="#60a5fa",
                bg="#1e3a8a"
            ).pack(anchor=tk.W, pady=(0, 10))
            
            tk.Label(
                analysis_frame,
                text=self.result.explanation,
                font=("Arial", 9),
                fg="#e5e7eb",
                bg="#1e3a8a",
                wraplength=600,
                justify=tk.LEFT
            ).pack(anchor=tk.W)
            
            # Issues section
            if self.result.issues:
                issues_frame = tk.Frame(
                    scrollable_frame,
                    bg="#7f1d1d",
                    relief=tk.RAISED,
                    borderwidth=1,
                    padx=15,
                    pady=15
                )
                issues_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
                
                header_frame = tk.Frame(issues_frame, bg="#7f1d1d")
                header_frame.pack(fill=tk.X, pady=(0, 10))
                
                tk.Label(
                    header_frame,
                    text="🐛",
                    font=("Arial", 14),
                    fg="#fca5a5",
                    bg="#7f1d1d"
                ).pack(side=tk.LEFT, padx=(0, 10))
                
                tk.Label(
                    header_frame,
                    text="PROBLEMAS DETECTADOS",
                    font=("Arial", 10, "bold"),
                    fg="#fca5a5",
                    bg="#7f1d1d"
                ).pack(side=tk.LEFT)
                
                for issue in self.result.issues:
                    issue_frame = tk.Frame(issues_frame, bg="#7f1d1d")
                    issue_frame.pack(fill=tk.X, pady=2)
                    
                    tk.Label(
                        issue_frame,
                        text="•",
                        font=("Arial", 12),
                        fg="#fca5a5",
                        bg="#7f1d1d"
                    ).pack(side=tk.LEFT, padx=(0, 5))
                    
                    tk.Label(
                        issue_frame,
                        text=issue,
                        font=("Arial", 9),
                        fg="#fecaca",
                        bg="#7f1d1d",
                        wraplength=550,
                        justify=tk.LEFT
                    ).pack(side=tk.LEFT)
            
            # Suggestions section
            if self.result.suggestions:
                suggestions_frame = tk.Frame(
                    scrollable_frame,
                    bg="#854d0e",
                    relief=tk.RAISED,
                    borderwidth=1,
                    padx=15,
                    pady=15
                )
                suggestions_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
                
                header_frame = tk.Frame(suggestions_frame, bg="#854d0e")
                header_frame.pack(fill=tk.X, pady=(0, 10))
                
                tk.Label(
                    header_frame,
                    text="💡",
                    font=("Arial", 14),
                    fg="#fbbf24",
                    bg="#854d0e"
                ).pack(side=tk.LEFT, padx=(0, 10))
                
                tk.Label(
                    header_frame,
                    text="SUGESTÕES",
                    font=("Arial", 10, "bold"),
                    fg="#fbbf24",
                    bg="#854d0e"
                ).pack(side=tk.LEFT)
                
                for suggestion in self.result.suggestions:
                    suggestion_frame = tk.Frame(suggestions_frame, bg="#854d0e")
                    suggestion_frame.pack(fill=tk.X, pady=2)
                    
                    tk.Label(
                        suggestion_frame,
                        text="•",
                        font=("Arial", 12),
                        fg="#fbbf24",
                        bg="#854d0e"
                    ).pack(side=tk.LEFT, padx=(0, 5))
                    
                    tk.Label(
                        suggestion_frame,
                        text=suggestion,
                        font=("Arial", 9),
                        fg="#fef3c7",
                        bg="#854d0e",
                        wraplength=550,
                        justify=tk.LEFT
                    ).pack(side=tk.LEFT)
    
    def show_metrics_output(self):
        """Show metrics tab"""
        for widget in self.output_content.winfo_children():
            widget.destroy()
        
        if self.result and self.result.metrics:
            metrics_frame = tk.Frame(self.output_content, bg="#0a0a0a")
            metrics_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
            
            # Grid layout for metrics
            row1 = tk.Frame(metrics_frame, bg="#0a0a0a")
            row1.pack(fill=tk.X, pady=(0, 10))
            
            # Complexity metric
            complex_frame = tk.Frame(
                row1,
                bg="#374151",
                relief=tk.RAISED,
                borderwidth=1,
                padx=20,
                pady=20
            )
            complex_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
            
            tk.Label(
                complex_frame,
                text="COMPLEXIDADE",
                font=("Arial", 8),
                fg="#9ca3af",
                bg="#374151"
            ).pack(pady=(0, 5))
            
            tk.Label(
                complex_frame,
                text=self.result.metrics.complexity,
                font=("Arial", 16, "bold"),
                fg="#ffffff",
                bg="#374151"
            ).pack()
            
            # Performance metric
            perf_frame = tk.Frame(
                row1,
                bg="#374151",
                relief=tk.RAISED,
                borderwidth=1,
                padx=20,
                pady=20
            )
            perf_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            tk.Label(
                perf_frame,
                text="PERFORMANCE ESTIMADA",
                font=("Arial", 8),
                fg="#9ca3af",
                bg="#374151"
            ).pack(pady=(0, 5))
            
            tk.Label(
                perf_frame,
                text=self.result.metrics.performance,
                font=("Arial", 16, "bold"),
                fg="#ffffff",
                bg="#374151"
            ).pack()
            
            # Security score metric
            row2 = tk.Frame(metrics_frame, bg="#0a0a0a")
            row2.pack(fill=tk.X)
            
            security_frame = tk.Frame(
                row2,
                bg="#374151",
                relief=tk.RAISED,
                borderwidth=1,
                padx=20,
                pady=20
            )
            security_frame.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(
                security_frame,
                text="PONTUAÇÃO SEGURANÇA",
                font=("Arial", 8),
                fg="#9ca3af",
                bg="#374151"
            ).pack(pady=(0, 5))
            
            score_color = "#10b981" if self.result.metrics.security_score > 80 else "#ef4444"
            tk.Label(
                security_frame,
                text=f"{self.result.metrics.security_score}/100",
                font=("Arial", 24, "bold"),
                fg=score_color,
                bg="#374151"
            ).pack()
            
            # Security indicator
            indicator_frame = tk.Frame(security_frame, bg="#374151", height=10)
            indicator_frame.pack(fill=tk.X, pady=(10, 0))
            indicator_frame.pack_propagate(False)
            
            # Fill based on score
            fill_width = min(200, self.result.metrics.security_score * 2)
            fill_color = "#10b981" if self.result.metrics.security_score > 80 else \
                        "#fbbf24" if self.result.metrics.security_score > 60 else "#ef4444"
            
            fill = tk.Frame(indicator_frame, bg=fill_color, width=fill_width)
            fill.pack(side=tk.LEFT, fill=tk.Y)
    
    def clear_input(self):
        """Clear the input code area"""
        self.code_input.delete(1.0, tk.END)
    
    def switch_tab(self, tab: OutputTab):
        """Switch between output tabs"""
        self.active_tab = tab
        
        # Update tab button styles
        self.code_tab.config(
            bg="#1e40af" if tab == OutputTab.CODE else "transparent",
            fg="#60a5fa" if tab == OutputTab.CODE else "#666666"
        )
        self.explanation_tab.config(
            bg="#1e40af" if tab == OutputTab.EXPLANATION else "transparent",
            fg="#60a5fa" if tab == OutputTab.EXPLANATION else "#666666"
        )
        self.metrics_tab.config(
            bg="#1e40af" if tab == OutputTab.METRICS else "transparent",
            fg="#60a5fa" if tab == OutputTab.METRICS else "#666666"
        )
        
        # Update content
        if self.result:
            if tab == OutputTab.CODE:
                self.show_code_output()
            elif tab == OutputTab.EXPLANATION:
                self.show_explanation_output()
            elif tab == OutputTab.METRICS:
                self.show_metrics_output()
        else:
            self.show_placeholder()
    
    def execute_action(self, analysis_type: CodeAnalysisType):
        """Execute code analysis action"""
        input_code = self.code_input.get(1.0, tk.END).strip()
        if not input_code:
            return
        
        # Start processing
        self.is_processing = True
        self.result = None
        self.show_placeholder()
        
        # Update processing indicator
        self.processing_label.config(text="PROCESSANDO SINAPSES...")
        
        # Run analysis in separate thread
        def analyze_thread():
            try:
                result = self.code_architect.analyze_code(
                    input_code,
                    analysis_type,
                    self.language,
                    self.target_lang if analysis_type == CodeAnalysisType.TRANSLATION else None
                )
                
                # Update UI in main thread
                self.root.after(0, self.on_analysis_complete, result)
            except Exception as e:
                print(f"Analysis error: {e}")
                self.root.after(0, self.on_analysis_error)
        
        thread = threading.Thread(target=analyze_thread, daemon=True)
        thread.start()
    
    def on_analysis_complete(self, result: CodeAnalysisResult):
        """Handle analysis completion"""
        self.is_processing = False
        self.result = result
        self.processing_label.config(text="")
        
        # Show appropriate tab content
        self.switch_tab(self.active_tab)
    
    def on_analysis_error(self):
        """Handle analysis error"""
        self.is_processing = False
        self.processing_label.config(text="ERRO NA ANÁLISE")
        self.show_placeholder()

# Main application
def main():
    root = tk.Tk()
    app = CodeArchitectApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()