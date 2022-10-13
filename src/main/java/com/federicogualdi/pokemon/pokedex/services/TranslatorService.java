package com.federicogualdi.pokemon.pokedex.services;

import com.federicogualdi.pokemon.pokedex.dto.FunTranslationsRequestDto;
import com.federicogualdi.pokemon.pokedex.dto.PokemonDto;
import com.federicogualdi.pokemon.pokedex.rest.FuntranslationsServiceRest;
import org.eclipse.microprofile.rest.client.inject.RestClient;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;

@ApplicationScoped
public class TranslatorService {

    @Inject
    @RestClient
    FuntranslationsServiceRest funtranslationsServiceRest;

    public PokemonDto applyYodaTranslation(PokemonDto pokemonDto) {
        pokemonDto.description = funtranslationsServiceRest.yodaTranslation(new FunTranslationsRequestDto(pokemonDto.description)).contents.translated;
        return pokemonDto;
    }

    public PokemonDto applyShakespeareTranslation(PokemonDto pokemonDto) {
        pokemonDto.description = funtranslationsServiceRest.shakespeareTranslation(new FunTranslationsRequestDto(pokemonDto.description)).contents.translated;
        return pokemonDto;
    }
}