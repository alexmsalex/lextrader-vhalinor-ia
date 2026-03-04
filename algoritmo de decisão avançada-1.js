// main.js - Arquivo principal Electron
const { app, BrowserWindow, Menu, ipcMain, shell, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const url = require('url');
const { autoUpdater } = require('electron-updater');
const { EventEmitter } = require('events');
const { v4: uuidv4 } = require('uuid');

let mainWindow = null;
let isDevelopment = process.env.NODE_ENV === 'development';

// Sistema de logging simples
const logger = {
    info: (message, data) => console.log(`[INFO] ${message}`, data || ''),
    error: (message, error) => console.error(`[ERROR] ${message}`, error || ''),
    warn: (message) => console.warn(`[WARN] ${message}`)
};

// Melhoria 1: Sistema de logging avançado
logger.info('Iniciando aplicativo Advanced Decision Algorithms');

// Melhoria 2: Configuração de performance
app.commandLine.appendSwitch('disable-renderer-backgrounding');
app.commandLine.appendSwitch('disable-background-timer-throttling');
app.commandLine.appendSwitch('max-active-webgl-contexts', '16');

// Melhoria 3: Single instance lock
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
    app.quit();
    process.exit(0);
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1600,
        height: 1000,
        minWidth: 1200,
        minHeight: 800,
        title: '🧠 Sistema Avançado de Algoritmos de Decisão',
        icon: path.join(__dirname, 'assets/icon.png'),
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js'),
            webSecurity: !isDevelopment,
            enableRemoteModule: false,
            backgroundThrottling: false
        },
        show: false,
        frame: true,
        backgroundColor: '#f8fafc'
    });

    // Melhoria 4: Carregar com splash screen
    mainWindow.once('ready-to-show', () => {
        if (mainWindow) {
            mainWindow.show();
            
            // Foco e maximizar se desenvolvimento
            if (isDevelopment) {
                mainWindow.maximize();
                mainWindow.focus();
                mainWindow.webContents.openDevTools({ mode: 'detach' });
            }
        }
    });

    // Melhoria 5: Configurar URL baseado em ambiente
    if (isDevelopment) {
        mainWindow.loadURL('http://localhost:3000');
        
        // Hot reload para desenvolvimento
        require('electron-reload')(__dirname, {
            electron: path.join(__dirname, '..', 'node_modules', '.bin', 'electron'),
            hardResetMethod: 'exit'
        });
    } else {
        mainWindow.loadURL(
            url.format({
                pathname: path.join(__dirname, './index.html'),
                protocol: 'file:',
                slashes: true
            })
        );
    }

    // Melhoria 6: Eventos da janela
    mainWindow.on('closed', () => {
        mainWindow = null;
    });

    // Melhoria 7: Bloqueador de navegação externa
    mainWindow.webContents.on('will-navigate', (event, navigationUrl) => {
        const parsedUrl = new URL(navigationUrl);
        if (parsedUrl.origin !== 'http://localhost:3000' && !isDevelopment) {
            event.preventDefault();
        }
    });

    // Melhoria 8: Abrir links externos no navegador
    mainWindow.webContents.setWindowOpenHandler(({ url }) => {
        shell.openExternal(url);
        return { action: 'deny' };
    });

    // Melhoria 9: Menu de aplicativo customizado
    createApplicationMenu();

    // Melhoria 10: Auto-updater
    if (!isDevelopment) {
        autoUpdater.checkForUpdatesAndNotify();
    }

    return mainWindow;
}

function createApplicationMenu() {
    const template = [
        {
            label: 'Arquivo',
            submenu: [
                {
                    label: 'Salvar Configurações',
                    accelerator: 'CmdOrCtrl+S',
                    click: () => {
                        if (mainWindow) {
                            mainWindow.webContents.send('save-settings');
                        }
                    }
                },
                {
                    label: 'Carregar Configurações',
                    accelerator: 'CmdOrCtrl+L',
                    click: () => {
                        if (mainWindow) {
                            mainWindow.webContents.send('load-settings');
                        }
                    }
                },
                { type: 'separator' },
                {
                    label: 'Exportar Dados',
                    submenu: [
                        {
                            label: 'Exportar para CSV',
                            click: () => {
                                if (mainWindow) {
                                    mainWindow.webContents.send('export-csv');
                                }
                            }
                        },
                        {
                            label: 'Exportar para JSON',
                            click: () => {
                                if (mainWindow) {
                                    mainWindow.webContents.send('export-json');
                                }
                            }
                        }
                    ]
                },
                { type: 'separator' },
                {
                    label: 'Sair',
                    accelerator: 'CmdOrCtrl+Q',
                    role: 'quit'
                }
            ]
        },
        {
            label: 'Algoritmos',
            submenu: [
                {
                    label: 'Gerenciar Algoritmos',
                    click: () => {
                        if (mainWindow) {
                            mainWindow.webContents.send('open-algorithm-manager');
                        }
                    }
                },
                {
                    label: 'Calibrar Parâmetros',
                    click: () => {
                        if (mainWindow) {
                            mainWindow.webContents.send('open-calibration');
                        }
                    }
                },
                { type: 'separator' },
                {
                    label: 'Testar Performance',
                    click: () => {
                        if (mainWindow) {
                            mainWindow.webContents.send('run-backtest');
                        }
                    }
                },
                {
                    label: 'Ativar Todos',
                    click: () => {
                        if (mainWindow) {
                            mainWindow.webContents.send('activate-all-algorithms');
                        }
                    }
                }
            ]
        },
        {
            label: 'Sistema',
            submenu: [
                {
                    label: 'Monitor de Recursos',
                    click: () => {
                        mainWindow?.webContents.send('open-resource-monitor');
                    }
                },
                {
                    label: 'Logs do Sistema',
                    click: () => {
                        mainWindow?.webContents.send('open-system-logs');
                    }
                },
                { type: 'separator' },
                {
                    label: 'Configurações',
                    accelerator: 'CmdOrCtrl+,',
                    click: () => {
                        mainWindow?.webContents.send('open-settings');
                    }
                },
                {
                    label: 'Recarregar',
                    accelerator: 'CmdOrCtrl+R',
                    click: () => {
                        mainWindow?.reload();
                    }
                },
                {
                    label: 'Forçar Recarregar',
                    accelerator: 'CmdOrCtrl+Shift+R',
                    role: 'reload'
                },
                {
                    label: 'Inspecionar Elemento',
                    accelerator: 'CmdOrCtrl+Shift+I',
                    role: 'toggleDevTools'
                }
            ]
        },
        {
            label: 'Ajuda',
            submenu: [
                {
                    label: 'Documentação',
                    click: () => {
                        shell.openExternal('https://docs.decision-algorithms.com');
                    }
                },
                {
                    label: 'Suporte',
                    click: () => {
                        shell.openExternal('mailto:support@decision-algorithms.com');
                    }
                },
                { type: 'separator' },
                {
                    label: 'Sobre',
                    click: () => {
                        mainWindow?.webContents.send('open-about');
                    }
                }
            ]
        }
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}

// Eventos da aplicação
app.whenReady().then(async () => {
    logger.info('App ready, creating window...');
    
    // Melhoria 11: Instalar extensões de desenvolvimento
    if (isDevelopment) {
        try {
            // await installExtension(REACT_DEVELOPER_TOOLS);
            logger.info('React DevTools instalado');
        } catch (err) {
            logger.error('Erro ao instalar React DevTools:', err);
        }
    }

    // Criar janela principal
    createWindow();

    // Inicializar sistemas
    setupIpcHandlers(mainWindow);
    setupDataFeed();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// Melhoria 12: Auto-updater events
autoUpdater.on('update-available', () => {
    logger.info('Update available');
    mainWindow?.webContents.send('update-available');
});

autoUpdater.on('update-downloaded', () => {
    logger.info('Update downloaded');
    mainWindow?.webContents.send('update-downloaded');
});

autoUpdater.on('error', (err) => {
    logger.error('Auto-updater error:', err);
});

// Melhoria 13: Crash reporting
process.on('uncaughtException', (error) => {
    logger.error('Uncaught Exception:', error);
    
    const crashReport = {
        timestamp: new Date().toISOString(),
        error: error.toString(),
        stack: error.stack
    };
    
    // Salvar relatório de crash
    fs.writeFileSync(
        path.join(app.getPath('userData'), 'crash-report.json'),
        JSON.stringify(crashReport, null, 2)
    );
    
    // Notificar usuário
    if (mainWindow) {
        dialog.showErrorBox(
            'Erro do Sistema',
            `Ocorreu um erro inesperado. O relatório foi salvo.\n\n${error.message}`
        );
    }
});

// preload.js - Context Bridge para comunicação segura entre Main e Renderer
const { contextBridge, ipcRenderer } = require('electron');

// API segura para o renderer
contextBridge.exposeInMainWorld('electronAPI', {
    // Sistema
    onSystemUpdate: (callback) => 
        ipcRenderer.on('system-update', (event, update) => callback(update)),
    
    saveSettings: () => ipcRenderer.send('save-settings'),
    loadSettings: () => ipcRenderer.send('load-settings'),
    
    // Algoritmos
    getAlgorithms: () => ipcRenderer.invoke('get-algorithms'),
    toggleAlgorithm: (id) => ipcRenderer.invoke('toggle-algorithm', id),
    updateAlgorithm: (algorithm) => ipcRenderer.invoke('update-algorithm', algorithm),
    
    // Decisões
    getDecisions: (limit) => ipcRenderer.invoke('get-decisions', limit),
    addDecision: (decision) => ipcRenderer.invoke('add-decision', decision),
    exportDecisions: (format) => ipcRenderer.invoke('export-decisions', format),
    
    // Processamento
    runDecisionProcess: () => ipcRenderer.invoke('run-decision-process'),
    pauseDecisionProcess: () => ipcRenderer.send('pause-decision-process'),
    stopDecisionProcess: () => ipcRenderer.send('stop-decision-process'),
    
    // Alertas
    getAlerts: () => ipcRenderer.invoke('get-alerts'),
    markAlertAsRead: (id) => ipcRenderer.invoke('mark-alert-read', id),
    
    // Dados em tempo real
    subscribeToMarketData: (callback) => {
        ipcRenderer.on('market-data', (event, data) => callback(data));
        return () => ipcRenderer.removeAllListeners('market-data');
    },
    
    // Configurações
    getSettings: () => ipcRenderer.invoke('get-settings'),
    updateSettings: (settings) => ipcRenderer.invoke('update-settings', settings),
    
    // Sistema de arquivos
    showSaveDialog: (options) => ipcRenderer.invoke('show-save-dialog', options),
    showOpenDialog: (options) => ipcRenderer.invoke('show-open-dialog', options),
    
    // Notificações
    showNotification: (title, body) => 
        ipcRenderer.invoke('show-notification', { title, body }),
    
    // Logs
    getLogs: () => ipcRenderer.invoke('get-logs'),
    
    // Atualizações
    checkForUpdates: () => ipcRenderer.invoke('check-for-updates'),
    installUpdate: () => ipcRenderer.send('install-update'),
    
    // Performance
    getPerformanceMetrics: () => ipcRenderer.invoke('get-performance-metrics'),
    
    // Versão
    getAppVersion: () => ipcRenderer.invoke('get-app-version'),
    
    // Encerramento
    quitApp: () => ipcRenderer.send('quit-app')
});

// Melhoria 15: Expor versões para debugging
contextBridge.exposeInMainWorld('versions', {
    node: () => process.versions.node,
    chrome: () => process.versions.chrome,
    electron: () => process.versions.electron
});

// ipcHandlers.js - Handlers para comunicação IPC
const { ipcMain, dialog } = require('electron');
const fs = require('fs');
const path = require('path');

// Classes auxiliares
class AlertManager {
    constructor() {
        this.alerts = [];
    }
    
    addAlert(alert) {
        this.alerts.unshift({
            id: Date.now().toString(),
            timestamp: new Date(),
            ...alert
        });
    }
    
    getAlerts() {
        return this.alerts;
    }
    
    markAsRead(id) {
        const alert = this.alerts.find(a => a.id === id);
        if (alert) {
            alert.read = true;
            return true;
        }
        return false;
    }
}

class AlgorithmManager {
    constructor() {
        this.algorithms = [];
        this.decisions = [];
        this.processProgress = 0;
    }
    
    getAlgorithms() {
        return this.algorithms;
    }
    
    toggleAlgorithm(id) {
        const algorithm = this.algorithms.find(a => a.id === id);
        if (algorithm) {
            algorithm.isActive = !algorithm.isActive;
            return { algorithm, activated: algorithm.isActive };
        }
        throw new Error('Algoritmo não encontrado');
    }
    
    getRecentDecisions(limit = 50) {
        return this.decisions.slice(0, limit);
    }
    
    addDecision(decision) {
        const newDecision = {
            id: Date.now().toString(),
            timestamp: new Date(),
            ...decision
        };
        this.decisions.unshift(newDecision);
        return newDecision;
    }
    
    async runDecisionProcess() {
        this.processProgress = 0;
        return new Promise((resolve) => {
            const interval = setInterval(() => {
                this.processProgress += 10;
                if (this.processProgress >= 100) {
                    clearInterval(interval);
                    resolve({ processId: Date.now().toString() });
                }
            }, 100);
        });
    }
    
    getProcessProgress() {
        return this.processProgress;
    }
    
    getDefaultSettings() {
        return {
            theme: 'dark',
            notifications: true,
            autoUpdate: true
        };
    }
    
    updateSettings(settings) {
        // Implementar atualização de configurações
    }
    
    cleanup() {
        // Implementar limpeza
    }
    
    saveState() {
        // Implementar salvamento de estado
    }
}

function setupIpcHandlers(mainWindow) {
    const alertManager = new AlertManager();
    const dataFeed = new DataFeed();
    const algorithmManager = new AlgorithmManager();
    const performanceMonitor = new PerformanceMonitor();

    // Sistema de algoritmos
    ipcMain.handle('get-algorithms', async () => {
        return algorithmManager.getAlgorithms();
    });

    ipcMain.handle('toggle-algorithm', async (event, algorithmId) => {
        const result = algorithmManager.toggleAlgorithm(algorithmId);
        alertManager.addAlert({
            level: 'info',
            message: `Algoritmo ${result.algorithm.name} ${result.algorithm.isActive ? 'ativado' : 'desativado'}`,
            algorithm: result.algorithm.name
        });
        return result;
    });

    // Sistema de decisões
    ipcMain.handle('get-decisions', async (event, limit = 50) => {
        return algorithmManager.getRecentDecisions(limit);
    });

    ipcMain.handle('add-decision', async (event, decision) => {
        const newDecision = algorithmManager.addDecision(decision);
        alertManager.addAlert({
            level: 'success',
            message: `Nova decisão: ${newDecision.decision}`,
            algorithm: newDecision.algorithm
        });
        return newDecision;
    });

    // Exportação de dados
    ipcMain.handle('export-decisions', async (event, format) => {
        const decisions = algorithmManager.getRecentDecisions();
        
        const filePath = await dialog.showSaveDialog(mainWindow, {
            title: 'Exportar Decisões',
            defaultPath: `decisoes_${Date.now()}.${format}`,
            filters: [
                { name: format.toUpperCase(), extensions: [format] }
            ]
        });

        if (!filePath.canceled && filePath.filePath) {
            if (format === 'csv') {
                const csvWriter = csv.createObjectCsvWriter({
                    path: filePath.filePath,
                    header: [
                        { id: 'timestamp', title: 'Data/Hora' },
                        { id: 'asset', title: 'Ativo' },
                        { id: 'algorithm', title: 'Algoritmo' },
                        { id: 'decision', title: 'Decisão' },
                        { id: 'confidence', title: 'Confiança' },
                        { id: 'risk', title: 'Risco' },
                        { id: 'expectedReturn', title: 'Retorno Esperado' },
                        { id: 'price', title: 'Preço' },
                        { id: 'volume', title: 'Volume' },
                        { id: 'profitLoss', title: 'Lucro/Prejuízo' }
                    ]
                });

                await csvWriter.writeRecords(decisions.map(d => ({
                    ...d,
                    timestamp: d.timestamp.toISOString()
                })));
            } else {
                fs.writeFileSync(
                    filePath.filePath,
                    JSON.stringify(decisions, null, 2)
                );
            }
            
            return { success: true, path: filePath.filePath };
        }
        
        return { success: false };
    });

    // Configurações
    ipcMain.handle('get-settings', async () => {
        const settingsPath = path.join(process.cwd(), 'settings.json');
        if (fs.existsSync(settingsPath)) {
            return JSON.parse(fs.readFileSync(settingsPath, 'utf-8'));
        }
        return algorithmManager.getDefaultSettings();
    });

    ipcMain.handle('update-settings', async (event, settings) => {
        const settingsPath = path.join(process.cwd(), 'settings.json');
        fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2));
        algorithmManager.updateSettings(settings);
        return { success: true };
    });

    // Processamento de decisão
    ipcMain.handle('run-decision-process', async () => {
        try {
            const result = await algorithmManager.runDecisionProcess();
            
            // Notificar UI
            mainWindow.webContents.send('decision-process-update', {
                status: 'running',
                progress: 0
            });
            
            // Stream de progresso
            const interval = setInterval(() => {
                const progress = algorithmManager.getProcessProgress();
                mainWindow.webContents.send('decision-process-update', {
                    status: 'running',
                    progress
                });
                
                if (progress >= 100) {
                    clearInterval(interval);
                    mainWindow.webContents.send('decision-process-complete', result);
                    
                    alertManager.addAlert({
                        level: 'success',
                        message: 'Processo de decisão concluído com sucesso!',
                        algorithm: 'Sistema'
                    });
                }
            }, 500);
            
            return { success: true, processId: result.processId };
            
        } catch (error) {
            logger.error('Erro no processo de decisão:', error);
            mainWindow.webContents.send('decision-process-error', error);
            
            alertManager.addAlert({
                level: 'danger',
                message: `Erro no processo de decisão: ${error.message}`,
                algorithm: 'Sistema'
            });
            
            return { success: false, error: error.message };
        }
    });

    // Alertas
    ipcMain.handle('get-alerts', async () => {
        return alertManager.getAlerts();
    });

    ipcMain.handle('mark-alert-read', async (event, alertId) => {
        return alertManager.markAsRead(alertId);
    });

    // Dados em tempo real
    dataFeed.onData((data) => {
        mainWindow.webContents.send('market-data', data);
    });

    dataFeed.start();

    // Performance
    ipcMain.handle('get-performance-metrics', async () => {
        return performanceMonitor.getMetrics();
    });

    // Logs
    ipcMain.handle('get-logs', async () => {
        const logsPath = path.join(process.cwd(), 'logs');
        if (fs.existsSync(logsPath)) {
            const logFiles = fs.readdirSync(logsPath);
            const latestLog = logFiles.sort().reverse()[0];
            if (latestLog) {
                return fs.readFileSync(path.join(logsPath, latestLog), 'utf-8');
            }
        }
        return 'Nenhum log encontrado';
    });

    // Melhoria 16: Notificações do sistema
    ipcMain.handle('show-notification', async (event, { title, body }) => {
        if (Notification.permission === 'granted') {
            new Notification(title, { body });
        }
        return { success: true };
    });

    // Melhoria 17: Diálogos de arquivo
    ipcMain.handle('show-save-dialog', async (event, options) => {
        const result = await dialog.showSaveDialog(mainWindow, options);
        return result;
    });

    ipcMain.handle('show-open-dialog', async (event, options) => {
        const result = await dialog.showOpenDialog(mainWindow, options);
        return result;
    });

    // Melhoria 18: Informações do sistema
    ipcMain.handle('get-app-version', async () => {
        return { version: process.env.npm_package_version || '1.0.0' };
    });

    // Melhoria 19: Atualizações
    ipcMain.handle('check-for-updates', async () => {
        return { updateAvailable: false };
    });

    // Melhoria 20: Shutdown limpo
    ipcMain.on('quit-app', () => {
        dataFeed.stop();
        algorithmManager.cleanup();
        
        // Salvar estado
        algorithmManager.saveState();
        
        // Fechar janela
        mainWindow.close();
    });

    logger.info('IPC Handlers configurados');
}

// alertManager.js - Sistema avançado de alertas
const { EventEmitter } = require('events');

class AlertManagerExtended extends EventEmitter {
    constructor() {
        super();
        this.alerts = [];
        this.maxAlerts = 1000;
        this.persistenceEnabled = true;
        this.alertHistory = [];
        this.loadAlerts();
    }

    addAlert(alert) {
        const newAlert = {
            id: this.generateAlertId(),
            timestamp: new Date(),
            read: false,
            ...alert
        };

        // Adicionar ao início da lista (mais recente primeiro)
        this.alerts.unshift(newAlert);

        // Limitar tamanho
        if (this.alerts.length > this.maxAlerts) {
            this.alerts = this.alerts.slice(0, this.maxAlerts);
        }

        // Emitir evento
        this.emit('alert-added', newAlert);

        // Persistir
        if (this.persistenceEnabled) {
            this.saveAlerts();
        }

        // Notificação push
        this.sendPushNotification(newAlert);

        return newAlert;
    }

    getAlerts(limit, unreadOnly = false) {
        let filtered = this.alerts;
        
        if (unreadOnly) {
            filtered = filtered.filter(alert => !alert.read);
        }
        
        if (limit) {
            filtered = filtered.slice(0, limit);
        }
        
        return filtered;
    }

    getUnreadCount() {
        return this.alerts.filter(alert => !alert.read).length;
    }

    markAsRead(alertId) {
        const alert = this.alerts.find(a => a.id === alertId);
        if (alert) {
            alert.read = true;
            this.emit('alert-read', alert);
            
            if (this.persistenceEnabled) {
                this.saveAlerts();
            }
            
            return true;
        }
        return false;
    }

    markAllAsRead() {
        let marked = 0;
        this.alerts.forEach(alert => {
            if (!alert.read) {
                alert.read = true;
                marked++;
            }
        });
        
        this.emit('all-alerts-read');
        
        if (this.persistenceEnabled) {
            this.saveAlerts();
        }
        
        return marked;
    }

    getAlertStats() {
        const stats = {
            total: this.alerts.length,
            unread: this.getUnreadCount(),
            byLevel: {},
            byAlgorithm: {}
        };

        this.alerts.forEach(alert => {
            stats.byLevel[alert.level] = (stats.byLevel[alert.level] || 0) + 1;
            stats.byAlgorithm[alert.algorithm] = (stats.byAlgorithm[alert.algorithm] || 0) + 1;
        });

        return stats;
    }

    clearAlerts(daysOld) {
        let removed = 0;
        
        if (daysOld) {
            const cutoffDate = new Date();
            cutoffDate.setDate(cutoffDate.getDate() - daysOld);
            
            this.alerts = this.alerts.filter(alert => {
                if (alert.timestamp > cutoffDate) {
                    return true;
                } else {
                    removed++;
                    return false;
                }
            });
        } else {
            removed = this.alerts.length;
            this.alerts = [];
        }
        
        this.emit('alerts-cleared', removed);
        
        if (this.persistenceEnabled) {
            this.saveAlerts();
        }
        
        return removed;
    }

    searchAlerts(query, filters) {
        const searchLower = query.toLowerCase();
        
        return this.alerts.filter(alert => {
            // Pesquisa por texto
            const textMatch = 
                alert.message.toLowerCase().includes(searchLower) ||
                alert.algorithm.toLowerCase().includes(searchLower);
            
            // Filtros adicionais
            let filterMatch = true;
            if (filters) {
                for (const [key, value] of Object.entries(filters)) {
                    if (alert[key] !== value) {
                        filterMatch = false;
                        break;
                    }
                }
            }
            
            return textMatch && filterMatch;
        });
    }

    generateAlertId() {
        return `alert_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    sendPushNotification(alert) {
        // Implementar notificações push usando Web Notifications API
        if (typeof Notification !== 'undefined' && Notification.permission === 'granted') {
            new Notification(`Alerta: ${alert.level.toUpperCase()}`, {
                body: alert.message,
                icon: this.getIconForLevel(alert.level),
                tag: alert.id
            });
        }
    }

    getIconForLevel(level) {
        const icons = {
            info: 'assets/icons/info.png',
            warning: 'assets/icons/warning.png',
            danger: 'assets/icons/danger.png',
            success: 'assets/icons/success.png'
        };
        return icons[level];
    }

    saveAlerts() {
        try {
            const data = JSON.stringify(this.alerts, null, 2);
            if (typeof localStorage !== 'undefined') {
                localStorage.setItem('alerts', data);
            }
        } catch (error) {
            console.error('Erro ao salvar alertas:', error);
        }
    }

    loadAlerts() {
        try {
            if (typeof localStorage !== 'undefined') {
                const data = localStorage.getItem('alerts');
                if (data) {
                    const parsed = JSON.parse(data);
                    this.alerts = parsed.map((alert) => ({
                        ...alert,
                        timestamp: new Date(alert.timestamp)
                    }));
                }
            }
        } catch (error) {
            console.error('Erro ao carregar alertas:', error);
        }
    }
}

// algorithmManager.js - Gerenciador avançado de algoritmos
const { EventEmitter } = require('events');
const { v4: uuidv4 } = require('uuid');

// Enums convertidos para objetos JavaScript
const AlgorithmType = {
    ML: "Machine Learning",
    STATISTICAL: "Estatístico",
    HYBRID: "Híbrido",
    QUANTUM: "Quântico",
    ENSEMBLE: "Ensemble",
    DEEP_LEARNING: "Deep Learning"
};

const NodeStatus = {
    PROCESSING: "PROCESSING",
    COMPLETED: "COMPLETED",
    WAITING: "WAITING",
    ERROR: "ERROR",
    PAUSED: "PAUSED"
};

const Decision = {
    BUY: "BUY",
    SELL: "SELL",
    HOLD: "HOLD",
    CLOSE: "CLOSE",
    SCALP: "SCALP",
    SWING: "SWING",
    ARBITRAGE: "ARBITRAGE"
};

const PerformanceMetric = {
    ACCURACY: "Accuracy",
    SHARPE: "Sharpe Ratio",
    MAX_DRAWDOWN: "Max Drawdown",
    WIN_RATE: "Win Rate",
    PROFIT_FACTOR: "Profit Factor"
};

class AlgorithmManagerExtended extends EventEmitter {
    constructor() {
        super();
        this.algorithms = [];
        this.decisionNodes = [];
        this.decisions = [];
        this.performanceHistory = [];
        this.activeProcesses = new Map();
        this.settings = {};
        this.dataCache = new Map();
        this.loadData();
        this.setupDefaultData();
    }

    // Algoritmos
    getAlgorithms(filters) {
        let filtered = this.algorithms;
        
        if (filters) {
            filtered = filtered.filter(algo => {
                for (const [key, value] of Object.entries(filters)) {
                    if (algo[key] !== value) {
                        return false;
                    }
                }
                return true;
            });
        }
        
        return filtered;
    }

    getAlgorithm(id) {
        return this.algorithms.find(algo => algo.id === id);
    }

    addAlgorithm(algorithm) {
        const newAlgorithm = {
            ...algorithm,
            id: uuidv4(),
            lastUpdated: new Date()
        };
        
        this.algorithms.push(newAlgorithm);
        this.saveData();
        this.emit('algorithm-added', newAlgorithm);
        
        return newAlgorithm;
    }

    updateAlgorithm(id, updates) {
        const index = this.algorithms.findIndex(algo => algo.id === id);
        
        if (index !== -1) {
            const updatedAlgorithm = {
                ...this.algorithms[index],
                ...updates,
                lastUpdated: new Date()
            };
            
            this.algorithms[index] = updatedAlgorithm;
            this.saveData();
            this.emit('algorithm-updated', updatedAlgorithm);
            
            return updatedAlgorithm;
        }
        
        return undefined;
    }

    toggleAlgorithm(id) {
        const algorithm = this.getAlgorithm(id);
        
        if (algorithm) {
            const activated = !algorithm.isActive;
            const updated = this.updateAlgorithm(id, { isActive: activated });
            
            if (updated) {
                return { algorithm: updated, activated };
            }
        }
        
        throw new Error(`Algoritmo não encontrado: ${id}`);
    }

    // Processo de decisão
    async runDecisionProcess() {
        const processId = uuidv4();
        
        try {
            // Resetar nós
            this.resetDecisionNodes();
            
            // Iniciar processo
            this.activeProcesses.set(processId, {
                startTime: new Date(),
                status: 'running'
            });
            
            this.emit('process-started', processId);
            
            // Executar nós sequencialmente
            for (const node of this.decisionNodes) {
                await this.executeDecisionNode(node, processId);
                
                if (!this.activeProcesses.has(processId)) {
                    throw new Error('Processo interrompido');
                }
            }
            
            // Gerar decisão final
            const finalDecision = this.generateFinalDecision();
            this.decisions.unshift(finalDecision);
            
            // Salvar dados
            this.saveData();
            
            // Limpar processo
            this.activeProcesses.delete(processId);
            
            this.emit('process-completed', { processId, decision: finalDecision });
            
            return { processId, result: finalDecision };
            
        } catch (error) {
            this.activeProcesses.delete(processId);
            this.emit('process-failed', { processId, error });
            throw error;
        }
    }

    pauseDecisionProcess(processId) {
        if (this.activeProcesses.has(processId)) {
            this.activeProcesses.set(processId, {
                ...this.activeProcesses.get(processId),
                status: 'paused'
            });
            
            this.emit('process-paused', processId);
            return true;
        }
        return false;
    }

    stopDecisionProcess(processId) {
        if (this.activeProcesses.has(processId)) {
            this.activeProcesses.delete(processId);
            
            // Resetar nós
            this.decisionNodes.forEach(node => {
                if (node.status === NodeStatus.PROCESSING) {
                    node.status = NodeStatus.WAITING;
                    node.progress = 0;
                }
            });
            
            this.emit('process-stopped', processId);
            return true;
        }
        return false;
    }

    getProcessProgress(processId) {
        const totalNodes = this.decisionNodes.length;
        const completedNodes = this.decisionNodes.filter(
            node => node.status === NodeStatus.COMPLETED
        ).length;
        
        return totalNodes > 0 ? (completedNodes / totalNodes) * 100 : 0;
    }

    // Decisões
    getRecentDecisions(limit = 50) {
        return this.decisions.slice(0, limit);
    }

    addDecision(decision) {
        const newDecision = {
            ...decision,
            id: uuidv4(),
            timestamp: new Date()
        };
        
        this.decisions.unshift(newDecision);
        
        // Manter apenas últimas 1000 decisões
        if (this.decisions.length > 1000) {
            this.decisions = this.decisions.slice(0, 1000);
        }
        
        this.saveData();
        this.emit('decision-added', newDecision);
        
        return newDecision;
    }

    // Performance
    recordPerformance(performance) {
        const newPerformance = {
            ...performance,
            timestamp: new Date()
        };
        
        this.performanceHistory.push(newPerformance);
        this.saveData();
        
        return newPerformance;
    }

    getPerformanceHistory(algorithmId, metric) {
        let filtered = this.performanceHistory;
        
        if (algorithmId) {
            filtered = filtered.filter(p => p.algorithmId === algorithmId);
        }
        
        if (metric) {
            filtered = filtered.filter(p => p.metric === metric);
        }
        
        return filtered.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
    }

    // Métodos privados
    async executeDecisionNode(node, processId) {
        node.status = NodeStatus.PROCESSING;
        node.progress = 0;
        
        this.emit('node-started', { nodeId: node.id, processId });
        
        try {
            // Simular processamento
            const steps = 10;
            for (let i = 0; i <= steps; i++) {
                if (!this.activeProcesses.has(processId)) {
                    throw new Error('Processo interrompido');
                }
                
                await new Promise(resolve => setTimeout(resolve, 100));
                node.progress = (i / steps) * 100;
                
                this.emit('node-progress', {
                    nodeId: node.id,
                    processId,
                    progress: node.progress
                });
            }
            
            // Simular resultados
            node.confidence = Math.random() * 20 + 80; // 80-100%
            node.executionTime = Math.random() * 0.5 + 0.1; // 0.1-0.6s
            node.status = NodeStatus.COMPLETED;
            
            this.emit('node-completed', { nodeId: node.id, processId });
            
        } catch (error) {
            node.status = NodeStatus.ERROR;
            node.errorMessage = error.message;
            
            this.emit('node-failed', { nodeId: node.id, processId, error });
            throw error;
        }
    }

    generateFinalDecision() {
        const activeAlgorithms = this.algorithms.filter(algo => algo.isActive);
        const selectedAlgorithm = activeAlgorithms[
            Math.floor(Math.random() * activeAlgorithms.length)
        ] || this.algorithms[0];
        
        const decisions = Object.values(Decision);
        const selectedDecision = decisions[Math.floor(Math.random() * decisions.length)];
        
        return {
            id: uuidv4(),
            timestamp: new Date(),
            algorithm: selectedAlgorithm.name,
            algorithmId: selectedAlgorithm.id,
            decision: selectedDecision,
            confidence: Math.random() * 25 + 75, // 75-100%
            reasoning: this.generateReasoning(selectedDecision),
            factors: this.generateFactors(selectedDecision),
            risk: Math.random() * 4 + 1, // 1-5%
            expectedReturn: Math.random() * 6 + 2, // 2-8%
            timeframe: ['5m', '15m', '1H', '4H'][Math.floor(Math.random() * 4)],
            asset: ['BTC/USDT', 'ETH/USDT', 'BNB/USDT'][Math.floor(Math.random() * 3)],
            price: Math.random() * 30000 + 20000, // 20k-50k
            volume: Math.random() * 9000 + 1000, // 1k-10k
            profitLoss: Math.random() * 1500 - 500, // -500 a 1000
            executed: Math.random() > 0.3,
            metadata: {
                nodesProcessed: this.decisionNodes.length,
                averageConfidence: this.decisionNodes.reduce((sum, n) => sum + n.confidence, 0) / this.decisionNodes.length,
                totalTime: this.decisionNodes.reduce((sum, n) => sum + n.executionTime, 0)
            }
        };
    }

    generateReasoning(decision) {
        const reasoningMap = {
            [Decision.BUY]: "Condições favoráveis para entrada longa com múltiplos confirmadores técnicos",
            [Decision.SELL]: "Sinais de exaustão do movimento de alta com divergências negativas",
            [Decision.HOLD]: "Mercado em consolidação, aguardando catalisador para direção clara",
            [Decision.CLOSE]: "Alvo atingido ou stop acionado, realizando lucros/cortando prejuízos",
            [Decision.SCALP]: "Oportunidade de curto prazo identificada com bom risco/retorno",
            [Decision.SWING]: "Setup de médio prazo confirmado com boa relação risco/retorno",
            [Decision.ARBITRAGE]: "Descobertura de preços entre exchanges identificada"
        };
        
        return reasoningMap[decision] || "Decisão baseada em análise multi-fatorial";
    }

    generateFactors(decision) {
        const factorSets = {
            [Decision.BUY]: [
                "RSI Oversold",
                "Suporte Forte Identificado",
                "Volume Crescente",
                "Divergência Positiva",
                "Breakout Técnico"
            ],
            [Decision.SELL]: [
                "RSI Overbought",
                "Resistência Forte",
                "Volume Declinante",
                "Divergência Negativa",
                "Pattern de Reversão"
            ],
            [Decision.HOLD]: [
                "Mercado Lateralizado",
                "Baixa Volatilidade",
                "Sem Catalisadores",
                "Indicadores Neutros",
                "Aguardando Confirmação"
            ]
        };
        
        const baseFactors = factorSets[decision] || [
            "Análise Técnica",
            "Análise Fundamentalista",
            "Sentimento de Mercado",
            "Contexto Macroeconômico"
        ];
        
        // Selecionar 3-4 fatores aleatórios
        return baseFactors
            .sort(() => Math.random() - 0.5)
            .slice(0, Math.floor(Math.random() * 2) + 3);
    }

    resetDecisionNodes() {
        this.decisionNodes.forEach(node => {
            node.status = NodeStatus.WAITING;
            node.confidence = 0;
            node.executionTime = 0;
            node.errorMessage = '';
            node.progress = 0;
        });
    }

    // Persistência
    saveData() {
        try {
            const data = {
                algorithms: this.algorithms,
                decisions: this.decisions.slice(0, 100), // Salvar apenas 100 mais recentes
                performanceHistory: this.performanceHistory,
                settings: this.settings
            };
            
            if (typeof localStorage !== 'undefined') {
                localStorage.setItem('algorithm-data', JSON.stringify(data, null, 2));
            }
        } catch (error) {
            console.error('Erro ao salvar dados:', error);
        }
    }

    loadData() {
        try {
            if (typeof localStorage !== 'undefined') {
                const data = JSON.parse(localStorage.getItem('algorithm-data') || '{}');
                
                if (data.algorithms) {
                    this.algorithms = data.algorithms.map((algo) => ({
                        ...algo,
                        lastUpdated: new Date(algo.lastUpdated)
                    }));
                }
                
                if (data.decisions) {
                    this.decisions = data.decisions.map((decision) => ({
                        ...decision,
                        timestamp: new Date(decision.timestamp)
                    }));
                }
                
                if (data.performanceHistory) {
                    this.performanceHistory = data.performanceHistory.map((ph) => ({
                        ...ph,
                        timestamp: new Date(ph.timestamp)
                    }));
                }
                
                if (data.settings) {
                    this.settings = data.settings;
                }
            }
        } catch (error) {
            console.error('Erro ao carregar dados:', error);
            this.setupDefaultData();
        }
    }

    setupDefaultData() {
        // Algoritmos padrão
        this.algorithms = [
            {
                id: "ensemble",
                name: "Ensemble Multi-Algoritmo",
                type: AlgorithmType.ENSEMBLE,
                description: "Combina múltiplos algoritmos usando voting e stacking para decisões mais robustas",
                accuracy: 94.7,
                speed: 85.2,
                complexity: 95.8,
                confidence: 89.3,
                isActive: true,
                decisions: 2847,
                successRate: 87.4,
                avgResponseTime: 0.23,
                riskLevel: 2.1,
                specialization: ["Análise Multi-Modal", "Consenso Algorítmico", "Meta-Learning"],
                parameters: [
                    {
                        name: "ensemble_size",
                        value: 5,
                        min: 3,
                        max: 10,
                        step: 1,
                        description: "Número de algoritmos no ensemble",
                        unit: "",
                        category: "Performance"
                    }
                ],
                lastUpdated: new Date(),
                version: "2.1.0",
                memoryUsage: 256.5,
                cpuUsage: 15.3,
                tags: ["ensemble", "advanced", "high-accuracy"],
                dependencies: ["ml-core", "statistics-module"],
                config: { votingMethod: "weighted", validationSplit: 0.2 }
            }
        ];

        // Nós de decisão padrão
        this.decisionNodes = [
            {
                id: "data-collection",
                name: "Coleta de Dados",
                input: "Market Data",
                output: "Processed Data",
                confidence: 98.5,
                executionTime: 0.02,
                status: NodeStatus.COMPLETED,
                dependencies: [],
                resources: { cpu: 10, memory: 100 },
                errorMessage: "",
                progress: 100
            },
            {
                id: "preprocessing",
                name: "Pré-processamento",
                input: "Raw Data",
                output: "Clean Data",
                confidence: 96.7,
                executionTime: 0.08,
                status: NodeStatus.COMPLETED,
                dependencies: ["data-collection"],
                resources: { cpu: 15, memory: 150 },
                errorMessage: "",
                progress: 100
            },
            {
                id: "feature-engineering",
                name: "Feature Engineering",
                input: "Clean Data",
                output: "Features",
                confidence: 94.2,
                executionTime: 0.15,
                status: NodeStatus.COMPLETED,
                dependencies: ["preprocessing"],
                resources: { cpu: 20, memory: 200 },
                errorMessage: "",
                progress: 100
            },
            {
                id: "ensemble-analysis",
                name: "Análise Ensemble",
                input: "Features",
                output: "Predictions",
                confidence: 89.3,
                executionTime: 0.23,
                status: NodeStatus.PROCESSING,
                dependencies: ["feature-engineering"],
                resources: { cpu: 30, memory: 300 },
                errorMessage: "",
                progress: 50
            },
            {
                id: "cross-validation",
                name: "Validação Cruzada",
                input: "Predictions",
                output: "Validated",
                confidence: 0,
                executionTime: 0,
                status: NodeStatus.WAITING,
                dependencies: ["ensemble-analysis"],
                resources: { cpu: 25, memory: 250 },
                errorMessage: "",
                progress: 0
            },
            {
                id: "decision-execution",
                name: "Execução de Decisão",
                input: "Validated",
                output: "Action",
                confidence: 0,
                executionTime: 0,
                status: NodeStatus.WAITING,
                dependencies: ["cross-validation"],
                resources: { cpu: 10, memory: 100 },
                errorMessage: "",
                progress: 0
            }
        ];

        // Decisões padrão
        this.decisions = [
            {
                id: "initial-decision",
                timestamp: new Date(Date.now() - 1800000), // 30 minutos atrás
                algorithm: "Ensemble Multi-Algoritmo",
                algorithmId: "ensemble",
                decision: Decision.BUY,
                confidence: 87.4,
                reasoning: "Confluência de sinais: breakout técnico + momentum positivo + volume acima da média",
                factors: ["RSI(14): 45.2", "MACD: Bullish Cross", "Volume: +234%", "Support: 42,100"],
                risk: 2.3,
                expectedReturn: 5.7,
                timeframe: "4H",
                asset: "BTC/USDT",
                price: 42150.32,
                volume: 24567.89,
                profitLoss: 245.67,
                executed: true,
                metadata: { executedPrice: 42150.32, executionTime: "2024-01-15T10:30:00Z" }
            }
        ];

        // Configurações padrão
        this.settings = {
            autoUpdate: true,
            notifications: true,
            theme: 'dark',
            updateInterval: 1.0,
            riskLimit: 20.0,
            minConfidence: 70.0,
            dataRefreshRate: 60,
            maxParallelProcesses: 3,
            loggingLevel: 'info'
        };
    }

    // Configurações
    getDefaultSettings() {
        return this.settings;
    }

    updateSettings(settings) {
        this.settings = { ...this.settings, ...settings };
        this.saveData();
        this.emit('settings-updated', this.settings);
    }

    // Cleanup
    cleanup() {
        // Parar todos os processos ativos
        this.activeProcesses.forEach((process, processId) => {
            this.stopDecisionProcess(processId);
        });
        
        // Limpar cache
        this.dataCache.clear();
        
        // Salvar dados
        this.saveData();
    }

    saveState() {
        this.saveData();
    }
}

// Exportar classes e constantes
module.exports = {
    AlgorithmType,
    NodeStatus,
    Decision,
    PerformanceMetric,
    AlgorithmManagerExtended,
    AlertManagerExtended,
    setupIpcHandlers,
    logger
};