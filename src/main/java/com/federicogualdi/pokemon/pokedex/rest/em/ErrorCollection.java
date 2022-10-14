package com.federicogualdi.pokemon.pokedex.rest.em;

import com.federicogualdi.pokemon.pokedex.rest.dto.ErrorDto;

import javax.ws.rs.core.Response.Status;

public enum ErrorCollection {
    NOT_FOUND_EXCEPTION(new ErrorDto()
            .title("Pokemon not found")
            .status(Status.NOT_FOUND.getStatusCode())),
    BAD_REQUEST_EXCEPTION(new ErrorDto()
            .title("Bad request")
            .status(Status.BAD_REQUEST.getStatusCode())),
    CLIENT_REST_ERROR_EXCEPTION(new ErrorDto()
            .title("Client Rest Server Error")
            .status(Status.SERVICE_UNAVAILABLE.getStatusCode())),
    INTERNAL_SERVER_ERROR_EXCEPTION(new ErrorDto()
            .title("Internal Server Error")
            .status(Status.INTERNAL_SERVER_ERROR.getStatusCode())),
    ;

    private final ErrorDto error;

    public ErrorDto getError() {
        return error;
    }

    ErrorCollection(final ErrorDto error) {
        this.error = error;
    }
}
