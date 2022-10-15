package com.federicogualdi.pokemon.pokedex.rest;

import com.federicogualdi.pokemon.pokedex.rest.dto.ErrorDto;
import com.federicogualdi.pokemon.pokedex.rest.dto.PokemonDto;
import com.federicogualdi.pokemon.pokedex.services.PokedexService;
import org.eclipse.microprofile.openapi.annotations.Operation;
import org.eclipse.microprofile.openapi.annotations.media.Content;
import org.eclipse.microprofile.openapi.annotations.media.Schema;
import org.eclipse.microprofile.openapi.annotations.responses.APIResponse;
import org.eclipse.microprofile.openapi.annotations.responses.APIResponses;
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
    @Operation(summary = "Get pokemon by name.")
    @APIResponses(value = {
            @APIResponse(responseCode = "200", description = "Containing the response.", content = @Content(mediaType = MediaType.APPLICATION_JSON, schema = @Schema(implementation = PokemonDto.class))),
            @APIResponse(responseCode = "400", description = "Bad Request.", content = @Content(mediaType = MediaType.APPLICATION_JSON, schema = @Schema(implementation = ErrorDto.class))),
            @APIResponse(responseCode = "404", description = "A pokemon with the given NAME hasn't been found.", content = @Content(mediaType = MediaType.APPLICATION_JSON, schema = @Schema(implementation = ErrorDto.class))),
            @APIResponse(responseCode = "500", description = "Unexpected error.", content = @Content(mediaType = MediaType.APPLICATION_JSON, schema = @Schema(implementation = ErrorDto.class))),
            @APIResponse(responseCode = "503", description = "Unhandled errors from third-party services.", content = @Content(mediaType = MediaType.APPLICATION_JSON, schema = @Schema(implementation = ErrorDto.class)))
    })
    public PokemonDto getPokemonByName(@PathParam("name") String pokemonName) {
        logger.trace("Received request to get pokemon: {}", pokemonName);
        return pokedexService.getByName(pokemonName);
    }

    @GET
    @Path("translated/{name}")
    @Operation(summary = "Get pokemon by name changing its description to a funny one.")
    @APIResponses(value = {
            @APIResponse(responseCode = "200", description = "Containing the response.", content = @Content(mediaType = MediaType.APPLICATION_JSON, schema = @Schema(implementation = PokemonDto.class))),
            @APIResponse(responseCode = "400", description = "Bad Request.", content = @Content(mediaType = MediaType.APPLICATION_JSON, schema = @Schema(implementation = ErrorDto.class))),
            @APIResponse(responseCode = "404", description = "A pokemon with the given NAME hasn't been found.", content = @Content(mediaType = MediaType.APPLICATION_JSON, schema = @Schema(implementation = ErrorDto.class))),
            @APIResponse(responseCode = "500", description = "Unexpected error.", content = @Content(mediaType = MediaType.APPLICATION_JSON, schema = @Schema(implementation = ErrorDto.class))),
            @APIResponse(responseCode = "503", description = "Unhandled errors from third-party services.", content = @Content(mediaType = MediaType.APPLICATION_JSON, schema = @Schema(implementation = ErrorDto.class)))
    })
    public PokemonDto getPokemonByNameWithTranslatedDescription(@PathParam("name") String pokemonName) {
        logger.trace("Received request to get with translated description pokemon: {}", pokemonName);
        return pokedexService.getByNameWithTranslatedDescription(pokemonName);
    }
}
