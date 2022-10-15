package com.federicogualdi.pokemon.pokedex.rest.em;

import org.eclipse.microprofile.rest.client.ext.ResponseExceptionMapper;

import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.Response;

public class RestClientProviderMapper implements ResponseExceptionMapper<WebApplicationException> {

    @Override
    public WebApplicationException toThrowable(Response response) {
        return new WebApplicationException(response.getStatus());
    }
}
