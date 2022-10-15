package com.federicogualdi.pokemon.pokedex.rest.em;

import javax.ws.rs.Produces;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;

@Provider
@Produces(MediaType.APPLICATION_JSON)
public class RestClientExceptionMapper extends BaseExceptionMapper implements ExceptionMapper<WebApplicationException> {

    @Override
    public Response toResponse(WebApplicationException exception) {
        return formatResponse(ErrorCollection.CLIENT_REST_ERROR_EXCEPTION, exception.getMessage());
    }

}