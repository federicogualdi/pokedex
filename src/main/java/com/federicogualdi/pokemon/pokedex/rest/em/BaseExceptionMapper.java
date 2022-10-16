package com.federicogualdi.pokemon.pokedex.rest.em;

import com.federicogualdi.pokemon.pokedex.rest.dto.ErrorDto;

import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.util.Objects;

public class BaseExceptionMapper {

    protected Response formatResponse(ErrorCollection errorType, String message) {
        ErrorDto.Builder builder = new ErrorDto.Builder();
        if (Objects.nonNull(message)) {
            builder.detail(message);
        }
        var error = builder.title(errorType.getError().getTitle()).status(errorType.getError().getStatus()).build();

        return Response.status(error.getStatus()).entity(error).type(MediaType.APPLICATION_JSON).build();
    }
}
