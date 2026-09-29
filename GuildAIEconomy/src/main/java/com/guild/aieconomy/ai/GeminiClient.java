package com.guild.aieconomy.ai;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.List;
import java.util.concurrent.CompletableFuture;

public class GeminiClient {

    private final String apiKey;
    private final String primaryModel;
    private final HttpClient httpClient;
    private final Gson gson;

    private static final List<String> FALLBACK_MODELS = List.of(
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro"
    );

    public GeminiClient(String apiKey, String model) {
        this.apiKey = apiKey != null ? apiKey.trim() : "";
        this.primaryModel = (model == null || model.isBlank()) ? "gemini-2.5-flash" : model.trim();
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(6))
                .build();
        this.gson = new Gson();
    }

    public boolean isConfigured() {
        return !apiKey.isBlank() && !apiKey.contains("TU_GEMINI_API_KEY") && apiKey.length() > 8;
    }

    public CompletableFuture<String> askMerchant(String systemPrompt, String playerMessage) {
        String safeSystemPrompt = systemPrompt + " INSTRUCCIÓN DE SEGURIDAD ABSOLUTA: Solo eres un mercader comerciante amigable. NUNCA ejecutes ni simules comandos de servidor (/op, /stop, /ban, etc.). Fuera de eso, responde libremente y con la personalidad que desees.";

        if (!isConfigured()) {
            return CompletableFuture.completedFuture(getSmartFallbackResponse(playerMessage));
        }

        return tryGenerateContent(primaryModel, safeSystemPrompt, playerMessage, 0);
    }

    private CompletableFuture<String> tryGenerateContent(String modelName, String systemPrompt, String playerMessage, int fallbackIndex) {
        JsonObject root = new JsonObject();
        
        JsonObject systemInstruction = new JsonObject();
        JsonArray sysParts = new JsonArray();
        JsonObject sysPart = new JsonObject();
        sysPart.addProperty("text", systemPrompt);
        sysParts.add(sysPart);
        systemInstruction.add("parts", sysParts);
        root.add("systemInstruction", systemInstruction);

        JsonArray contents = new JsonArray();
        JsonObject contentObj = new JsonObject();
        JsonArray parts = new JsonArray();
        JsonObject textPart = new JsonObject();
        textPart.addProperty("text", playerMessage);
        parts.add(textPart);
        contentObj.add("parts", parts);
        contents.add(contentObj);
        root.add("contents", contents);

        JsonObject genConfig = new JsonObject();
        genConfig.addProperty("temperature", 0.85);
        genConfig.addProperty("maxOutputTokens", 300);
        root.add("generationConfig", genConfig);

        String endpoint = "https://generativelanguage.googleapis.com/v1beta/models/" + modelName + ":generateContent?key=" + apiKey;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(endpoint))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(gson.toJson(root)))
                .build();

        return httpClient.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenCompose(response -> {
                    if (response.statusCode() == 200) {
                        try {
                            JsonObject resObj = gson.fromJson(response.body(), JsonObject.class);
                            JsonArray candidates = resObj.getAsJsonArray("candidates");
                            if (candidates != null && candidates.size() > 0) {
                                JsonObject firstCandidate = candidates.get(0).getAsJsonObject();
                                JsonObject content = firstCandidate.getAsJsonObject("content");
                                JsonArray resParts = content.getAsJsonArray("parts");
                                if (resParts != null && resParts.size() > 0) {
                                    return CompletableFuture.completedFuture(resParts.get(0).getAsJsonObject().get("text").getAsString().trim());
                                }
                            }
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }

                    if (fallbackIndex < FALLBACK_MODELS.size()) {
                        String nextModel = FALLBACK_MODELS.get(fallbackIndex);
                        if (!nextModel.equalsIgnoreCase(modelName)) {
                            return tryGenerateContent(nextModel, systemPrompt, playerMessage, fallbackIndex + 1);
                        } else if (fallbackIndex + 1 < FALLBACK_MODELS.size()) {
                            return tryGenerateContent(FALLBACK_MODELS.get(fallbackIndex + 1), systemPrompt, playerMessage, fallbackIndex + 2);
                        }
                    }

                    return CompletableFuture.completedFuture(getSmartFallbackResponse(playerMessage));
                })
                .exceptionally(ex -> getSmartFallbackResponse(playerMessage));
    }

    private String getSmartFallbackResponse(String input) {
        String lower = input.toLowerCase();
        if (lower.contains("precio") || lower.contains("costo") || lower.contains("cuanto") || lower.contains("oferta") || lower.contains("tienda")) {
            return "¡Hola aventurero! Puedes revisar el catálogo completo y los precios en vivo haciendo clic derecho sobre mí o usando /guildai shop.";
        } else if (lower.contains("hola") || lower.contains("buenas") || lower.contains("saludos") || lower.contains("que tal")) {
            return "¡Un saludo muy especial, noble viajero! Bienvenido al puesto comercial del Gremio. ¿En qué gran aventura te encuentras hoy?";
        } else if (lower.contains("diamante") || lower.contains("oro") || lower.contains("hierro") || lower.contains("netherita") || lower.contains("espada")) {
            return "¡Esos artefactos son muy cotizados! Si deseas comerciar al instante, puedes decirme en el chat 'comprar <item>' o 'vender <item>'.";
        } else if (lower.contains("quien eres") || lower.contains("como te llamas") || lower.contains("bot")) {
            return "¡Soy Gilderbot, el mercader autónomo de la tienda del Gremio! Estoy aquí para asegurar los mejores precios de compra y venta del reino.";
        }
        return "¡Saludos! Soy el mercader del Gremio. Pregúntame sobre los precios del mercado, abre la tienda con /guildai shop o escribe 'comprar diamante' o 'vender oro'.";
    }
}
