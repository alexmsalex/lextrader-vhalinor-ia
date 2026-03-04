import React, { useState, useEffect } from 'react';
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
} from '@mui/icons-material';

// Enums e tipos
enum BrokerStatus {
  CONNECTED = 'connected',
  DISCONNECTED = 'disconnected',
  CONNECTING = 'connecting',
  ERROR = 'error',
}

enum OrderType {
  BUY = 'buy',
  SELL = 'sell',
}

enum OrderMethod {
  MARKET = 'market',
  LIMIT = 'limit',
  STOP = 'stop',
}

interface Broker {
  id: string;
  name: string;
  url: string;
  status: BrokerStatus;
  region: string;
  commission: number;
  features: string[];
}

interface TradeOrder {
  symbol: string;
  type: OrderType;
  quantity: number;
  price: number | null;
  orderType: OrderMethod;
}

// Componente estilizado
const StyledCard = styled(Card)(({ theme }) => ({
  transition: 'transform 0.2s, box-shadow 0.2s',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.shadows[8],
  },
}));

const StatusChip = styled(Chip)<{ status: BrokerStatus }>(({ theme, status }) => {
  const colorMap = {
    [BrokerStatus.CONNECTED]: theme.palette.success.main,
    [BrokerStatus.CONNECTING]: theme.palette.warning.main,
    [BrokerStatus.ERROR]: theme.palette.error.main,
    [BrokerStatus.DISCONNECTED]: theme.palette.grey[500],
  };
  return {
    backgroundColor: colorMap[status],
    color: 'white',
    fontWeight: 'bold',
  };
});

// Componente principal
const BrokerIntegration: React.FC = () => {
  // Estados
  const [brokers, setBrokers] = useState<Broker[]>([
    {
      id: 'homebroker-pt',
      name: 'HomeBroker PT',
      url: 'https://www.homebroker.com/pt/invest',
      status: BrokerStatus.DISCONNECTED,
      region: 'Portugal',
      commission: 0.1,
      features: ['Ações', 'ETFs', 'Derivados', 'CFDs'],
    },
    {
      id: 'interactive-brokers',
      name: 'Interactive Brokers',
      url: 'https://www.interactivebrokers.com',
      status: BrokerStatus.CONNECTED,
      region: 'Global',
      commission: 0.05,
      features: ['Ações', 'Opções', 'Futuros', 'Forex', 'Criptos'],
    },
    {
      id: 'degiro',
      name: 'DEGIRO',
      url: 'https://www.degiro.pt',
      status: BrokerStatus.DISCONNECTED,
      region: 'Europa',
      commission: 0.04,
      features: ['Ações', 'ETFs', 'Obrigações', 'Opções'],
    },
  ]);

  const [selectedTab, setSelectedTab] = useState(0);
  const [connectionProgress, setConnectionProgress] = useState<Record<string, number>>({});
  const [tradeOrder, setTradeOrder] = useState<TradeOrder>({
    symbol: '',
    type: OrderType.BUY,
    quantity: 0,
    price: null,
    orderType: OrderMethod.MARKET,
  });

  const [accountBalance] = useState(25750.30);
  const [totalProfit] = useState(3247.89);
  const [activePositions] = useState(7);

  // Funções utilitárias
  const getStatusIcon = (status: BrokerStatus) => {
    switch (status) {
      case BrokerStatus.CONNECTED:
        return <CheckCircleIcon color="success" />;
      case BrokerStatus.CONNECTING:
        return <RefreshIcon color="warning" className="rotating" />;
      case BrokerStatus.ERROR:
        return <ErrorIcon color="error" />;
      case BrokerStatus.DISCONNECTED:
        return <PublicIcon color="disabled" />;
    }
  };

  const getStatusText = (status: BrokerStatus) => {
    const textMap = {
      [BrokerStatus.CONNECTED]: 'Conectado',
      [BrokerStatus.CONNECTING]: 'Conectando',
      [BrokerStatus.ERROR]: 'Erro',
      [BrokerStatus.DISCONNECTED]: 'Desconectado',
    };
    return textMap[status];
  };

  // Função de conexão
  const connectToBroker = async (brokerId: string) => {
    setBrokers(prev =>
      prev.map(broker =>
        broker.id === brokerId
          ? { ...broker, status: BrokerStatus.CONNECTING }
          : broker
      )
    );

    // Simular progresso de conexão
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 200));
      setConnectionProgress(prev => ({ ...prev, [brokerId]: i }));
    }

    // Simular resultado
    setTimeout(() => {
      setBrokers(prev =>
        prev.map(broker =>
          broker.id === brokerId
            ? {
                ...broker,
                status:
                  brokerId === 'homebroker-pt'
                    ? BrokerStatus.ERROR
                    : BrokerStatus.CONNECTED,
              }
            : broker
        )
      );
      setConnectionProgress(prev => ({ ...prev, [brokerId]: 0 }));
    }, 2100);
  };

  // Função para executar ordem
  const executeOrder = () => {
    if (!tradeOrder.symbol || tradeOrder.quantity <= 0) {
      alert('Preencha todos os campos obrigatórios');
      return;
    }

    // Aqui você implementaria a lógica real de execução
    alert('Ordem executada com sucesso!');
    
    // Reset do formulário
    setTradeOrder({
      symbol: '',
      type: OrderType.BUY,
      quantity: 0,
      price: null,
      orderType: OrderMethod.MARKET,
    });
  };

  // Manipuladores de eventos
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

  const handleTradeOrderChange = (
    field: keyof TradeOrder,
    value: string | number | OrderType | OrderMethod | null
  ) => {
    setTradeOrder(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  // Renderizar componente BrokerCard
  const renderBrokerCard = (broker: Broker) => (
    <StyledCard key={broker.id} sx={{ mb: 3 }}>
      <CardHeader
        avatar={getStatusIcon(broker.status)}
        title={
          <Box display="flex" alignItems="center" justifyContent="space-between">
            <Box>
              <Typography variant="h6">{broker.name}</Typography>
              <Typography variant="body2" color="text.secondary">
                {broker.region}
              </Typography>
            </Box>
            <StatusChip
              label={getStatusText(broker.status)}
              status={broker.status}
              size="small"
            />
          </Box>
        }
        action={
          <Button
            variant={
              broker.status === BrokerStatus.CONNECTED ? 'outlined' : 'contained'
            }
            color="primary"
            onClick={() => connectToBroker(broker.id)}
            disabled={broker.status === BrokerStatus.CONNECTING}
            startIcon={
              broker.status === BrokerStatus.CONNECTED ? (
                <RefreshIcon />
              ) : null
            }
          >
            {broker.status === BrokerStatus.CONNECTED
              ? 'Reconectar'
              : 'Conectar'}
          </Button>
        }
      />
      <CardContent>
        {broker.status === BrokerStatus.CONNECTING && (
          <Box sx={{ mb: 2 }}>
            <LinearProgress
              variant="determinate"
              value={connectionProgress[broker.id] || 0}
              sx={{ mb: 1 }}
            />
            <Typography variant="caption" color="text.secondary">
              Conectando... {connectionProgress[broker.id] || 0}%
            </Typography>
          </Box>
        )}

        {broker.status === BrokerStatus.ERROR && broker.id === 'homebroker-pt' && (
          <Alert
            severity="warning"
            icon={<WarningIcon />}
            sx={{ mb: 2 }}
          >
            Acesso restrito por região. Use VPN para Portugal.
          </Alert>
        )}

        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Recursos disponíveis:
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {broker.features.map((feature, index) => (
              <Chip
                key={index}
                label={feature}
                size="small"
                variant="outlined"
              />
            ))}
          </Box>
        </Box>

        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="body2" color="text.secondary">
            Comissão: {broker.commission}%
          </Typography>
          <IconButton
            size="small"
            href={broker.url}
            target="_blank"
            title="Visitar site"
          >
            <LanguageIcon fontSize="small" />
          </IconButton>
        </Box>
      </CardContent>
    </StyledCard>
  );

  // Renderizar formulário de trading
  const renderTradingForm = () => (
    <Card sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
        <SwapHorizIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
        Nova Ordem
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Símbolo"
            placeholder="Ex: AAPL, PETR4"
            value={tradeOrder.symbol}
            onChange={(e) => handleTradeOrderChange('symbol', e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <BarChartIcon />
                </InputAdornment>
              ),
            }}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Tipo</InputLabel>
            <Select
              value={tradeOrder.type}
              label="Tipo"
              onChange={(e) =>
                handleTradeOrderChange('type', e.target.value as OrderType)
              }
            >
              <MenuItem value={OrderType.BUY}>Comprar</MenuItem>
              <MenuItem value={OrderType.SELL}>Vender</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Quantidade"
            type="number"
            value={tradeOrder.quantity || ''}
            onChange={(e) =>
              handleTradeOrderChange('quantity', parseInt(e.target.value) || 0)
            }
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Tipo de Ordem</InputLabel>
            <Select
              value={tradeOrder.orderType}
              label="Tipo de Ordem"
              onChange={(e) =>
                handleTradeOrderChange('orderType', e.target.value as OrderMethod)
              }
            >
              <MenuItem value={OrderMethod.MARKET}>Mercado</MenuItem>
              <MenuItem value={OrderMethod.LIMIT}>Limitada</MenuItem>
              <MenuItem value={OrderMethod.STOP}>Stop</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        {tradeOrder.orderType !== OrderMethod.MARKET && (
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Preço"
              type="number"
              value={tradeOrder.price || ''}
              onChange={(e) =>
                handleTradeOrderChange(
                  'price',
                  e.target.value ? parseFloat(e.target.value) : null
                )
              }
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <AttachMoneyIcon />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
        )}

        <Grid item xs={12}>
          <Button
            variant="contained"
            color="primary"
            size="large"
            fullWidth
            onClick={executeOrder}
            startIcon={<BoltIcon />}
            sx={{ py: 2, fontSize: '1.1rem' }}
          >
            Executar Ordem
          </Button>
        </Grid>
      </Grid>
    </Card>
  );

  // Renderizar informações da conta
  const renderAccountInfo = () => (
    <Grid container spacing={3}>
      <Grid item xs={12} md={4}>
        <Card sx={{ p: 3, textAlign: 'center' }}>
          <AccountBalanceIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
          <Typography variant="h4" gutterBottom>
            €{accountBalance.toLocaleString('pt-PT', {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Saldo Total
          </Typography>
        </Card>
      </Grid>

      <Grid item xs={12} md={4}>
        <Card sx={{ p: 3, textAlign: 'center' }}>
          <TrendingUpIcon sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
          <Typography variant="h4" gutterBottom color="success.main">
            €{totalProfit.toLocaleString('pt-PT', {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Lucro Total
          </Typography>
        </Card>
      </Grid>

      <Grid item xs={12} md={4}>
        <Card sx={{ p: 3, textAlign: 'center' }}>
          <BarChartIcon sx={{ fontSize: 48, color: 'warning.main', mb: 2 }} />
          <Typography variant="h4" gutterBottom color="warning.main">
            {activePositions}
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Posições Ativas
          </Typography>
        </Card>
      </Grid>
    </Grid>
  );

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Cabeçalho */}
      <Box sx={{ mb: 4 }}>
        <Box display="flex" alignItems="center" sx={{ mb: 1 }}>
          <PublicIcon sx={{ fontSize: 32, mr: 2, color: 'primary.main' }} />
          <Box>
            <Typography variant="h4" component="h1" fontWeight="bold">
              Integração com Corretoras
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Conecte-se às principais corretoras para operações em tempo real
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
          <Tab icon={<AccountBalanceIcon />} label="Corretoras" />
          <Tab icon={<SwapHorizIcon />} label="Trading" />
          <Tab icon={<TrendingUpIcon />} label="Conta" />
        </Tabs>
      </Paper>

      {/* Conteúdo das Tabs */}
      {selectedTab === 0 && (
        <Box>
          <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
            🏢 Corretoras Disponíveis
          </Typography>
          {brokers.map(renderBrokerCard)}
        </Box>
      )}

      {selectedTab === 1 && renderTradingForm()}

      {selectedTab === 2 && (
        <Box>
          <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
            💰 Resumo da Conta
          </Typography>
          {renderAccountInfo()}
        </Box>
      )}

      {/* Estilos CSS para animação */}
      <style>{`
        @keyframes rotate {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }
        .rotating {
          animation: rotate 1s linear infinite;
        }
      `}</style>
    </Container>
  );
};

export default BrokerIntegration;