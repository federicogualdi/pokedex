package com.federicogualdi.pokemon.pokedex.api.rest;

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
    @Path("/shakespeare.json")
    @Produces(MediaType.APPLICATION_JSON)
    String shakespeareTranslation(@QueryParam("text") String text);

    @POST
    @Path("/yoda.json")
    @Produces(MediaType.APPLICATION_JSON)
    String yodaTranslation(@QueryParam("text") String text);
}
