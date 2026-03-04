
import React, { useState, useEffect } from 'react';
import { 
  Activity, Brain, Zap, Sparkles, Shield, TrendingUp, StopCircle, 
  PlayCircle, Heart, SendHorizontal, Settings, Target, ShieldAlert,
  Globe, BarChart3, Binary, RefreshCcw, Users, BarChartHorizontal, Package,
  Sigma, Database, Share2, Bot, ShieldCheck, DraftingCompass
} from 'lucide-react';
import { Typography, Box, Chip } from '@mui/material';
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
import { PluginHub } from './components/PluginHub';
import { SylphAssistant } from './components/SylphAssistant';
import { AGIStrategist } from './components/AGIStrategist';
import { NeuralCortex } from './components/NeuralCortex';
import { NeuralMindMap } from './components/NeuralMindMap';
import { BotLexTerminal } from './components/BotLexTerminal';
import { AuthHub } from './components/AuthHub';
import { DependencyMonitor } from './components/DependencyMonitor';
import { CognitiveTrainingHub } from './components/CognitiveTrainingHub';
import { LTBTradingSuite } from './components/LTBTradingSuite';
import TradingViewWidget from './components/TradingViewWidget';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('execucao');
  const [isThinking, setIsThinking] = useState(false);
  const [isSimulating, setIsSimulating] = useState(false);
  const [livePrice, setLivePrice] = useState(98500.00);
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Kernel LEXTRADER-IAG 4.7.2 carregado. Interface TradingView Pro ativa no cockpit.', timestamp: new Date().toLocaleTimeString() }
  ]);
  
  const { snapshot: nexusSnapshot } = useNexusConsciousness(isSimulating);

  useEffect(() => {
    if (isSimulating) {
      const interval = setInterval(() => {
        setLivePrice(prev => prev + (Math.random() - 0.485) * (prev * 0.0007));
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [isSimulating]);

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;
    setMessages(prev => [...prev, { role: 'user', content: text, timestamp: new Date().toLocaleTimeString() }]);
    setIsThinking(true);
    try {
      // Fix: removed 3rd argument from getLuthienResponse to match signature
      const res = await getLuthienResponse(text, messages.slice(-5));
      setMessages(prev => [...prev, { role: 'assistant', content: res.text, timestamp: new Date().toLocaleTimeString() }]);
    } finally {
      setIsThinking(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#020617] text-slate-100 overflow-hidden font-sans">
      <SylphAssistant />
      
      <aside className="w-80 bg-[#010409] border-r border-indigo-500/10 flex flex-col z-30 shadow-2xl overflow-y-auto scrollbar-hide">
        <div className="p-8 border-b border-indigo-500/10 text-center sticky top-0 bg-[#010409] z-10">
          <div className="inline-flex p-4 bg-indigo-600 rounded-3xl shadow-[0_0_30px_rgba(79,70,229,0.5)] mb-4">
            <Heart size={28} className={`text-white ${isSimulating ? 'animate-pulse' : ''}`} />
          </div>
          <div className="flex flex-col">
            <span className="text-white font-black text-xl italic tracking-tighter uppercase font-mono">LEXTRADER</span>
            <span className="text-indigo-400 text-[8px] font-black tracking-[0.4em] uppercase mt-1">Ultimate Core v4.7.2</span>
          </div>
        </div>
        
        <nav className="flex-1 p-6 space-y-2">
          <SidebarItem active={activeTab === 'execucao'} onClick={() => setActiveTab('execucao')} icon={<TrendingUp size={18} />} label="Cockpit" />
          <SidebarItem active={activeTab === 'ltb'} onClick={() => setActiveTab('ltb')} icon={<DraftingCompass size={18} className="text-cyan-400" />} label="LTB Professional" />
          <SidebarItem active={activeTab === 'training'} onClick={() => setActiveTab('training')} icon={<Brain size={18} className="text-indigo-400" />} label="Training" />
          <SidebarItem active={activeTab === 'botlex'} onClick={() => setActiveTab('botlex')} icon={<Bot size={18} className="text-indigo-400" />} label="BOTLEX AGI" />
          <SidebarItem active={activeTab === 'omega'} onClick={() => setActiveTab('omega')} icon={<Target size={18} className="text-orange-400" />} label="Omega Terminal" />
          <SidebarItem active={activeTab === 'cortex'} onClick={() => setActiveTab('cortex')} icon={<Database size={18} className="text-emerald-400" />} label="Neural Cortex" />
          <SidebarItem active={activeTab === 'copy'} onClick={() => setActiveTab('copy')} icon={<Users size={18} className="text-cyan-400" />} label="Copy Trading" />
          <SidebarItem active={activeTab === 'analyze'} onClick={() => setActiveTab('analyze')} icon={<BarChartHorizontal size={18} className="text-emerald-400" />} label="IAG Analyze" />
          <SidebarItem active={activeTab === 'nexus'} onClick={() => setActiveTab('nexus')} icon={<Brain size={18} className="text-indigo-400" />} label="Neural Nexus" />
          <SidebarItem active={activeTab === 'risk'} onClick={() => setActiveTab('risk')} icon={<ShieldAlert size={18} className="text-red-400" />} label="Risk AGI" />
          <SidebarItem active={activeTab === 'luthien'} onClick={() => setActiveTab('luthien')} icon={<Sparkles size={18} className="text-indigo-400" />} label="Luthien ASI" />
        </nav>
      </aside>

      <main className="flex-1 overflow-y-auto relative flex flex-col bg-[#020617]">
        <header className="bg-[#020617]/95 backdrop-blur-3xl border-b border-indigo-500/10 p-6 flex justify-between items-center sticky top-0 z-40">
          <div className="flex items-center gap-10">
            <h1 className="text-2xl font-black tracking-tighter uppercase italic text-white flex items-center gap-4 font-mono">
              ULTIMATE NEXUS v4.7.2
              {isSimulating && <div className="w-2.5 h-2.5 rounded-full bg-green-500 animate-ping" />}
            </h1>
            <button onClick={() => setIsSimulating(!isSimulating)} className={`px-8 py-2 rounded-xl text-[10px] font-black transition-all uppercase flex items-center gap-2 ${isSimulating ? 'bg-red-600' : 'bg-green-600'}`}>
              {isSimulating ? <><StopCircle size={16}/> Stop Engine</> : <><PlayCircle size={16}/> Start Engine</>}
            </button>
          </div>
        </header>

        <div className="p-8 flex-1">
           {activeTab === 'execucao' && (
             <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
               <div className="lg:col-span-8">
                 <TradingCockpit price={livePrice} />
               </div>
               <div className="lg:col-span-4 space-y-8">
                 <ExchangeDashboard />
                 <ModuleMonitor />
                 <div className="p-6 bg-indigo-500/5 border border-indigo-500/10 rounded-[2.5rem] space-y-4 shadow-inner">
                    <div className="flex justify-between items-center mb-2">
                      <h4 className="text-[10px] font-black uppercase text-slate-400">Memory Sync</h4>
                      <RefreshCcw size={12} className="text-indigo-400 animate-spin-slow" />
                    </div>
                    <div className="flex justify-between items-center text-[10px] font-black uppercase">
                      <span className="text-slate-400">Engrams Saved</span>
                      <span className="text-indigo-400 font-mono">1,247</span>
                    </div>
                  </div>
               </div>
             </div>
           )}
           {activeTab === 'ltb' && <LTBTradingSuite />}
           {activeTab === 'training' && <CognitiveTrainingHub />}
           {activeTab === 'botlex' && <BotLexTerminal nexusSnapshot={nexusSnapshot} />}
           {activeTab === 'nexus' && <div className="grid grid-cols-1 lg:grid-cols-2 gap-8"><NexusVisualizer snapshot={nexusSnapshot} /><LuthienChat messages={messages} onSend={handleSendMessage} isThinking={isThinking} /></div>}
           {activeTab === 'omega' && <OmegaTradingTerminal />}
           {activeTab === 'cortex' && <NeuralCortex />}
           {activeTab === 'copy' && <CopyTradingHub />}
           {activeTab === 'analyze' && <NeuralOperationAnalyzer />}
           {activeTab === 'risk' && <NeuralOverrideController />}
           {activeTab === 'luthien' && <LuthienChat messages={messages} onSend={handleSendMessage} isThinking={isThinking} />}
        </div>
      </main>
    </div>
  );
};

const TradingCockpit: React.FC<{ price: number }> = ({ price }) => (
  <div className="bg-[#0d1117] border border-white/5 rounded-[4rem] p-1 shadow-2xl h-[700px] relative overflow-hidden flex flex-col">
    <div className="p-10 pb-4 flex justify-between items-start">
      <Box>
        <Typography variant="h3" sx={{ fontWeight: 'black', color: 'white', letterSpacing: -2, mb: 0.5, fontFamily: 'JetBrains Mono, monospace' }}>
          ${price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
        </Typography>
        <Typography variant="caption" sx={{ color: '#4ade80', fontWeight: 'black', letterSpacing: 2 }}>
          PROFESSIONAL TRADINGVIEW TERMINAL / USDT PAIR
        </Typography>
      </Box>
      <div className="flex gap-2">
        <Chip label="LIVE" size="small" sx={{ bgcolor: '#ef4444', color: 'white', fontWeight: 'black' }} />
        <Chip label="ADVANCED CHART" size="small" variant="outlined" sx={{ borderColor: '#6366f1', color: '#818cf8', fontWeight: 'black' }} />
      </div>
    </div>
    
    <div className="flex-1 w-full rounded-[3.5rem] overflow-hidden">
      <TradingViewWidget symbol="BINANCE:BTCUSDT" type="chart" />
    </div>
  </div>
);

const SidebarItem: React.FC<{ active: boolean, onClick: () => void, icon: React.ReactNode, label: string }> = ({ active, onClick, icon, label }) => (
  <button onClick={onClick} className={`w-full flex items-center gap-4 px-5 py-4 rounded-2xl transition-all border ${active ? 'bg-indigo-600 border-indigo-500 text-white shadow-lg shadow-indigo-500/20' : 'border-transparent text-slate-500 hover:bg-white/5'}`}>{icon} <span className="font-black text-[10px] uppercase tracking-wider">{label}</span></button>
);

const LuthienChat: React.FC<{ messages: Message[], onSend: (t: string) => void, isThinking: boolean }> = ({ messages, onSend, isThinking }) => {
  const [localInput, setLocalInput] = useState('');
  return (
    <div className="flex flex-col h-full bg-[#0d1117]/50 border border-indigo-500/10 rounded-[4rem] p-12 shadow-2xl overflow-hidden">
      <div className="flex-1 overflow-y-auto space-y-6 mb-8 pr-4 scrollbar-hide">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] px-8 py-5 rounded-3xl text-sm ${m.role === 'user' ? 'bg-indigo-600 text-white shadow-xl shadow-indigo-500/10' : 'bg-black/40 text-slate-300 border border-white/5'}`}>{m.content}</div>
          </div>
        ))}
        {isThinking && <div className="text-indigo-400 animate-pulse italic text-xs font-bold pl-4">Luthien está processando...</div>}
      </div>
      <div className="flex gap-4 p-4 bg-black/40 rounded-3xl border border-white/5 backdrop-blur-xl">
        <input value={localInput} onChange={e => setLocalInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && (onSend(localInput), setLocalInput(''))} placeholder="Consultar Luthien ASI..." className="flex-1 bg-transparent border-none px-6 text-sm text-white outline-none" />
        <button onClick={() => (onSend(localInput), setLocalInput(''))} className="w-12 h-12 bg-indigo-600 rounded-2xl flex items-center justify-center hover:bg-indigo-500 transition-colors shadow-lg shadow-indigo-500/20"><SendHorizontal size={20} className="text-white" /></button>
      </div>
    </div>
  );
};

export default App;
