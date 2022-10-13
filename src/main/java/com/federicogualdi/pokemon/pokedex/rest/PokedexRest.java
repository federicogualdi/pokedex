package com.federicogualdi.pokemon.pokedex.rest;

import com.federicogualdi.pokemon.pokedex.dto.PokemonDto;
import com.federicogualdi.pokemon.pokedex.services.PokedexService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.inject.Inject;
import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;

@Path("/api/v1/pokemon")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class PokedexRest {

    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    @Inject
    PokedexService pokedexService;

    @GET
    @Path("/{name}")
    public PokemonDto getPokemonByName(@PathParam("name") String pokemonName) {
        logger.trace("Received request to get pokemon: {}", pokemonName);
        return pokedexService.getByName(pokemonName);
    }

    @GET
    @Path("translated/{name}")
    public PokemonDto getPokemonByNameWithTranslatedDescription(@PathParam("name") String pokemonName) {
        logger.trace("Received request to get with translated description pokemon: {}", pokemonName);
        return pokedexService.getByNameWithTranslatedDescription(pokemonName);
    }
}
