
import React, { useState } from 'react';
import { Box, Grid, Paper, Typography, Button, Avatar, Chip, LinearProgress } from '@mui/material';
import { Users, TrendingUp, ShieldCheck, Zap, Star } from 'lucide-react';

interface StrategyProvider {
  id: string;
  name: string;
  avatar: string;
  roi: number;
  winRate: number;
  risk: number;
  followers: number;
  tags: string[];
}

export const CopyTradingHub: React.FC = () => {
  const providers: StrategyProvider[] = [
    { id: '1', name: 'Neural Alpha Bot', avatar: 'N', roi: 428.5, winRate: 84.2, risk: 3, followers: 1240, tags: ['Scalping', 'AI-Powered'] },
    { id: '2', name: 'Quantum Whale', avatar: 'Q', roi: 1120.2, winRate: 72.1, risk: 5, followers: 850, tags: ['Swing', 'BTC-Focused'] },
    { id: '3', name: 'Nexus Stabilizer', avatar: 'S', roi: 125.4, winRate: 91.5, risk: 1, followers: 3200, tags: ['Low-Risk', 'Forex'] },
  ];

  return (
    <Box sx={{ spaceY: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
         <Box>
           <Typography variant="h4" sx={{ fontWeight: 'black', color: 'white', fontStyle: 'italic' }}>COPY TRADING HUB</Typography>
           <Typography variant="caption" sx={{ color: '#6366f1', fontWeight: 'bold', letterSpacing: 2 }}>SYNC YOUR PORTFOLIO WITH TOP NEURAL NODES</Typography>
         </Box>
         <Button variant="contained" startIcon={<Star size={18} />} sx={{ bgcolor: '#6366f1', borderRadius: 4, px: 4, fontWeight: 'black' }}>BECOME A PROVIDER</Button>
      </Box>

      <Grid container spacing={4}>
        {providers.map(p => (
          <Grid item xs={12} md={4} key={p.id}>
            <Paper sx={{ p: 4, bgcolor: '#0a0a0a', border: '1px solid #1e293b', borderRadius: 8, transition: 'transform 0.3s', '&:hover': { transform: 'translateY(-10px)', borderColor: '#6366f1' } }}>
               <Box sx={{ display: 'flex', gap: 3, alignItems: 'center', mb: 3 }}>
                 <Avatar sx={{ width: 64, height: 64, bgcolor: '#6366f1', fontWeight: 'black', fontSize: '1.5rem' }}>{p.avatar}</Avatar>
                 <Box>
                   <Typography variant="h6" sx={{ color: 'white', fontWeight: 'black' }}>{p.name}</Typography>
                   <Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
                     {p.tags.map(t => <Chip key={t} label={t} size="small" sx={{ height: 18, fontSize: '0.6rem', bgcolor: '#1e293b', color: '#94a3b8', fontWeight: 'bold' }} />)}
                   </Box>
                 </Box>
               </Box>

               <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
                  <Box>
                    <Typography variant="caption" sx={{ color: '#475569', fontWeight: 'bold', display: 'block' }}>ROI (TOTAL)</Typography>
                    <Typography variant="h5" sx={{ color: '#10b981', fontWeight: 'black' }}>+{p.roi}%</Typography>
                  </Box>
                  <Box sx={{ textAlign: 'right' }}>
                    <Typography variant="caption" sx={{ color: '#475569', fontWeight: 'bold', display: 'block' }}>FOLLOWERS</Typography>
                    <Typography variant="h5" sx={{ color: 'white', fontWeight: 'black' }}>{p.followers.toLocaleString()}</Typography>
                  </Box>
               </Box>

               <Box sx={{ spaceY: 3, mb: 4 }}>
                  <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="caption" sx={{ color: '#94a3b8', fontWeight: 'bold' }}>WIN RATE</Typography>
                      <Typography variant="caption" sx={{ color: 'white', fontWeight: 'bold' }}>{p.winRate}%</Typography>
                    </Box>
                    <LinearProgress variant="determinate" value={p.winRate} sx={{ height: 4, borderRadius: 2, bgcolor: '#1e293b', '& .MuiLinearProgress-bar': { bgcolor: '#10b981' } }} />
                  </Box>
                  <Box sx={{ mt: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="caption" sx={{ color: '#94a3b8', fontWeight: 'bold' }}>RISK INDEX</Typography>
                      <Typography variant="caption" sx={{ color: '#ef4444', fontWeight: 'bold' }}>{p.risk}/10</Typography>
                    </Box>
                    <LinearProgress variant="determinate" value={p.risk * 10} sx={{ height: 4, borderRadius: 2, bgcolor: '#1e293b', '& .MuiLinearProgress-bar': { bgcolor: '#ef4444' } }} />
                  </Box>
               </Box>

               <Button fullWidth variant="contained" sx={{ bgcolor: 'white', color: 'black', py: 1.5, borderRadius: 4, fontWeight: 'black', '&:hover': { bgcolor: '#e2e8f0' } }}>SYNC NOW</Button>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};
