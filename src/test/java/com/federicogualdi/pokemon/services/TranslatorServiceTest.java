package com.federicogualdi.pokemon.services;

import com.federicogualdi.pokemon.pokedex.rest.dto.FunTranslationsDto;
import com.federicogualdi.pokemon.pokedex.rest.dto.PokemonDto;
import com.federicogualdi.pokemon.pokedex.services.PokedexService;
import com.federicogualdi.pokemon.pokedex.services.TranslatorService;
import com.federicogualdi.pokemon.utils.ResourceUtils;
import com.federicogualdi.pokemon.utils.RestClientResource;
import io.quarkus.test.common.QuarkusTestResource;
import io.quarkus.test.junit.QuarkusTest;
import io.vertx.core.json.Json;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import javax.inject.Inject;

import static org.junit.jupiter.api.Assertions.assertAll;

@QuarkusTest
@QuarkusTestResource(RestClientResource.class)
public class TranslatorServiceTest {

    @Inject
    TranslatorService translatorService;

    @Inject
    PokedexService pokedexService;

    @Test
    @Tag("translator-service")
    @DisplayName("Should apply shakespeare translation.")
    void applyShakespeareTranslationToPokemon() {
        var pokemon = pokedexService.getByName("pikachu");
        var pokemonTranslated = translatorService.applyShakespeareTranslation(pokemon);

        var shakespeareTranslations = Json.decodeValue(
                ResourceUtils.getResource(String.format("funtranslations/shakespeare.%s-description.json", pokemon.getName())),
                FunTranslationsDto.class);


        assertAll(
                () -> Assertions.assertNotEquals(pokemon.getDescription(), pokemonTranslated.getDescription()),
                () -> Assertions.assertEquals(pokemonTranslated.getDescription(), shakespeareTranslations.contents.getTranslated())
        );
    }

    @Test
    @Tag("translator-service")
    @DisplayName("Should apply yoda translation.")
    void applyYodaTranslationToPokemon() {
        var pokemon = pokedexService.getByName("mewtwo");
        var pokemonTranslated = translatorService.applyYodaTranslation(pokemon);

        var yodaTranslations = Json.decodeValue(
                ResourceUtils.getResource(String.format("funtranslations/yoda.%s-description.json", pokemon.getName())),
                FunTranslationsDto.class);


        assertAll(
                () -> Assertions.assertNotEquals(pokemon.getDescription(), pokemonTranslated.getDescription()),
                () -> Assertions.assertEquals(pokemonTranslated.getDescription(), yodaTranslations.contents.getTranslated())
        );
    }

}
