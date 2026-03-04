// BacktestingEngine.tsx
import React, { useState, useEffect, useCallback } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, ReferenceLine } from 'recharts';
import './BacktestingEngine.css';

// Tipos
interface BacktestResult {
  strategy: string;
  timeframe: string;
  startDate: string;
  endDate: string;
  totalReturn: number;
  annualizedReturn: number;
  volatility: number;
  sharpeRatio: number;
  maxDrawdown: number;
  winRate: number;
  profitFactor: number;
  totalTrades: number;
  avgTrade: number;
  calmarRatio: number;
  sortinoRatio: number;
}

interface EquityCurvePoint {
  date: string;
  equity: number;
  drawdown: number;
  benchmark: number;
}

interface TradeAnalysis {
  winningTrades: number;
  losingTrades: number;
  avgWin: number;
  avgLoss: number;
  largestWin: number;
  largestLoss: number;
  consecutiveWins: number;
  consecutiveLosses: number;
}

// Dados iniciais (equivalente aos init methods)
const initBacktestResults = (): BacktestResult[] => [
  {
    strategy: 'RSI Divergence',
    timeframe: '4H',
    startDate: '2023-01-01',
    endDate: '2024-12-01',
    totalReturn: 147.3,
    annualizedReturn: 73.6,
    volatility: 24.8,
    sharpeRatio: 2.97,
    maxDrawdown: -12.4,
    winRate: 68.7,
    profitFactor: 2.41,
    totalTrades: 287,
    avgTrade: 0.51,
    calmarRatio: 5.94,
    sortinoRatio: 4.23
  },
  {
    strategy: 'EMA Crossover',
    timeframe: '1H',
    startDate: '2023-01-01',
    endDate: '2024-12-01',
    totalReturn: 89.2,
    annualizedReturn: 44.6,
    volatility: 19.3,
    sharpeRatio: 2.31,
    maxDrawdown: -8.9,
    winRate: 72.4,
    profitFactor: 1.98,
    totalTrades: 412,
    avgTrade: 0.22,
    calmarRatio: 5.01,
    sortinoRatio: 3.47
  },
  {
    strategy: 'Bollinger Squeeze',
    timeframe: '15M',
    startDate: '2023-01-01',
    endDate: '2024-12-01',
    totalReturn: 123.8,
    annualizedReturn: 61.9,
    volatility: 31.2,
    sharpeRatio: 1.98,
    maxDrawdown: -18.7,
    winRate: 64.2,
    profitFactor: 2.78,
    totalTrades: 634,
    avgTrade: 0.19,
    calmarRatio: 3.31,
    sortinoRatio: 2.89
  },
  {
    strategy: 'Grid Trading',
    timeframe: '5M',
    startDate: '2023-01-01',
    endDate: '2024-12-01',
    totalReturn: 67.4,
    annualizedReturn: 33.7,
    volatility: 12.6,
    sharpeRatio: 2.67,
    maxDrawdown: -5.2,
    winRate: 78.9,
    profitFactor: 1.67,
    totalTrades: 1847,
    avgTrade: 0.04,
    calmarRatio: 6.48,
    sortinoRatio: 3.92
  },
  {
    strategy: 'Mean Reversion',
    timeframe: '1D',
    startDate: '2023-01-01',
    endDate: '2024-12-01',
    totalReturn: 92.7,
    annualizedReturn: 46.4,
    volatility: 16.8,
    sharpeRatio: 2.76,
    maxDrawdown: -9.1,
    winRate: 71.3,
    profitFactor: 2.12,
    totalTrades: 156,
    avgTrade: 0.59,
    calmarRatio: 5.10,
    sortinoRatio: 4.01
  }
];

const initEquityCurve = (): EquityCurvePoint[] => {
  const data: EquityCurvePoint[] = [];
  let equity = 10000;
  let benchmark = 10000;
  let maxEquity = equity;
  
  const startDate = new Date('2023-01-01');
  
  for (let i = 0; i < 365; i++) {
    const date = new Date(startDate);
    date.setDate(startDate.getDate() + i);
    const dateStr = date.toISOString().split('T')[0];
    
    // Simular performance da estratégia com viés positivo
    const strategyReturn = (Math.random() - 0.45) * 0.02;
    equity *= (1 + strategyReturn);
    
    // Simular performance do benchmark
    const benchmarkReturn = (Math.random() - 0.48) * 0.015;
    benchmark *= (1 + benchmarkReturn);
    
    // Calcular drawdown
    maxEquity = Math.max(maxEquity, equity);
    const drawdown = ((equity - maxEquity) / maxEquity) * 100;
    
    data.push({
      date: dateStr,
      equity: Math.round(equity),
      drawdown,
      benchmark: Math.round(benchmark)
    });
  }
  
  return data;
};

const initTradeAnalysis = (): TradeAnalysis => ({
  winningTrades: 197,
  losingTrades: 90,
  avgWin: 2.47,
  avgLoss: -1.02,
  largestWin: 12.34,
  largestLoss: -4.67,
  consecutiveWins: 8,
  consecutiveLosses: 3
});

// Componente principal
const BacktestingEngine: React.FC = () => {
  // Estados (equivalente aos states da classe)
  const [activeTab, setActiveTab] = useState<'results' | 'equity' | 'analysis'>('results');
  const [backtestResults, setBacktestResults] = useState<BacktestResult[]>(initBacktestResults);
  const [equityCurve, setEquityCurve] = useState<EquityCurvePoint[]>(initEquityCurve);
  const [tradeAnalysis, setTradeAnalysis] = useState<TradeAnalysis>(initTradeAnalysis);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [progress, setProgress] = useState<number>(0);
  const [selectedStrategy, setSelectedStrategy] = useState<string>('RSI Divergence');

  // Funções utilitárias (equivalentes aos métodos da classe)
  const getReturnColor = useCallback((value: number): string => {
    return value > 0 ? '#10b981' : '#ef4444';
  }, []);

  const formatPercent = useCallback((value: number): string => {
    return `${value > 0 ? '+' : ''}${value.toFixed(1)}%`;
  }, []);

  // Função de execução de backtest (equivalente a runBacktest)
  const runBacktest = useCallback(async () => {
    if (isRunning) return;
    
    setIsRunning(true);
    setProgress(0);
    
    // Simular execução do backtest
    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev + 2;
        
        if (newProgress >= 100) {
          clearInterval(interval);
          setIsRunning(false);
          
          // Atualizar resultados após conclusão
          setBacktestResults(prev => prev.map(result => ({
            ...result,
            totalReturn: result.totalReturn + (Math.random() - 0.5) * 5,
            sharpeRatio: Math.max(1, Math.min(4, result.sharpeRatio + (Math.random() - 0.5) * 0.2)),
            winRate: Math.max(55, Math.min(85, result.winRate + (Math.random() - 0.5) * 2))
          })));
          
          return 100;
        }
        
        return newProgress;
      });
    }, 100); // 100ms interval
    
    return () => clearInterval(interval);
  }, [isRunning]);

  // Sistema de atualizações periódicas (equivalente ao start_update_thread)
  useEffect(() => {
    const interval = setInterval(() => {
      if (!isRunning) {
        setBacktestResults(prev => prev.map(result => ({
          ...result,
          totalReturn: Math.max(20, Math.min(200, result.totalReturn + (Math.random() - 0.5) * 2)),
          sharpeRatio: Math.max(1, Math.min(4, result.sharpeRatio + (Math.random() - 0.5) * 0.1)),
          winRate: Math.max(55, Math.min(85, result.winRate + (Math.random() - 0.5) * 1))
        })));
      }
    }, 5000); // 5 segundos

    return () => clearInterval(interval);
  }, [isRunning]);

  // Componentes de renderização
  const renderHeader = () => {
    const statusText = isRunning ? `📊 EXECUTANDO ${progress}%` : '▶️ PRONTO';
    const statusColor = isRunning ? '#f59e0b' : '#10b981';

    return (
      <header className="backtest-header">
        <div className="backtest-header-left">
          <span className="backtest-header-icon">📊</span>
          <h1 className="backtest-header-title">Engine de Backtesting</h1>
        </div>
        <div className="backtest-header-right">
          <div 
            className="backtest-badge status-badge"
            style={{ backgroundColor: statusColor }}
          >
            {statusText}
          </div>
          <div className="backtest-badge strategies-badge">
            {backtestResults.length} ESTRATÉGIAS
          </div>
        </div>
      </header>
    );
  };

  const renderTabs = () => (
    <div className="backtest-tabs">
      <button 
        className={`backtest-tab ${activeTab === 'results' ? 'active' : ''}`}
        onClick={() => setActiveTab('results')}
      >
        📋 Resultados
      </button>
      <button 
        className={`backtest-tab ${activeTab === 'equity' ? 'active' : ''}`}
        onClick={() => setActiveTab('equity')}
      >
        📈 Curva de Equity
      </button>
      <button 
        className={`backtest-tab ${activeTab === 'analysis' ? 'active' : ''}`}
        onClick={() => setActiveTab('analysis')}
      >
        🔍 Análise de Trades
      </button>
    </div>
  );

  const renderResultCard = (result: BacktestResult, index: number) => (
    <div key={index} className="result-card">
      <div className="result-header">
        <div className="result-header-left">
          <span className="result-icon">🧮</span>
          <div className="result-info">
            <h3 className="result-strategy">{result.strategy}</h3>
            <p className="result-meta">
              {result.timeframe} • {result.startDate} - {result.endDate}
            </p>
          </div>
        </div>
        <div className="result-header-right">
          <div 
            className="result-total-return"
            style={{ color: getReturnColor(result.totalReturn) }}
          >
            +{result.totalReturn.toFixed(1)}%
          </div>
        </div>
      </div>

      <div className="result-main-metrics">
        <div className="main-metric">
          <span className="metric-label">Retorno Anual</span>
          <span className="metric-value" style={{ color: '#3b82f6' }}>
            {result.annualizedReturn.toFixed(1)}%
          </span>
        </div>
        <div className="main-metric">
          <span className="metric-label">Sharpe Ratio</span>
          <span className="metric-value">{result.sharpeRatio.toFixed(2)}</span>
        </div>
        <div className="main-metric">
          <span className="metric-label">Max Drawdown</span>
          <span className="metric-value" style={{ color: '#ef4444' }}>
            {result.maxDrawdown.toFixed(1)}%
          </span>
        </div>
      </div>

      <div className="result-detail-metrics">
        <div className="detail-metric">
          <span className="metric-label">Win Rate</span>
          <span className="metric-value">{result.winRate.toFixed(1)}%</span>
        </div>
        <div className="detail-metric">
          <span className="metric-label">Profit Factor</span>
          <span className="metric-value">{result.profitFactor.toFixed(2)}</span>
        </div>
        <div className="detail-metric">
          <span className="metric-label">Total Trades</span>
          <span className="metric-value">{result.totalTrades}</span>
        </div>
        <div className="detail-metric">
          <span className="metric-label">Calmar Ratio</span>
          <span className="metric-value">{result.calmarRatio.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );

  const renderResultsTab = () => (
    <div className="results-tab">
      {/* Progress Bar */}
      {isRunning && (
        <div className="progress-section">
          <h3 className="progress-title">Executando Backtest: {progress}%</h3>
          <div className="progress-bar">
            <div 
              className="progress-fill"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="progress-text">Processando dados históricos...</p>
        </div>
      )}

      {/* Botão de Execução */}
      <div className="execution-controls">
        <button 
          onClick={runBacktest}
          disabled={isRunning}
          className={`execute-button ${isRunning ? 'running' : 'ready'}`}
        >
          {isRunning ? '⏸️ Executando...' : '▶️ Executar Backtest'}
        </button>
      </div>

      {/* Lista de Resultados */}
      <div className="results-list">
        {backtestResults.map((result, index) => renderResultCard(result, index))}
      </div>
    </div>
  );

  const renderEquityTab = () => {
    // Formatar datas para o gráfico
    const formattedData = equityCurve.map(point => ({
      ...point,
      date: new Date(point.date).toLocaleDateString('pt-BR', { month: 'short', day: 'numeric' })
    }));

    return (
      <div className="equity-tab">
        <div className="equity-chart">
          <ResponsiveContainer width="100%" height={500}>
            <LineChart data={formattedData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis 
                dataKey="date" 
                stroke="#6b7280"
                fontSize={12}
                interval={30}
              />
              <YAxis 
                stroke="#6b7280"
                fontSize={12}
                tickFormatter={(value) => `$${value.toLocaleString()}`}
              />
              <Tooltip 
                formatter={(value) => [`$${Number(value).toLocaleString()}`, 'Valor']}
                labelFormatter={(label) => `Data: ${label}`}
                contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e5e7eb' }}
              />
              <Legend />
              <Area 
                type="monotone" 
                dataKey="equity" 
                stroke="#3b82f6" 
                fill="#3b82f6" 
                fillOpacity={0.3}
                strokeWidth={2}
                name="Estratégia"
              />
              <Area 
                type="monotone" 
                dataKey="benchmark" 
                stroke="#6b7280" 
                fill="#6b7280" 
                fillOpacity={0.2}
                strokeWidth={1}
                name="Benchmark"
              />
              <ReferenceLine y={10000} stroke="#6b7280" strokeDasharray="3 3" label="Início" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Estatísticas da Curva */}
        <div className="equity-stats">
          <div className="stat-card">
            <h4>Retorno Total</h4>
            <div className="stat-value" style={{ color: '#10b981' }}>
              {((equityCurve[equityCurve.length - 1]?.equity - 10000) / 10000 * 100).toFixed(1)}%
            </div>
          </div>
          <div className="stat-card">
            <h4>Max Drawdown</h4>
            <div className="stat-value" style={{ color: '#ef4444' }}>
              {Math.min(...equityCurve.map(p => p.drawdown)).toFixed(1)}%
            </div>
          </div>
          <div className="stat-card">
            <h4>Sharpe Ratio</h4>
            <div className="stat-value">2.97</div>
          </div>
          <div className="stat-card">
            <h4>Volatilidade</h4>
            <div className="stat-value">24.8%</div>
          </div>
        </div>
      </div>
    );
  };

  const renderAnalysisTab = () => (
    <div className="analysis-tab">
      {/* Cards de Trades */}
      <div className="trades-grid">
        <div className="trade-card winner-card">
          <h3>📈 Trades Vencedores</h3>
          <div className="trade-value">{tradeAnalysis.winningTrades}</div>
          <div className="trade-avg">
            Avg: +{tradeAnalysis.avgWin.toFixed(2)}%
          </div>
        </div>
        <div className="trade-card loser-card">
          <h3>📉 Trades Perdedores</h3>
          <div className="trade-value">{tradeAnalysis.losingTrades}</div>
          <div className="trade-avg">
            Avg: {tradeAnalysis.avgLoss.toFixed(2)}%
          </div>
        </div>
      </div>

      {/* Extremos */}
      <div className="extremes-grid">
        <div className="extreme-card">
          <h4>Maior Ganho</h4>
          <div className="extreme-value" style={{ color: '#10b981' }}>
            +{tradeAnalysis.largestWin.toFixed(2)}%
          </div>
        </div>
        <div className="extreme-card">
          <h4>Maior Perda</h4>
          <div className="extreme-value" style={{ color: '#ef4444' }}>
            {tradeAnalysis.largestLoss.toFixed(2)}%
          </div>
        </div>
      </div>

      {/* Sequências */}
      <div className="sequences-grid">
        <div className="sequence-card">
          <h4>Vitórias Consecutivas</h4>
          <div className="sequence-value" style={{ color: '#10b981' }}>
            {tradeAnalysis.consecutiveWins}
          </div>
        </div>
        <div className="sequence-card">
          <h4>Perdas Consecutivas</h4>
          <div className="sequence-value" style={{ color: '#ef4444' }}>
            {tradeAnalysis.consecutiveLosses}
          </div>
        </div>
      </div>

      {/* Análise de Performance */}
      <div className="performance-analysis">
        <h3>📊 Análise de Performance</h3>
        <div className="performance-metrics">
          <div className="performance-metric">
            <span>Win Rate:</span>
            <span className="metric-value">
              {((tradeAnalysis.winningTrades / (tradeAnalysis.winningTrades + tradeAnalysis.losingTrades)) * 100).toFixed(1)}%
            </span>
          </div>
          <div className="performance-metric">
            <span>Profit Factor:</span>
            <span className="metric-value">2.41</span>
          </div>
          <div className="performance-metric">
            <span>Expectativa Matemática:</span>
            <span className="metric-value" style={{ color: '#10b981' }}>
              +0.51%
            </span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'results':
        return renderResultsTab();
      case 'equity':
        return renderEquityTab();
      case 'analysis':
        return renderAnalysisTab();
      default:
        return renderResultsTab();
    }
  };

  const renderControls = () => (
    <div className="backtest-controls">
      <button 
        onClick={() => setBacktestResults(initBacktestResults())}
        className="btn btn-info"
      >
        🔄 Resetar Dados
      </button>
      <button 
        onClick={() => setIsRunning(false)}
        disabled={!isRunning}
        className="btn btn-warning"
      >
        ⏹️ Parar Backtest
      </button>
      <button 
        onClick={() => console.log('Exportando dados...')}
        className="btn btn-success"
      >
        📤 Exportar Resultados
      </button>
    </div>
  );

  return (
    <div className="backtest-container">
      <div className="backtest-main-card">
        {renderHeader()}
        {renderControls()}
        {renderTabs()}
        <div className="backtest-content">
          {renderTabContent()}
        </div>
      </div>
    </div>
  );
};

export default BacktestingEngine;