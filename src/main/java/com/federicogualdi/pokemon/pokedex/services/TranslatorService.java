package com.federicogualdi.pokemon.pokedex.services;

import com.federicogualdi.pokemon.pokedex.rest.client.FuntranslationsServiceRest;
import com.federicogualdi.pokemon.pokedex.rest.dto.FunTranslationsRequestDto;
import com.federicogualdi.pokemon.pokedex.rest.dto.PokemonDto;
import org.eclipse.microprofile.rest.client.inject.RestClient;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;

@ApplicationScoped
public class TranslatorService {

    @Inject
    @RestClient
    FuntranslationsServiceRest funtranslationsServiceRest;

    public PokemonDto applyYodaTranslation(PokemonDto pokemonDto) {
        return new PokemonDto.Builder()
                .name(pokemonDto.getName())
                .description(funtranslationsServiceRest.yodaTranslation(
                                new FunTranslationsRequestDto(pokemonDto.getDescription()))
                        .contents.getTranslated())
                .habitat(pokemonDto.getHabitat())
                .isLegendary(pokemonDto.isLegendary())
                .build();
    }

    public PokemonDto applyShakespeareTranslation(PokemonDto pokemonDto) {
        return new PokemonDto.Builder()
                .name(pokemonDto.getName())
                .description(funtranslationsServiceRest.shakespeareTranslation(
                                new FunTranslationsRequestDto(pokemonDto.getDescription()))
                        .contents.getTranslated())
                .habitat(pokemonDto.getHabitat())
                .isLegendary(pokemonDto.isLegendary())
                .build();
    }
}
