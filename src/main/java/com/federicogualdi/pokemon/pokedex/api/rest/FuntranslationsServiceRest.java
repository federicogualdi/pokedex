package com.federicogualdi.pokemon.pokedex.api.rest;

import com.federicogualdi.pokemon.pokedex.messages.rest.dto.FunTranslationsDto;
import com.federicogualdi.pokemon.pokedex.messages.rest.dto.FunTranslationsRequestDto;
import org.eclipse.microprofile.rest.client.inject.RegisterRestClient;

import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;

@Path("/translate")
@RegisterRestClient
public interface FuntranslationsServiceRest {

    @POST
    @Path("/shakespeare")
    @Produces(MediaType.APPLICATION_JSON)
    FunTranslationsDto shakespeareTranslation(FunTranslationsRequestDto req);

    @POST
    @Path("/yoda")
    @Produces(MediaType.APPLICATION_JSON)
    FunTranslationsDto yodaTranslation(FunTranslationsRequestDto req);
}
