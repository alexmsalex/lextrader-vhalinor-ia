
import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, Grid, Tab, Tabs, Chip, Button, Switch, FormControlLabel, LinearProgress, Divider } from '@mui/material';
import { Brain, Zap, ShieldCheck, Globe, Activity, ShieldAlert, Wallet, Lock, Play, Pause, TrendingUp, History } from 'lucide-react';
import { motion as m, AnimatePresence } from 'framer-motion';
import { getAutonomousDirective } from '../services/gemini';
import { AccountType, TradingDirective, SecurityFund } from '../types';

// Fix: cast motion to any to avoid "Property 'initial' does not exist" type errors
const motion = m as any;

export const AGIStrategist: React.FC<{ nexusSnapshot: any }> = ({ nexusSnapshot }) => {
  const [accountType, setAccountType] = useState<AccountType>(AccountType.DEMO);
  const [isAutoPilot, setIsAutoPilot] = useState(false);
  const [securityFund, setSecurityFund] = useState<SecurityFund>({
    totalReserved: 12450.32,
    dailyGains: 842.15,
    lastTransfer: new Date().toISOString(),
    status: 'PROTECTED',
    reserveProgress: 85
  });
  const [activeDirective, setActiveDirective] = useState<TradingDirective | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const triggerAutonomousScan = async () => {
    setIsGenerating(true);
    const directive = await getAutonomousDirective("BTC/USDT", 98500, nexusSnapshot);
    if (directive) {
      setActiveDirective(directive);
      if (isAutoPilot) {
        console.log(`PAS: Executando Ordem em conta ${accountType}`, directive);
      }
    }
    setIsGenerating(false);
  };

  return (
    <Box sx={{ p: 4, display: 'flex', flexDirection: 'column', gap: 4, height: '100%', bgcolor: '#020617' }}>
      <header className="flex justify-between items-end border-b border-white/10 pb-6">
        <div>
          <Typography variant="h4" sx={{ fontWeight: 900, color: 'white', letterSpacing: -1 }}>
            AGI <span className="text-indigo-500 font-black">OMNI-STRATEGIC</span>
          </Typography>
          <Typography variant="caption" sx={{ color: '#6366f1', fontWeight: 'black', letterSpacing: 4, display: 'flex', alignItems: 'center', gap: 1 }}>
            <Activity size={12} className="animate-pulse" /> PROTOCOLO DE AUTOMAÇÃO SOBERANA (PAS)
          </Typography>
        </div>
        
        <div className="flex gap-4">
           <Paper sx={{ p: 1.5, bgcolor: '#0d1117', border: '1px solid #1e293b', borderRadius: 4, display: 'flex', gap: 2 }}>
              <Button 
                onClick={() => setAccountType(AccountType.DEMO)}
                sx={{ 
                  px: 3, borderRadius: 2, fontSize: '10px', fontWeight: 'black',
                  bgcolor: accountType === AccountType.DEMO ? 'rgba(99, 102, 241, 0.1)' : 'transparent',
                  color: accountType === AccountType.DEMO ? '#818cf8' : '#475569'
                }}
              >SIMULAÇÃO (DEMO)</Button>
              <Button 
                onClick={() => setAccountType(AccountType.REAL)}
                sx={{ 
                  px: 3, borderRadius: 2, fontSize: '10px', fontWeight: 'black',
                  bgcolor: accountType === AccountType.REAL ? 'rgba(239, 68, 68, 0.1)' : 'transparent',
                  color: accountType === AccountType.REAL ? '#ef4444' : '#475569'
                }}
              >APLICAÇÃO (REAL)</Button>
           </Paper>
        </div>
      </header>

      <Grid container spacing={4}>
        {/* Fix: use item xs/lg instead of size prop for Grid v1 */}
        <Grid item xs={12} lg={4}>
          <div className="space-y-6">
            <Paper sx={{ p: 4, bgcolor: '#0d1117', border: '1px solid #1e293b', borderRadius: 8 }}>
              <div className="flex justify-between items-center mb-6">
                <Typography variant="subtitle2" sx={{ color: 'white', fontWeight: 'black', display: 'flex', alignItems: 'center', gap: 2 }}>
                  <ShieldCheck size={18} className="text-indigo-400" /> STATUS DA AUTOMAÇÃO
                </Typography>
                <Switch checked={isAutoPilot} onChange={(e) => setIsAutoPilot(e.target.checked)} color="primary" />
              </div>
              
              <div className="space-y-4 mb-6">
                <StatusItem label="Ponte API" status="CONECTADO" color="#10b981" />
                <StatusItem label="Latência" status="45ms" color="#6366f1" />
                <StatusItem label="Modo" status={isAutoPilot ? "AUTÔNOMO" : "MANUAL"} color={isAutoPilot ? "#10b981" : "#f59e0b"} />
              </div>

              <Button 
                fullWidth 
                variant="contained" 
                onClick={triggerAutonomousScan}
                disabled={isGenerating}
                sx={{ py: 2, borderRadius: 3, bgcolor: '#6366f1', fontWeight: 'black' }}
                startIcon={isAutoPilot ? <Pause size={16}/> : <Play size={16}/>}
              >
                {isAutoPilot ? 'PAUSAR AUTOMAÇÃO' : 'INICIAR CICLO AGI'}
              </Button>
            </Paper>

            <Paper sx={{ p: 4, bgcolor: 'linear-gradient(135deg, #111827 0%, #020617 100%)', border: '1px solid #10b98130', borderRadius: 8 }}>
               <div className="flex justify-between items-start mb-4">
                 <div>
                   <Typography variant="caption" sx={{ color: '#10b981', fontWeight: 'black', tracking: 2 }}>FUNDO DE SEGURANÇA NEURAL</Typography>
                   <Typography variant="h4" sx={{ color: 'white', fontWeight: 'black', mt: 1 }}>${securityFund.totalReserved.toLocaleString()}</Typography>
                 </div>
                 <Lock size={24} className="text-emerald-500" />
               </div>
               <LinearProgress variant="determinate" value={securityFund.reserveProgress} sx={{ height: 4, borderRadius: 2, bgcolor: '#1e293b', '& .MuiLinearProgress-bar': { bgcolor: '#10b981' } }} />
               <div className="flex justify-between mt-3">
                 <span className="text-[10px] font-bold text-slate-500 uppercase">Ganhos de Hoje</span>
                 <span className="text-[10px] font-black text-emerald-400">+${securityFund.dailyGains}</span>
               </div>
               <Typography variant="caption" sx={{ color: '#475569', fontSize: '8px', mt: 2, display: 'block' }}>20% DE CADA LUCRO TRANSFERIDO AUTOMATICAMENTE</Typography>
            </Paper>
          </div>
        </Grid>

        {/* Fix: use item xs/lg instead of size prop for Grid v1 */}
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 4, bgcolor: '#020617', border: '1px solid #1e293b', borderRadius: 8, minHeight: '500px', display: 'flex', flexDirection: 'column' }}>
            <div className="flex items-center justify-between mb-8 border-b border-white/5 pb-4">
              <Typography variant="h6" sx={{ color: 'white', fontWeight: 'black', display: 'flex', alignItems: 'center', gap: 2 }}>
                <Zap size={20} className="text-yellow-400" /> DIRETRIZ DE OPERAÇÃO ATIVA
              </Typography>
              <Chip label={accountType} size="small" color={accountType === AccountType.REAL ? "error" : "primary"} sx={{ fontWeight: 'black' }} />
            </div>

            <Box sx={{ flex: 1 }}>
              {!activeDirective ? (
                <div className="flex flex-col items-center justify-center h-full text-slate-700 opacity-30 gap-4">
                  <Activity size={80} strokeWidth={1} />
                  <Typography variant="h6" fontWeight="900" sx={{ letterSpacing: 5 }}>AGUARDANDO SINAL IAG</Typography>
                </div>
              ) : (
                <motion.div initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }}>
                   <div className="grid grid-cols-2 gap-8 mb-8">
                      <DirectiveCard label="AÇÃO" value={activeDirective.side} color={activeDirective.side === 'BUY' ? '#10b981' : '#ef4444'} />
                      <DirectiveCard label="CONFIANÇA" value={`${(activeDirective.confidence * 100).toFixed(1)}%`} color="#6366f1" />
                   </div>

                   <div className="grid grid-cols-3 gap-4 mb-8">
                      <PriceBox label="ENTRADA" value={activeDirective.entryPrice} />
                      <PriceBox label="STOP-LOSS" value={activeDirective.stopLoss} isDanger />
                      <PriceBox label="TAKE-PROFIT" value={activeDirective.takeProfit} isSuccess />
                   </div>

                   <Paper sx={{ p: 3, bgcolor: '#0d1117', border: '1px solid #1e293b', borderRadius: 4 }}>
                      <Typography variant="caption" sx={{ color: '#475569', fontWeight: 'black', mb: 2, display: 'block' }}>LOG DE EXECUÇÃO PAS</Typography>
                      <div className="space-y-2">
                        <LogLine time="14:02:11" msg="Sincronizando com Binance API..." />
                        <LogLine time="14:02:12" msg={`Verificando conta ${accountType}... OK`} />
                        <LogLine time="14:02:13" msg="Calculando Stop-Loss Dinâmico via Gemini..." />
                        <LogLine time="14:02:14" msg="Aguardando trigger de preço no Nexus..." />
                      </div>
                   </Paper>
                </motion.div>
              )}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

const StatusItem = ({ label, status, color }: any) => (
  <div className="flex justify-between items-center border-b border-white/5 pb-2">
    <span className="text-[10px] font-black text-slate-500 uppercase">{label}</span>
    <span style={{ color, fontSize: '10px', fontWeight: 'black' }}>{status}</span>
  </div>
);

const DirectiveCard = ({ label, value, color }: any) => (
  <Box sx={{ p: 4, bgcolor: 'rgba(255,255,255,0.02)', border: `1px solid ${color}30`, borderRadius: 6, textAlign: 'center' }}>
    <Typography variant="caption" sx={{ color: '#475569', fontWeight: 'black', tracking: 2 }}>{label}</Typography>
    <Typography variant="h3" sx={{ color, fontWeight: 'black', mt: 1 }}>{value}</Typography>
  </Box>
);

const PriceBox = ({ label, value, isDanger, isSuccess }: any) => (
  <Box sx={{ p: 2, bgcolor: '#0a0a0a', border: '1px solid #1e293b', borderRadius: 4, textAlign: 'center' }}>
    <Typography variant="caption" sx={{ color: '#475569', fontWeight: 'bold' }}>{label}</Typography>
    <Typography sx={{ 
      color: isDanger ? '#ef4444' : isSuccess ? '#10b981' : 'white', 
      fontWeight: 'black', fontSize: '1rem', fontFamily: 'monospace' 
    }}>${value.toLocaleString()}</Typography>
  </Box>
);

const LogLine = ({ time, msg }: any) => (
  <div className="flex gap-4 font-mono text-[9px]">
    <span className="text-indigo-400">{time}</span>
    <span className="text-slate-400 uppercase">{msg}</span>
  </div>
);
