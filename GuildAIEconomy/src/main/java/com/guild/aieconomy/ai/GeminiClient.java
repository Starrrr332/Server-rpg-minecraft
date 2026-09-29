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
        return apiKey != null && !apiKey.isBlank() && !apiKey.equals("TU_GEMINI_API_KEY_AQUI");
    }

    public CompletableFuture<String> askMerchant(String systemPrompt, String playerMessage) {
        if (!isConfigured()) {
            return CompletableFuture.completedFuture("¡Hola! Soy el Mercader del Gremio. (Configura mi API Key de Gemini en config.yml para hablar con IA)");
        }

        JsonObject root = new JsonObject();
        
        // System instruction
        JsonObject systemInstruction = new JsonObject();
        JsonArray sysParts = new JsonArray();
        JsonObject sysPart = new JsonObject();
        sysPart.addProperty("text", systemPrompt);
        sysParts.add(sysPart);
        systemInstruction.add("parts", sysParts);
        root.add("systemInstruction", systemInstruction);

        // Contents
        JsonArray contents = new JsonArray();
        JsonObject contentObj = new JsonObject();
        JsonArray parts = new JsonArray();
        JsonObject textPart = new JsonObject();
        textPart.addProperty("text", playerMessage);
        parts.add(textPart);
        contentObj.add("parts", parts);
        contents.add(contentObj);
        root.add("contents", contents);

        // Generation config
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
                        return "El mercado está agitado hoy... (Error IA: " + response.statusCode() + ")";
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
                    return "¡Salud, aventurero! ¿Deseas comerciar con el Gremio?";
                })
                .exceptionally(ex -> "No pude comunicarme con los dioses del mercado en este momento.");
    }
}
