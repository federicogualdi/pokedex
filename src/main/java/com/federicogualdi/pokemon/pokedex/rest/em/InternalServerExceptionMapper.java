package com.federicogualdi.pokemon.pokedex.rest.em;

import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;

@Provider
@Produces(MediaType.APPLICATION_JSON)
public class InternalServerExceptionMapper extends BaseExceptionMapper implements ExceptionMapper<Exception> {

    @Override
    public Response toResponse(Exception exception) {
        return formatResponse(ErrorCollection.INTERNAL_SERVER_ERROR_EXCEPTION, exception.getMessage());
    }

}