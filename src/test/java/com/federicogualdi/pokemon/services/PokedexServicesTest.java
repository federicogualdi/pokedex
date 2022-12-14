package com.federicogualdi.pokemon.services;

import com.federicogualdi.pokemon.pokedex.services.PokedexService;
import com.federicogualdi.pokemon.utils.RestClientResource;
import io.quarkus.test.common.QuarkusTestResource;
import io.quarkus.test.junit.QuarkusTest;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import javax.inject.Inject;
import javax.ws.rs.BadRequestException;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.Response;

import static org.junit.jupiter.api.Assertions.*;

@QuarkusTest
@QuarkusTestResource(RestClientResource.class)
public class PokedexServicesTest {

    @Inject
    PokedexService pokedexService;

    @Test
    @Tag("pokedex-service")
    @DisplayName("Should get pokemon by name.")
    void getPokemonByName() {
        String pokemonName = "pikachu";
        var pokemon = pokedexService.getByName(pokemonName);

        assertAll(
                () -> Assertions.assertEquals("pikachu", pokemon.getName()),
                () -> Assertions.assertEquals("When several of these POKéMON gather, their electricity could build and cause lightning storms.", pokemon.getDescription()),
                () -> Assertions.assertEquals("forest", pokemon.getHabitat()),
                () -> Assertions.assertEquals(false, pokemon.isLegendary())
        );
    }

    @Test
    @Tag("pokedex-service")
    @DisplayName("Should get translated pokemon by name")
    void getTranslatedPokemonByName() {
        String pokemonName = "mewtwo";
        var pokemon = pokedexService.getByNameWithTranslatedDescription(pokemonName);

        assertAll(
                () -> Assertions.assertEquals("mewtwo", pokemon.getName()),
                () -> Assertions.assertEquals("Created by a scientist after years of horrific gene splicing and dna engineering experiments, it was.", pokemon.getDescription()),
                () -> Assertions.assertEquals("rare", pokemon.getHabitat()),
                () -> Assertions.assertEquals(true, pokemon.isLegendary())
        );
    }

    @Test
    @Tag("pokedex-service")
    @DisplayName("Should fail when is requested pokemon by blank name.")
    void getPokemonByBlankName() {
        String emptyName = "";
        String notUsefulName = " ";

        assertThrows(
                BadRequestException.class,
                () -> pokedexService.getByName(emptyName)
        );
        assertThrows(
                BadRequestException.class,
                () -> pokedexService.getByName(notUsefulName)
        );
    }

    @Test
    @Tag("pokedex-service")
    @DisplayName("Ensure that 'pokemon' is different from 'translated pokemon'")
    void ensurePokemonIsDifferentFromTranslatedPokemon() {
        String pokemonName = "mewtwo";
        var pokemon = pokedexService.getByName(pokemonName);
        var pokemonTranslated = pokedexService.getByNameWithTranslatedDescription(pokemonName);

        Assertions.assertNotEquals(pokemon, pokemonTranslated);
    }

    @Test
    @Tag("pokedex-service")
    @DisplayName("Ensure that space or capital letter in pokemon name returns the same pokemon")
    void ensurePokemonNameFormattingIsNotImportant() {
        String pokemonName = "mewtwo";
        String badlyFormattedName = " mewTwo    ";

        var pokemon = pokedexService.getByName(pokemonName);
        var pokemonBadlyFormatted = pokedexService.getByName(badlyFormattedName);
        Assertions.assertEquals(pokemon, pokemonBadlyFormatted);

        var pokemonTranslated = pokedexService.getByNameWithTranslatedDescription(pokemonName);
        var pokemonTranslatedBadlyFormatted = pokedexService.getByNameWithTranslatedDescription(badlyFormattedName);
        Assertions.assertEquals(pokemonTranslated, pokemonTranslatedBadlyFormatted);
    }

    @Test
    @Tag("pokedex-service")
    @DisplayName("Should fallback with normal pokemon when translating services can't translate")
    void fallingbackThirdPartyServicesError() {
        String pokemonName = "bulbasaur";
        var pokemon = pokedexService.getByName(pokemonName);
        var pokemonFallingBack = pokedexService.getByNameWithTranslatedDescription(pokemonName);

        // Bulbasaur is mapped as 429 error for FunTranslations endpoint
        WebApplicationException exception = assertThrows(
                WebApplicationException.class,
                () -> pokedexService.getTranslatedPokemon(pokemonName)
        );

        // Ensure that 429 is coming back from FunTranslations
        assertEquals(exception.getResponse().getStatus(), Response.Status.TOO_MANY_REQUESTS.getStatusCode());

        // Ensure that 'pokemon' and 'falling-back pokemon' are equals
        assertAll(
                () -> Assertions.assertNotSame(pokemon, pokemonFallingBack),
                () -> Assertions.assertEquals(pokemon, pokemonFallingBack)
        );
    }
}
