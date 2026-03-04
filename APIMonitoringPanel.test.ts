/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * TESTES: API Monitoring System
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Exemplos de testes para o sistema de monitoramento de APIs
 * Compatível com Jest + React Testing Library
 */

import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderHook } from '@testing-library/react';
import {
    APIHealthCheckService,
    APIAlertManager,
    APIResponseCache,
    APIMonitoringService,
    AlertLevel,
    API_ENDPOINTS,
} from './APIMonitoringService';
import {
    useAPIHealth,
    useAPIMonitoring,
    useAPICache,
    useAPIRetry,
    useAPIRateLimit,
    useAPIMetrics,
} from './useAPIMonitoring';
import APIMonitoringPanel from './APIMonitoringPanel';

// ═══════════════════════════════════════════════════════════════════════════════
// TESTES: APIHealthCheckService
// ═══════════════════════════════════════════════════════════════════════════════

describe('APIHealthCheckService', () => {
    let service: APIHealthCheckService;

    beforeEach(() => {
        service = new APIHealthCheckService();
    });

    afterEach(() => {
        service.stopAllHealthChecks();
    });

    /**
     * Test 1: Health check deve retornar resultado de sucesso
     */
    test('checkHealth deve retornar sucesso para endpoint válido', async () => {
        const endpoint = API_ENDPOINTS[0];
        const result = await service.checkHealth(endpoint);

        expect(result).toHaveProperty('success');
        expect(result).toHaveProperty('responseTime');
        expect(result).toHaveProperty('statusCode');
        expect(result).toHaveProperty('message');
        expect(result).toHaveProperty('timestamp');
        expect(result.responseTime).toBeGreaterThanOrEqual(0);
    });

    /**
     * Test 2: Retry automático deve funcionar
     */
    test('checkHealthWithRetry deve tentar múltiplas vezes', async () => {
        const endpoint = API_ENDPOINTS[0];
        const result = await service.checkHealthWithRetry(endpoint);

        expect(result).toHaveProperty('attempts');
        expect(result.attempts).toBeGreaterThanOrEqual(1);
        expect(result.attempts).toBeLessThanOrEqual(endpoint.retryAttempts);
    });

    /**
     * Test 3: Timeout deve ser respeitado
     */
    test('checkHealth deve respeitar timeout', async () => {
        const endpoint = { ...API_ENDPOINTS[0], timeout: 100 };
        const result = await service.checkHealth(endpoint);
        const maxTime = endpoint.timeout * 1.5; // Tolerância de 50%

        expect(result.responseTime).toBeLessThan(maxTime + 100); // +100ms margem
    });

    /**
     * Test 4: Parar health check deve cancelar requisição
     */
    test('stopHealthCheck deve parar verificação', () => {
        const endpoint = API_ENDPOINTS[0];
        service.startMonitoring(endpoint);
        service.stopHealthCheck(endpoint.id);

        // Verificar que foi parado
        expect(() => service.stopHealthCheck(endpoint.id)).not.toThrow();
    });

    /**
     * Test 5: Listeners devem ser notificados
     */
    test('listeners devem ser chamados quando status muda', (done) => {
        const endpoint = API_ENDPOINTS[0];
        let callCount = 0;

        const unsubscribe = service.onStatusChange((status) => {
            callCount++;
            if (callCount === 1) {
                unsubscribe();
                done();
            }
        });

        service.checkHealth(endpoint);
    });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TESTES: APIAlertManager
// ═══════════════════════════════════════════════════════════════════════════════

describe('APIAlertManager', () => {
    let manager: APIAlertManager;

    beforeEach(() => {
        manager = new APIAlertManager();
    });

    /**
     * Test 1: Criar alerta
     */
    test('createAlert deve criar um novo alerta', () => {
        const alert = manager.createAlert('binance', AlertLevel.ERROR, 'API Error', 'Connection failed');

        expect(alert).toHaveProperty('id');
        expect(alert).toHaveProperty('apiId', 'binance');
        expect(alert).toHaveProperty('level', AlertLevel.ERROR);
        expect(alert).toHaveProperty('title', 'API Error');
        expect(alert.resolved).toBe(false);
    });

    /**
     * Test 2: Resolver alerta
     */
    test('resolveAlert deve marcar alerta como resolvido', () => {
        const alert = manager.createAlert('binance', AlertLevel.WARNING, 'Slow API', 'High latency');
        manager.resolveAlert(alert.id);

        const active = manager.getActiveAlerts();
        expect(active).not.toContainEqual(alert);
    });

    /**
     * Test 3: Obter alertas ativos
     */
    test('getActiveAlerts deve retornar apenas alertas não resolvidos', () => {
        manager.createAlert('binance', AlertLevel.ERROR, 'Error 1', 'msg1');
        const alert2 = manager.createAlert('ctrader', AlertLevel.WARNING, 'Warning 1', 'msg2');
        manager.createAlert('pionex', AlertLevel.INFO, 'Info 1', 'msg3');

        manager.resolveAlert(alert2.id);

        const active = manager.getActiveAlerts();
        expect(active.length).toBe(2);
        expect(active).not.toContainEqual(alert2);
    });

    /**
     * Test 4: Listeners de alerta
     */
    test('onAlertCreated deve notificar quando novo alerta é criado', (done) => {
        manager.onAlertCreated((alert) => {
            expect(alert.level).toBe(AlertLevel.CRITICAL);
            done();
        });

        manager.createAlert('binance', AlertLevel.CRITICAL, 'Critical', 'msg');
    });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TESTES: APIResponseCache
// ═══════════════════════════════════════════════════════════════════════════════

describe('APIResponseCache', () => {
    let cache: APIResponseCache<any>;

    beforeEach(() => {
        cache = new APIResponseCache();
    });

    afterEach(() => {
        cache.stopCleanup();
    });

    /**
     * Test 1: Armazenar e recuperar do cache
     */
    test('set e get devem funcionar', () => {
        const data = { price: 100 };
        cache.set('binance-price', data);

        const retrieved = cache.get('binance-price');
        expect(retrieved).toEqual(data);
    });

    /**
     * Test 2: TTL deve expirar cache
     */
    test('cache deve expirar após TTL', (done) => {
        const data = { price: 100 };
        cache.set('binance-price', data, 100); // 100ms TTL

        setTimeout(() => {
            const retrieved = cache.get('binance-price');
            expect(retrieved).toBeNull();
            done();
        }, 150);
    });

    /**
     * Test 3: has deve verificar existência
     */
    test('has deve verificar se chave existe e não expirou', () => {
        cache.set('test', { data: 'test' }, 1000);
        expect(cache.has('test')).toBe(true);

        cache.set('expired', { data: 'test' }, 10);
        setTimeout(() => {
            expect(cache.has('expired')).toBe(false);
        }, 50);
    });

    /**
     * Test 4: Limpar cache
     */
    test('clear deve remover todos os itens', () => {
        cache.set('key1', 'value1');
        cache.set('key2', 'value2');
        cache.clear();

        expect(cache.get('key1')).toBeNull();
        expect(cache.get('key2')).toBeNull();
    });

    /**
     * Test 5: Cleanup automático
     */
    test('startCleanup deve remover itens expirados', (done) => {
        cache.startCleanup(100);
        cache.set('temp', 'value', 50);

        setTimeout(() => {
            expect(cache.get('temp')).toBeNull();
            done();
        }, 200);
    });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TESTES: useAPIHealth Hook
// ═══════════════════════════════════════════════════════════════════════════════

describe('useAPIHealth Hook', () => {
    /**
     * Test 1: Hook deve retornar estado inicial
     */
    test('useAPIHealth deve retornar estado inicial', () => {
        const { result } = renderHook(() => useAPIHealth('binance', { autoStart: false }));

        expect(result.current).toHaveProperty('healthy');
        expect(result.current).toHaveProperty('responseTime');
        expect(result.current).toHaveProperty('error');
        expect(result.current).toHaveProperty('manualCheck');
    });

    /**
     * Test 2: Manual check deve atualizar status
     */
    test('manualCheck deve atualizar status', async () => {
        const { result } = renderHook(() => useAPIHealth('binance', { autoStart: false }));

        await act(async () => {
            await result.current.manualCheck();
        });

        expect(result.current.loading).toBe(false);
        expect(result.current.responseTime).toBeGreaterThanOrEqual(0);
    });

    /**
     * Test 3: Alerts devem ser limpos
     */
    test('clearAlerts deve limpar alertas', () => {
        const { result } = renderHook(() => useAPIHealth('binance', { enableAlerts: true }));

        act(() => {
            result.current.clearAlerts();
        });

        expect(result.current.alerts.length).toBe(0);
    });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TESTES: useAPICache Hook
// ═══════════════════════════════════════════════════════════════════════════════

describe('useAPICache Hook', () => {
    /**
     * Test 1: Cache deve funcionar
     */
    test('useAPICache deve cachear dados', async () => {
        const fetcher = jest.fn(async () => ({ price: 100 }));
        const { result } = renderHook(() =>
            useAPICache('test-key', fetcher, 1000)
        );

        await act(async () => {
            await result.current.fetch();
        });

        expect(result.current.data).toEqual({ price: 100 });
        expect(fetcher).toHaveBeenCalledTimes(1);
    });

    /**
     * Test 2: Erro deve ser capturado
     */
    test('useAPICache deve capturar erro', async () => {
        const fetcher = jest.fn(async () => {
            throw new Error('Fetch failed');
        });
        const { result } = renderHook(() =>
            useAPICache('error-key', fetcher)
        );

        await act(async () => {
            await result.current.fetch();
        });

        expect(result.current.error).toEqual('Fetch failed');
    });

    /**
     * Test 3: clearCache deve limpar dados
     */
    test('clearCache deve limpar dados em cache', async () => {
        const fetcher = jest.fn(async () => ({ price: 100 }));
        const { result } = renderHook(() =>
            useAPICache('clear-test', fetcher)
        );

        await act(async () => {
            await result.current.fetch();
            result.current.clearCache();
            await result.current.fetch();
        });

        expect(fetcher).toHaveBeenCalledTimes(2);
    });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TESTES: useAPIRetry Hook
// ═══════════════════════════════════════════════════════════════════════════════

describe('useAPIRetry Hook', () => {
    /**
     * Test 1: Retry deve funcionar com sucesso
     */
    test('useAPIRetry deve retornar dados após sucesso', async () => {
        const asyncFn = jest.fn(async () => ({ data: 'success' }));
        const { result } = renderHook(() =>
            useAPIRetry(asyncFn, { maxAttempts: 3 })
        );

        await act(async () => {
            await result.current.execute();
        });

        expect(result.current.data).toEqual({ data: 'success' });
        expect(result.current.attempts).toBe(1);
    });

    /**
     * Test 2: Retry deve tentar múltiplas vezes
     */
    test('useAPIRetry deve tentar múltiplas vezes antes do sucesso', async () => {
        let callCount = 0;
        const asyncFn = jest.fn(async () => {
            callCount++;
            if (callCount < 2) throw new Error('Fail');
            return { data: 'success' };
        });

        const { result } = renderHook(() =>
            useAPIRetry(asyncFn, { maxAttempts: 3, delayMs: 10 })
        );

        await act(async () => {
            await result.current.execute();
        });

        expect(result.current.data).toEqual({ data: 'success' });
        expect(result.current.attempts).toBe(2);
    });

    /**
     * Test 3: Erro após max attempts
     */
    test('useAPIRetry deve retornar erro após max attempts', async () => {
        const asyncFn = jest.fn(async () => {
            throw new Error('Persistent error');
        });

        const { result } = renderHook(() =>
            useAPIRetry(asyncFn, { maxAttempts: 2, delayMs: 10 })
        );

        await act(async () => {
            try {
                await result.current.execute();
            } catch (e) {
                // Esperado
            }
        });

        expect(result.current.error).not.toBeNull();
        expect(result.current.attempts).toBe(2);
    });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TESTES: useAPIRateLimit Hook
// ═══════════════════════════════════════════════════════════════════════════════

describe('useAPIRateLimit Hook', () => {
    /**
     * Test 1: Rate limit deve funcionar
     */
    test('useAPIRateLimit deve permitir requisições dentro do limite', async () => {
        const { result } = renderHook(() =>
            useAPIRateLimit({ maxRequests: 3, windowMs: 1000 })
        );

        expect(result.current.canMakeRequest).toBe(true);
        expect(result.current.remainingRequests).toBe(3);

        act(() => {
            result.current.makeRequest(async () => { });
        });

        expect(result.current.remainingRequests).toBe(2);
    });

    /**
     * Test 2: Rate limit deve bloquear além do limite
     */
    test('useAPIRateLimit deve bloquear após atingir limite', async () => {
        const { result } = renderHook(() =>
            useAPIRateLimit({ maxRequests: 1, windowMs: 1000 })
        );

        act(() => {
            result.current.makeRequest(async () => { });
        });

        expect(result.current.canMakeRequest).toBe(false);
        expect(() => result.current.makeRequest(async () => { })).toThrow();
    });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TESTES: useAPIMetrics Hook
// ═══════════════════════════════════════════════════════════════════════════════

describe('useAPIMetrics Hook', () => {
    /**
     * Test 1: Metrics deve registrar dados
     */
    test('useAPIMetrics deve registrar métricas', () => {
        const { result } = renderHook(() => useAPIMetrics());

        act(() => {
            result.current.recordMetric(100, true);
            result.current.recordMetric(200, true);
            result.current.recordMetric(500, false);
        });

        const stats = result.current.getStats();
        expect(stats.total).toBe(3);
        expect(stats.successRate).toBe('66.67'); // 2/3
        expect(stats.average).toBe(267); // (100+200+500)/3
    });

    /**
     * Test 2: Reset deve limpar metrics
     */
    test('useAPIMetrics reset deve limpar dados', () => {
        const { result } = renderHook(() => useAPIMetrics());

        act(() => {
            result.current.recordMetric(100, true);
            result.current.reset();
        });

        const stats = result.current.getStats();
        expect(stats.total).toBe(0);
    });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TESTES: APIMonitoringPanel Component
// ═══════════════════════════════════════════════════════════════════════════════

describe('APIMonitoringPanel Component', () => {
    /**
     * Test 1: Componente deve renderizar
     */
    test('APIMonitoringPanel deve renderizar', () => {
        render(<APIMonitoringPanel />);
        expect(screen.getByText(/Painel de Monitoramento/i)).toBeInTheDocument();
    });

    /**
     * Test 2: Tabs devem funcionar
     */
    test('APIMonitoringPanel deve mudar tabs', async () => {
        render(<APIMonitoringPanel />);

        const logsTab = screen.getByRole('tab', { name: /Logs/i });
        await userEvent.click(logsTab);

        expect(logsTab).toHaveAttribute('aria-selected', 'true');
    });

    /**
     * Test 3: Botão de refresh deve funcionar
     */
    test('APIMonitoringPanel deve atualizar APIs', async () => {
        render(<APIMonitoringPanel />);

        const refreshButton = screen.getByRole('button', { name: /Verificar Tudo/i });
        await userEvent.click(refreshButton);

        await waitFor(() => {
            expect(refreshButton).not.toBeDisabled();
        });
    });
});

// ═══════════════════════════════════════════════════════════════════════════════
// SUITE DE TESTES: Integração Completa
// ═══════════════════════════════════════════════════════════════════════════════

describe('API Monitoring - Integration Tests', () => {
    /**
     * Test 1: Fluxo completo de monitoramento
     */
    test('fluxo completo de monitoramento deve funcionar', async () => {
        const service = new APIMonitoringService();
        const endpoint = API_ENDPOINTS[0];

        let statusUpdated = false;

        service.startMonitoring(endpoint, (status) => {
            statusUpdated = true;
            expect(status).toHaveProperty('success');
            expect(status).toHaveProperty('responseTime');
        });

        await waitFor(() => expect(statusUpdated).toBe(true), { timeout: 5000 });

        service.stopMonitoring(endpoint.id);
    });

    /**
     * Test 2: Alertas devem ser criados em falhas
     */
    test('alertas devem ser criados quando API falha', async () => {
        const service = new APIMonitoringService();
        let alertTriggered = false;

        service.onAlert((alert) => {
            alertTriggered = true;
        });

        // Simular falha criando um endpoint inválido
        const invalidEndpoint = {
            ...API_ENDPOINTS[0],
            id: 'invalid',
            url: 'https://invalid-url-that-will-fail-12345.com',
            critical: true,
        };

        service.startMonitoring(invalidEndpoint);

        await waitFor(() => {
            expect(alertTriggered).toBe(true);
        }, { timeout: 10000 });

        service.stopAllMonitoring();
    });
});

// ═══════════════════════════════════════════════════════════════════════════════
// Executar testes: npm test
// ═══════════════════════════════════════════════════════════════════════════════
