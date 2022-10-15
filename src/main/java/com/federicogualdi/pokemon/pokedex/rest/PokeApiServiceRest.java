package com.federicogualdi.pokemon.pokedex.rest;

import com.federicogualdi.pokemon.pokedex.rest.dto.PokeApiPokemonDto;
import com.federicogualdi.pokemon.pokedex.rest.em.RestClientProviderMapper;
import org.eclipse.microprofile.rest.client.annotation.RegisterProvider;
import org.eclipse.microprofile.rest.client.inject.RegisterRestClient;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

@Path("/v2")
@RegisterRestClient
@RegisterProvider(value = RestClientProviderMapper.class)
public interface PokeApiServiceRest {

    @GET
    @Path("/pokemon-species/{name}/")
    @Produces(MediaType.APPLICATION_JSON)
    PokeApiPokemonDto getPokemonSpecies(@PathParam("name") String name);
}
