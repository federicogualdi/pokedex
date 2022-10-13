package com.federicogualdi.pokemon.pokedex.services;

import com.federicogualdi.pokemon.pokedex.constant.Habitat;
import com.federicogualdi.pokemon.pokedex.converter.PokemonConverter;
import com.federicogualdi.pokemon.pokedex.dto.PokeApiPokemonDto;
import com.federicogualdi.pokemon.pokedex.dto.PokemonDto;
import com.federicogualdi.pokemon.pokedex.rest.PokeApiServiceRest;
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
        return pokemonConverter.from(getPokeApiPokemon(pokemonName));
    }

    public PokemonDto getByNameWithTranslatedDescription(String pokemonName) {
        var pokemonDto = getByName(pokemonName);

        try {

            return neededYodaTranslation(pokemonDto) ?
                    pokemonConverter.toYodaTranslation(pokemonDto) :
                    pokemonConverter.toShakespeareTranslation(pokemonDto);

        } catch (WebApplicationException webApplicationException) {

            logger.error("Unable to find Translation for '{}', falling back with {}: {}", pokemonName, pokemonDto, webApplicationException.getMessage(), webApplicationException);
            return pokemonDto;

        }
    }

    private PokeApiPokemonDto getPokeApiPokemon(String pokemonName) {
        return this.pokeApiServiceRest.getPokemonSpecies(pokemonName.toLowerCase().trim());
    }

    private static boolean neededYodaTranslation(PokemonDto pokemonDto) {
        return Habitat.CAVE.value().equals(pokemonDto.habitat) || pokemonDto.isLegendary;
    }
}
