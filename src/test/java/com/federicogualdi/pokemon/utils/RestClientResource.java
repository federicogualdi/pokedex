package com.federicogualdi.pokemon.utils;

import com.github.tomakehurst.wiremock.WireMockServer;
import io.quarkus.test.common.QuarkusTestResourceLifecycleManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.HashMap;
import java.util.Map;

import static com.github.tomakehurst.wiremock.client.WireMock.*;

public class RestClientResource implements QuarkusTestResourceLifecycleManager {
    private final static Logger logger = LoggerFactory.getLogger(RestClientResource.class);

    public static WireMockServer wireMockServer;

    @Override
    public Map<String, String> start() {
        wireMockServer = new WireMockServer();
        wireMockServer.start();

        logger.info("Starting rest client mock server on {}.", wireMockServer.baseUrl());

        // PokeApi
        stubFor(get(urlEqualTo("/pokeapi/v2/pokemon-species/pikachu/"))
                .willReturn(aResponse()
                        .withHeader("Content-Type", "application/json")
                        .withBody(ResourceUtils.getResource("pokeapi/pikachu.json"))));
        stubFor(get(urlEqualTo("/pokeapi/v2/pokemon-species/mewtwo/"))
                .willReturn(aResponse()
                        .withHeader("Content-Type", "application/json")
                        .withBody(ResourceUtils.getResource("pokeapi/mewtwo.json"))));
        stubFor(get(urlEqualTo("/pokeapi/v2/pokemon-species/bulbasaur/"))
                .willReturn(aResponse()
                        .withHeader("Content-Type", "application/json")
                        .withBody(ResourceUtils.getResource("pokeapi/bulbasaur.json"))));


        // FunTranslations
        /// Pikachu
        stubFor(post(urlEqualTo("/funtranslations/translate/shakespeare"))
                .withRequestBody(equalTo("{\"text\":\"When several of these POKéMON gather, their electricity could build and cause lightning storms.\"}"))
                .willReturn(aResponse()
                        .withHeader("Content-Type", "application/json")
                        .withBody(ResourceUtils.getResource("funtranslations/shakespeare.pikachu-description.json"))));
        stubFor(post(urlEqualTo("/funtranslations/translate/yoda"))
                .withRequestBody(equalTo("{\"text\":\"When several of these POKéMON gather, their electricity could build and cause lightning storms.\"}"))
                .willReturn(aResponse()
                        .withHeader("Content-Type", "application/json")
                        .withBody(ResourceUtils.getResource("funtranslations/yoda.pikachu-description.json"))));

        /// Mewtwo
        stubFor(post(urlEqualTo("/funtranslations/translate/shakespeare"))
                .withRequestBody(equalTo("{\"text\":\"It was created by a scientist after years of horrific gene splicing and DNA engineering experiments.\"}"))
                .willReturn(aResponse()
                        .withHeader("Content-Type", "application/json")
                        .withBody(ResourceUtils.getResource("funtranslations/shakespeare.mewtwo-description.json"))));
        stubFor(post(urlEqualTo("/funtranslations/translate/yoda"))
                .withRequestBody(equalTo("{\"text\":\"It was created by a scientist after years of horrific gene splicing and DNA engineering experiments.\"}"))
                .willReturn(aResponse()
                        .withHeader("Content-Type", "application/json")
                        .withBody(ResourceUtils.getResource("funtranslations/yoda.mewtwo-description.json"))));


        Map<String, String> props = new HashMap<>();
        props.put("com.federicogualdi.pokemon.pokedex.rest.client.PokeApiServiceRest/mp-rest/url", wireMockServer.baseUrl() + "/pokeapi");
        props.put("com.federicogualdi.pokemon.pokedex.rest.client.FuntranslationsServiceRest/mp-rest/url", wireMockServer.baseUrl() + "/funtranslations");
        return props;
    }

    @Override
    public void stop() {
        if (wireMockServer != null) {
            wireMockServer.stop();
        }
    }
}
