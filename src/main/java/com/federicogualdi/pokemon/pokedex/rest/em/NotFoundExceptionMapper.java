package com.federicogualdi.pokemon.pokedex.rest.em;


import javax.ws.rs.NotFoundException;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;

@Provider
@Produces(MediaType.APPLICATION_JSON)
public class NotFoundExceptionMapper extends BaseExceptionMapper
        implements ExceptionMapper<NotFoundException> {

    @Override
    public Response toResponse(NotFoundException exception) {
        return formatResponse(ErrorCollection.NOT_FOUND_EXCEPTION, exception.getMessage());
    }
}
