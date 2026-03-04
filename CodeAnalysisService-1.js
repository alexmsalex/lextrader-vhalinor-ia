/**
 * CyberArchitect Code Analysis Service v3.0
 * Sistema avançado de análise estática e dinâmica de código com IA
 * Integração com padrões de mercado financeiro e segurança cibernética
 */

import * as acorn from 'https://esm.sh/acorn@^8.11.0';
import * as walk from 'https://esm.sh/acorn-walk@^8.3.0';

export const CodeComplexity = {
    VERY_LOW: {
        level: 'VERY_LOW',
        score: 0.9,
        description: 'Código extremamente simples e linear',
        maxCyclomatic: 5,
        maxLines: 50,
        maintainability: 'EXCELLENT'
    },
    LOW: {
        level: 'LOW',
        score: 0.8,
        description: 'Código simples com estrutura clara',
        maxCyclomatic: 10,
        maxLines: 100,
        maintainability: 'HIGH'
    },
    MEDIUM: {
        level: 'MEDIUM',
        score: 0.7,
        description: 'Código moderado com algumas complexidades',
        maxCyclomatic: 20,
        maxLines: 200,
        maintainability: 'MEDIUM'
    },
    HIGH: {
        level: 'HIGH',
        score: 0.6,
        description: 'Código complexo com múltiplas responsabilidades',
        maxCyclomatic: 30,
        maxLines: 500,
        maintainability: 'LOW'
    },
    VERY_HIGH: {
        level: 'VERY_HIGH',
        score: 0.5,
        description: 'Código extremamente complexo e difícil de manter',
        maxCyclomatic: 50,
        maxLines: 1000,
        maintainability: 'POOR'
    },
    CRITICAL: {
        level: 'CRITICAL',
        score: 0.3,
        description: 'Código crítico com riscos significativos',
        maxCyclomatic: 100,
        maxLines: 2000,
        maintainability: 'CRITICAL'
    }
};

export const SecurityLevel = {
    EXCELLENT: {
        level: 'EXCELLENT',
        score: 95,
        color: '#00FF00',
        description: 'Segurança excepcional sem vulnerabilidades conhecidas'
    },
    GOOD: {
        level: 'GOOD',
        score: 85,
        color: '#90EE90',
        description: 'Boa segurança com vulnerabilidades mínimas'
    },
    MODERATE: {
        level: 'MODERATE',
        score: 70,
        color: '#FFFF00',
        description: 'Segurança moderada com algumas preocupações'
    },
    WEAK: {
        level: 'WEAK',
        score: 50,
        color: '#FFA500',
        description: 'Segurança fraca com vulnerabilidades significativas'
    },
    POOR: {
        level: 'POOR',
        score: 30,
        color: '#FF0000',
        description: 'Segurança pobre com riscos críticos'
    },
    CRITICAL: {
        level: 'CRITICAL',
        score: 10,
        color: '#8B0000',
        description: 'Segurança crítica - requer atenção imediata'
    }
};

export const IssueSeverity = {
    INFO: {
        level: 'INFO',
        priority: 1,
        color: '#1E90FF',
        description: 'Informação ou sugestão de melhoria'
    },
    WARNING: {
        level: 'WARNING',
        priority: 2,
        color: '#FFD700',
        description: 'Problema potencial que pode afetar qualidade'
    },
    MINOR: {
        level: 'MINOR',
        priority: 3,
        color: '#FFA500',
        description: 'Problema menor que afeta qualidade'
    },
    MAJOR: {
        level: 'MAJOR',
        priority: 4,
        color: '#FF4500',
        description: 'Problema significativo que requer atenção'
    },
    CRITICAL: {
        level: 'CRITICAL',
        priority: 5,
        color: '#8B0000',
        description: 'Problema crítico que requer ação imediata'
    },
    BLOCKER: {
        level: 'BLOCKER',
        priority: 6,
        color: '#000000',
        description: 'Problema bloqueante - impede funcionamento'
    }
};

export const PerformanceLevel = {
    EXCELLENT: {
        level: 'EXCELLENT',
        score: 95,
        description: 'Desempenho excepcional e otimizado'
    },
    GOOD: {
        level: 'GOOD',
        score: 80,
        description: 'Bom desempenho com pequenas otimizações possíveis'
    },
    MODERATE: {
        level: 'MODERATE',
        score: 65,
        description: 'Desempenho moderado - algumas otimizações necessárias'
    },
    POOR: {
        level: 'POOR',
        score: 40,
        description: 'Desempenho fraco - otimizações significativas necessárias'
    },
    CRITICAL: {
        level: 'CRITICAL',
        score: 20,
        description: 'Desempenho crítico - requer reestruturação completa'
    }
};

export class CodeMetric {
    constructor() {
        this.metrics = new Map();
        this.benchmarks = this.loadBenchmarks();
        this.patterns = this.loadSecurityPatterns();
        this.performancePatterns = this.loadPerformancePatterns();
    }

    loadBenchmarks() {
        return {
            cyclomaticComplexity: {
                excellent: 5,
                good: 10,
                moderate: 20,
                poor: 30,
                critical: 50
            },
            linesOfCode: {
                excellent: 50,
                good: 100,
                moderate: 200,
                poor: 500,
                critical: 1000
            },
            depthOfInheritance: {
                excellent: 1,
                good: 2,
                moderate: 3,
                poor: 4,
                critical: 5
            },
            coupling: {
                excellent: 5,
                good: 10,
                moderate: 15,
                poor: 20,
                critical: 30
            },
            maintainabilityIndex: {
                excellent: 85,
                good: 65,
                moderate: 50,
                poor: 30,
                critical: 20
            }
        };
    }

    loadSecurityPatterns() {
        return {
            vulnerabilities: [
                {
                    pattern: /eval\(/g,
                    severity: IssueSeverity.CRITICAL,
                    description: 'Uso de eval() - risco de injeção de código',
                    fix: 'Use JSON.parse() ou funções específicas'
                },
                {
                    pattern: /innerHTML\s*=/g,
                    severity: IssueSeverity.MAJOR,
                    description: 'Uso de innerHTML - risco de XSS',
                    fix: 'Use textContent ou manipulação segura de DOM'
                },
                {
                    pattern: /localStorage\.setItem\([^)]*secret[^)]*\)/gi,
                    severity: IssueSeverity.CRITICAL,
                    description: 'Armazenamento de dados sensíveis no localStorage',
                    fix: 'Use armazenamento seguro ou criptografia'
                },
                {
                    pattern: /fetch\([^)]*\)\.then\([^)]*\)/g,
                    severity: IssueSeverity.MINOR,
                    description: 'Tratamento de erro ausente em fetch',
                    fix: 'Adicione .catch() para tratamento de erros'
                },
                {
                    pattern: /Math\.random\(\)/g,
                    severity: IssueSeverity.WARNING,
                    description: 'Uso de Math.random() para segurança',
                    fix: 'Use crypto.getRandomValues() para criptografia'
                },
                {
                    pattern: /setTimeout\([^)]*,\s*0\)/g,
                    severity: IssueSeverity.INFO,
                    description: 'setTimeout com delay zero',
                    fix: 'Considere usar setImmediate ou microtasks'
                }
            ],
            bestPractices: [
                {
                    pattern: /const\s+\w+\s*=/g,
                    score: 1,
                    description: 'Uso de const para variáveis imutáveis'
                },
                {
                    pattern: /=>/g,
                    score: 1,
                    description: 'Uso de arrow functions'
                },
                {
                    pattern: /import\s+{[^}]*}\s+from/g,
                    score: 2,
                    description: 'Importações desestruturadas'
                },
                {
                    pattern: /async\s+function/g,
                    score: 1,
                    description: 'Uso de async/await'
                },
                {
                    pattern: /try\s*{[^}]*}\s*catch/g,
                    score: 2,
                    description: 'Tratamento de erros com try/catch'
                },
                {
                    pattern: /\/\/\s*TODO:/gi,
                    score: -1,
                    description: 'TODO comments encontrados'
                }
            ]
        };
    }

    loadPerformancePatterns() {
        return {
            antiPatterns: [
                {
                    pattern: /for\s*\(\s*let\s+i\s*=\s*0\s*;\s*i\s*<\s*array\.length\s*;/g,
                    severity: IssueSeverity.MINOR,
                    description: 'Loop com cálculo de length em cada iteração',
                    fix: 'Armazene array.length em variável antes do loop'
                },
                {
                    pattern: /\.innerHTML\s*=\s*['"][^'"]*['"]\s*\+/g,
                    severity: IssueSeverity.MAJOR,
                    description: 'Concatenação repetida de innerHTML',
                    fix: 'Use DocumentFragment ou string concatenada antes de atribuir'
                },
                {
                    pattern: /\.getElementById\([^)]*\)\.style\./g,
                    severity: IssueSeverity.MINOR,
                    description: 'Múltiplas alterações de estilo diretas',
                    fix: 'Use classes CSS ou altere style.cssText uma vez'
                },
                {
                    pattern: /\.addEventListener\([^)]*,\s*\([^)]*\)\s*=>/g,
                    severity: IssueSeverity.WARNING,
                    description: 'Arrow function anônima em event listener',
                    fix: 'Defina função separada para permitir remoção do listener'
                },
                {
                    pattern: /JSON\.parse\(JSON\.stringify\(/g,
                    severity: IssueSeverity.MINOR,
                    description: 'Deep clone usando JSON - perda de tipos',
                    fix: 'Use structuredClone() ou biblioteca de clone profundo'
                },
                {
                    pattern: /\.filter\(\)\.map\(\)/g,
                    severity: IssueSeverity.INFO,
                    description: 'Chaining filter().map() ineficiente',
                    fix: 'Use .reduce() ou combine as operações'
                }
            ],
            optimizationOpportunities: [
                {
                    pattern: /\.querySelectorAll\(/g,
                    description: 'querySelectorAll pode ser otimizado',
                    suggestion: 'Considere getElementById ou getElementsByClassName para seletores simples'
                },
                {
                    pattern: /Array\(n\)\.fill\(/g,
                    description: 'Criação de array com fill',
                    suggestion: 'Use new Array(n) e preencha com loop se performance for crítica'
                },
                {
                    pattern: /Object\.keys\([^)]*\)\.forEach\(/g,
                    description: 'Iteração sobre keys de objeto',
                    suggestion: 'Considere Object.entries() se precisar de valores também'
                },
                {
                    pattern: /\.includes\([^)]*\)\s*&&/g,
                    description: 'Múltiplas verificações includes',
                    suggestion: 'Use Set para verificação de múltiplos valores'
                }
            ]
        };
    }

    calculateCyclomaticComplexity(ast) {
        let complexity = 1; // Base complexity

        walk.simple(ast, {
            IfStatement: () => complexity++,
            ForStatement: () => complexity++,
            ForInStatement: () => complexity++,
            ForOfStatement: () => complexity++,
            WhileStatement: () => complexity++,
            DoWhileStatement: () => complexity++,
            SwitchCase: (node) => {
                if (node.test) complexity++;
            },
            ConditionalExpression: () => complexity++,
            TryStatement: () => complexity++,
            CatchClause: () => complexity++,
            LogicalExpression: (node) => {
                if (node.operator === '&&' || node.operator === '||') complexity++;
            }
        });

        return complexity;
    }

    calculateLinesOfCode(code) {
        const lines = code.split('\n');
        let loc = 0;
        let commentLines = 0;
        let emptyLines = 0;

        lines.forEach(line => {
            const trimmed = line.trim();
            if (trimmed === '') {
                emptyLines++;
            } else if (trimmed.startsWith('//') || trimmed.startsWith('/*')) {
                commentLines++;
            } else {
                loc++;
            }
        });

        return {
            total: lines.length,
            code: loc,
            comments: commentLines,
            empty: emptyLines,
            commentRatio: commentLines / (loc || 1)
        };
    }

    calculateMaintainabilityIndex(complexity, loc, halsteadVolume) {
        // Simplified Maintainability Index calculation
        const MI = 171 - 5.2 * Math.log(halsteadVolume) - 0.23 * complexity - 16.2 * Math.log(loc);
        return Math.max(0, Math.min(100, MI));
    }

    calculateHalsteadMetrics(ast) {
        let operators = new Set();
        let operands = new Set();
        let operatorCount = 0;
        let operandCount = 0;

        walk.simple(ast, {
            BinaryExpression: (node) => {
                operators.add(node.operator);
                operatorCount++;
            },
            UnaryExpression: (node) => {
                operators.add(node.operator);
                operatorCount++;
            },
            AssignmentExpression: (node) => {
                operators.add(node.operator);
                operatorCount++;
            },
            UpdateExpression: (node) => {
                operators.add(node.operator);
                operatorCount++;
            },
            LogicalExpression: (node) => {
                operators.add(node.operator);
                operatorCount++;
            },
            Identifier: (node) => {
                operands.add(node.name);
                operandCount++;
            },
            Literal: (node) => {
                operands.add(node.value?.toString() || '');
                operandCount++;
            }
        });

        const n1 = operators.size; // Distinct operators
        const n2 = operands.size;  // Distinct operands
        const N1 = operatorCount;  // Total operators
        const N2 = operandCount;   // Total operands

        const vocabulary = n1 + n2;
        const length = N1 + N2;
        const volume = length * Math.log2(vocabulary || 1);
        const difficulty = (n1 / 2) * (N2 / n2);
        const effort = difficulty * volume;

        return {
            vocabulary,
            length,
            volume,
            difficulty,
            effort,
            bugs: Math.pow(effort, 2 / 3) / 3000,
            time: effort / 18 // seconds
        };
    }

    calculateCoupling(ast) {
        const imports = new Set();
        const exports = new Set();
        const externalCalls = new Set();

        walk.simple(ast, {
            ImportDeclaration: (node) => {
                imports.add(node.source.value);
            },
            ExportNamedDeclaration: (node) => {
                if (node.source) {
                    exports.add(node.source.value);
                }
            },
            ExportDefaultDeclaration: () => {
                exports.add('default');
            },
            CallExpression: (node) => {
                if (node.callee.type === 'Identifier') {
                    externalCalls.add(node.callee.name);
                }
            }
        });

        return {
            importCount: imports.size,
            exportCount: exports.size,
            externalCallCount: externalCalls.size,
            imports: Array.from(imports),
            exports: Array.from(exports)
        };
    }

    analyzeCodeStructure(code) {
        try {
            const ast = acorn.parse(code, {
                ecmaVersion: 'latest',
                sourceType: 'module'
            });

            const complexity = this.calculateCyclomaticComplexity(ast);
            const loc = this.calculateLinesOfCode(code);
            const halstead = this.calculateHalsteadMetrics(ast);
            const coupling = this.calculateCoupling(ast);
            const maintainability = this.calculateMaintainabilityIndex(
                complexity,
                loc.code,
                halstead.volume
            );

            return {
                ast,
                complexity,
                loc,
                halstead,
                coupling,
                maintainability,
                depth: this.calculateDepth(ast)
            };
        } catch (error) {
            console.error('❌ Erro na análise de estrutura:', error);
            return null;
        }
    }

    calculateDepth(ast, currentDepth = 0, maxDepth = 0) {
        let max = maxDepth;

        walk.simple(ast, {
            enter: (node) => {
                if (this.isScopingNode(node)) {
                    max = Math.max(max, currentDepth + 1);
                    this.calculateDepth(node, currentDepth + 1, max);
                }
            }
        });

        return max;
    }

    isScopingNode(node) {
        return [
            'FunctionDeclaration',
            'FunctionExpression',
            'ArrowFunctionExpression',
            'BlockStatement',
            'IfStatement',
            'ForStatement',
            'WhileStatement',
            'DoWhileStatement',
            'SwitchStatement',
            'TryStatement',
            'CatchClause'
        ].includes(node.type);
    }
}

export class SecurityAnalyzer {
    constructor() {
        this.vulnerabilityDB = this.loadVulnerabilityDB();
        this.cryptoPatterns = this.loadCryptoPatterns();
        this.apiPatterns = this.loadAPIPatterns();
    }

    loadVulnerabilityDB() {
        return {
            xss: [
                {
                    pattern: /\.innerHTML\s*=\s*[^;]*[+\s]*userInput/gi,
                    severity: IssueSeverity.CRITICAL,
                    description: 'Injeção XSS via innerHTML com entrada de usuário',
                    cwe: 'CWE-79',
                    fix: 'Use textContent ou sanitize input'
                },
                {
                    pattern: /document\.write\([^)]*userInput/gi,
                    severity: IssueSeverity.CRITICAL,
                    description: 'Injeção XSS via document.write',
                    cwe: 'CWE-79',
                    fix: 'Evite document.write com dados dinâmicos'
                }
            ],
            injection: [
                {
                    pattern: /eval\([^)]*userInput/gi,
                    severity: IssueSeverity.CRITICAL,
                    description: 'Injeção de código via eval',
                    cwe: 'CWE-94',
                    fix: 'Não use eval com dados externos'
                },
                {
                    pattern: /Function\([^)]*userInput/gi,
                    severity: IssueSeverity.CRITICAL,
                    description: 'Injeção de código via Function constructor',
                    cwe: 'CWE-94',
                    fix: 'Evite Function constructor com dados externos'
                }
            ],
            crypto: [
                {
                    pattern: /Math\.random\(\)/g,
                    severity: IssueSeverity.MAJOR,
                    description: 'Uso de PRNG não criptográfico',
                    cwe: 'CWE-338',
                    fix: 'Use crypto.getRandomValues()'
                },
                {
                    pattern: /CryptoJS\.AES\.encrypt\([^)]*\)/g,
                    severity: IssueSeverity.WARNING,
                    description: 'Uso de CryptoJS - biblioteca não mantida',
                    cwe: 'CWE-326',
                    fix: 'Use Web Crypto API'
                }
            ],
            auth: [
                {
                    pattern: /localStorage\.setItem\([^)]*token[^)]*\)/gi,
                    severity: IssueSeverity.MAJOR,
                    description: 'Armazenamento de token no localStorage',
                    cwe: 'CWE-312',
                    fix: 'Use HttpOnly cookies ou sessionStorage'
                },
                {
                    pattern: /password\s*=\s*['"][^'"]*['"]/gi,
                    severity: IssueSeverity.CRITICAL,
                    description: 'Credenciais embutidas no código',
                    cwe: 'CWE-798',
                    fix: 'Use variáveis de ambiente'
                }
            ]
        };
    }

    loadCryptoPatterns() {
        return {
            secure: [
                /crypto\.getRandomValues\(/g,
                /crypto\.subtle\.encrypt\(/g,
                /crypto\.subtle\.digest\(/g,
                /HMAC/g,
                /PBKDF2/g
            ],
            insecure: [
                /MD5/g,
                /SHA1/g,
                /base64\.encode\(/g,
                /xor\s*\(/gi,
                /ROT13/g
            ]
        };
    }

    loadAPIPatterns() {
        return {
            bestPractices: [
                {
                    pattern: /fetch\([^)]*\)\.then\([^)]*\)/g,
                    check: (code) => code.includes('.catch('),
                    severity: IssueSeverity.MINOR,
                    description: 'Fetch sem tratamento de erro'
                },
                {
                    pattern: /setTimeout\([^)]*\)/g,
                    check: (code) => code.includes('clearTimeout('),
                    severity: IssueSeverity.WARNING,
                    description: 'setTimeout sem clearTimeout'
                },
                {
                    pattern: /addEventListener\([^)]*\)/g,
                    check: (code) => code.includes('removeEventListener('),
                    severity: IssueSeverity.WARNING,
                    description: 'addEventListener sem removeEventListener'
                }
            ],
            memory: [
                {
                    pattern: /setInterval\([^)]*\)/g,
                    severity: IssueSeverity.MINOR,
                    description: 'setInterval pode vazar memória'
                },
                {
                    pattern: /new\s+Image\(\)/g,
                    severity: IssueSeverity.WARNING,
                    description: 'Criação de Image sem limpeza'
                }
            ]
        };
    }

    scanForVulnerabilities(code) {
        const vulnerabilities = [];
        const securityScore = {
            total: 100,
            deductions: 0,
            patternsFound: []
        };

        // Scan for each vulnerability type
        Object.entries(this.vulnerabilityDB).forEach(([type, patterns]) => {
            patterns.forEach(vuln => {
                const matches = code.match(vuln.pattern);
                if (matches) {
                    vulnerabilities.push({
                        type,
                        severity: vuln.severity,
                        description: vuln.description,
                        cwe: vuln.cwe,
                        fix: vuln.fix,
                        matches: matches.length,
                        pattern: vuln.pattern.toString()
                    });

                    securityScore.deductions += vuln.severity.priority * 10;
                    securityScore.patternsFound.push(type);
                }
            });
        });

        // Check crypto patterns
        Object.entries(this.cryptoPatterns).forEach(([category, patterns]) => {
            patterns.forEach(pattern => {
                if (code.match(pattern)) {
                    vulnerabilities.push({
                        type: 'CRYPTO',
                        severity: category === 'secure' ?
                            IssueSeverity.INFO : IssueSeverity.MAJOR,
                        description: category === 'secure' ?
                            'Uso de API criptográfica segura' :
                            'Uso de primitiva criptográfica insegura',
                        matches: 1,
                        category
                    });
                }
            });
        });

        // Check API best practices
        this.apiPatterns.bestPractices.forEach(practice => {
            if (code.match(practice.pattern) && !practice.check(code)) {
                vulnerabilities.push({
                    type: 'API_BEST_PRACTICE',
                    severity: practice.severity,
                    description: practice.description,
                    fix: 'Implemente a prática recomendada'
                });
                securityScore.deductions += 5;
            }
        });

        securityScore.final = Math.max(0, securityScore.total - securityScore.deductions);

        return {
            vulnerabilities,
            securityScore: this.calculateSecurityLevel(securityScore.final),
            details: securityScore
        };
    }

    calculateSecurityLevel(score) {
        if (score >= 95) return SecurityLevel.EXCELLENT;
        if (score >= 85) return SecurityLevel.GOOD;
        if (score >= 70) return SecurityLevel.MODERATE;
        if (score >= 50) return SecurityLevel.WEAK;
        if (score >= 30) return SecurityLevel.POOR;
        return SecurityLevel.CRITICAL;
    }

    analyzeDependencies(code) {
        const dependencies = new Set();
        const importPattern = /import\s+.*from\s+['"]([^'"]+)['"]/g;
        const requirePattern = /require\(['"]([^'"]+)['"]\)/g;

        let match;
        while ((match = importPattern.exec(code)) !== null) {
            dependencies.add(match[1]);
        }

        while ((match = requirePattern.exec(code)) !== null) {
            dependencies.add(match[1]);
        }

        // Analyze dependency risk
        const riskyDependencies = this.identifyRiskyDependencies(Array.from(dependencies));

        return {
            dependencies: Array.from(dependencies),
            count: dependencies.size,
            riskyDependencies,
            dependencyRisk: this.calculateDependencyRisk(riskyDependencies.length, dependencies.size)
        };
    }

    identifyRiskyDependencies(deps) {
        const risky = [
            'eval',
            'vm',
            'child_process',
            'fs',
            'http',
            'https',
            'net',
            'dgram',
            'crypto',
            'tls',
            'cluster',
            'worker_threads'
        ];

        return deps.filter(dep =>
            risky.some(risk => dep.includes(risk)) ||
            dep.startsWith('http://') ||
            dep.startsWith('https://')
        );
    }

    calculateDependencyRisk(riskyCount, totalCount) {
        if (totalCount === 0) return SecurityLevel.EXCELLENT;

        const riskRatio = riskyCount / totalCount;
        if (riskRatio === 0) return SecurityLevel.EXCELLENT;
        if (riskRatio < 0.1) return SecurityLevel.GOOD;
        if (riskRatio < 0.3) return SecurityLevel.MODERATE;
        if (riskRatio < 0.5) return SecurityLevel.WEAK;
        return SecurityLevel.POOR;
    }
}

export class PerformanceAnalyzer {
    constructor() {
        this.benchmarks = this.loadPerformanceBenchmarks();
        this.antiPatterns = this.loadPerformanceAntiPatterns();
        this.optimizationPatterns = this.loadOptimizationPatterns();
    }

    loadPerformanceBenchmarks() {
        return {
            loopPerformance: {
                threshold: 1000,
                description: 'Loops com mais de 1000 iterações'
            },
            domOperations: {
                threshold: 10,
                description: 'Mais de 10 operações DOM consecutivas'
            },
            memoryUsage: {
                threshold: 1000000,
                description: 'Uso de memória acima de 1MB'
            },
            apiCalls: {
                threshold: 5,
                description: 'Mais de 5 chamadas API simultâneas'
            }
        };
    }

    loadPerformanceAntiPatterns() {
        return [
            {
                pattern: /for\s*\(\s*let\s+i\s*=\s*0\s*;\s*i\s*<\s*array\.length\s*;/g,
                severity: IssueSeverity.MINOR,
                description: 'Recálculo de length em loop',
                impact: 'O(n²)',
                fix: 'Cache array.length antes do loop'
            },
            {
                pattern: /\.innerHTML\s*\+=/g,
                severity: IssueSeverity.MAJOR,
                description: 'Concatenação repetida de innerHTML',
                impact: 'Reflow múltiplo',
                fix: 'Construa string e atribua uma vez'
            },
            {
                pattern: /\.getElementById\([^)]*\)\.style\./g,
                severity: IssueSeverity.MINOR,
                description: 'Múltiplas alterações de estilo',
                impact: 'Reflow múltiplo',
                fix: 'Use classes CSS'
            },
            {
                pattern: /new\s+Array\([^)]*\)\.fill\(/g,
                severity: IssueSeverity.WARNING,
                description: 'Criação de array grande com fill',
                impact: 'Alocação de memória',
                fix: 'Use TypedArray se possível'
            },
            {
                pattern: /JSON\.stringify\([^)]*\)\.match\(/g,
                severity: IssueSeverity.MINOR,
                description: 'Parse JSON para regex',
                impact: 'CPU intensivo',
                fix: 'Processe objeto diretamente'
            },
            {
                pattern: /\.filter\([^)]*\)\.map\([^)]*\)\.reduce\(/g,
                severity: IssueSeverity.WARNING,
                description: 'Chaining excessivo de array methods',
                impact: 'Múltiplas iterações',
                fix: 'Combine operações em um reduce'
            }
        ];
    }

    loadOptimizationPatterns() {
        return [
            {
                pattern: /document\.querySelectorAll\(/g,
                suggestion: 'Use getElementById para IDs únicos',
                improvement: '2-10x'
            },
            {
                pattern: /\.forEach\(/g,
                suggestion: 'Considere for loop para performance crítica',
                improvement: '2-3x'
            },
            {
                pattern: /Object\.assign\(/g,
                suggestion: 'Use spread operator para objetos pequenos',
                improvement: '1.5-2x'
            },
            {
                pattern: /Array\.from\(/g,
                suggestion: 'Use spread operator para iteráveis',
                improvement: '2-3x'
            },
            {
                pattern: /\.includes\(/g,
                suggestion: 'Use Set para múltiplas verificações',
                improvement: 'O(1) vs O(n)'
            }
        ];
    }

    analyzePerformance(code, structure) {
        const issues = [];
        const optimizations = [];
        let performanceScore = 100;

        // Check anti-patterns
        this.antiPatterns.forEach(pattern => {
            const matches = code.match(pattern.pattern);
            if (matches) {
                issues.push({
                    type: 'PERFORMANCE_ANTI_PATTERN',
                    severity: pattern.severity,
                    description: pattern.description,
                    impact: pattern.impact,
                    fix: pattern.fix,
                    occurrences: matches.length
                });
                performanceScore -= pattern.severity.priority * 5;
            }
        });

        // Check optimization opportunities
        this.optimizationPatterns.forEach(pattern => {
            if (code.match(pattern.pattern)) {
                optimizations.push({
                    type: 'OPTIMIZATION_OPPORTUNITY',
                    description: pattern.suggestion,
                    improvement: pattern.improvement,
                    pattern: pattern.pattern.toString()
                });
            }
        });

        // Analyze structure for performance issues
        if (structure) {
            const structureIssues = this.analyzeStructurePerformance(structure);
            issues.push(...structureIssues.issues);
            performanceScore -= structureIssues.deductions;
        }

        // Calculate loops and complexity
        const loopAnalysis = this.analyzeLoops(code);
        issues.push(...loopAnalysis.issues);
        performanceScore -= loopAnalysis.deductions;

        return {
            issues,
            optimizations,
            performanceScore: this.calculatePerformanceLevel(performanceScore),
            metrics: {
                loopCount: loopAnalysis.loopCount,
                nestedLoopDepth: loopAnalysis.maxDepth,
                domOperations: this.countDOMOperations(code),
                apiCalls: this.countAPICalls(code)
            }
        };
    }

    analyzeStructurePerformance(structure) {
        const issues = [];
        let deductions = 0;

        // Check cyclomatic complexity
        if (structure.complexity > 20) {
            issues.push({
                type: 'HIGH_COMPLEXITY',
                severity: IssueSeverity.MAJOR,
                description: `Complexidade ciclomática alta: ${structure.complexity}`,
                fix: 'Refatore em funções menores',
                threshold: 20
            });
            deductions += 10;
        }

        // Check maintainability index
        if (structure.maintainability < 50) {
            issues.push({
                type: 'LOW_MAINTAINABILITY',
                severity: IssueSeverity.WARNING,
                description: `Índice de manutenibilidade baixo: ${structure.maintainability.toFixed(1)}`,
                fix: 'Melhore documentação e estrutura',
                threshold: 50
            });
            deductions += 5;
        }

        // Check Halstead bugs
        if (structure.halstead.bugs > 0.5) {
            issues.push({
                type: 'HIGH_BUG_POTENTIAL',
                severity: IssueSeverity.MINOR,
                description: `Potencial de bugs alto: ${structure.halstead.bugs.toFixed(2)}`,
                fix: 'Simplifique lógica complexa',
                metric: 'Halstead bugs'
            });
            deductions += 3;
        }

        return { issues, deductions };
    }

    analyzeLoops(code) {
        const loopPatterns = [
            /for\s*\([^)]*\)\s*{/g,
            /while\s*\([^)]*\)\s*{/g,
            /do\s*{[^}]*}\s*while/g,
            /\.forEach\([^)]*\)/g,
            /\.map\([^)]*\)/g,
            /\.filter\([^)]*\)/g,
            /\.reduce\([^)]*\)/g
        ];

        let loopCount = 0;
        let maxDepth = 0;
        const issues = [];
        let deductions = 0;

        loopPatterns.forEach(pattern => {
            const matches = code.match(pattern);
            if (matches) {
                loopCount += matches.length;

                // Check for nested loops
                if (matches.length > 3) {
                    issues.push({
                        type: 'MULTIPLE_LOOPS',
                        severity: IssueSeverity.WARNING,
                        description: `Múltiplos loops (${matches.length}) detectados`,
                        fix: 'Considere otimizar ou combinar loops',
                        pattern: pattern.toString()
                    });
                    deductions += 5;
                }
            }
        });

        // Analyze loop depth
        const depth = this.calculateLoopDepth(code);
        maxDepth = Math.max(maxDepth, depth);

        if (maxDepth > 3) {
            issues.push({
                type: 'DEEP_LOOP_NESTING',
                severity: IssueSeverity.MAJOR,
                description: `Aninhamento profundo de loops: ${maxDepth} níveis`,
                fix: 'Refatore loops aninhados em funções separadas',
                threshold: 3
            });
            deductions += 15;
        }

        return { loopCount, maxDepth, issues, deductions };
    }

    calculateLoopDepth(code) {
        let depth = 0;
        let maxDepth = 0;
        const lines = code.split('\n');

        lines.forEach(line => {
            const trimmed = line.trim();
            if (trimmed.includes('for') || trimmed.includes('while') || trimmed.includes('forEach')) {
                depth++;
                maxDepth = Math.max(maxDepth, depth);
            }
            if (trimmed.includes('}')) {
                depth = Math.max(0, depth - 1);
            }
        });

        return maxDepth;
    }

    countDOMOperations(code) {
        const domPatterns = [
            /\.getElementById\(/g,
            /\.querySelector\(/g,
            /\.querySelectorAll\(/g,
            /\.createElement\(/g,
            /\.appendChild\(/g,
            /\.removeChild\(/g,
            /\.setAttribute\(/g,
            /\.classList\./g,
            /\.style\./g
        ];

        return domPatterns.reduce((count, pattern) => {
            const matches = code.match(pattern);
            return count + (matches ? matches.length : 0);
        }, 0);
    }

    countAPICalls(code) {
        const apiPatterns = [
            /fetch\(/g,
            /XMLHttpRequest/g,
            /\.get\(/g,
            /\.post\(/g,
            /axios\./g,
            /\.ajax\(/g
        ];

        return apiPatterns.reduce((count, pattern) => {
            const matches = code.match(pattern);
            return count + (matches ? matches.length : 0);
        }, 0);
    }

    calculatePerformanceLevel(score) {
        if (score >= 95) return PerformanceLevel.EXCELLENT;
        if (score >= 80) return PerformanceLevel.GOOD;
        if (score >= 65) return PerformanceLevel.MODERATE;
        if (score >= 40) return PerformanceLevel.POOR;
        return PerformanceLevel.CRITICAL;
    }
}

export class CodeAnalysisService {
    constructor(config = {}) {
        this.config = {
            enableSecurityAnalysis: config.enableSecurityAnalysis !== false,
            enablePerformanceAnalysis: config.enablePerformanceAnalysis !== false,
            enableStructureAnalysis: config.enableStructureAnalysis !== false,
            enableAIRecommendations: config.enableAIRecommendations !== false,
            strictMode: config.strictMode || false,
            ...config
        };

        this.metricAnalyzer = new CodeMetric();
        this.securityAnalyzer = new SecurityAnalyzer();
        this.performanceAnalyzer = new PerformanceAnalyzer();
        this.analysisHistory = [];
        this.benchmarkData = this.loadBenchmarkData();

        console.log('🔍 CyberArchitect Code Analysis Service v3.0 inicializado');
    }

    loadBenchmarkData() {
        return {
            averageComplexity: 15,
            averageSecurityScore: 75,
            averagePerformanceScore: 70,
            industryStandards: {
                maxCyclomatic: 20,
                minSecurity: 70,
                minPerformance: 65,
                maxLinesPerFunction: 50,
                maxDepth: 3
            }
        };
    }

    analyze(code, context = {}) {
        const analysisId = `analysis_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        console.log(`🔍 Iniciando análise de código [${analysisId}]...`);

        const startTime = Date.now();

        try {
            // Validar entrada
            if (!this.validateInput(code)) {
                throw new Error('Código de entrada inválido');
            }

            // Coletar métricas básicas
            const basicMetrics = this.collectBasicMetrics(code);

            // Análise de estrutura (se habilitado)
            const structureAnalysis = this.config.enableStructureAnalysis ?
                this.analyzeStructure(code) : null;

            // Análise de segurança (se habilitado)
            const securityAnalysis = this.config.enableSecurityAnalysis ?
                this.analyzeSecurity(code, structureAnalysis) : null;

            // Análise de performance (se habilitado)
            const performanceAnalysis = this.config.enablePerformanceAnalysis ?
                this.analyzePerformance(code, structureAnalysis) : null;

            // Análise de estilo e boas práticas
            const styleAnalysis = this.analyzeCodeStyle(code);

            // Gerar recomendações
            const recommendations = this.generateRecommendations(
                structureAnalysis,
                securityAnalysis,
                performanceAnalysis,
                styleAnalysis
            );

            // Calcular scores finais
            const finalScores = this.calculateFinalScores(
                structureAnalysis,
                securityAnalysis,
                performanceAnalysis,
                styleAnalysis
            );

            // Gerar relatório completo
            const report = this.generateReport({
                analysisId,
                basicMetrics,
                structureAnalysis,
                securityAnalysis,
                performanceAnalysis,
                styleAnalysis,
                recommendations,
                finalScores,
                context,
                processingTime: Date.now() - startTime
            });

            // Atualizar histórico
            this.updateAnalysisHistory(report);

            // Comparar com benchmarks
            const benchmarkComparison = this.compareWithBenchmarks(finalScores);

            console.log(`✅ Análise concluída em ${Date.now() - startTime}ms`);
            console.log(`📊 Scores: Complexidade=${finalScores.complexity.level}, Segurança=${finalScores.security.level}, Performance=${finalScores.performance.level}`);

            return {
                ...report,
                benchmarkComparison
            };

        } catch (error) {
            console.error('❌ Erro na análise de código:', error);
            return this.getFallbackAnalysis(error, analysisId);
        }
    }

    validateInput(code) {
        if (!code || typeof code !== 'string') {
            throw new Error('Código deve ser uma string não vazia');
        }

        if (code.length > 1000000) { // 1MB limit
            throw new Error('Código excede o tamanho máximo de 1MB');
        }

        // Verificar sintaxe básica
        try {
            acorn.parse(code, { ecmaVersion: 'latest', sourceType: 'module' });
            return true;
        } catch (error) {
            throw new Error(`Erro de sintaxe: ${error.message}`);
        }
    }

    collectBasicMetrics(code) {
        const lines = code.split('\n');
        const chars = code.length;

        return {
            lines: lines.length,
            characters: chars,
            nonEmptyLines: lines.filter(line => line.trim().length > 0).length,
            commentLines: lines.filter(line => line.trim().startsWith('//') || line.trim().startsWith('/*')).length,
            functions: (code.match(/function\s+\w+|const\s+\w+\s*=\s*\(|let\s+\w+\s*=\s*\(|var\s+\w+\s*=\s*\(|=>/g) || []).length,
            imports: (code.match(/import\s+.*from|require\(/g) || []).length,
            exports: (code.match(/export\s+/g) || []).length
        };
    }

    analyzeStructure(code) {
        try {
            const structure = this.metricAnalyzer.analyzeCodeStructure(code);

            if (!structure) {
                return {
                    success: false,
                    error: 'Falha na análise de estrutura'
                };
            }

            // Calcular complexidade
            const complexity = this.calculateComplexityLevel(
                structure.complexity,
                structure.loc.code
            );

            // Calcular acoplamento
            const coupling = this.calculateCouplingLevel(structure.coupling);

            // Calcular coesão (simplificado)
            const cohesion = this.calculateCohesion(structure);

            return {
                success: true,
                ast: structure.ast,
                metrics: {
                    cyclomaticComplexity: structure.complexity,
                    linesOfCode: structure.loc,
                    halstead: structure.halstead,
                    coupling: structure.coupling,
                    maintainabilityIndex: structure.maintainability,
                    depth: structure.depth
                },
                levels: {
                    complexity,
                    coupling,
                    cohesion,
                    maintainability: this.calculateMaintainabilityLevel(structure.maintainability)
                },
                structureHealth: this.calculateStructureHealth(structure)
            };

        } catch (error) {
            console.error('❌ Erro na análise de estrutura:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    calculateComplexityLevel(cyclomatic, lines) {
        const ratio = cyclomatic / (lines || 1);

        if (cyclomatic <= 5 && ratio <= 0.1) return CodeComplexity.VERY_LOW;
        if (cyclomatic <= 10 && ratio <= 0.15) return CodeComplexity.LOW;
        if (cyclomatic <= 20 && ratio <= 0.2) return CodeComplexity.MEDIUM;
        if (cyclomatic <= 30 && ratio <= 0.25) return CodeComplexity.HIGH;
        if (cyclomatic <= 50 && ratio <= 0.3) return CodeComplexity.VERY_HIGH;
        return CodeComplexity.CRITICAL;
    }

    calculateCouplingLevel(coupling) {
        const totalCoupling = coupling.importCount + coupling.externalCallCount;

        if (totalCoupling <= 5) return { level: 'VERY_LOW', score: 0.9 };
        if (totalCoupling <= 10) return { level: 'LOW', score: 0.8 };
        if (totalCoupling <= 15) return { level: 'MEDIUM', score: 0.7 };
        if (totalCoupling <= 20) return { level: 'HIGH', score: 0.6 };
        return { level: 'VERY_HIGH', score: 0.5 };
    }

    calculateCohesion(structure) {
        // Simplified cohesion calculation
        const functions = this.countFunctions(structure.ast);
        const avgFunctionSize = structure.loc.code / (functions || 1);

        let cohesionScore = 0.7; // Base

        if (avgFunctionSize > 50) cohesionScore -= 0.2;
        if (structure.coupling.importCount > 10) cohesionScore -= 0.1;
        if (structure.depth > 3) cohesionScore -= 0.1;

        return {
            level: cohesionScore > 0.8 ? 'HIGH' : cohesionScore > 0.6 ? 'MEDIUM' : 'LOW',
            score: cohesionScore
        };
    }

    countFunctions(ast) {
        let count = 0;

        walk.simple(ast, {
            FunctionDeclaration: () => count++,
            FunctionExpression: () => count++,
            ArrowFunctionExpression: () => count++
        });

        return count;
    }

    calculateMaintainabilityIndex(maintainability) {
        if (maintainability >= 85) return 'EXCELLENT';
        if (maintainability >= 65) return 'GOOD';
        if (maintainability >= 50) return 'MODERATE';
        if (maintainability >= 30) return 'POOR';
        return 'CRITICAL';
    }

    calculateStructureHealth(structure) {
        let score = 100;

        // Deductions based on metrics
        if (structure.complexity > 20) score -= 20;
        if (structure.loc.code > 200) score -= 15;
        if (structure.coupling.importCount > 10) score -= 10;
        if (structure.depth > 3) score -= 10;
        if (structure.maintainability < 50) score -= 20;

        return {
            score: Math.max(0, score),
            level: score >= 90 ? 'EXCELLENT' :
                score >= 70 ? 'GOOD' :
                    score >= 50 ? 'MODERATE' :
                        score >= 30 ? 'POOR' : 'CRITICAL'
        };
    }

    analyzeSecurity(code, structure) {
        const vulnerabilityScan = this.securityAnalyzer.scanForVulnerabilities(code);
        const dependencyAnalysis = this.securityAnalyzer.analyzeDependencies(code);

        // Additional checks based on structure
        let structureIssues = [];
        if (structure?.success) {
            structureIssues = this.checkStructureSecurity(structure);
        }

        const allIssues = [
            ...vulnerabilityScan.vulnerabilities,
            ...structureIssues
        ];

        // Calculate overall security score
        const overallScore = this.calculateOverallSecurityScore(
            vulnerabilityScan.securityScore,
            dependencyAnalysis.dependencyRisk,
            allIssues
        );

        return {
            vulnerabilityScan,
            dependencyAnalysis,
            structureIssues,
            overallScore,
            recommendations: this.generateSecurityRecommendations(allIssues, dependencyAnalysis)
        };
    }

    checkStructureSecurity(structure) {
        const issues = [];

        // Check for large functions
        if (structure.metrics.linesOfCode.code > 100) {
            issues.push({
                type: 'LARGE_FUNCTION',
                severity: IssueSeverity.WARNING,
                description: 'Função muito grande - difícil de auditar',
                fix: 'Quebre em funções menores',
                lines: structure.metrics.linesOfCode.code
            });
        }

        // Check for deep nesting
        if (structure.metrics.depth > 4) {
            issues.push({
                type: 'DEEP_NESTING',
                severity: IssueSeverity.MINOR,
                description: 'Aninhamento profundo - aumenta complexidade',
                fix: 'Refatore para reduzir aninhamento',
                depth: structure.metrics.depth
            });
        }

        // Check for high complexity
        if (structure.metrics.cyclomaticComplexity > 15) {
            issues.push({
                type: 'HIGH_COMPLEXITY',
                severity: IssueSeverity.WARNING,
                description: 'Alta complexidade ciclomática - aumenta risco',
                fix: 'Simplifique a lógica',
                complexity: structure.metrics.cyclomaticComplexity
            });
        }

        return issues;
    }

    calculateOverallSecurityScore(vulnerabilityScore, dependencyRisk, issues) {
        let score = vulnerabilityScore.score;

        // Adjust based on dependency risk
        score *= (dependencyRisk.score / 100);

        // Deductions for issues
        issues.forEach(issue => {
            score -= issue.severity.priority * 2;
        });

        // Ensure within bounds
        score = Math.max(0, Math.min(100, score));

        return this.securityAnalyzer.calculateSecurityLevel(score);
    }

    generateSecurityRecommendations(issues, dependencyAnalysis) {
        const recommendations = [];

        // Critical vulnerabilities
        const criticalVulns = issues.filter(i => i.severity.level === 'CRITICAL');
        if (criticalVulns.length > 0) {
            recommendations.push({
                priority: 'CRITICAL',
                action: 'IMMEDIATE_FIX',
                description: `Corrija ${criticalVulns.length} vulnerabilidades críticas`,
                details: criticalVulns.map(v => v.description)
            });
        }

        // Major vulnerabilities
        const majorVulns = issues.filter(i => i.severity.level === 'MAJOR');
        if (majorVulns.length > 0) {
            recommendations.push({
                priority: 'HIGH',
                action: 'PRIORITY_FIX',
                description: `Corrija ${majorVulns.length} vulnerabilidades importantes`,
                details: majorVulns.map(v => v.description)
            });
        }

        // Dependency risks
        if (dependencyAnalysis.riskyDependencies.length > 0) {
            recommendations.push({
                priority: 'MEDIUM',
                action: 'REVIEW_DEPENDENCIES',
                description: `Revise ${dependencyAnalysis.riskyDependencies.length} dependências de risco`,
                dependencies: dependencyAnalysis.riskyDependencies
            });
        }

        // General improvements
        if (issues.length === 0) {
            recommendations.push({
                priority: 'LOW',
                action: 'MAINTAIN_SECURITY',
                description: 'Código seguro - mantenha boas práticas'
            });
        }

        return recommendations;
    }

    analyzePerformance(code, structure) {
        return this.performanceAnalyzer.analyzePerformance(code, structure);
    }

    analyzeCodeStyle(code) {
        const styleIssues = [];
        const styleScore = {
            total: 100,
            deductions: 0
        };

        // Check for consistent formatting
        const formatting = this.checkFormatting(code);
        styleIssues.push(...formatting.issues);
        styleScore.deductions += formatting.deductions;

        // Check naming conventions
        const naming = this.checkNamingConventions(code);
        styleIssues.push(...naming.issues);
        styleScore.deductions += naming.deductions;

        // Check comments
        const comments = this.checkComments(code);
        styleIssues.push(...comments.issues);
        styleScore.deductions += comments.deductions;

        // Check modern JavaScript features
        const modernJS = this.checkModernJavaScript(code);
        styleIssues.push(...modernJS.issues);
        styleScore.deductions += modernJS.deductions;

        return {
            issues: styleIssues,
            score: Math.max(0, styleScore.total - styleScore.deductions),
            categories: {
                formatting,
                naming,
                comments,
                modernJS
            }
        };
    }

    checkFormatting(code) {
        const issues = [];
        let deductions = 0;
        const lines = code.split('\n');

        // Check indentation
        let inconsistentIndentation = false;
        lines.forEach((line, index) => {
            if (line.trim().length > 0 && !line.startsWith(' ') && !line.startsWith('\t')) {
                // Check if this line should be indented
                const prevLine = index > 0 ? lines[index - 1] : '';
                if (prevLine.trim().endsWith('{') || prevLine.includes('=>')) {
                    inconsistentIndentation = true;
                }
            }
        });

        if (inconsistentIndentation) {
            issues.push({
                type: 'INDENTATION',
                severity: IssueSeverity.WARNING,
                description: 'Indentação inconsistente',
                fix: 'Use indentação consistente (2 ou 4 espaços)'
            });
            deductions += 5;
        }

        // Check line length
        const longLines = lines.filter(line => line.length > 120);
        if (longLines.length > 0) {
            issues.push({
                type: 'LINE_LENGTH',
                severity: IssueSeverity.INFO,
                description: `${longLines.length} linhas com mais de 120 caracteres`,
                fix: 'Quebre linhas longas para melhor legibilidade'
            });
            deductions += 2;
        }

        // Check trailing spaces
        const trailingSpaces = lines.filter(line => line.endsWith(' '));
        if (trailingSpaces.length > 0) {
            issues.push({
                type: 'TRAILING_SPACES',
                severity: IssueSeverity.INFO,
                description: 'Espaços em branco no final das linhas',
                fix: 'Remova espaços em branco desnecessários'
            });
            deductions += 1;
        }

        return { issues, deductions };
    }

    checkNamingConventions(code) {
        const issues = [];
        let deductions = 0;

        // Check variable naming
        const varPattern = /(?:let|const|var)\s+([a-z][a-zA-Z0-9]*)/g;
        let match;
        while ((match = varPattern.exec(code)) !== null) {
            const varName = match[1];
            if (varName.includes('_')) {
                issues.push({
                    type: 'VARIABLE_NAMING',
                    severity: IssueSeverity.WARNING,
                    description: `Variável "${varName}" usa snake_case`,
                    fix: 'Use camelCase para variáveis JavaScript'
                });
                deductions += 2;
            }
        }

        // Check function naming
        const funcPattern = /function\s+([A-Z][a-zA-Z0-9]*)|(?:const|let)\s+([a-z][a-zA-Z0-9]*)\s*=\s*(?:\([^)]*\)|[^=]*=>)/g;
        while ((match = funcPattern.exec(code)) !== null) {
            const funcName = match[1] || match[2];
            if (funcName && !/^[a-z]/.test(funcName)) {
                issues.push({
                    type: 'FUNCTION_NAMING',
                    severity: IssueSeverity.WARNING,
                    description: `Função "${funcName}" deve começar com letra minúscula`,
                    fix: 'Use camelCase para nomes de função'
                });
                deductions += 3;
            }
        }

        // Check constant naming
        const constPattern = /const\s+([A-Z_][A-Z0-9_]*)/g;
        while ((match = constPattern.exec(code)) !== null) {
            const constName = match[1];
            if (!constName.includes('_')) {
                issues.push({
                    type: 'CONSTANT_NAMING',
                    severity: IssueSeverity.INFO,
                    description: `Constante "${constName}" não usa SNAKE_CASE`,
                    fix: 'Use SNAKE_CASE para constantes'
                });
                deductions += 1;
            }
        }

        return { issues, deductions };
    }

    checkComments(code) {
        const issues = [];
        let deductions = 0;
        const lines = code.split('\n');

        const totalLines = lines.length;
        const commentLines = lines.filter(line =>
            line.trim().startsWith('//') || line.trim().startsWith('/*')
        ).length;

        const commentRatio = commentLines / totalLines;

        // Check for too few comments
        if (commentRatio < 0.05 && totalLines > 50) {
            issues.push({
                type: 'INSUFFICIENT_COMMENTS',
                severity: IssueSeverity.WARNING,
                description: 'Poucos comentários no código',
                fix: 'Adicione comentários para documentar lógica complexa',
                ratio: commentRatio.toFixed(2)
            });
            deductions += 5;
        }

        // Check for TODO comments
        const todoComments = lines.filter(line =>
            line.includes('TODO') || line.includes('FIXME')
        );

        if (todoComments.length > 0) {
            issues.push({
                type: 'TODO_COMMENTS',
                severity: IssueSeverity.INFO,
                description: `${todoComments.length} comentários TODO/FIXME encontrados`,
                fix: 'Resolva ou remova comentários TODO',
                examples: todoComments.slice(0, 3)
            });
            deductions += 2;
        }

        // Check for commented code
        const commentedCode = lines.filter(line =>
            line.trim().startsWith('// ') && line.length > 10
        ).length;

        if (commentedCode > 5) {
            issues.push({
                type: 'COMMENTED_CODE',
                severity: IssueSeverity.INFO,
                description: `${commentedCode} linhas de código comentadas`,
                fix: 'Remova código comentado ou converta em documentação'
            });
            deductions += 1;
        }

        return { issues, deductions };
    }

    checkModernJavaScript(code) {
        const issues = [];
        let deductions = 0;
        let score = 0;

        // Check for modern features
        const modernFeatures = {
            'arrow functions': /=>/g,
            'template literals': /`[^`]*\${[^}]*}[^`]*`/g,
            'destructuring': /const\s+{[^}]*}\s*=/g,
            'spread operator': /\.\.\./g,
            'async/await': /async\s+function|await\s+/g,
            'optional chaining': /\?\./g,
            'nullish coalescing': /\?\?/g
        };

        Object.entries(modernFeatures).forEach(([feature, pattern]) => {
            if (code.match(pattern)) {
                score += 5; // Bonus for using modern features
            }
        });

        // Check for deprecated features
        const deprecatedFeatures = {
            'var keyword': /\bvar\s+/g,
            'function constructor': /new\s+Function\(/g,
            'with statement': /\bwith\s*\(/g,
            'eval': /\beval\(/g
        };

        Object.entries(deprecatedFeatures).forEach(([feature, pattern]) => {
            if (code.match(pattern)) {
                issues.push({
                    type: 'DEPRECATED_FEATURE',
                    severity: IssueSeverity.WARNING,
                    description: `Uso de ${feature} desencorajado`,
                    fix: `Substitua ${feature} por alternativa moderna`
                });
                deductions += 10;
            }
        });

        // Calculate final score
        const finalScore = Math.max(0, 50 + score - deductions);

        return {
            issues,
            deductions,
            score: finalScore,
            modernFeatureCount: Object.keys(modernFeatures).filter(f => code.match(modernFeatures[f])).length
        };
    }

    generateRecommendations(structure, security, performance, style) {
        const recommendations = [];

        // Structure recommendations
        if (structure?.success) {
            if (structure.levels.complexity.level === 'HIGH' ||
                structure.levels.complexity.level === 'VERY_HIGH' ||
                structure.levels.complexity.level === 'CRITICAL') {
                recommendations.push({
                    category: 'STRUCTURE',
                    priority: 'HIGH',
                    description: 'Complexidade alta detectada',
                    action: 'Refatore funções complexas em funções menores',
                    metric: `Complexidade ciclomática: ${structure.metrics.cyclomaticComplexity}`
                });
            }

            if (structure.metrics.linesOfCode.code > 200) {
                recommendations.push({
                    category: 'STRUCTURE',
                    priority: 'MEDIUM',
                    description: 'Código extenso detectado',
                    action: 'Considere modularizar em arquivos separados',
                    metric: `${structure.metrics.linesOfCode.code} linhas de código`
                });
            }
        }

        // Security recommendations
        if (security?.overallScore) {
            if (security.overallScore.level === 'WEAK' ||
                security.overallScore.level === 'POOR' ||
                security.overallScore.level === 'CRITICAL') {
                recommendations.push({
                    category: 'SECURITY',
                    priority: 'CRITICAL',
                    description: 'Pontuação de segurança baixa',
                    action: 'Revise e corrija vulnerabilidades identificadas',
                    score: `${security.overallScore.score}/100`
                });
            }

            if (security.dependencyAnalysis.riskyDependencies.length > 0) {
                recommendations.push({
                    category: 'SECURITY',
                    priority: 'HIGH',
                    description: 'Dependências de risco detectadas',
                    action: 'Revise as dependências listadas',
                    count: security.dependencyAnalysis.riskyDependencies.length
                });
            }
        }

        // Performance recommendations
        if (performance?.performanceScore) {
            if (performance.performanceScore.level === 'POOR' ||
                performance.performanceScore.level === 'CRITICAL') {
                recommendations.push({
                    category: 'PERFORMANCE',
                    priority: 'HIGH',
                    description: 'Desempenho abaixo do ideal',
                    action: 'Implemente otimizações sugeridas',
                    score: performance.performanceScore.level
                });
            }

            if (performance.optimizations.length > 0) {
                performance.optimizations.slice(0, 3).forEach(opt => {
                    recommendations.push({
                        category: 'PERFORMANCE',
                        priority: 'MEDIUM',
                        description: `Oportunidade de otimização: ${opt.description}`,
                        action: opt.description,
                        improvement: opt.improvement
                    });
                });
            }
        }

        // Style recommendations
        if (style?.score < 70) {
            recommendations.push({
                category: 'STYLE',
                priority: 'LOW',
                description: 'Oportunidades de melhoria de estilo',
                action: 'Considere as sugestões de estilo',
                score: `${style.score}/100`
            });
        }

        // Sort by priority
        const priorityOrder = { CRITICAL: 4, HIGH: 3, MEDIUM: 2, LOW: 1 };
        recommendations.sort((a, b) => priorityOrder[b.priority] - priorityOrder[a.priority]);

        return recommendations;
    }

    calculateFinalScores(structure, security, performance, style) {
        // Calculate weighted average
        let complexityScore = 50; // Default
        let securityScore = 50;
        let performanceScore = 50;
        let styleScore = 50;

        if (structure?.success) {
            complexityScore = structure.levels.complexity.score * 100;
        }

        if (security?.overallScore) {
            securityScore = security.overallScore.score;
        }

        if (performance?.performanceScore) {
            performanceScore = performance.performanceScore.score;
        }

        if (style?.score) {
            styleScore = style.score;
        }

        // Weighted average (adjust weights as needed)
        const weights = {
            complexity: 0.3,
            security: 0.4,
            performance: 0.2,
            style: 0.1
        };

        const overallScore =
            complexityScore * weights.complexity +
            securityScore * weights.security +
            performanceScore * weights.performance +
            styleScore * weights.style;

        return {
            complexity: this.metricAnalyzer.calculateComplexityLevelBasedOnScore(complexityScore),
            security: security?.overallScore || SecurityLevel.MODERATE,
            performance: performance?.performanceScore || PerformanceLevel.MODERATE,
            style: this.calculateStyleLevel(styleScore),
            overall: this.calculateOverallLevel(overallScore),
            scores: {
                complexity: complexityScore,
                security: securityScore,
                performance: performanceScore,
                style: styleScore,
                overall: overallScore
            }
        };
    }

    calculateStyleLevel(score) {
        if (score >= 90) return { level: 'EXCELLENT', score };
        if (score >= 75) return { level: 'GOOD', score };
        if (score >= 60) return { level: 'MODERATE', score };
        if (score >= 40) return { level: 'POOR', score };
        return { level: 'CRITICAL', score };
    }

    calculateOverallLevel(score) {
        if (score >= 90) return { level: 'EXCELLENT', score };
        if (score >= 75) return { level: 'GOOD', score };
        if (score >= 60) return { level: 'MODERATE', score };
        if (score >= 40) return { level: 'POOR', score };
        return { level: 'CRITICAL', score };
    }

    generateReport(data) {
        return {
            analysisId: data.analysisId,
            timestamp: new Date(),
            summary: {
                linesOfCode: data.basicMetrics.lines,
                functions: data.basicMetrics.functions,
                imports: data.basicMetrics.imports,
                processingTime: data.processingTime
            },
            scores: data.finalScores,
            structure: data.structureAnalysis,
            security: data.securityAnalysis,
            performance: data.performanceAnalysis,
            style: data.styleAnalysis,
            recommendations: data.recommendations,
            context: data.context,
            metadata: {
                serviceVersion: '3.0',
                analysisDepth: this.getAnalysisDepth(),
                config: this.config
            }
        };
    }

    getAnalysisDepth() {
        let depth = 'BASIC';
        if (this.config.enableStructureAnalysis) depth = 'INTERMEDIATE';
        if (this.config.enableSecurityAnalysis && this.config.enablePerformanceAnalysis) {
            depth = 'ADVANCED';
        }
        return depth;
    }

    updateAnalysisHistory(report) {
        this.analysisHistory.push(report);

        // Keep history limited
        if (this.analysisHistory.length > 1000) {
            this.analysisHistory = this.analysisHistory.slice(-500);
        }
    }

    compareWithBenchmarks(scores) {
        const comparisons = {};

        // Compare each score with benchmarks
        Object.keys(scores.scores).forEach(key => {
            const score = scores.scores[key];
            const benchmark = this.benchmarkData.averageSecurityScore; // Simplified

            comparisons[key] = {
                score,
                benchmark,
                difference: score - benchmark,
                status: score >= benchmark ? 'ABOVE_AVERAGE' : 'BELOW_AVERAGE'
            };
        });

        // Overall comparison
        const overallBenchmark = 70; // Industry standard
        comparisons.overall = {
            score: scores.scores.overall,
            benchmark: overallBenchmark,
            difference: scores.scores.overall - overallBenchmark,
            status: scores.scores.overall >= overallBenchmark ? 'ABOVE_AVERAGE' : 'BELOW_AVERAGE'
        };

        return comparisons;
    }

    getFallbackAnalysis(error, analysisId) {
        return {
            analysisId,
            timestamp: new Date(),
            error: error.message,
            scores: {
                complexity: CodeComplexity.MEDIUM,
                security: SecurityLevel.MODERATE,
                performance: PerformanceLevel.MODERATE,
                overall: { level: 'MODERATE', score: 50 }
            },
            recommendations: [
                {
                    category: 'SYSTEM',
                    priority: 'HIGH',
                    description: 'Erro na análise de código',
                    action: 'Verifique a sintaxe do código e tente novamente'
                }
            ],
            fallback: true
        };
    }

    getAnalysisStatistics() {
        if (this.analysisHistory.length === 0) {
            return {
                totalAnalyses: 0,
                averageScores: {},
                trend: 'NO_DATA'
            };
        }

        const recentAnalyses = this.analysisHistory.slice(-100);

        const averages = {
            complexity: 0,
            security: 0,
            performance: 0,
            overall: 0
        };

        recentAnalyses.forEach(analysis => {
            if (analysis.scores?.scores) {
                Object.keys(averages).forEach(key => {
                    if (analysis.scores.scores[key]) {
                        averages[key] += analysis.scores.scores[key];
                    }
                });
            }
        });

        Object.keys(averages).forEach(key => {
            averages[key] = averages[key] / recentAnalyses.length;
        });

        // Calculate trend
        let trend = 'STABLE';
        if (recentAnalyses.length >= 2) {
            const first = recentAnalyses[0].scores?.scores?.overall || 50;
            const last = recentAnalyses[recentAnalyses.length - 1].scores?.scores?.overall || 50;

            if (last > first + 5) trend = 'IMPROVING';
            else if (last < first - 5) trend = 'DECLINING';
        }

        return {
            totalAnalyses: this.analysisHistory.length,
            recentAnalyses: recentAnalyses.length,
            averageScores: averages,
            trend,
            lastAnalysis: this.analysisHistory[this.analysisHistory.length - 1]?.timestamp
        };
    }

    exportAnalysisData() {
        return {
            config: { ...this.config },
            analysisHistory: this.analysisHistory.slice(-100),
            statistics: this.getAnalysisStatistics(),
            benchmarks: this.benchmarkData,
            exportTimestamp: new Date()
        };
    }

    importAnalysisData(data) {
        if (!data) return;

        if (data.config) {
            this.config = { ...this.config, ...data.config };
        }

        if (data.analysisHistory) {
            this.analysisHistory = data.analysisHistory;
        }

        if (data.benchmarks) {
            this.benchmarkData = { ...this.benchmarkData, ...data.benchmarks };
        }

        console.log('📥 Dados de análise importados');
    }

    reset() {
        this.analysisHistory = [];
        console.log('🔄 Code Analysis Service resetado');
    }
}

// Método utilitário para análise rápida
CodeAnalysisService.quickAnalyze = function (code) {
    const service = new CodeAnalysisService({
        enableSecurityAnalysis: true,
        enablePerformanceAnalysis: true,
        enableStructureAnalysis: true
    });

    return service.analyze(code);
};

// Exportar utilitários
export {
    CodeComplexity,
    SecurityLevel,
    IssueSeverity,
    PerformanceLevel
};

// Exportar instância singleton
const codeAnalysisService = new CodeAnalysisService();

export default codeAnalysisService;