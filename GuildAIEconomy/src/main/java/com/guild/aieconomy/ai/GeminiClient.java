package com.guild.aieconomy.ai;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.concurrent.CompletableFuture;

public class GeminiClient {

    private final String apiKey;
    private final String model;
    private final HttpClient httpClient;
    private final Gson gson;

    public GeminiClient(String apiKey, String model) {
        this.apiKey = apiKey;
        this.model = (model == null || model.isBlank()) ? "gemini-1.5-flash" : model;
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(5))
                .build();
        this.gson = new Gson();
    }

    public boolean isConfigured() {
        return apiKey != null && !apiKey.isBlank() && apiKey.startsWith("AIzaSy");
    }

    public CompletableFuture<String> askMerchant(String systemPrompt, String playerMessage) {
        if (!isConfigured()) {
            return CompletableFuture.completedFuture(getSmartFallbackResponse(playerMessage));
        }

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
        genConfig.addProperty("temperature", 0.7);
        genConfig.addProperty("maxOutputTokens", 150);
        root.add("generationConfig", genConfig);

        String endpoint = "https://generativelanguage.googleapis.com/v1beta/models/" + model + ":generateContent?key=" + apiKey;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(endpoint))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(gson.toJson(root)))
                .build();

        return httpClient.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(response -> {
                    if (response.statusCode() != 200) {
                        return getSmartFallbackResponse(playerMessage);
                    }
                    try {
                        JsonObject resObj = gson.fromJson(response.body(), JsonObject.class);
                        JsonArray candidates = resObj.getAsJsonArray("candidates");
                        if (candidates != null && candidates.size() > 0) {
                            JsonObject firstCandidate = candidates.get(0).getAsJsonObject();
                            JsonObject content = firstCandidate.getAsJsonObject("content");
                            JsonArray resParts = content.getAsJsonArray("parts");
                            if (resParts != null && resParts.size() > 0) {
                                return resParts.get(0).getAsJsonObject().get("text").getAsString().trim();
                            }
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    return getSmartFallbackResponse(playerMessage);
                })
                .exceptionally(ex -> getSmartFallbackResponse(playerMessage));
    }

    private String getSmartFallbackResponse(String input) {
        String lower = input.toLowerCase();
        if (lower.contains("precio") || lower.contains("costo") || lower.contains("cuanto") || lower.contains("oferta")) {
            return "¡Revisa la tienda con clic derecho sobre mí o usa /guildai shop para ver los precios actualizados del mercado!";
        } else if (lower.contains("hola") || lower.contains("buenas") || lower.contains("saludos")) {
            return "¡Salud, aventurero! Bienvenido a las arcas del Gremio. ¿Vienes a comerciar o a vender tus tesoros?";
        } else if (lower.contains("diamante") || lower.contains("oro") || lower.contains("hierro")) {
            return "¡Los minerales valiosos siempre están en alta demanda en nuestro Gremio! Revisa el stock en el cofre.";
        }
        return "¡Bienvenido a la tienda del Gremio! Usa clic derecho sobre mí o escribe /guildai shop para hacer negocios.";
    }
}
