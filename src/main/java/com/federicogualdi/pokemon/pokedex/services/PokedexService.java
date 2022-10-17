package com.federicogualdi.pokemon.pokedex.services;

import com.federicogualdi.pokemon.pokedex.converter.PokemonConverter;
import com.federicogualdi.pokemon.pokedex.enums.Habitat;
import com.federicogualdi.pokemon.pokedex.rest.client.PokeApiServiceRest;
import com.federicogualdi.pokemon.pokedex.rest.dto.PokemonDto;
import io.quarkus.cache.CacheResult;
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

    @CacheResult(cacheName = "pokemon-cache")
    public PokemonDto getByName(String pokemonName) {
        String pokemonNameEdited = pokemonName.toLowerCase().trim();
        if (StringUtils.isBlank(pokemonNameEdited)) throw new BadRequestException("Pokemon name can not be blank");

        try {

            return pokemonConverter.from(pokeApiServiceRest.getPokemonSpecies(pokemonNameEdited));

        } catch (WebApplicationException e) {
            if (e.getResponse().getStatus() == 404) {
                throw new NotFoundException(String.format("Pokemon '%s' was not found on PokeApi", pokemonNameEdited));
            }
            throw e;
        }
    }

    public PokemonDto getByNameWithTranslatedDescription(String pokemonName) {

        try {

            return getTranslatedPokemon(pokemonName);

        } catch (WebApplicationException e) {

            switch (e.getResponse().getStatus()) {
                case 400:
                case 404:
                    throw e;
                case 429:
                    logger.warn("FunTranslations rate limited occurred for '{}', falling back with untranslated one: {}", pokemonName, e.getMessage());
                    break;
                default:
                    logger.error("Unable to find Translation for '{}', falling back with untranslated one: {}", pokemonName, e.getMessage(), e);
                    break;
            }

            return PokemonDto.clone(getByName(pokemonName));
        }
    }

    @CacheResult(cacheName = "funny-pokemon-cache")
    public PokemonDto getTranslatedPokemon(String pokemonName) {
        var pokemonDto = PokemonDto.clone(getByName(pokemonName));
        return neededYodaTranslation(pokemonDto) ?
                pokemonConverter.toYodaTranslation(pokemonDto) :
                pokemonConverter.toShakespeareTranslation(pokemonDto);
    }

    private boolean neededYodaTranslation(PokemonDto pokemonDto) {
        return Habitat.CAVE.value().equals(pokemonDto.getHabitat()) || pokemonDto.isLegendary();
    }
}
