package com.federicogualdi.pokemon.rest;

import com.federicogualdi.pokemon.utils.RestClientResource;
import io.quarkus.test.common.QuarkusTestResource;
import io.quarkus.test.junit.QuarkusTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;

@QuarkusTest
@QuarkusTestResource(RestClientResource.class)
public class PokedexRestTest {

    @Test
    @Tag("pokemon")
    @DisplayName("Should get pokemon.")
    public void testGetPokemonByNameEndpoint() {
        String pokemonName = "pikachu";
        given()
                .pathParam("name", pokemonName)
                .when().get("/api/v1/pokemon/{name}")
                .then()
                .statusCode(200)
                .body("name", is(pokemonName));
    }

    @Test
    @Tag("pokemon")
    @DisplayName("Should fail when pokemon name is blank.")
    public void testGetPokemonByNameBlankEndpoint() {
        String pokemonName = " ";
        given()
                .pathParam("name", pokemonName)
                .when().get("/api/v1/pokemon/{name}")
                .then()
                .statusCode(400);
    }

    @Test
    @Tag("pokemon")
    @DisplayName("Should fail when pokemon is not found.")
    public void testGetPokemonByNameNotFoundEndpoint() {
        String pokemonName = "NOT_EXISTING_POKEMON";
        given()
                .pathParam("name", pokemonName)
                .when().get("/api/v1/pokemon/{name}")
                .then()
                .statusCode(404);
    }

    @Test
    @Tag("translated-pokemon")
    @DisplayName("Should get pokemon with funny description.")
    public void testGetTranslatedPokemonByNameEndpoint() {
        String pokemonName = "mewtwo";
        given()
                .pathParam("name", pokemonName)
                .when().get("/api/v1/pokemon/translated/{name}")
                .then()
                .statusCode(200)
                .body("name", is(pokemonName));
    }

    @Test
    @Tag("translated-pokemon")
    @DisplayName("Should fail when translated pokemon name is blank.")
    public void testGetTranslatedPokemonByNameBlankEndpoint() {
        String pokemonName = " ";
        given()
                .pathParam("name", pokemonName)
                .when().get("/api/v1/pokemon/{name}")
                .then()
                .statusCode(400);
    }

    @Test
    @Tag("translated-pokemon")
    @DisplayName("Should fail when pokemon is not found.")
    public void testGetTranslatedPokemonByNameNotFoundEndpoint() {
        String pokemonName = "NOT_EXISTING_POKEMON";
        given()
                .pathParam("name", pokemonName)
                .when().get("/api/v1/pokemon/translated/{name}")
                .then()
                .statusCode(404);
    }
}