<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 LEXTRADER-IAG - Sistema de Trading Algorítmico Avançado</title>
    
    <!-- Framework CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
    
    <!-- Charting Libraries -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
    
    <!-- DataGrid -->
    <link href="https://cdn.jsdelivr.net/npm/tabulator-tables@5.5.2/dist/css/tabulator_midnight.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/tabulator-tables@5.5.2/dist/js/tabulator.min.js"></script>
    
    <!-- Custom Styles -->
    <style>
        :root {
            --primary: #3b82f6;
            --primary-dark: #1e3a8a;
            --primary-light: #60a5fa;
            --secondary: #10b981;
            --secondary-dark: #047857;
            --secondary-light: #34d399;
            --danger: #ef4444;
            --danger-dark: #b91c1c;
            --danger-light: #f87171;
            --warning: #f59e0b;
            --warning-dark: #d97706;
            --warning-light: #fbbf24;
            --info: #6366f1;
            --info-dark: #4f46e5;
            --info-light: #818cf8;
            --dark: #111827;
            --dark-light: #1f2937;
            --dark-lighter: #374151;
            --gray: #6b7280;
            --gray-light: #9ca3af;
            --gray-lighter: #d1d5db;
            --white: #ffffff;
            --black: #000000;
        }

        body {
            background: linear-gradient(135deg, var(--dark) 0%, var(--dark-light) 100%);
            color: var(--gray-lighter);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
        }

        .gradient-bg {
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--dark) 100%);
        }

        /* Cards */
        .card-glass {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .card-header-glass {
            background: rgba(15, 23, 42, 0.9);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Sparklines */
        .sparkline {
            height: 40px;
            width: 100%;
        }

        /* Progress Bars */
        .progress-animated {
            background: var(--dark-lighter);
            border-radius: 10px;
            overflow: hidden;
            position: relative;
        }

        .progress-animated::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            background: linear-gradient(90deg, var(--primary), var(--primary-light));
            animation: progress-glow 2s ease-in-out infinite;
        }

        @keyframes progress-glow {
            0%, 100% { opacity: 0.8; }
            50% { opacity: 1; }
        }

        /* LED Indicators */
        .led {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }

        .led-success { background-color: var(--secondary); box-shadow: 0 0 10px var(--secondary); }
        .led-warning { background-color: var(--warning); box-shadow: 0 0 10px var(--warning); }
        .led-danger { background-color: var(--danger); box-shadow: 0 0 10px var(--danger); }
        .led-processing { background-color: var(--primary); animation: blink 1s infinite; }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--dark-lighter);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--gray);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--gray-light);
        }

        /* Navigation */
        .nav-pills .nav-link.active {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            border-radius: 8px;
        }

        /* Hover Effects */
        .hover-lift {
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .hover-lift:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3) !important;
        }

        /* Performance Score */
        .performance-score {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
            background: conic-gradient(var(--primary) 0% 85%, var(--dark-lighter) 85% 100%);
        }

        /* Table Styling */
        .table-dark-custom {
            background: var(--dark-light);
            color: var(--gray-lighter);
        }

        .table-dark-custom th {
            background: var(--dark-lighter);
            border-color: var(--dark-lighter);
            font-weight: 600;
        }

        .table-dark-custom td {
            border-color: var(--dark-lighter);
        }

        /* Button Styles */
        .btn-primary-custom {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            border: none;
            color: white;
        }

        .btn-primary-custom:hover {
            background: linear-gradient(135deg, var(--primary-dark), var(--primary));
        }

        .btn-success-custom {
            background: linear-gradient(135deg, var(--secondary), var(--secondary-dark));
            border: none;
            color: white;
        }

        .btn-danger-custom {
            background: linear-gradient(135deg, var(--danger), var(--danger-dark));
            border: none;
            color: white;
        }

        /* Tabs */
        .custom-tab {
            padding: 10px 20px;
            border-radius: 8px 8px 0 0;
            background: var(--dark-light);
            color: var(--gray-light);
            border: 1px solid transparent;
            text-decoration: none;
        }

        .custom-tab.active {
            background: var(--dark-lighter);
            color: var(--primary-light);
            border-color: var(--primary);
            border-bottom-color: transparent;
        }

        /* Metrics Cards */
        .metric-card {
            background: var(--dark-lighter);
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid var(--primary);
        }

        .metric-card h3 {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .metric-card .trend {
            font-size: 12px;
            padding: 2px 8px;
            border-radius: 12px;
            display: inline-block;
        }

        .trend-up {
            background: rgba(16, 185, 129, 0.2);
            color: var(--secondary);
        }

        .trend-down {
            background: rgba(239, 68, 68, 0.2);
            color: var(--danger);
        }

        /* Alerts */
        .alert-custom {
            border-radius: 10px;
            border: none;
            background: var(--dark-lighter);
        }

        .alert-success { border-left: 4px solid var(--secondary); }
        .alert-warning { border-left: 4px solid var(--warning); }
        .alert-danger { border-left: 4px solid var(--danger); }
        .alert-info { border-left: 4px solid var(--info); }

        /* Animation Classes */
        .pulse {
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark gradient-bg shadow">
        <div class="container-fluid">
            <a class="navbar-brand fw-bold" href="#">
                <i class="bi bi-rocket-takeoff me-2"></i>
                LEXTRADER-IAG
            </a>
            
            <div class="d-flex align-items-center">
                <div class="dropdown me-3">
                    <button class="btn btn-outline-light dropdown-toggle" type="button" id="executionModeDropdown" data-bs-toggle="dropdown">
                        <i class="bi bi-play-circle me-2"></i>
                        <span id="currentMode">PAPER</span>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-dark">
                        <li><a class="dropdown-item" href="#" data-mode="PAPER">📝 Paper Trading</a></li>
                        <li><a class="dropdown-item" href="#" data-mode="LIVE">💰 Live Trading</a></li>
                        <li><a class="dropdown-item" href="#" data-mode="SIMULATION">🧪 Simulation</a></li>
                        <li><a class="dropdown-item" href="#" data-mode="BACKTEST">📊 Backtest</a></li>
                    </ul>
                </div>
                
                <button id="systemToggle" class="btn btn-success-custom me-2">
                    <i class="bi bi-play-fill me-1"></i> Iniciar Sistema
                </button>
                
                <button class="btn btn-outline-light me-2" data-bs-toggle="modal" data-bs-target="#settingsModal">
                    <i class="bi bi-gear"></i>
                </button>
                
                <button class="btn btn-outline-light" data-bs-toggle="modal" data-bs-target="#helpModal">
                    <i class="bi bi-question-circle"></i>
                </button>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container-fluid py-4">
        <div class="row">
            <!-- Sidebar -->
            <div class="col-lg-3 col-xl-2">
                <div class="card card-glass mb-4">
                    <div class="card-header card-header-glass">
                        <h6 class="mb-0"><i class="bi bi-speedometer2 me-2"></i>Resumo Rápido</h6>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <small class="text-muted">💰 Capital Total</small>
                            <h5 class="fw-bold" id="totalCapital">$ 284,567.89</h5>
                            <span class="trend trend-up">+2.34%</span>
                        </div>
                        
                        <div class="mb-3">
                            <small class="text-muted">📈 P&L Hoje</small>
                            <h5 class="fw-bold text-success" id="dailyPnl">+$ 2,345.67</h5>
                        </div>
                        
                        <div class="mb-3">
                            <small class="text-muted">🎯 Taxa de Acerto</small>
                            <h5 class="fw-bold" id="winRate">87.4%</h5>
                        </div>
                        
                        <div class="mb-3">
                            <small class="text-muted">⚡ Operações Hoje</small>
                            <h5 class="fw-bold" id="dailyTrades">342</h5>
                        </div>
                        
                        <hr class="my-3">
                        
                        <h6 class="mb-3"><i class="bi bi-graph-up me-2"></i>Ativos Monitorados</h6>
                        <div id="monitoredAssets">
                            <!-- Dynamic content -->
                        </div>
                    </div>
                </div>
                
                <div class="card card-glass">
                    <div class="card-header card-header-glass">
                        <h6 class="mb-0"><i class="bi bi-lightning-charge me-2"></i>Sinais Ativos</h6>
                    </div>
                    <div class="card-body">
                        <div id="activeSignals">
                            <!-- Dynamic content -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- Main Content Area -->
            <div class="col-lg-9 col-xl-10">
                <!-- Tab Navigation -->
                <ul class="nav nav-pills mb-4" id="mainTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="dashboard-tab" data-bs-toggle="pill" data-bs-target="#dashboard">
                            <i class="bi bi-speedometer2 me-2"></i>Dashboard
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="algorithms-tab" data-bs-toggle="pill" data-bs-target="#algorithms">
                            <i class="bi bi-cpu me-2"></i>Algoritmos
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="trading-tab" data-bs-toggle="pill" data-bs-target="#trading">
                            <i class="bi bi-graph-up me-2"></i>Trading
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="analysis-tab" data-bs-toggle="pill" data-bs-target="#analysis">
                            <i class="bi bi-bar-chart me-2"></i>Análise
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="portfolio-tab" data-bs-toggle="pill" data-bs-target="#portfolio">
                            <i class="bi bi-wallet2 me-2"></i>Portfólio
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="monitoring-tab" data-bs-toggle="pill" data-bs-target="#monitoring">
                            <i class="bi bi-eye me-2"></i>Monitoramento
                        </button>
                    </li>
                </ul>

                <!-- Tab Content -->
                <div class="tab-content" id="mainTabContent">
                    <!-- Dashboard Tab -->
                    <div class="tab-pane fade show active" id="dashboard" role="tabpanel">
                        <div class="row">
                            <!-- Main Metrics -->
                            <div class="col-xxl-9">
                                <div class="row mb-4">
                                    <div class="col-md-3 mb-3">
                                        <div class="metric-card hover-lift">
                                            <small class="text-muted">💰 Patrimônio Total</small>
                                            <h3>$ 284,567.89</h3>
                                            <span class="trend trend-up">+2.34%</span>
                                        </div>
                                    </div>
                                    <div class="col-md-3 mb-3">
                                        <div class="metric-card hover-lift">
                                            <small class="text-muted">📈 P&L Diário</small>
                                            <h3 class="text-success">+$ 2,345.67</h3>
                                            <span class="trend trend-up">+1.23%</span>
                                        </div>
                                    </div>
                                    <div class="col-md-3 mb-3">
                                        <div class="metric-card hover-lift">
                                            <small class="text-muted">🎯 Taxa de Acerto</small>
                                            <h3>87.4%</h3>
                                            <span class="trend trend-up">↑ 1.2%</span>
                                        </div>
                                    </div>
                                    <div class="col-md-3 mb-3">
                                        <div class="metric-card hover-lift">
                                            <small class="text-muted">⚡ Sharpe Ratio</small>
                                            <h3>2.85</h3>
                                            <span class="text-muted">Estável</span>
                                        </div>
                                    </div>
                                </div>

                                <!-- Performance Chart -->
                                <div class="card card-glass mb-4">
                                    <div class="card-header card-header-glass d-flex justify-content-between align-items-center">
                                        <h6 class="mb-0"><i class="bi bi-graph-up me-2"></i>Performance do Portfólio</h6>
                                        <div class="btn-group btn-group-sm">
                                            <button class="btn btn-outline-light active">1D</button>
                                            <button class="btn btn-outline-light">1W</button>
                                            <button class="btn btn-outline-light">1M</button>
                                            <button class="btn btn-outline-light">1Y</button>
                                        </div>
                                    </div>
                                    <div class="card-body">
                                        <div class="chart-container">
                                            <canvas id="performanceChart"></canvas>
                                        </div>
                                    </div>
                                </div>

                                <!-- Recent Activity -->
                                <div class="card card-glass">
                                    <div class="card-header card-header-glass">
                                        <h6 class="mb-0"><i class="bi bi-clock-history me-2"></i>Atividade Recente</h6>
                                    </div>
                                    <div class="card-body">
                                        <div class="table-responsive">
                                            <table class="table table-dark-custom table-hover">
                                                <thead>
                                                    <tr>
                                                        <th>Hora</th>
                                                        <th>Tipo</th>
                                                        <th>Descrição</th>
                                                        <th>Status</th>
                                                        <th>Valor</th>
                                                    </tr>
                                                </thead>
                                                <tbody id="recentActivity">
                                                    <!-- Dynamic content -->
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Side Metrics -->
                            <div class="col-xxl-3">
                                <!-- System Status -->
                                <div class="card card-glass mb-4">
                                    <div class="card-header card-header-glass">
                                        <h6 class="mb-0"><i class="bi bi-pc-display me-2"></i>Status do Sistema</h6>
                                    </div>
                                    <div class="card-body">
                                        <div class="mb-3">
                                            <div class="d-flex justify-content-between mb-1">
                                                <small>CPU</small>
                                                <small id="cpuUsage">42%</small>
                                            </div>
                                            <div class="progress progress-animated" style="height: 8px;">
                                                <div class="progress-bar" role="progressbar" style="width: 42%"></div>
                                            </div>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <div class="d-flex justify-content-between mb-1">
                                                <small>Memória</small>
                                                <small id="memoryUsage">68%</small>
                                            </div>
                                            <div class="progress progress-animated" style="height: 8px;">
                                                <div class="progress-bar" role="progressbar" style="width: 68%"></div>
                                            </div>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <div class="d-flex justify-content-between mb-1">
                                                <small>GPU</small>
                                                <small id="gpuUsage">15%</small>
                                            </div>
                                            <div class="progress progress-animated" style="height: 8px;">
                                                <div class="progress-bar" role="progressbar" style="width: 15%"></div>
                                            </div>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <div class="d-flex justify-content-between mb-1">
                                                <small>Rede</small>
                                                <small id="networkLatency">24ms</small>
                                            </div>
                                            <div class="progress progress-animated" style="height: 8px;">
                                                <div class="progress-bar" role="progressbar" style="width: 24%"></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Active Alerts -->
                                <div class="card card-glass mb-4">
                                    <div class="card-header card-header-glass">
                                        <h6 class="mb-0"><i class="bi bi-bell me-2"></i>Alertas Ativos</h6>
                                    </div>
                                    <div class="card-body">
                                        <div id="activeAlerts">
                                            <!-- Dynamic content -->
                                        </div>
                                    </div>
                                </div>

                                <!-- Quick Actions -->
                                <div class="card card-glass">
                                    <div class="card-header card-header-glass">
                                        <h6 class="mb-0"><i class="bi bi-lightning me-2"></i>Ações Rápidas</h6>
                                    </div>
                                    <div class="card-body">
                                        <button class="btn btn-success-custom w-100 mb-2">
                                            <i class="bi bi-graph-up me-2"></i>Trade Rápido
                                        </button>
                                        <button class="btn btn-warning w-100 mb-2">
                                            <i class="bi bi-shield-check me-2"></i>Verificar Risco
                                        </button>
                                        <button class="btn btn-info w-100">
                                            <i class="bi bi-file-earmark-text me-2"></i>Gerar Relatório
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Algorithms Tab -->
                    <div class="tab-pane fade" id="algorithms" role="tabpanel">
                        <div class="card card-glass">
                            <div class="card-header card-header-glass d-flex justify-content-between align-items-center">
                                <h6 class="mb-0"><i class="bi bi-cpu me-2"></i>Algoritmos Avançados</h6>
                                <div>
                                    <input type="text" class="form-control form-control-sm d-inline-block w-auto me-2" placeholder="Buscar algoritmo...">
                                    <select class="form-select form-select-sm d-inline-block w-auto">
                                        <option>Todos</option>
                                        <option>Ativos</option>
                                        <option>Inativos</option>
                                        <option>Otimizando</option>
                                    </select>
                                </div>
                            </div>
                            <div class="card-body">
                                <div id="algorithmCards">
                                    <!-- Dynamic algorithm cards -->
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Trading Tab -->
                    <div class="tab-pane fade" id="trading" role="tabpanel">
                        <div class="row">
                            <!-- Trading Controls -->
                            <div class="col-lg-4 mb-4">
                                <div class="card card-glass h-100">
                                    <div class="card-header card-header-glass">
                                        <h6 class="mb-0"><i class="bi bi-currency-exchange me-2"></i>Controles de Trading</h6>
                                    </div>
                                    <div class="card-body">
                                        <div class="mb-3">
                                            <label class="form-label">Símbolo</label>
                                            <input type="text" class="form-control" value="BTC/USDT">
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label class="form-label">Timeframe</label>
                                            <select class="form-select">
                                                <option>1m</option>
                                                <option selected>1h</option>
                                                <option>4h</option>
                                                <option>1d</option>
                                            </select>
                                        </div>
                                        
                                        <button class="btn btn-primary-custom w-100 mb-4">
                                            <i class="bi bi-download me-2"></i>Carregar Dados
                                        </button>
                                        
                                        <hr class="my-4">
                                        
                                        <h6 class="mb-3">Nova Ordem</h6>
                                        
                                        <div class="mb-3">
                                            <label class="form-label">Tipo</label>
                                            <select class="form-select">
                                                <option selected>MARKET</option>
                                                <option>LIMIT</option>
                                                <option>STOP</option>
                                            </select>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label class="form-label">Lado</label>
                                            <select class="form-select">
                                                <option selected>BUY</option>
                                                <option>SELL</option>
                                            </select>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label class="form-label">Quantidade</label>
                                            <input type="number" class="form-control" value="0.1" step="0.01">
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label class="form-label">Preço (para LIMIT)</label>
                                            <input type="number" class="form-control" value="0.0" step="0.01">
                                        </div>
                                        
                                        <div class="row">
                                            <div class="col-6">
                                                <button class="btn btn-success-custom w-100">
                                                    <i class="bi bi-arrow-up me-2"></i>Comprar
                                                </button>
                                            </div>
                                            <div class="col-6">
                                                <button class="btn btn-danger-custom w-100">
                                                    <i class="bi bi-arrow-down me-2"></i>Vender
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Trading Charts -->
                            <div class="col-lg-8">
                                <div class="card card-glass mb-4">
                                    <div class="card-header card-header-glass">
                                        <h6 class="mb-0"><i class="bi bi-graph-up me-2"></i>Gráfico de Preços</h6>
                                    </div>
                                    <div class="card-body">
                                        <div id="priceChart" style="height: 400px;"></div>
                                    </div>
                                </div>
                                
                                <div class="card card-glass">
                                    <div class="card-header card-header-glass">
                                        <h6 class="mb-0"><i class="bi bi-list-check me-2"></i>Ordens Abertas</h6>
                                    </div>
                                    <div class="card-body">
                                        <div id="ordersGrid"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Analysis Tab -->
                    <div class="tab-pane fade" id="analysis" role="tabpanel">
                        <div class="row">
                            <!-- Technical Analysis -->
                            <div class="col-md-6 mb-4">
                                <div class="card card-glass h-100">
                                    <div class="card-header card-header-glass">
                                        <h6 class="mb-0"><i class="bi bi-graph-up me-2"></i>Análise Técnica</h6>
                                    </div>
                                    <div class="card-body">
                                        <div class="row">
                                            <div class="col-6 mb-3">
                                                <div class="metric-card">
                                                    <small>RSI (14)</small>
                                                    <h4>62.3</h4>
                                                    <small class="text-warning">Neutral</small>
                                                </div>
                                            </div>
                                            <div class="col-6 mb-3">
                                                <div class="metric-card">
                                                    <small>MACD</small>
                                                    <h4>+15.2</h4>
                                                    <small class="text-success">Bullish</small>
                                                </div>
                                            </div>
                                            <div class="col-6 mb-3">
                                                <div class="metric-card">
                                                    <small>Bollinger</small>
                                                    <h4>Upper</h4>
                                                    <small class="text-danger">Overbought</small>
                                                </div>
                                            </div>
                                            <div class="col-6 mb-3">
                                                <div class="metric-card">
                                                    <small>Volume</small>
                                                    <h4>+215%</h4>
                                                    <small class="text-info">High</small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Risk Analysis -->
                            <div class="col-md-6 mb-4">
                                <div class="card card-glass h-100">
                                    <div class="card-header card-header-glass">
                                        <h6 class="mb-0"><i class="bi bi-shield me-2"></i>Análise de Risco</h6>
                                    </div>
                                    <div class="card-body">
                                        <div class="row">
                                            <div class="col-6 mb-3">
                                                <div class="metric-card">
                                                    <small>VaR (95%)</small>
                                                    <h4>2.1%</h4>
                                                    <small class="text-warning">Moderate</small>
                                                </div>
                                            </div>
                                            <div class="col-6 mb-3">
                                                <div class="metric-card">
                                                    <small>CVaR</small>
                                                    <h4>3.8%</h4>
                                                    <small class="text-danger">High</small>
                                                </div>
                                            </div>
                                            <div class="col-6 mb-3">
                                                <div class="metric-card">
                                                    <small>Sharpe</small>
                                                    <h4>2.85</h4>
                                                    <small class="text-success">Excellent</small>
                                                </div>
                                            </div>
                                            <div class="col-6 mb-3">
                                                <div class="metric-card">
                                                    <small>Drawdown</small>
                                                    <h4>12.3%</h4>
                                                    <small class="text-warning">Moderate</small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Portfolio Tab -->
                    <div class="tab-pane fade" id="portfolio" role="tabpanel">
                        <div class="row">
                            <div class="col-lg-8">
                                <div class="card card-glass mb-4">
                                    <div class="card-header card-header-glass">
                                        <h6 class="mb-0"><i class="bi bi-wallet2 me-2"></i>Posições do Portfólio</h6>
                                    </div>
                                    <div class="card-body">
                                        <div id="portfolioGrid"></div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="col-lg-4">
                                <div class="card card-glass mb-4">
                                    <div class="card-header card-header-glass">
                                        <h6 class="mb-0"><i class="bi bi-pie-chart me-2"></i>Resumo do Portfólio</h6>
                                    </div>
                                    <div class="card-body">
                                        <div class="mb-3">
                                            <small class="text-muted">💰 Valor Total</small>
                                            <h5 class="fw-bold">$ 284,567.89</h5>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <small class="text-muted">📈 P&L Total</small>
                                            <h5 class="fw-bold text-success">+$ 12,456.78</h5>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <small class="text-muted">🎯 P&L %</small>
                                            <h5 class="fw-bold">+4.56%</h5>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <small class="text-muted">🛡️ Risco Médio</small>
                                            <h5 class="fw-bold">5.8/10</h5>
                                        </div>
                                        
                                        <hr class="my-3">
                                        
                                        <h6 class="mb-3">Alocação por Classe</h6>
                                        <div id="allocationChart"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Monitoring Tab -->
                    <div class="tab-pane fade" id="monitoring" role="tabpanel">
                        <div class="row">
                            <!-- System Logs -->
                            <div class="col-md-6 mb-4">
                                <div class="card card-glass h-100">
                                    <div class="card-header card-header-glass d-flex justify-content-between align-items-center">
                                        <h6 class="mb-0"><i class="bi bi-journal-text me-2"></i>Logs do Sistema</h6>
                                        <div>
                                            <button class="btn btn-sm btn-outline-light me-2">
                                                <i class="bi bi-trash"></i>
                                            </button>
                                            <button class="btn btn-sm btn-outline-light">
                                                <i class="bi bi-download"></i>
                                            </button>
                                        </div>
                                    </div>
                                    <div class="card-body">
                                        <div class="system-logs" style="height: 400px; overflow-y: auto;">
                                            <div class="log-entry text-success mb-2">
                                                <small>[14:30:25] [INFO] Sistema inicializado com sucesso</small>
                                            </div>
                                            <div class="log-entry text-success mb-2">
                                                <small>[14:30:26] [INFO] Conectado à Binance API</small>
                                            </div>
                                            <div class="log-entry text-warning mb-2">
                                                <small>[14:31:10] [WARNING] Alta volatilidade detectada</small>
                                            </div>
                                            <div class="log-entry text-success mb-2">
                                                <small>[14:31:15] [SUCCESS] Ordem executada: BUY 0.5 BTC</small>
                                            </div>
                                            <div class="log-entry text-danger mb-2">
                                                <small>[14:32:45] [ERROR] Falha na conexão com Bybit API</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Real-time Metrics -->
                            <div class="col-md-6">
                                <div class="card card-glass h-100">
                                    <div class="card-header card-header-glass">
                                        <h6 class="mb-0"><i class="bi bi-speedometer me-2"></i>Métricas em Tempo Real</h6>
                                    </div>
                                    <div class="card-body">
                                        <div class="row">
                                            <div class="col-6 mb-4">
                                                <div class="metric-card">
                                                    <small>📊 CPU Usage</small>
                                                    <h4>42%</h4>
                                                    <div class="sparkline mt-2">
                                                        <canvas class="sparkline-chart"></canvas>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="col-6 mb-4">
                                                <div class="metric-card">
                                                    <small>💾 Memory</small>
                                                    <h4>68%</h4>
                                                    <div class="sparkline mt-2">
                                                        <canvas class="sparkline-chart"></canvas>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="col-6 mb-4">
                                                <div class="metric-card">
                                                    <small>⚡ Latência API</small>
                                                    <h4>87ms</h4>
                                                    <div class="sparkline mt-2">
                                                        <canvas class="sparkline-chart"></canvas>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="col-6 mb-4">
                                                <div class="metric-card">
                                                    <small>📈 Trades/min</small>
                                                    <h4>3.2</h4>
                                                    <div class="sparkline mt-2">
                                                        <canvas class="sparkline-chart"></canvas>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Status Bar -->
    <footer class="navbar navbar-dark gradient-bg fixed-bottom">
        <div class="container-fluid">
            <div class="navbar-text">
                <span class="me-4">
                    <span class="led led-success"></span>
                    <small id="systemStatus">Sistema operando normalmente</small>
                </span>
                <span class="me-4">
                    <small id="lastUpdate">Última atualização: --:--:--</small>
                </span>
            </div>
            <div class="navbar-text">
                <span class="me-4">
                    <i class="bi bi-wifi text-success"></i>
                    <small id="connectionStatus">Conectado</small>
                </span>
                <span>
                    <small id="executionModeDisplay">Modo: PAPER</small>
                </span>
            </div>
        </div>
    </footer>

    <!-- Modals -->
    <!-- Settings Modal -->
    <div class="modal fade" id="settingsModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content bg-dark">
                <div class="modal-header">
                    <h5 class="modal-title"><i class="bi bi-gear me-2"></i>Configurações do Sistema</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <ul class="nav nav-tabs mb-3" role="tablist">
                        <li class="nav-item">
                            <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#generalSettings">
                                Geral
                            </button>
                        </li>
                        <li class="nav-item">
                            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#riskSettings">
                                Risco
                            </button>
                        </li>
                        <li class="nav-item">
                            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#notificationSettings">
                                Notificações
                            </button>
                        </li>
                    </ul>
                    
                    <div class="tab-content">
                        <div class="tab-pane fade show active" id="generalSettings">
                            <div class="mb-3">
                                <label class="form-label">Tema</label>
                                <select class="form-select">
                                    <option selected>Escuro</option>
                                    <option>Claro</option>
                                    <option>Automático</option>
                                </select>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Idioma</label>
                                <select class="form-select">
                                    <option selected>Português (BR)</option>
                                    <option>English (US)</option>
                                    <option>Español</option>
                                </select>
                            </div>
                            
                            <div class="form-check mb-3">
                                <input class="form-check-input" type="checkbox" id="autoTrading">
                                <label class="form-check-label" for="autoTrading">
                                    Auto-trading
                                </label>
                            </div>
                        </div>
                        
                        <div class="tab-pane fade" id="riskSettings">
                            <div class="mb-3">
                                <label class="form-label">Tolerância a Risco</label>
                                <input type="range" class="form-range" min="0" max="100" value="50">
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Tamanho Máx. Posição (% do capital)</label>
                                <input type="number" class="form-control" value="10" step="1" min="1" max="100">
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Perda Diária Máxima (% do capital)</label>
                                <input type="number" class="form-control" value="2" step="0.5" min="0.1" max="10">
                            </div>
                        </div>
                        
                        <div class="tab-pane fade" id="notificationSettings">
                            <div class="form-check mb-3">
                                <input class="form-check-input" type="checkbox" id="enableNotifications" checked>
                                <label class="form-check-label" for="enableNotifications">
                                    Notificações Habilitadas
                                </label>
                            </div>
                            
                            <div class="form-check mb-3">
                                <input class="form-check-input" type="checkbox" id="enableSound">
                                <label class="form-check-label" for="enableSound">
                                    Som Habilitado
                                </label>
                            </div>
                            
                            <h6 class="mb-3">Tipos de Notificação</h6>
                            
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="tradeSignals" checked>
                                <label class="form-check-label" for="tradeSignals">
                                    📈 Sinais de Trade
                                </label>
                            </div>
                            
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="riskAlerts" checked>
                                <label class="form-check-label" for="riskAlerts">
                                    🚨 Alertas de Risco
                                </label>
                            </div>
                            
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="systemAlerts" checked>
                                <label class="form-check-label" for="systemAlerts">
                                    🔧 Alertas de Sistema
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="button" class="btn btn-primary-custom" data-bs-dismiss="modal">Salvar Configurações</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Help Modal -->
    <div class="modal fade" id="helpModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content bg-dark">
                <div class="modal-header">
                    <h5 class="modal-title"><i class="bi bi-question-circle me-2"></i>Ajuda - LEXTRADER-IAG</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <h6>LEXTRADER-IAG - Sistema de Trading Algorítmico Avançado</h6>
                    
                    <p class="mt-3">
                        <strong>📚 FUNCIONALIDADES PRINCIPAIS:</strong>
                    </p>
                    
                    <ul>
                        <li><strong>🤖 ALGORITMOS AVANÇADOS</strong> - Quantum Ensemble, LSTM Adaptativo, Otimizador Bayesiano</li>
                        <li><strong>💼 GESTÃO DE PORTFÓLIO</strong> - Alocação dinâmica, controle de risco em tempo real</li>
                        <li><strong>📊 ANÁLISE AVANÇADA</strong> - Técnica, fundamentalista, sentimento e risco</li>
                        <li><strong>👁️ MONITORAMENTO</strong> - Logs em tempo real, métricas de performance</li>
                        <li><strong>🧪 BACKTESTING</strong> - Teste de estratégias históricas</li>
                    </ul>
                    
                    <p class="mt-3">
                        <strong>🎯 COMO USAR:</strong>
                    </p>
                    
                    <ol>
                        <li>Configure seus algoritmos na aba "🤖 Algoritmos"</li>
                        <li>Defina seu perfil de risco em "Configurações"</li>
                        <li>Monitore as decisões em "💰 Trading"</li>
                        <li>Acompanhe o desempenho em "📊 Dashboard"</li>
                        <li>Ajuste estratégias baseado em "📊 Análise"</li>
                    </ol>
                    
                    <div class="alert alert-danger mt-3">
                        <strong>⚠️ AVISOS IMPORTANTES:</strong><br>
                        • Trading envolve riscos significativos<br>
                        • Sempre teste estratégias antes de usar capital real<br>
                        • Monitoramento constante é essencial<br>
                        • Diversificação reduz risco
                    </div>
                    
                    <p class="text-center mt-4">
                        <small>Para suporte técnico: suporte@lextrader.com.br</small>
                    </p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary-custom" data-bs-dismiss="modal">Fechar</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Quick Trade Modal -->
    <div class="modal fade" id="quickTradeModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content bg-dark">
                <div class="modal-header">
                    <h5 class="modal-title"><i class="bi bi-lightning me-2"></i>Trade Rápido</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label class="form-label">Símbolo</label>
                        <input type="text" class="form-control" value="BTC/USDT">
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Lado</label>
                        <select class="form-select">
                            <option selected>BUY</option>
                            <option>SELL</option>
                        </select>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Quantidade</label>
                        <input type="number" class="form-control" value="0.1" step="0.01">
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="button" class="btn btn-success-custom">
                        <i class="bi bi-arrow-up me-2"></i>Comprar
                    </button>
                    <button type="button" class="btn btn-danger-custom">
                        <i class="bi bi-arrow-down me-2"></i>Vender
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <script>
        // Main Application Class
        class AdvancedTradingDashboard {
            constructor() {
                this.isRunning = true;
                this.executionMode = 'PAPER';
                this.algorithms = [];
                this.portfolio = [];
                this.alerts = [];
                this.settings = {
                    riskTolerance: 'MODERATE',
                    maxPositionSize: 0.1,
                    maxDailyLoss: 0.02,
                    autoTrading: false,
                    notificationsEnabled: true,
                    soundEnabled: false,
                    theme: 'dark',
                    language: 'pt-BR'
                };
                
                this.initializeData();
                this.setupEventListeners();
                this.initializeCharts();
                this.initializeDataGrids();
                this.startBackgroundUpdates();
            }

            initializeData() {
                // Initialize sample algorithms
                this.algorithms = [
                    {
                        id: 'quantum_ensemble',
                        name: 'Quantum Ensemble Pro',
                        type: 'QUANTUM',
                        description: 'Ensemble quântico que combina múltiplas redes neurais com superposição quântica',
                        version: '3.2.1',
                        accuracy: 94.7,
                        winRate: 87.4,
                        sharpeRatio: 2.85,
                        maxDrawdown: 12.3,
                        isActive: true,
                        isOptimizing: false,
                        decisionsMade: 15247,
                        totalProfit: 284500.75,
                        specializations: ['Análise Quântica', 'Ensemble Learning'],
                        compatibleAssets: ['BTC', 'ETH', 'SPX', 'NASDAQ']
                    }
                ];

                // Initialize portfolio
                this.portfolio = [
                    {
                        symbol: 'BTC/USDT',
                        assetClass: 'CRYPTO',
                        quantity: 0.85,
                        entryPrice: 42890.45,
                        currentPrice: 43256.78,
                        positionType: 'LONG',
                        unrealizedPnl: 311.38,
                        unrealizedPnlPercent: 0.85,
                        riskScore: 5.8
                    }
                ];

                // Initialize alerts
                this.alerts = [
                    {
                        id: 'ALERT-001',
                        timestamp: new Date(),
                        type: 'TRADE_SIGNAL',
                        title: 'Novo Sinal de Compra Detectado',
                        message: 'Quantum Ensemble detectou forte sinal de compra para ETH/USDT',
                        priority: 8,
                        isAcknowledged: false
                    }
                ];
            }

            setupEventListeners() {
                // System toggle
                document.getElementById('systemToggle').addEventListener('click', () => {
                    this.toggleSystem();
                });

                // Execution mode dropdown
                document.querySelectorAll('[data-mode]').forEach(item => {
                    item.addEventListener('click', (e) => {
                        const mode = e.target.getAttribute('data-mode');
                        this.changeExecutionMode(mode);
                    });
                });

                // Tab navigation
                document.querySelectorAll('#mainTabs button').forEach(tab => {
                    tab.addEventListener('shown.bs.tab', (event) => {
                        console.log(`Tab changed to: ${event.target.textContent}`);
                    });
                });

                // Quick actions
                document.querySelectorAll('.btn-success-custom').forEach(btn => {
                    if (btn.textContent.includes('Trade Rápido')) {
                        btn.addEventListener('click', () => {
                            const modal = new bootstrap.Modal(document.getElementById('quickTradeModal'));
                            modal.show();
                        });
                    }
                });
            }

            initializeCharts() {
                // Performance Chart
                const performanceCtx = document.getElementById('performanceChart').getContext('2d');
                this.performanceChart = new Chart(performanceCtx, {
                    type: 'line',
                    data: {
                        labels: Array.from({length: 30}, (_, i) => `Dia ${i+1}`),
                        datasets: [{
                            label: 'Patrimônio',
                            data: Array.from({length: 30}, () => 10000 + Math.random() * 5000),
                            borderColor: 'rgb(59, 130, 246)',
                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false }
                        },
                        scales: {
                            x: {
                                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                                ticks: { color: 'rgba(255, 255, 255, 0.7)' }
                            },
                            y: {
                                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                                ticks: { color: 'rgba(255, 255, 255, 0.7)' }
                            }
                        }
                    }
                });

                // Price Chart (Plotly)
                const priceChartData = [{
                    x: Array.from({length: 100}, (_, i) => i),
                    close: Array.from({length: 100}, () => 42000 + Math.random() * 1000),
                    high: Array.from({length: 100}, () => 42500 + Math.random() * 500),
                    low: Array.from({length: 100}, () => 41500 + Math.random() * 500),
                    open: Array.from({length: 100}, () => 41800 + Math.random() * 800),
                    type: 'candlestick',
                    increasing: { line: { color: '#10b981' } },
                    decreasing: { line: { color: '#ef4444' } }
                }];

                const priceLayout = {
                    title: 'BTC/USDT - 1h',
                    paper_bgcolor: '#1f2937',
                    plot_bgcolor: '#1f2937',
                    font: { color: '#d1d5db' },
                    xaxis: {
                        gridcolor: 'rgba(255, 255, 255, 0.1)',
                        showgrid: true
                    },
                    yaxis: {
                        gridcolor: 'rgba(255, 255, 255, 0.1)',
                        showgrid: true
                    }
                };

                Plotly.newPlot('priceChart', priceChartData, priceLayout, {responsive: true});

                // Sparkline charts
                document.querySelectorAll('.sparkline-chart').forEach(canvas => {
                    const ctx = canvas.getContext('2d');
                    new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: Array.from({length: 20}, (_, i) => i),
                            datasets: [{
                                data: Array.from({length: 20}, () => Math.random() * 100),
                                borderColor: 'rgb(59, 130, 246)',
                                borderWidth: 1,
                                fill: false,
                                tension: 0.4
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: { legend: { display: false } },
                            scales: { x: { display: false }, y: { display: false } }
                        }
                    });
                });
            }

            initializeDataGrids() {
                // Orders Grid
                this.ordersGrid = new Tabulator('#ordersGrid', {
                    layout: 'fitColumns',
                    data: [
                        {id: 'ORD-001', symbol: 'BTC/USDT', type: 'LIMIT', side: 'BUY', quantity: 0.5, price: 42150.00, status: 'OPEN', time: '10:30:25'},
                        {id: 'ORD-002', symbol: 'ETH/USDT', type: 'MARKET', side: 'SELL', quantity: 2.0, price: 2456.78, status: 'FILLED', time: '10:25:15'}
                    ],
                    columns: [
                        {title: 'ID', field: 'id', width: 100},
                        {title: 'Símbolo', field: 'symbol'},
                        {title: 'Tipo', field: 'type'},
                        {title: 'Lado', field: 'side', formatter: (cell) => {
                            const side = cell.getValue();
                            return side === 'BUY' ? 
                                '<span class="badge bg-success">BUY</span>' : 
                                '<span class="badge bg-danger">SELL</span>';
                        }},
                        {title: 'Quantidade', field: 'quantity'},
                        {title: 'Preço', field: 'price', formatter: 'money', formatterParams: {precision: 2}},
                        {title: 'Status', field: 'status', formatter: (cell) => {
                            const status = cell.getValue();
                            const colors = {
                                'OPEN': 'warning',
                                'FILLED': 'success',
                                'PENDING': 'info',
                                'CANCELLED': 'secondary'
                            };
                            return `<span class="badge bg-${colors[status] || 'secondary'}">${status}</span>`;
                        }},
                        {title: 'Tempo', field: 'time'}
                    ]
                });

                // Portfolio Grid
                this.portfolioGrid = new Tabulator('#portfolioGrid', {
                    layout: 'fitColumns',
                    data: this.portfolio,
                    columns: [
                        {title: 'Símbolo', field: 'symbol'},
                        {title: 'Tipo', field: 'positionType', formatter: (cell) => {
                            const type = cell.getValue();
                            return type === 'LONG' ? 
                                '<span class="badge bg-success">LONG</span>' : 
                                '<span class="badge bg-danger">SHORT</span>';
                        }},
                        {title: 'Quantidade', field: 'quantity', formatter: 'number', formatterParams: {precision: 4}},
                        {title: 'Entrada', field: 'entryPrice', formatter: 'money', formatterParams: {precision: 2}},
                        {title: 'Atual', field: 'currentPrice', formatter: 'money', formatterParams: {precision: 2}},
                        {title: 'P&L', field: 'unrealizedPnl', formatter: (cell) => {
                            const value = cell.getValue();
                            const color = value >= 0 ? 'text-success' : 'text-danger';
                            return `<span class="${color}">$${value.toFixed(2)}</span>`;
                        }},
                        {title: 'P&L %', field: 'unrealizedPnlPercent', formatter: (cell) => {
                            const value = cell.getValue();
                            const color = value >= 0 ? 'text-success' : 'text-danger';
                            return `<span class="${color}">${value.toFixed(2)}%</span>`;
                        }},
                        {title: 'Risco', field: 'riskScore', formatter: (cell) => {
                            const value = cell.getValue();
                            let color = 'success';
                            if (value > 7) color = 'danger';
                            else if (value > 4) color = 'warning';
                            return `<span class="badge bg-${color}">${value.toFixed(1)}</span>`;
                        }}
                    ]
                });
            }

            startBackgroundUpdates() {
                // Update clock
                setInterval(() => {
                    const now = new Date();
                    document.getElementById('lastUpdate').textContent = 
                        `Última atualização: ${now.toLocaleTimeString()}`;
                }, 1000);

                // Update metrics
                setInterval(() => {
                    this.updateMetrics();
                }, 5000);

                // Update market data
                setInterval(() => {
                    this.updateMarketData();
                }, 2000);
            }

            updateMetrics() {
                // Update CPU usage
                const cpuUsage = 40 + Math.random() * 30;
                document.getElementById('cpuUsage').textContent = `${Math.round(cpuUsage)}%`;
                document.querySelector('#cpuUsage + .progress-bar').style.width = `${cpuUsage}%`;

                // Update memory usage
                const memoryUsage = 50 + Math.random() * 30;
                document.getElementById('memoryUsage').textContent = `${Math.round(memoryUsage)}%`;
                document.querySelector('#memoryUsage + .progress-bar').style.width = `${memoryUsage}%`;

                // Update GPU usage
                const gpuUsage = 10 + Math.random() * 20;
                document.getElementById('gpuUsage').textContent = `${Math.round(gpuUsage)}%`;
                document.querySelector('#gpuUsage + .progress-bar').style.width = `${gpuUsage}%`;

                // Update network latency
                const latency = 10 + Math.random() * 90;
                document.getElementById('networkLatency').textContent = `${Math.round(latency)}ms`;
                document.querySelector('#networkLatency + .progress-bar').style.width = `${Math.min(100, latency)}%`;

                // Update monitored assets
                this.updateMonitoredAssets();

                // Update active signals
                this.updateActiveSignals();

                // Update active alerts
                this.updateActiveAlerts();

                // Update recent activity
                this.updateRecentActivity();
            }

            updateMarketData() {
                // Simulate price updates
                if (this.performanceChart) {
                    const data = this.performanceChart.data.datasets[0].data;
                    data.push(10000 + Math.random() * 5000);
                    if (data.length > 30) data.shift();
                    this.performanceChart.update('none');
                }
            }

            updateMonitoredAssets() {
                const assets = [
                    {symbol: 'BTC/USDT', change: 2.34, isPositive: true},
                    {symbol: 'ETH/USDT', change: 1.89, isPositive: true},
                    {symbol: 'SOL/USDT', change: 0.56, isPositive: false},
                    {symbol: 'ADA/USDT', change: 0.42, isPositive: true},
                    {symbol: 'DOT/USDT', change: 3.21, isPositive: true}
                ];

                const container = document.getElementById('monitoredAssets');
                container.innerHTML = assets.map(asset => `
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span>${asset.symbol}</span>
                        <span class="${asset.isPositive ? 'text-success' : 'text-danger'}">
                            ${asset.isPositive ? '+' : ''}${asset.change}%
                        </span>
                    </div>
                `).join('');
            }

            updateActiveSignals() {
                const signals = [
                    {symbol: 'BTC/USDT', signal: 'BUY', confidence: 91.7},
                    {symbol: 'ETH/USDT', signal: 'HOLD', confidence: 76.8},
                    {symbol: 'SOL/USDT', signal: 'SELL', confidence: 84.2}
                ];

                const container = document.getElementById('activeSignals');
                container.innerHTML = signals.map(signal => `
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <div>
                            <span>${signal.symbol}</span>
                            <span class="badge ${signal.signal === 'BUY' ? 'bg-success' : signal.signal === 'SELL' ? 'bg-danger' : 'bg-warning'} ms-2">
                                ${signal.signal}
                            </span>
                        </div>
                        <span class="text-muted">${signal.confidence}%</span>
                    </div>
                `).join('');
            }

            updateActiveAlerts() {
                const alerts = [
                    {type: 'TRADE_SIGNAL', title: 'Novo Sinal de Compra', priority: 8},
                    {type: 'RISK_ALERT', title: 'Alta Volatilidade', priority: 6},
                    {type: 'SYSTEM_ALERT', title: 'API Reconectada', priority: 3}
                ];

                const container = document.getElementById('activeAlerts');
                container.innerHTML = alerts.map(alert => `
                    <div class="alert alert-custom ${this.getAlertClass(alert.type)} mb-2">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <i class="bi ${this.getAlertIcon(alert.type)} me-2"></i>
                                <small>${alert.title}</small>
                            </div>
                            <span class="badge ${alert.priority >= 8 ? 'bg-danger' : alert.priority >= 5 ? 'bg-warning' : 'bg-info'}">
                                ${alert.priority}
                            </span>
                        </div>
                    </div>
                `).join('');
            }

            updateRecentActivity() {
                const activities = [
                    {time: '14:30:25', type: 'INFO', description: 'Sistema inicializado', status: '✅', value: ''},
                    {time: '14:30:26', type: 'INFO', description: 'Conectado à Binance API', status: '✅', value: ''},
                    {time: '14:31:10', type: 'WARNING', description: 'Alta volatilidade detectada', status: '⚠️', value: ''},
                    {time: '14:31:15', type: 'SUCCESS', description: 'Ordem executada', status: '✅', value: '+$1,250.00'},
                    {time: '14:32:45', type: 'ERROR', description: 'Falha na conexão', status: '❌', value: ''}
                ];

                const container = document.getElementById('recentActivity');
                container.innerHTML = activities.map(activity => `
                    <tr>
                        <td>${activity.time}</td>
                        <td>${activity.type}</td>
                        <td>${activity.description}</td>
                        <td>${activity.status}</td>
                        <td>${activity.value}</td>
                    </tr>
                `).join('');
            }

            getAlertClass(type) {
                const classes = {
                    'TRADE_SIGNAL': 'alert-info',
                    'RISK_ALERT': 'alert-warning',
                    'SYSTEM_ALERT': 'alert-danger',
                    'PERFORMANCE_ALERT': 'alert-success'
                };
                return classes[type] || 'alert-info';
            }

            getAlertIcon(type) {
                const icons = {
                    'TRADE_SIGNAL': 'bi-graph-up',
                    'RISK_ALERT': 'bi-shield-exclamation',
                    'SYSTEM_ALERT': 'bi-exclamation-triangle',
                    'PERFORMANCE_ALERT': 'bi-graph-up-arrow'
                };
                return icons[type] || 'bi-info-circle';
            }

            toggleSystem() {
                const toggleBtn = document.getElementById('systemToggle');
                const statusElement = document.getElementById('systemStatus');
                
                this.isRunning = !this.isRunning;
                
                if (this.isRunning) {
                    toggleBtn.innerHTML = '<i class="bi bi-pause-fill me-1"></i> Parar Sistema';
                    toggleBtn.classList.remove('btn-success-custom');
                    toggleBtn.classList.add('btn-warning');
                    statusElement.textContent = 'Sistema iniciado';
                    this.showToast('Sistema iniciado com sucesso!', 'success');
                } else {
                    toggleBtn.innerHTML = '<i class="bi bi-play-fill me-1"></i> Iniciar Sistema';
                    toggleBtn.classList.remove('btn-warning');
                    toggleBtn.classList.add('btn-success-custom');
                    statusElement.textContent = 'Sistema parado';
                    this.showToast('Sistema parado com sucesso!', 'warning');
                }
            }

            changeExecutionMode(mode) {
                this.executionMode = mode;
                
                const currentModeElement = document.getElementById('currentMode');
                const modeDisplayElement = document.getElementById('executionModeDisplay');
                
                currentModeElement.textContent = mode;
                modeDisplayElement.textContent = `Modo: ${mode}`;
                
                const modeColors = {
                    'PAPER': 'info',
                    'LIVE': 'danger',
                    'SIMULATION': 'warning',
                    'BACKTEST': 'primary'
                };
                
                const dropdown = document.getElementById('executionModeDropdown');
                dropdown.classList.remove('btn-info', 'btn-danger', 'btn-warning', 'btn-primary');
                dropdown.classList.add(`btn-${modeColors[mode] || 'outline-light'}`);
                
                this.showToast(`Modo alterado para: ${mode}`, 'info');
            }

            showToast(message, type = 'info') {
                // Create toast element
                const toast = document.createElement('div');
                toast.className = `toast align-items-center text-bg-${type} border-0`;
                toast.setAttribute('role', 'alert');
                toast.setAttribute('aria-live', 'assertive');
                toast.setAttribute('aria-atomic', 'true');
                
                toast.innerHTML = `
                    <div class="d-flex">
                        <div class="toast-body">
                            ${message}
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                    </div>
                `;
                
                // Add to container
                const container = document.querySelector('.toast-container') || this.createToastContainer();
                container.appendChild(toast);
                
                // Initialize and show toast
                const bsToast = new bootstrap.Toast(toast);
                bsToast.show();
                
                // Remove after hiding
                toast.addEventListener('hidden.bs.toast', () => {
                    toast.remove();
                });
            }

            createToastContainer() {
                const container = document.createElement('div');
                container.className = 'toast-container position-fixed top-0 end-0 p-3';
                container.style.zIndex = '1060';
                document.body.appendChild(container);
                return container;
            }

            // Algorithm Management Methods
            loadAlgorithmCards() {
                const container = document.getElementById('algorithmCards');
                
                this.algorithms.forEach(algorithm => {
                    const card = this.createAlgorithmCard(algorithm);
                    container.appendChild(card);
                });
            }

            createAlgorithmCard(algorithm) {
                const performanceScore = this.calculatePerformanceScore(algorithm);
                
                const card = document.createElement('div');
                card.className = 'card card-glass mb-3 hover-lift';
                
                card.innerHTML = `
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <div class="d-flex align-items-center mb-1">
                                    <span class="led ${algorithm.isActive ? 'led-success' : 'led-danger'}"></span>
                                    <h5 class="mb-0">${algorithm.name} v${algorithm.version}</h5>
                                </div>
                                <span class="badge bg-primary">${algorithm.type}</span>
                            </div>
                            <div class="performance-score">
                                ${Math.round(performanceScore)}%
                            </div>
                        </div>
                        
                        <p class="text-muted mb-3">${algorithm.description}</p>
                        
                        <div class="row mb-3">
                            <div class="col-4">
                                <small class="text-muted d-block">🎯 Precisão</small>
                                <h6>${algorithm.accuracy.toFixed(1)}%</h6>
                            </div>
                            <div class="col-4">
                                <small class="text-muted d-block">📈 Win Rate</small>
                                <h6>${algorithm.winRate.toFixed(1)}%</h6>
                            </div>
                            <div class="col-4">
                                <small class="text-muted d-block">⚡ Sharpe</small>
                                <h6>${algorithm.sharpeRatio.toFixed(2)}</h6>
                            </div>
                        </div>
                        
                        <div class="d-flex justify-content-between">
                            <button class="btn btn-sm ${algorithm.isActive ? 'btn-warning' : 'btn-success'}" 
                                    onclick="app.toggleAlgorithm('${algorithm.id}')">
                                ${algorithm.isActive ? '⏸️ Pausar' : '▶️ Ativar'}
                            </button>
                            <div>
                                <button class="btn btn-sm btn-info me-2" onclick="app.optimizeAlgorithm('${algorithm.id}')">
                                    📈 Otimizar
                                </button>
                                <button class="btn btn-sm btn-secondary" onclick="app.showAlgorithmDetails('${algorithm.id}')">
                                    🔍 Detalhes
                                </button>
                            </div>
                        </div>
                    </div>
                `;
                
                return card;
            }

            calculatePerformanceScore(algorithm) {
                const weights = {
                    accuracy: 0.15,
                    winRate: 0.20,
                    sharpeRatio: 0.15,
                    maxDrawdown: -0.10
                };
                
                let score = 0;
                score += algorithm.accuracy * weights.accuracy;
                score += algorithm.winRate * weights.winRate;
                score += algorithm.sharpeRatio * 10 * weights.sharpeRatio;
                score += (100 - algorithm.maxDrawdown) * weights.maxDrawdown;
                
                return Math.max(0, Math.min(100, score));
            }

            toggleAlgorithm(id) {
                const algorithm = this.algorithms.find(a => a.id === id);
                if (algorithm) {
                    algorithm.isActive = !algorithm.isActive;
                    this.showToast(
                        `Algoritmo ${algorithm.name} ${algorithm.isActive ? 'ativado' : 'desativado'}`,
                        algorithm.isActive ? 'success' : 'warning'
                    );
                    // Refresh algorithm cards
                    document.getElementById('algorithmCards').innerHTML = '';
                    this.loadAlgorithmCards();
                }
            }

            optimizeAlgorithm(id) {
                this.showToast('Iniciando otimização do algoritmo...', 'info');
                // Simulate optimization process
                setTimeout(() => {
                    this.showToast('Otimização concluída!', 'success');
                }, 3000);
            }

            showAlgorithmDetails(id) {
                const algorithm = this.algorithms.find(a => a.id === id);
                if (!algorithm) return;
                
                const modal = new bootstrap.Modal(document.createElement('div'));
                modal._element.className = 'modal fade';
                modal._element.innerHTML = `
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content bg-dark">
                            <div class="modal-header">
                                <h5 class="modal-title">Detalhes: ${algorithm.name}</h5>
                                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <pre class="text-light">${JSON.stringify(algorithm, null, 2)}</pre>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                            </div>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(modal._element);
                modal.show();
                
                modal._element.addEventListener('hidden.bs.modal', () => {
                    modal._element.remove();
                });
            }
        }

        // Initialize application
        let app;
        document.addEventListener('DOMContentLoaded', () => {
            app = new AdvancedTradingDashboard();
            app.loadAlgorithmCards();
        });
    </script>
</body>
</html>