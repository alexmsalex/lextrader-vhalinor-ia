
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  Box,
  Grid, // Fix: changed Grid2 to Grid
  Paper,
  Typography,
  Button,
  LinearProgress,
  Chip,
  alpha,
  styled,
  keyframes,
  IconButton
} from '@mui/material';
import {
  Brain,
  Zap,
  Activity,
  RefreshCcw,
  Sparkles,
  Cpu,
  Database,
  BarChart3,
  Target,
  Shield,
  Info,
  Share2,
  Download
} from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer
} from 'recharts';
import { motion as m, AnimatePresence } from 'framer-motion';
import { learningEngine, LearningStats, TrainingMetrics } from '../services/LearningService';

// Fix: cast motion to any to avoid "Property 'initial' does not exist" type errors
const motion = m as any;

const StyledPaper = styled(Paper)(({ theme }) => ({
  background: 'linear-gradient(145deg, #0f172a 0%, #1e293b 100%)',
  border: `1px solid ${alpha('#334155', 0.3)}`,
  backdropFilter: 'blur(10px)',
  transition: 'all 0.3s ease',
  '&:hover': {
    borderColor: alpha('#6366f1', 0.5),
    transform: 'translateY(-2px)'
  }
}));

const MetricCard = styled(Box)(({ theme }) => ({
  padding: '16px',
  borderRadius: '16px',
  background: alpha('#1e293b', 0.5),
  border: `1px solid ${alpha('#334155', 0.3)}`,
  '&:hover': {
    borderColor: alpha('#6366f1', 0.5),
    background: alpha('#1e293b', 0.8)
  }
}));

const PerformanceMetrics = React.memo(({ metrics }: { metrics: TrainingMetrics }) => {
  const data = useMemo(() => [
    { label: 'Generalization', value: metrics.generalization, color: '#6366f1', icon: <Brain size={12} /> },
    { label: 'Response Time', value: metrics.responseTime, color: '#10b981', icon: <Zap size={12} /> },
    { label: 'Accuracy', value: metrics.accuracy, color: '#f59e0b', icon: <Target size={12} /> },
    { label: 'Stability', value: metrics.stability, color: '#8b5cf6', icon: <Shield size={12} /> }
  ], [metrics]);

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      {data.map((item, index) => (
        <motion.div key={item.label} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: index * 0.1 }}>
          <MetricCard>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                {item.icon}
                <Typography variant="caption" sx={{ color: '#94a3b8', fontWeight: 700, fontSize: '10px' }}>{item.label}</Typography>
              </Box>
              <Typography variant="caption" sx={{ color: item.color, fontWeight: 900 }}>{item.value}%</Typography>
            </Box>
            <LinearProgress variant="determinate" value={item.value} sx={{ height: 6, borderRadius: 3, bgcolor: alpha('#1e293b', 0.5), '& .MuiLinearProgress-bar': { background: item.color } }} />
          </MetricCard>
        </motion.div>
      ))}
    </Box>
  );
});

export const CognitiveServices: React.FC = () => {
  const [stats, setStats] = useState<LearningStats>(learningEngine.getStats());
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
    stats.history.map((h, i) => ({ epoch: i + 1, loss: h.loss, accuracy: h.accuracy || 0 })), 
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
        {/* Fix: use item xs/lg instead of size prop for Grid v1 */}
        <Grid item xs={12} lg={8}>
          <StyledPaper sx={{ p: 3, height: '400px', display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
               <Typography variant="subtitle2" sx={{ color: 'white', fontWeight: 900, display: 'flex', alignItems: 'center', gap: 1 }}>
                 <BarChart3 size={18} className="text-indigo-400" /> CONVERGENCE ANALYSIS
               </Typography>
               <Chip label={`Epochs: ${stats.epochs}`} size="small" sx={{ bgcolor: alpha('#6366f1', 0.1), color: '#818cf8', fontWeight: 700 }} />
            </Box>
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
                  <Area type="monotone" dataKey="accuracy" stroke="#10b981" fill="transparent" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </Box>
          </StyledPaper>
        </Grid>

        {/* Fix: use item xs/lg instead of size prop for Grid v1 */}
        <Grid item xs={12} lg={4}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3, height: '100%' }}>
            <StyledPaper sx={{ p: 3, flex: 1 }}>
              <Typography variant="subtitle2" sx={{ color: 'white', fontWeight: 900, mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Cpu size={18} className="text-indigo-400" /> SYNAPTIC EFFICIENCY
              </Typography>
              <PerformanceMetrics metrics={stats.metrics} />
            </StyledPaper>

            <StyledPaper sx={{ p: 3, bgcolor: alpha('#6366f1', 0.05) }}>
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
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
               <Typography variant="h6" sx={{ color: 'white', fontWeight: 900 }}>Gemini Cortex Advice</Typography>
               <Box sx={{ display: 'flex', gap: 1 }}>
                  <IconButton size="small"><Share2 size={16}/></IconButton>
                  <IconButton size="small"><Download size={16}/></IconButton>
               </Box>
            </Box>
            <Typography variant="body1" sx={{ color: '#cbd5e1', fontStyle: 'italic', lineHeight: 1.8 }}>"{geminiAdvice}"</Typography>
          </StyledPaper>
        </motion.div>
      )}
    </Box>
  );
};
