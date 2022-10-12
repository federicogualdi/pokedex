package com.federicogualdi.pokemon.pokedex.services;

import com.federicogualdi.pokemon.pokedex.api.rest.FuntranslationsServiceRest;
import com.federicogualdi.pokemon.pokedex.api.rest.PokeApiServiceRest;
import com.federicogualdi.pokemon.pokedex.api.rest.converter.PokemonConverter;
import com.federicogualdi.pokemon.pokedex.messages.rest.dto.PokemonDto;
import org.eclipse.microprofile.rest.client.inject.RestClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;

@ApplicationScoped
public class PokedexService {

    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    @Inject
    @RestClient
    PokeApiServiceRest pokeApiServiceRest;

    @Inject
    @RestClient
    FuntranslationsServiceRest translatorService;

    @Inject
    PokemonConverter pokemonConverter;

    public PokemonDto getByName(String pokemonName) {
        var pokemonPokeApi = this.pokeApiServiceRest.getPokemonSpecies(pokemonName);
        logger.debug("Received pokemon {} from PokeApi", pokemonPokeApi);
        return pokemonConverter.fromPokeAPi(pokemonPokeApi);
    }
}
