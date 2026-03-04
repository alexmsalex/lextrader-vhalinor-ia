import React, { useState, useEffect, useCallback } from 'react';
import {
    Box,
    Button,
    Card,
    CardContent,
    CardHeader,
    CircularProgress,
    Chip,
    Container,
    Grid,
    IconButton,
    LinearProgress,
    Paper,
    Tab,
    Tabs,
    TextField,
    Typography,
    Alert,
    Divider,
    InputAdornment,
    MenuItem,
    Select,
    FormControl,
    InputLabel,
    SelectChangeEvent,
    styled,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Tooltip,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    List,
    ListItem,
    ListItemText,
    ListItemIcon,
} from '@mui/material';
import {
    CheckCircle as CheckCircleIcon,
    Error as ErrorIcon,
    Refresh as RefreshIcon,
    Public as PublicIcon,
    AccountBalance as AccountBalanceIcon,
    TrendingUp as TrendingUpIcon,
    SwapHoriz as SwapHorizIcon,
    Bolt as BoltIcon,
    Warning as WarningIcon,
    Language as LanguageIcon,
    AttachMoney as AttachMoneyIcon,
    BarChart as BarChartIcon,
    Speed as SpeedIcon,
    Visibility as VisibilityIcon,
    MoreVert as MoreVertIcon,
    Assessment as AssessmentIcon,
    Timeline as TimelineIcon,
    Cloud as CloudIcon,
    WifiOff as WifiOffIcon,
    AccessTime as AccessTimeIcon,
    CheckCircleOutline as CheckCircleOutlineIcon,
} from '@mui/icons-material';

// ═══════════════════════════════════════════════════════════════════════════════
// TIPOS E INTERFACES
// ═══════════════════════════════════════════════════════════════════════════════

enum BrokerStatus {
    CONNECTED = 'connected',
    DISCONNECTED = 'disconnected',
    CONNECTING = 'connecting',
    ERROR = 'error',
    DEGRADED = 'degraded',
}

enum APIHealthStatus {
    HEALTHY = 'healthy',
    DEGRADED = 'degraded',
    UNHEALTHY = 'unhealthy',
    UNKNOWN = 'unknown',
}

interface APIMetrics {
    uptime: number; // percentual
    responseTime: number; // ms
    requestsPerMinute: number;
    errorRate: number; // percentual
    lastHealthCheck: Date;
    statusCode: number;
    message: string;
}

interface APIHealth {
    id: string;
    name: string;
    url: string;
    status: APIHealthStatus;
    metrics: APIMetrics;
    region: string;
    lastResponse: Date | null;
    averageResponseTime: number;
    totalRequests: number;
    failedRequests: number;
    consecutiveFailures: number;
}

interface RequestLog {
    id: string;
    apiId: string;
    timestamp: Date;
    method: string;
    endpoint: string;
    statusCode: number;
    responseTime: number;
    success: boolean;
    errorMessage?: string;
}

interface PerformanceData {
    timestamp: Date;
    responseTime: number;
    statusCode: number;
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPONENTES ESTILIZADOS
// ═══════════════════════════════════════════════════════════════════════════════

const StyledCard = styled(Card)(({ theme }) => ({
    transition: 'transform 0.2s, box-shadow 0.2s',
    '&:hover': {
        transform: 'translateY(-4px)',
        boxShadow: theme.shadows[8],
    },
}));

const HealthChip = styled(Chip)<{ status: APIHealthStatus }>(({ theme, status }) => {
    const colorMap = {
        [APIHealthStatus.HEALTHY]: theme.palette.success.main,
        [APIHealthStatus.DEGRADED]: theme.palette.warning.main,
        [APIHealthStatus.UNHEALTHY]: theme.palette.error.main,
        [APIHealthStatus.UNKNOWN]: theme.palette.grey[500],
    };

    const iconMap = {
        [APIHealthStatus.HEALTHY]: <CheckCircleIcon />,
        [APIHealthStatus.DEGRADED]: <WarningIcon />,
        [APIHealthStatus.UNHEALTHY]: <ErrorIcon />,
        [APIHealthStatus.UNKNOWN]: <CloudIcon />,
    };

    return {
        backgroundColor: colorMap[status],
        color: 'white',
        fontWeight: 'bold',
        '& .MuiChip-icon': {
            color: 'white !important',
        },
    };
});

const MetricBox = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(2),
    textAlign: 'center',
    background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
    color: 'white',
    borderRadius: theme.spacing(1),
}));

// ═══════════════════════════════════════════════════════════════════════════════
// COMPONENTE PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

const APIMonitoringPanel: React.FC = () => {
    // ─ Estados ─
    const [apis, setApis] = useState<APIHealth[]>([
        {
            id: 'binance',
            name: 'Binance API',
            url: 'https://api.binance.com',
            status: APIHealthStatus.HEALTHY,
            region: 'Global',
            metrics: {
                uptime: 99.98,
                responseTime: 245,
                requestsPerMinute: 1250,
                errorRate: 0.02,
                lastHealthCheck: new Date(),
                statusCode: 200,
                message: 'OK',
            },
            lastResponse: new Date(),
            averageResponseTime: 245,
            totalRequests: 50000,
            failedRequests: 2,
            consecutiveFailures: 0,
        },
        {
            id: 'ctrader',
            name: 'cTrader API',
            url: 'https://api.spotware.com',
            status: APIHealthStatus.HEALTHY,
            region: 'Europa',
            metrics: {
                uptime: 99.95,
                responseTime: 320,
                requestsPerMinute: 850,
                errorRate: 0.05,
                lastHealthCheck: new Date(),
                statusCode: 200,
                message: 'OK',
            },
            lastResponse: new Date(),
            averageResponseTime: 320,
            totalRequests: 35000,
            failedRequests: 5,
            consecutiveFailures: 0,
        },
        {
            id: 'pionex',
            name: 'Pionex API',
            url: 'https://api.pionex.com',
            status: APIHealthStatus.DEGRADED,
            region: 'Ásia',
            metrics: {
                uptime: 98.5,
                responseTime: 850,
                requestsPerMinute: 450,
                errorRate: 1.5,
                lastHealthCheck: new Date(),
                statusCode: 200,
                message: 'Slow Response',
            },
            lastResponse: new Date(),
            averageResponseTime: 850,
            totalRequests: 20000,
            failedRequests: 45,
            consecutiveFailures: 1,
        },
    ]);

    const [requestLogs, setRequestLogs] = useState<RequestLog[]>([
        {
            id: '1',
            apiId: 'binance',
            timestamp: new Date(Date.now() - 60000),
            method: 'GET',
            endpoint: '/api/v3/ticker/price',
            statusCode: 200,
            responseTime: 235,
            success: true,
        },
        {
            id: '2',
            apiId: 'binance',
            timestamp: new Date(Date.now() - 45000),
            method: 'GET',
            endpoint: '/api/v3/account',
            statusCode: 200,
            responseTime: 250,
            success: true,
        },
        {
            id: '3',
            apiId: 'pionex',
            timestamp: new Date(Date.now() - 30000),
            method: 'POST',
            endpoint: '/api/v1/orders',
            statusCode: 200,
            responseTime: 1250,
            success: true,
        },
        {
            id: '4',
            apiId: 'ctrader',
            timestamp: new Date(Date.now() - 15000),
            method: 'GET',
            endpoint: '/api/v1/trading',
            statusCode: 500,
            responseTime: 5000,
            success: false,
            errorMessage: 'Timeout',
        },
    ]);

    const [selectedTab, setSelectedTab] = useState(0);
    const [isRefreshing, setIsRefreshing] = useState(false);
    const [selectedAPIDetails, setSelectedAPIDetails] = useState<string | null>(null);
    const [detailsDialogOpen, setDetailsDialogOpen] = useState(false);
    const [autoRefresh, setAutoRefresh] = useState(true);
    const [refreshInterval, setRefreshInterval] = useState(30000); // 30 segundos

    // ─ Funções Utilitárias ─
    const getHealthIcon = (status: APIHealthStatus) => {
        switch (status) {
            case APIHealthStatus.HEALTHY:
                return <CheckCircleIcon color="success" />;
            case APIHealthStatus.DEGRADED:
                return <WarningIcon color="warning" />;
            case APIHealthStatus.UNHEALTHY:
                return <ErrorIcon color="error" />;
            case APIHealthStatus.UNKNOWN:
                return <CloudIcon color="disabled" />;
        }
    };

    const getHealthText = (status: APIHealthStatus) => {
        const textMap = {
            [APIHealthStatus.HEALTHY]: 'Saudável',
            [APIHealthStatus.DEGRADED]: 'Degradado',
            [APIHealthStatus.UNHEALTHY]: 'Indisponível',
            [APIHealthStatus.UNKNOWN]: 'Desconhecido',
        };
        return textMap[status];
    };

    const getResponseTimeColor = (responseTime: number) => {
        if (responseTime < 300) return '#4caf50'; // Verde - Rápido
        if (responseTime < 1000) return '#ff9800'; // Laranja - Aceitável
        return '#f44336'; // Vermelho - Lento
    };

    const getUptimeColor = (uptime: number) => {
        if (uptime >= 99.5) return '#4caf50'; // Verde
        if (uptime >= 99) return '#ff9800'; // Laranja
        return '#f44336'; // Vermelho
    };

    // ─ Funções de API ─
    const performHealthCheck = async (apiId: string) => {
        setIsRefreshing(true);
        try {
            // Simular health check
            await new Promise(resolve => setTimeout(resolve, 1500));

            setApis(prevApis =>
                prevApis.map(api =>
                    api.id === apiId
                        ? {
                            ...api,
                            status: Math.random() > 0.1 ? APIHealthStatus.HEALTHY : APIHealthStatus.DEGRADED,
                            metrics: {
                                ...api.metrics,
                                responseTime: Math.random() * 500 + 200,
                                lastHealthCheck: new Date(),
                            },
                            lastResponse: new Date(),
                        }
                        : api
                )
            );

            // Adicionar log
            setRequestLogs(prev => [
                {
                    id: Date.now().toString(),
                    apiId,
                    timestamp: new Date(),
                    method: 'GET',
                    endpoint: '/health',
                    statusCode: 200,
                    responseTime: Math.random() * 500 + 200,
                    success: true,
                },
                ...prev.slice(0, 19),
            ]);
        } finally {
            setIsRefreshing(false);
        }
    };

    const performAllHealthChecks = async () => {
        setIsRefreshing(true);
        try {
            for (const api of apis) {
                await performHealthCheck(api.id);
                await new Promise(resolve => setTimeout(resolve, 300));
            }
        } finally {
            setIsRefreshing(false);
        }
    };

    const getAPIStats = (apiId: string) => {
        const api = apis.find(a => a.id === apiId);
        if (!api) return null;

        const apiLogs = requestLogs.filter(log => log.apiId === apiId);
        const successCount = apiLogs.filter(log => log.success).length;
        const totalResponseTime = apiLogs.reduce((sum, log) => sum + log.responseTime, 0);

        return {
            totalRequests: apiLogs.length,
            successRequests: successCount,
            failedRequests: apiLogs.length - successCount,
            averageResponseTime: apiLogs.length > 0 ? totalResponseTime / apiLogs.length : 0,
            lastRequest: apiLogs[0]?.timestamp || null,
        };
    };

    // ─ Auto-refresh ─
    useEffect(() => {
        if (!autoRefresh) return;

        const interval = setInterval(() => {
            performAllHealthChecks();
        }, refreshInterval);

        return () => clearInterval(interval);
    }, [autoRefresh, refreshInterval]);

    // ─ Manipuladores de Eventos ─
    const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
        setSelectedTab(newValue);
    };

    const handleOpenDetails = (apiId: string) => {
        setSelectedAPIDetails(apiId);
        setDetailsDialogOpen(true);
    };

    const handleCloseDetails = () => {
        setDetailsDialogOpen(false);
        setSelectedAPIDetails(null);
    };

    // ─ Renderizadores ─
    const renderAPICard = (api: APIHealth) => (
        <StyledCard key={api.id} sx={{ mb: 2 }}>
            <CardHeader
                avatar={getHealthIcon(api.status)}
                title={
                    <Box display="flex" alignItems="center" justifyContent="space-between" width="100%">
                        <Box>
                            <Typography variant="h6">{api.name}</Typography>
                            <Typography variant="caption" color="text.secondary">
                                {api.url}
                            </Typography>
                        </Box>
                        <HealthChip
                            icon={getHealthIcon(api.status)}
                            label={getHealthText(api.status)}
                            status={api.status}
                            size="small"
                        />
                    </Box>
                }
                action={
                    <Box>
                        <Tooltip title="Verificar saúde">
                            <IconButton
                                size="small"
                                onClick={() => performHealthCheck(api.id)}
                                disabled={isRefreshing}
                            >
                                <RefreshIcon />
                            </IconButton>
                        </Tooltip>
                        <Tooltip title="Detalhes">
                            <IconButton
                                size="small"
                                onClick={() => handleOpenDetails(api.id)}
                            >
                                <VisibilityIcon />
                            </IconButton>
                        </Tooltip>
                    </Box>
                }
            />
            <CardContent>
                <Grid container spacing={2} sx={{ mb: 2 }}>
                    {/* Tempo de Resposta */}
                    <Grid item xs={12} sm={6} md={3}>
                        <Box sx={{ textAlign: 'center' }}>
                            <Box
                                sx={{
                                    fontSize: '2rem',
                                    fontWeight: 'bold',
                                    color: getResponseTimeColor(api.metrics.responseTime),
                                    mb: 1,
                                }}
                            >
                                <SpeedIcon sx={{ mr: 0.5, verticalAlign: 'middle' }} />
                                {api.metrics.responseTime.toFixed(0)}ms
                            </Box>
                            <Typography variant="caption" color="text.secondary">
                                Tempo de Resposta
                            </Typography>
                        </Box>
                    </Grid>

                    {/* Uptime */}
                    <Grid item xs={12} sm={6} md={3}>
                        <Box sx={{ textAlign: 'center' }}>
                            <Box
                                sx={{
                                    fontSize: '2rem',
                                    fontWeight: 'bold',
                                    color: getUptimeColor(api.metrics.uptime),
                                    mb: 1,
                                }}
                            >
                                {api.metrics.uptime.toFixed(2)}%
                            </Box>
                            <Typography variant="caption" color="text.secondary">
                                Uptime
                            </Typography>
                        </Box>
                    </Grid>

                    {/* Taxa de Erro */}
                    <Grid item xs={12} sm={6} md={3}>
                        <Box sx={{ textAlign: 'center' }}>
                            <Box
                                sx={{
                                    fontSize: '2rem',
                                    fontWeight: 'bold',
                                    color: api.metrics.errorRate > 1 ? '#f44336' : '#4caf50',
                                    mb: 1,
                                }}
                            >
                                {api.metrics.errorRate.toFixed(2)}%
                            </Box>
                            <Typography variant="caption" color="text.secondary">
                                Taxa de Erro
                            </Typography>
                        </Box>
                    </Grid>

                    {/* Requisições por Minuto */}
                    <Grid item xs={12} sm={6} md={3}>
                        <Box sx={{ textAlign: 'center' }}>
                            <Box sx={{ fontSize: '2rem', fontWeight: 'bold', mb: 1 }}>
                                {api.metrics.requestsPerMinute}
                            </Box>
                            <Typography variant="caption" color="text.secondary">
                                Req/Minuto
                            </Typography>
                        </Box>
                    </Grid>
                </Grid>

                <Divider sx={{ my: 2 }} />

                {/* Informações Adicionais */}
                <Grid container spacing={1}>
                    <Grid item xs={12} sm={6}>
                        <Typography variant="body2" color="text.secondary">
                            <AccessTimeIcon sx={{ fontSize: '1rem', mr: 0.5, verticalAlign: 'middle' }} />
                            Última verificação: {api.metrics.lastHealthCheck.toLocaleTimeString('pt-PT')}
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <Typography variant="body2" color="text.secondary">
                            <CloudIcon sx={{ fontSize: '1rem', mr: 0.5, verticalAlign: 'middle' }} />
                            Região: {api.region}
                        </Typography>
                    </Grid>
                    <Grid item xs={12}>
                        <Typography variant="body2" color="text.secondary">
                            Status Code: <Chip label={api.metrics.statusCode} size="small" />
                            Mensagem: {api.metrics.message}
                        </Typography>
                    </Grid>
                </Grid>
            </CardContent>
        </StyledCard>
    );

    const renderHealthOverview = () => (
        <Box>
            <Box sx={{ mb: 3, display: 'flex', gap: 1 }}>
                <Button
                    variant="contained"
                    startIcon={<RefreshIcon />}
                    onClick={performAllHealthChecks}
                    disabled={isRefreshing}
                >
                    {isRefreshing ? 'Verificando...' : 'Verificar Tudo'}
                </Button>
                <FormControl sx={{ minWidth: 150 }}>
                    <InputLabel>Auto-refresh</InputLabel>
                    <Select
                        value={autoRefresh ? refreshInterval : 0}
                        label="Auto-refresh"
                        onChange={(e) => {
                            const value = e.target.value as number;
                            setAutoRefresh(value > 0);
                            if (value > 0) setRefreshInterval(value);
                        }}
                    >
                        <MenuItem value={0}>Desativado</MenuItem>
                        <MenuItem value={10000}>10 segundos</MenuItem>
                        <MenuItem value={30000}>30 segundos</MenuItem>
                        <MenuItem value={60000}>1 minuto</MenuItem>
                    </Select>
                </FormControl>
            </Box>

            {apis.map(renderAPICard)}
        </Box>
    );

    const renderRequestLogs = () => (
        <TableContainer component={Paper}>
            <Table>
                <TableHead sx={{ backgroundColor: '#f5f5f5' }}>
                    <TableRow>
                        <TableCell sx={{ fontWeight: 'bold' }}>API</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Hora</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Método</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Endpoint</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Status</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Tempo (ms)</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Resultado</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {requestLogs.slice(0, 20).map(log => {
                        const api = apis.find(a => a.id === log.apiId);
                        return (
                            <TableRow key={log.id}>
                                <TableCell>
                                    <Chip label={api?.name || 'Desconhecido'} size="small" />
                                </TableCell>
                                <TableCell>
                                    <Typography variant="caption">
                                        {log.timestamp.toLocaleTimeString('pt-PT')}
                                    </Typography>
                                </TableCell>
                                <TableCell>
                                    <Chip
                                        label={log.method}
                                        size="small"
                                        color={log.method === 'GET' ? 'primary' : 'secondary'}
                                        variant="outlined"
                                    />
                                </TableCell>
                                <TableCell>
                                    <Typography variant="caption" sx={{ wordBreak: 'break-word' }}>
                                        {log.endpoint}
                                    </Typography>
                                </TableCell>
                                <TableCell>
                                    <Chip
                                        label={log.statusCode}
                                        size="small"
                                        color={log.statusCode < 400 ? 'success' : 'error'}
                                        variant="filled"
                                    />
                                </TableCell>
                                <TableCell>
                                    <Box
                                        sx={{
                                            color: getResponseTimeColor(log.responseTime),
                                            fontWeight: 'bold',
                                        }}
                                    >
                                        {log.responseTime.toFixed(0)}
                                    </Box>
                                </TableCell>
                                <TableCell>
                                    {log.success ? (
                                        <CheckCircleOutlineIcon sx={{ color: 'success.main' }} />
                                    ) : (
                                        <Tooltip title={log.errorMessage}>
                                            <ErrorIcon sx={{ color: 'error.main' }} />
                                        </Tooltip>
                                    )}
                                </TableCell>
                            </TableRow>
                        );
                    })}
                </TableBody>
            </Table>
        </TableContainer>
    );

    const renderPerformanceMetrics = () => {
        const healthyApis = apis.filter(a => a.status === APIHealthStatus.HEALTHY).length;
        const degradedApis = apis.filter(a => a.status === APIHealthStatus.DEGRADED).length;
        const unhealthyApis = apis.filter(a => a.status === APIHealthStatus.UNHEALTHY).length;

        const totalRequests = requestLogs.length;
        const successfulRequests = requestLogs.filter(l => l.success).length;
        const failedRequests = totalRequests - successfulRequests;
        const avgResponseTime = requestLogs.length > 0
            ? requestLogs.reduce((sum, log) => sum + log.responseTime, 0) / requestLogs.length
            : 0;

        return (
            <Grid container spacing={3}>
                {/* Status Geral */}
                <Grid item xs={12} sm={6} md={3}>
                    <MetricBox>
                        <CheckCircleIcon sx={{ fontSize: 40, mb: 1 }} />
                        <Typography variant="h4">{healthyApis}</Typography>
                        <Typography variant="body2">APIs Saudáveis</Typography>
                    </MetricBox>
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                    <MetricBox sx={{ background: `linear-gradient(135deg, #ff9800 0%, #f57c00 100%)` }}>
                        <WarningIcon sx={{ fontSize: 40, mb: 1 }} />
                        <Typography variant="h4">{degradedApis}</Typography>
                        <Typography variant="body2">APIs Degradadas</Typography>
                    </MetricBox>
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                    <MetricBox sx={{ background: `linear-gradient(135deg, #f44336 0%, #d32f2f 100%)` }}>
                        <ErrorIcon sx={{ fontSize: 40, mb: 1 }} />
                        <Typography variant="h4">{unhealthyApis}</Typography>
                        <Typography variant="body2">APIs Indisponíveis</Typography>
                    </MetricBox>
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                    <MetricBox sx={{ background: `linear-gradient(135deg, #2196f3 0%, #1976d2 100%)` }}>
                        <BarChartIcon sx={{ fontSize: 40, mb: 1 }} />
                        <Typography variant="h4">{totalRequests}</Typography>
                        <Typography variant="body2">Total de Requisições</Typography>
                    </MetricBox>
                </Grid>

                {/* Métricas Detalhadas */}
                <Grid item xs={12} md={6}>
                    <Card sx={{ p: 3 }}>
                        <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
                            📊 Taxa de Sucesso
                        </Typography>
                        <Box sx={{ mb: 2 }}>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                <Typography variant="body2">Sucesso</Typography>
                                <Typography variant="body2" color="success.main" sx={{ fontWeight: 'bold' }}>
                                    {successfulRequests} ({((successfulRequests / totalRequests) * 100).toFixed(1)}%)
                                </Typography>
                            </Box>
                            <LinearProgress
                                variant="determinate"
                                value={(successfulRequests / totalRequests) * 100}
                                sx={{ height: 8, borderRadius: 4 }}
                            />
                        </Box>

                        <Box>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                <Typography variant="body2">Falhas</Typography>
                                <Typography variant="body2" color="error.main" sx={{ fontWeight: 'bold' }}>
                                    {failedRequests} ({((failedRequests / totalRequests) * 100).toFixed(1)}%)
                                </Typography>
                            </Box>
                            <LinearProgress
                                variant="determinate"
                                value={(failedRequests / totalRequests) * 100}
                                color="error"
                                sx={{ height: 8, borderRadius: 4 }}
                            />
                        </Box>
                    </Card>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Card sx={{ p: 3 }}>
                        <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
                            ⚡ Tempo de Resposta Médio
                        </Typography>
                        <Box sx={{ textAlign: 'center' }}>
                            <Box
                                sx={{
                                    fontSize: '3rem',
                                    fontWeight: 'bold',
                                    color: getResponseTimeColor(avgResponseTime),
                                    mb: 2,
                                }}
                            >
                                {avgResponseTime.toFixed(0)}ms
                            </Box>
                            <Typography variant="body2" color="text.secondary">
                                Média de todas as requisições
                            </Typography>
                        </Box>
                    </Card>
                </Grid>
            </Grid>
        );
    };

    const selectedAPI = apis.find(a => a.id === selectedAPIDetails);

    return (
        <Container maxWidth="lg" sx={{ py: 4 }}>
            {/* Cabeçalho */}
            <Box sx={{ mb: 4 }}>
                <Box display="flex" alignItems="center" sx={{ mb: 1 }}>
                    <CloudIcon sx={{ fontSize: 32, mr: 2, color: 'primary.main' }} />
                    <Box>
                        <Typography variant="h4" component="h1" fontWeight="bold">
                            Painel de Monitoramento de APIs
                        </Typography>
                        <Typography variant="subtitle1" color="text.secondary">
                            Monitore a saúde, desempenho e disponibilidade de suas APIs em tempo real
                        </Typography>
                    </Box>
                </Box>
                <Divider />
            </Box>

            {/* Tabs */}
            <Paper sx={{ mb: 3 }}>
                <Tabs
                    value={selectedTab}
                    onChange={handleTabChange}
                    variant="fullWidth"
                    sx={{ borderBottom: 1, borderColor: 'divider' }}
                >
                    <Tab icon={<CloudIcon />} label="APIs" />
                    <Tab icon={<TimelineIcon />} label="Logs" />
                    <Tab icon={<AssessmentIcon />} label="Métricas" />
                </Tabs>
            </Paper>

            {/* Conteúdo */}
            {selectedTab === 0 && renderHealthOverview()}
            {selectedTab === 1 && renderRequestLogs()}
            {selectedTab === 2 && renderPerformanceMetrics()}

            {/* Dialog de Detalhes */}
            <Dialog open={detailsDialogOpen} onClose={handleCloseDetails} maxWidth="sm" fullWidth>
                <DialogTitle sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <CloudIcon />
                    Detalhes da API: {selectedAPI?.name}
                </DialogTitle>
                <DialogContent>
                    {selectedAPI && (
                        <Box sx={{ pt: 2 }}>
                            <List>
                                <ListItem>
                                    <ListItemIcon>
                                        <CloudIcon />
                                    </ListItemIcon>
                                    <ListItemText
                                        primary="URL"
                                        secondary={selectedAPI.url}
                                    />
                                </ListItem>

                                <ListItem>
                                    <ListItemIcon>
                                        {getHealthIcon(selectedAPI.status)}
                                    </ListItemIcon>
                                    <ListItemText
                                        primary="Status"
                                        secondary={getHealthText(selectedAPI.status)}
                                    />
                                </ListItem>

                                <ListItem>
                                    <ListItemIcon>
                                        <SpeedIcon />
                                    </ListItemIcon>
                                    <ListItemText
                                        primary="Tempo de Resposta Médio"
                                        secondary={`${selectedAPI.averageResponseTime.toFixed(0)}ms`}
                                    />
                                </ListItem>

                                <ListItem>
                                    <ListItemIcon>
                                        <BarChartIcon />
                                    </ListItemIcon>
                                    <ListItemText
                                        primary="Total de Requisições"
                                        secondary={selectedAPI.totalRequests}
                                    />
                                </ListItem>

                                <ListItem>
                                    <ListItemIcon>
                                        <ErrorIcon />
                                    </ListItemIcon>
                                    <ListItemText
                                        primary="Requisições Falhadas"
                                        secondary={selectedAPI.failedRequests}
                                    />
                                </ListItem>

                                <ListItem>
                                    <ListItemIcon>
                                        <AccessTimeIcon />
                                    </ListItemIcon>
                                    <ListItemText
                                        primary="Última Resposta"
                                        secondary={selectedAPI.lastResponse?.toLocaleString('pt-PT') || 'N/A'}
                                    />
                                </ListItem>

                                <ListItem>
                                    <ListItemIcon>
                                        <WarningIcon />
                                    </ListItemIcon>
                                    <ListItemText
                                        primary="Falhas Consecutivas"
                                        secondary={selectedAPI.consecutiveFailures}
                                    />
                                </ListItem>
                            </List>

                            <Divider sx={{ my: 2 }} />

                            <Typography variant="h6" gutterBottom>
                                Últimas Requisições
                            </Typography>
                            <List dense>
                                {requestLogs
                                    .filter(log => log.apiId === selectedAPI.id)
                                    .slice(0, 5)
                                    .map(log => (
                                        <ListItem key={log.id}>
                                            <ListItemIcon>
                                                {log.success ? (
                                                    <CheckCircleOutlineIcon sx={{ color: 'success.main' }} />
                                                ) : (
                                                    <ErrorIcon sx={{ color: 'error.main' }} />
                                                )}
                                            </ListItemIcon>
                                            <ListItemText
                                                primary={`${log.method} ${log.endpoint}`}
                                                secondary={`${log.statusCode} - ${log.responseTime.toFixed(0)}ms`}
                                            />
                                        </ListItem>
                                    ))}
                            </List>
                        </Box>
                    )}
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDetails}>Fechar</Button>
                    <Button
                        variant="contained"
                        onClick={() => {
                            if (selectedAPI) performHealthCheck(selectedAPI.id);
                            handleCloseDetails();
                        }}
                    >
                        Verificar Agora
                    </Button>
                </DialogActions>
            </Dialog>
        </Container>
    );
};

export default APIMonitoringPanel;
