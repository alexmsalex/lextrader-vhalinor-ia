
import React, { useState, useEffect, useMemo } from 'react';
import { 
  Heart, TrendingUp, DraftingCompass, Bot, Brain, Database, 
  ShieldCheck, Target, PlayCircle, StopCircle, Radio, Shield, 
  Activity, Cpu, Sparkles, Lock, Settings, BarChartHorizontal, Users,
  ShieldAlert, Sigma, LineChart, Globe, Atom
} from 'lucide-react';
import { Box, Chip, Tooltip } from '@mui/material';
import { Message } from './types';
import { getLuthienResponse } from './services/gemini';
import { useNexusConsciousness } from './useNexusConsciousness';
import { NexusVisualizer } from './NexusVisualizer';
import { OmegaTradingTerminal } from './OmegaTradingTerminal';
import { NeuralOperationAnalyzer } from './NeuralOperationAnalyzer';
import { NeuralOverrideController } from './NeuralOverrideController';
import { ExchangeDashboard } from './components/ExchangeDashboard';
import { ModuleMonitor } from './components/ModuleMonitor';
import { CopyTradingHub } from './components/CopyTradingHub';
import { SylphAssistant } from './components/SylphAssistant';
import { NeuralCortex } from './components/NeuralCortex';
import { NeuralMindMap } from './components/NeuralMindMap';
import { BotLexTerminal } from './components/BotLexTerminal';
import { AuthHub } from './components/AuthHub';
import { DependencyMonitor } from './components/DependencyMonitor';
import { CognitiveTrainingHub } from './components/CognitiveTrainingHub';
import { LTBTradingSuite } from './components/LTBTradingSuite';
import { neuralPredictor } from './services/NeuralPredictor';
import { NeuralPredictionDash } from './components/NeuralPredictionDash';
import { MarketIntelligencePanel } from './components/MarketIntelligencePanel';
import { QuantumFieldDashboard } from './components/QuantumFieldDashboard';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('execucao');
  const [isSimulating, setIsSimulating] = useState(false);
  const [priceHistory, setPriceHistory] = useState<number[]>([]);
  
  const { snapshot: nexusSnapshot } = useNexusConsciousness(isSimulating);

  useEffect(() => {
    const interval = setInterval(() => {
      if (isSimulating) {
        const nextPrice = 98500 + (Math.random() - 0.5) * 1000;
        setPriceHistory(prev => [...prev.slice(-199), nextPrice]);
      } else if (priceHistory.length === 0) {
        setPriceHistory(Array(100).fill(98500).map(p => p + (Math.random() - 0.5) * 500));
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [isSimulating, priceHistory.length]);

  return (
    <div className="flex h-screen bg-[#020617] text-slate-100 overflow-hidden font-sans">
      <SylphAssistant />
      
      <aside className="w-80 bg-[#010409] border-r border-indigo-500/10 flex flex-col z-30 shadow-2xl overflow-y-auto scrollbar-hide">
        <div className="p-8 border-b border-indigo-500/10 text-center sticky top-0 bg-[#010409] z-10">
          <div className="inline-flex p-4 bg-indigo-600 rounded-3xl shadow-[0_0_30px_rgba(79,70,229,0.5)] mb-4">
            <Heart size={28} className={isSimulating ? 'animate-pulse' : ''} />
          </div>
          <div className="flex flex-col">
            <span className="text-white font-black text-xl italic uppercase font-mono">LEXTRADER</span>
            <span className="text-indigo-400 text-[8px] font-black tracking-[0.4em] uppercase mt-1">SOVEREIGN CORE v5.0.0</span>
          </div>
        </div>
        
        <nav className="flex-1 p-6 space-y-2">
          <SidebarItem active={activeTab === 'execucao'} onClick={() => setActiveTab('execucao')} icon={<TrendingUp size={18} />} label="Cockpit Principal" />
          <SidebarItem active={activeTab === 'cortex'} onClick={() => setActiveTab('cortex')} icon={<Database size={18} className="text-emerald-400" />} label="Neural Memory (STM)" />
          <SidebarItem active={activeTab === 'quantum'} onClick={() => setActiveTab('quantum')} icon={<Atom size={18} className="text-cyan-400" />} label="Núcleo Quântico" />
          <SidebarItem active={activeTab === 'intel'} onClick={() => setActiveTab('intel')} icon={<Globe size={18} className="text-indigo-400" />} label="Market Intel" />
          <SidebarItem active={activeTab === 'forecast'} onClick={() => setActiveTab('forecast')} icon={<LineChart size={18} className="text-indigo-400" />} label="Neural Forecast" />
          <SidebarItem active={activeTab === 'ltb'} onClick={() => setActiveTab('ltb')} icon={<DraftingCompass size={18} className="text-cyan-400" />} label="LTB Professional" />
          <SidebarItem active={activeTab === 'training'} onClick={() => setActiveTab('training')} icon={<Cpu size={18} className="text-amber-400" />} label="Córtex Training" />
          <SidebarItem active={activeTab === 'botlex'} onClick={() => setActiveTab('botlex')} icon={<Bot size={18} />} label="BOTLEX AGI" />
          <SidebarItem active={activeTab === 'omega'} onClick={() => setActiveTab('omega')} icon={<Target size={18} className="text-orange-400" />} label="Omega Terminal" />
          <SidebarItem active={activeTab === 'mindmap'} onClick={() => setActiveTab('mindmap')} icon={<Brain size={18} className="text-purple-400" />} label="Neural Mind Map" />
          <SidebarItem active={activeTab === 'risk'} onClick={() => setActiveTab('risk')} icon={<ShieldAlert size={18} className="text-red-400" />} label="Risk AGI" />
          <SidebarItem active={activeTab === 'auth'} onClick={() => setActiveTab('auth')} icon={<Lock size={18} className="text-rose-400" />} label="Auth Gateway" />
        </nav>
      </aside>

      <main className="flex-1 overflow-y-auto relative flex flex-col bg-[#020617]">
        <header className="bg-[#020617]/95 backdrop-blur-3xl border-b border-indigo-500/10 p-6 flex justify-between items-center sticky top-0 z-40">
          <div className="flex items-center gap-10">
            <h1 className="text-2xl font-black tracking-tighter uppercase italic text-white flex items-center gap-4 font-mono">
              ULTIMATE NEXUS
              {isSimulating && <div className="w-2.5 h-2.5 rounded-full bg-green-500 animate-ping" />}
            </h1>
            <div className="flex gap-2">
              <button onClick={() => setIsSimulating(!isSimulating)} className={`px-6 py-2 rounded-xl text-[9px] font-black transition-all uppercase flex items-center gap-2 ${isSimulating ? 'bg-red-600/20 text-red-400 border border-red-500/30' : 'bg-green-600/20 text-green-400 border border-green-500/30'}`}>
                {isSimulating ? <><StopCircle size={14}/> Halt Engine</> : <><PlayCircle size={14}/> Start Engine</>}
              </button>
            </div>
          </div>
          <div className="flex gap-6 items-center">
             <div className="flex flex-col items-end">
                <span className="text-[9px] font-black text-slate-500 uppercase">Neural Confidence</span>
                <span className="text-indigo-400 font-mono text-xs">{(neuralPredictor.getStats().accuracy * 100).toFixed(1)}%</span>
             </div>
             <div className="w-10 h-10 rounded-full border border-indigo-500/20 bg-indigo-500/5 flex items-center justify-center">
                <Shield size={18} className="text-indigo-400" />
             </div>
          </div>
        </header>

        <div className="p-8 flex-1">
           {activeTab === 'execucao' && (
             <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
               <div className="lg:col-span-8">
                 <OmegaTradingTerminal />
               </div>
               <div className="lg:col-span-4 space-y-8">
                 <ModuleMonitor />
                 <ExchangeDashboard />
                 <DependencyMonitor />
               </div>
             </div>
           )}
           {activeTab === 'quantum' && <QuantumFieldDashboard priceHistory={priceHistory} />}
           {activeTab === 'intel' && <MarketIntelligencePanel symbol="BTC/USDT" />}
           {activeTab === 'forecast' && <NeuralPredictionDash prices={priceHistory} />}
           {activeTab === 'ltb' && <LTBTradingSuite />}
           {activeTab === 'training' && <CognitiveTrainingHub />}
           {activeTab === 'botlex' && <BotLexTerminal nexusSnapshot={nexusSnapshot} />}
           {activeTab === 'cortex' && <NeuralCortex />}
           {activeTab === 'mindmap' && <NeuralMindMap />}
           {activeTab === 'risk' && <NeuralOverrideController />}
           {activeTab === 'auth' && <AuthHub />}
           {activeTab === 'omega' && <OmegaTradingTerminal />}
        </div>
      </main>
    </div>
  );
};

const SidebarItem: React.FC<{ active: boolean, onClick: () => void, icon: React.ReactNode, label: string }> = ({ active, onClick, icon, label }) => (
  <button onClick={onClick} className={`w-full flex items-center gap-4 px-5 py-4 rounded-2xl transition-all border ${active ? 'bg-indigo-600 border-indigo-500 text-white shadow-lg shadow-indigo-500/20' : 'border-transparent text-slate-500 hover:bg-white/5'}`}>{icon} <span className="font-black text-[10px] uppercase tracking-wider">{label}</span></button>
);

export default App;
