// ═══════════════════════════════════════════════════════════════════════════════
// API Monitoring Configuration
// ═══════════════════════════════════════════════════════════════════════════════

export interface APIEndpointConfig {
    id: string;
    name: string;
    url: string;
    healthCheckEndpoint: string;
    healthCheckInterval: number; // ms
    timeout: number; // ms
    retryAttempts: number;
    retryDelay: number; // ms
    region: string;
    critical: boolean; // Se falhar, afeta operações críticas
    notifyOnFailure: boolean;
}

export interface HealthCheckConfig {
    enabled: boolean;
    interval: number; // ms
    timeout: number; // ms
    retries: number;
    alertThreshold: {
        responseTime: number; // ms
        errorRate: number; // percentual
        consecutiveFailures: number;
    };
}

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURAÇÕES PADRÃO
// ═══════════════════════════════════════════════════════════════════════════════

export const API_ENDPOINTS: APIEndpointConfig[] = [
    {
        id: 'binance',
        name: 'Binance API',
        url: 'https://api.binance.com',
        healthCheckEndpoint: '/api/v3/ping',
        healthCheckInterval: 30000,
        timeout: 5000,
        retryAttempts: 3,
        retryDelay: 1000,
        region: 'Global',
        critical: true,
        notifyOnFailure: true,
    },
    {
        id: 'ctrader',
        name: 'cTrader API',
        url: 'https://api.spotware.com',
        healthCheckEndpoint: '/api/v1/health',
        healthCheckInterval: 30000,
        timeout: 5000,
        retryAttempts: 3,
        retryDelay: 1000,
        region: 'Europa',
        critical: true,
        notifyOnFailure: true,
    },
    {
        id: 'pionex',
        name: 'Pionex API',
        url: 'https://api.pionex.com',
        healthCheckEndpoint: '/api/v1/system/status',
        healthCheckInterval: 45000,
        timeout: 5000,
        retryAttempts: 3,
        retryDelay: 1000,
        region: 'Ásia',
        critical: false,
        notifyOnFailure: false,
    },
];

export const HEALTH_CHECK_CONFIG: HealthCheckConfig = {
    enabled: true,
    interval: 30000, // 30 segundos
    timeout: 5000, // 5 segundos
    retries: 3,
    alertThreshold: {
        responseTime: 1000, // 1 segundo
        errorRate: 5, // 5%
        consecutiveFailures: 3,
    },
};

// ═══════════════════════════════════════════════════════════════════════════════
// SERVIÇO DE HEALTH CHECK
// ═══════════════════════════════════════════════════════════════════════════════

export class APIHealthCheckService {
    private abortControllers: Map<string, AbortController> = new Map();
    private listeners: Set<(status: any) => void> = new Set();

    /**
     * Realizar health check para um endpoint
     */
    async checkHealth(endpoint: APIEndpointConfig): Promise<{
        success: boolean;
        responseTime: number;
        statusCode: number;
        message: string;
        timestamp: Date;
    }> {
        const startTime = performance.now();
        const abortController = new AbortController();
        this.abortControllers.set(endpoint.id, abortController);

        try {
            const response = await fetch(endpoint.url + endpoint.healthCheckEndpoint, {
                method: 'GET',
                signal: abortController.signal,
                timeout: endpoint.timeout,
            });

            const responseTime = performance.now() - startTime;

            return {
                success: response.ok,
                responseTime: Math.round(responseTime),
                statusCode: response.status,
                message: response.statusText || 'OK',
                timestamp: new Date(),
            };
        } catch (error: any) {
            const responseTime = performance.now() - startTime;

            if (error.name === 'AbortError') {
                return {
                    success: false,
                    responseTime: Math.round(responseTime),
                    statusCode: 0,
                    message: 'Timeout',
                    timestamp: new Date(),
                };
            }

            return {
                success: false,
                responseTime: Math.round(responseTime),
                statusCode: 0,
                message: error.message || 'Erro de conexão',
                timestamp: new Date(),
            };
        } finally {
            this.abortControllers.delete(endpoint.id);
        }
    }

    /**
     * Realizar health check com retry automático
     */
    async checkHealthWithRetry(
        endpoint: APIEndpointConfig,
        attempt: number = 0
    ): Promise<{
        success: boolean;
        responseTime: number;
        statusCode: number;
        message: string;
        timestamp: Date;
        attempts: number;
    }> {
        const result = await this.checkHealth(endpoint);

        if (!result.success && attempt < endpoint.retryAttempts - 1) {
            await new Promise(resolve => setTimeout(resolve, endpoint.retryDelay));
            return this.checkHealthWithRetry(endpoint, attempt + 1);
        }

        return {
            ...result,
            attempts: attempt + 1,
        };
    }

    /**
     * Parar health check
     */
    stopHealthCheck(apiId: string) {
        const controller = this.abortControllers.get(apiId);
        if (controller) {
            controller.abort();
            this.abortControllers.delete(apiId);
        }
    }

    /**
     * Parar todos os health checks
     */
    stopAllHealthChecks() {
        this.abortControllers.forEach(controller => controller.abort());
        this.abortControllers.clear();
    }

    /**
     * Registrar listener para alterações
     */
    onStatusChange(callback: (status: any) => void) {
        this.listeners.add(callback);
        return () => this.listeners.delete(callback);
    }

    /**
     * Notificar listeners
     */
    private notifyListeners(status: any) {
        this.listeners.forEach(listener => listener(status));
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// ALERTAS E NOTIFICAÇÕES
// ═══════════════════════════════════════════════════════════════════════════════

export enum AlertLevel {
    INFO = 'info',
    WARNING = 'warning',
    ERROR = 'error',
    CRITICAL = 'critical',
}

export interface APIAlert {
    id: string;
    apiId: string;
    level: AlertLevel;
    title: string;
    message: string;
    timestamp: Date;
    resolved: boolean;
    actions?: {
        label: string;
        action: () => void;
    }[];
}

export class APIAlertManager {
    private alerts: Map<string, APIAlert> = new Map();
    private listeners: Set<(alert: APIAlert) => void> = new Set();

    createAlert(
        apiId: string,
        level: AlertLevel,
        title: string,
        message: string
    ): APIAlert {
        const alert: APIAlert = {
            id: `${apiId}-${Date.now()}`,
            apiId,
            level,
            title,
            message,
            timestamp: new Date(),
            resolved: false,
        };

        this.alerts.set(alert.id, alert);
        this.notifyListeners(alert);

        return alert;
    }

    resolveAlert(alertId: string) {
        const alert = this.alerts.get(alertId);
        if (alert) {
            alert.resolved = true;
            this.notifyListeners(alert);
        }
    }

    getActiveAlerts(): APIAlert[] {
        return Array.from(this.alerts.values()).filter(alert => !alert.resolved);
    }

    onAlertCreated(callback: (alert: APIAlert) => void) {
        this.listeners.add(callback);
        return () => this.listeners.delete(callback);
    }

    private notifyListeners(alert: APIAlert) {
        this.listeners.forEach(listener => listener(alert));
    }

    clearResolved() {
        Array.from(this.alerts.entries()).forEach(([id, alert]) => {
            if (alert.resolved) {
                this.alerts.delete(id);
            }
        });
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// CACHE DE REQUISIÇÕES
// ═══════════════════════════════════════════════════════════════════════════════

export interface CacheEntry<T> {
    data: T;
    timestamp: Date;
    ttl: number; // ms
}

export class APIResponseCache<T = any> {
    private cache: Map<string, CacheEntry<T>> = new Map();
    private cleanupInterval: NodeJS.Timeout | null = null;

    set(key: string, data: T, ttl: number = 60000) {
        this.cache.set(key, {
            data,
            timestamp: new Date(),
            ttl,
        });
    }

    get(key: string): T | null {
        const entry = this.cache.get(key);
        if (!entry) return null;

        const age = Date.now() - entry.timestamp.getTime();
        if (age > entry.ttl) {
            this.cache.delete(key);
            return null;
        }

        return entry.data;
    }

    has(key: string): boolean {
        return this.get(key) !== null;
    }

    clear() {
        this.cache.clear();
    }

    startCleanup(interval: number = 60000) {
        this.cleanupInterval = setInterval(() => {
            const now = Date.now();
            this.cache.forEach((entry, key) => {
                if (now - entry.timestamp.getTime() > entry.ttl) {
                    this.cache.delete(key);
                }
            });
        }, interval);
    }

    stopCleanup() {
        if (this.cleanupInterval) {
            clearInterval(this.cleanupInterval);
            this.cleanupInterval = null;
        }
    }

    getStats() {
        return {
            size: this.cache.size,
            entries: Array.from(this.cache.entries()).map(([key, entry]) => ({
                key,
                age: Date.now() - entry.timestamp.getTime(),
                ttl: entry.ttl,
            })),
        };
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SERVIÇO INTEGRADO
// ═══════════════════════════════════════════════════════════════════════════════

export class APIMonitoringService {
    private healthCheckService: APIHealthCheckService;
    private alertManager: APIAlertManager;
    private responseCache: APIResponseCache;
    private monitoringIntervals: Map<string, NodeJS.Timeout> = new Map();

    constructor() {
        this.healthCheckService = new APIHealthCheckService();
        this.alertManager = new APIAlertManager();
        this.responseCache = new APIResponseCache();
        this.responseCache.startCleanup();
    }

    /**
     * Iniciar monitoramento de uma API
     */
    startMonitoring(
        endpoint: APIEndpointConfig,
        onStatusChange?: (status: any) => void
    ) {
        if (this.monitoringIntervals.has(endpoint.id)) {
            return; // Já está monitorando
        }

        const checkInterval = setInterval(async () => {
            const result = await this.healthCheckService.checkHealthWithRetry(endpoint);

            // Verificar alertas
            if (!result.success && endpoint.critical) {
                this.alertManager.createAlert(
                    endpoint.id,
                    AlertLevel.CRITICAL,
                    `${endpoint.name} Indisponível`,
                    `A API não está respondendo. Última resposta: ${result.message}`
                );
            }

            if (result.responseTime > HEALTH_CHECK_CONFIG.alertThreshold.responseTime) {
                this.alertManager.createAlert(
                    endpoint.id,
                    AlertLevel.WARNING,
                    `${endpoint.name} Lento`,
                    `Tempo de resposta acima do normal: ${result.responseTime}ms`
                );
            }

            if (onStatusChange) {
                onStatusChange(result);
            }
        }, endpoint.healthCheckInterval);

        this.monitoringIntervals.set(endpoint.id, checkInterval);
    }

    /**
     * Parar monitoramento de uma API
     */
    stopMonitoring(apiId: string) {
        const interval = this.monitoringIntervals.get(apiId);
        if (interval) {
            clearInterval(interval);
            this.monitoringIntervals.delete(apiId);
        }
        this.healthCheckService.stopHealthCheck(apiId);
    }

    /**
     * Parar todos os monitoramentos
     */
    stopAllMonitoring() {
        this.monitoringIntervals.forEach(interval => clearInterval(interval));
        this.monitoringIntervals.clear();
        this.healthCheckService.stopAllHealthChecks();
    }

    /**
     * Obter alertas ativos
     */
    getActiveAlerts(): APIAlert[] {
        return this.alertManager.getActiveAlerts();
    }

    /**
     * Registrar listener de alertas
     */
    onAlert(callback: (alert: APIAlert) => void) {
        return this.alertManager.onAlertCreated(callback);
    }

    /**
     * Destruir serviço
     */
    destroy() {
        this.stopAllMonitoring();
        this.responseCache.stopCleanup();
        this.alertManager.clearResolved();
    }
}

// Exportar instância global (singleton)
export const apiMonitoringService = new APIMonitoringService();
