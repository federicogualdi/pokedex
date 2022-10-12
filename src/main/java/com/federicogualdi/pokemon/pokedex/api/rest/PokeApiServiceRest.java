package com.federicogualdi.pokemon.pokedex.api.rest;

import com.federicogualdi.pokemon.pokedex.messages.rest.dto.PokeApiPokemonDto;
import com.federicogualdi.pokemon.pokedex.messages.rest.dto.PokemonDto;
import org.eclipse.microprofile.rest.client.inject.RegisterRestClient;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;

@Path("/v2")
@RegisterRestClient
public interface PokeApiServiceRest {

    @GET
    @Path("/pokemon-species/{name}/")
    @Produces(MediaType.APPLICATION_JSON)
    PokeApiPokemonDto getPokemonSpecies(@PathParam("name") String name) throws WebApplicationException;
}
