package com.federicogualdi.pokemon;

import io.quarkus.test.junit.QuarkusTest;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;

@QuarkusTest
public class PokedexResourceTest {

    @Test
    public void testGetPokemonByNameEndpoint() {
        String pokemonName = "mewtwo";
        given()
                .pathParam("name", pokemonName)
                .when().get("/api/v1/pokemon/{name}")
                .then()
                .statusCode(200)
                .body("name", is(pokemonName));
    }

    @Test
    public void testGetPokemonByNameNotFoundEndpoint() {
        String pokemonName = "ABC";
        given()
                .pathParam("name", pokemonName)
                .when().get("/api/v1/pokemon/{name}")
                .then()
                .statusCode(404);
    }

    @Test
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
    public void testGetTranslatedPokemonByNameNotFoundEndpoint() {
        String pokemonName = "ABC";
        given()
                .pathParam("name", pokemonName)
                .when().get("/api/v1/pokemon/translated/{name}")
                .then()
                .statusCode(404);
    }
}