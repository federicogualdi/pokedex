package com.federicogualdi.pokemon.pokedex.rest.em;

import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.util.Objects;

public class BaseExceptionMapper {

    protected Response formatResponse(ErrorCollection errorType, String message) {
        if (Objects.nonNull(message)) {
            errorType.getError().setDetail(message);
        }
        var status = errorType.getError().getStatus();

        var error = errorType.getError();

        return Response.status(status).entity(error).type(MediaType.APPLICATION_JSON).build();
    }
}
