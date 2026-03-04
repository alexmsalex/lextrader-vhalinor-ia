package com.behavioralanalytics;

import java.time.Instant;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.Consumer;
import java.util.stream.Collectors;

// ==================== TIPOS E INTERFACES ====================

class OrderFlow {
    private String timestamp;
    private String symbol;
    private List<OrderLevel> bids;
    private List<OrderLevel> asks;
    private List<Trade> trades;
    private double volume;
    private double price;
    private double spread;
    private int marketDepth;

    // Construtor
    public OrderFlow(String timestamp, String symbol, List<OrderLevel> bids, List<OrderLevel> asks, 
                     List<Trade> trades, double volume, double price, double spread, int marketDepth) {
        this.timestamp = timestamp;
        this.symbol = symbol;
        this.bids = bids;
        this.asks = asks;
        this.trades = trades;
        this.volume = volume;
        this.price = price;
        this.spread = spread;
        this.marketDepth = marketDepth;
    }

    // Getters e Setters
    public String getTimestamp() { return timestamp; }
    public void setTimestamp(String timestamp) { this.timestamp = timestamp; }
    public String getSymbol() { return symbol; }
    public void setSymbol(String symbol) { this.symbol = symbol; }
    public List<OrderLevel> getBids() { return bids; }
    public void setBids(List<OrderLevel> bids) { this.bids = bids; }
    public List<OrderLevel> getAsks() { return asks; }
    public void setAsks(List<OrderLevel> asks) { this.asks = asks; }
    public List<Trade> getTrades() { return trades; }
    public void setTrades(List<Trade> trades) { this.trades = trades; }
    public double getVolume() { return volume; }
    public void setVolume(double volume) { this.volume = volume; }
    public double getPrice() { return price; }
    public void setPrice(double price) { this.price = price; }
    public double getSpread() { return spread; }
    public void setSpread(double spread) { this.spread = spread; }
    public int getMarketDepth() { return marketDepth; }
    public void setMarketDepth(int marketDepth) { this.marketDepth = marketDepth; }
}

class OrderLevel {
    private double price;
    private double quantity;
    private int orderCount;
    private boolean isAggressive;

    public OrderLevel(double price, double quantity, int orderCount, boolean isAggressive) {
        this.price = price;
        this.quantity = quantity;
        this.orderCount = orderCount;
        this.isAggressive = isAggressive;
    }

    public OrderLevel(double price, double quantity, int orderCount) {
        this(price, quantity, orderCount, false);
    }

    // Getters e Setters
    public double getPrice() { return price; }
    public void setPrice(double price) { this.price = price; }
    public double getQuantity() { return quantity; }
    public void setQuantity(double quantity) { this.quantity = quantity; }
    public int getOrderCount() { return orderCount; }
    public void setOrderCount(int orderCount) { this.orderCount = orderCount; }
    public boolean isAggressive() { return isAggressive; }
    public void setAggressive(boolean aggressive) { isAggressive = aggressive; }
}

class Trade {
    private String id;
    private double price;
    private double quantity;
    private String timestamp;
    private String side; // "buy" ou "sell"
    private boolean isLargeOrder;

    public Trade(String id, double price, double quantity, String timestamp, String side, boolean isLargeOrder) {
        this.id = id;
        this.price = price;
        this.quantity = quantity;
        this.timestamp = timestamp;
        this.side = side;
        this.isLargeOrder = isLargeOrder;
    }

    // Getters e Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public double getPrice() { return price; }
    public void setPrice(double price) { this.price = price; }
    public double getQuantity() { return quantity; }
    public void setQuantity(double quantity) { this.quantity = quantity; }
    public String getTimestamp() { return timestamp; }
    public void setTimestamp(String timestamp) { this.timestamp = timestamp; }
    public String getSide() { return side; }
    public void setSide(String side) { this.side = side; }
    public boolean isLargeOrder() { return isLargeOrder; }
    public void setLargeOrder(boolean largeOrder) { isLargeOrder = largeOrder; }
}

class BehavioralAnalysis {
    private double manipulationProbability;
    private String retailSentiment; // Extreme_Fear, Fear, Neutral, Greed, Extreme_Greed
    private String whaleActivity; // None, Light, Moderate, Heavy, Extreme
    private double riskLevel;
    private double confidence;
    private List<String> patterns;
    private List<String> recommendations;
    private double anomalyScore;
    private double liquidityImpact;

    public BehavioralAnalysis(double manipulationProbability, String retailSentiment, String whaleActivity,
                              double riskLevel, double confidence, List<String> patterns, 
                              List<String> recommendations, double anomalyScore, double liquidityImpact) {
        this.manipulationProbability = manipulationProbability;
        this.retailSentiment = retailSentiment;
        this.whaleActivity = whaleActivity;
        this.riskLevel = riskLevel;
        this.confidence = confidence;
        this.patterns = patterns;
        this.recommendations = recommendations;
        this.anomalyScore = anomalyScore;
        this.liquidityImpact = liquidityImpact;
    }

    // Getters e Setters
    public double getManipulationProbability() { return manipulationProbability; }
    public void setManipulationProbability(double manipulationProbability) { this.manipulationProbability = manipulationProbability; }
    public String getRetailSentiment() { return retailSentiment; }
    public void setRetailSentiment(String retailSentiment) { this.retailSentiment = retailSentiment; }
    public String getWhaleActivity() { return whaleActivity; }
    public void setWhaleActivity(String whaleActivity) { this.whaleActivity = whaleActivity; }
    public double getRiskLevel() { return riskLevel; }
    public void setRiskLevel(double riskLevel) { this.riskLevel = riskLevel; }
    public double getConfidence() { return confidence; }
    public void setConfidence(double confidence) { this.confidence = confidence; }
    public List<String> getPatterns() { return patterns; }
    public void setPatterns(List<String> patterns) { this.patterns = patterns; }
    public List<String> getRecommendations() { return recommendations; }
    public void setRecommendations(List<String> recommendations) { this.recommendations = recommendations; }
    public double getAnomalyScore() { return anomalyScore; }
    public void setAnomalyScore(double anomalyScore) { this.anomalyScore = anomalyScore; }
    public double getLiquidityImpact() { return liquidityImpact; }
    public void setLiquidityImpact(double liquidityImpact) { this.liquidityImpact = liquidityImpact; }
}

class AnalysisConfig {
    private String model;
    private Map<String, Object> responseSchema;
    private double temperature;
    private int maxOutputTokens;
    private boolean enableHistoricalAnalysis;
    private double riskThreshold;

    public AnalysisConfig() {
        this.model = "gemini-3-flash-preview";
        this.temperature = 0.2;
        this.maxOutputTokens = 1024;
        this.enableHistoricalAnalysis = true;
        this.riskThreshold = 70;
    }

    // Getters e Setters
    public String getModel() { return model; }
    public void setModel(String model) { this.model = model; }
    public Map<String, Object> getResponseSchema() { return responseSchema; }
    public void setResponseSchema(Map<String, Object> responseSchema) { this.responseSchema = responseSchema; }
    public double getTemperature() { return temperature; }
    public void setTemperature(double temperature) { this.temperature = temperature; }
    public int getMaxOutputTokens() { return maxOutputTokens; }
    public void setMaxOutputTokens(int maxOutputTokens) { this.maxOutputTokens = maxOutputTokens; }
    public boolean isEnableHistoricalAnalysis() { return enableHistoricalAnalysis; }
    public void setEnableHistoricalAnalysis(boolean enableHistoricalAnalysis) { this.enableHistoricalAnalysis = enableHistoricalAnalysis; }
    public double getRiskThreshold() { return riskThreshold; }
    public void setRiskThreshold(double riskThreshold) { this.riskThreshold = riskThreshold; }
}

class HistoricalPattern {
    private String timestamp;
    private String pattern;
    private double impact;
    private int duration;

    public HistoricalPattern(String timestamp, String pattern, double impact, int duration) {
        this.timestamp = timestamp;
        this.pattern = pattern;
        this.impact = impact;
        this.duration = duration;
    }

    // Getters e Setters
    public String getTimestamp() { return timestamp; }
    public void setTimestamp(String timestamp) { this.timestamp = timestamp; }
    public String getPattern() { return pattern; }
    public void setPattern(String pattern) { this.pattern = pattern; }
    public double getImpact() { return impact; }
    public void setImpact(double impact) { this.impact = impact; }
    public int getDuration() { return duration; }
    public void setDuration(int duration) { this.duration = duration; }
}

class ProcessedData {
    private double volumeImbalance;
    private double largeOrderRatio;
    private double tradeClustering;
    private double volatilityScore;

    public ProcessedData(double volumeImbalance, double largeOrderRatio, double tradeClustering, double volatilityScore) {
        this.volumeImbalance = volumeImbalance;
        this.largeOrderRatio = largeOrderRatio;
        this.tradeClustering = tradeClustering;
        this.volatilityScore = volatilityScore;
    }

    // Getters e Setters
    public double getVolumeImbalance() { return volumeImbalance; }
    public void setVolumeImbalance(double volumeImbalance) { this.volumeImbalance = volumeImbalance; }
    public double getLargeOrderRatio() { return largeOrderRatio; }
    public void setLargeOrderRatio(double largeOrderRatio) { this.largeOrderRatio = largeOrderRatio; }
    public double getTradeClustering() { return tradeClustering; }
    public void setTradeClustering(double tradeClustering) { this.tradeClustering = tradeClustering; }
    public double getVolatilityScore() { return volatilityScore; }
    public void setVolatilityScore(double volatilityScore) { this.volatilityScore = volatilityScore; }
}

class HistoricalStats {
    private int totalAnalyses;
    private int highRiskCount;
    private Map<String, Integer> commonPatterns;
    private double averageRisk;

    public HistoricalStats(int totalAnalyses, int highRiskCount, Map<String, Integer> commonPatterns, double averageRisk) {
        this.totalAnalyses = totalAnalyses;
        this.highRiskCount = highRiskCount;
        this.commonPatterns = commonPatterns;
        this.averageRisk = averageRisk;
    }

    // Getters e Setters
    public int getTotalAnalyses() { return totalAnalyses; }
    public void setTotalAnalyses(int totalAnalyses) { this.totalAnalyses = totalAnalyses; }
    public int getHighRiskCount() { return highRiskCount; }
    public void setHighRiskCount(int highRiskCount) { this.highRiskCount = highRiskCount; }
    public Map<String, Integer> getCommonPatterns() { return commonPatterns; }
    public void setCommonPatterns(Map<String, Integer> commonPatterns) { this.commonPatterns = commonPatterns; }
    public double getAverageRisk() { return averageRisk; }
    public void setAverageRisk(double averageRisk) { this.averageRisk = averageRisk; }
}

class AnalysisEvent {
    private String type;
    private Map<String, Object> data;

    public AnalysisEvent(String type, Map<String, Object> data) {
        this.type = type;
        this.data = data;
    }

    public String getType() { return type; }
    public Map<String, Object> getData() { return data; }
}

class CacheEntry {
    private BehavioralAnalysis analysis;
    private long timestamp;

    public CacheEntry(BehavioralAnalysis analysis, long timestamp) {
        this.analysis = analysis;
        this.timestamp = timestamp;
    }

    public BehavioralAnalysis getAnalysis() { return analysis; }
    public long getTimestamp() { return timestamp; }
}

// ==================== INTERFACE DO EVENT LISTENER ====================

interface AnalysisEventListener {
    void onEvent(AnalysisEvent event);
}

// ==================== CLASSE PRINCIPAL ====================

class BehavioralAnalytics {
    private static final Map<String, Object> PATTERN_DEFINITIONS = new HashMap<>();
    private static final Map<String, RiskLevel> RISK_LEVELS = new HashMap<>();
    
    static {
        PATTERN_DEFINITIONS.put("WHALE_WALL", "Large limit orders at specific price levels");
        PATTERN_DEFINITIONS.put("SPOOFING", "Quick placement and cancellation of large orders");
        PATTERN_DEFINITIONS.put("PUMP_DUMP", "Artificial price inflation followed by rapid sell-off");
        PATTERN_DEFINITIONS.put("STOP_HUNTING", "Intentional triggering of stop-loss orders");
        PATTERN_DEFINITIONS.put("ORDER_BOOK_IMBALANCE", "Significant disparity between bid/ask volumes");
        PATTERN_DEFINITIONS.put("MOMENTUM_EXHAUSTION", "Declining volume during price moves");

        RISK_LEVELS.put("LOW", new RiskLevel(0, 30, "#10B981"));
        RISK_LEVELS.put("MEDIUM", new RiskLevel(31, 60, "#F59E0B"));
        RISK_LEVELS.put("HIGH", new RiskLevel(61, 85, "#EF4444"));
        RISK_LEVELS.put("EXTREME", new RiskLevel(86, 100, "#7C3AED"));
    }

    private GoogleGenAI ai;
    private AnalysisConfig config;
    private List<HistoricalPattern> historicalPatterns = new ArrayList<>();
    private Map<String, CacheEntry> analysisCache = new ConcurrentHashMap<>();
    private long cacheTTL = 5 * 60 * 1000; // 5 minutos
    private List<AnalysisEventListener> listeners = new ArrayList<>();

    public BehavioralAnalytics() {
        this(new AnalysisConfig());
    }

    public BehavioralAnalytics(AnalysisConfig config) {
        String apiKey = System.getenv("GOOGLE_AI_API_KEY");
        if (apiKey == null) {
            apiKey = System.getenv("API_KEY");
        }
        if (apiKey == null) {
            throw new IllegalArgumentException("API_KEY não encontrada nas variáveis de ambiente. Configure GOOGLE_AI_API_KEY ou API_KEY.");
        }

        this.ai = new GoogleGenAI(apiKey);
        this.config = config;
    }

    public void addListener(AnalysisEventListener listener) {
        listeners.add(listener);
    }

    public void removeListener(AnalysisEventListener listener) {
        listeners.remove(listener);
    }

    private void emitEvent(String type, Map<String, Object> data) {
        AnalysisEvent event = new AnalysisEvent(type, data);
        for (AnalysisEventListener listener : listeners) {
            listener.onEvent(event);
        }
    }

    /**
     * Realiza análise comportamental completa do fluxo de ordens
     */
    public BehavioralAnalysis analyzeBehavior(OrderFlow orderFlow) throws Exception {
        try {
            // Emitir evento de início de análise
            Map<String, Object> startData = new HashMap<>();
            startData.put("symbol", orderFlow.getSymbol());
            startData.put("timestamp", Instant.now().toString());
            emitEvent("analysisStarted", startData);

            // Verificar cache
            String cacheKey = generateCacheKey(orderFlow);
            CacheEntry cached = analysisCache.get(cacheKey);
            
            if (cached != null && (System.currentTimeMillis() - cached.getTimestamp()) < cacheTTL) {
                Map<String, Object> cacheData = new HashMap<>();
                cacheData.put("symbol", orderFlow.getSymbol());
                emitEvent("cacheHit", cacheData);
                return cached.getAnalysis();
            }

            // Pré-processamento dos dados
            ProcessedData processedData = preprocessOrderFlow(orderFlow);
            
            // Detecção de padrões técnicos
            List<String> technicalPatterns = detectTechnicalPatterns(processedData);
            
            // Análise de sentimento com IA
            Map<String, Object> aiAnalysis = performAIAnalysis(orderFlow, technicalPatterns);
            
            // Análise histórica (se habilitada)
            List<HistoricalPattern> historicalInsights = new ArrayList<>();
            if (config.isEnableHistoricalAnalysis()) {
                historicalInsights = analyzeHistoricalPatterns(orderFlow.getSymbol());
            }

            // Combinação dos resultados
            BehavioralAnalysis finalAnalysis = combineAnalyses(
                aiAnalysis, 
                technicalPatterns, 
                historicalInsights,
                processedData
            );

            // Validação da análise
            validateAnalysis(finalAnalysis);

            // Armazenar em cache
            analysisCache.put(cacheKey, new CacheEntry(finalAnalysis, System.currentTimeMillis()));

            // Adicionar aos padrões históricos
            if (finalAnalysis.getAnomalyScore() > 50) {
                historicalPatterns.add(new HistoricalPattern(
                    Instant.now().toString(),
                    technicalPatterns.isEmpty() ? "Unknown" : technicalPatterns.get(0),
                    finalAnalysis.getRiskLevel(),
                    300 // 5 minutos em segundos
                ));
            }

            // Emitir evento de conclusão
            Map<String, Object> completeData = new HashMap<>();
            completeData.put("symbol", orderFlow.getSymbol());
            completeData.put("analysis", finalAnalysis);
            completeData.put("timestamp", Instant.now().toString());
            emitEvent("analysisCompleted", completeData);

            return finalAnalysis;

        } catch (Exception error) {
            Map<String, Object> errorData = new HashMap<>();
            errorData.put("error", error.getMessage());
            errorData.put("symbol", orderFlow.getSymbol());
            emitEvent("analysisError", errorData);
            
            // Retornar análise segura em caso de erro
            return getFallbackAnalysis(orderFlow);
        }
    }

    /**
     * Análise em batch para múltiplos símbolos
     */
    public Map<String, BehavioralAnalysis> analyzeBatch(List<OrderFlow> orderFlows) throws Exception {
        Map<String, BehavioralAnalysis> results = new ConcurrentHashMap<>();
        int batchSize = 5;
        
        for (int i = 0; i < orderFlows.size(); i += batchSize) {
            int end = Math.min(i + batchSize, orderFlows.size());
            List<OrderFlow> batch = orderFlows.subList(i, end);
            
            List<CompletableFuture<Map.Entry<String, BehavioralAnalysis>>> futures = new ArrayList<>();
            
            for (OrderFlow orderFlow : batch) {
                CompletableFuture<Map.Entry<String, BehavioralAnalysis>> future = 
                    CompletableFuture.supplyAsync(() -> {
                        try {
                            BehavioralAnalysis analysis = analyzeBehavior(orderFlow);
                            return new AbstractMap.SimpleEntry<>(orderFlow.getSymbol(), analysis);
                        } catch (Exception e) {
                            System.err.println("Falha na análise de " + orderFlow.getSymbol() + ": " + e.getMessage());
                            return null;
                        }
                    });
                futures.add(future);
            }
            
            CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
            
            for (CompletableFuture<Map.Entry<String, BehavioralAnalysis>> future : futures) {
                Map.Entry<String, BehavioralAnalysis> entry = future.get();
                if (entry != null) {
                    results.put(entry.getKey(), entry.getValue());
                }
            }
            
            // Delay entre batches para evitar rate limiting
            if (i + batchSize < orderFlows.size()) {
                Thread.sleep(1000);
            }
        }
        
        return results;
    }

    /**
     * Obtém estatísticas históricas para um símbolo
     */
    public HistoricalStats getHistoricalStats(String symbol) {
        List<HistoricalPattern> symbolPatterns = historicalPatterns.stream()
            .filter(p -> extractSymbolFromPattern(p).equals(symbol))
            .collect(Collectors.toList());
        
        Map<String, Integer> patternFrequency = new HashMap<>();
        for (HistoricalPattern p : symbolPatterns) {
            patternFrequency.put(p.getPattern(), patternFrequency.getOrDefault(p.getPattern(), 0) + 1);
        }
        
        List<HistoricalPattern> highRiskPatterns = symbolPatterns.stream()
            .filter(p -> p.getImpact() > 70)
            .collect(Collectors.toList());
        
        double averageRisk = 0;
        if (!symbolPatterns.isEmpty()) {
            averageRisk = symbolPatterns.stream()
                .mapToDouble(HistoricalPattern::getImpact)
                .sum() / symbolPatterns.size();
        }
        
        return new HistoricalStats(
            symbolPatterns.size(),
            highRiskPatterns.size(),
            patternFrequency,
            averageRisk
        );
    }

    /**
     * Reseta os padrões históricos
     */
    public void clearHistoricalData() {
        historicalPatterns.clear();
        analysisCache.clear();
        Map<String, Object> clearData = new HashMap<>();
        clearData.put("timestamp", Instant.now().toString());
        emitEvent("dataCleared", clearData);
    }

    // ==================== MÉTODOS PRIVADOS ====================

    private Map<String, Object> performAIAnalysis(OrderFlow orderFlow, List<String> technicalPatterns) throws Exception {
        String prompt = buildAnalysisPrompt(orderFlow, technicalPatterns);
        
        // Simulação da chamada à API (substituir pela implementação real)
        Map<String, Object> result = ai.generateContent(prompt, config);
        
        // Validação dos resultados
        validateAIResponse(result);
        
        Map<String, Object> analysis = new HashMap<>();
        analysis.put("manipulationProbability", result.getOrDefault("manipulationProbability", 0.0));
        analysis.put("retailSentiment", result.getOrDefault("retailSentiment", "Neutral"));
        analysis.put("whaleActivity", result.getOrDefault("whaleActivity", "None"));
        analysis.put("riskLevel", result.getOrDefault("riskLevel", 50.0));
        analysis.put("confidence", result.getOrDefault("confidence", 80.0));
        analysis.put("patterns", result.getOrDefault("detectedPatterns", new ArrayList<String>()));
        analysis.put("anomalyScore", result.getOrDefault("anomalyScore", 0.0));
        
        return analysis;
    }

    private String buildAnalysisPrompt(OrderFlow orderFlow, List<String> technicalPatterns) {
        long largeTrades = orderFlow.getTrades().stream()
            .filter(Trade::isLargeOrder)
            .count();
        
        StringBuilder prompt = new StringBuilder();
        prompt.append("Realize uma análise comportamental completa do mercado para o símbolo " + orderFlow.getSymbol() + ".\n\n");
        prompt.append("CONTEXTO DO MERCADO:\n");
        prompt.append("- Volume total: " + String.format("%.0f", orderFlow.getVolume()) + "\n");
        prompt.append("- Spread atual: " + String.format("%.4f", orderFlow.getSpread()) + "\n");
        prompt.append("- Profundidade do mercado: " + orderFlow.getMarketDepth() + "\n");
        prompt.append("- Trades grandes detectados: " + largeTrades + "\n\n");
        
        prompt.append("PADRÕES TÉCNICOS DETECTADOS:\n");
        for (String pattern : technicalPatterns) {
            prompt.append("- " + pattern + "\n");
        }
        prompt.append("\n");
        
        prompt.append("DADOS DO FLUXO DE ORDENS:\n");
        prompt.append("Bids: " + orderFlow.getBids().stream().limit(5)
            .map(b -> String.format("{price: %.2f, qty: %.2f}", b.getPrice(), b.getQuantity()))
            .collect(Collectors.joining(", ")) + "\n");
        prompt.append("Asks: " + orderFlow.getAsks().stream().limit(5)
            .map(a -> String.format("{price: %.2f, qty: %.2f}", a.getPrice(), a.getQuantity()))
            .collect(Collectors.joining(", ")) + "\n");
        
        prompt.append("\nANÁLISE SOLICITADA:\n");
        prompt.append("1. Avalie a probabilidade de manipulação de mercado\n");
        prompt.append("2. Determine o sentimento dos pequenos investidores (retail)\n");
        prompt.append("3. Identifique atividade de grandes players (whales)\n");
        prompt.append("4. Calcule o nível de risco geral\n");
        prompt.append("5. Detecte padrões comportamentais anômalos\n");
        
        return prompt.toString();
    }

    private ProcessedData preprocessOrderFlow(OrderFlow orderFlow) {
        double totalBidVolume = orderFlow.getBids().stream()
            .mapToDouble(OrderLevel::getQuantity)
            .sum();
        double totalAskVolume = orderFlow.getAsks().stream()
            .mapToDouble(OrderLevel::getQuantity)
            .sum();
        
        long largeTrades = orderFlow.getTrades().stream()
            .filter(t -> t.getQuantity() > 1000)
            .count();
        int totalTrades = orderFlow.getTrades().size();
        
        // Calcular clustering de trades (agrupamento temporal)
        double timeClustering = 0;
        if (orderFlow.getTrades().size() > 1) {
            List<Long> timeDiffs = new ArrayList<>();
            for (int i = 1; i < orderFlow.getTrades().size(); i++) {
                long diff = Instant.parse(orderFlow.getTrades().get(i).getTimestamp()).toEpochMilli() -
                           Instant.parse(orderFlow.getTrades().get(i-1).getTimestamp()).toEpochMilli();
                timeDiffs.add(diff);
            }
            double avgDiff = timeDiffs.stream().mapToLong(Long::longValue).average().orElse(0);
            long finalAvgDiff = (long) avgDiff;
            long count = timeDiffs.stream().filter(d -> d < finalAvgDiff / 2).count();
            timeClustering = (double) count / timeDiffs.size();
        }
        
        double volumeImbalance = totalBidVolume > 0 ? 
            (totalAskVolume - totalBidVolume) / (totalAskVolume + totalBidVolume) : 0;
        
        double largeOrderRatio = totalTrades > 0 ? (double) largeTrades / totalTrades : 0;
        
        return new ProcessedData(
            volumeImbalance,
            largeOrderRatio,
            timeClustering,
            calculateVolatility(orderFlow)
        );
    }

    private List<String> detectTechnicalPatterns(ProcessedData processedData) {
        List<String> patterns = new ArrayList<>();
        
        if (Math.abs(processedData.getVolumeImbalance()) > 0.7) {
            patterns.add("ORDER_BOOK_IMBALANCE");
        }
        
        if (processedData.getLargeOrderRatio() > 0.3) {
            patterns.add("WHALE_ACTIVITY");
        }
        
        if (processedData.getTradeClustering() > 0.6) {
            patterns.add("TRADE_CLUSTERING");
        }
        
        if (processedData.getVolatilityScore() > 0.8) {
            patterns.add("HIGH_VOLATILITY");
        }
        
        return patterns;
    }

    private double calculateVolatility(OrderFlow orderFlow) {
        if (orderFlow.getTrades().size() < 5) return 0;
        
        List<Double> prices = orderFlow.getTrades().stream()
            .map(Trade::getPrice)
            .collect(Collectors.toList());
        List<Double> returns = new ArrayList<>();
        
        for (int i = 1; i < prices.size(); i++) {
            returns.add(Math.abs((prices.get(i) - prices.get(i-1)) / prices.get(i-1)));
        }
        
        double avgReturn = returns.stream().mapToDouble(Double::doubleValue).average().orElse(0);
        double variance = returns.stream()
            .mapToDouble(r -> Math.pow(r - avgReturn, 2))
            .average().orElse(0);
        
        return Math.sqrt(variance) * Math.sqrt(365); // Volatilidade anualizada
    }

    private BehavioralAnalysis combineAnalyses(
            Map<String, Object> aiAnalysis,
            List<String> technicalPatterns,
            List<HistoricalPattern> historicalInsights,
            ProcessedData processedData) {
        
        // Fatores de ajuste baseados em dados técnicos
        double patternBonus = technicalPatterns.size() * 5;
        double imbalancePenalty = Math.abs(processedData.getVolumeImbalance()) * 20;
        
        // Ajustar risco baseado em padrões históricos
        double historicalRisk = 0;
        if (!historicalInsights.isEmpty()) {
            historicalRisk = historicalInsights.stream()
                .mapToDouble(HistoricalPattern::getImpact)
                .average().orElse(0);
        }
        
        double baseRisk = (double) aiAnalysis.getOrDefault("riskLevel", 50.0);
        double adjustedRisk = Math.min(100, baseRisk + patternBonus + imbalancePenalty);
        
        // Gerar recomendações baseadas na análise
        String sentiment = (String) aiAnalysis.getOrDefault("retailSentiment", "Neutral");
        List<String> recommendations = generateRecommendations(
            adjustedRisk,
            sentiment,
            technicalPatterns
        );
        
        @SuppressWarnings("unchecked")
        List<String> aiPatterns = (List<String>) aiAnalysis.getOrDefault("patterns", new ArrayList<>());
        List<String> allPatterns = new ArrayList<>(aiPatterns);
        allPatterns.addAll(technicalPatterns);
        
        return new BehavioralAnalysis(
            (double) aiAnalysis.getOrDefault("manipulationProbability", 0.0),
            sentiment,
            (String) aiAnalysis.getOrDefault("whaleActivity", "None"),
            adjustedRisk,
            (double) aiAnalysis.getOrDefault("confidence", 80.0),
            allPatterns,
            recommendations,
            (double) aiAnalysis.getOrDefault("anomalyScore", 0.0),
            calculateLiquidityImpact(processedData.getVolumeImbalance())
        );
    }

    private List<String> generateRecommendations(double riskLevel, String sentiment, List<String> patterns) {
        List<String> recommendations = new ArrayList<>();
        
        if (riskLevel > 80) {
            recommendations.add("⚠️ CONSIDERAR REDUÇÃO DE EXPOSIÇÃO");
            recommendations.add("🔍 MONITORAR ATIVIDADE DE WHALES DE PERTO");
        }
        
        if (patterns.contains("ORDER_BOOK_IMBALANCE")) {
            recommendations.add("📊 VERIFICAR DESEQUILÍBRIO NO BOOK DE ORDENS");
        }
        
        if ("Extreme_Greed".equals(sentiment)) {
            recommendations.add("💰 CUIDADO COM SOBREVALORIZAÇÃO - CONSIDERAR TAKING PROFITS");
        } else if ("Extreme_Fear".equals(sentiment)) {
            recommendations.add("📉 OPORTUNIDADE POTENCIAL DE COMPRA (FEAR & GREED)");
        }
        
        if (patterns.contains("HIGH_VOLATILITY")) {
            recommendations.add("⚡ AJUSTAR STOP-LOSS PARA VOLATILIDADE ELEVADA");
        }
        
        return recommendations;
    }

    private double calculateLiquidityImpact(double volumeImbalance) {
        return Math.abs(volumeImbalance) * 100;
    }

    private void validateAnalysis(BehavioralAnalysis analysis) {
        List<String> errors = new ArrayList<>();
        
        if (analysis.getRiskLevel() < 0 || analysis.getRiskLevel() > 100) {
            errors.add("riskLevel fora do intervalo 0-100");
        }
        
        if (analysis.getManipulationProbability() < 0 || analysis.getManipulationProbability() > 100) {
            errors.add("manipulationProbability fora do intervalo 0-100");
        }
        
        if (analysis.getConfidence() < 0 || analysis.getConfidence() > 100) {
            errors.add("confidence fora do intervalo 0-100");
        }
        
        if (!errors.isEmpty()) {
            throw new IllegalArgumentException("Análise inválida: " + String.join(", ", errors));
        }
    }

    private void validateAIResponse(Map<String, Object> response) {
        List<String> requiredFields = Arrays.asList("manipulationProbability", "retailSentiment", "whaleActivity", "riskLevel");
        
        for (String field : requiredFields) {
            if (!response.containsKey(field)) {
                throw new IllegalArgumentException("Campo obrigatório ausente na resposta da IA: " + field);
            }
        }
        
        // Validar enumerações
        String sentiment = (String) response.get("retailSentiment");
        List<String> validSentiments = Arrays.asList("Extreme_Fear", "Fear", "Neutral", "Greed", "Extreme_Greed");
        if (!validSentiments.contains(sentiment)) {
            throw new IllegalArgumentException("Sentimento inválido: " + sentiment);
        }
        
        String whaleActivity = (String) response.get("whaleActivity");
        List<String> validWhaleActivity = Arrays.asList("None", "Light", "Moderate", "Heavy", "Extreme");
        if (!validWhaleActivity.contains(whaleActivity)) {
            throw new IllegalArgumentException("Atividade de whale inválida: " + whaleActivity);
        }
    }

    private BehavioralAnalysis getFallbackAnalysis(OrderFlow orderFlow) {
        System.err.println("Usando análise de fallback para " + orderFlow.getSymbol());
        
        List<String> patterns = Collections.singletonList("FALLBACK_ANALYSIS");
        List<String> recommendations = Collections.singletonList("⚠️ ANÁLISE LIMITADA - VERIFICAR CONEXÃO COM IA");
        
        return new BehavioralAnalysis(
            0.0,
            "Neutral",
            "None",
            50.0,
            0.0,
            patterns,
            recommendations,
            0.0,
            0.0
        );
    }

    private String generateCacheKey(OrderFlow orderFlow) {
        String timestamp = orderFlow.getTimestamp();
        // Arredondar para minutos
        long minutes;
        try {
            minutes = Instant.parse(timestamp).toEpochMilli() / 60000;
        } catch (Exception e) {
            minutes = System.currentTimeMillis() / 60000;
        }
        return orderFlow.getSymbol() + "_" + minutes + "_" + 
               String.format("%.0f", orderFlow.getVolume()) + "_" + 
               String.format("%.4f", orderFlow.getPrice());
    }

    private List<HistoricalPattern> analyzeHistoricalPatterns(String symbol) {
        return historicalPatterns.stream()
            .filter(p -> extractSymbolFromPattern(p).equals(symbol))
            .limit(10)
            .collect(Collectors.toList());
    }

    private String extractSymbolFromPattern(HistoricalPattern pattern) {
        // Implementar lógica para extrair símbolo do padrão
        return "UNKNOWN";
    }
}

// ==================== CLASSE SIMULADA DO GOOGLE GEN AI ====================

class GoogleGenAI {
    private String apiKey;

    public GoogleGenAI(String apiKey) {
        this.apiKey = apiKey;
    }

    public Map<String, Object> generateContent(String prompt, AnalysisConfig config) {
        // Simulação da resposta da IA
        Map<String, Object> result = new HashMap<>();
        result.put("manipulationProbability", 45.0);
        result.put("retailSentiment", "Neutral");
        result.put("whaleActivity", "Moderate");
        result.put("riskLevel", 55.0);
        result.put("confidence", 85.0);
        
        List<String> patterns = Arrays.asList("ORDER_BOOK_IMBALANCE", "WHALE_ACTIVITY");
        result.put("detectedPatterns", patterns);
        result.put("anomalyScore", 35.0);
        
        return result;
    }
}

class RiskLevel {
    private int min;
    private int max;
    private String color;

    public RiskLevel(int min, int max, String color) {
        this.min = min;
        this.max = max;
        this.color = color;
    }

    public int getMin() { return min; }
    public int getMax() { return max; }
    public String getColor() { return color; }
}

// ==================== FUNÇÕES UTILITÁRIAS ====================

class AnalysisUtils {
    
    /**
     * Utilitário para formatar análise para exibição
     */
    public static String formatAnalysis(BehavioralAnalysis analysis) {
        StringBuilder sb = new StringBuilder();
        sb.append("\n📊 ANÁLISE COMPORTAMENTAL\n");
        sb.append("────────────────────────\n");
        sb.append(String.format("🔍 Probabilidade de Manipulação: %.1f%%\n", analysis.getManipulationProbability()));
        sb.append(String.format("😊 Sentimento Retail: %s\n", analysis.getRetailSentiment().replace('_', ' ')));
        sb.append(String.format("🐋 Atividade Whale: %s\n", analysis.getWhaleActivity()));
        sb.append(String.format("⚠️  Nível de Risco: %.1f%% (%s)\n", analysis.getRiskLevel(), getRiskCategory(analysis.getRiskLevel())));
        sb.append(String.format("📈 Confiança: %.1f%%\n", analysis.getConfidence()));
        sb.append(String.format("🎯 Anomalia: %.1f%%\n", analysis.getAnomalyScore()));
        sb.append(String.format("💧 Impacto na Liquidez: %.1f%%\n\n", analysis.getLiquidityImpact()));
        
        sb.append("📋 PADRÕES DETECTADOS:\n");
        for (String pattern : analysis.getPatterns()) {
            sb.append("• ").append(pattern).append("\n");
        }
        
        sb.append("\n💡 RECOMENDAÇÕES:\n");
        for (String rec : analysis.getRecommendations()) {
            sb.append("• ").append(rec).append("\n");
        }
        
        return sb.toString();
    }

    private static String getRiskCategory(double riskLevel) {
        if (riskLevel <= 30) return "BAIXO";
        if (riskLevel <= 60) return "MÉDIO";
        if (riskLevel <= 85) return "ALTO";
        return "EXTREMO";
    }
}

// ==================== MARKET MONITOR ====================

class MarketMonitor {
    private BehavioralAnalytics analytics;
    private Set<String> monitoredSymbols;
    private ScheduledExecutorService scheduler;
    private ScheduledFuture<?> scheduledTask;

    public MarketMonitor() {
        this.analytics = new BehavioralAnalytics();
        this.monitoredSymbols = Collections.newSetFromMap(new ConcurrentHashMap<>());
        this.scheduler = Executors.newScheduledThreadPool(1);
        
        // Configurar listeners
        analytics.addListener(event -> {
            switch (event.getType()) {
                case "analysisCompleted":
                    System.out.println("✅ Análise concluída para " + event.getData().get("symbol"));
                    BehavioralAnalysis analysis = (BehavioralAnalysis) event.getData().get("analysis");
                    System.out.println(AnalysisUtils.formatAnalysis(analysis));
                    break;
                case "analysisError":
                    System.err.println("❌ Erro na análise: " + event.getData().get("symbol") + 
                                       " - " + event.getData().get("error"));
                    break;
            }
        });
    }

    public void addSymbol(String symbol) {
        monitoredSymbols.add(symbol);
        System.out.println("➕ Símbolo adicionado: " + symbol);
    }

    public void removeSymbol(String symbol) {
        monitoredSymbols.remove(symbol);
        System.out.println("➖ Símbolo removido: " + symbol);
    }

    public void startMonitoring(long intervalMs) {
        if (scheduledTask != null && !scheduledTask.isDone()) {
            System.err.println("⚠️ Monitoramento já está em execução");
            return;
        }

        System.out.println("🚀 Iniciando monitoramento (intervalo: " + intervalMs + "ms)");
        
        scheduledTask = scheduler.scheduleAtFixedRate(() -> {
            // Aqui você implementaria a coleta de dados em tempo real
            System.out.println("📡 Coletando dados do mercado...");
            
            // Exemplo simulado
            for (String symbol : monitoredSymbols) {
                try {
                    OrderFlow mockOrderFlow = generateMockOrderFlow(symbol);
                    analytics.analyzeBehavior(mockOrderFlow);
                } catch (Exception e) {
                    System.err.println("Erro ao analisar " + symbol + ": " + e.getMessage());
                }
            }
        }, 0, intervalMs, TimeUnit.MILLISECONDS);
    }

    public void stopMonitoring() {
        if (scheduledTask != null) {
            scheduledTask.cancel(false);
            scheduledTask = null;
            System.out.println("🛑 Monitoramento parado");
        }
    }

    public void shutdown() {
        stopMonitoring();
        scheduler.shutdown();
        try {
            if (!scheduler.awaitTermination(5, TimeUnit.SECONDS)) {
                scheduler.shutdownNow();
            }
        } catch (InterruptedException e) {
            scheduler.shutdownNow();
        }
    }

    private OrderFlow generateMockOrderFlow(String symbol) {
        Random rand = new Random();
        
        List<OrderLevel> bids = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            bids.add(new OrderLevel(100 - i * 0.1, rand.nextDouble() * 100, rand.nextInt(10)));
        }
        
        List<OrderLevel> asks = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            asks.add(new OrderLevel(100 + i * 0.1, rand.nextDouble() * 100, rand.nextInt(10)));
        }
        
        List<Trade> trades = new ArrayList<>();
        for (int i = 0; i < 20; i++) {
            trades.add(new Trade(
                "trade_" + i,
                99.5 + rand.nextDouble() * 1,
                rand.nextDouble() * 50,
                Instant.now().minusSeconds(i * 1000).toString(),
                rand.nextDouble() > 0.5 ? "buy" : "sell",
                rand.nextDouble() > 0.8
            ));
        }
        
        return new OrderFlow(
            Instant.now().toString(),
            symbol,
            bids,
            asks,
            trades,
            10000 + rand.nextDouble() * 5000,
            100,
            0.1,
            1000
        );
    }
}

// ==================== CLASSE PRINCIPAL DE EXEMPLO ====================

public class BehavioralAnalyticsApp {
    public static void main(String[] args) {
        System.out.println("=== SISTEMA DE ANÁLISE COMPORTAMENTAL ===\n");
        
        try {
            // Exemplo 1: Análise única
            System.out.println("📊 Exemplo 1: Análise única");
            BehavioralAnalytics analytics = new BehavioralAnalytics();
            MarketMonitor monitor = new MarketMonitor();
            
            OrderFlow orderFlow = monitor.generateMockOrderFlow("BTCUSDT");
            BehavioralAnalysis analysis = analytics.analyzeBehavior(orderFlow);
            System.out.println(AnalysisUtils.formatAnalysis(analysis));
            
            // Exemplo 2: Monitoramento em tempo real
            System.out.println("\n🚀 Exemplo 2: Monitoramento em tempo real");
            MarketMonitor realTimeMonitor = new MarketMonitor();
            realTimeMonitor.addSymbol("BTCUSDT");
            realTimeMonitor.addSymbol("ETHUSDT");
            realTimeMonitor.startMonitoring(30000); // Atualizar a cada 30 segundos
            
            // Exemplo 3: Análise em batch
            System.out.println("\n📦 Exemplo 3: Análise em batch");
            List<OrderFlow> batchFlows = Arrays.asList(
                monitor.generateMockOrderFlow("BTCUSDT"),
                monitor.generateMockOrderFlow("ETHUSDT"),
                monitor.generateMockOrderFlow("SOLUSDT")
            );
            
            Map<String, BehavioralAnalysis> batchAnalysis = analytics.analyzeBatch(batchFlows);
            for (Map.Entry<String, BehavioralAnalysis> entry : batchAnalysis.entrySet()) {
                System.out.println("\n--- " + entry.getKey() + " ---");
                System.out.println(AnalysisUtils.formatAnalysis(entry.getValue()));
            }
            
            // Exemplo 4: Obter estatísticas históricas
            System.out.println("\n📈 Exemplo 4: Estatísticas históricas");
            HistoricalStats stats = analytics.getHistoricalStats("BTCUSDT");
            System.out.println("Total de análises: " + stats.getTotalAnalyses());
            System.out.println("Risco médio: " + String.format("%.2f%%", stats.getAverageRisk()));
            
            // Manter o monitoramento rodando por um tempo
            System.out.println("\n⏱️ Monitoramento rodando por 10 segundos...");
            Thread.sleep(10000);
            
            // Parar monitoramento
            realTimeMonitor.stopMonitoring();
            realTimeMonitor.shutdown();
            
            System.out.println("\n✅ Demonstração concluída!");
            
        } catch (Exception e) {
            System.err.println("Erro na execução: " + e.getMessage());
            e.printStackTrace();
        }
    }
}