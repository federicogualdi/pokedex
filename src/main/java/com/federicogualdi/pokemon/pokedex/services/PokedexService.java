package com.federicogualdi.pokemon.pokedex.services;

import com.federicogualdi.pokemon.pokedex.api.rest.PokeApiServiceRest;
import com.federicogualdi.pokemon.pokedex.api.rest.converter.PokemonConverter;
import com.federicogualdi.pokemon.pokedex.messages.rest.dto.PokeApiPokemonDto;
import com.federicogualdi.pokemon.pokedex.messages.rest.dto.PokemonDto;
import org.eclipse.microprofile.rest.client.inject.RestClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.ws.rs.WebApplicationException;

@ApplicationScoped
public class PokedexService {

    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    @Inject
    @RestClient
    PokeApiServiceRest pokeApiServiceRest;

    @Inject
    PokemonConverter pokemonConverter;

    public PokemonDto getByName(String pokemonName) {
        var pokemon = pokemonConverter.fromPokeAPi(getPokeApiPokemon(pokemonName));
        logger.debug("Returned {} as '{}'", pokemon, pokemonName);
        return pokemon;
    }

    public PokemonDto getByNameWithTranslatedDescription(String pokemonName) {
        var pokemonDto = getByName(pokemonName);

        try {

            if ("cave".equals(pokemonDto.habitat) || pokemonDto.isLegendary) {
                var pokemonYodaTranslated = pokemonConverter.toYodaTranslation(pokemonDto);
                logger.debug("Returned {} as Yoda-Translation of '{}'", pokemonYodaTranslated, pokemonName);
                return pokemonYodaTranslated;
            }
            var pokemonShakespeareTranslated = pokemonConverter.toShakespeareTranslation(pokemonDto);
            logger.debug("Returned {} as Shakespeare-Translation of '{}'", pokemonShakespeareTranslated, pokemonName);
            return pokemonConverter.toShakespeareTranslation(pokemonDto);

        } catch (WebApplicationException webApplicationException) {

            logger.error("Unable to find Translation for '{}', falling back with {}: {}", pokemonName, pokemonDto, webApplicationException.getMessage(), webApplicationException);
            return pokemonDto;

        }
    }

    private PokeApiPokemonDto getPokeApiPokemon(String pokemonName) {
        var pokemonPokeApi = this.pokeApiServiceRest.getPokemonSpecies(pokemonName.toLowerCase());
        logger.debug("Received pokemon {} from PokeApi", pokemonPokeApi);
        return pokemonPokeApi;
    }
}
