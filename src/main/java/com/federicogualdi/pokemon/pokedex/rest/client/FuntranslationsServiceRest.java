package com.federicogualdi.pokemon.pokedex.rest.client;

import com.federicogualdi.pokemon.pokedex.rest.dto.FunTranslationsDto;
import com.federicogualdi.pokemon.pokedex.rest.dto.FunTranslationsRequestDto;
import com.federicogualdi.pokemon.pokedex.rest.em.RestClientProviderMapper;
import org.eclipse.microprofile.rest.client.annotation.RegisterProvider;
import org.eclipse.microprofile.rest.client.inject.RegisterRestClient;

import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

@Path("/translate")
@RegisterRestClient
@RegisterProvider(value = RestClientProviderMapper.class)
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
