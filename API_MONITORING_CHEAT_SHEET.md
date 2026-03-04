# 📋 Quick Reference - Painel de API

## 🚀 INÍCIO RÁPIDO (30 segundos)

### Passo 1: Copiar Arquivos

```bash
cp APIMonitoringPanel.tsx src/
cp APIMonitoringService.ts src/
cp useAPIMonitoring.ts src/
```

### Passo 2: Adicionar ao App

```tsx
// App.tsx
import APIMonitoringPanel from './APIMonitoringPanel';

export default function App() {
  return <APIMonitoringPanel />;
}
```

### Passo 3: Executar

```bash
npm start
```

✅ **Pronto! Veja em <http://localhost:3000>**

---

## 📖 CHEAT SHEET

### **Monitorar 1 API**

```tsx
const { healthy, responseTime, manualCheck } = useAPIHealth('binance');
// Resultado: ✅ ou ❌ + tempo em ms
```

### **Monitorar Todas as APIs**

```tsx
const { allAPIsStatus, alerts, getOverallHealth } = useAPIMonitoring();
// health = { healthy: 3, degraded: 0, unhealthy: 0 }
```

### **Cache com TTL**

```tsx
const { data, fetch } = useAPICache('key', fetcher, 60000);
// 60 segundos de cache
```

### **Retry Automático**

```tsx
const { execute, data, attempts } = useAPIRetry(fetchFn, { maxAttempts: 3 });
// Tenta até 3 vezes com backoff
```

### **Rate Limit**

```tsx
const { canMakeRequest, makeRequest } = useAPIRateLimit({ 
  maxRequests: 10, 
  windowMs: 1000 
});
// 10 requisições por segundo
```

### **Coletar Métricas**

```tsx
const { recordMetric, getStats } = useAPIMetrics();
recordMetric(250, true); // responseTime, success
const stats = getStats(); // { average, min, max, successRate }
```

---

## 🎨 COMPONENTES

| Componente | Importar | Uso |
|-----------|----------|-----|
| **APIMonitoringPanel** | `import APIMonitoringPanel from './APIMonitoringPanel'` | Dashboard completo |
| **EnhancedBrokerIntegration** | `import Enhanced from './EnhancedBrokerIntegration'` | Com monitoramento |

---

## 🔧 CONFIGURAÇÃO RÁPIDA

### Adicionar API

```typescript
// APIMonitoringService.ts
export const API_ENDPOINTS = [
  {
    id: 'minha-api',
    name: 'Minha API',
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
];
```

### Customizar Alertas

```typescript
export const HEALTH_CHECK_CONFIG = {
  interval: 30000,
  timeout: 5000,
  retries: 3,
  alertThreshold: {
    responseTime: 1000,    // > 1s = alerta
    errorRate: 5,          // > 5% = alerta
    consecutiveFailures: 3, // 3 falhas = alerta
  },
};
```

---

## 💾 ESTADO & PROPS

### useAPIHealth

```typescript
{
  healthy: boolean,           // Saudável?
  responseTime: number,       // ms
  lastCheck: Date,           // Última verificação
  error: string | null,      // Mensagem de erro
  loading: boolean,          // Carregando?
  alerts: APIAlert[],        // Alertas ativos
  manualCheck: () => void,   // Verificar agora
  clearAlerts: () => void,   // Limpar alertas
}
```

### useAPIMonitoring

```typescript
{
  allAPIsStatus: Record<string, HealthStatus>,
  alerts: APIAlert[],
  stats: Record<string, APIStats>,
  getOverallHealth: () => { healthy, degraded, unhealthy },
  getAverageResponseTime: () => number,
  resolveAlert: (alertId: string) => void,
}
```

---

## ⚠️ ERROS COMUNS

### ❌ Erro: "Module not found"

**Solução:** Verifique o caminho de importação

```tsx
// ✅ Correto
import APIMonitoringPanel from './APIMonitoringPanel';

// ❌ Errado
import APIMonitoringPanel from 'APIMonitoringPanel';
```

### ❌ Erro: "Cannot find module '@mui/material'"

**Solução:** Instale Material-UI

```bash
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material
```

### ❌ APIs não monitoradas

**Solução:** Verifique `API_ENDPOINTS` contém suas APIs

```typescript
console.log(API_ENDPOINTS); // Debug
```

### ❌ Alertas não funcionam

**Solução:** Ative `enableAlerts: true`

```tsx
useAPIHealth('binance', { enableAlerts: true })
```

---

## 📊 STATUS CODES

### Cores por Status

```
🟢 Verde (Saudável):  < 300ms, uptime > 99.5%
🟡 Amarelo (Degradado): 300-1000ms, uptime 99-99.5%
🔴 Vermelho (Erro):   > 1000ms, uptime < 99%
```

### Icons

```
✅ Conectado/Saudável
⚠️ Degradado/Aviso
❌ Erro/Desconectado
⏳ Conectando...
❓ Desconhecido
```

---

## 🧪 TESTAR

### Executar Suite de Testes

```bash
npm test APIMonitoringPanel.test.ts
```

### Testar Hook Individual

```typescript
import { renderHook, act } from '@testing-library/react';
import { useAPIHealth } from './useAPIMonitoring';

const { result } = renderHook(() => useAPIHealth('binance'));
await act(async () => {
  await result.current.manualCheck();
});
```

---

## 🔌 INTEGRAÇÃO COM BACKEND

### Conectar com API Real

```typescript
// APIMonitoringService.ts
async checkHealth(endpoint: APIEndpointConfig) {
  const headers = {
    'Authorization': `Bearer ${process.env.REACT_APP_API_TOKEN}`,
  };
  
  const response = await fetch(endpoint.url, { headers });
  // ...
}
```

### Persistir Histórico

```typescript
service.onAlert(async (alert) => {
  await fetch('/api/alerts', {
    method: 'POST',
    body: JSON.stringify(alert),
  });
});
```

---

## 📱 RESPONSIVO

### Mobile-First

- ✅ Funciona em celular
- ✅ Tabs escondidas em mobile
- ✅ Cards em grid responsivo
- ✅ Fontes legíveis

### Testar

```bash
# DevTools > Device Toolbar (F12)
```

---

## 🎯 CASOS DE USO

### 1️⃣ Dashboard de APIs

```tsx
<APIMonitoringPanel />
```

### 2️⃣ Widget em Sidebar

```tsx
const { allAPIsStatus, getOverallHealth } = useAPIMonitoring();
<div>
  {Object.entries(allAPIsStatus).map(([id, status]) => (
    <div key={id}>{id}: {status.healthy ? '✅' : '❌'}</div>
  ))}
</div>
```

### 3️⃣ Verificação em Trade

```tsx
const { healthy } = useAPIHealth('binance');
if (!healthy) {
  alert('API da Binance está lenta!');
  return;
}
// Proceder com trade
```

### 4️⃣ Fallback em Erro

```tsx
const { data, fetch } = useAPICache('prices', fetchPrices, 300000);
useEffect(() => {
  fetch().catch(() => {
    // Usar dados em cache ou padrão
  });
}, []);
```

---

## 🔗 LINKS ÚTEIS

- 📚 [Documentação Completa](./API_MONITORING_GUIDE.md)
- 🎯 [Implementação](./API_MONITORING_IMPLEMENTATION.md)
- ✅ [Checklist de Integração](./ENTREGA_PAINEL_API_COMPLETO.md)
- 🧪 [Testes](./APIMonitoringPanel.test.ts)

---

## 🚀 PERFORMANCE

| Operação | Tempo |
|----------|-------|
| Health check | ~250ms |
| Renderizar dashboard | < 100ms |
| Cache hit | < 1ms |
| Retry com backoff | 1-4s |

---

## 💡 DICAS

1. **Auto-refresh**: Deixe ligado em produção
2. **Cache**: Configure TTL baseado em seus dados
3. **Alertas**: Customize thresholds para suas APIs
4. **Logs**: Ative em desenvolvimento, desative em produção
5. **Rate Limit**: Ajuste conforme necessário

---

## 🎓 EXEMPLOS PRONTOS

```tsx
// 1. Health Check Simples
const health = useAPIHealth('binance');

// 2. Dashboard Completo
const monitor = useAPIMonitoring();

// 3. Com Retry
const { execute } = useAPIRetry(fetchFn);

// 4. Com Cache
const { data } = useAPICache('key', fetchFn, 60000);

// 5. Com Rate Limit
const { makeRequest } = useAPIRateLimit();

// 6. Com Métricas
const { recordMetric, getStats } = useAPIMetrics();
```

---

## 📞 SUPORTE

**Dúvida?** Verifique:

1. Console.error em DevTools (F12)
2. Documentação (README.md)
3. Exemplos (*.test.ts)
4. Tipos TypeScript (*.d.ts)

---

## ✨ RESUMO

| Item | Status |
|------|--------|
| **Arquivos** | 6 criados |
| **Linhas** | ~4,150 |
| **Funcionalidades** | 10 implementadas |
| **Hooks** | 6 customizados |
| **Testes** | 33+ unitários |
| **Documentação** | Completa |
| **Pronto** | ✅ SIM |

---

**Desenvolvido com ❤️ para LEXTRADER-IAG 4.0**  
**v1.0.0 | 2025-01-16**
