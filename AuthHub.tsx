
import React, { useState } from 'react';
import { Box, Typography, Paper, Grid, TextField, Button, Select, MenuItem, FormControl, InputLabel, IconButton, Switch, Chip, Tooltip, CircularProgress } from '@mui/material';
import { Shield, Key, Eye, EyeOff, Link, CheckCircle, XCircle, Settings, Server, Lock, User, KeyRound, Globe, Info } from 'lucide-react';
import { ApiCredential, AccountType } from '../types';
import { platformApis } from '../services/PlatformAPIs';

export const AuthHub: React.FC = () => {
  const [showSecret, setShowSecret] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [credentials, setCredentials] = useState<ApiCredential[]>([
    { platform: 'BINANCE', apiKey: 'BK-9402...', apiSecret: '********', type: AccountType.DEMO, status: 'CONNECTED' },
    { platform: 'CTRADER', apiKey: 'trader_lex_pro', apiSecret: '********', type: AccountType.REAL, status: 'DISCONNECTED' },
    { platform: 'PIONEX', apiKey: 'lex_operator_01', apiSecret: '********', type: AccountType.DEMO, status: 'CONNECTED' }
  ]);

  const [formData, setFormData] = useState<Partial<ApiCredential>>({
    platform: 'BINANCE',
    type: AccountType.DEMO,
    apiKey: '',
    apiSecret: ''
  });

  const handleEstablishConnection = async () => {
    if (!formData.apiKey || !formData.apiSecret) return;
    
    setIsConnecting(true);
    const res = await platformApis.connect(formData as ApiCredential);
    
    if (res.success) {
      const newCred: ApiCredential = {
        platform: formData.platform as any,
        apiKey: formData.apiKey || '',
        apiSecret: '********',
        type: formData.type || AccountType.DEMO,
        status: 'CONNECTED'
      };
      setCredentials(prev => [newCred, ...prev]);
      setFormData({ ...formData, apiKey: '', apiSecret: '' });
    } else {
      console.error(res.message);
    }
    setIsConnecting(false);
  };

  const handleTestConnection = (platform: string) => {
    console.log(`[AUTH] Handshake com ${platform} iniciado...`);
  };

  const isLoginMode = formData.platform === 'CTRADER' || formData.platform === 'PIONEX';

  return (
    <Box sx={{ p: 4, bgcolor: '#020617', minHeight: '100%', display: 'flex', flexDirection: 'column', gap: 4 }}>
      <header className="flex justify-between items-center border-b border-white/10 pb-6">
        <div>
          <Typography variant="h4" sx={{ fontWeight: 900, color: 'white', letterSpacing: -1 }}>
            AUTH <span className="text-indigo-500">GATEWAY</span>
          </Typography>
          <Typography variant="caption" sx={{ color: '#6366f1', fontWeight: 'black', letterSpacing: 4, display: 'flex', alignItems: 'center', gap: 1 }}>
            <Lock size={12} /> SISTEMA DE CONECTIVIDADE MULTI-PLATAFORMA
          </Typography>
        </div>
        <div className="flex gap-3">
          <div className="flex items-center gap-2 px-4 py-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20">
            <Globe size={16} className="text-indigo-400" />
            <span className="text-[10px] font-black text-indigo-400 uppercase tracking-widest">Bridges Ativas: {credentials.length}</span>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-emerald-500/10 rounded-xl border border-emerald-500/20">
            <Shield size={16} className="text-emerald-500" />
            <span className="text-[10px] font-black text-emerald-500 uppercase">Criptografia Ativa</span>
          </div>
        </div>
      </header>

      <Grid container spacing={4}>
        <Grid item xs={12} lg={4}>
          <Paper sx={{ 
            p: 4, bgcolor: '#0d1117', border: '1px solid #1e293b', borderRadius: 8, 
            position: 'relative', overflow: 'hidden',
            boxShadow: '0 10px 40px rgba(0,0,0,0.4)'
          }}>
            <div className="absolute -top-4 -right-4 p-4 opacity-[0.03] rotate-12">
               <KeyRound size={120} />
            </div>
            
            <Typography variant="subtitle2" sx={{ color: 'white', fontWeight: 'black', mb: 4, display: 'flex', alignItems: 'center', gap: 2 }}>
              <Settings size={18} className="text-indigo-400" /> NOVA CONEXÃO
            </Typography>

            <div className="space-y-6 relative z-10">
              <FormControl fullWidth variant="filled" sx={{ bgcolor: 'rgba(0,0,0,0.3)', borderRadius: 2 }}>
                <InputLabel sx={{ color: '#475569', fontSize: '0.75rem', fontWeight: 'black' }}>SELECIONAR PLATAFORMA</InputLabel>
                <Select
                  value={formData.platform}
                  onChange={(e) => setFormData({ ...formData, platform: e.target.value as any, apiKey: '', apiSecret: '' })}
                  sx={{ color: 'white', fontWeight: 'black', fontSize: '0.9rem' }}
                >
                  <MenuItem value="BINANCE">BINANCE (API KEY)</MenuItem>
                  <MenuItem value="BYBIT">BYBIT (API KEY)</MenuItem>
                  <MenuItem value="CTRADER">CTRADER (LOGIN/SENHA)</MenuItem>
                  <MenuItem value="PIONEX">PIONEX (LOGIN/SENHA)</MenuItem>
                </Select>
              </FormControl>

              <FormControl fullWidth variant="filled" sx={{ bgcolor: 'rgba(0,0,0,0.3)', borderRadius: 2 }}>
                <InputLabel sx={{ color: '#475569', fontSize: '0.75rem', fontWeight: 'black' }}>TIPO DE EXECUÇÃO</InputLabel>
                <Select
                  value={formData.type}
                  onChange={(e) => setFormData({ ...formData, type: e.target.value as any })}
                  sx={{ color: 'white', fontWeight: 'black', fontSize: '0.9rem' }}
                >
                  <MenuItem value={AccountType.DEMO}>MODO SIMULAÇÃO (DEMO)</MenuItem>
                  <MenuItem value={AccountType.REAL}>MODO PRODUÇÃO (REAL)</MenuItem>
                </Select>
              </FormControl>

              <Box sx={{ p: 2, bgcolor: 'rgba(99, 102, 241, 0.05)', borderRadius: 3, border: '1px dashed rgba(99, 102, 241, 0.2)' }}>
                 <Typography variant="caption" sx={{ color: '#818cf8', fontWeight: 'black', display: 'flex', alignItems: 'center', gap: 1.5, textTransform: 'uppercase' }}>
                   <User size={14} /> 
                   {isLoginMode ? "Requer credenciais de usuário" : "Requer chaves de integração API"}
                 </Typography>
              </Box>

              <TextField
                fullWidth
                label={isLoginMode ? "USUÁRIO / LOGIN" : "API KEY / TOKEN"}
                variant="filled"
                value={formData.apiKey}
                onChange={(e) => setFormData({...formData, apiKey: e.target.value})}
                placeholder={isLoginMode ? "Ex: trader_pro_01" : "Insira sua Key"}
                sx={{ bgcolor: 'rgba(0,0,0,0.3)', borderRadius: 2, '& input': { color: 'white', fontFamily: 'monospace', fontWeight: 'bold' } }}
              />

              <TextField
                fullWidth
                label={isLoginMode ? "SENHA DE ACESSO" : "SECRET / PRIVATE KEY"}
                type={showSecret ? 'text' : 'password'}
                variant="filled"
                value={formData.apiSecret}
                onChange={(e) => setFormData({...formData, apiSecret: e.target.value})}
                InputProps={{
                  endAdornment: (
                    <IconButton onClick={() => setShowSecret(!showSecret)} sx={{ color: '#475569' }}>
                      {showSecret ? <EyeOff size={18}/> : <Eye size={18}/>}
                    </IconButton>
                  )
                }}
                sx={{ bgcolor: 'rgba(0,0,0,0.3)', borderRadius: 2, '& input': { color: 'white', fontFamily: 'monospace' } }}
              />

              <Button 
                fullWidth 
                variant="contained" 
                onClick={handleEstablishConnection}
                disabled={isConnecting}
                startIcon={isConnecting ? <CircularProgress size={18} color="inherit" /> : <Link size={18} />}
                sx={{ 
                  bgcolor: '#6366f1', py: 2, borderRadius: 3, fontWeight: 'black', mt: 2,
                  boxShadow: '0 4px 20px rgba(99, 102, 241, 0.3)',
                  transition: 'all 0.3s',
                  '&:hover': { bgcolor: '#4f46e5', transform: 'scale(1.01)' }
                }}
              >
                {isConnecting ? "SINCRONIZANDO..." : "ESTABELECER PONTE NEURAL"}
              </Button>
            </div>
          </Paper>
        </Grid>

        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 4, bgcolor: '#0d1117', border: '1px solid #1e293b', borderRadius: 8, height: '100%', display: 'flex', flexDirection: 'column' }}>
            <div className="flex justify-between items-center mb-8">
              <Typography variant="subtitle2" sx={{ color: 'white', fontWeight: 'black', display: 'flex', alignItems: 'center', gap: 2 }}>
                <Server size={18} className="text-indigo-400" /> PONTES ATIVAS NO KERNEL
              </Typography>
              <Chip label={`${credentials.length} ATIVAS`} size="small" sx={{ height: 20, bgcolor: 'rgba(99, 102, 241, 0.1)', color: '#818cf8', fontWeight: 'black', fontSize: '9px' }} />
            </div>

            <div className="space-y-4 flex-1">
              {credentials.map((cred, idx) => (
                <Box key={idx} sx={{ 
                  p: 3, bgcolor: 'rgba(255,255,255,0.02)', border: '1px solid #1e293b', borderRadius: 4, 
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center', 
                  transition: 'all 0.2s', '&:hover': { bgcolor: 'rgba(255,255,255,0.04)', borderColor: '#6366f140' } 
                }}>
                  <div className="flex items-center gap-6">
                    <Box sx={{ 
                      p: 2, bgcolor: cred.type === AccountType.REAL ? 'rgba(239, 68, 68, 0.1)' : 'rgba(99, 102, 241, 0.1)', 
                      borderRadius: 3, border: `1px solid ${cred.type === AccountType.REAL ? '#ef444430' : '#6366f130'}`,
                      display: 'flex', alignItems: 'center', justifyContent: 'center'
                    }}>
                       {cred.type === AccountType.REAL ? <Lock size={20} className="text-rose-500" /> : <Settings size={20} className="text-indigo-500" />}
                    </Box>
                    <div>
                      <div className="flex items-center gap-3">
                        <Typography sx={{ color: 'white', fontWeight: 'black', fontSize: '0.95rem' }}>{cred.platform}</Typography>
                        <Chip 
                          label={cred.type === AccountType.REAL ? "REAL / LIVE" : "DEMO / SIM"} 
                          size="small" 
                          sx={{ 
                            height: 18, fontWeight: 'black', fontSize: '8px', 
                            bgcolor: cred.type === AccountType.REAL ? '#ef4444' : '#6366f1', 
                            color: 'white', px: 1
                          }} 
                        />
                      </div>
                      <Typography sx={{ color: '#475569', fontSize: '0.7rem', fontWeight: 'black', mt: 0.5, fontFamily: 'monospace' }}>
                        ID: <span className="text-indigo-400">{cred.apiKey}</span>
                      </Typography>
                    </div>
                  </div>

                  <div className="flex items-center gap-6">
                    <div className="flex flex-col items-end gap-1">
                       <div className="flex items-center gap-2">
                          {cred.status === 'CONNECTED' ? <CheckCircle size={14} className="text-emerald-500" /> : <XCircle size={14} className="text-rose-500" />}
                          <span className={`text-[10px] font-black uppercase ${cred.status === 'CONNECTED' ? 'text-emerald-500' : 'text-rose-500'}`}>{cred.status}</span>
                       </div>
                       <Typography variant="caption" sx={{ color: '#334155', fontSize: '8px', fontWeight: 'black' }}>PULSE: 12ms</Typography>
                    </div>

                    <Button 
                      size="small" 
                      variant="outlined" 
                      onClick={() => handleTestConnection(cred.platform)}
                      sx={{ borderColor: '#334155', color: '#94a3b8', fontSize: '9px', fontWeight: 'black', borderRadius: 2, px: 2, height: 32, '&:hover': { borderColor: '#6366f1', color: 'white' } }}
                    >
                      TEST SYNC
                    </Button>
                    
                    <Tooltip title="Configurações de Ponte">
                      <IconButton size="small" sx={{ color: '#475569' }}>
                        <Settings size={16} />
                      </IconButton>
                    </Tooltip>
                  </div>
                </Box>
              ))}
            </div>

            <Box sx={{ mt: 4, p: 3, bgcolor: 'rgba(239, 68, 68, 0.05)', borderRadius: 6, border: '1px solid rgba(239, 68, 68, 0.1)', display: 'flex', gap: 3, alignItems: 'center' }}>
               <div className="p-2 bg-rose-500/10 rounded-full">
                 <Shield size={20} className="text-rose-500" />
               </div>
               <Typography variant="body2" sx={{ color: '#94a3b8', fontStyle: 'italic', fontSize: '0.75rem', lineHeight: 1.5 }}>
                 <strong>SEGURANÇA CRÍTICA:</strong> As credenciais são processadas em ambiente isolado (Sandboxed). O LEXTRADER-IAG 4.7.2 nunca solicita chaves com permissão de saque. Use chaves exclusivas para operação e leitura.
               </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};
