package com.federicogualdi.pokemon.pokedex.rest.em;


import javax.ws.rs.BadRequestException;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;

@Provider
@Produces(MediaType.APPLICATION_JSON)
public class BadRequestExceptionMapper extends BaseExceptionMapper
        implements ExceptionMapper<BadRequestException> {

    @Override
    public Response toResponse(BadRequestException exception) {
        return formatResponse(ErrorCollection.BAD_REQUEST_EXCEPTION, exception.getMessage());
    }
}
