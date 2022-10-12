package com.federicogualdi.pokemon.pokedex.api.rest.converter;

import com.federicogualdi.pokemon.pokedex.api.rest.FuntranslationsServiceRest;
import com.federicogualdi.pokemon.pokedex.messages.rest.dto.FunTranslationsRequestDto;
import com.federicogualdi.pokemon.pokedex.messages.rest.dto.PokeApiPokemonDto;
import com.federicogualdi.pokemon.pokedex.messages.rest.dto.PokeApiPokemonFlavorTextEntriesDto;
import com.federicogualdi.pokemon.pokedex.messages.rest.dto.PokemonDto;
import org.eclipse.microprofile.rest.client.inject.RestClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;

@ApplicationScoped
public class PokemonConverter {

    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    @Inject
    @RestClient
    FuntranslationsServiceRest translatorService;

    public PokemonDto fromPokeAPi(PokeApiPokemonDto pokemonPokeApi) {
        PokemonDto pokemonConverted = new PokemonDto();
        pokemonConverted.name = pokemonPokeApi.name;
        pokemonConverted.habitat = pokemonPokeApi.habitat.name;
        pokemonConverted.isLegendary = pokemonPokeApi.isLegendary;

        if (!pokemonPokeApi.flavorTextEntries.isEmpty()) {
            pokemonConverted.description = pokemonPokeApi.flavorTextEntries.stream().filter(PokeApiPokemonFlavorTextEntriesDto::isEnglish).findFirst().map(d -> d.flavorText.replaceAll("\\n", " ").replaceAll("\\f", " ")).orElse(null);
        }

        logger.debug("Converted PokeAPiPokemon '{}' in Pokemon: {}", pokemonPokeApi.name, pokemonConverted);
        return pokemonConverted;
    }

    public PokemonDto toYodaTranslation(PokemonDto pokemonDto) {
        return applyYodaTranslation(pokemonDto);
    }

    public PokemonDto toShakespeareTranslation(PokemonDto pokemonDto) {
        return applyShakespeareTranslation(pokemonDto);
    }

    private PokemonDto applyYodaTranslation(PokemonDto pokemonDto) {
        pokemonDto.description = translatorService.yodaTranslation(new FunTranslationsRequestDto(pokemonDto.description)).contents.translated;
        logger.info("Applied Yoda-Translation to '{}': {}", pokemonDto.name, pokemonDto);
        return pokemonDto;
    }

    private PokemonDto applyShakespeareTranslation(PokemonDto pokemonDto) {
        pokemonDto.description = translatorService.shakespeareTranslation(new FunTranslationsRequestDto(pokemonDto.description)).contents.translated;
        logger.info("Applied Shakespeare-Translation to '{}': {}", pokemonDto.name, pokemonDto);
        return pokemonDto;
    }
}
