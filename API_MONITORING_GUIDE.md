# 📡 Painel de Monitoramento de APIs - Guia Completo

## 🎯 Visão Geral

Este painel oferece **monitoramento em tempo real** de suas APIs com:

- ✅ **Health Checks Automáticos** - Verificação periódica do status
- ⚡ **Latência em Tempo Real** - Monitoramento de performance
- 📊 **Métricas Detalhadas** - Uptime, taxa de erro, requisições/minuto
- 🔔 **Sistema de Alertas** - Notificações de falhas e degradação
- 📈 **Dashboard de Performance** - Gráficos e histórico
- 🔄 **Retry Automático** - Recuperação inteligente de falhas
- 💾 **Cache de Respostas** - Otimização de requisições

---

## 📁 Arquivos Criados

### 1. **APIMonitoringPanel.tsx** (1,000+ linhas)

Componente React principal com interface completa.

**Recursos:**

- Dashboard com 3 abas: APIs, Logs, Métricas
- Cards individuais para cada API com status em tempo real
- Tabela de logs de requisições
- Gráficos de performance
- Dialog detalhado para cada API
- Auto-refresh configurável

### 2. **APIMonitoringService.ts** (400+ linhas)

Serviço TypeScript para gerenciar APIs.

**Classes:**

- `APIHealthCheckService` - Verificação de saúde
- `APIAlertManager` - Sistema de alertas
- `APIResponseCache` - Cache inteligente
- `APIMonitoringService` - Orquestração integrada

### 3. **useAPIMonitoring.ts** (350+ linhas)

Hooks React customizados para fácil integração.

**Hooks disponíveis:**

- `useAPIHealth()` - Monitorar uma API individual
- `useAPIMonitoring()` - Monitorar todas as APIs
- `useAPICache()` - Cachear respostas
- `useAPIRetry()` - Retry automático com backoff
- `useAPIRateLimit()` - Controlar limite de requisições
- `useAPIMetrics()` - Coletar métricas

---

## 🚀 Como Usar

### Opção 1: Usar o Painel Completo

```tsx
import APIMonitoringPanel from './APIMonitoringPanel';

function App() {
  return (
    <div>
      <APIMonitoringPanel />
    </div>
  );
}

export default App;
```

---

### Opção 2: Usar Hooks Individuais

#### **Monitorar uma API específica**

```tsx
import { useAPIHealth } from './useAPIMonitoring';

function MyComponent() {
  const { healthy, responseTime, lastCheck, error, manualCheck } = useAPIHealth(
    'binance',
    { autoStart: true, interval: 30000 }
  );

  return (
    <div>
      <p>Status: {healthy ? '✅ OK' : '❌ Erro'}</p>
      <p>Tempo: {responseTime}ms</p>
      <p>Última verificação: {lastCheck.toLocaleTimeString()}</p>
      {error && <p style={{ color: 'red' }}>Erro: {error}</p>}
      <button onClick={manualCheck}>Verificar Agora</button>
    </div>
  );
}
```

#### **Monitorar todas as APIs**

```tsx
import { useAPIMonitoring } from './useAPIMonitoring';

function Dashboard() {
  const { allAPIsStatus, alerts, getOverallHealth, getAverageResponseTime } = 
    useAPIMonitoring();

  const health = getOverallHealth();
  const avgTime = getAverageResponseTime();

  return (
    <div>
      <h2>Status Geral</h2>
      <p>Saudáveis: {health.healthy}</p>
      <p>Indisponíveis: {health.unhealthy}</p>
      <p>Tempo médio: {avgTime}ms</p>
      
      <h3>Alertas ({alerts.length})</h3>
      {alerts.map(alert => (
        <div key={alert.id} style={{ color: alert.level }}>
          {alert.title}: {alert.message}
        </div>
      ))}
    </div>
  );
}
```

#### **Cachear respostas de API**

```tsx
import { useAPICache } from './useAPIMonitoring';

function PricesComponent() {
  const { data, loading, error, fetch } = useAPICache(
    'binance-prices',
    async () => {
      const response = await fetch('https://api.binance.com/api/v3/ticker/price');
      return response.json();
    },
    60000 // Cache por 60 segundos
  );

  return (
    <div>
      {loading && <p>Carregando...</p>}
      {error && <p>Erro: {error}</p>}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
      <button onClick={fetch}>Atualizar</button>
    </div>
  );
}
```

#### **Usar Retry automático**

```tsx
import { useAPIRetry } from './useAPIMonitoring';

function RobustComponent() {
  const { data, loading, error, attempts, execute } = useAPIRetry(
    async () => {
      const response = await fetch('/api/data');
      if (!response.ok) throw new Error('Falha na requisição');
      return response.json();
    },
    {
      maxAttempts: 3,
      delayMs: 1000,
      backoffMultiplier: 2,
      onRetry: (attempt, error) => {
        console.log(`Tentativa ${attempt} falhou:`, error.message);
      },
    }
  );

  return (
    <div>
      <button onClick={execute}>Tentar</button>
      <p>Tentativas: {attempts}/3</p>
      {loading && <p>Processando...</p>}
      {error && <p style={{ color: 'red' }}>Erro: {error.message}</p>}
      {data && <p>Sucesso: {JSON.stringify(data)}</p>}
    </div>
  );
}
```

#### **Controlar Rate Limit**

```tsx
import { useAPIRateLimit } from './useAPIMonitoring';

function RateLimitedComponent() {
  const { canMakeRequest, requestCount, remainingRequests, makeRequest } = 
    useAPIRateLimit({ maxRequests: 10, windowMs: 1000 });

  const handleFetch = async () => {
    try {
      await makeRequest(async () => {
        const response = await fetch('/api/data');
        return response.json();
      });
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div>
      <p>Requisições: {requestCount}/10</p>
      <p>Restantes: {remainingRequests}</p>
      <button onClick={handleFetch} disabled={!canMakeRequest}>
        Fetch
      </button>
    </div>
  );
}
```

#### **Coletar Métricas**

```tsx
import { useAPIMetrics } from './useAPIMonitoring';

function MetricsComponent() {
  const { metrics, recordMetric, getStats, reset } = useAPIMetrics();
  const stats = getStats();

  return (
    <div>
      <h3>Estatísticas</h3>
      <p>Total: {stats.total}</p>
      <p>Média: {stats.average}ms</p>
      <p>Min/Max: {stats.min}/{stats.max}ms</p>
      <p>Taxa de Sucesso: {stats.successRate}%</p>
      <button onClick={() => recordMetric(250, true)}>Registrar Sucesso</button>
      <button onClick={() => recordMetric(5000, false)}>Registrar Falha</button>
      <button onClick={reset}>Limpar</button>
    </div>
  );
}
```

---

## 🔧 Configuração

### Editar Endpoints

Abra `APIMonitoringService.ts` e modifique `API_ENDPOINTS`:

```typescript
export const API_ENDPOINTS: APIEndpointConfig[] = [
  {
    id: 'minha-api',
    name: 'Minha API Customizada',
    url: 'https://api.exemplo.com',
    healthCheckEndpoint: '/health',
    healthCheckInterval: 30000,
    timeout: 5000,
    retryAttempts: 3,
    retryDelay: 1000,
    region: 'Brasil',
    critical: true,
    notifyOnFailure: true,
  },
  // ... mais APIs
];
```

### Configurar Alertas

```typescript
export const HEALTH_CHECK_CONFIG: HealthCheckConfig = {
  enabled: true,
  interval: 30000, // Verificar a cada 30 segundos
  timeout: 5000,   // Timeout de 5 segundos
  retries: 3,      // Tentar 3 vezes
  alertThreshold: {
    responseTime: 1000,      // Alerta se > 1s
    errorRate: 5,            // Alerta se > 5%
    consecutiveFailures: 3,  // Alerta se 3 falhas seguidas
  },
};
```

---

## 📊 Integração com App Existente

### Em `App.tsx`

```tsx
import React from 'react';
import APIMonitoringPanel from './APIMonitoringPanel';
import BrokerIntegration from './BrokerIntegration';

function App() {
  return (
    <div>
      {/* Seu conteúdo existente */}
      <BrokerIntegration />
      
      {/* Novo painel */}
      <APIMonitoringPanel />
    </div>
  );
}

export default App;
```

### Ou em um novo layout com tabs

```tsx
import { Tabs, TabPanel } from '@mui/material';

function App() {
  const [tab, setTab] = React.useState(0);

  return (
    <Tabs value={tab} onChange={(e, v) => setTab(v)}>
      <Tab label="Trading" />
      <Tab label="APIs" />
      <Tab label="Configurações" />
    </Tabs>

    {tab === 0 && <BrokerIntegration />}
    {tab === 1 && <APIMonitoringPanel />}
    {tab === 2 && <SettingsPage />}
  );
}
```

---

## 🎨 Personalizações

### Cores dos Status

Edite em `APIMonitoringPanel.tsx`:

```tsx
const HealthChip = styled(Chip)<{ status: APIHealthStatus }>(
  ({ theme, status }) => ({
    // Customizar aqui
  })
);
```

### Temas Material-UI

```tsx
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: { main: '#1976d2' },
    success: { main: '#4caf50' },
    warning: { main: '#ff9800' },
    error: { main: '#f44336' },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <APIMonitoringPanel />
    </ThemeProvider>
  );
}
```

---

## 📈 Performance

### Otimizações Implementadas

1. **Cache Automático** - Respostas são cacheadas
2. **Debounce** - Requisições não são feitas em excesso
3. **Lazy Loading** - Componentes carregam sob demanda
4. **Paginação** - Logs são exibidos em páginas
5. **Limpeza de Memória** - Histórico limitado a 100 items

### Monitoramento de Performance

```tsx
import { useAPIMetrics } from './useAPIMonitoring';

function PerformanceMonitor() {
  const { recordMetric, getStats } = useAPIMetrics();

  React.useEffect(() => {
    const startTime = performance.now();
    
    // Sua operação aqui
    const duration = performance.now() - startTime;
    recordMetric(duration, true);
  }, []);
}
```

---

## 🔒 Segurança

### Headers de Autenticação

Modifique em `APIMonitoringService.ts`:

```typescript
async checkHealth(endpoint: APIEndpointConfig) {
  const headers = new Headers({
    'Authorization': `Bearer ${YOUR_TOKEN}`,
    'Content-Type': 'application/json',
  });

  const response = await fetch(endpoint.url, { headers });
  // ...
}
```

### Rate Limiting

```tsx
const { canMakeRequest, makeRequest } = useAPIRateLimit({
  maxRequests: 100,
  windowMs: 60000, // 100 requisições por minuto
});
```

---

## 🐛 Debugging

### Ativar Logging

```typescript
// Em APIMonitoringService.ts
private notifyListeners(status: any) {
  console.log('[API Health]', status); // Debug
  this.listeners.forEach(listener => listener(status));
}
```

### Inspeccionar Cache

```typescript
const stats = responseCache.getStats();
console.log('Cache:', stats);
// Output: { size: 5, entries: [...] }
```

---

## 📞 Suporte

Para erros ou dúvidas:

1. Verifique `console.error()` para mensagens de erro
2. Inspecione a aba "Logs" para histórico de requisições
3. Use a aba "Métricas" para ver performance geral

---

## ✅ Checklist de Integração

- [ ] Cópia dos 3 arquivos (TSX, TS, TS hooks)
- [ ] Importação em App.tsx
- [ ] Verificação das dependências Material-UI
- [ ] Teste do componente de monitoramento
- [ ] Configuração das APIs (endpoints)
- [ ] Verificação de alertas funcionando
- [ ] Teste do auto-refresh
- [ ] Verificação de performance

---

**Versão:** 1.0.0  
**Data:** 2025-01-16  
**Compatibilidade:** React 18+, TypeScript 4.5+, Material-UI v5
