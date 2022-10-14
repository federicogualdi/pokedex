package com.federicogualdi.pokemon.pokedex.services;

import com.federicogualdi.pokemon.pokedex.converter.PokemonConverter;
import com.federicogualdi.pokemon.pokedex.enums.Habitat;
import com.federicogualdi.pokemon.pokedex.rest.PokeApiServiceRest;
import com.federicogualdi.pokemon.pokedex.rest.dto.PokeApiPokemonDto;
import com.federicogualdi.pokemon.pokedex.rest.dto.PokemonDto;
import org.apache.commons.lang3.StringUtils;
import org.eclipse.microprofile.rest.client.inject.RestClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.ws.rs.BadRequestException;
import javax.ws.rs.NotFoundException;
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

        } catch (WebApplicationException e) {

            switch (e.getResponse().getStatus()) {
                case 429:
                    logger.warn("FunTranslations rate limited occurred for '{}', falling back with {}: {}", pokemonName, pokemonDto, e.getMessage());
                    break;
                default:
                    logger.error("Unable to find Translation for '{}', falling back with {}: {}", pokemonName, pokemonDto, e.getMessage(), e);
                    break;
            }

            return pokemonDto;
        }
    }

    private PokeApiPokemonDto getPokeApiPokemon(String pokemonName) {
        String pokemonNameEdited = pokemonName.toLowerCase().trim();
        if (StringUtils.isBlank(pokemonNameEdited)) throw new BadRequestException("Pokemon Name can not be blank");

        try {
            return this.pokeApiServiceRest.getPokemonSpecies(pokemonNameEdited);
        } catch (WebApplicationException e) {
            switch (e.getResponse().getStatus()) {
                case 404:
                    throw new NotFoundException();
                default:
                    //throw new BadRequestException(e.getMessage());
                    throw e;
            }
        }
    }

    private static boolean neededYodaTranslation(PokemonDto pokemonDto) {
        return Habitat.CAVE.value().equals(pokemonDto.habitat) || pokemonDto.isLegendary;
    }
}
