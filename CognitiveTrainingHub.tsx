
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { Box, Grid, Paper, Typography, Button, LinearProgress, Chip, alpha, styled } from '@mui/material';
import { Brain, Zap, Activity, RefreshCcw, Sparkles, Database, Cpu } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer } from 'recharts';
import { motion as m, AnimatePresence } from 'framer-motion';
import { learningEngine } from '../services/LearningService';

// Fix: cast motion components to any to bypass type errors for standard motion props
const motion = m as any;

const StyledPaper = styled(Paper)(({ theme }) => ({
  background: 'linear-gradient(145deg, #0f172a 0%, #1e293b 100%)',
  border: `1px solid ${alpha('#334155', 0.3)}`,
  backdropFilter: 'blur(10px)',
  '&:hover': { borderColor: alpha('#6366f1', 0.5) }
}));

export const CognitiveTrainingHub: React.FC = () => {
  const [stats, setStats] = useState(learningEngine.getStats());
  const [isLoading, setIsLoading] = useState(false);
  const [geminiAdvice, setGeminiAdvice] = useState<string | null>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      setStats(learningEngine.getStats());
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleSync = async () => {
    setIsLoading(true);
    const advice = await learningEngine.consolidateWithGemini();
    setGeminiAdvice(advice);
    setIsLoading(false);
  };

  const chartData = useMemo(() => 
    stats.history.map((h, i) => ({ epoch: i + 1, loss: h.loss })), 
    [stats.history]
  );

  return (
    <Box sx={{ p: 0, display: 'flex', flexDirection: 'column', gap: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 900, color: 'white' }}>Cognitive <span className="text-indigo-500">Training Hub</span></Typography>
          <Typography variant="caption" sx={{ color: '#94a3b8', fontWeight: 700, letterSpacing: '2px' }}>REINFORCEMENT LEARNING KERNEL</Typography>
        </Box>
        <Chip label="SYNAPSE ACTIVE" color="success" sx={{ fontWeight: 900, fontSize: '10px' }} icon={<Activity size={12}/>} />
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} lg={8}>
          <StyledPaper sx={{ p: 3, height: '400px', display: 'flex', flexDirection: 'column' }}>
            <Typography variant="subtitle2" sx={{ color: 'white', fontWeight: 900, mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
              <Activity size={18} className="text-indigo-400" /> CONVERGENCE ANALYSIS (LOSS)
            </Typography>
            <Box sx={{ flex: 1, minWidth: 0 }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="colorLoss" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke={alpha('#334155', 0.5)} vertical={false} />
                  <XAxis dataKey="epoch" hide />
                  <YAxis stroke="#64748b" fontSize={11} />
                  <RechartsTooltip contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: 8 }} />
                  <Area type="monotone" dataKey="loss" stroke="#ef4444" fill="url(#colorLoss)" strokeWidth={2} isAnimationActive={false} />
                </AreaChart>
              </ResponsiveContainer>
            </Box>
          </StyledPaper>
        </Grid>

        <Grid item xs={12} lg={4}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3, height: '100%' }}>
            <StyledPaper sx={{ p: 3, flex: 1 }}>
              <Typography variant="subtitle2" sx={{ color: 'white', fontWeight: 900, mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Cpu size={18} className="text-indigo-400" /> SYNAPTIC STATS
              </Typography>
              <div className="space-y-4">
                <MetricRow label="Accuracy" value={stats.metrics.accuracy} color="#10b981" />
                <MetricRow label="Stability" value={stats.metrics.stability} color="#6366f1" />
                <MetricRow label="Generalization" value={stats.metrics.generalization} color="#f59e0b" />
              </div>
            </StyledPaper>

            <StyledPaper sx={{ p: 3, bgcolor: alpha('#6366f1', 0.05), border: `1px solid ${alpha('#6366f1', 0.3)}` }}>
              <Typography variant="subtitle2" sx={{ color: 'white', fontWeight: 900, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Brain size={18} className="text-indigo-400" /> NEURAL CONSOLIDATION
              </Typography>
              <Button fullWidth onClick={handleSync} disabled={isLoading} variant="contained" sx={{ bgcolor: '#6366f1', fontWeight: 900 }} startIcon={isLoading ? <RefreshCcw className="animate-spin" size={16}/> : <Sparkles size={16}/>}>
                {isLoading ? 'SYNCING...' : 'BRAIN SYNC'}
              </Button>
            </StyledPaper>
          </Box>
        </Grid>
      </Grid>

      {geminiAdvice && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <StyledPaper sx={{ p: 4, borderLeft: '4px solid #6366f1' }}>
            <Typography variant="h6" sx={{ color: 'white', fontWeight: 900, mb: 2 }}>Gemini Cortex Advice</Typography>
            <Typography variant="body1" sx={{ color: '#cbd5e1', fontStyle: 'italic', lineHeight: 1.8 }}>"{geminiAdvice}"</Typography>
          </StyledPaper>
        </motion.div>
      )}
    </Box>
  );
};

const MetricRow = ({ label, value, color }: any) => (
  <Box>
    <div className="flex justify-between mb-1">
      <Typography variant="caption" sx={{ color: '#94a3b8', fontWeight: 700 }}>{label.toUpperCase()}</Typography>
      <Typography variant="caption" sx={{ color: 'white', fontWeight: 900 }}>{value}%</Typography>
    </div>
    <LinearProgress variant="determinate" value={value} sx={{ height: 4, borderRadius: 2, bgcolor: alpha('#1e293b', 0.5), '& .MuiLinearProgress-bar': { bgcolor: color } }} />
  </Box>
);
