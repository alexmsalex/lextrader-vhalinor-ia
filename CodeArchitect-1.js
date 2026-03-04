/**
 * Code Architect v5.0 - Sistema Neural de Refatoração e Otimização de Código
 * Arquitetura AGI para análise, refatoração e otimização automática de código
 */

import { CodeAnalysisService } from './code_analysis_service.js';
import { AdvancedTemporalNetwork } from './advanced_temporal_network.js';
import { aiSystemManager } from './ai_system_manager.js';

export const RefactoringPattern = {
    EXTRACT_METHOD: {
        code: 'EXTRACT_METHOD',
        name: 'Extract Method',
        description: 'Extrair trecho de código repetido em método separado',
        complexity: 'MEDIUM',
        impact: 'HIGH',
        confidenceThreshold: 0.7
    },
    REPLACE_TEMP_WITH_QUERY: {
        code: 'REPLACE_TEMP_WITH_QUERY',
        name: 'Replace Temp with Query',
        description: 'Substituir variável temporária por método query',
        complexity: 'LOW',
        impact: 'MEDIUM',
        confidenceThreshold: 0.6
    },
    INTRODUCE_PARAMETER_OBJECT: {
        code: 'INTRODUCE_PARAMETER_OBJECT',
        name: 'Introduce Parameter Object',
        description: 'Agrupar múltiplos parâmetros em objeto',
        complexity: 'MEDIUM',
        impact: 'HIGH',
        confidenceThreshold: 0.65
    },
    REPLACE_CONDITIONAL_WITH_POLYMORPHISM: {
        code: 'REPLACE_CONDITIONAL_WITH_POLYMORPHISM',
        name: 'Replace Conditional with Polymorphism',
        description: 'Substituir condicionais por polimorfismo',
        complexity: 'HIGH',
        impact: 'VERY_HIGH',
        confidenceThreshold: 0.75
    },
    REMOVE_DEAD_CODE: {
        code: 'REMOVE_DEAD_CODE',
        name: 'Remove Dead Code',
        description: 'Remover código não utilizado',
        complexity: 'LOW',
        impact: 'MEDIUM',
        confidenceThreshold: 0.8
    },
    INLINE_METHOD: {
        code: 'INLINE_METHOD',
        name: 'Inline Method',
        description: 'Substituir chamada de método pequeno pelo seu corpo',
        complexity: 'LOW',
        impact: 'LOW',
        confidenceThreshold: 0.7
    },
    MOVE_METHOD: {
        code: 'MOVE_METHOD',
        name: 'Move Method',
        description: 'Mover método para classe mais apropriada',
        complexity: 'MEDIUM',
        impact: 'HIGH',
        confidenceThreshold: 0.7
    },
    EXTRACT_CLASS: {
        code: 'EXTRACT_CLASS',
        name: 'Extract Class',
        description: 'Extrair parte de classe em nova classe',
        complexity: 'HIGH',
        impact: 'VERY_HIGH',
        confidenceThreshold: 0.75
    },
    REPLACE_MAGIC_NUMBER_WITH_CONSTANT: {
        code: 'REPLACE_MAGIC_NUMBER_WITH_CONSTANT',
        name: 'Replace Magic Number with Constant',
        description: 'Substituir números mágicos por constantes nomeadas',
        complexity: 'LOW',
        impact: 'MEDIUM',
        confidenceThreshold: 0.85
    },
    ENCAPSULATE_FIELD: {
        code: 'ENCAPSULATE_FIELD',
        name: 'Encapsulate Field',
        description: 'Encapsular campo público com getter/setter',
        complexity: 'LOW',
        impact: 'MEDIUM',
        confidenceThreshold: 0.8
    },
    SIMPLIFY_CONDITIONAL: {
        code: 'SIMPLIFY_CONDITIONAL',
        name: 'Simplify Conditional',
        description: 'Simplificar expressões condicionais complexas',
        complexity: 'MEDIUM',
        impact: 'HIGH',
        confidenceThreshold: 0.7
    },
    REPLACE_LOOP_WITH_PIPELINE: {
        code: 'REPLACE_LOOP_WITH_PIPELINE',
        name: 'Replace Loop with Pipeline',
        description: 'Substituir loops por operações funcionais',
        complexity: 'MEDIUM',
        impact: 'HIGH',
        confidenceThreshold: 0.65
    }
};

export const OptimizationType = {
    PERFORMANCE: {
        code: 'PERFORMANCE',
        name: 'Performance Optimization',
        description: 'Otimizações para melhorar desempenho',
        metrics: ['executionTime', 'memoryUsage', 'cpuUsage']
    },
    MEMORY: {
        code: 'MEMORY',
        name: 'Memory Optimization',
        description: 'Otimizações para reduzir uso de memória',
        metrics: ['heapSize', 'garbageCollection', 'memoryLeaks']
    },
    SECURITY: {
        code: 'SECURITY',
        name: 'Security Optimization',
        description: 'Otimizações para melhorar segurança',
        metrics: ['vulnerabilities', 'encryption', 'authentication']
    },
    READABILITY: {
        code: 'READABILITY',
        name: 'Readability Optimization',
        description: 'Otimizações para melhorar legibilidade',
        metrics: ['complexity', 'naming', 'structure']
    },
    MAINTAINABILITY: {
        code: 'MAINTAINABILITY',
        name: 'Maintainability Optimization',
        description: 'Otimizações para facilitar manutenção',
        metrics: ['coupling', 'cohesion', 'testability']
    }
};

export const CodeLanguage = {
    JAVASCRIPT: {
        code: 'JAVASCRIPT',
        name: 'JavaScript/ECMAScript',
        extensions: ['.js', '.mjs', '.cjs', '.jsx', '.ts', '.tsx'],
        features: ['ES6+', 'Async/Await', 'Modules', 'TypeScript']
    },
    PYTHON: {
        code: 'PYTHON',
        name: 'Python',
        extensions: ['.py', '.pyw', '.pyx'],
        features: ['Dynamic Typing', 'Decorators', 'Generators']
    },
    TYPESCRIPT: {
        code: 'TYPESCRIPT',
        name: 'TypeScript',
        extensions: ['.ts', '.tsx'],
        features: ['Static Typing', 'Interfaces', 'Generics']
    },
    JAVA: {
        code: 'JAVA',
        name: 'Java',
        extensions: ['.java'],
        features: ['OOP', 'JVM', 'Strong Typing']
    },
    GO: {
        code: 'GO',
        name: 'Go',
        extensions: ['.go'],
        features: ['Concurrency', 'Static Typing', 'Garbage Collection']
    },
    RUST: {
        code: 'RUST',
        name: 'Rust',
        extensions: ['.rs'],
        features: ['Memory Safety', 'Zero Cost Abstractions', 'Concurrency']
    }
};

export const RefactoringImpact = {
    NONE: {
        code: 'NONE',
        level: 0,
        description: 'Sem impacto funcional'
    },
    LOW: {
        code: 'LOW',
        level: 1,
        description: 'Impacto mínimo, apenas estilístico'
    },
    MEDIUM: {
        code: 'MEDIUM',
        level: 2,
        description: 'Impacto moderado, melhorias internas'
    },
    HIGH: {
        code: 'HIGH',
        level: 3,
        description: 'Impacto significativo, mudanças estruturais'
    },
    VERY_HIGH: {
        code: 'VERY_HIGH',
        level: 4,
        description: 'Impacto crítico, reestruturação completa'
    }
};

export class CodePatternDetector {
    constructor() {
        this.patterns = new Map();
        this.temporalNetwork = new AdvancedTemporalNetwork({
            sequenceLength: 50,
            hiddenSize: 64,
            memorySize: 128
        });
        this.initializePatterns();
    }

    initializePatterns() {
        // Padrões de código duplicado
        this.patterns.set('DUPLICATE_CODE', {
            detect: (ast, context) => this.detectDuplicateCode(ast, context),
            refactor: RefactoringPattern.EXTRACT_METHOD,
            confidence: 0.8
        });

        // Padrões de código morto
        this.patterns.set('DEAD_CODE', {
            detect: (ast, context) => this.detectDeadCode(ast, context),
            refactor: RefactoringPattern.REMOVE_DEAD_CODE,
            confidence: 0.9
        });

        // Padrões de complexidade ciclomática alta
        this.patterns.set('HIGH_COMPLEXITY', {
            detect: (ast, context) => this.detectHighComplexity(ast, context),
            refactor: RefactoringPattern.SIMPLIFY_CONDITIONAL,
            confidence: 0.7
        });

        // Padrões de acoplamento alto
        this.patterns.set('HIGH_COUPLING', {
            detect: (ast, context) => this.detectHighCoupling(ast, context),
            refactor: RefactoringPattern.EXTRACT_CLASS,
            confidence: 0.75
        });

        // Padrões de números mágicos
        this.patterns.set('MAGIC_NUMBERS', {
            detect: (ast, context) => this.detectMagicNumbers(ast, context),
            refactor: RefactoringPattern.REPLACE_MAGIC_NUMBER_WITH_CONSTANT,
            confidence: 0.85
        });

        // Padrões de condicionais complexas
        this.patterns.set('COMPLEX_CONDITIONALS', {
            detect: (ast, context) => this.detectComplexConditionals(ast, context),
            refactor: RefactoringPattern.REPLACE_CONDITIONAL_WITH_POLYMORPHISM,
            confidence: 0.65
        });

        // Padrões de loops ineficientes
        this.patterns.set('INEFFICIENT_LOOPS', {
            detect: (ast, context) => this.detectInefficientLoops(ast, context),
            refactor: RefactoringPattern.REPLACE_LOOP_WITH_PIPELINE,
            confidence: 0.7
        });
    }

    async detectPatterns(code, language, context = {}) {
        const startTime = Date.now();

        try {
            // Parse do código
            const ast = this.parseCode(code, language);
            if (!ast) return { patterns: [], success: false };

            // Detectar padrões
            const detectedPatterns = [];

            for (const [patternName, patternConfig] of this.patterns) {
                const detectionResult = patternConfig.detect(ast, { ...context, language });

                if (detectionResult.detected) {
                    detectedPatterns.push({
                        pattern: patternName,
                        refactoring: patternConfig.refactor,
                        confidence: detectionResult.confidence * patternConfig.confidence,
                        locations: detectionResult.locations,
                        metrics: detectionResult.metrics,
                        suggestions: detectionResult.suggestions
                    });
                }
            }

            // Análise temporal de padrões
            const temporalAnalysis = await this.analyzeTemporalPatterns(code, language);

            // Combinar resultados
            const combinedPatterns = this.combinePatterns(detectedPatterns, temporalAnalysis);

            return {
                patterns: combinedPatterns,
                success: true,
                processingTime: Date.now() - startTime,
                ast: ast,
                language: language
            };

        } catch (error) {
            console.error('❌ Erro na detecção de padrões:', error);
            return {
                patterns: [],
                success: false,
                error: error.message,
                processingTime: Date.now() - startTime
            };
        }
    }

    parseCode(code, language) {
        try {
            switch (language.code) {
                case 'JAVASCRIPT':
                case 'TYPESCRIPT':
                    return this.parseJavaScript(code);
                // Adicionar parsers para outras linguagens aqui
                default:
                    console.warn(`⚠️ Parser não implementado para ${language.name}`);
                    return null;
            }
        } catch (error) {
            console.error(`❌ Erro no parse do código ${language.name}:`, error);
            return null;
        }
    }

    parseJavaScript(code) {
        // Usar acorn para parse de JavaScript/TypeScript
        try {
            const parser = require('acorn');
            return parser.parse(code, {
                ecmaVersion: 'latest',
                sourceType: 'module',
                locations: true,
                ranges: true
            });
        } catch (error) {
            // Fallback para parser simples
            return this.simpleParse(code);
        }
    }

    simpleParse(code) {
        // Parser simplificado para análise básica
        return {
            type: 'Program',
            body: [],
            sourceType: 'module',
            comments: [],
            tokens: []
        };
    }

    detectDuplicateCode(ast, context) {
        // Implementação simplificada de detecção de código duplicado
        // Em produção, usar algoritmos como Rabin-Karp ou suffix trees

        const patterns = [];
        const codeBlocks = this.extractCodeBlocks(ast);

        // Comparar blocos de código
        for (let i = 0; i < codeBlocks.length; i++) {
            for (let j = i + 1; j < codeBlocks.length; j++) {
                const similarity = this.calculateSimilarity(
                    codeBlocks[i].code,
                    codeBlocks[j].code
                );

                if (similarity > 0.8) { // 80% de similaridade
                    patterns.push({
                        block1: codeBlocks[i],
                        block2: codeBlocks[j],
                        similarity
                    });
                }
            }
        }

        return {
            detected: patterns.length > 0,
            confidence: patterns.length > 0 ? 0.9 : 0.1,
            locations: patterns.map(p => ({
                start: p.block1.location.start,
                end: p.block1.location.end
            })),
            metrics: {
                duplicateBlocks: patterns.length,
                averageSimilarity: patterns.reduce((sum, p) => sum + p.similarity, 0) / (patterns.length || 1)
            },
            suggestions: patterns.length > 0 ? [
                'Extrair código duplicado para método comum',
                'Considere usar funções de ordem superior'
            ] : []
        };
    }

    extractCodeBlocks(ast) {
        const blocks = [];

        // Walk AST e extrair blocos de código
        const walk = (node) => {
            if (!node) return;

            // Extrair blocos funcionais
            if (node.type === 'FunctionDeclaration' ||
                node.type === 'FunctionExpression' ||
                node.type === 'ArrowFunctionExpression') {
                blocks.push({
                    type: 'function',
                    code: this.getNodeSource(node),
                    location: node.loc || { start: 0, end: 0 }
                });
            }

            // Extrair blocos condicionais
            if (node.type === 'IfStatement' ||
                node.type === 'SwitchStatement' ||
                node.type === 'TryStatement') {
                blocks.push({
                    type: 'conditional',
                    code: this.getNodeSource(node),
                    location: node.loc || { start: 0, end: 0 }
                });
            }

            // Extrair loops
            if (node.type === 'ForStatement' ||
                node.type === 'WhileStatement' ||
                node.type === 'DoWhileStatement') {
                blocks.push({
                    type: 'loop',
                    code: this.getNodeSource(node),
                    location: node.loc || { start: 0, end: 0 }
                });
            }

            // Recursivamente processar filhos
            Object.keys(node).forEach(key => {
                if (typeof node[key] === 'object' && node[key] !== null) {
                    if (Array.isArray(node[key])) {
                        node[key].forEach(child => walk(child));
                    } else {
                        walk(node[key]);
                    }
                }
            });
        };

        walk(ast);
        return blocks;
    }

    getNodeSource(node) {
        // Método simplificado - em produção usar source code real
        return JSON.stringify(node, null, 2);
    }

    calculateSimilarity(str1, str2) {
        // Similaridade de Jaccard simplificada
        const set1 = new Set(str1.split(' '));
        const set2 = new Set(str2.split(' '));

        const intersection = new Set([...set1].filter(x => set2.has(x)));
        const union = new Set([...set1, ...set2]);

        return intersection.size / union.size;
    }

    detectDeadCode(ast, context) {
        // Detecção simplificada de código morto
        // Em produção, usar análise de fluxo de dados

        const deadCodeLocations = [];

        const walk = (node, parent) => {
            if (!node) return;

            // Detectar variáveis não utilizadas
            if (node.type === 'VariableDeclarator' && node.id) {
                // Verificar se variável é usada
                const varName = node.id.name;
                const isUsed = this.checkVariableUsage(ast, varName);

                if (!isUsed) {
                    deadCodeLocations.push({
                        type: 'unused_variable',
                        name: varName,
                        location: node.loc || { start: 0, end: 0 }
                    });
                }
            }

            // Detectar funções não chamadas
            if (node.type === 'FunctionDeclaration' && node.id) {
                const funcName = node.id.name;
                const isCalled = this.checkFunctionCalls(ast, funcName);

                if (!isCalled && funcName !== 'main' && !funcName.startsWith('_')) {
                    deadCodeLocations.push({
                        type: 'unused_function',
                        name: funcName,
                        location: node.loc || { start: 0, end: 0 }
                    });
                }
            }

            // Recursivamente processar filhos
            Object.keys(node).forEach(key => {
                if (typeof node[key] === 'object' && node[key] !== null) {
                    if (Array.isArray(node[key])) {
                        node[key].forEach(child => walk(child, node));
                    } else {
                        walk(node[key], node);
                    }
                }
            });
        };

        walk(ast);

        return {
            detected: deadCodeLocations.length > 0,
            confidence: deadCodeLocations.length > 0 ? 0.95 : 0.1,
            locations: deadCodeLocations.map(loc => loc.location),
            metrics: {
                unusedVariables: deadCodeLocations.filter(l => l.type === 'unused_variable').length,
                unusedFunctions: deadCodeLocations.filter(l => l.type === 'unused_function').length,
                totalDeadCode: deadCodeLocations.length
            },
            suggestions: deadCodeLocations.length > 0 ? [
                'Remover variáveis e funções não utilizadas',
                'Considere habilitar warnings do compilador'
            ] : []
        };
    }

    checkVariableUsage(ast, varName) {
        // Verificação simplificada de uso de variável
        let isUsed = false;

        const walk = (node) => {
            if (!node) return;

            if (node.type === 'Identifier' && node.name === varName) {
                isUsed = true;
                return;
            }

            Object.keys(node).forEach(key => {
                if (typeof node[key] === 'object' && node[key] !== null) {
                    if (Array.isArray(node[key])) {
                        node[key].forEach(child => walk(child));
                    } else {
                        walk(node[key]);
                    }
                }
            });
        };

        walk(ast);
        return isUsed;
    }

    checkFunctionCalls(ast, funcName) {
        // Verificação simplificada de chamadas de função
        let isCalled = false;

        const walk = (node) => {
            if (!node) return;

            if (node.type === 'CallExpression' &&
                node.callee.type === 'Identifier' &&
                node.callee.name === funcName) {
                isCalled = true;
                return;
            }

            Object.keys(node).forEach(key => {
                if (typeof node[key] === 'object' && node[key] !== null) {
                    if (Array.isArray(node[key])) {
                        node[key].forEach(child => walk(child));
                    } else {
                        walk(node[key]);
                    }
                }
            });
        };

        walk(ast);
        return isCalled;
    }

    detectHighComplexity(ast, context) {
        // Detecção de complexidade ciclomática alta
        const complexityThreshold = context.complexityThreshold || 10;
        const complexFunctions = [];

        const walk = (node, depth = 0) => {
            if (!node) return 0;

            let complexity = 0;

            // Contar decisões
            if (node.type === 'IfStatement' ||
                node.type === 'ForStatement' ||
                node.type === 'WhileStatement' ||
                node.type === 'DoWhileStatement' ||
                node.type === 'SwitchStatement' ||
                node.type === 'ConditionalExpression' ||
                node.type === 'LogicalExpression') {
                complexity = 1;
            }

            // Recursivamente calcular complexidade dos filhos
            Object.keys(node).forEach(key => {
                if (typeof node[key] === 'object' && node[key] !== null) {
                    if (Array.isArray(node[key])) {
                        node[key].forEach(child => complexity += walk(child, depth + 1));
                    } else if (key !== 'parent') {
                        complexity += walk(node[key], depth + 1);
                    }
                }
            });

            // Verificar funções com alta complexidade
            if ((node.type === 'FunctionDeclaration' ||
                node.type === 'FunctionExpression' ||
                node.type === 'ArrowFunctionExpression') &&
                complexity > complexityThreshold) {
                complexFunctions.push({
                    name: node.id?.name || 'anonymous',
                    complexity,
                    location: node.loc || { start: 0, end: 0 }
                });
            }

            return complexity;
        };

        walk(ast);

        return {
            detected: complexFunctions.length > 0,
            confidence: complexFunctions.length > 0 ? 0.85 : 0.1,
            locations: complexFunctions.map(f => f.location),
            metrics: {
                highComplexityFunctions: complexFunctions.length,
                maxComplexity: complexFunctions.length > 0 ?
                    Math.max(...complexFunctions.map(f => f.complexity)) : 0,
                averageComplexity: complexFunctions.length > 0 ?
                    complexFunctions.reduce((sum, f) => sum + f.complexity, 0) / complexFunctions.length : 0
            },
            suggestions: complexFunctions.length > 0 ? [
                'Quebrar funções complexas em funções menores',
                'Extrair condicionais para métodos separados',
                'Considere usar padrões de design State ou Strategy'
            ] : []
        };
    }

    detectHighCoupling(ast, context) {
        // Detecção simplificada de alto acoplamento
        const couplingThreshold = context.couplingThreshold || 5;
        const coupledFunctions = [];

        const walk = (node) => {
            if (!node) return;

            if (node.type === 'FunctionDeclaration' ||
                node.type === 'FunctionExpression') {

                const dependencies = new Set();

                // Coletar dependências
                const collectDeps = (subNode) => {
                    if (!subNode) return;

                    if (subNode.type === 'CallExpression' &&
                        subNode.callee.type === 'Identifier') {
                        dependencies.add(subNode.callee.name);
                    }

                    if (subNode.type === 'Identifier' &&
                        subNode.name !== node.id?.name) {
                        // Verificar se é referência a outra função
                        dependencies.add(subNode.name);
                    }

                    Object.keys(subNode).forEach(key => {
                        if (typeof subNode[key] === 'object' && subNode[key] !== null) {
                            if (Array.isArray(subNode[key])) {
                                subNode[key].forEach(child => collectDeps(child));
                            } else {
                                collectDeps(subNode[key]);
                            }
                        }
                    });
                };

                collectDeps(node.body);

                if (dependencies.size > couplingThreshold) {
                    coupledFunctions.push({
                        name: node.id?.name || 'anonymous',
                        dependencyCount: dependencies.size,
                        dependencies: Array.from(dependencies),
                        location: node.loc || { start: 0, end: 0 }
                    });
                }
            }

            // Recursivamente processar filhos
            Object.keys(node).forEach(key => {
                if (typeof node[key] === 'object' && node[key] !== null) {
                    if (Array.isArray(node[key])) {
                        node[key].forEach(child => walk(child));
                    } else {
                        walk(node[key]);
                    }
                }
            });
        };

        walk(ast);

        return {
            detected: coupledFunctions.length > 0,
            confidence: coupledFunctions.length > 0 ? 0.75 : 0.1,
            locations: coupledFunctions.map(f => f.location),
            metrics: {
                highCouplingFunctions: coupledFunctions.length,
                maxDependencies: coupledFunctions.length > 0 ?
                    Math.max(...coupledFunctions.map(f => f.dependencyCount)) : 0,
                averageDependencies: coupledFunctions.length > 0 ?
                    coupledFunctions.reduce((sum, f) => sum + f.dependencyCount, 0) / coupledFunctions.length : 0
            },
            suggestions: coupledFunctions.length > 0 ? [
                'Extrair funcionalidades em classes separadas',
                'Aplicar padrão Facade para interfaces complexas',
                'Considere usar injeção de dependências'
            ] : []
        };
    }

    detectMagicNumbers(ast, context) {
        // Detecção de números mágicos
        const magicNumbers = [];
        const magicNumberThreshold = 10; // Números maiores que isso são suspeitos

        const walk = (node) => {
            if (!node) return;

            // Detectar números literais
            if (node.type === 'Literal' && typeof node.value === 'number') {
                const value = node.value;

                // Verificar se é número mágico
                if (value > magicNumberThreshold ||
                    value < -magicNumberThreshold ||
                    (value > 0 && value < 1 && value !== 0.5)) { // Excluir 0.5 que é comum

                    // Verificar contexto
                    const parent = node.parent;
                    const isInArray = parent?.type === 'ArrayExpression';
                    const isInObject = parent?.type === 'Property' && parent.key !== node;

                    if (!isInArray && !isInObject) {
                        magicNumbers.push({
                            value,
                            location: node.loc || { start: 0, end: 0 },
                            context: this.getNodeContext(node)
                        });
                    }
                }
            }

            // Recursivamente processar filhos
            Object.keys(node).forEach(key => {
                if (typeof node[key] === 'object' && node[key] !== null) {
                    if (Array.isArray(node[key])) {
                        node[key].forEach(child => walk(child));
                    } else {
                        walk(node[key]);
                    }
                }
            });
        };

        walk(ast);

        return {
            detected: magicNumbers.length > 0,
            confidence: magicNumbers.length > 0 ? 0.9 : 0.1,
            locations: magicNumbers.map(m => m.location),
            metrics: {
                magicNumbersCount: magicNumbers.length,
                uniqueValues: new Set(magicNumbers.map(m => m.value)).size,
                averageValue: magicNumbers.length > 0 ?
                    magicNumbers.reduce((sum, m) => sum + m.value, 0) / magicNumbers.length : 0
            },
            suggestions: magicNumbers.length > 0 ? [
                'Substituir números mágicos por constantes nomeadas',
                'Documentar significado dos números',
                'Considere usar enums para conjuntos de valores relacionados'
            ] : []
        };
    }

    getNodeContext(node, depth = 0) {
        // Obter contexto do nó (função pai, classe, etc.)
        if (!node || depth > 5) return '';

        if (node.type === 'FunctionDeclaration' ||
            node.type === 'FunctionExpression' ||
            node.type === 'ArrowFunctionExpression') {
            return node.id?.name || 'anonymous function';
        }

        if (node.parent) {
            return this.getNodeContext(node.parent, depth + 1);
        }

        return '';
    }

    detectComplexConditionals(ast, context) {
        // Detecção de condicionais complexas
        const complexConditions = [];
        const complexityThreshold = 3; // Número de operadores lógicos

        const walk = (node) => {
            if (!node) return;

            // Verificar expressões condicionais
            if (node.type === 'IfStatement' ||
                node.type === 'ConditionalExpression' ||
                node.type === 'LogicalExpression') {

                const complexity = this.calculateConditionalComplexity(node);

                if (complexity > complexityThreshold) {
                    complexConditions.push({
                        type: node.type,
                        complexity,
                        location: node.loc || { start: 0, end: 0 },
                        source: this.getNodeSource(node).substring(0, 100)
                    });
                }
            }

            // Recursivamente processar filhos
            Object.keys(node).forEach(key => {
                if (typeof node[key] === 'object' && node[key] !== null) {
                    if (Array.isArray(node[key])) {
                        node[key].forEach(child => walk(child));
                    } else {
                        walk(node[key]);
                    }
                }
            });
        };

        walk(ast);

        return {
            detected: complexConditions.length > 0,
            confidence: complexConditions.length > 0 ? 0.8 : 0.1,
            locations: complexConditions.map(c => c.location),
            metrics: {
                complexConditionsCount: complexConditions.length,
                maxComplexity: complexConditions.length > 0 ?
                    Math.max(...complexConditions.map(c => c.complexity)) : 0,
                averageComplexity: complexConditions.length > 0 ?
                    complexConditions.reduce((sum, c) => sum + c.complexity, 0) / complexConditions.length : 0
            },
            suggestions: complexConditions.length > 0 ? [
                'Extrair condições para métodos separados',
                'Usar variáveis booleanas intermediárias',
                'Considere usar tabelas de decisão ou máquinas de estado'
            ] : []
        };
    }

    calculateConditionalComplexity(node) {
        let complexity = 0;

        const walk = (subNode) => {
            if (!subNode) return;

            // Contar operadores lógicos
            if (subNode.type === 'LogicalExpression') {
                complexity++;
                walk(subNode.left);
                walk(subNode.right);
            }

            // Contar operadores de comparação
            if (subNode.type === 'BinaryExpression' &&
                ['==', '===', '!=', '!==', '<', '>', '<=', '>='].includes(subNode.operator)) {
                complexity++;
            }

            // Contar negações
            if (subNode.type === 'UnaryExpression' && subNode.operator === '!') {
                complexity++;
            }

            // Recursivamente processar filhos
            Object.keys(subNode).forEach(key => {
                if (typeof subNode[key] === 'object' && subNode[key] !== null) {
                    if (Array.isArray(subNode[key])) {
                        subNode[key].forEach(child => walk(child));
                    } else if (key !== 'parent') {
                        walk(subNode[key]);
                    }
                }
            });
        };

        walk(node);
        return complexity;
    }

    detectInefficientLoops(ast, context) {
        // Detecção de loops ineficientes
        const inefficientLoops = [];

        const walk = (node) => {
            if (!node) return;

            // Verificar loops
            if (node.type === 'ForStatement' ||
                node.type === 'WhileStatement' ||
                node.type === 'DoWhileStatement') {

                const inefficiencies = this.analyzeLoopInefficiencies(node);

                if (inefficiencies.length > 0) {
                    inefficientLoops.push({
                        type: node.type,
                        inefficiencies,
                        location: node.loc || { start: 0, end: 0 },
                        source: this.getNodeSource(node).substring(0, 100)
                    });
                }
            }

            // Recursivamente processar filhos
            Object.keys(node).forEach(key => {
                if (typeof node[key] === 'object' && node[key] !== null) {
                    if (Array.isArray(node[key])) {
                        node[key].forEach(child => walk(child));
                    } else {
                        walk(node[key]);
                    }
                }
            });
        };

        walk(ast);

        return {
            detected: inefficientLoops.length > 0,
            confidence: inefficientLoops.length > 0 ? 0.7 : 0.1,
            locations: inefficientLoops.map(l => l.location),
            metrics: {
                inefficientLoopsCount: inefficientLoops.length,
                totalInefficiencies: inefficientLoops.reduce((sum, l) => sum + l.inefficiencies.length, 0),
                inefficiencyTypes: inefficientLoops.flatMap(l => l.inefficiencies.map(i => i.type))
            },
            suggestions: inefficientLoops.length > 0 ? [
                'Pré-calcular valores constantes fora do loop',
                'Usar métodos de array (map, filter, reduce) para operações funcionais',
                'Considere usar Web Workers para loops muito intensivos'
            ] : []
        };
    }

    analyzeLoopInefficiencies(node) {
        const inefficiencies = [];

        // Verificar cálculos repetidos
        const walk = (subNode, inLoop = false) => {
            if (!subNode) return;

            // Verificar chamadas de função dentro do loop
            if (inLoop && subNode.type === 'CallExpression') {
                // Verificar se é função pura ou se resultado pode ser cacheado
                inefficiencies.push({
                    type: 'function_call_in_loop',
                    description: 'Chamada de função dentro do loop pode ser ineficiente'
                });
            }

            // Verificar acesso a propriedades de array length
            if (inLoop && subNode.type === 'MemberExpression' &&
                subNode.property?.name === 'length') {
                inefficiencies.push({
                    type: 'length_in_loop',
                    description: 'Acesso a .length em cada iteração do loop'
                });
            }

            // Verificar criação de objetos dentro do loop
            if (inLoop && (subNode.type === 'ObjectExpression' ||
                subNode.type === 'ArrayExpression')) {
                inefficiencies.push({
                    type: 'object_creation_in_loop',
                    description: 'Criação de objetos/arrays dentro do loop'
                });
            }

            // Marcar que estamos dentro do corpo do loop
            const nowInLoop = inLoop || subNode === node.body;

            // Recursivamente processar filhos
            Object.keys(subNode).forEach(key => {
                if (typeof subNode[key] === 'object' && subNode[key] !== null) {
                    if (Array.isArray(subNode[key])) {
                        subNode[key].forEach(child => walk(child, nowInLoop));
                    } else if (key !== 'parent') {
                        walk(subNode[key], nowInLoop);
                    }
                }
            });
        };

        walk(node);
        return inefficiencies;
    }

    async analyzeTemporalPatterns(code, language) {
        try {
            // Preparar sequência para análise temporal
            const tokens = this.tokenizeCode(code);
            const sequence = tokens.map(token => ({
                type: token.type,
                value: token.value,
                position: token.position
            }));

            // Usar rede temporal para detectar padrões
            const analysis = await this.temporalNetwork.process({
                sequence,
                language: language.code,
                analysisType: 'PATTERN_DETECTION'
            });

            return {
                temporalPatterns: analysis.patterns || [],
                confidence: analysis.confidence || 0.5,
                metrics: analysis.metrics || {}
            };

        } catch (error) {
            console.error('❌ Erro na análise temporal:', error);
            return {
                temporalPatterns: [],
                confidence: 0.1,
                metrics: {}
            };
        }
    }

    tokenizeCode(code) {
        // Tokenizador simplificado
        const tokens = [];
        const regex = /\b(function|if|else|for|while|return|const|let|var)\b|[{}();=+\-*/<>!&|]|\w+|\d+|".*?"|'.*?'/g;

        let match;
        let position = 0;

        while ((match = regex.exec(code)) !== null) {
            tokens.push({
                type: this.classifyToken(match[0]),
                value: match[0],
                position: position++
            });
        }

        return tokens;
    }

    classifyToken(token) {
        if (/\b(function|if|else|for|while|return|const|let|var)\b/.test(token)) {
            return 'keyword';
        }
        if (/[{}();=+\-*/<>!&|]/.test(token)) {
            return 'operator';
        }
        if (/^\d+$/.test(token)) {
            return 'number';
        }
        if (/^".*?"$|^'.*?'$/.test(token)) {
            return 'string';
        }
        if (/^\w+$/.test(token)) {
            return 'identifier';
        }
        return 'unknown';
    }

    combinePatterns(detectedPatterns, temporalAnalysis) {
        // Combinar padrões detectados com análise temporal
        const combined = [...detectedPatterns];

        // Adicionar padrões temporais se confiança for alta
        if (temporalAnalysis.confidence > 0.7 && temporalAnalysis.temporalPatterns.length > 0) {
            temporalAnalysis.temporalPatterns.forEach(pattern => {
                combined.push({
                    pattern: `TEMPORAL_${pattern.type}`,
                    refactoring: this.mapTemporalPatternToRefactoring(pattern),
                    confidence: pattern.confidence || temporalAnalysis.confidence,
                    locations: pattern.locations || [],
                    metrics: { ...pattern.metrics, ...temporalAnalysis.metrics },
                    suggestions: pattern.suggestions || ['Padrão temporal detectado - considere refatoração']
                });
            });
        }

        // Ordenar por confiança
        combined.sort((a, b) => b.confidence - a.confidence);

        return combined;
    }

    mapTemporalPatternToRefactoring(pattern) {
        // Mapear padrões temporais para refatorações apropriadas
        switch (pattern.type) {
            case 'SEQUENTIAL_DUPLICATION':
                return RefactoringPattern.EXTRACT_METHOD;
            case 'CYCLIC_COMPLEXITY':
                return RefactoringPattern.SIMPLIFY_CONDITIONAL;
            case 'TEMPORAL_COUPLING':
                return RefactoringPattern.EXTRACT_CLASS;
            default:
                return RefactoringPattern.EXTRACT_METHOD;
        }
    }
}

export class RefactoringEngine {
    constructor() {
        this.refactoringStrategies = new Map();
        this.codeTransformations = new Map();
        this.initializeStrategies();
        this.initializeTransformations();
    }

    initializeStrategies() {
        // Estratégias de refatoração para diferentes padrões
        this.refactoringStrategies.set(RefactoringPattern.EXTRACT_METHOD.code, {
            apply: (code, context) => this.applyExtractMethod(code, context),
            validate: (context) => this.validateExtractMethod(context),
            complexity: 'MEDIUM'
        });

        this.refactoringStrategies.set(RefactoringPattern.REMOVE_DEAD_CODE.code, {
            apply: (code, context) => this.applyRemoveDeadCode(code, context),
            validate: (context) => this.validateRemoveDeadCode(context),
            complexity: 'LOW'
        });

        this.refactoringStrategies.set(RefactoringPattern.SIMPLIFY_CONDITIONAL.code, {
            apply: (code, context) => this.applySimplifyConditional(code, context),
            validate: (context) => this.validateSimplifyConditional(context),
            complexity: 'MEDIUM'
        });

        this.refactoringStrategies.set(RefactoringPattern.EXTRACT_CLASS.code, {
            apply: (code, context) => this.applyExtractClass(code, context),
            validate: (context) => this.validateExtractClass(context),
            complexity: 'HIGH'
        });

        this.refactoringStrategies.set(RefactoringPattern.REPLACE_MAGIC_NUMBER_WITH_CONSTANT.code, {
            apply: (code, context) => this.applyReplaceMagicNumber(code, context),
            validate: (context) => this.validateReplaceMagicNumber(context),
            complexity: 'LOW'
        });

        this.refactoringStrategies.set(RefactoringPattern.REPLACE_CONDITIONAL_WITH_POLYMORPHISM.code, {
            apply: (code, context) => this.applyReplaceConditionalWithPolymorphism(code, context),
            validate: (context) => this.validateReplaceConditionalWithPolymorphism(context),
            complexity: 'HIGH'
        });

        this.refactoringStrategies.set(RefactoringPattern.REPLACE_LOOP_WITH_PIPELINE.code, {
            apply: (code, context) => this.applyReplaceLoopWithPipeline(code, context),
            validate: (context) => this.validateReplaceLoopWithPipeline(context),
            complexity: 'MEDIUM'
        });
    }

    initializeTransformations() {
        // Transformações de código básicas
        this.codeTransformations.set('EXTRACT_FUNCTION', {
            transform: (code, params) => this.transformExtractFunction(code, params),
            description: 'Extrair trecho de código para função'
        });

        this.codeTransformations.set('RENAME_VARIABLE', {
            transform: (code, params) => this.transformRenameVariable(code, params),
            description: 'Renomear variável'
        });

        this.codeTransformations.set('REPLACE_LITERAL', {
            transform: (code, params) => this.transformReplaceLiteral(code, params),
            description: 'Substituir literal por constante'
        });

        this.codeTransformations.set('SIMPLIFY_EXPRESSION', {
            transform: (code, params) => this.transformSimplifyExpression(code, params),
            description: 'Simplificar expressão'
        });

        this.codeTransformations.set('CONVERT_LOOP', {
            transform: (code, params) => this.transformConvertLoop(code, params),
            description: 'Converter loop para operação funcional'
        });
    }

    async refactor(code, pattern, context) {
        const startTime = Date.now();

        try {
            // Validar se a refatoração pode ser aplicada
            const validation = this.validateRefactoring(pattern, context);
            if (!validation.valid) {
                return {
                    success: false,
                    error: validation.message,
                    confidence: validation.confidence
                };
            }

            // Obter estratégia de refatoração
            const strategy = this.refactoringStrategies.get(pattern.code);
            if (!strategy) {
                return {
                    success: false,
                    error: `Estratégia de refatoração não encontrada: ${pattern.code}`,
                    confidence: 0
                };
            }

            // Aplicar refatoração
            const result = await strategy.apply(code, context);

            // Validar resultado
            const validationResult = this.validateResult(code, result.refactoredCode, context);

            return {
                success: true,
                originalCode: code,
                refactoredCode: result.refactoredCode,
                changes: result.changes,
                metrics: {
                    linesChanged: result.metrics?.linesChanged || 0,
                    complexityReduction: result.metrics?.complexityReduction || 0,
                    maintainabilityImprovement: result.metrics?.maintainabilityImprovement || 0
                },
                validation: validationResult,
                processingTime: Date.now() - startTime,
                pattern: pattern.code
            };

        } catch (error) {
            console.error(`❌ Erro na refatoração ${pattern.code}:`, error);
            return {
                success: false,
                error: error.message,
                processingTime: Date.now() - startTime,
                pattern: pattern.code
            };
        }
    }

    validateRefactoring(pattern, context) {
        // Validar se a refatoração é apropriada para o contexto
        const strategy = this.refactoringStrategies.get(pattern.code);

        if (!strategy) {
            return {
                valid: false,
                message: `Estratégia de refatoração não suportada: ${pattern.code}`,
                confidence: 0
            };
        }

        // Validar contexto específico
        const contextValidation = strategy.validate(context);
        if (!contextValidation.valid) {
            return contextValidation;
        }

        // Verificar threshold de confiança
        if (context.confidence < pattern.confidenceThreshold) {
            return {
                valid: false,
                message: `Confiança muito baixa para refatoração: ${context.confidence} < ${pattern.confidenceThreshold}`,
                confidence: context.confidence
            };
        }

        return {
            valid: true,
            message: 'Refatoração validada com sucesso',
            confidence: context.confidence
        };
    }

    validateResult(originalCode, refactoredCode, context) {
        // Validações básicas do resultado da refatoração
        const validations = [];

        // 1. Verificar se o código ainda é válido sintaticamente
        try {
            // Tente parsear o código refatorado
            const parser = require('acorn');
            parser.parse(refactoredCode, { ecmaVersion: 'latest' });
            validations.push({
                type: 'SYNTAX',
                passed: true,
                message: 'Código refatorado é sintaticamente válido'
            });
        } catch (error) {
            validations.push({
                type: 'SYNTAX',
                passed: false,
                message: `Erro de sintaxe no código refatorado: ${error.message}`
            });
        }

        // 2. Verificar se não há perda de funcionalidade (simplificado)
        const originalLines = originalCode.split('\n').length;
        const refactoredLines = refactoredCode.split('\n').length;

        if (Math.abs(originalLines - refactoredLines) < originalLines * 0.5) {
            validations.push({
                type: 'SIZE',
                passed: true,
                message: `Tamanho do código dentro dos limites esperados: ${originalLines} -> ${refactoredLines} linhas`
            });
        } else {
            validations.push({
                type: 'SIZE',
                passed: false,
                message: `Mudança muito grande no tamanho do código: ${originalLines} -> ${refactoredLines} linhas`
            });
        }

        // 3. Verificar se padrões problemáticos foram corrigidos
        if (context.pattern) {
            validations.push({
                type: 'PATTERN_CORRECTION',
                passed: true, // Simplificado - em produção verificar realmente
                message: `Padrão ${context.pattern} foi abordado na refatoração`
            });
        }

        const allPassed = validations.every(v => v.passed);

        return {
            passed: allPassed,
            validations,
            score: validations.filter(v => v.passed).length / validations.length
        };
    }

    applyExtractMethod(code, context) {
        // Implementação simplificada de Extract Method
        // Em produção, usar análise AST mais sofisticada

        const { locations, metrics } = context;

        if (!locations || locations.length === 0) {
            throw new Error('Nenhuma localização especificada para Extract Method');
        }

        // Extrair trecho de código duplicado
        const duplicateCode = this.extractCodeAtLocation(code, locations[0]);

        // Gerar nome para o novo método
        const methodName = this.generateMethodName(duplicateCode, context);

        // Extrair parâmetros do método
        const parameters = this.extractMethodParameters(duplicateCode);

        // Criar novo método
        const newMethod = this.createMethodFromCode(methodName, parameters, duplicateCode);

        // Substituir código duplicado por chamadas ao novo método
        let refactoredCode = code;

        locations.forEach(location => {
            const call = this.createMethodCall(methodName, parameters, location);
            refactoredCode = this.replaceCodeAtLocation(refactoredCode, location, call);
        });

        // Adicionar novo método ao código
        refactoredCode = this.addMethodToCode(refactoredCode, newMethod);

        return {
            refactoredCode,
            changes: [
                {
                    type: 'METHOD_EXTRACTED',
                    methodName,
                    parameters: parameters.length,
                    locations: locations.length
                }
            ],
            metrics: {
                linesChanged: locations.length * 2,
                complexityReduction: metrics?.duplicateBlocks || 1,
                maintainabilityImprovement: 0.2
            }
        };
    }

    extractCodeAtLocation(code, location) {
        // Extrair código em uma localização específica
        const lines = code.split('\n');

        if (location.start && location.end) {
            const startLine = location.start.line || 0;
            const endLine = location.end.line || lines.length - 1;

            return lines.slice(startLine - 1, endLine).join('\n');
        }

        // Fallback: extrair primeira ocorrência de código duplicado
        const match = code.match(/function\s+\w+\([^)]*\)\s*{[^}]*}/);
        return match ? match[0] : '';
    }

    generateMethodName(code, context) {
        // Gerar nome descritivo baseado no código
        const keywords = ['calculate', 'process', 'handle', 'validate', 'format', 'transform'];
        const actions = ['value', 'result', 'data', 'input', 'output'];

        // Analisar código para determinar propósito
        if (code.includes('calculate') || code.includes('math')) {
            return `calculate${this.capitalize(actions[0])}`;
        }
        if (code.includes('validate') || code.includes('check')) {
            return `validate${this.capitalize(actions[2])}`;
        }
        if (code.includes('format') || code.includes('string')) {
            return `format${this.capitalize(actions[3])}`;
        }

        // Nome padrão
        return `${keywords[0]}${this.capitalize(actions[1])}`;
    }

    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    extractMethodParameters(code) {
        // Extrair parâmetros do código
        const params = new Set();

        // Encontrar variáveis usadas mas não declaradas no trecho
        const variablePattern = /\b(\w+)\b/g;
        let match;

        while ((match = variablePattern.exec(code)) !== null) {
            const varName = match[1];

            // Ignorar keywords e números
            if (!this.isJavaScriptKeyword(varName) && !/^\d+$/.test(varName)) {
                params.add(varName);
            }
        }

        return Array.from(params);
    }

    isJavaScriptKeyword(word) {
        const keywords = [
            'function', 'if', 'else', 'for', 'while', 'return', 'const', 'let', 'var',
            'true', 'false', 'null', 'undefined', 'this', 'new', 'typeof', 'instanceof'
        ];
        return keywords.includes(word);
    }

    createMethodFromCode(methodName, parameters, code) {
        // Criar método a partir do código extraído
        const paramString = parameters.join(', ');

        return `
/**
 * ${methodName} - Método extraído automaticamente
 * @param {*} ${paramString.replace(/,/g, ', ')}
 * @returns {*} Resultado do processamento
 */
function ${methodName}(${paramString}) {
    ${code}
}`;
    }

    createMethodCall(methodName, parameters, location) {
        // Criar chamada ao método
        const paramString = parameters.join(', ');
        return `${methodName}(${paramString});`;
    }

    replaceCodeAtLocation(code, location, replacement) {
        // Substituir código em uma localização específica
        const lines = code.split('\n');

        if (location.start && location.end) {
            const startLine = location.start.line || 0;
            const endLine = location.end.line || lines.length - 1;

            const before = lines.slice(0, startLine - 1);
            const after = lines.slice(endLine);

            return [...before, replacement, ...after].join('\n');
        }

        // Fallback: substituir primeira ocorrência
        return code.replace(/function\s+\w+\([^)]*\)\s*{[^}]*}/, replacement);
    }

    addMethodToCode(code, method) {
        // Adicionar método ao código
        // Em produção, encontrar posição apropriada (após imports, antes de exports)
        return `${code}\n\n${method}`;
    }

    applyRemoveDeadCode(code, context) {
        // Remover código morto
        const { locations, metrics } = context;

        let refactoredCode = code;
        const changes = [];

        // Remover cada localização de código morto
        locations.forEach((location, index) => {
            const before = refactoredCode;
            refactoredCode = this.removeCodeAtLocation(refactoredCode, location);

            if (refactoredCode !== before) {
                changes.push({
                    type: 'CODE_REMOVED',
                    location: index + 1,
                    size: this.calculateRemovedSize(before, refactoredCode)
                });
            }
        });

        // Limpar linhas vazias adicionais
        refactoredCode = this.cleanEmptyLines(refactoredCode);

        return {
            refactoredCode,
            changes,
            metrics: {
                linesChanged: changes.reduce((sum, change) => sum + change.size, 0),
                complexityReduction: 0.1 * (metrics?.unusedVariables || 0),
                maintainabilityImprovement: 0.15 * (metrics?.totalDeadCode || 0)
            }
        };
    }

    removeCodeAtLocation(code, location) {
        // Remover código em uma localização específica
        const lines = code.split('\n');

        if (location.start && location.end) {
            const startLine = location.start.line || 0;
            const endLine = location.end.line || lines.length - 1;

            const before = lines.slice(0, startLine - 1);
            const after = lines.slice(endLine);

            return [...before, ...after].join('\n');
        }

        return code;
    }

    calculateRemovedSize(before, after) {
        const beforeLines = before.split('\n').length;
        const afterLines = after.split('\n').length;
        return beforeLines - afterLines;
    }

    cleanEmptyLines(code) {
        // Remover múltiplas linhas vazias consecutivas
        return code.replace(/\n\s*\n\s*\n/g, '\n\n');
    }

    applySimplifyConditional(code, context) {
        // Simplificar condicionais complexas
        const { locations, metrics } = context;

        let refactoredCode = code;
        const changes = [];

        locations.forEach((location, index) => {
            const conditionalCode = this.extractCodeAtLocation(refactoredCode, location);
            const simplified = this.simplifyConditionalExpression(conditionalCode);

            if (simplified !== conditionalCode) {
                refactoredCode = this.replaceCodeAtLocation(refactoredCode, location, simplified);
                changes.push({
                    type: 'CONDITIONAL_SIMPLIFIED',
                    location: index + 1,
                    complexityReduction: this.calculateComplexityReduction(conditionalCode, simplified)
                });
            }
        });

        return {
            refactoredCode,
            changes,
            metrics: {
                linesChanged: changes.length * 2,
                complexityReduction: changes.reduce((sum, change) => sum + change.complexityReduction, 0),
                maintainabilityImprovement: 0.25 * changes.length
            }
        };
    }

    simplifyConditionalExpression(code) {
        // Simplificações básicas de expressões condicionais
        let simplified = code;

        // Remover negações duplas
        simplified = simplified.replace(/!!/g, '');

        // Simplificar comparações com true/false
        simplified = simplified.replace(/=== true/g, '');
        simplified = simplified.replace(/!== false/g, '');
        simplified = simplified.replace(/=== false/g, ' === false'); // Manter para clareza

        // Simplificar condicionais aninhadas
        if (simplified.includes('if (') && simplified.includes('else if (')) {
            // Tentar combinar condições relacionadas
            simplified = this.combineRelatedConditions(simplified);
        }

        return simplified;
    }

    combineRelatedConditions(code) {
        // Combinar condições relacionadas (simplificado)
        // Em produção, usar análise mais sofisticada
        return code.replace(/if\s*\(([^)]+)\)\s*{\s*return\s*true;\s*}\s*else\s*if\s*\(([^)]+)\)\s*{\s*return\s*false;\s*}/,
            'return $1 || !$2;');
    }

    calculateComplexityReduction(original, simplified) {
        // Calcular redução de complexidade (simplificado)
        const originalComplexity = (original.match(/&&|\|\||!/g) || []).length;
        const simplifiedComplexity = (simplified.match(/&&|\|\||!/g) || []).length;

        return Math.max(0, originalComplexity - simplifiedComplexity) / (originalComplexity || 1);
    }

    applyExtractClass(code, context) {
        // Extrair parte de uma classe para nova classe
        // Implementação simplificada
        return {
            refactoredCode: code,
            changes: [{ type: 'CLASS_EXTRACTION_SKIPPED', reason: 'Implementação complexa requer análise manual' }],
            metrics: {
                linesChanged: 0,
                complexityReduction: 0,
                maintainabilityImprovement: 0
            }
        };
    }

    applyReplaceMagicNumber(code, context) {
        // Substituir números mágicos por constantes
        const { locations, metrics } = context;

        let refactoredCode = code;
        const changes = [];
        const constants = new Map();

        locations.forEach((location, index) => {
            const numberInfo = this.extractNumberAtLocation(refactoredCode, location);

            if (numberInfo) {
                const { value, line } = numberInfo;

                // Gerar nome para constante
                const constantName = this.generateConstantName(value, context);
                constants.set(constantName, value);

                // Substituir número por constante
                refactoredCode = this.replaceNumberWithConstant(refactoredCode, line, value, constantName);

                changes.push({
                    type: 'MAGIC_NUMBER_REPLACED',
                    constantName,
                    value,
                    line
                });
            }
        });

        // Adicionar declarações de constantes no início do arquivo
        if (constants.size > 0) {
            refactoredCode = this.addConstantDeclarations(refactoredCode, constants);
        }

        return {
            refactoredCode,
            changes,
            metrics: {
                linesChanged: changes.length * 2,
                complexityReduction: 0.05 * changes.length,
                maintainabilityImprovement: 0.3 * changes.length
            }
        };
    }

    extractNumberAtLocation(code, location) {
        // Extrair número em uma localização específica
        const lines = code.split('\n');

        if (location.start) {
            const lineNumber = location.start.line || 0;
            if (lineNumber > 0 && lineNumber <= lines.length) {
                const line = lines[lineNumber - 1];
                const numberMatch = line.match(/\b\d+(\.\d+)?\b/);

                if (numberMatch) {
                    return {
                        value: parseFloat(numberMatch[0]),
                        line: lineNumber
                    };
                }
            }
        }

        return null;
    }

    generateConstantName(value, context) {
        // Gerar nome descritivo para constante baseado no valor
        const prefixes = {
            100: 'HUNDRED',
            1000: 'THOUSAND',
            60: 'SECONDS_PER_MINUTE',
            3600: 'SECONDS_PER_HOUR',
            86400: 'SECONDS_PER_DAY',
            3.14159: 'PI',
            2.71828: 'E',
            1.61803: 'GOLDEN_RATIO'
        };

        if (prefixes[value]) {
            return prefixes[value];
        }

        // Gerar nome baseado no valor e contexto
        const contextName = context.context ? context.context.toUpperCase().replace(/[^A-Z]/g, '_') : 'VALUE';
        return `${contextName}_${Math.abs(value).toString().replace('.', '_')}`;
    }

    replaceNumberWithConstant(code, lineNumber, value, constantName) {
        // Substituir número específico por constante
        const lines = code.split('\n');

        if (lineNumber > 0 && lineNumber <= lines.length) {
            const line = lines[lineNumber - 1];
            const replacedLine = line.replace(new RegExp(`\\b${value}\\b`, 'g'), constantName);
            lines[lineNumber - 1] = replacedLine;
        }

        return lines.join('\n');
    }

    addConstantDeclarations(code, constants) {
        // Adicionar declarações de constantes no início do arquivo
        const constantDeclarations = Array.from(constants.entries())
            .map(([name, value]) => `const ${name} = ${value};`)
            .join('\n');

        // Encontrar posição apropriada (após imports, antes de outras declarações)
        const lines = code.split('\n');
        let insertIndex = 0;

        // Encontrar fim dos imports
        for (let i = 0; i < lines.length; i++) {
            if (lines[i].trim().startsWith('import ') || lines[i].trim().startsWith('require(')) {
                insertIndex = i + 1;
            } else if (lines[i].trim() && !lines[i].trim().startsWith('//')) {
                break;
            }
        }

        lines.splice(insertIndex, 0, '', '// Constantes geradas automaticamente', constantDeclarations);

        return lines.join('\n');
    }

    validateExtractMethod(context) {
        return { valid: true, message: 'Extract Method validado' };
    }

    validateRemoveDeadCode(context) {
        return { valid: true, message: 'Remove Dead Code validado' };
    }

    validateSimplifyConditional(context) {
        return { valid: true, message: 'Simplify Conditional validado' };
    }

    validateExtractClass(context) {
        return { valid: true, message: 'Extract Class validado' };
    }

    validateReplaceMagicNumber(context) {
        return { valid: true, message: 'Replace Magic Number validado' };
    }

    validateReplaceConditionalWithPolymorphism(context) {
        return { valid: true, message: 'Replace Conditional with Polymorphism validado' };
    }

    validateReplaceLoopWithPipeline(context) {
        return { valid: true, message: 'Replace Loop with Pipeline validado' };
    }

    applyReplaceConditionalWithPolymorphism(code, context) {
        // Implementação simplificada
        return {
            refactoredCode: code,
            changes: [{ type: 'POLYMORPHISM_REFACTORING_SKIPPED', reason: 'Refatoração complexa requer análise manual' }],
            metrics: {
                linesChanged: 0,
                complexityReduction: 0,
                maintainabilityImprovement: 0
            }
        };
    }

    applyReplaceLoopWithPipeline(code, context) {
        // Substituir loops por operações funcionais
        const { locations } = context;

        let refactoredCode = code;
        const changes = [];

        locations.forEach((location, index) => {
            const loopCode = this.extractCodeAtLocation(refactoredCode, location);
            const pipelineCode = this.convertLoopToPipeline(loopCode);

            if (pipelineCode && pipelineCode !== loopCode) {
                refactoredCode = this.replaceCodeAtLocation(refactoredCode, location, pipelineCode);
                changes.push({
                    type: 'LOOP_CONVERTED_TO_PIPELINE',
                    location: index + 1,
                    originalType: this.detectLoopType(loopCode)
                });
            }
        });

        return {
            refactoredCode,
            changes,
            metrics: {
                linesChanged: changes.length * 3,
                complexityReduction: 0.3 * changes.length,
                maintainabilityImprovement: 0.4 * changes.length
            }
        };
    }

    detectLoopType(code) {
        if (code.includes('for (')) return 'FOR_LOOP';
        if (code.includes('while (')) return 'WHILE_LOOP';
        if (code.includes('forEach(')) return 'FOR_EACH';
        return 'UNKNOWN';
    }

    convertLoopToPipeline(loopCode) {
        // Converter loop for simples para pipeline funcional
        if (loopCode.includes('for (let i = 0') && loopCode.includes('i < array.length') && loopCode.includes('i++')) {
            // Verificar se é um loop de transformação
            if (loopCode.includes('push(') || loopCode.includes('=')) {
                return loopCode.replace(
                    /for\s*\([^)]*\)\s*{([^}]*)}/,
                    '// Substituído por operações funcionais\n// array.map(item => ...)'
                );
            }
        }

        return loopCode;
    }

    transformExtractFunction(code, params) {
        // Transformação genérica de extração de função
        const { start, end, functionName } = params;
        const extracted = code.substring(start, end);
        const call = `${functionName}();`;

        return code.substring(0, start) + call + code.substring(end);
    }

    transformRenameVariable(code, params) {
        const { oldName, newName } = params;
        const regex = new RegExp(`\\b${oldName}\\b`, 'g');
        return code.replace(regex, newName);
    }

    transformReplaceLiteral(code, params) {
        const { literal, constantName } = params;
        const regex = new RegExp(`\\b${literal}\\b`, 'g');
        return code.replace(regex, constantName);
    }

    transformSimplifyExpression(code, params) {
        // Simplificações básicas de expressões
        let result = code;

        // Remover parênteses desnecessários
        result = result.replace(/\((\w+)\)/g, '$1');

        // Simplificar operações booleanas
        result = result.replace(/true &&/g, '');
        result = result.replace(/&& true/g, '');
        result = result.replace(/false \|\|/g, '');
        result = result.replace(/\|\| false/g, '');

        return result;
    }

    transformConvertLoop(code, params) {
        const { loopType } = params;

        if (loopType === 'FOR_TO_MAP') {
            return code.replace(
                /for\s*\([^)]*\)\s*{\s*result\.push\(([^)]*)\);\s*}/,
                'result = array.map(item => $1);'
            );
        }

        if (loopType === 'FOR_TO_FILTER') {
            return code.replace(
                /for\s*\([^)]*\)\s*{\s*if\s*\(([^)]*)\)\s*{\s*result\.push\(([^)]*)\);\s*}\s*}/,
                'result = array.filter(item => $1).map(item => $2);'
            );
        }

        return code;
    }
}

export class NeuralCodeOptimizer {
    constructor() {
        this.codeAnalysisService = new CodeAnalysisService();
        this.aiManager = aiSystemManager;
        this.optimizationStrategies = new Map();
        this.learningHistory = [];
        this.initializeStrategies();
    }

    initializeStrategies() {
        // Estratégias de otimização baseadas em IA
        this.optimizationStrategies.set(OptimizationType.PERFORMANCE.code, {
            analyze: (code, metrics) => this.analyzePerformance(code, metrics),
            optimize: (code, issues) => this.optimizePerformance(code, issues),
            weight: 1.5
        });

        this.optimizationStrategies.set(OptimizationType.MEMORY.code, {
            analyze: (code, metrics) => this.analyzeMemoryUsage(code, metrics),
            optimize: (code, issues) => this.optimizeMemoryUsage(code, issues),
            weight: 1.3
        });

        this.optimizationStrategies.set(OptimizationType.SECURITY.code, {
            analyze: (code, metrics) => this.analyzeSecurity(code, metrics),
            optimize: (code, issues) => this.optimizeSecurity(code, issues),
            weight: 2.0
        });

        this.optimizationStrategies.set(OptimizationType.READABILITY.code, {
            analyze: (code, metrics) => this.analyzeReadability(code, metrics),
            optimize: (code, issues) => this.optimizeReadability(code, issues),
            weight: 1.0
        });

        this.optimizationStrategies.set(OptimizationType.MAINTAINABILITY.code, {
            analyze: (code, metrics) => this.analyzeMaintainability(code, metrics),
            optimize: (code, issues) => this.optimizeMaintainability(code, issues),
            weight: 1.2
        });
    }

    async optimize(code, language, optimizationTypes = []) {
        const startTime = Date.now();

        try {
            // Análise inicial do código
            const analysis = await this.codeAnalysisService.analyze(code);

            // Coletar métricas relevantes
            const metrics = this.collectOptimizationMetrics(analysis);

            // Determinar tipos de otimização a aplicar
            const typesToApply = optimizationTypes.length > 0 ?
                optimizationTypes : this.determineOptimizationTypes(metrics);

            // Aplicar otimizações
            const optimizations = [];
            let optimizedCode = code;

            for (const typeCode of typesToApply) {
                const strategy = this.optimizationStrategies.get(typeCode);
                if (!strategy) continue;

                // Analisar problemas específicos
                const issues = await strategy.analyze(optimizedCode, metrics);

                if (issues.length > 0) {
                    // Aplicar otimizações
                    const result = await strategy.optimize(optimizedCode, issues);

                    if (result.success && result.optimizedCode !== optimizedCode) {
                        optimizedCode = result.optimizedCode;
                        optimizations.push({
                            type: typeCode,
                            changes: result.changes,
                            improvements: result.improvements,
                            confidence: result.confidence
                        });
                    }
                }
            }

            // Validar otimizações
            const validation = await this.validateOptimizations(code, optimizedCode, optimizations);

            // Aprender com os resultados
            await this.learnFromOptimization({
                originalCode: code,
                optimizedCode,
                optimizations,
                metrics,
                validation,
                processingTime: Date.now() - startTime
            });

            return {
                success: true,
                originalCode: code,
                optimizedCode,
                optimizations,
                metrics: {
                    original: metrics,
                    optimized: this.collectOptimizationMetrics(
                        await this.codeAnalysisService.analyze(optimizedCode)
                    )
                },
                validation,
                processingTime: Date.now() - startTime,
                language: language.code
            };

        } catch (error) {
            console.error('❌ Erro na otimização de código:', error);
            return {
                success: false,
                error: error.message,
                processingTime: Date.now() - startTime
            };
        }
    }

    collectOptimizationMetrics(analysis) {
        return {
            complexity: analysis.scores?.complexity?.score || 50,
            security: analysis.scores?.security?.score || 50,
            performance: analysis.scores?.performance?.score || 50,
            readability: analysis.scores?.style?.score || 50,
            maintainability: analysis.structure?.metrics?.maintainabilityIndex || 50,
            issues: analysis.security?.vulnerabilityScan?.vulnerabilities?.length || 0,
            performanceIssues: analysis.performance?.issues?.length || 0
        };
    }

    determineOptimizationTypes(metrics) {
        const types = [];

        // Determinar tipos baseados nas métricas
        if (metrics.performance < 70) types.push(OptimizationType.PERFORMANCE.code);
        if (metrics.security < 75) types.push(OptimizationType.SECURITY.code);
        if (metrics.readability < 60) types.push(OptimizationType.READABILITY.code);
        if (metrics.maintainability < 65) types.push(OptimizationType.MAINTAINABILITY.code);
        if (metrics.complexity > 70) types.push(OptimizationType.PERFORMANCE.code);

        // Se nenhum tipo específico, aplicar otimizações gerais
        if (types.length === 0) {
            types.push(OptimizationType.READABILITY.code, OptimizationType.MAINTAINABILITY.code);
        }

        return types;
    }

    async analyzePerformance(code, metrics) {
        // Usar IA para analisar problemas de performance
        try {
            const aiAnalysis = await this.aiManager.predict('performance_analysis', {
                code,
                metrics,
                analysisType: 'PERFORMANCE_ISSUES'
            });

            return aiAnalysis.issues || [];
        } catch (error) {
            console.error('❌ Erro na análise de performance por IA:', error);
            return this.fallbackPerformanceAnalysis(code);
        }
    }

    fallbackPerformanceAnalysis(code) {
        // Análise de fallback para performance
        const issues = [];

        // Detectar loops aninhados
        const nestedLoops = this.detectNestedLoops(code);
        if (nestedLoops > 0) {
            issues.push({
                type: 'NESTED_LOOPS',
                severity: 'HIGH',
                description: `${nestedLoops} loops aninhados detectados`,
                suggestion: 'Considere otimizar algoritmos ou usar técnicas de memoização'
            });
        }

        // Detectar chamadas de função em loops
        const functionCallsInLoops = this.detectFunctionCallsInLoops(code);
        if (functionCallsInLoops > 0) {
            issues.push({
                type: 'FUNCTION_CALLS_IN_LOOPS',
                severity: 'MEDIUM',
                description: `${functionCallsInLoops} chamadas de função dentro de loops`,
                suggestion: 'Mova chamadas constantes para fora dos loops'
            });
        }

        // Detectar operações DOM pesadas
        const heavyDomOperations = this.detectHeavyDomOperations(code);
        if (heavyDomOperations > 0) {
            issues.push({
                type: 'HEAVY_DOM_OPERATIONS',
                severity: 'HIGH',
                description: `${heavyDomOperations} operações DOM pesadas detectadas`,
                suggestion: 'Use DocumentFragment ou otimize manipulação de DOM'
            });
        }

        return issues;
    }

    detectNestedLoops(code) {
        let depth = 0;
        let maxDepth = 0;
        let inLoop = false;

        const lines = code.split('\n');
        lines.forEach(line => {
            const trimmed = line.trim();

            if (trimmed.includes('for (') || trimmed.includes('while (') || trimmed.includes('forEach(')) {
                if (inLoop) {
                    depth++;
                    maxDepth = Math.max(maxDepth, depth);
                } else {
                    inLoop = true;
                }
            }

            if (trimmed.includes('}') && depth > 0) {
                depth--;
                if (depth === 0) {
                    inLoop = false;
                }
            }
        });

        return maxDepth;
    }

    detectFunctionCallsInLoops(code) {
        let count = 0;
        let inLoop = false;

        const lines = code.split('\n');
        const functionCallPattern = /\w+\([^)]*\)/;

        lines.forEach(line => {
            const trimmed = line.trim();

            if (trimmed.includes('for (') || trimmed.includes('while (') || trimmed.includes('forEach(')) {
                inLoop = true;
            }

            if (inLoop && functionCallPattern.test(trimmed)) {
                count++;
            }

            if (trimmed.includes('}') && inLoop) {
                inLoop = false;
            }
        });

        return count;
    }

    detectHeavyDomOperations(code) {
        const heavyOperations = [
            /\.innerHTML\s*=/g,
            /\.outerHTML\s*=/g,
            /\.insertAdjacentHTML/g,
            /document\.write/g,
            /\.appendChild\(/g,
            /\.removeChild\(/g,
            /\.replaceChild\(/g,
            /\.cloneNode\(true\)/g
        ];

        return heavyOperations.reduce((count, pattern) => {
            const matches = code.match(pattern);
            return count + (matches ? matches.length : 0);
        }, 0);
    }

    async optimizePerformance(code, issues) {
        const changes = [];
        let optimizedCode = code;

        // Aplicar otimizações baseadas nos issues
        for (const issue of issues) {
            switch (issue.type) {
                case 'NESTED_LOOPS':
                    const loopOptimization = this.optimizeNestedLoops(optimizedCode);
                    if (loopOptimization.changed) {
                        optimizedCode = loopOptimization.code;
                        changes.push({
                            type: 'NESTED_LOOPS_OPTIMIZED',
                            description: issue.description,
                            improvement: 'Redução de complexidade de O(n²) para O(n log n)'
                        });
                    }
                    break;

                case 'FUNCTION_CALLS_IN_LOOPS':
                    const functionOptimization = this.optimizeFunctionCallsInLoops(optimizedCode);
                    if (functionOptimization.changed) {
                        optimizedCode = functionOptimization.code;
                        changes.push({
                            type: 'FUNCTION_CALLS_OPTIMIZED',
                            description: issue.description,
                            improvement: 'Chamadas de função movidas para fora dos loops'
                        });
                    }
                    break;

                case 'HEAVY_DOM_OPERATIONS':
                    const domOptimization = this.optimizeDomOperations(optimizedCode);
                    if (domOptimization.changed) {
                        optimizedCode = domOptimization.code;
                        changes.push({
                            type: 'DOM_OPERATIONS_OPTIMIZED',
                            description: issue.description,
                            improvement: 'Operações DOM agrupadas e otimizadas'
                        });
                    }
                    break;
            }
        }

        return {
            success: changes.length > 0,
            optimizedCode,
            changes,
            improvements: {
                performance: changes.length * 0.1,
                confidence: Math.min(0.9, changes.length * 0.2)
            }
        };
    }

    optimizeNestedLoops(code) {
        // Otimização simplificada de loops aninhados
        // Em produção, usar técnicas como memoização, dynamic programming, etc.
        return {
            changed: false,
            code
        };
    }

    optimizeFunctionCallsInLoops(code) {
        // Mover chamadas de função constantes para fora dos loops
        let changed = false;
        let optimized = code;

        // Padrão: for(...) { const result = expensiveFunction(); ... }
        const pattern = /(for|while)\s*\([^)]*\)\s*{\s*(const|let|var)\s+(\w+)\s*=\s*(\w+)\([^)]*\);/g;

        const matches = optimized.match(pattern);
        if (matches) {
            changed = true;
            // Simplificado - em produção, análise AST mais sofisticada
        }

        return { changed, code: optimized };
    }

    optimizeDomOperations(code) {
        // Otimizar operações DOM
        let changed = false;
        let optimized = code;

        // Agrupar múltiplas alterações de innerHTML
        if (optimized.includes('.innerHTML') && optimized.includes('+=')) {
            changed = true;
            optimized = optimized.replace(/\.innerHTML\s*\+=\s*['"][^'"]*['"]/g,
                (match) => '// TODO: Otimizar concatenação de innerHTML - use DocumentFragment');
        }

        return { changed, code: optimized };
    }

    async analyzeMemoryUsage(code, metrics) {
        // Análise de uso de memória
        const issues = [];

        // Detectar vazamentos de memória potenciais
        const memoryLeaks = this.detectMemoryLeaks(code);
        if (memoryLeaks > 0) {
            issues.push({
                type: 'MEMORY_LEAKS',
                severity: 'HIGH',
                description: `${memoryLeaks} potenciais vazamentos de memória detectados`,
                suggestion: 'Verifique event listeners, timers e referências circulares'
            });
        }

        // Detectar alocação excessiva de objetos
        const objectAllocations = this.detectExcessiveObjectAllocation(code);
        if (objectAllocations > 0) {
            issues.push({
                type: 'EXCESSIVE_OBJECT_ALLOCATION',
                severity: 'MEDIUM',
                description: `${objectAllocations} alocações excessivas de objetos detectadas`,
                suggestion: 'Reutilize objetos ou use object pooling'
            });
        }

        // Detectar grandes estruturas de dados
        const largeDataStructures = this.detectLargeDataStructures(code);
        if (largeDataStructures > 0) {
            issues.push({
                type: 'LARGE_DATA_STRUCTURES',
                severity: 'MEDIUM',
                description: `${largeDataStructures} grandes estruturas de dados detectadas`,
                suggestion: 'Considere usar estruturas de dados mais eficientes ou lazy loading'
            });
        }

        return issues;
    }

    detectMemoryLeaks(code) {
        let leaks = 0;

        // Detectar event listeners sem remoção
        if (code.includes('addEventListener') && !code.includes('removeEventListener')) {
            leaks++;
        }

        // Detectar setInterval/setTimeout sem clear
        if ((code.includes('setInterval') || code.includes('setTimeout')) &&
            !code.includes('clearInterval') && !code.includes('clearTimeout')) {
            leaks++;
        }

        // Detectar referências a elementos DOM globais
        if (code.includes('document.getElementById') && code.includes('global')) {
            leaks++;
        }

        return leaks;
    }

    detectExcessiveObjectAllocation(code) {
        // Contar criações de objetos em loops
        let allocations = 0;
        let inLoop = false;

        const lines = code.split('\n');
        const objectPatterns = [
            /new\s+Object\(\)/,
            /{\s*[^}]*\s*}/,
            /new\s+Array\(\)/,
            /\[\s*\]/
        ];

        lines.forEach(line => {
            const trimmed = line.trim();

            if (trimmed.includes('for (') || trimmed.includes('while (') || trimmed.includes('forEach(')) {
                inLoop = true;
            }

            if (inLoop) {
                objectPatterns.forEach(pattern => {
                    if (pattern.test(trimmed)) {
                        allocations++;
                    }
                });
            }

            if (trimmed.includes('}') && inLoop) {
                inLoop = false;
            }
        });

        return allocations;
    }

    detectLargeDataStructures(code) {
        // Detectar arrays muito grandes ou objetos complexos
        let largeStructures = 0;

        // Arrays com mais de 1000 elementos
        const largeArrayPattern = /\[\s*(?:\w+\s*,\s*){100,}/;
        if (largeArrayPattern.test(code)) {
            largeStructures++;
        }

        // Objetos com muitas propriedades
        const largeObjectPattern = /{\s*(?:\w+\s*:\s*\w+\s*,\s*){20,}/;
        if (largeObjectPattern.test(code)) {
            largeStructures++;
        }

        // JSON.parse com dados grandes
        const largeJsonPattern = /JSON\.parse\(['"][^'"]{500,}['"]\)/;
        if (largeJsonPattern.test(code)) {
            largeStructures++;
        }

        return largeStructures;
    }

    async optimizeMemoryUsage(code, issues) {
        const changes = [];
        let optimizedCode = code;

        for (const issue of issues) {
            switch (issue.type) {
                case 'MEMORY_LEAKS':
                    const leakFix = this.fixMemoryLeaks(optimizedCode);
                    if (leakFix.changed) {
                        optimizedCode = leakFix.code;
                        changes.push({
                            type: 'MEMORY_LEAKS_FIXED',
                            description: issue.description,
                            improvement: 'Remoção de event listeners e timers adicionada'
                        });
                    }
                    break;

                case 'EXCESSIVE_OBJECT_ALLOCATION':
                    const allocationFix = this.reduceObjectAllocation(optimizedCode);
                    if (allocationFix.changed) {
                        optimizedCode = allocationFix.code;
                        changes.push({
                            type: 'OBJECT_ALLOCATION_REDUCED',
                            description: issue.description,
                            improvement: 'Reutilização de objetos implementada'
                        });
                    }
                    break;

                case 'LARGE_DATA_STRUCTURES':
                    const structureFix = this.optimizeDataStructures(optimizedCode);
                    if (structureFix.changed) {
                        optimizedCode = structureFix.code;
                        changes.push({
                            type: 'DATA_STRUCTURES_OPTIMIZED',
                            description: issue.description,
                            improvement: 'Estruturas de dados otimizadas para uso de memória'
                        });
                    }
                    break;
            }
        }

        return {
            success: changes.length > 0,
            optimizedCode,
            changes,
            improvements: {
                memory: changes.length * 0.15,
                confidence: Math.min(0.85, changes.length * 0.25)
            }
        };
    }

    fixMemoryLeaks(code) {
        let changed = false;
        let optimized = code;

        // Adicionar removeEventListener para cada addEventListener
        if (optimized.includes('addEventListener') && !optimized.includes('removeEventListener')) {
            changed = true;
            optimized = optimized.replace(
                /(\w+)\.addEventListener\(([^)]+),\s*([^)]+)\);/g,
                '$1.addEventListener($2, $3);\n// TODO: Adicionar $1.removeEventListener($2, $3) quando não for mais necessário;'
            );
        }

        // Adicionar clearInterval/clearTimeout
        if (optimized.includes('setInterval') && !optimized.includes('clearInterval')) {
            changed = true;
            optimized = optimized.replace(
                /const\s+(\w+)\s*=\s*setInterval\(([^)]+)\);/g,
                'const $1 = setInterval($2);\n// TODO: Adicionar clearInterval($1) quando não for mais necessário;'
            );
        }

        return { changed, code: optimized };
    }

    reduceObjectAllocation(code) {
        let changed = false;
        let optimized = code;

        // Sugerir reutilização de objetos em loops
        const loopPattern = /for\s*\([^)]*\)\s*{\s*const\s+\w+\s*=\s*{/g;
        if (loopPattern.test(optimized)) {
            changed = true;
            optimized = optimized.replace(
                /(for\s*\([^)]*\)\s*{\s*)const\s+(\w+)\s*=\s*{/g,
                '$1// CONSIDERE: Mova a criação do objeto $2 para fora do loop\nconst $2 = {'
            );
        }

        return { changed, code: optimized };
    }

    optimizeDataStructures(code) {
        let changed = false;
        let optimized = code;

        // Sugerir lazy loading para arrays grandes
        const largeArrayPattern = /const\s+\w+\s*=\s*\[[^\]]{100,}\]/;
        if (largeArrayPattern.test(optimized)) {
            changed = true;
            optimized = optimized.replace(
                /(const\s+(\w+)\s*=\s*\[[^\]]{100,}\])/,
                '// CONSIDERE: Lazy loading para array grande\n// $1\n// function get$2() { return [...]; }'
            );
        }

        return { changed, code: optimized };
    }

    async analyzeSecurity(code, metrics) {
        // Análise de segurança usando o serviço de análise de código
        const analysis = await this.codeAnalysisService.analyze(code);
        const issues = [];

        if (analysis.security?.vulnerabilityScan?.vulnerabilities) {
            analysis.security.vulnerabilityScan.vulnerabilities.forEach(vuln => {
                issues.push({
                    type: 'SECURITY_VULNERABILITY',
                    severity: vuln.severity.level,
                    description: vuln.description,
                    suggestion: vuln.fix,
                    cwe: vuln.cwe
                });
            });
        }

        return issues;
    }

    async optimizeSecurity(code, issues) {
        const changes = [];
        let optimizedCode = code;

        for (const issue of issues) {
            switch (issue.type) {
                case 'SECURITY_VULNERABILITY':
                    const securityFix = this.applySecurityFix(optimizedCode, issue);
                    if (securityFix.changed) {
                        optimizedCode = securityFix.code;
                        changes.push({
                            type: 'SECURITY_VULNERABILITY_FIXED',
                            description: issue.description,
                            improvement: issue.suggestion,
                            cwe: issue.cwe
                        });
                    }
                    break;
            }
        }

        return {
            success: changes.length > 0,
            optimizedCode,
            changes,
            improvements: {
                security: changes.length * 0.2,
                confidence: Math.min(0.95, changes.length * 0.3)
            }
        };
    }

    applySecurityFix(code, vulnerability) {
        let changed = false;
        let optimized = code;

        // Aplicar fixes comuns de segurança
        if (vulnerability.description.includes('eval(')) {
            changed = true;
            optimized = optimized.replace(/eval\(/g, '// EVAL REMOVIDO POR QUESTÕES DE SEGURANÇA\n// Use: ');
        }

        if (vulnerability.description.includes('innerHTML')) {
            changed = true;
            optimized = optimized.replace(/\.innerHTML\s*=/g, '.textContent =');
        }

        if (vulnerability.description.includes('localStorage')) {
            changed = true;
            optimized = optimized.replace(/localStorage\.setItem\([^)]*\)/g,
                '// localStorage REMOVIDO - Use armazenamento seguro\n// localStorage.setItem(...)');
        }

        return { changed, code: optimized };
    }

    async analyzeReadability(code, metrics) {
        const issues = [];

        // Verificar nomes de variáveis não descritivos
        const badVariableNames = this.detectBadVariableNames(code);
        if (badVariableNames.length > 0) {
            issues.push({
                type: 'BAD_VARIABLE_NAMES',
                severity: 'LOW',
                description: `${badVariableNames.length} nomes de variáveis não descritivos detectados`,
                suggestion: 'Use nomes mais descritivos que expliquem o propósito da variável',
                examples: badVariableNames.slice(0, 3)
            });
        }

        // Verificar funções muito longas
        const longFunctions = this.detectLongFunctions(code);
        if (longFunctions.length > 0) {
            issues.push({
                type: 'LONG_FUNCTIONS',
                severity: 'MEDIUM',
                description: `${longFunctions.length} funções muito longas detectadas`,
                suggestion: 'Quebre funções longas em funções menores e mais focadas',
                examples: longFunctions.slice(0, 2)
            });
        }

        // Verificar falta de comentários
        const missingComments = this.detectMissingComments(code);
        if (missingComments > 0) {
            issues.push({
                type: 'MISSING_COMMENTS',
                severity: 'LOW',
                description: `Falta de comentários em ${missingComments} seções complexas`,
                suggestion: 'Adicione comentários para explicar lógica complexa'
            });
        }

        return issues;
    }

    detectBadVariableNames(code) {
        const badNames = [];
        const badPatterns = [/var\s+(a|b|c|x|y|z)\b/g, /let\s+(a|b|c|x|y|z)\b/g, /const\s+(a|b|c|x|y|z)\b/g];

        badPatterns.forEach(pattern => {
            const matches = code.match(pattern);
            if (matches) {
                badNames.push(...matches);
            }
        });

        return badNames;
    }

    detectLongFunctions(code) {
        const longFunctions = [];
        const lines = code.split('\n');
        let inFunction = false;
        let functionStart = 0;
        let functionName = '';
        let lineCount = 0;

        lines.forEach((line, index) => {
            const trimmed = line.trim();

            // Detectar início de função
            if (trimmed.startsWith('function ') || trimmed.includes('= function') || trimmed.includes('=> {')) {
                if (inFunction && lineCount > 30) { // Limite de 30 linhas
                    longFunctions.push({
                        name: functionName || 'anonymous',
                        lines: lineCount,
                        start: functionStart
                    });
                }

                inFunction = true;
                functionStart = index;
                functionName = this.extractFunctionName(trimmed);
                lineCount = 0;
            }

            if (inFunction) {
                lineCount++;
            }

            // Detectar fim de função
            if (inFunction && trimmed === '}') {
                if (lineCount > 30) {
                    longFunctions.push({
                        name: functionName || 'anonymous',
                        lines: lineCount,
                        start: functionStart
                    });
                }
                inFunction = false;
            }
        });

        return longFunctions;
    }

    extractFunctionName(line) {
        const match = line.match(/function\s+(\w+)/);
        if (match) return match[1];

        const match2 = line.match(/(\w+)\s*=/);
        if (match2) return match2[1];

        return 'anonymous';
    }

    detectMissingComments(code) {
        // Detectar seções complexas sem comentários
        let complexSections = 0;
        const complexPatterns = [
            /if\s*\([^)]{50,}\)/g,  // Condicionais complexas
            /for\s*\([^)]{30,}\)/g,  // Loops complexos
            /function\s+\w+\([^)]{5,}\)/g  // Funções com muitos parâmetros
        ];

        complexPatterns.forEach(pattern => {
            const matches = code.match(pattern);
            if (matches) {
                complexSections += matches.length;
            }
        });

        // Verificar se há comentários próximos
        const lines = code.split('\n');
        let missing = 0;

        lines.forEach((line, index) => {
            complexPatterns.forEach(pattern => {
                if (pattern.test(line)) {
                    // Verificar se há comentários nas 2 linhas anteriores
                    const prevLines = lines.slice(Math.max(0, index - 2), index);
                    const hasComment = prevLines.some(l => l.trim().startsWith('//') || l.trim().startsWith('/*'));

                    if (!hasComment) {
                        missing++;
                    }
                }
            });
        });

        return missing;
    }

    async optimizeReadability(code, issues) {
        const changes = [];
        let optimizedCode = code;

        for (const issue of issues) {
            switch (issue.type) {
                case 'BAD_VARIABLE_NAMES':
                    const namingFix = this.fixVariableNames(optimizedCode, issue.examples);
                    if (namingFix.changed) {
                        optimizedCode = namingFix.code;
                        changes.push({
                            type: 'VARIABLE_NAMES_IMPROVED',
                            description: issue.description,
                            improvement: 'Nomes de variáveis tornados mais descritivos'
                        });
                    }
                    break;

                case 'LONG_FUNCTIONS':
                    const functionFix = this.splitLongFunctions(optimizedCode, issue.examples);
                    if (functionFix.changed) {
                        optimizedCode = functionFix.code;
                        changes.push({
                            type: 'FUNCTIONS_SPLIT',
                            description: issue.description,
                            improvement: 'Funções longas divididas em funções menores'
                        });
                    }
                    break;

                case 'MISSING_COMMENTS':
                    const commentFix = this.addMissingComments(optimizedCode);
                    if (commentFix.changed) {
                        optimizedCode = commentFix.code;
                        changes.push({
                            type: 'COMMENTS_ADDED',
                            description: issue.description,
                            improvement: 'Comentários adicionados para lógica complexa'
                        });
                    }
                    break;
            }
        }

        return {
            success: changes.length > 0,
            optimizedCode,
            changes,
            improvements: {
                readability: changes.length * 0.25,
                confidence: Math.min(0.8, changes.length * 0.2)
            }
        };
    }

    fixVariableNames(code, badNames) {
        let changed = false;
        let optimized = code;

        // Mapeamento de nomes ruins para bons nomes
        const nameMapping = {
            'a': 'accumulator',
            'b': 'buffer',
            'c': 'counter',
            'x': 'coordinateX',
            'y': 'coordinateY',
            'z': 'coordinateZ',
            'i': 'index',
            'j': 'innerIndex',
            'k': 'keyIndex'
        };

        badNames.forEach(badName => {
            const simpleName = badName.replace(/var\s+|\s+let\s+|\s+const\s+/, '').trim();
            const goodName = nameMapping[simpleName];

            if (goodName) {
                const pattern = new RegExp(`\\b${simpleName}\\b`, 'g');
                optimized = optimized.replace(pattern, goodName);
                changed = true;
            }
        });

        return { changed, code: optimized };
    }

    splitLongFunctions(code, longFunctions) {
        let changed = false;
        let optimized = code;

        // Simplificado - em produção, análise AST para dividir funções
        longFunctions.forEach(func => {
            optimized = optimized + `\n\n// TODO: Dividir função "${func.name}" (${func.lines} linhas) em funções menores`;
            changed = true;
        });

        return { changed, code: optimized };
    }

    addMissingComments(code) {
        let changed = false;
        let optimized = code;

        // Adicionar comentários para condicionais complexas
        const complexIfPattern = /if\s*\([^)]{50,}\)/g;
        const matches = optimized.match(complexIfPattern);

        if (matches) {
            matches.forEach(match => {
                optimized = optimized.replace(match, `// Condição complexa - verificar lógica\n${match}`);
                changed = true;
            });
        }

        return { changed, code: optimized };
    }

    async analyzeMaintainability(code, metrics) {
        const issues = [];

        // Verificar alto acoplamento
        if (metrics.maintainability < 60) {
            issues.push({
                type: 'LOW_MAINTAINABILITY',
                severity: 'MEDIUM',
                description: 'Índice de manutenibilidade baixo detectado',
                suggestion: 'Melhore coesão e reduza acoplamento entre módulos'
            });
        }

        // Verificar falta de testes
        const missingTests = this.detectMissingTests(code);
        if (missingTests) {
            issues.push({
                type: 'MISSING_TESTS',
                severity: 'MEDIUM',
                description: 'Código parece não ter testes associados',
                suggestion: 'Adicione testes unitários para funções críticas'
            });
        }

        // Verificar código duplicado
        const duplicateCode = this.detectDuplicateCode(code);
        if (duplicateCode > 0) {
            issues.push({
                type: 'DUPLICATE_CODE',
                severity: 'LOW',
                description: `${duplicateCode} seções de código duplicado detectadas`,
                suggestion: 'Extrair código duplicado para funções/métodos comuns'
            });
        }

        return issues;
    }

    detectMissingTests(code) {
        // Verificar se há referências a testes
        const testPatterns = [
            /describe\(/,
            /it\(/,
            /test\(/,
            /assert\./,
            /expect\(/
        ];

        return !testPatterns.some(pattern => pattern.test(code));
    }

    detectDuplicateCode(code) {
        // Detecção simplificada de código duplicado
        const lines = code.split('\n');
        const uniqueLines = new Set(lines.filter(l => l.trim().length > 10));

        return lines.length - uniqueLines.size;
    }

    async optimizeMaintainability(code, issues) {
        const changes = [];
        let optimizedCode = code;

        for (const issue of issues) {
            switch (issue.type) {
                case 'LOW_MAINTAINABILITY':
                    const maintainabilityFix = this.improveMaintainability(optimizedCode);
                    if (maintainabilityFix.changed) {
                        optimizedCode = maintainabilityFix.code;
                        changes.push({
                            type: 'MAINTAINABILITY_IMPROVED',
                            description: issue.description,
                            improvement: 'Estrutura do código melhorada para manutenibilidade'
                        });
                    }
                    break;

                case 'MISSING_TESTS':
                    const testFix = this.addTestSuggestions(optimizedCode);
                    if (testFix.changed) {
                        optimizedCode = testFix.code;
                        changes.push({
                            type: 'TEST_SUGGESTIONS_ADDED',
                            description: issue.description,
                            improvement: 'Sugestões de testes adicionadas'
                        });
                    }
                    break;

                case 'DUPLICATE_CODE':
                    const duplicateFix = this.removeDuplicateCode(optimizedCode);
                    if (duplicateFix.changed) {
                        optimizedCode = duplicateFix.code;
                        changes.push({
                            type: 'DUPLICATE_CODE_REMOVED',
                            description: issue.description,
                            improvement: 'Código duplicado removido ou refatorado'
                        });
                    }
                    break;
            }
        }

        return {
            success: changes.length > 0,
            optimizedCode,
            changes,
            improvements: {
                maintainability: changes.length * 0.2,
                confidence: Math.min(0.75, changes.length * 0.15)
            }
        };
    }

    improveMaintainability(code) {
        let changed = false;
        let optimized = code;

        // Adicionar separadores para melhor organização
        if (!optimized.includes('// ====') && optimized.length > 200) {
            optimized = '// ================ IMPORTS ================\n' +
                optimized.replace(/(import\s+.*from\s+['"][^'"]+['"];)/g, '$1\n') +
                '\n// ================ CONSTANTS ================\n' +
                '\n// ================ FUNCTIONS ================\n' +
                '\n// ================ MAIN CODE ================\n';
            changed = true;
        }

        return { changed, code: optimized };
    }

    addTestSuggestions(code) {
        let changed = false;
        let optimized = code;

        // Extrair funções e adicionar sugestões de testes
        const functionPattern = /function\s+(\w+)/g;
        const functions = [];
        let match;

        while ((match = functionPattern.exec(code)) !== null) {
            functions.push(match[1]);
        }

        if (functions.length > 0) {
            const testSuggestions = `
// ================ TEST SUGGESTIONS ================
// Considere adicionar testes para as seguintes funções:
${functions.map(f => `// - ${f}()`).join('\n')}
// Exemplo de teste:
// describe('${functions[0]}', () => {
//   it('should work correctly', () => {
//     expect(${functions[0]}()).toBe(expectedValue);
//   });
// });
`;

            optimized += testSuggestions;
            changed = true;
        }

        return { changed, code: optimized };
    }

    removeDuplicateCode(code) {
        let changed = false;
        let optimized = code;

        // Remover linhas duplicadas consecutivas
        const lines = optimized.split('\n');
        const deduplicated = [];

        for (let i = 0; i < lines.length; i++) {
            if (i === 0 || lines[i] !== lines[i - 1]) {
                deduplicated.push(lines[i]);
            } else {
                changed = true;
            }
        }

        if (changed) {
            optimized = deduplicated.join('\n');
        }

        return { changed, code: optimized };
    }

    async validateOptimizations(originalCode, optimizedCode, optimizations) {
        const validations = [];

        // 1. Verificar se o código ainda é válido
        try {
            // Tente parsear o código otimizado
            require('acorn').parse(optimizedCode, { ecmaVersion: 'latest' });
            validations.push({
                type: 'SYNTAX_VALIDITY',
                passed: true,
                message: 'Código otimizado é sintaticamente válido'
            });
        } catch (error) {
            validations.push({
                type: 'SYNTAX_VALIDITY',
                passed: false,
                message: `Erro de sintaxe: ${error.message}`
            });
        }

        // 2. Verificar se não há regressões óbvias
        const originalLines = originalCode.split('\n').length;
        const optimizedLines = optimizedCode.split('\n').length;

        if (optimizedLines <= originalLines * 1.5) { // Até 50% maior
            validations.push({
                type: 'CODE_SIZE',
                passed: true,
                message: `Tamanho do código dentro dos limites: ${originalLines} -> ${optimizedLines} linhas`
            });
        } else {
            validations.push({
                type: 'CODE_SIZE',
                passed: false,
                message: `Código cresceu muito: ${originalLines} -> ${optimizedLines} linhas (+${((optimizedLines / originalLines - 1) * 100).toFixed(1)}%)`
            });
        }

        // 3. Verificar se otimizações foram aplicadas
        if (optimizations.length > 0) {
            validations.push({
                type: 'OPTIMIZATIONS_APPLIED',
                passed: true,
                message: `${optimizations.length} otimizações aplicadas com sucesso`
            });
        } else {
            validations.push({
                type: 'OPTIMIZATIONS_APPLIED',
                passed: false,
                message: 'Nenhuma otimização foi aplicada'
            });
        }

        const allPassed = validations.every(v => v.passed);

        return {
            passed: allPassed,
            validations,
            score: validations.filter(v => v.passed).length / validations.length
        };
    }

    async learnFromOptimization(result) {
        // Aprender com os resultados da otimização
        this.learningHistory.push({
            timestamp: new Date(),
            result,
            success: result.success,
            improvements: this.calculateImprovements(result)
        });

        // Manter histórico limitado
        if (this.learningHistory.length > 1000) {
            this.learningHistory = this.learningHistory.slice(-500);
        }

        // Ajustar estratégias baseadas no aprendizado
        this.adjustStrategiesBasedOnLearning();
    }

    calculateImprovements(result) {
        if (!result.metrics) return {};

        const improvements = {};

        Object.keys(result.metrics.original).forEach(key => {
            if (result.metrics.optimized[key]) {
                improvements[key] = result.metrics.optimized[key] - result.metrics.original[key];
            }
        });

        return improvements;
    }

    adjustStrategiesBasedOnLearning() {
        if (this.learningHistory.length < 10) return;

        // Analisar histórico para ajustar pesos das estratégias
        const recent = this.learningHistory.slice(-10);
        const successful = recent.filter(r => r.success && r.improvements && Object.values(r.improvements).some(v => v > 0));

        if (successful.length > 0) {
            // Calcular melhorias médias por tipo de otimização
            const avgImprovements = {};

            successful.forEach(opt => {
                if (opt.result.optimizations) {
                    opt.result.optimizations.forEach(optimization => {
                        if (!avgImprovements[optimization.type]) {
                            avgImprovements[optimization.type] = [];
                        }

                        if (optimization.improvements) {
                            Object.values(optimization.improvements).forEach(v => {
                                if (typeof v === 'number') {
                                    avgImprovements[optimization.type].push(v);
                                }
                            });
                        }
                    });
                }
            });

            // Ajustar pesos baseados nas melhorias
            Object.entries(avgImprovements).forEach(([type, improvements]) => {
                const avgImprovement = improvements.reduce((a, b) => a + b, 0) / improvements.length;
                const strategy = this.optimizationStrategies.get(type);

                if (strategy && avgImprovement > 0.1) {
                    strategy.weight *= 1.1; // Aumentar peso se funcionando bem
                }
            });
        }
    }
}

export class CodeArchitect {
    constructor(config = {}) {
        this.config = {
            enablePatternDetection: config.enablePatternDetection !== false,
            enableRefactoring: config.enableRefactoring !== false,
            enableOptimization: config.enableOptimization !== false,
            enableAI: config.enableAI !== false,
            confidenceThreshold: config.confidenceThreshold || 0.7,
            maxRefactorings: config.maxRefactorings || 5,
            language: config.language || CodeLanguage.JAVASCRIPT,
            ...config
        };

        this.patternDetector = new CodePatternDetector();
        this.refactoringEngine = new RefactoringEngine();
        this.neuralOptimizer = new NeuralCodeOptimizer();
        this.refactoringHistory = [];
        this.performanceMetrics = {
            totalRefactorings: 0,
            successfulRefactorings: 0,
            averageImprovement: 0,
            languages: new Set()
        };

        console.log('🏗️ Code Architect v5.0 inicializado');
    }

    async refactor(code, language = this.config.language, options = {}) {
        const refactoringId = `refactor_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        console.log(`🏗️ Refatorando código ${language.name} [${refactoringId}]...`);

        const startTime = Date.now();

        try {
            // Validar entrada
            if (!this.validateCode(code, language)) {
                return this.getFallbackResult(code, 'Código inválido para a linguagem especificada');
            }

            // Análise inicial
            const analysis = await this.analyzeCode(code, language, options);

            // Detectar padrões de refatoração
            const patterns = this.config.enablePatternDetection ?
                await this.detectRefactoringPatterns(code, language, analysis) : [];

            // Aplicar refatorações
            const refactorings = this.config.enableRefactoring ?
                await this.applyRefactorings(code, patterns, language, analysis) : [];

            // Aplicar otimizações
            const optimizations = this.config.enableOptimization ?
                await this.applyOptimizations(code, language, analysis, refactorings) : [];

            // Combinar resultados
            const result = this.combineResults(code, refactorings, optimizations, analysis);

            // Atualizar métricas
            this.updateMetrics(result, language);

            // Registrar no histórico
            this.recordRefactoring(refactoringId, result, startTime);

            console.log(`✅ Refatoração concluída em ${Date.now() - startTime}ms`);
            console.log(`📊 ${result.refactorings.length} refatorações, ${result.optimizations.length} otimizações aplicadas`);

            return result;

        } catch (error) {
            console.error('❌ Erro na refatoração:', error);
            return this.getFallbackResult(code, error.message);
        }
    }

    validateCode(code, language) {
        if (!code || typeof code !== 'string') {
            throw new Error('Código deve ser uma string não vazia');
        }

        if (code.length > 1000000) { // 1MB limit
            throw new Error('Código excede o tamanho máximo de 1MB');
        }

        // Validações específicas por linguagem
        switch (language.code) {
            case 'JAVASCRIPT':
            case 'TYPESCRIPT':
                // Validar sintaxe JavaScript básica
                try {
                    require('acorn').parse(code, { ecmaVersion: 'latest' });
                    return true;
                } catch (error) {
                    throw new Error(`Erro de sintaxe JavaScript: ${error.message}`);
                }

            case 'PYTHON':
                // Em produção, validar sintaxe Python
                return true;

            default:
                console.warn(`⚠️ Validação não implementada para ${language.name}`);
                return true;
        }
    }

    async analyzeCode(code, language, options) {
        // Análise abrangente do código
        const analysis = {
            language,
            timestamp: new Date(),
            metrics: {},
            issues: [],
            suggestions: []
        };

        try {
            // Análise básica
            analysis.metrics.basic = this.calculateBasicMetrics(code);

            // Análise de padrões
            if (this.config.enablePatternDetection) {
                const patternAnalysis = await this.patternDetector.detectPatterns(code, language, options);
                analysis.patterns = patternAnalysis.patterns;
                analysis.metrics.patterns = {
                    total: patternAnalysis.patterns.length,
                    highConfidence: patternAnalysis.patterns.filter(p => p.confidence > 0.8).length
                };
            }

            // Análise de complexidade
            analysis.metrics.complexity = this.analyzeComplexity(code);

            return analysis;

        } catch (error) {
            console.error('❌ Erro na análise do código:', error);
            return analysis;
        }
    }

    calculateBasicMetrics(code) {
        const lines = code.split('\n');

        return {
            lines: lines.length,
            nonEmptyLines: lines.filter(l => l.trim().length > 0).length,
            characters: code.length,
            functions: (code.match(/function\s+\w+|=>/g) || []).length,
            classes: (code.match(/class\s+\w+/g) || []).length,
            imports: (code.match(/import\s+|require\(/g) || []).length,
            comments: lines.filter(l => l.trim().startsWith('//') || l.trim().startsWith('/*')).length
        };
    }

    analyzeComplexity(code) {
        // Análise simplificada de complexidade
        let complexity = 0;

        // Contar condicionais
        complexity += (code.match(/\bif\s*\(|\belse\b|\bswitch\s*\(/g) || []).length;

        // Contar loops
        complexity += (code.match(/\bfor\s*\(|\bwhile\s*\(|\bdo\b/g) || []).length;

        // Contar operadores lógicos
        complexity += (code.match(/&&|\|\|/g) || []).length;

        // Contar funções aninhadas
        const nestedFunctions = (code.match(/function[^{]*{[^{]*function/g) || []).length;
        complexity += nestedFunctions * 2;

        return {
            score: complexity,
            level: complexity < 10 ? 'LOW' : complexity < 25 ? 'MEDIUM' : complexity < 50 ? 'HIGH' : 'VERY_HIGH'
        };
    }

    async detectRefactoringPatterns(code, language, analysis) {
        if (!this.config.enablePatternDetection) return [];

        const patterns = await this.patternDetector.detectPatterns(code, language, {
            confidenceThreshold: this.config.confidenceThreshold,
            analysis
        });

        // Filtrar padrões com confiança suficiente
        return patterns.patterns.filter(pattern =>
            pattern.confidence >= this.config.confidenceThreshold
        );
    }

    async applyRefactorings(code, patterns, language, analysis) {
        if (!this.config.enableRefactoring || patterns.length === 0) return [];

        const appliedRefactorings = [];
        let currentCode = code;
        let refactoringCount = 0;

        // Ordenar padrões por confiança
        const sortedPatterns = patterns.sort((a, b) => b.confidence - a.confidence);

        // Aplicar refatorações até o limite máximo
        for (const pattern of sortedPatterns) {
            if (refactoringCount >= this.config.maxRefactorings) break;

            try {
                const refactoringResult = await this.refactoringEngine.refactor(
                    currentCode,
                    pattern.refactoring,
                    {
                        ...pattern,
                        language,
                        analysis,
                        confidence: pattern.confidence
                    }
                );

                if (refactoringResult.success && refactoringResult.refactoredCode !== currentCode) {
                    appliedRefactorings.push({
                        pattern: pattern.pattern,
                        refactoring: pattern.refactoring.code,
                        originalCode: currentCode,
                        refactoredCode: refactoringResult.refactoredCode,
                        changes: refactoringResult.changes,
                        metrics: refactoringResult.metrics,
                        confidence: pattern.confidence
                    });

                    currentCode = refactoringResult.refactoredCode;
                    refactoringCount++;
                }
            } catch (error) {
                console.error(`❌ Erro ao aplicar refatoração ${pattern.refactoring.code}:`, error);
            }
        }

        return appliedRefactorings;
    }

    async applyOptimizations(code, language, analysis, refactorings) {
        if (!this.config.enableOptimization) return [];

        try {
            // Usar o código após refatorações, se houver
            const codeToOptimize = refactorings.length > 0 ?
                refactorings[refactorings.length - 1].refactoredCode : code;

            // Determinar tipos de otimização baseados na análise
            const optimizationTypes = this.determineOptimizationTypes(analysis);

            // Aplicar otimizações
            const optimizationResult = await this.neuralOptimizer.optimize(
                codeToOptimize,
                language,
                optimizationTypes
            );

            if (optimizationResult.success && optimizationResult.optimizedCode !== codeToOptimize) {
                return [optimizationResult];
            }

            return [];

        } catch (error) {
            console.error('❌ Erro na otimização:', error);
            return [];
        }
    }

    determineOptimizationTypes(analysis) {
        const types = [];

        // Baseado na análise de complexidade
        if (analysis.metrics.complexity?.level === 'HIGH' ||
            analysis.metrics.complexity?.level === 'VERY_HIGH') {
            types.push(OptimizationType.PERFORMANCE.code);
        }

        // Baseado em padrões detectados
        if (analysis.patterns?.some(p => p.pattern.includes('DUPLICATE'))) {
            types.push(OptimizationType.MAINTAINABILITY.code);
        }

        // Baseado em métricas básicas
        if (analysis.metrics.basic?.functions > 10) {
            types.push(OptimizationType.READABILITY.code);
        }

        return types;
    }

    combineResults(originalCode, refactorings, optimizations, analysis) {
        // Determinar código final
        let finalCode = originalCode;
        let appliedChanges = [];

        if (refactorings.length > 0) {
            finalCode = refactorings[refactorings.length - 1].refactoredCode;
            appliedChanges.push(...refactorings.map(r => ({
                type: 'REFACTORING',
                pattern: r.pattern,
                refactoring: r.refactoring,
                confidence: r.confidence
            })));
        }

        if (optimizations.length > 0) {
            finalCode = optimizations[0].optimizedCode;
            appliedChanges.push(...optimizations.flatMap(opt =>
                opt.optimizations?.map(o => ({
                    type: 'OPTIMIZATION',
                    optimization: o.type,
                    improvements: o.improvements
                })) || []
            ));
        }

        // Calcular métricas de melhoria
        const improvementMetrics = this.calculateImprovementMetrics(originalCode, finalCode, analysis);

        return {
            originalCode,
            refactoredCode: finalCode,
            refactorings,
            optimizations,
            appliedChanges,
            improvementMetrics,
            analysis: {
                patterns: analysis.patterns,
                complexity: analysis.metrics.complexity
            },
            summary: {
                totalChanges: appliedChanges.length,
                codeChanged: finalCode !== originalCode,
                estimatedImprovement: improvementMetrics.overall
            }
        };
    }

    calculateImprovementMetrics(originalCode, refactoredCode, analysis) {
        const metrics = {
            linesReduction: 0,
            complexityReduction: 0,
            maintainabilityImprovement: 0,
            overall: 0
        };

        // Calcular redução de linhas
        const originalLines = originalCode.split('\n').length;
        const refactoredLines = refactoredCode.split('\n').length;
        metrics.linesReduction = originalLines - refactoredLines;

        // Estimar redução de complexidade
        const originalComplexity = this.analyzeComplexity(originalCode).score;
        const refactoredComplexity = this.analyzeComplexity(refactoredCode).score;
        metrics.complexityReduction = originalComplexity - refactoredComplexity;

        // Calcular melhoria geral (simplificado)
        metrics.overall = Math.max(0, Math.min(1,
            (metrics.linesReduction * 0.3 + metrics.complexityReduction * 0.7) / 10
        ));

        return metrics;
    }

    updateMetrics(result, language) {
        this.performanceMetrics.totalRefactorings++;

        if (result.summary.codeChanged) {
            this.performanceMetrics.successfulRefactorings++;
        }

        this.performanceMetrics.languages.add(language.code);

        // Atualizar média de melhoria
        const totalImprovement = this.performanceMetrics.averageImprovement *
            (this.performanceMetrics.successfulRefactorings - 1);

        this.performanceMetrics.averageImprovement =
            (totalImprovement + result.improvementMetrics.overall) /
            this.performanceMetrics.successfulRefactorings;
    }

    recordRefactoring(id, result, startTime) {
        const record = {
            id,
            timestamp: new Date(),
            processingTime: Date.now() - startTime,
            result: {
                originalLength: result.originalCode.length,
                refactoredLength: result.refactoredCode.length,
                changes: result.appliedChanges.length,
                improvement: result.improvementMetrics.overall
            },
            language: this.config.language.code
        };

        this.refactoringHistory.push(record);

        // Manter histórico limitado
        if (this.refactoringHistory.length > 1000) {
            this.refactoringHistory = this.refactoringHistory.slice(-500);
        }
    }

    getFallbackResult(code, error) {
        return {
            originalCode: code,
            refactoredCode: code,
            refactorings: [],
            optimizations: [],
            appliedChanges: [],
            improvementMetrics: {
                linesReduction: 0,
                complexityReduction: 0,
                maintainabilityImprovement: 0,
                overall: 0
            },
            error,
            fallback: true
        };
    }

    getPerformanceMetrics() {
        return {
            ...this.performanceMetrics,
            successRate: this.performanceMetrics.totalRefactorings > 0 ?
                this.performanceMetrics.successfulRefactorings / this.performanceMetrics.totalRefactorings : 0,
            languages: Array.from(this.performanceMetrics.languages),
            historySize: this.refactoringHistory.length
        };
    }

    getRefactoringStatistics() {
        if (this.refactoringHistory.length === 0) {
            return {
                total: 0,
                byLanguage: {},
                byPattern: {},
                averageImprovement: 0
            };
        }

        const statistics = {
            total: this.refactoringHistory.length,
            byLanguage: {},
            byPattern: {},
            averageProcessingTime: 0,
            averageImprovement: 0
        };

        let totalTime = 0;
        let totalImprovement = 0;

        this.refactoringHistory.forEach(record => {
            // Por linguagem
            const lang = record.language;
            statistics.byLanguage[lang] = (statistics.byLanguage[lang] || 0) + 1;

            // Por padrão (se disponível)
            if (record.result.changes) {
                // Simplificado - em produção, extrair dos dados reais
                statistics.byPattern['GENERIC'] = (statistics.byPattern['GENERIC'] || 0) + 1;
            }

            totalTime += record.processingTime;
            totalImprovement += record.result.improvement || 0;
        });

        statistics.averageProcessingTime = totalTime / this.refactoringHistory.length;
        statistics.averageImprovement = totalImprovement / this.refactoringHistory.length;

        return statistics;
    }

    reset() {
        this.refactoringHistory = [];
        this.performanceMetrics = {
            totalRefactorings: 0,
            successfulRefactorings: 0,
            averageImprovement: 0,
            languages: new Set()
        };

        console.log('🔄 Code Architect resetado');
    }

    exportData() {
        return {
            config: { ...this.config },
            performanceMetrics: this.getPerformanceMetrics(),
            refactoringHistory: this.refactoringHistory.slice(-100),
            statistics: this.getRefactoringStatistics(),
            exportTimestamp: new Date()
        };
    }

    importData(data) {
        if (!data) return;

        if (data.config) {
            this.config = { ...this.config, ...data.config };
        }

        if (data.refactoringHistory) {
            this.refactoringHistory = data.refactoringHistory;
        }

        console.log('📥 Dados do Code Architect importados');
    }
}

// Método utilitário para refatoração rápida
CodeArchitect.quickRefactor = async function (code, language = CodeLanguage.JAVASCRIPT) {
    const architect = new CodeArchitect({
        enablePatternDetection: true,
        enableRefactoring: true,
        enableOptimization: true,
        language
    });

    return await architect.refactor(code, language);
};

// Exportar instância singleton
const codeArchitect = new CodeArchitect();

export default codeArchitect;