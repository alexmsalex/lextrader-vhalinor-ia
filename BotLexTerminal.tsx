
import React, { useState, useEffect, useCallback, useMemo } from "react";
import {
  Box,
  Typography,
  Paper,
  Grid, // Fix: changed Grid2 to Grid
  Button,
  LinearProgress,
  alpha,
  styled,
  keyframes
} from "@mui/material";
import {
  Bot,
  Zap,
  ShieldCheck,
  Wallet,
  Lock,
  Play,
  Pause,
  Activity,
  Terminal as TerminalIcon,
  AlertTriangle,
  TrendingUp,
  Cpu,
  Network,
  Database
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { botlex } from "../services/botlex-engine";
import { AccountType, BotState, LogEntry } from '../types';

// Animations
const pulse = keyframes`
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
`;

const glow = keyframes`
  0%, 100% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.3); }
  50% { box-shadow: 0 0 40px rgba(99, 102, 241, 0.6); }
`;

// Styled Components
const StyledPaper = styled(Paper)(({ theme }) => ({
  background: 'linear-gradient(145deg, #0f172a 0%, #1e293b 100%)',
  border: `1px solid ${alpha('#334155', 0.3)}`,
  backdropFilter: 'blur(10px)',
  '&:hover': {
    borderColor: alpha('#6366f1', 0.5),
  }
}));

const StatusBadge = styled('div')<{ $active: boolean }>(({ $active }) => ({
  padding: '4px 12px',
  borderRadius: '20px',
  fontSize: '10px',
  fontWeight: 900,
  letterSpacing: '2px',
  textTransform: 'uppercase',
  background: $active 
    ? 'linear-gradient(90deg, #10b981 0%, #059669 100%)'
    : 'linear-gradient(90deg, #6366f1 0%, #4f46e5 100%)',
  animation: $active ? `${pulse} 2s infinite` : 'none'
}));

const LogEntryItem = styled(motion.div)({
  fontFamily: '"JetBrains Mono", monospace',
  fontSize: '11px',
  lineHeight: '1.6',
  padding: '4px 0',
  borderBottom: '1px solid rgba(255,255,255,0.05)',
  '&:last-child': {
    borderBottom: 'none'
  }
});

// Custom hooks
const useBotState = (pollInterval = 1000) => {
  const [state, setState] = useState<BotState>(botlex.getState());
  const [performance, setPerformance] = useState({ fps: 60, memory: 0 });

  useEffect(() => {
    let animationFrameId: number;
    let lastUpdate = Date.now();
    let frameCount = 0;

    const updatePerformance = () => {
      frameCount++;
      const now = Date.now();
      if (now - lastUpdate >= 1000) {
        setPerformance(prev => ({
          fps: frameCount,
          memory: performance.memory
        }));
        frameCount = 0;
        lastUpdate = now;
      }
      animationFrameId = requestAnimationFrame(updatePerformance);
    };

    animationFrameId = requestAnimationFrame(updatePerformance);

    // Poll bot state
    const intervalId = setInterval(() => {
      setState(botlex.getState());
    }, pollInterval);

    return () => {
      clearInterval(intervalId);
      cancelAnimationFrame(animationFrameId);
    };
  }, [pollInterval]);

  return { state, performance };
};

// Memoized components
const AccountSwitcher = React.memo(({ 
  activeAccount, 
  onAccountChange 
}: { 
  activeAccount: AccountType;
  onAccountChange: (account: AccountType) => void;
}) => (
  <Box sx={{ 
    display: 'flex', 
    gap: 1,
    p: 0.5,
    bgcolor: alpha('#0f172a', 0.8),
    borderRadius: 3,
    border: `1px solid ${alpha('#334155', 0.5)}`
  }}>
    <Button
      variant={activeAccount === AccountType.DEMO ? 'contained' : 'text'}
      onClick={() => onAccountChange(AccountType.DEMO)}
      sx={{
        minWidth: 80,
        fontSize: '10px',
        fontWeight: 900,
        borderRadius: 2,
        bgcolor: activeAccount === AccountType.DEMO 
          ? 'linear-gradient(90deg, #6366f1 0%, #4f46e5 100%)' 
          : 'transparent',
        color: activeAccount === AccountType.DEMO ? 'white' : '#94a3b8',
        '&:hover': {
          bgcolor: alpha('#6366f1', 0.1)
        }
      }}
    >
      DEMO
    </Button>
    <Button
      variant={activeAccount === AccountType.REAL ? 'contained' : 'text'}
      onClick={() => onAccountChange(AccountType.REAL)}
      sx={{
        minWidth: 80,
        fontSize: '10px',
        fontWeight: 900,
        borderRadius: 2,
        bgcolor: activeAccount === AccountType.REAL
          ? 'linear-gradient(90deg, #ef4444 0%, #dc2626 100%)'
          : 'transparent',
        color: activeAccount === AccountType.REAL ? 'white' : '#94a3b8',
        '&:hover': {
          bgcolor: alpha('#ef4444', 0.1)
        }
      }}
    >
      REAL
    </Button>
  </Box>
));

const TradePosition = React.memo(({ trade }: { trade: BotState['activeTrade'] }) => {
  if (!trade) return null;

  return (
    <Box sx={{ mt: 3 }}>
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between',
        mb: 2,
        p: 2,
        bgcolor: alpha('#10b981', 0.05),
        borderRadius: 2,
        border: `1px solid ${alpha('#10b981', 0.2)}`
      }}>
        <Box>
          <Typography variant="caption" sx={{ color: '#94a3b8', fontWeight: 700, display: 'block' }}>
            {trade.symbol}
          </Typography>
          <Typography variant="h6" sx={{ color: 'white', fontWeight: 900, fontFamily: 'monospace' }}>
            ${trade.currentPrice.toFixed(2)}
          </Typography>
        </Box>
        <Box sx={{ textAlign: 'right' }}>
          <Typography variant="caption" sx={{ 
            color: trade.pnl >= 0 ? '#10b981' : '#ef4444',
            fontWeight: 900,
            display: 'block'
          }}>
            {trade.pnl >= 0 ? '+' : ''}{trade.pnl.toFixed(2)} ({trade.pnlPercent.toFixed(2)}%)
          </Typography>
          <Typography variant="caption" sx={{ color: '#94a3b8', fontSize: '10px' }}>
            Entry: ${trade.entryPrice}
          </Typography>
        </Box>
      </Box>
      
      <Box sx={{ mt: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
          <Typography variant="caption" sx={{ color: '#94a3b8', fontWeight: 700 }}>
            Position Progress
          </Typography>
          <Typography variant="caption" sx={{ color: '#10b981', fontWeight: 900 }}>
            {trade.progress}%
          </Typography>
        </Box>
        <LinearProgress 
          variant="determinate" 
          value={trade.progress}
          sx={{
            height: 6,
            borderRadius: 3,
            bgcolor: alpha('#1e293b', 0.5),
            '& .MuiLinearProgress-bar': {
              background: 'linear-gradient(90deg, #10b981 0%, #34d399 100%)',
              borderRadius: 3
            }
          }}
        />
      </Box>
    </Box>
  );
});

export const BotLexTerminal: React.FC<{ nexusSnapshot: any }> = ({ nexusSnapshot }) => {
  const { state, performance } = useBotState(1000);
  const [autoScroll, setAutoScroll] = useState(true);
  
  const logsContainerRef = React.useRef<HTMLDivElement>(null);
  
  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    if (autoScroll && logsContainerRef.current) {
      logsContainerRef.current.scrollTop = logsContainerRef.current.scrollHeight;
    }
  }, [state.logs, autoScroll]);
  
  const handleToggle = useCallback(() => {
    botlex.toggle(!state.isRunning);
  }, [state.isRunning]);
  
  const handleAccountChange = useCallback((account: AccountType) => {
    botlex.setAccount(account);
  }, []);
  
  const metrics = useMemo(() => ({
    dailyGains: state.securityFund.dailyGains,
    weeklyGains: state.securityFund.dailyGains * 7,
    winRate: state.metrics.winRate,
    totalTrades: state.metrics.totalTrades
  }), [state.securityFund.dailyGains, state.metrics]);
  
  const formattedLogs = useMemo(() => 
    state.logs.slice(-100).map((log, index) => ({
      id: `${Date.now()}-${index}`,
      ...log,
      level: log.message.includes('ERROR') ? 'error' : 
             log.message.includes('WARN') ? 'warning' : 
             log.message.includes('INFO') ? 'info' : 'debug'
    }))
  , [state.logs]);

  return (
    <Box sx={{ 
      p: { xs: 2, md: 4 },
      bgcolor: '#020617',
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      gap: 4,
      overflow: 'hidden'
    }}>
      {/* Header */}
      <Box sx={{
        display: 'flex',
        flexDirection: { xs: 'column', md: 'row' },
        gap: 3,
        alignItems: { xs: 'stretch', md: 'center' },
        justifyContent: 'space-between',
        pb: 4,
        borderBottom: `1px solid ${alpha('#334155', 0.3)}`
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
          <Box sx={{
            p: 2,
            borderRadius: 3,
            background: state.isRunning 
              ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
              : 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
            animation: `${glow} 2s infinite`,
            boxShadow: state.isRunning 
              ? '0 0 40px rgba(16, 185, 129, 0.4)' 
              : '0 0 40px rgba(99, 102, 241, 0.4)'
          }}>
            <Bot size={32} className="text-white" />
          </Box>
          <Box>
            <Typography variant="h4" sx={{ 
              fontWeight: 900, 
              color: 'white', 
              letterSpacing: -0.5,
              fontSize: { xs: '1.5rem', md: '2rem' }
            }}>
              BOTLEX <Box component="span" sx={{ color: '#6366f1' }}>AGI</Box>
            </Typography>
            <StatusBadge $active={state.isRunning}>
              {state.isRunning ? 'SYSTEM ACTIVE' : 'STANDBY MODE'}
            </StatusBadge>
          </Box>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 3, alignItems: 'center' }}>
          <AccountSwitcher 
            activeAccount={state.activeAccount}
            onAccountChange={handleAccountChange}
          />
          
          <Button
            onClick={handleToggle}
            variant="contained"
            sx={{
              px: 4,
              py: 1.5,
              borderRadius: 3,
              fontWeight: 900,
              fontSize: '11px',
              letterSpacing: '2px',
              textTransform: 'uppercase',
              background: state.isRunning
                ? 'linear-gradient(90deg, #ef4444 0%, #dc2626 100%)'
                : 'linear-gradient(90deg, #10b981 0%, #059669 100%)',
              '&:hover': {
                transform: 'translateY(-2px)',
                boxShadow: state.isRunning
                  ? '0 10px 30px rgba(239, 68, 68, 0.3)'
                  : '0 10px 30px rgba(16, 185, 129, 0.3)'
              },
              transition: 'all 0.3s ease'
            }}
          >
            {state.isRunning ? (
              <>
                <Pause size={14} style={{ marginRight: 8 }} />
                STOP BOT
              </>
            ) : (
              <>
                <Play size={14} style={{ marginRight: 8 }} />
                START BOT
              </>
            )}
          </Button>
        </Box>
      </Box>
      
      {/* Main Content */}
      <Grid container spacing={3} sx={{ flex: 1, overflow: 'hidden' }}>
        {/* Left Panel */}
        {/* Fix: use item xs/md instead of size prop for Grid v1 */}
        <Grid item xs={12} md={4}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3, height: '100%' }}>
            {/* Balance Card */}
            <StyledPaper sx={{ p: 3, flex: 1 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
                <Box>
                  <Typography variant="caption" sx={{ 
                    color: '#94a3b8', 
                    fontWeight: 700, 
                    letterSpacing: '1px',
                    display: 'block',
                    mb: 1
                  }}>
                    NEURAL BALANCE
                  </Typography>
                  <Typography variant="h3" sx={{ 
                    color: 'white', 
                    fontWeight: 900,
                    fontFamily: 'monospace',
                    background: 'linear-gradient(90deg, #fff 0%, #94a3b8 100%)',
                    backgroundClip: 'text',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent'
                  }}>
                    ${state.balance.toLocaleString(undefined, { 
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2 
                    })}
                  </Typography>
                </Box>
                <Wallet size={24} className="text-indigo-400" />
              </Box>
              
              <Box sx={{ display: 'flex', gap: 3, mb: 3 }}>
                <Box sx={{ flex: 1 }}>
                  <Typography variant="caption" sx={{ color: '#94a3b8', display: 'block', mb: 0.5 }}>
                    Daily
                  </Typography>
                  <Typography variant="h6" sx={{ color: '#10b981', fontWeight: 900 }}>
                    +${metrics.dailyGains.toFixed(2)}
                  </Typography>
                </Box>
                <Box sx={{ flex: 1 }}>
                  <Typography variant="caption" sx={{ color: '#94a3b8', display: 'block', mb: 0.5 }}>
                    Weekly
                  </Typography>
                  <Typography variant="h6" sx={{ color: '#6366f1', fontWeight: 900 }}>
                    +${metrics.weeklyGains.toFixed(2)}
                  </Typography>
                </Box>
              </Box>
              
              <Box sx={{ 
                display: 'flex', 
                justifyContent: 'space-between',
                alignItems: 'center',
                p: 2,
                bgcolor: alpha('#1e293b', 0.3),
                borderRadius: 2
              }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Cpu size={12} className="text-indigo-400" />
                  <Typography variant="caption" sx={{ color: '#94a3b8', fontSize: '10px' }}>
                    Win Rate
                  </Typography>
                </Box>
                <Typography variant="caption" sx={{ color: '#10b981', fontWeight: 900 }}>
                  {metrics.winRate}%
                </Typography>
              </Box>
            </StyledPaper>
            
            {/* Security Fund */}
            <StyledPaper sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
                <Box>
                  <Typography variant="caption" sx={{ 
                    color: '#10b981', 
                    fontWeight: 700, 
                    letterSpacing: '1px',
                    display: 'block',
                    mb: 1
                  }}>
                    SECURITY RESERVE
                  </Typography>
                  <Typography variant="h4" sx={{ color: 'white', fontWeight: 900 }}>
                    ${state.securityFund.totalReserved.toLocaleString()}
                  </Typography>
                </Box>
                <Box sx={{ 
                  p: 1.5, 
                  bgcolor: alpha('#10b981', 0.1),
                  borderRadius: 2
                }}>
                  <ShieldCheck size={20} className="text-emerald-500" />
                </Box>
              </Box>
              
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="caption" sx={{ color: '#94a3b8', fontSize: '11px' }}>
                    Reserve Progress
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#10b981', fontWeight: 700 }}>
                    {state.securityFund.reserveProgress}%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={state.securityFund.reserveProgress}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    bgcolor: alpha('#1e293b', 0.5),
                    '& .MuiLinearProgress-bar': {
                      background: 'linear-gradient(90deg, #10b981 0%, #34d399 100%)',
                      borderRadius: 4
                    }
                  }}
                />
              </Box>
              
              <Typography variant="caption" sx={{ 
                color: '#64748b', 
                fontSize: '9px',
                display: 'block',
                textAlign: 'center'
              }}>
                APEX RESERVE ACTIVE • {state.activeAccount === AccountType.REAL ? 'LIVE PROTECTION' : 'SIMULATION MODE'}
              </Typography>
            </StyledPaper>
            
            {/* Active Trade */}
            <StyledPaper sx={{ p: 3, flex: 1 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                <Activity size={18} className="text-indigo-400" />
                <Typography variant="subtitle2" sx={{ color: 'white', fontWeight: 900 }}>
                  ACTIVE POSITION
                </Typography>
              </Box>
              
              {state.activeTrade ? (
                <TradePosition trade={state.activeTrade} />
              ) : (
                <Box sx={{ 
                  display: 'flex', 
                  flexDirection: 'column', 
                  alignItems: 'center',
                  justifyContent: 'center',
                  py: 8,
                  opacity: 0.5
                }}>
                  <Box sx={{ 
                    p: 3,
                    borderRadius: '50%',
                    bgcolor: alpha('#1e293b', 0.5),
                    mb: 2
                  }}>
                    <Network size={24} className="text-slate-500" />
                  </Box>
                  <Typography variant="caption" sx={{ 
                    color: '#94a3b8', 
                    fontWeight: 700,
                    letterSpacing: '1px'
                  }}>
                    SCANNERS IN STANDBY
                  </Typography>
                  <Typography variant="caption" sx={{ 
                    color: '#64748b', 
                    fontSize: '10px',
                    textAlign: 'center',
                    mt: 1
                  }}>
                    Awaiting market signals...
                  </Typography>
                </Box>
              )}
            </StyledPaper>
          </Box>
        </Grid>
        
        {/* Logs Panel */}
        {/* Fix: use item xs/md instead of size prop for Grid v1 */}
        <Grid item xs={12} md={8}>
          <StyledPaper sx={{ 
            display: 'flex', 
            flexDirection: 'column', 
            height: '100%',
            overflow: 'hidden'
          }}>
            {/* Logs Header */}
            <Box sx={{ 
              p: 2,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              borderBottom: `1px solid ${alpha('#334155', 0.3)}`
            }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <TerminalIcon size={18} className="text-indigo-400" />
                <Typography variant="caption" sx={{ 
                  color: 'white', 
                  fontWeight: 900,
                  letterSpacing: '1px'
                }}>
                  KERNEL LOGS
                </Typography>
                <Box sx={{ 
                  px: 1.5,
                  py: 0.5,
                  bgcolor: alpha('#1e293b', 0.5),
                  borderRadius: 1,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1
                }}>
                  <Database size={10} />
                  <Typography variant="caption" sx={{ 
                    color: '#94a3b8', 
                    fontSize: '9px',
                    fontWeight: 700
                  }}>
                    {formattedLogs.length}
                  </Typography>
                </Box>
              </Box>
              
              <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                <Button
                  size="small"
                  onClick={() => setAutoScroll(!autoScroll)}
                  sx={{
                    fontSize: '9px',
                    fontWeight: 700,
                    color: autoScroll ? '#10b981' : '#94a3b8'
                  }}
                >
                  {autoScroll ? 'AUTO-SCROLL: ON' : 'AUTO-SCROLL: OFF'}
                </Button>
                <Box sx={{ display: 'flex', gap: 0.5 }}>
                  <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: '#ef4444' }} />
                  <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: '#f59e0b' }} />
                  <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: '#10b981' }} />
                </Box>
              </Box>
            </Box>
            
            {/* Logs Content */}
            <Box
              ref={logsContainerRef}
              sx={{
                flex: 1,
                p: 3,
                overflowY: 'auto',
                fontFamily: '"JetBrains Mono", monospace',
                fontSize: '11px',
                '&::-webkit-scrollbar': {
                  width: '6px'
                },
                '&::-webkit-scrollbar-track': {
                  background: alpha('#0f172a', 0.5)
                },
                '&::-webkit-scrollbar-thumb': {
                  background: alpha('#6366f1', 0.3),
                  borderRadius: '3px'
                }
              }}
            >
              <AnimatePresence>
                {formattedLogs.map((log, index) => (
                  <LogEntryItem
                    key={log.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Box sx={{ display: 'flex', gap: 2 }}>
                      <Box sx={{ 
                        minWidth: 140,
                        color: '#64748b',
                        fontSize: '10px',
                        fontFamily: 'monospace'
                      }}>
                        [{log.timestamp}]
                      </Box>
                      <Box sx={{ 
                        color: log.level === 'error' ? '#ef4444' :
                               log.level === 'warning' ? '#f59e0b' :
                               log.level === 'info' ? '#3b82f6' : '#94a3b8',
                        fontWeight: log.level === 'error' ? 700 : 400,
                        flex: 1,
                        wordBreak: 'break-word'
                      }}>
                        {log.message}
                      </Box>
                    </Box>
                  </LogEntryItem>
                ))}
              </AnimatePresence>
              
              {state.logs.length === 0 && (
                <Box sx={{ 
                  display: 'flex', 
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  height: '100%',
                  opacity: 0.5
                }}>
                  <TerminalIcon size={48} className="text-slate-700" />
                  <Typography variant="caption" sx={{ 
                    color: '#94a3b8',
                    mt: 2,
                    fontWeight: 700
                  }}>
                    NO LOGS AVAILABLE
                  </Typography>
                </Box>
              )}
            </Box>
            
            {/* Footer */}
            <Box sx={{ 
              p: 2,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              borderTop: `1px solid ${alpha('#334155', 0.3)}`,
              bgcolor: alpha('#0f172a', 0.5)
            }}>
              <Box sx={{ display: 'flex', gap: 4 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Box sx={{ 
                    width: 6, 
                    height: 6, 
                    borderRadius: '50%',
                    bgcolor: performance.fps > 50 ? '#10b981' : '#f59e0b',
                    animation: `${pulse} 1s infinite`
                  }} />
                  <Typography variant="caption" sx={{ 
                    color: '#94a3b8',
                    fontSize: '10px',
                    fontWeight: 700
                  }}>
                    FPS: {performance.fps}
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Cpu size={10} className="text-indigo-400" />
                  <Typography variant="caption" sx={{ 
                    color: '#94a3b8',
                    fontSize: '10px',
                    fontWeight: 700
                  }}>
                    AGI Load: {state.isRunning ? '78%' : '12%'}
                  </Typography>
                </Box>
              </Box>
              
              <Typography variant="caption" sx={{ 
                color: '#64748b',
                fontSize: '9px',
                fontWeight: 900,
                letterSpacing: '1px'
              }}>
                KERNEL v4.8.0 • SOVEREIGN EDITION
              </Typography>
            </Box>
          </StyledPaper>
        </Grid>
      </Grid>
    </Box>
  );
};
